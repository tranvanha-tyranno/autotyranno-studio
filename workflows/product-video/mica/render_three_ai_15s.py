"""Generate three real 15-second AI videos from the supplied mica-box images."""
from __future__ import annotations

import base64, json, re, shutil, subprocess, time
from datetime import datetime, timezone
from pathlib import Path
from importlib.util import spec_from_file_location, module_from_spec

import imageio_ffmpeg, requests

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "videos" / "2026-10-28-inox-kettle-3clips-ai15"
BASE = "http://127.0.0.1:18610"
FF = imageio_ffmpeg.get_ffmpeg_exe()
spec = spec_from_file_location("runner", ROOT / "workflows/product-video/run.py")
runner = module_from_spec(spec); assert spec.loader is not None; spec.loader.exec_module(runner)

JOBS = [
    (r"C:\Users\tyranno\AppData\Local\Temp\codex-clipboard-13b8ac5a-88ef-474d-a22e-b1f51459f3bb.png", "01-factory", "Ê ê ê! Đây là ấm inox cao cấp 1,8 lít nha! Nấu nhanh, tự ngắt điện khi nước sôi, tay cầm cách nhiệt và đế xoay 360 độ. Nhìn gọn mà tiện lắm luôn!", ["walk forward through the factory aisle with clear background parallax", "continue with a brisk small side move and a gentle camera push while keeping the front of the box toward camera"]),
    (r"C:\Users\tyranno\AppData\Local\Temp\codex-clipboard-60c4dd6f-e070-4bf6-a1c6-7058d413d711.png", "02-mall", "Các dợ nhìn nè! Ấm inox 1,8 lít, vòi rót gọn, tay cầm cách nhiệt, nắp mở tiện và đế xoay 360 độ. Để góc bếp hay mang đi đều thấy tiện nha!", ["walk sideways through the mall corridor with lights and background moving clearly", "continue past the mall lights with a gentle pull back then a small forward camera move, front of the box stays facing camera"]),
    (r"C:\Users\tyranno\AppData\Local\Temp\codex-clipboard-bf6674cd-0a5f-4f9e-b029-834f3a8fd341.png", "03-appliance-store", "Inox sáng bóng, dung tích 1,8 lít, nút mở nắp tiện và tự ngắt điện khi nước sôi. Mấy ní cần một chiếc ấm gọn gàng thì xem kỹ mẫu này nha!", ["move briskly past the appliance shelves with natural parallax and a small downward camera settle", "continue along the aisle with a short upward camera lift and a gentle lateral move, keep the box front facing camera"]),
]

def data_url(p: Path) -> str:
    return "data:image/png;base64," + base64.b64encode(p.read_bytes()).decode()

def prompt(action: str) -> str:
    return f"""Create a real AI-generated 10-second vertical 9:16 product video from this exact reference image. Begin moving immediately: {action}. Keep the transparent acrylic handled box suspended in the adult woman's hand, front facing camera. Preserve the silver stainless-steel 1.8L kettle, black handle and lid, red indicator light, every Vietnamese label and all box geometry exactly. Natural camera and hand movement with visible parallax; box may bob 1–2 cm but must not spin, flip, morph or touch any surface. No face, body, extra hands, extra fingers, new props, new text, subtitles, logos, watermark, music or sound effects. One continuous realistic shot, no slideshow, no static hold."""

def duration(p: Path) -> float:
    r = subprocess.run([FF, "-hide_banner", "-i", str(p)], capture_output=True, text=True, encoding="utf-8", errors="replace")
    m = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", r.stderr)
    if not m: raise RuntimeError(f"Cannot measure {p}")
    return int(m[1])*3600 + int(m[2])*60 + float(m[3])

def poll(task_id: str, headers: dict, path: Path) -> dict:
    last = None
    for _ in range(100):
        task = requests.get(BASE+"/v1/videos/"+task_id, headers=headers, timeout=35).json()
        state = (task.get("status"), task.get("progress"))
        if state != last: print(task_id, state, flush=True); last = state
        if task.get("status") == "failed":
            path.write_text(json.dumps(task, ensure_ascii=False, indent=2), encoding="utf-8")
            raise RuntimeError(task.get("error") or "Muse AI task failed")
        if task.get("status") == "completed":
            path.write_text(json.dumps(task, ensure_ascii=False, indent=2), encoding="utf-8")
            return task
        time.sleep(7)
    raise RuntimeError("Muse AI task remains pending")

def media_url(task: dict) -> str:
    return task.get("url") or task.get("video", {}).get("url") or task.get("result", {}).get("url")

