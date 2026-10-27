"""Render stronger camera motion in Muse, interpolate to 60 fps, reuse Adam audio."""
import base64
import json
from pathlib import Path
import re
import subprocess
import sys
import time

import imageio_ffmpeg
import requests

folder = Path(__file__).resolve().parent
project = folder.parent
state_path = folder / 'cocobear-smooth-motion-task.json'
source = folder / 'cocobear-smooth-muse-original.mp4'
prompt = '''Animate this exact reference photograph as a polished product-review shot. The product is the Coco Bear kettle inside the transparent handled package in the original appliance store. Preserve the reference scene, product, hand, packaging, Vietnamese lettering, logo, shelf contents, original lighting and colors. No replacement setting, festive effects, extra objects, new people or additional graphics. Do not unbox or change the product.

The CAMERA MUST MOVE visibly and continuously from the first second. A controlled gimbal shot, not a nearly static photograph: track sideways in a graceful 15-degree front arc around the center of the boxed kettle, moving from the reference front view toward a modest right three-quarter view, while dollying in by about 10 percent. Then trace a gentle returning curve toward the starting view, ending with a subtle pullback. Use fluid acceleration and deceleration, constant subject tracking and smooth natural perspective parallax. The motion should feel intentional and clearly visible while remaining elegant, with no abrupt pauses or reversals. Keep every edge of the package inside the frame with comfortable margins. Focus remains clear across the package and kettle. Natural consistent reflections on the rigid clear box.

The hand and package stay still; only camera moves. The original store must remain the same throughout with only perspective changes from the moving camera. Do not invent an unseen back view or rotate a full circle. No changing letters, deforming glass, shape drift, flickering, duplicate fingers, jump cuts, transitions, artificial background changes, subtitles, speech, music or sound effects. One continuous realistic shot, 9:16 portrait, 720x1280, ten seconds. Prioritize exact product identity and scene continuity.'''
(folder / 'cocobear-smooth-motion-prompt.txt').write_text(prompt, encoding='utf-8')
env = (project / 'experiments/muse2api-czg86389/.env').read_text(encoding='utf-8-sig')
key = next(x.split('=', 1)[1].strip().strip('"\'') for x in env.splitlines() if x.startswith('MUSE2API_KEY='))
headers = {'Authorization': f'Bearer {key}'}
base = 'http://127.0.0.1:18610'
if not state_path.exists():
    reference = Path(r'C:\Users\tyranno\AppData\Roaming\genzshop-studio\output\test\0p6mj9fkzdyh\image-0p6mj9fkzdyh.png')
    payload = {'prompt': prompt, 'duration': 10, 'size': '9:16', 'resolution': '720p', 'reference_image': 'data:image/png;base64,' + base64.b64encode(reference.read_bytes()).decode()}
    result = requests.post(base + '/v1/videos', headers=headers, json=payload, timeout=90)
    result.raise_for_status()
    state_path.write_text(json.dumps(result.json(), indent=2), encoding='utf-8')
task_id = json.loads(state_path.read_text(encoding='utf-8'))['id']
print('task', task_id, flush=True)
if not source.exists():
    for _ in range(90):
        response = requests.get(base + '/v1/videos/' + task_id, headers=headers, timeout=30)
        response.raise_for_status()
        status = response.json()
        print('generation', status.get('status'), 'milestone', status.get('progress'), flush=True)
        if status.get('status') == 'failed':
            raise RuntimeError(status.get('error'))
        if status.get('status') == 'completed':
            media = requests.get(status['url'], headers=headers, timeout=120)
            media.raise_for_status()
            source.write_bytes(media.content)
            state_path.write_text(json.dumps(status, ensure_ascii=False, indent=2), encoding='utf-8')
            break
        time.sleep(10)
    else:
        raise RuntimeError('Generation still pending; rerun to resume same task')
ff = imageio_ffmpeg.get_ffmpeg_exe()
probe = subprocess.run([ff, '-hide_banner', '-i', str(source)], capture_output=True, text=True, encoding='utf-8', errors='replace')
duration = re.search(r'Duration: (\d+):(\d+):(\d+\.\d+)', probe.stderr)
if not duration:
    raise RuntimeError('Cannot measure Muse output')
seconds = int(duration[1]) * 3600 + int(duration[2]) * 60 + float(duration[3])
print('source_seconds', seconds, 'interpolating_to_60fps', flush=True)
output = folder / 'cocobear-adam-smooth-20s.mp4'
audio_source = folder / 'cocobear-review-adam-v3-20s.mp4'
filtergraph = f'[0:v]setpts={20/seconds:.8f}*(PTS-STARTPTS),minterpolate=fps=60:mi_mode=mci:mc_mode=obmc:me_mode=bilat:me=hexbs:search_param=8:vsbmc=0,tpad=stop_mode=clone:stop_duration=1,trim=duration=20,scale=720:1280:force_original_aspect_ratio=increase:force_divisible_by=2,crop=720:1280,setsar=1[v]'
command = [ff, '-y', '-i', str(source), '-i', str(audio_source), '-filter_complex', filtergraph, '-map', '[v]', '-map', '1:a:0', '-c:v', 'libx264', '-preset', 'fast', '-crf', '18', '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-t', '20', '-movflags', '+faststart', str(output)]
with (folder / 'cocobear-smooth-render.log').open('w', encoding='utf-8') as logfile:
    process = subprocess.run(command, stdout=logfile, stderr=logfile)
if process.returncode:
    raise RuntimeError('Video processing failed; see cocobear-smooth-render.log')
subprocess.run([ff, '-v', 'error', '-i', str(output), '-f', 'null', '-'], capture_output=True, check=True)
subprocess.run([ff, '-y', '-i', str(output), '-vf', 'fps=1/4,scale=216:384,tile=5x1', '-frames:v', '1', str(folder / 'cocobear-smooth-contact-sheet.jpg')], capture_output=True, check=True)
report = {'task_id': task_id, 'source_seconds': seconds, 'output_seconds': 20, 'target_fps': 60, 'processing': 'optical flow interpolation; original generation slowed to 20 seconds; no repeated loop', 'audio': 'existing full Adam V3 review reused without new synthesis', 'output': str(output), 'decode_check': 'passed'}
(folder / 'cocobear-smooth-check.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
print(json.dumps(report), flush=True)
