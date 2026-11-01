"""Build three local 6-second previews after Muse returned a 502/text-only error."""
from __future__ import annotations

import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import imageio_ffmpeg
import requests

from importlib.util import spec_from_file_location, module_from_spec

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "videos" / "2026-10-28-inox-kettle-3clips"
FF = imageio_ffmpeg.get_ffmpeg_exe()
runner_spec = spec_from_file_location("local_runner", ROOT / "workflows/product-video/run.py")
runner = module_from_spec(runner_spec)
assert runner_spec.loader is not None
runner_spec.loader.exec_module(runner)

REFS = [
    (r"C:\Users\tyranno\AppData\Local\Temp\codex-clipboard-13b8ac5a-88ef-474d-a22e-b1f51459f3bb.png", "01-01-factory-forward", "Ấm inox cao cấp 1,8 lít", "[excited] Ê ê ê! Ấm inox 1,8 lít, đun sôi nhanh và tự ngắt điện khi nước sôi nè!", "forward"),
    (r"C:\Users\tyranno\AppData\Local\Temp\codex-clipboard-60c4dd6f-e070-4bf6-a1c6-7058d413d711.png", "02-02-mall-sidewalk", "Ấm inox cao cấp 1,8 lít", "[playful] Các dợ nhìn nè! Vòi rót gọn, tay cầm cách nhiệt, đế xoay 360 độ luôn á!", "side"),
    (r"C:\Users\tyranno\AppData\Local\Temp\codex-clipboard-bf6674cd-0a5f-4f9e-b029-834f3a8fd341.png", "03-03-appliance-shelf", "Ấm inox cao cấp 1,8 lít", "[amazed] Inox sáng bóng, nắp mở tiện, dung tích 1,8 lít; mấy ní thấy hợp thì chốt nha!", "shelf"),
]


def duration(path: Path) -> float:
    result = subprocess.run([FF, "-hide_banner", "-i", str(path)], capture_output=True, text=True, encoding="utf-8", errors="replace")
    match = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", result.stderr)
    if not match:
        raise RuntimeError(f"Cannot measure {path}")
    return int(match[1]) * 3600 + int(match[2]) * 60 + float(match[3])


def tts(text: str, target: Path) -> bool:
    if target.exists():
        return False
    key = runner.eleven_key()
    result = requests.post(
        "https://api.elevenlabs.io/v1/text-to-speech/pNInz6obpgDQGcFmaJgB",
        params={"output_format": "mp3_44100_128"},
        headers={"xi-api-key": key, "Accept": "audio/mpeg"},
        json={"text": text, "model_id": "eleven_v3", "language_code": "vi", "voice_settings": {"stability": 0.5}},
        timeout=180,
    )
    if result.status_code != 200:
        raise RuntimeError(f"ElevenLabs HTTP {result.status_code}: {result.text[:300]}")
    target.write_bytes(result.content)
    return True


def local_video(source: Path, voice: Path, target: Path, variant: str) -> None:
    voice_seconds = duration(voice)
    tempo = max(1.0, voice_seconds / 5.8)
    if tempo > 1.25:
        raise RuntimeError(f"Voice is too long for six seconds ({voice_seconds:.2f}s)")
    if variant == "side":
        x = "iw/2-(iw/zoom/2)+sin(on/28)*18"
        y = "ih/2-(ih/zoom/2)"
    elif variant == "shelf":
        x = "iw/2-(iw/zoom/2)-sin(on/31)*12"
        y = "ih/2-(ih/zoom/2)+sin(on/37)*10"
    else:
        x = "iw/2-(iw/zoom/2)"
        y = "ih/2-(ih/zoom/2)-sin(on/32)*9"
    filters = (
        "[0:v]scale=900:1600:force_original_aspect_ratio=increase,"
        f"zoompan=z='min(zoom+0.0007,1.12)':x='{x}':y='{y}':d=1:s=720x1280:fps=30,setsar=1[v];"
        f"[1:a]atempo={tempo:.8f},apad,atrim=duration=6[a]"
    )
    result = subprocess.run(
        [FF, "-y", "-loop", "1", "-i", str(source), "-i", str(voice), "-filter_complex", filters, "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-t", "6", "-movflags", "+faststart", str(target)],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    if result.returncode:
        raise RuntimeError(result.stderr[-1200:])
    subprocess.run([FF, "-v", "error", "-i", str(target), "-f", "null", "-"], capture_output=True, check=True)


def main() -> None:
    manifest = {
        "profile": "mica-uploaded-images-fast-v1-local-fallback",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source": "Muse upstream returned 502/text-only error; no retry issued",
        "outputs": [],
        "provider_calls": {"muse_videos": 0, "elevenlabs_tts": 0},
    }
    for index, (source, slug, product, dialogue, variant) in enumerate(REFS, 1):
        directory = OUT / slug
        directory.mkdir(parents=True, exist_ok=True)
        input_path = directory / "input.png"
        if not input_path.exists():
            input_path.write_bytes(Path(source).read_bytes())
        (directory / "dialogue.txt").write_text(dialogue, encoding="utf-8")
        (directory / "fallback-note.txt").write_text(
            "Muse upstream returned a 502/text-only error. This final keeps the supplied image exact and uses local FFmpeg camera push/pan; it does not physically animate the hand or kettle.",
            encoding="utf-8",
        )
        voice = directory / "voice.mp3"
        if tts(dialogue, voice):
            manifest["provider_calls"]["elevenlabs_tts"] += 1
        final = directory / "final.mp4"
        local_video(input_path, voice, final, variant)
        subprocess.run([FF, "-y", "-i", str(final), "-vf", "fps=1,scale=180:320,tile=3x2", "-frames:v", "1", str(directory / "contact-sheet.jpg")], capture_output=True, check=True)
        report = {
            "index": index,
            "slug": slug,
            "product": product,
            "seconds": duration(final),
            "resolution": "720x1280",
            "fps": 30,
            "visual_method": "exact supplied still + local FFmpeg zoompan/pan",
            "voice": "Adam eleven_v3",
            "decode": "passed",
            "muse_media": "not generated: upstream 502/text-only error; no retry issued",
            "claims": "Only dialogue claims visible in source image were used.",
            "physical_motion": "not represented; camera push/pan only",
        }
        (directory / "verification.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        manifest["outputs"].append({"index": index, "slug": slug, "product": product, "path": str(final), "source": source})
        print("READY", final, flush=True)
    (OUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
