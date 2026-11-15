"""Resumable local ASR diagnostics, one exact-mix chapter at a time.

No network downloads or generation providers. The base model must already exist
in the local faster-whisper cache. ASR output is not a claim of manual listening,
an authoritative transcript, or proof that a flagged omission actually occurred.
The chapter boundary and audio hashes prevent reuse of stale recognition caches.
"""
from __future__ import annotations

import argparse
import difflib
import gc
import hashlib
import importlib.metadata
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import time
import unicodedata
import wave

# Set these before importing any inference/numerical runtime. This does not cap
# total process RAM; chapter-sized inputs avoid decoding the entire mix at once.
for _name in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS",
              "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_name] = "2"

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_BATCH = ROOT / "videos/2026-11-14-o-banh-mi-va-lam-phat"
MODEL = "base"
NORMALIZER_VERSION = "vi-number-words/1"
PARAMETERS = {
    "model": MODEL, "device": "cpu", "compute_type": "int8",
    "cpu_threads": 2, "num_workers": 1, "local_files_only": True,
    "language": "vi", "beam_size": 1, "best_of": 1,
    "word_timestamps": False, "condition_on_previous_text": False,
    "vad_filter": False, "temperature": 0,
    "sample_rate": 16000, "channels": 1, "sample_width_bytes": 2,
    "normalizer": NORMALIZER_VERSION,
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")
    temporary.replace(path)


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def signature(value) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                    separators=(",", ":")).encode("utf-8")).hexdigest()


