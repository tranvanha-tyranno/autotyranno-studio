import json
import pathlib
import re
import subprocess
import wave
import imageio_ffmpeg

root = pathlib.Path(__file__).resolve().parent
source = root / 'muse-cocobear-review-10s.mp4'
voice = root / 'muse-cocobear-review-voice.wav'
output = root / 'cocobear-review-final-20s.mp4'
ff = imageio_ffmpeg.get_ffmpeg_exe()
probe = subprocess.run([ff, '-hide_banner', '-i', str(source)], capture_output=True, text=True, encoding='utf-8', errors='replace')
match = re.search(r'Duration: (\d+):(\d+):(\d+\.\d+)', probe.stderr)
if not match:
    raise RuntimeError('Cannot read video duration')
source_duration = int(match[1]) * 3600 + int(match[2]) * 60 + float(match[3])
with wave.open(str(voice), 'rb') as audio:
    voice_duration = audio.getnframes() / audio.getframerate()
tempo = max(1.0, voice_duration / 19.7)
filters = f'[0:v]setpts={20/source_duration:.8f}*(PTS-STARTPTS),fps=24,trim=duration=20[v];[1:a]atempo={tempo:.8f},apad,atrim=duration=20[a]'
process = subprocess.run([ff, '-y', '-i', str(source), '-i', str(voice), '-filter_complex', filters, '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-preset', 'fast', '-crf', '18', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-t', '20', '-movflags', '+faststart', str(output)], capture_output=True, text=True, encoding='utf-8', errors='replace')
if process.returncode:
    raise RuntimeError(process.stderr[-1800:])
report = {'source_seconds': source_duration, 'voice_seconds': voice_duration, 'voice_tempo': tempo, 'target_seconds': 20, 'visual_edit': 'slow camera motion to 20 seconds; no looping', 'output': str(output)}
(root / 'cocobear-review-media-check.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
print(json.dumps(report))
# Contact sheet for visual inspection.
subprocess.run([ff, '-y', '-i', str(output), '-vf', 'fps=1/4,scale=216:384,tile=5x1', '-frames:v', '1', str(root / 'cocobear-review-contact-sheet.jpg')], capture_output=True, check=True)
