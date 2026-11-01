"""Retry three real Muse AI clips with concise prompts after an upstream 502."""
from __future__ import annotations

import base64
import json
import re
import shutil
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

import imageio_ffmpeg
import requests

from importlib.util import spec_from_file_location, module_from_spec

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "videos" / "2026-10-28-inox-kettle-3clips-ai"
BASE = "http://127.0.0.1:18610"
FF = imageio_ffmpeg.get_ffmpeg_exe()
spec = spec_from_file_location("runner", ROOT / "workflows/product-video/run.py")
runner = module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(runner)

REFS = [
    (r"C:\Users\tyranno\AppData\Local\Temp\codex-clipboard-13b8ac5a-88ef-474d-a22e-b1f51459f3bb.png", "01-factory", "forward through the factory aisle", "[excited] Ê ê ê! Ấm inox 1,8 lít, đun sôi nhanh và tự ngắt điện khi nước sôi nè!"),
    (r"C:\Users\tyranno\AppData\Local\Temp\codex-clipboard-60c4dd6f-e070-4bf6-a1c6-7058d413d711.png", "02-mall", "sideways through the mall corridor", "[playful] Các dợ nhìn nè! Vòi rót gọn, tay cầm cách nhiệt, đế xoay 360 độ luôn á!"),
    (r"C:\Users\tyranno\AppData\Local\Temp\codex-clipboard-bf6674cd-0a5f-4f9e-b029-834f3a8fd341.png", "03-appliance-store", "past the appliance shelves", "[amazed] Inox sáng bóng, nắp mở tiện, dung tích 1,8 lít; mấy ní thấy hợp thì chốt nha!"),
]


def data_url(path: Path) -> str:
    return "data:image/png;base64," + base64.b64encode(path.read_bytes()).decode()


def prompt_for(index: int, action: str) -> str:
    return f"""Create a real AI-generated 6-second vertical 9:16 product video from this exact reference image. Animate the scene immediately: {action}. Keep the transparent acrylic handled box suspended in the adult woman's hand, with the front of the box facing the camera throughout. Preserve the stainless steel 1.8L kettle, black handle and lid, red indicator light, all Vietnamese text and labels, box geometry, hand, nails, lighting and background. The camera and the hand move naturally; the box may bob 1–2 cm but must not spin, flip, morph or touch a surface. No face, body, extra hands, extra fingers, new props, new text, subtitles, logos, watermark, music or sound effects. One continuous shot, visible motion from the first frame, realistic parallax, no static slideshow, no image-only hold."""


def read_duration(path: Path) -> float:
    result = subprocess.run([FF, "-hide_banner", "-i", str(path)], capture_output=True, text=True, encoding="utf-8", errors="replace")
    m = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", result.stderr)
    if not m:
        raise RuntimeError(f"Cannot measure {path}")
    return int(m[1]) * 3600 + int(m[2]) * 60 + float(m[3])


def wait_video(task_id: str, headers: dict, task_path: Path) -> dict:
    last = None
    for _ in range(100):
        task = requests.get(BASE + "/v1/videos/" + task_id, headers=headers, timeout=35).json()
        state = (task.get("status"), task.get("progress"))
        if state != last:
            print(task_id, state, flush=True)
            last = state
        if task.get("status") == "failed":
            task_path.write_text(json.dumps(task, ensure_ascii=False, indent=2), encoding="utf-8")
            raise RuntimeError(task.get("error") or "Muse AI video generation failed")
        if task.get("status") == "completed":
            task_path.write_text(json.dumps(task, ensure_ascii=False, indent=2), encoding="utf-8")
            return task
        time.sleep(7)
    raise RuntimeError("Muse task remains pending after polling window")


def media_url(task: dict) -> str:
    return task.get("url") or task.get("video", {}).get("url") or task.get("result", {}).get("url")


