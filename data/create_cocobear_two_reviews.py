"""Resumeable Muse image/video generation and Adam V3 composition for two reviews."""
import argparse
import base64
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time

from PIL import Image
import imageio_ffmpeg
import requests

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'data/cocobear-two-reviews'
OUT.mkdir(exist_ok=True)
REF = Path(r'C:\Users\tyranno\AppData\Roaming\genzshop-studio\output\test\0p6mj9fkzdyh\image-0p6mj9fkzdyh.png')
FF = imageio_ffmpeg.get_ffmpeg_exe()
BASE = 'http://127.0.0.1:18610'
env = (ROOT/'experiments/muse2api-czg86389/.env').read_text(encoding='utf-8-sig')
MUSE_KEY = next(line.split('=',1)[1].strip().strip('\"\'') for line in env.splitlines() if line.startswith('MUSE2API_KEY='))
HEADERS = {'Authorization': 'Bearer ' + MUSE_KEY}

SCRIPTS = [
    '''[excited] Ê Ê Ê! NỬA ĐÊM con đòi sữa, mẹ còn phải lật đật đi đun nước hả?

[playful] Các dợ ơi! Coco Bear PRO có REMOTE điều khiển từ xa nè!

[amazed] Đèn ngủ dịu nhẹ, giữ ấm tới 72 TIẾNG! Dữ thần vậy!

[confident] Mấy ní BẤM GIỎ HÀNG, CHỐT NGAY một em về dùng! Tiện quá trời!''',
    '''[sarcastic] Trời ơi! Năm 2026 rồi, ai còn ngồi CANH NƯỚC pha sữa nữa vậy?

[excited] Các dợ nhìn Coco Bear PRO này! Điều khiển từ xa, chỉnh nhiệt tiện ghê!

[amazed] Có cả ĐÈN NGỦ, giữ ấm tới 72 TIẾNG! Thiệt luôn á!

[playful] Mấy ní ơi, thích thì NHẤN GIỎ HÀNG CHỐT ĐƠN LIỀN! Mua về dùng cho tiện, hahahaaaa!''',
]
SETTINGS = [
    ('night-nursery', 'a tasteful home baby-feeding preparation corner at night, a pale oak side table against a soft beige bedroom wall, a dim warm shaded lamp in the far background, gentle moonlight through a curtain, calm cozy midnight atmosphere, realistic soft practical lighting. No child or person present, no crib next to the kettle'),
    ('daylight-kitchen', 'a bright contemporary home kitchen in daylight, a warm cream stone countertop, softly blurred oak cabinets and a distant green plant, clean sunlit morning atmosphere, natural window lighting and believable reflections'),
]
PRODUCT = '''The actual unboxed Coco Bear PRO milk-water warming kettle from the reference photo: ivory-white rounded base, clear glass jug partly filled with clear water, thick ivory handle on the right, metallic collar near the rim, transparent lid with an ivory bear-shaped knob, glossy black rounded front control panel with two digital temperature readouts, exact Coco Bear branding. Keep the original product design, dimensions, parts and markings consistent. It is a water kettle, not a baby bottle, coffee machine or blender. Use the references only for product identity. Remove the transport package and original holding hand for this new staged scene. Do not add new labels, packaging text, feature icons or superimposed captions. No extra product, no duplicate handle, no warped glass.'''

def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')

def data_url(path):
    return 'data:image/png;base64,' + base64.b64encode(path.read_bytes()).decode()

def clip_dir(index):
    path = OUT / f'clip-{index+1}-{SETTINGS[index][0]}'
    path.mkdir(exist_ok=True)
    (path/'dialogue.txt').write_text(SCRIPTS[index], encoding='utf-8')
    return path

def wait_task(path, endpoint, payload, target, idempotency=None):
    state_path = path/(target.stem+'-task.json')
    if target.exists():
        return
    if state_path.exists():
        task = json.loads(state_path.read_text(encoding='utf-8'))
    else:
        headers = dict(HEADERS)
        if idempotency:
            headers['Idempotency-Key'] = idempotency
        response = requests.post(BASE+endpoint, headers=headers, json=payload, timeout=90)
        response.raise_for_status()
        task = response.json()
        write_json(state_path, task)
    task_id = task['id']
    print(path.name, target.name, 'task', task_id, flush=True)
    last = None
    for _ in range(100):
        result = requests.get(BASE+endpoint+'/'+task_id, headers=HEADERS, timeout=35)
        result.raise_for_status()
        task = result.json()
        current = (task.get('status'), task.get('progress'))
        if current != last:
            print(path.name, target.name, current, flush=True)
            last = current
        if task.get('status') == 'failed':
            write_json(state_path, task)
            raise RuntimeError(task.get('error', 'Muse task failed'))
        if task.get('status') == 'completed':
            url = task.get('url') or task.get('result',{}).get('url') or task['data'][0]['url']
            media = requests.get(url, headers=HEADERS, timeout=120)
            media.raise_for_status()
            target.write_bytes(media.content)
            write_json(state_path, task)
            return
        time.sleep(10)
    raise RuntimeError('Task remains pending; rerun to resume same task')