def runtime_versions():
    versions = {}
    for package in ("faster-whisper", "ctranslate2"):
        try:
            versions[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            versions[package] = "not-installed"
    return versions


_DIGITS = ("không", "một", "hai", "ba", "bốn", "năm", "sáu", "bảy", "tám", "chín")


def _under_thousand(n: int, padded=False) -> list[str]:
    out = []
    hundreds, rest = divmod(n, 100)
    tens, ones = divmod(rest, 10)
    if hundreds or padded:
        out += [_DIGITS[hundreds], "trăm"]
    if tens > 1:
        out += [_DIGITS[tens], "mươi"]
    elif tens == 1:
        out += ["mười"]
    elif ones and (hundreds or padded):
        out += ["linh"]
    if ones:
        out += [_DIGITS[ones]]
    return out


def integer_words(n: int) -> list[str]:
    if not n:
        return ["không"]
    if n < 0:
        return ["âm"] + integer_words(-n)
    if n >= 10**12:
        return [_DIGITS[int(digit)] for digit in str(n)]
    groups = []
    while n:
        n, part = divmod(n, 1000)
        groups.append(part)
    names = ("", "nghìn", "triệu", "tỷ")
    out = []
    for index in reversed(range(len(groups))):
        part = groups[index]
        if part:
            out += _under_thousand(part)
            if names[index]:
                out += [names[index]]
    return out


def _numeric_words(match: re.Match) -> str:
    token = match.group(0).replace("−", "-")
    prefix = []
    if token.startswith(("-", "+")):
        if token[0] == "-":
            prefix = ["âm"]
        token = token[1:]
    # Vietnamese grouping such as 22.440; accept English grouping 22,440 too.
    # Mixed separators use the final separator as decimal, unless all groups
    # have three digits. Ambiguous ASR punctuation remains diagnostic only.
    groups = re.split(r"[.,]", token)
    if len(groups) > 1 and all(len(g) == 3 for g in groups[1:]):
        words = integer_words(int("".join(groups)))
    elif len(groups) > 1:
        words = integer_words(int("".join(groups[:-1]) or "0"))
        words += ["phẩy"] + [_DIGITS[int(d)] for d in groups[-1]]
    else:
        words = integer_words(int(token))
    return " " + " ".join(prefix + words) + " "


def normalized_tokens(text: str) -> list[str]:
    text = unicodedata.normalize("NFKC", text).casefold()
    text = re.sub(r"(?<!\w)[+\-−]?\d+(?:[.,]\d+)*", _numeric_words, text)
    text = text.replace("%", " phần trăm ")
    tokens = re.findall(r"[^\W\d_]+", text, flags=re.UNICODE)
    aliases = {"ngàn": "nghìn", "lẻ": "linh", "mốt": "một", "tư": "bốn", "lăm": "năm"}
    return [aliases.get(word, word) for word in tokens]


def diagnostics(expected: str, observed: str):
    a, b = normalized_tokens(expected), normalized_tokens(observed)
    matcher = difflib.SequenceMatcher(None, a, b, autojunk=False)
    blocks = matcher.get_matching_blocks()
    matched = sum(block.size for block in blocks)
    coverage = matched / max(1, len(a))
    tail_start = max(0, len(a) - 25)
    tail_matched = sum(max(0, min(len(a), block.a + block.size) - max(tail_start, block.a))
                       for block in blocks)
    tail_coverage = tail_matched / max(1, len(a) - tail_start)
    gaps = []
    for tag, a1, a2, b1, b2 in matcher.get_opcodes():
        if tag in ("delete", "replace") and a2 - a1 >= 20:
            gaps.append({"expectedTokenStart": a1, "expectedTokenEnd": a2,
                         "expectedNormalizedText": " ".join(a[a1:a2]),
                         "observedNormalizedText": " ".join(b[b1:b2])})
    flags = []
    if coverage < .60:
        flags.append("low_expected_token_coverage")
    if len(b) < len(a) * .65:
        flags.append("recognition_much_shorter_than_expected")
    if gaps:
        flags.append("long_expected_span_without_close_match")
    if tail_coverage < .40:
        flags.append("weak_match_at_expected_chapter_tail")
    return {"tokenSimilarity": round(matcher.ratio(), 4),
            "expectedTokenCoverage": round(coverage, 4),
            "expectedTailTokenCoverage": round(tail_coverage, 4),
            "expectedTokens": len(a), "observedTokens": len(b),
            "diagnosticFlags": flags, "possibleOmissionSpans": gaps,
            "requiresHumanReview": bool(flags),
            "limit": "ASR errors, number formatting and paraphrases can trigger flags. A flag is not a confirmed omission."}


def resolve_ffmpeg(explicit: str | None) -> str:
    if explicit:
        found = shutil.which(explicit) or (str(Path(explicit).resolve()) if Path(explicit).is_file() else None)
        if not found:
            raise FileNotFoundError("Specified FFmpeg executable was not found")
        return found
    found = shutil.which("ffmpeg")
    if found:
        return found
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def chapter_bounds(plan, source: Path):
    fps = plan["fps"]
    with wave.open(str(source), "rb") as wav:
        sample_rate, sample_count = wav.getframerate(), wav.getnframes()
    chapters = plan["chapters"]
    if not chapters or chapters[0]["from"] != 0:
        raise ValueError("Chapter timeline must start at frame zero")
    rows = []
    for i, chapter in enumerate(chapters):
        begin = chapter["from"]
        end = chapters[i + 1]["from"] if i + 1 < len(chapters) else plan["durationFrames"]
        if begin < 0 or end <= begin:
            raise ValueError("Non-increasing chapter boundaries")
        start_sample, end_sample = round(begin * sample_rate / fps), round(end * sample_rate / fps)
        if end_sample > sample_count + 1:
            raise ValueError("Final mix is shorter than the chapter timeline")
        expected = " ".join(s["text"] for s in plan["segments"] if s["chapterId"] == chapter["id"])
        if not expected:
            raise ValueError("No expected narration for chapter " + chapter["id"])
        rows.append({"index": i, "chapter": chapter["id"], "startFrame": begin, "endFrameExclusive": end,
                     "startSample": start_sample, "endSampleExclusive": min(sample_count, end_sample),
                     "sourceSampleRate": sample_rate, "startSeconds": begin / fps,
                     "endSeconds": end / fps, "expected": expected})
    return rows


def prepare_chunk(row, source: Path, source_hash: str, directory: Path, ffmpeg: str):
    chunk_key = signature({"sourceSHA256": source_hash, "startSample": row["startSample"],
                           "endSample": row["endSampleExclusive"], "sourceRate": row["sourceSampleRate"],
                           "output": [16000, 1, "pcm_s16le"]})
    safe_id = re.sub(r"[^a-zA-Z0-9_-]", "-", row["chapter"])
    target = directory / f'{row["index"] + 1:02}-{safe_id}-{chunk_key[:16]}.wav'
    receipt = target.with_suffix(".json")
    if target.exists() and receipt.exists():
        previous = load(receipt)
        if previous.get("chunkKey") == chunk_key and previous.get("sha256") == sha(target):
            return target, previous
        raise ValueError("Cached chapter audio does not match its receipt")
    directory.mkdir(parents=True, exist_ok=True)
    partial = target.with_suffix(".partial.wav")
    command = [ffmpeg, "-y", "-v", "error", "-threads", "2", "-filter_threads", "2",
               "-i", str(source), "-map", "0:a:0", "-af",
               f'atrim=start_sample={row["startSample"]}:end_sample={row["endSampleExclusive"]},asetpts=PTS-STARTPTS',
               "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", str(partial)]
    result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, timeout=120)
    if result.returncode:
        raise RuntimeError("FFmpeg chapter split failed: " + result.stderr.decode(errors="replace")[-2500:])
    with wave.open(str(partial), "rb") as wav:
        samples = wav.getnframes()
        if (wav.getframerate(), wav.getnchannels(), wav.getsampwidth()) != (16000, 1, 2):
            raise ValueError("Expected 16 kHz mono signed 16-bit chapter WAV")
    expected_samples = (row["endSampleExclusive"] - row["startSample"]) * 16000 / row["sourceSampleRate"]
    if abs(samples - expected_samples) > 2:
        raise ValueError("Chapter resample length differs by more than two output samples")
    partial.replace(target)
    meta = {"chunkKey": chunk_key, "sha256": sha(target), "sourceSHA256": source_hash,
            "samples": samples, "sampleRate": 16000, "channels": 1, "sampleWidthBytes": 2,
            "sourceStartSample": row["startSample"], "sourceEndSampleExclusive": row["endSampleExclusive"],
            "sourceSampleRate": row["sourceSampleRate"], "seconds": samples / 16000,
            "boundaryScope": "Exact source-mix sample interval; resampled output may round by up to two samples."}
    save(receipt, meta)
    return target, meta


