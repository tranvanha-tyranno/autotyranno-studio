"""Staged multi-location helmet batch using the existing resumable local workflow."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
BATCH = ROOT / "videos/2026-10-28-helmet-reference-30s"
spec = importlib.util.spec_from_file_location("product_runner", ROOT / "workflows/product-video/run.py")
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)
config = runner.read_json(BATCH / "batch.json")
clip = config["clips"][0]
path = runner.clip_path(BATCH, 1, clip)
PRESERVE_BRAND = (
    "Resolve the generic clean-image instruction as follows: preserve all original physical "
    "product branding on the helmet exactly from reference 1. Remove only added graphic overlays "
    "or watermarks. The small factory ROCKRIDER wordmark must remain. This explicit product "
    "preservation requirement takes precedence over the generic request to remove logos. "
    "There is no ambiguity: retain original product letters, add no new advertising text. "
    "Generate the requested photograph now."
)

def images(number):
    if number == 1:
        runner.opening(BATCH, config, 1, clip)
        shutil.copy2(path / "opening.png", path / "scene-01-opening.png")
        return
    if not (path / "opening.png").exists():
        raise RuntimeError("Inspect opening.png before generating further scenes.")
    expected = path / f"scene-{number:02}-opening.png"
    if expected.exists():
        return
    target = expected
    state_path = path / f"scene-{number:02}-opening-task.json"
    if state_path.exists() and runner.read_json(state_path).get("status") == "failed":
        target = path / f"scene-{number:02}-opening-revised.png"
    prompt = (path / f"scene-{number:02}-opening-prompt.txt").read_text(encoding="utf-8")
    payload = {
        "prompt": prompt, "size": "9:16",
        "images": [
            {"url": runner.image_url(BATCH / "input/original.png")},
            {"url": runner.image_url(path / "opening.png")},
        ],
        "timeout": 600,
        "extra": PRESERVE_BRAND,
    }
    runner.task_media(BATCH, config, path, target, "/v1/images/tasks", payload)
    if target != expected:
        shutil.copy2(target, expected)

def repair_logo():
    # The provider's generic reference-image suffix strips product lettering.
    # Its supported `extra` field is appended last; use it to preserve the
    # factory wordmark in the one close-up where its disappearance is visible.
    target = path / "scene-02-opening-corrected.png"
    prompt = (
        "Edit reference image 2 with only this small product-fidelity correction. "
        "Keep the identical helmet, hands, sleeves, shop background, framing, light and vents. "
        "Restore the original product's small light-colored ROCKRIDER wordmark, precisely as "
        "pictured on the diagonal top-left ridge of the helmet in reference image 1. "
        "The letters must follow the existing ridge perspective, small and subtle. "
        "Do not add any other text, overlay, caption or watermark. Do not redesign any part."
    )
    (path / "scene-02-logo-repair-prompt.txt").write_text(prompt, encoding="utf-8")
    runner.task_media(BATCH, config, path, target, "/v1/images/tasks", {
        "prompt": prompt, "size": "9:16", "timeout": 600,
        "images": [{"url": runner.image_url(BATCH / "input/original.png")},
                   {"url": runner.image_url(path / "scene-02-opening.png")}],
        "extra": PRESERVE_BRAND,
    })
    print("REPAIR_READY_FOR_INSPECTION", target, flush=True)

def video(number, revision=False):
    source = path / f"scene-{number:02}-opening.png"
    if not source.exists():
        raise RuntimeError("Generate and inspect the scene opening first.")
    prompt = (path / f"scene-{number:02}-prompt.txt").read_text(encoding="utf-8")
    target = path / f"scene-{number:02}{'-v2' if revision else ''}.mp4"
    upload = path / f"scene-{number:02}-upload.png"
    # Preserve downloaded originals; give the provider a real PNG, not a WebP
    # carrying a .png filename.
    with runner.Image.open(source) as image:
        image.convert("RGB").save(upload, format="PNG")
    runner.task_media(BATCH, config, path, target, "/v1/videos", {
        "prompt": prompt, "duration": 10, "size": "9:16", "resolution": "720p",
        "images": [
            {"url": runner.image_url(upload)},
            {"url": runner.image_url(BATCH / "input/original.png")},
        ],
    })
    seconds = runner.duration(target)
    runner.run_ff([runner.FF, "-y", "-i", str(target), "-vf",
                   "fps=1/2,scale=216:384,tile=5x1", "-frames:v", "1",
                   str(path / f"{target.stem}-contact-sheet.jpg")])
    if seconds < 9.96:
        raise RuntimeError(f"Scene {number} is only {seconds}s, inspect provider result before proceeding.")
    print("SCENE_READY", number, seconds, flush=True)

def align_voice():
    # These four inter-paragraph silences were measured from this exact Adam take.
    # Keep 80 ms beyond speech on each side; adjust each paragraph independently
    # so its relevant product detail begins with the corresponding picture.
    boundaries = [
        (0.0, 7.422245),
        (7.953107, 14.698005),
        (15.310771, 21.909116),
        (22.729048, 28.519320),
        (29.252925, runner.duration(path / "voice.mp3")),
    ]
    filters = ["[0:a]asplit=5" + "".join(f"[s{n}]" for n in range(5))]
    records = []
    replacement_info = path / "voice-replacement.json"
    replacement = runner.read_json(replacement_info) if replacement_info.exists() else None
    for n, (start, end) in enumerate(boundaries):
        input_label = f"s{n}"
        if n == 1 and replacement:
            filters.append("[s1]anullsink")
            input_label = "1:a"
            start, end = 0.0, runner.duration(BATCH / replacement["audio"])
        tempo = max(1.0, (end-start) / 5.96)
        if tempo > 1.25:
            raise RuntimeError("A narration paragraph needs more than 1.25x; revise timing.")
        filters.append(
            f"[{input_label}]atrim=start={start:.8f}:end={end:.8f},asetpts=PTS-STARTPTS,"
            f"atempo={tempo:.8f},apad,atrim=duration=6[a{n}]"
        )
        records.append({"scene": n+1, "source_start": start, "source_end": end,
                        "audio_tempo": tempo, "final_start": 6*n, "final_end": 6*(n+1),
                        "source": replacement["audio"] if n == 1 and replacement else "voice.mp3"})
    filters.append("".join(f"[a{n}]" for n in range(5)) + "concat=n=5:v=0:a=1,loudnorm=I=-16:TP=-1.5:LRA=9[a]")
    command = [runner.FF, "-y", "-i", str(path / "voice.mp3")]
    if replacement:
        command += ["-i", str(BATCH / replacement["audio"])]
    command += ["-filter_complex", ";".join(filters), "-map", "[a]", "-ar", "48000",
                str(path / "voice-aligned.wav")]
    runner.run_ff(command)
    runner.save_json(path / "voice-timing.json", {
        "method": "Separate five paragraphs at four measured inter-paragraph silences; preserve speech with 80ms margins.",
        "source_sha256": hashlib.sha256((path / "voice.mp3").read_bytes()).hexdigest(),
        "paragraphs": records,
    })
    print("VOICE_ALIGNED", records, flush=True)

def render():
    if not (path / "voice-aligned.wav").exists():
        align_voice()
    sources = [path / f"scene-{n:02}.mp4" for n in range(1, 6)]
    durations = [runner.duration(source) for source in sources]
    if any(seconds < 9.96 for seconds in durations):
        raise RuntimeError("Insufficient independent footage; no padding or loops allowed.")
    speeds = clip.get("scene_visual_speeds", [1.5] * 5)
    if len(speeds) != 5 or any(not 1 <= value <= 2 for value in speeds):
        raise RuntimeError("Invalid per-scene visual speeds.")
    filters = []
    for n in range(5):
        filters.append(
            f"[{n}:v]trim=duration={6*speeds[n]:.8f},setpts=(PTS-STARTPTS)/{speeds[n]:.8f},"
            f"scale=720:1280:force_original_aspect_ratio=increase:force_divisible_by=2,"
            f"crop=720:1280,setsar=1,fps=30[v{n}]"
        )
    filters.append("".join(f"[v{n}]" for n in range(5)) + "concat=n=5:v=1:a=0[v]")
    filters.append("[5:a]apad,atrim=duration=30[a]")
    command = [runner.FF, "-y"]
    for source in sources:
        command += ["-i", str(source)]
    target = path / "final.mp4"
    command += [
        "-i", str(path / "voice-aligned.wav"), "-filter_complex", ";".join(filters),
        "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "18",
        "-preset", "fast", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
        "-t", "30", "-movflags", "+faststart", str(target),
    ]
    runner.run_ff(command)
    runner.run_ff([runner.FF, "-v", "error", "-i", str(target), "-f", "null", "-"])
    runner.run_ff([runner.FF, "-y", "-i", str(target), "-vf",
                   "fps=1/2,scale=180:320,tile=5x3", "-frames:v", "1",
                   str(path / "contact-sheet.jpg")])
    final_seconds = runner.duration(target)
    if abs(final_seconds - 30) > .1:
        raise RuntimeError("Incorrect final duration.")
    runner.save_json(path / "verification.json", {
        "final_seconds": final_seconds, "resolution": "720x1280", "fps": 30,
        "source_seconds": durations, "used_seconds_per_source": [6*speed for speed in speeds],
        "visual_speeds": speeds,
        "independent_scenes": 5, "looped": False, "slowed_to_fill": False,
        "narration": "Vietnamese Adam / eleven_v3, five paragraphs individually aligned to six-second scenes",
        "audio_original_seconds": runner.duration(path / "voice.mp3"),
        "audio_final_seconds": runner.duration(path / "voice-aligned.wav"),
        "decode_check": "passed", "visual_qa": "pending",
        "sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
    })
    print("READY", target, flush=True)

parser = argparse.ArgumentParser()
parser.add_argument("stage", choices=["plan", "images", "repair-logo", "videos", "voices", "align-voice", "render"])
parser.add_argument("--scene", type=int, choices=range(1, 6))
parser.add_argument("--revision", action="store_true")
args = parser.parse_args()
if args.stage == "plan":
    runner.warm_cache(BATCH, config)
    report = runner.plan(BATCH, config, [(1, clip)])
    missing_images = [n for n in range(1, 6) if not (path / f"scene-{n:02}-opening.png").exists()]
    extra = sum(n != 1 for n in missing_images)
    report["provider_calls_by_kind"]["additional_scene_opening_calls"] = extra
    report["provider_calls_if_run_now"] += extra
    report["multi_location_note"] = "Five separately inspected scene opening images, each anchored to original product and scene-one presenter."
    runner.save_json(BATCH / "cost-plan.json", report)
    print(json.dumps(report, ensure_ascii=False, indent=2), flush=True)
elif args.stage == "voices":
    runner.voice(BATCH, config, 1, clip)
    print("VOICE_SECONDS", runner.duration(path / "voice.mp3"), flush=True)
elif args.stage == "render":
    render()
elif args.stage == "align-voice":
    align_voice()
elif args.stage == "repair-logo":
    repair_logo()
else:
    for number in ([args.scene] if args.scene else range(1, 6)):
        if args.stage == "images":
            images(number)
        else:
            video(number, revision=args.revision)