def generate_scene(image: Path, text: str, scene_dir: Path, headers: dict) -> Path:
    scene_dir.mkdir(parents=True, exist_ok=True)
    prompt_path = scene_dir / "prompt.txt"; prompt_path.write_text(text, encoding="utf-8")
    task_path = scene_dir / "task.json"; raw = scene_dir / "scene.mp4"
    if raw.exists(): return raw
    if task_path.exists():
        task = poll(json.loads(task_path.read_text(encoding="utf-8"))["id"], headers, task_path)
    else:
        payload = {"prompt": text, "duration": 10, "size": "9:16", "resolution": "720p", "reference_image": data_url(image)}
        r = requests.post(BASE+"/v1/videos", headers={**headers, "Content-Type": "application/json"}, json=payload, timeout=90)
        if r.status_code >= 400: raise RuntimeError(f"Muse HTTP {r.status_code}: {r.text[:500]}")
        task = r.json(); task_path.write_text(json.dumps(task, ensure_ascii=False, indent=2), encoding="utf-8")
        task = poll(task["id"], headers, task_path)
    url = media_url(task)
    if not url: raise RuntimeError("Muse completed without media URL")
    r = requests.get(url, headers=headers, timeout=120); r.raise_for_status(); raw.write_bytes(r.content)
    if duration(raw) < 9.96: raise RuntimeError(f"AI scene shorter than 10 seconds: {duration(raw):.2f}s")
    return raw

def concat_15(scene1: Path, scene2: Path, out: Path) -> None:
    filt = "[0:v]scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,setsar=1,fps=30,trim=duration=10,setpts=PTS-STARTPTS[a];[1:v]scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,setsar=1,fps=30,trim=duration=5,setpts=PTS-STARTPTS[b];[a][b]concat=n=2:v=1:a=0[v]"
    subprocess.run([FF,"-y","-i",str(scene1),"-i",str(scene2),"-filter_complex",filt,"-map","[v]","-an","-c:v","libx264","-preset","fast","-crf","18","-pix_fmt","yuv420p","-t","15","-movflags","+faststart",str(out)], capture_output=True, check=True)

def tts(text: str, target: Path) -> None:
    if target.exists(): return
    r = requests.post("https://api.elevenlabs.io/v1/text-to-speech/pNInz6obpgDQGcFmaJgB", params={"output_format":"mp3_44100_128"}, headers={"xi-api-key":runner.eleven_key(),"Accept":"audio/mpeg"}, json={"text":text,"model_id":"eleven_v3","language_code":"vi","voice_settings":{"stability":0.5}}, timeout=180)
    if r.status_code != 200: raise RuntimeError(f"ElevenLabs HTTP {r.status_code}: {r.text[:300]}")
    target.write_bytes(r.content)

def mux(video: Path, voice: Path, final: Path) -> None:
    sec = duration(voice); tempo = max(1.0, sec/14.5)
    if tempo > 1.25: raise RuntimeError(f"Dialogue too long for 15 seconds: {sec:.2f}s")
    filt = f"[1:a]atempo={tempo:.8f},apad,atrim=duration=15[a]"
    subprocess.run([FF,"-y","-i",str(video),"-i",str(voice),"-filter_complex",filt,"-map","0:v","-map","[a]","-c:v","copy","-c:a","aac","-b:a","160k","-t","15","-movflags","+faststart",str(final)], capture_output=True, check=True)
    subprocess.run([FF,"-v","error","-i",str(final),"-f","null","-"], capture_output=True, check=True)

def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    plan = {"profile":"mica-ai-15s","target_seconds":15,"input_count":3,"opening_image_calls":0,"planned_provider_calls":{"muse_video_scenes":6,"elevenlabs_tts":3,"optional_llm":0},"strategy":"two independent 10s AI scenes per input; trim scene 2 to 5s and concatenate to 15s; no looping or still fallback"}
    (OUT/"cost-plan.json").write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding="utf-8")
    headers = runner.muse_headers(); manifest={"profile":"mica-ai-15s","created_at":datetime.now(timezone.utc).isoformat(),"provider_calls":{"muse_video_scenes":0,"elevenlabs_tts":0},"outputs":[]}
    for idx,(src,slug,dialogue,actions) in enumerate(JOBS,1):
        d=OUT/f"{idx:02d}-{slug}"; d.mkdir(parents=True,exist_ok=True); image=Path(src); shutil.copy2(image,d/"input.png"); (d/"dialogue.txt").write_text(dialogue,encoding="utf-8")
        scenes=[]
        for n,action in enumerate(actions,1):
            scenes.append(generate_scene(d/"input.png",prompt(action),d/f"scene-{n:02d}",headers)); manifest["provider_calls"]["muse_video_scenes"]+=1
        silent=d/"muse-ai-15s.mp4"; concat_15(scenes[0],scenes[1],silent)
        voice=d/"voice.mp3"; tts(dialogue,voice); manifest["provider_calls"]["elevenlabs_tts"]+=1
        final=d/"final.mp4"; mux(silent,voice,final)
        subprocess.run([FF,"-y","-i",str(final),"-vf","fps=1,scale=180:320,tile=5x3","-frames:v","1",str(d/"contact-sheet.jpg")],capture_output=True,check=True)
        report={"index":idx,"slug":slug,"seconds":duration(final),"resolution":"720x1280","fps":30,"visual_method":"two independent Muse AI scenes concatenated to 15 seconds","decode":"passed","still_fallback":False}
        (d/"verification.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8"); manifest["outputs"].append({"index":idx,"slug":slug,"path":str(final)}); print("READY",final,flush=True)
    (OUT/"manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding="utf-8")

if __name__ == "__main__": main()