def mux_audio(video: Path, voice: Path, final: Path) -> None:
    voice_seconds = read_duration(voice)
    tempo = max(1.0, voice_seconds / 5.8)
    if tempo > 1.25:
        raise RuntimeError(f"Dialogue too long for 6 seconds: {voice_seconds:.2f}s")
    filters = f"[0:v]scale=720:1280:force_original_aspect_ratio=increase,force_divisible_by=2,crop=720:1280,setsar=1,fps=30[v];[1:a]atempo={tempo:.8f},apad,atrim=duration=6[a]"
    subprocess.run([FF, "-y", "-i", str(video), "-i", str(voice), "-filter_complex", filters, "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-t", "6", "-movflags", "+faststart", str(final)], capture_output=True, check=True)
    subprocess.run([FF, "-v", "error", "-i", str(final), "-f", "null", "-"], capture_output=True, check=True)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    headers = runner.muse_headers()
    manifest = {"profile": "mica-uploaded-images-ai-v1", "created_at": datetime.now(timezone.utc).isoformat(), "provider_calls": {"muse_videos": 0, "elevenlabs_tts": 0}, "outputs": []}
    for index, (source, slug, action, dialogue) in enumerate(REFS, 1):
        source_path = Path(source)
        directory = OUT / f"{index:02d}-{slug}"
        directory.mkdir(parents=True, exist_ok=True)
        input_path = directory / "input.png"
        shutil.copy2(source_path, input_path)
        prompt = prompt_for(index, action)
        (directory / "video-prompt.txt").write_text(prompt, encoding="utf-8")
        (directory / "dialogue.txt").write_text(dialogue, encoding="utf-8")
        task_path = directory / "muse-task.json"
        raw = directory / "muse-original.mp4"
        if not raw.exists():
            if task_path.exists():
                task_id = json.loads(task_path.read_text(encoding="utf-8"))["id"]
                task = wait_video(task_id, headers, task_path)
            else:
                payload = {"prompt": prompt, "duration": 6, "size": "9:16", "resolution": "720p", "reference_image": data_url(input_path)}
                response = requests.post(BASE + "/v1/videos", headers={**headers, "Content-Type": "application/json"}, json=payload, timeout=90)
                if response.status_code >= 400:
                    raise RuntimeError(f"Muse HTTP {response.status_code}: {response.text[:500]}")
                task = response.json()
                task_path.write_text(json.dumps(task, ensure_ascii=False, indent=2), encoding="utf-8")
                manifest["provider_calls"]["muse_videos"] += 1
                task = wait_video(task["id"], headers, task_path)
            url = media_url(task)
            if not url:
                raise RuntimeError("Muse completed without media URL")
            response = requests.get(url, headers=headers, timeout=120)
            response.raise_for_status()
            raw.write_bytes(response.content)
        if read_duration(raw) < 5.96:
            raise RuntimeError(f"Muse output shorter than 6 seconds: {read_duration(raw):.2f}s")
        old_voice = ROOT / "videos/2026-10-28-inox-kettle-3clips" / f"{index:02d}-0{index}-" + ""
        # Reuse the already generated Adam voice for matching dialogue to avoid a new TTS call.
        candidates = list((ROOT / "videos/2026-10-28-inox-kettle-3clips").glob(f"{index:02d}-*/voice.mp3"))
        voice = directory / "voice.mp3"
        if candidates:
            shutil.copy2(candidates[0], voice)
        else:
            raise RuntimeError("Cached Adam voice not found")
        final = directory / "final.mp4"
        mux_audio(raw, voice, final)
        subprocess.run([FF, "-y", "-i", str(final), "-vf", "fps=1,scale=180:320,tile=3x2", "-frames:v", "1", str(directory / "contact-sheet.jpg")], capture_output=True, check=True)
        report = {"index": index, "slug": slug, "seconds": read_duration(final), "resolution": "720x1280", "fps": 30, "visual_method": "Muse AI image-to-video", "voice": "Adam eleven_v3 reused from cache", "decode": "passed", "physical_motion": "AI generated; inspect contact sheet and playback"}
        (directory / "verification.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        manifest["outputs"].append({"index": index, "slug": slug, "path": str(final), "raw": str(raw)})
        print("READY", final, flush=True)
    (OUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
