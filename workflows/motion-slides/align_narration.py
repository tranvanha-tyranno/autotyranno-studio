"""Local ASR timestamps mapped back onto the approved script (no new TTS calls)."""
from __future__ import annotations
import argparse
import difflib
import json
import math
import re
from pathlib import Path
import numpy as np


def normalized(word):
    return re.sub(r"[^\w]", "", word.casefold())


def align(script, words, duration):
    original = script.split()
    tokens = [normalized(w) for w in original]
    recognized = [normalized(w["word"]) for w in words]
    matcher = difflib.SequenceMatcher(None, tokens, recognized, autojunk=False)
    anchors = {}
    for block in matcher.get_matching_blocks():
        for offset in range(block.size):
            anchors[block.a+offset] = words[block.b+offset]["start"]
    # Keep approved spelling and facts; ASR is only a timing aid.
    anchors.setdefault(0, .35)
    anchors[len(original)] = min(duration-.3, words[-1]["end"] if words else duration-.5)
    indexes = sorted(anchors)
    times = np.interp(np.arange(len(original)+1), indexes, [anchors[x] for x in indexes])
    times = np.maximum.accumulate(times)
    cues = []
    sentence_start = 0
    for i, word in enumerate(original):
        if not (word.endswith((".", "!", "?", ":", ";")) or i == len(original)-1):
            continue
        count=i+1-sentence_start
        parts=math.ceil(count/16)
        # Balance long sentences rather than leaving a tiny trailing fragment.
        for part in range(parts):
            start=sentence_start+round(count*part/parts)
            end=sentence_start+round(count*(part+1)/parts)
            cues.append({"start":round(float(times[start]),3),
                         "end":round(max(float(times[end]),float(times[start])+.25),3),
                         "text":" ".join(original[start:end]),
                         "words":[{"text":original[k],"start":round(float(times[k]),3)}
                                  for k in range(start,end)]})
        sentence_start=i+1
    return cues, round((len(anchors)-1)/max(1,len(original)),3)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--source",type=Path,required=True)
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    from faster_whisper import WhisperModel
    model=None
    scenes=json.loads((args.source/"timed-scenes.json").read_text(encoding="utf-8"))
    args.output.mkdir(parents=True,exist_ok=True)
    all_cues=[]
    for i,scene in enumerate(scenes):
        cache=args.output/f"asr-{i+1:02}.json"
        if cache.exists():
            words=json.loads(cache.read_text(encoding="utf-8"))
        else:
            if model is None:
                model=WhisperModel("base",device="cpu",compute_type="int8",cpu_threads=6)
            segments,_=model.transcribe(
                str(args.source/f"clip-{i+1:02}-scene-{i+1:02}"/"voice-timed.wav"),
                language="vi",word_timestamps=True,beam_size=5,vad_filter=True,
                initial_prompt="SQL, SELECT, FROM, WHERE, ORDER BY, LIMIT, OFFSET, App, Web, id, wait_min.")
            words=[{"word":w.word.strip(),"start":w.start,"end":w.end}
                   for seg in segments for w in seg.words or []]
            cache.write_text(json.dumps(words,ensure_ascii=False,indent=2),encoding="utf-8")
        cues,matched=align(scene["dialogue"],words,scene["duration_seconds"])
        all_cues.append({"scene":i+1,"method":"local Whisper base word timing + exact script matching/interpolation",
                         "matched_fraction":matched,"cues":cues})
        print("ALIGNED",i+1,"matched",matched,flush=True)
    (args.output/"captions.json").write_text(json.dumps(all_cues,ensure_ascii=False,indent=2),encoding="utf-8")


if __name__=="__main__":
    main()