def make_voice(index):
    path = clip_dir(index)
    voice = path/'adam-v3.mp3'
    if voice.exists():
        return
    key = os.environ['ELEVENLABS_API_KEY']
    response = requests.post('https://api.elevenlabs.io/v1/text-to-speech/pNInz6obpgDQGcFmaJgB', params={'output_format': 'mp3_44100_128'}, headers={'xi-api-key': key, 'Accept': 'audio/mpeg'}, json={'text': SCRIPTS[index], 'model_id': 'eleven_v3', 'language_code': 'vi', 'voice_settings': {'stability': 0.5}}, timeout=180)
    print(path.name, 'Adam_V3_HTTP', response.status_code, flush=True)
    if response.status_code != 200:
        raise RuntimeError(response.text[:800].replace(key, '[REDACTED]'))
    if not response.headers.get('content-type','').startswith('audio/'):
        raise RuntimeError('Missing audio response')
    voice.write_bytes(response.content)
    write_json(path/'voice-info.json', {'voice': 'Adam - Dominant, Firm', 'voice_id': 'pNInz6obpgDQGcFmaJgB', 'model_id': 'eleven_v3', 'language': 'vi', 'request_id': response.headers.get('request-id'), 'character_cost': response.headers.get('character-cost')})

def make_image(index):
    path = clip_dir(index)
    crop = OUT/'product-reference-crop.png'
    if not crop.exists():
        Image.open(REF).crop((143, 666, 653, 1248)).save(crop)
    prompt = 'Create one photorealistic vertical 9:16 product-review opening photograph. ' + PRODUCT + '\nSetting: ' + SETTINGS[index][1] + '''. Product standing stably on the tabletop, complete product fully visible with generous space on both sides to allow a later camera orbit. Start at a modest front-left three-quarter angle, about 15 degrees left of the front, so the front control panel is clearly legible and the right handle is visible. Product occupies about 60 percent of frame height. Eye-level tabletop product photography, realistic size, no border, no extra caption or watermark. Keep all background elements physically plausible and consistent.'''
    (path/'image-prompt.txt').write_text(prompt, encoding='utf-8')
    wait_task(path, '/v1/images/tasks', {'prompt': prompt, 'size': '9:16', 'images': [{'url': data_url(crop)}, {'url': data_url(REF)}], 'timeout': 600}, path/'opening.png', f'cocobear-two-review-background-{index+1}')
    with Image.open(path/'opening.png') as image:
        print(path.name, 'opening_size', image.size, flush=True)

def make_video(index):
    path = clip_dir(index)
    prompt = '''Generate a continuous, clearly moving multi-angle product review from this exact opening photograph. ''' + PRODUCT.split('Use the references')[0] + ''' Preserve this opening photograph's new tabletop setting, original light, all background objects and the exact kettle throughout. The product is rigid and stationary on the table.

Only the camera moves: a visible smooth stabilized orbit from the initial front-left three-quarter angle, through a clear frontal view, toward a front-right three-quarter angle. Total camera arc about 45-55 degrees, never show the unseen back. The viewer must see genuinely different perspectives of the lid, glass jug, handle and front control panel. Begin motion immediately; maintain smooth, moderately energetic progress across the arc rather than spending the clip static or reversing repeatedly. Include a gentle 8 percent dolly-in around the middle then pull back just enough to keep the complete product visible. Natural background parallax and realistic reflections demonstrate camera motion. Ease in and out softly without abrupt jerks.

One continuous ten-second shot, no cuts, no morph transitions, no product turntable. Keep kettle fully in frame, sharp and identifiable at all times. Never change the kettle design, brand lettering, temperature digits, handle, bear lid knob or glass proportions. No extra fingers or people, no water pouring, no operating buttons, no boiling steam, no text overlays, no music, speech or sound effects. Vertical 9:16, 720p, realistic product photography. Prioritize identity and stable design over extreme angle.'''
    (path/'video-prompt.txt').write_text(prompt, encoding='utf-8')
    wait_task(path, '/v1/videos', {'prompt': prompt, 'duration': 10, 'size': '9:16', 'resolution': '720p', 'reference_image': data_url(path/'opening.png')}, path/'muse-original.mp4')
    subprocess.run([FF, '-y', '-i', str(path/'muse-original.mp4'), '-vf', 'fps=1/2,scale=216:384,tile=5x1', '-frames:v', '1', str(path/'source-contact-sheet.jpg')], capture_output=True, check=True)