def verify(batch: Path, ffmpeg: str):
    source, plan_path = batch / "audio/final-mix.wav", batch / "plan.json"
    plan = load(plan_path)
    source_hash = sha(source)
    versions = runtime_versions()
    out = batch / "audio/asr-base-chapters"
    out.mkdir(parents=True, exist_ok=True)
    rows = chapter_bounds(plan, source)
    run_key = signature({"sourceSHA256": source_hash, "planSHA256": sha(plan_path),
                         "parameters": PARAMETERS, "versions": versions})
    progress_path, report_path = batch / "audio/asr-base-progress.json", batch / "audio/asr-base-review.json"
    started = time.perf_counter()
    model, completed = None, []
    progress = {"schema": "economy-story-asr-progress/1", "runKey": run_key,
                "sourceSHA256": source_hash, "parameters": PARAMETERS, "runtimeVersions": versions,
                "status": "running", "completedChapters": completed, "currentChapter": None,
                "scope": "Independent local ASR diagnostics; not manual listening or aesthetic approval."}
    save(progress_path, progress)
    try:
        for row in rows:
            progress["currentChapter"] = {"chapter": row["chapter"], "phase": "splitting", "partialSegments": []}
            save(progress_path, progress)
            chapter_file, chunk = prepare_chunk(row, source, source_hash, out / "chunks", ffmpeg)
            request = {"sourceSHA256": source_hash, "chapterAudioSHA256": chunk["sha256"],
                       "startFrame": row["startFrame"], "endFrameExclusive": row["endFrameExclusive"],
                       "expectedSHA256": signature(row["expected"]), "parameters": PARAMETERS,
                       "runtimeVersions": versions}
            request_hash = signature(request)
            cache = out / "cache" / (request_hash + ".json")
            if cache.exists():
                chapter = load(cache)
                if chapter.get("requestHash") != request_hash or chapter.get("request") != request:
                    raise ValueError("ASR cache request does not match its key")
                record = {**chapter, "cacheHit": True}
            else:
                if model is None:
                    progress["currentChapter"]["phase"] = "loading-local-base-model"
                    save(progress_path, progress)
                    from faster_whisper import WhisperModel
                    model = WhisperModel(MODEL, device="cpu", compute_type="int8", cpu_threads=2,
                                         num_workers=1, local_files_only=True)
                progress["currentChapter"]["phase"] = "recognizing"
                save(progress_path, progress)
                chapter_started = time.perf_counter()
                segments, info = model.transcribe(str(chapter_file), language="vi", beam_size=1,
                    best_of=1, word_timestamps=False, condition_on_previous_text=False,
                    vad_filter=False, temperature=0)
                observed_segments = []
                for segment in segments:
                    observed_segments.append({"start": segment.start, "end": segment.end, "text": segment.text,
                        "globalStart": row["startSeconds"] + segment.start,
                        "globalEnd": row["startSeconds"] + segment.end})
                    progress["currentChapter"]["partialSegments"] = observed_segments
                    progress["currentChapter"]["wallSeconds"] = round(time.perf_counter() - chapter_started, 3)
                    save(progress_path, progress)
                observed = " ".join(s["text"].strip() for s in observed_segments)
                record = {"schema": "economy-story-chapter-asr/1", "requestHash": request_hash,
                          "request": request, "chapter": row["chapter"], "expected": row["expected"],
                          "recognized": observed, "segments": observed_segments,
                          "language": info.language, "wallSeconds": round(time.perf_counter() - chapter_started, 3),
                          "chapterAudio": str(chapter_file.relative_to(batch)), "chunk": chunk,
                          "diagnostics": diagnostics(row["expected"], observed), "cacheHit": False}
                save(cache, record)
                del segments, info
            completed.append(record)
            progress["currentChapter"] = None
            progress["wallSeconds"] = round(time.perf_counter() - started, 3)
            save(progress_path, progress)
            print("ASR_CHAPTER", row["chapter"], record["diagnostics"]["tokenSimilarity"],
                  "cached" if record["cacheHit"] else "recognized", flush=True)
            gc.collect()
    except Exception as error:
        progress["status"] = "failed-resumable"
        progress["error"] = {"type": type(error).__name__, "message": str(error)}
        progress["wallSeconds"] = round(time.perf_counter() - started, 3)
        save(progress_path, progress)
        raise
    report = {"schema": "economy-story-asr-review/1", "runKey": run_key,
              "status": "complete-asr-diagnostics", "sourceSHA256": source_hash,
              "planSHA256": sha(plan_path), "parameters": PARAMETERS, "runtimeVersions": versions,
              "chapters": completed, "wallSeconds": round(time.perf_counter() - started, 3),
              "durationSeconds": plan["durationFrames"] / plan["fps"],
              "flaggedChapters": [c["chapter"] for c in completed if c["diagnostics"]["requiresHumanReview"]],
              "scope": "Every chapter of the exact final mix recognized independently with a local model. ASR can mishear names, numbers and words; flags require review and are not confirmed omissions.",
              "memoryScope": "One chapter WAV is decoded for inference at a time; one base model is retained. This is not a fixed total-RAM cap.",
              "continuousListening": False, "aestheticApproval": False, "userApproval": "pending"}
    save(report_path, report)
    progress["status"] = "complete"
    save(progress_path, progress)
    print("ASR_COMPLETE", len(completed), "chapters; flagged", report["flaggedChapters"], flush=True)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch", type=Path, default=DEFAULT_BATCH)
    parser.add_argument("--ffmpeg", help="Optional local FFmpeg executable; no downloads")
    args = parser.parse_args()
    verify(args.batch.resolve(), resolve_ffmpeg(args.ffmpeg))


if __name__ == "__main__":
    main()