def probe_seconds(path):
    info = subprocess.run([FF, '-hide_banner', '-i', str(path)], capture_output=True, text=True, encoding='utf-8', errors='replace')
    match = re.search(r'Duration: (\d+):(\d+):(\d+\.\d+)', info.stderr)
    if not match:
        raise RuntimeError('Missing media duration: '+str(path))
    return int(match[1])*3600+int(match[2])*60+float(match[3])

def render(index):
    path = clip_dir(index)
    final = path/f'cocobear-script-{index+1}-adam-20s.mp4'
    if final.exists() and (path/'verification.json').exists():
        print('verified output exists', str(final), flush=True)
        return
    source_seconds = probe_seconds(path/'muse-original.mp4')
    voice_seconds = probe_seconds(path/'adam-v3.mp3')
    voice_speed = max(1, voice_seconds/19.8)
    filters = f'[0:v]setpts={20/source_seconds:.8f}*(PTS-STARTPTS),minterpolate=fps=60:mi_mode=mci:mc_mode=obmc:me_mode=bilat:me=hexbs:search_param=8:vsbmc=0,tpad=stop_mode=clone:stop_duration=1,trim=duration=20,scale=720:1280:force_original_aspect_ratio=increase:force_divisible_by=2,crop=720:1280,setsar=1[v];[1:a]atempo={voice_speed:.8f},apad,atrim=duration=20[a]'
    print(path.name, 'rendering 60fps', 'source_seconds', source_seconds, 'voice_seconds', voice_seconds, 'voice_speed', voice_speed, flush=True)
    with (path/'render.log').open('w', encoding='utf-8') as log:
        result = subprocess.run([FF, '-y', '-i', str(path/'muse-original.mp4'), '-i', str(path/'adam-v3.mp3'), '-filter_complex', filters, '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-preset', 'fast', '-crf', '18', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-t', '20', '-movflags', '+faststart', str(final)], stdout=log, stderr=log)
    if result.returncode:
        raise RuntimeError('Render failed; see '+str(path/'render.log'))
    subprocess.run([FF, '-v', 'error', '-i', str(final), '-f', 'null', '-'], capture_output=True, check=True)
    duration = probe_seconds(final)
    if abs(duration-20)>0.1:
        raise RuntimeError('Unexpected final duration')
    subprocess.run([FF, '-y', '-i', str(final), '-vf', 'fps=1/4,scale=216:384,tile=5x1', '-frames:v', '1', str(path/'contact-sheet.jpg')], capture_output=True, check=True)
    write_json(path/'verification.json', {'script': index+1, 'setting': SETTINGS[index][0], 'source_seconds': source_seconds, 'voice_seconds': voice_seconds, 'voice_speed': voice_speed, 'final_seconds': duration, 'resolution': '720x1280', 'fps': 60, 'decode': 'passed', 'method': 'Muse reference image restaging, Muse image-to-video camera orbit; slow footage and interpolate, no loop; full Adam V3 dialogue', 'file': str(final), 'sha256': hashlib.sha256(final.read_bytes()).hexdigest()})
    print('READY', str(final), flush=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('stage', choices=['prepare', 'images', 'voices', 'videos', 'render'])
    parser.add_argument('--clip', type=int, choices=[1,2])
    args = parser.parse_args()
    indices = [args.clip-1] if args.clip else [0,1]
    if args.stage in ['prepare', 'voices']:
        with ThreadPoolExecutor(max_workers=2) as pool:
            voices = [pool.submit(make_voice, i) for i in indices]
            if args.stage == 'prepare':
                for i in indices:
                    make_image(i)
            for voice in voices:
                voice.result()
    elif args.stage == 'images':
        for i in indices: make_image(i)
    elif args.stage == 'videos':
        for i in indices: make_video(i)
    elif args.stage == 'render':
        with ThreadPoolExecutor(max_workers=2) as pool:
            list(pool.map(render, indices))
