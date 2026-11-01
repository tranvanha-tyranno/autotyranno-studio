"""Staged, resumable Muse2API + Adam V3 product review batches."""
from __future__ import annotations

import argparse
import base64
import copy
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import hashlib
import importlib.util
import io
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import time

from PIL import Image
import imageio_ffmpeg
import requests

PROJECT = Path(__file__).resolve().parents[2]
FF = imageio_ffmpeg.get_ffmpeg_exe()
CACHE_ROOT = PROJECT / '.cache' / 'product-video'
MUSE_CACHE = CACHE_ROOT / 'muse'
TTS_CACHE = CACHE_ROOT / 'tts'


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def save_json(path, data):
    path = Path(path)
    staging = path.with_suffix('.pending.json')
    staging.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    staging.replace(path)


def _hashable(value):
    """Make request payloads stable without hashing large data URLs into manifests."""
    if isinstance(value, dict):
        return {key: _hashable(value[key]) for key in sorted(value)}
    if isinstance(value, list):
        return [_hashable(item) for item in value]
    if isinstance(value, str) and value.startswith('data:') and ';base64,' in value:
        return {'data_url_sha256': hashlib.sha256(value.encode()).hexdigest(), 'bytes': len(value)}
    return value


def request_key(namespace, payload):
    canonical = json.dumps({'namespace': namespace, 'payload': _hashable(payload)}, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(canonical.encode()).hexdigest()


def cache_enabled(config, kind):
    cache = config.get('cache', True)
    if isinstance(cache, bool):
        return cache
    return bool(cache.get(kind, True))


def cache_paths(root, key, suffix):
    root.mkdir(parents=True, exist_ok=True)
    return root / f'{key}{suffix}', root / f'{key}.json'


def initialize(args):
    config = read_json(args.config)
    config.setdefault('cache', {'muse': True, 'tts': True})
    image = Path(args.image).resolve()
    output = Path(args.output).resolve()
    validate(config)
    with Image.open(image) as source:
        source.verify()
    if output.exists():
        raise ValueError('Batch directory already exists. Resume it or choose a new batch name.')
    (output/'input').mkdir(parents=True)
    copied = output/'input'/('original'+image.suffix.lower())
    shutil.copy2(image, copied)
    refs = [str(copied.relative_to(output))]
    if config.get('product_crop'):
        with Image.open(copied) as original:
            w, h = original.size
            left, top, right, bottom = config['product_crop']
            original.crop((int(left*w), int(top*h), int(right*w), int(bottom*h))).save(output/'input/product-crop.png')
        refs.insert(0, 'input/product-crop.png')
    config['references'] = refs
    config['created_at'] = datetime.now().astimezone().isoformat()
    config['product_image_sha256'] = hashlib.sha256(copied.read_bytes()).hexdigest()
    for index, clip in enumerate(config['clips'], 1):
        path = output/f'clip-{index:02}-{clip["slug"]}'
        path.mkdir()
        (path/'dialogue.txt').write_text(clip['dialogue'].strip(), encoding='utf-8')
        for number, scene in enumerate(clip.get('scenes', []), 1):
            revision = scene.get('revision', 1)
            suffix = f'-r{revision:02}' if revision > 1 else ''
            folder = path/f'scene-{number:02}{suffix}'
            folder.mkdir()
            for name, value in [('dialogue', scene['dialogue']), ('opening-prompt', scene['opening_prompt']), ('video-prompt', scene['video_prompt'])]:
                (folder/f'{name}.txt').write_text(value.strip(), encoding='utf-8')
        if clip.get('reuse_voice'):
            supplied = Path(clip['reuse_voice'])
            if not supplied.is_absolute():
                supplied = PROJECT/supplied
            old_script = supplied.with_name('dialogue.txt')
            if old_script.read_text(encoding='utf-8-sig').strip() != clip['dialogue'].strip():
                raise ValueError('Cannot reuse voice: supplied script differs')
            shutil.copy2(supplied, path/'voice.mp3')
            save_json(path/'voice-info.json', {'source': str(supplied), 'provider': 'ElevenLabs', 'model': 'eleven_v3', 'voice': 'Adam', 'reused_after_exact_script_check': True})
    save_json(output/'batch.json', config)
    print('BATCH', output, flush=True)


def validate(config):
    duration_seconds = config.get('duration_seconds', 20)
    if not isinstance(duration_seconds, (int, float)) or duration_seconds <= 0:
        raise ValueError('duration_seconds must be a positive number')
    if not config.get('product_description') or not config.get('clips'):
        raise ValueError('product_description and clips are required')
    if config.get('product_crop'):
        x0,y0,x1,y1 = config['product_crop']
        if not (0 <= x0 < x1 <= 1 and 0 <= y0 < y1 <= 1):
            raise ValueError('product_crop must use normalized bounds inside the supplied image')
    for clip in config['clips']:
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', clip['slug']):
            raise ValueError('Invalid clip slug')
        for field in ['background', 'presenter', 'dialogue']:
            if not clip.get(field):
                raise ValueError('Missing clip field: '+field)
        if clip.get('presentation_mode','presenter') not in ['presenter','hands_only']:
            raise ValueError('presentation_mode must be presenter or hands_only')
        if 'scenes' not in clip:
            storyboard_module().talking_module().validate(config, clip)
        if 'scenes' in clip:
            storyboard_module().validate_scenes(config, clip)
            continue
        speed = clip.get('visual_speed', config.get('visual_speed',1.0))
        count = clip.get('scene_count', config.get('scene_count',2))
        if not 1.0 <= speed <= 2.0:
            raise ValueError('visual_speed must be between 1 and 2; slowing footage to fill duration is not allowed')
        required_scenes = math.ceil(duration_seconds*speed/10)
        if not isinstance(count,int) or not required_scenes <= count <= 6:
            raise ValueError('scene_count does not provide enough independent footage for the requested duration and speed')
        for field in ['shot_prompts','shot_motion']:
            if clip.get(field) and len(clip[field]) != count:
                raise ValueError(field+' must have one entry per scene')


def muse_headers():
    key = os.environ.get('MUSE2API_KEY')
    if not key:
        env = (PROJECT/'experiments/muse2api-czg86389/.env').read_text(encoding='utf-8-sig')
        key = next(line.split('=',1)[1].strip().strip('\"\'') for line in env.splitlines() if line.startswith('MUSE2API_KEY='))
    return {'Authorization': 'Bearer '+key}


def eleven_key():
    key = os.environ.get('ELEVENLABS_API_KEY')
    if key:
        return key
    secret = PROJECT/'.secrets/elevenlabs.dpapi.xml'
    if os.name != 'nt' or not secret.exists():
        raise ValueError('ElevenLabs credential unavailable: set ELEVENLABS_API_KEY')
    safe = str(secret).replace("'", "''")
    command = f"$taskStoredSecret=Import-Clixml -LiteralPath '{safe}'; [System.Net.NetworkCredential]::new('', $taskStoredSecret).Password"
    result = subprocess.run(['powershell.exe','-NoProfile','-NonInteractive','-Command',command], capture_output=True, text=True)
    if result.returncode or not result.stdout.strip():
        raise ValueError('Cannot decrypt local ElevenLabs credential for this Windows account')
    return result.stdout.strip()


def image_url(path):
    # Providers have returned WebP bytes with .png filenames. Upload a real PNG,
    # preserving the downloaded original separately for reproducibility.
    with Image.open(path) as image:
        buffer = io.BytesIO()
        image.convert('RGB').save(buffer, format='PNG')
    return 'data:image/png;base64,'+base64.b64encode(buffer.getvalue()).decode()


def storyboard_module():
    spec = importlib.util.spec_from_file_location('product_storyboard', Path(__file__).with_name('storyboard.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def clip_path(batch, index, clip):
    return batch/f'clip-{index:02}-{clip["slug"]}'


def task_media(batch, config, path, target, endpoint, payload):
    state_path = path/(target.stem+'-task.json')
    if target.exists():
        return
    headers = muse_headers()
    base = config.get('muse_base', 'http://127.0.0.1:18610').rstrip('/')
    cache_key = request_key(endpoint, payload)
    cached_media, cached_meta = cache_paths(MUSE_CACHE, cache_key, target.suffix or '.bin')
    if cache_enabled(config, 'muse') and cached_media.exists():
        shutil.copy2(cached_media, target)
        save_json(state_path, {'id': f'cache_{cache_key[:16]}', 'status': 'completed', 'progress': 100, 'cache_hit': True, 'cache_key': cache_key, 'cached_at': cached_meta.stat().st_mtime if cached_meta.exists() else None})
        print(path.name, target.name, 'MUSE_CACHE_HIT', cache_key[:12], flush=True)
        return
    # Persist an intent before POST. If interrupted in the acceptance window,
    # require reconciliation of the existing job instead of silently POSTing twice.
    pending = path/(target.stem+'-submission.json')
    if state_path.exists():
        state = read_json(state_path)
    else:
        if pending.exists():
            raise RuntimeError('Submission result uncertain. Reconcile local Muse task store before retry: '+str(pending))
        save_json(pending, {'endpoint': endpoint, 'prompt_sha256': hashlib.sha256(payload['prompt'].encode()).hexdigest(), 'intent_at': datetime.now().astimezone().isoformat()})
        if endpoint == '/v1/images/tasks':
            headers['Idempotency-Key'] = hashlib.sha256((str(batch)+str(target)).encode()).hexdigest()
        response = requests.post(base+endpoint, headers=headers, json=payload, timeout=90)
        if response.status_code >= 400:
            save_json(path/(target.stem+'-provider-error.json'), {'http_status': response.status_code, 'detail': response.text[:1200]})
            raise RuntimeError('Muse rejected request: HTTP '+str(response.status_code))
        state = response.json()
        state['cache_key'] = cache_key
        save_json(state_path, state)
    task_id = state['id']
    print(path.name, target.name, 'task', task_id, flush=True)
    last = None
    for _ in range(100):
        result = requests.get(base+endpoint+'/'+task_id, headers=headers, timeout=35)
        result.raise_for_status()
        state = result.json()
        signature = (state.get('status'),state.get('progress'))
        if signature != last:
            print(path.name, target.name, signature, flush=True)
            last = signature
        if state.get('status') == 'failed':
            save_json(state_path, state)
            raise RuntimeError(str(state.get('error','Muse task failed'))[:1000])
        if state.get('status') == 'completed':
            url = state.get('url') or state.get('result',{}).get('url') or state['data'][0]['url']
            media = requests.get(url, headers=muse_headers(), timeout=120)
            media.raise_for_status()
            staging = target.with_suffix('.download')
            staging.write_bytes(media.content)
            staging.replace(target)
            if cache_enabled(config, 'muse') and not cached_media.exists():
                shutil.copy2(target, cached_media)
                save_json(cached_meta, {'endpoint': endpoint, 'cache_key': cache_key, 'source_task': task_id, 'media_bytes': target.stat().st_size})
            save_json(state_path,state)
            return
        time.sleep(10)
    raise RuntimeError('Generation still pending. Resume this stage with the saved task ID.')


def voice(batch,config,index,clip):
    path = clip_path(batch,index,clip)
    target = path/'voice.mp3'
    if target.exists():
        return
    payload = {'text': clip['dialogue'], 'model_id':'eleven_v3','language_code':'vi','voice_settings':{'stability':0.5}, 'voice_id':'pNInz6obpgDQGcFmaJgB', 'output_format':'mp3_44100_128'}
    cache_key = request_key('elevenlabs-tts', payload)
    cached_voice, cached_meta = cache_paths(TTS_CACHE, cache_key, '.mp3')
    if cache_enabled(config, 'tts') and cached_voice.exists():
        shutil.copy2(cached_voice, target)
        save_json(path/'voice-info.json', {'provider':'ElevenLabs','model_id':'eleven_v3','voice':'Adam','cache_hit':True,'cache_key':cache_key,'cached_at':cached_meta.stat().st_mtime if cached_meta.exists() else None})
        print(path.name, 'TTS_CACHE_HIT', cache_key[:12], flush=True)
        return
    if (path/'voice-request.json').exists():
        raise RuntimeError('Prior TTS request unresolved. Inspect voice-request.json before a new billable call.')
    key = eleven_key()
    save_json(path/'voice-request.json', {'provider':'ElevenLabs','voice_id':'pNInz6obpgDQGcFmaJgB','model_id':'eleven_v3','text_sha256':hashlib.sha256(clip['dialogue'].encode()).hexdigest()})
    response = requests.post('https://api.elevenlabs.io/v1/text-to-speech/pNInz6obpgDQGcFmaJgB',params={'output_format':'mp3_44100_128'},headers={'xi-api-key':key,'Accept':'audio/mpeg'},json=payload,timeout=180)
    if response.status_code != 200:
        detail = response.text[:1000].replace(key,'[REDACTED]')
        save_json(path/'voice-provider-error.json', {'http_status':response.status_code,'detail':detail})
        raise RuntimeError('ElevenLabs HTTP '+str(response.status_code)+': '+detail)
    if not response.headers.get('content-type','').startswith('audio/'):
        raise RuntimeError('Expected audio response from ElevenLabs')
    target.write_bytes(response.content)
    if cache_enabled(config, 'tts') and not cached_voice.exists():
        shutil.copy2(target, cached_voice)
        save_json(cached_meta, {'provider':'ElevenLabs','model_id':'eleven_v3','voice':'Adam','cache_key':cache_key,'media_bytes':target.stat().st_size})
    save_json(path/'voice-info.json',{'provider':'ElevenLabs','model_id':'eleven_v3','voice':'Adam','request_id':response.headers.get('request-id'),'character_cost':response.headers.get('character-cost'),'cache_key':cache_key,'cache_hit':False})
    print(path.name,'Adam V3 ready',flush=True)


def opening(batch,config,index,clip):
    path = clip_path(batch,index,clip)
    hands_only = clip.get('presentation_mode') == 'hands_only'
    if hands_only:
        human = f'''HANDS-ONLY DEMONSTRATION: {clip['presenter']}. Show exactly one adult hand and a short section of forearm entering from the side edge of the image. The rest of the person is completely outside the camera view. NO face, head, hair, shoulders, chest, torso or full person anywhere, including glass, mirror, kettle and window reflections. One relaxed hand presents the product with an open palm beside it; fingers clear of product, no touching controls, no lifting. Natural wrist and anatomically plausible five fingers. Frame the tabletop and the product, not a person. There is no space in the shot for a face or body.'''
    else:
        human = f'''One fictional adult presenter: {clip['presenter']}. This is a newly invented character, not a likeness of any real individual. Presenter behind and beside the tabletop, waist-up visible, with a relaxed natural expression and hands resting safely beside the product. Adult presenter occupies the upper background.'''
    prompt = f'''Create a realistic vertical 9:16 product review opening photograph from the supplied product reference. Product identity: {config['product_description']}
New background: {clip['background']}
{human}
Do not obscure the kettle, front panel, spout, lid, logo or handle. Product occupies about 55 percent of frame height in the foreground with space on both sides for camera motion. Keep the whole product in frame, realistic scale, physically stable contact with the tabletop. No child, extra person, packaging, retail bag, text overlay or watermark. Use the reference for the exact product, not for the person or background. Preserve the exact visible product parts, color and branding; never invent additional features. {clip.get('staging','')}
High-quality natural product photography, soft realistic light. Clear front three-quarter view of the product, no unnatural hands or warped glass.'''
    if clip.get('opening_prompt'):
        prompt = clip['opening_prompt']
    (path/'opening-prompt.txt').write_text(prompt,encoding='utf-8')
    payload={'prompt':prompt,'size':'9:16','images':[{'url':image_url(batch/ref)} for ref in config['references']],'timeout':600}
    task_media(batch,config,path,path/'opening.png','/v1/images/tasks',payload)


def shot(batch,config,index,clip,number):
    path=clip_path(batch,index,clip)
    move = (
        'At medium-wide camera distance, sweep visibly from front-left through the front control panel toward the handle side, a 35-45 degree arc over ten seconds. Dolly OUT five percent to preserve clear margins. Show the front and handle side while keeping the entire kettle centered. No close-up.'
        if number == 1 else
        'A fresh medium-wide shot: travel briskly in the opposite direction from the front toward the spout side, a 25-35 degree arc over ten seconds, ending slightly higher to reveal the lid and glass jug. Keep a fixed distance, generous margins and the complete kettle centered. No close-up, no pan toward the presenter.'
    )
    if number == 3:
        move = 'A third new product-review angle: brisk smooth forward and slightly rising camera movement, about a ten percent push-in plus a 20-degree arc toward the lid and spout. Keep the complete product centered, including base and full handle, and end with a clear front three-quarter view. No static hold, no extreme close-up.'
    if clip.get('shot_motion'):
        move = clip['shot_motion'][number-1]
    if clip.get('presentation_mode') == 'hands_only':
        consistency = 'Maintain this exact room, lighting and the same one adult hand and sleeve. HANDS ONLY: no face, head, hair, shoulders, torso, full person or reflections of a face/body in any frame. The person stays entirely beyond the side edge of the picture; only hand and forearm are visible.'
        action = ('The single adult hand makes a clear, natural open-palm presentation beside the kettle, with one purposeful wrist turn, then settles. Keep five realistic fingers, no extra hands and no finger crossing over the product.' if number == 1 else 'The same single adult hand makes one brief, clear index-finger pointing gesture beside the control panel, without touching it, then returns to a relaxed open palm. Fingers never block the logo or display. Keep five realistic fingers and no extra hands.')
        if number == 3:
            action = 'The same single adult hand moves deliberately from an open palm beside the base to a relaxed presenting position beside the handle, then makes a short final presenting gesture. Do not grip or lift the kettle. Keep five realistic fingers and keep the hand separate from the product outline.'
        people = action + ' No pulling a full person into view; no camera movement up toward a face. Do not lift, unbox, operate, pour from or open the kettle. No speaking or lip-sync; narration is added separately.'
    else:
        consistency = 'Maintain this exact room, lighting and the same single fictional adult presenter throughout this clip. The person remains in the same clothes and place.'
        people = 'Presenter remains a quiet secondary background figure in the same position, with only natural blinking. Do not move attention or framing onto the face. No leaning, bending, walking, waving or following the camera. Hands stay still, clear of the product. Mouth stays relaxed; separate voice-over, no speaking or lip-sync. Do not pick up, pour from or operate the appliance.'
    prompt=f'''Generate a ten-second energetic realistic product-review shot from this exact opening photograph. Keep the product identity: {config['product_description']}
{consistency}
TARGET LOCK: track the KETTLE, not the person. Keep the kettle centered at the middle of the frame, with its complete base, spout, lid and handle within the central 80 percent of the frame, all the way to the final frame. If necessary reduce the orbit angle rather than let any part leave the image. {move}
The motion begins immediately and stays visibly active at normal speed, smooth gimbal tracking with natural background parallax. Brief gentle ease-in and ease-out only, no long static pauses, no ultra-slow motion, no abrupt jerk. The product stays rigid, stationary on the tabletop; camera moves around it. Do not show an invented rear view or spin it 360 degrees.
{people}
Preserve kettle shape, handle, lid, front controls, logo and digits consistently. No morphing, moving letters, boiling steam, scene changes, subtitles or added graphics. No music, narration or sound effects. Full-screen vertical 9:16, 720p, one continuous shot at normal camera speed.'''
    if clip.get('shot_prompts') and clip['shot_prompts'][number-1]:
        prompt = clip['shot_prompts'][number-1]
    (path/f'scene-{number:02}-prompt.txt').write_text(prompt,encoding='utf-8')
    target=path/f'scene-{number:02}.mp4'
    task_media(batch,config,path,target,'/v1/videos',{'prompt':prompt,'duration':10,'size':'9:16','resolution':'720p','reference_image':image_url(path/'opening.png')})
    run_ff([FF,'-y','-i',str(target),'-vf','fps=1/2,scale=216:384,tile=5x1','-frames:v','1',str(path/f'scene-{number:02}-contact-sheet.jpg')])


def run_ff(command):
    result=subprocess.run(command,capture_output=True,text=True,encoding='utf-8',errors='replace')
    if result.returncode:
        raise RuntimeError(result.stderr[-1800:])
    return result


def duration(path):
    result=subprocess.run([FF,'-hide_banner','-i',str(path)],capture_output=True,text=True,encoding='utf-8',errors='replace')
    match=re.search(r'Duration: (\d+):(\d+):(\d+\.\d+)',result.stderr)
    if not match: raise RuntimeError('Cannot read media duration: '+str(path))
    return int(match[1])*3600+int(match[2])*60+float(match[3])


def plan(batch, config, selected):
    """Count billable provider calls before executing a batch."""
    rows = []
    totals = {'tts_calls': 0, 'opening_image_calls': 0, 'video_scene_calls': 0, 'cache_hits': 0, 'local_steps': 0, 'optional_llm_calls': 0}
    for index, clip in selected:
        path = clip_path(batch, index, clip)
        count = clip.get('scene_count', config.get('scene_count', 2))
        tts_payload = {'text': clip['dialogue'], 'model_id':'eleven_v3','language_code':'vi','voice_settings':{'stability':0.5}, 'voice_id':'pNInz6obpgDQGcFmaJgB', 'output_format':'mp3_44100_128'}
        tts_key = request_key('elevenlabs-tts', tts_payload)
        tts_cache, _ = cache_paths(TTS_CACHE, tts_key, '.mp3')
        tts_needed = not (path/'voice.mp3').exists()
        tts_hit = tts_needed and cache_enabled(config,'tts') and tts_cache.exists()
        opening_needed = not (path/'opening.png').exists()
        opening_prompt = path/'opening-prompt.txt'
        opening_key_known = opening_prompt.exists()
        scene_missing = [n for n in range(1,count+1) if not (path/f'scene-{n:02}.mp4').exists()]
        row = {'clip': path.name, 'tts': 'cache_hit' if tts_hit else ('call' if tts_needed else 'ready'), 'opening_image': 'call' if opening_needed else 'ready', 'video_scenes': len(scene_missing), 'scene_count': count, 'visual_speed': clip.get('visual_speed',config.get('visual_speed',1.0)), 'cache_key_available_for_opening': opening_key_known}
        rows.append(row)
        totals['tts_calls'] += int(tts_needed and not tts_hit)
        totals['opening_image_calls'] += int(opening_needed)
        totals['video_scene_calls'] += len(scene_missing)
        totals['cache_hits'] += int((not tts_needed) or tts_hit)
        totals['local_steps'] += 1 + len(scene_missing) + int(opening_needed)
    # Script and prompt creation can be done locally from supplied fields; only an
    # optional LLM copywriting pass would be billable and is off by default.
    report = {'batch': str(batch), 'provider_calls_if_run_now': totals['tts_calls'] + totals['opening_image_calls'] + totals['video_scene_calls'], 'provider_calls_by_kind': {key:value for key,value in totals.items() if key.endswith('_calls')}, 'cache_hits': totals['cache_hits'], 'local_steps': totals['local_steps'], 'optional_llm_calls': 0, 'llm_policy': 'off_when_dialogue_and_product_description_are supplied', 'clips': rows, 'cache_root': str(CACHE_ROOT), 'generated_at': datetime.now().astimezone().isoformat()}
    save_json(batch/'cost-plan.json', report)
    print(json.dumps(report, ensure_ascii=False, indent=2), flush=True)
    return report


def warm_cache(batch, config):
    """Index already-generated local artifacts without making provider calls."""
    indexed = {'tts': 0, 'media': 0, 'skipped': 0}
    for index, clip in enumerate(config['clips'], 1):
        path = clip_path(batch, index, clip)
        voice = path/'voice.mp3'
        if voice.exists() and (path/'dialogue.txt').exists():
            payload = {'text': clip['dialogue'], 'model_id':'eleven_v3','language_code':'vi','voice_settings':{'stability':0.5}, 'voice_id':'pNInz6obpgDQGcFmaJgB', 'output_format':'mp3_44100_128'}
            key = request_key('elevenlabs-tts', payload)
            target, meta = cache_paths(TTS_CACHE, key, '.mp3')
            if not target.exists():
                shutil.copy2(voice, target)
                save_json(meta, {'provider':'ElevenLabs','cache_key':key,'source':str(voice),'media_bytes':voice.stat().st_size,'warmed_without_provider_call':True})
                indexed['tts'] += 1
            else:
                indexed['skipped'] += 1
        else:
            indexed['skipped'] += 1
    save_json(batch/'cache-index.json', {'indexed':indexed,'cache_root':str(CACHE_ROOT),'provider_calls':0,'generated_at':datetime.now().astimezone().isoformat()})
    print(json.dumps(indexed, ensure_ascii=False, indent=2), flush=True)


def render(batch,config,index,clip):
    path=clip_path(batch,index,clip)
    output_duration=float(config.get('duration_seconds',20))
    count=clip.get('scene_count',config.get('scene_count',2))
    speed=clip.get('visual_speed',config.get('visual_speed',1.0))
    sources=[path/f'scene-{n:02}.mp4' for n in range(1,count+1)]
    durations=[duration(p) for p in sources]
    if any(d < 9.96 for d in durations):
        raise RuntimeError('A generated scene is shorter than 10 seconds. Generate a new scene; never pad by looping or slowing it down.')
    audio_duration=duration(path/'voice.mp3')
    tempo=max(1.0,audio_duration/(output_duration-0.2))
    if tempo>1.25:
        raise RuntimeError('Dialogue too long; revise or extend with new footage, do not clip spoken words.')
    target=path/'final.mp4'
    filters=[]
    seconds_per_scene=output_duration*speed/count
    for n in range(count):
        filters.append(f'[{n}:v]trim=duration={seconds_per_scene:.8f},setpts=(PTS-STARTPTS)/{speed:.8f},scale=720:1280:force_original_aspect_ratio=increase:force_divisible_by=2,crop=720:1280,setsar=1,fps=30[v{n}]')
    filters.append(''.join(f'[v{n}]' for n in range(count))+f'concat=n={count}:v=1:a=0[v]')
    filters.append(f'[{count}:a]atempo={tempo:.8f},apad,atrim=duration={output_duration:.3f}[a]')
    command=[FF,'-y']
    for source in sources: command.extend(['-i',str(source)])
    command.extend(['-i',str(path/'voice.mp3'),'-filter_complex',';'.join(filters),'-map','[v]','-map','[a]','-c:v','libx264','-crf','18','-preset','fast','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-t',f'{output_duration:.3f}','-movflags','+faststart',str(target)])
    run_ff(command)
    run_ff([FF,'-v','error','-i',str(target),'-f','null','-'])
    final_duration=duration(target)
    if abs(final_duration-output_duration)>0.1: raise RuntimeError('Unexpected output duration')
    run_ff([FF,'-y','-i',str(target),'-vf','fps=1/2,scale=144:256,tile=5x2','-frames:v','1',str(path/'contact-sheet.jpg')])
    save_json(path/'verification.json',{'final_seconds':final_duration,'resolution':'720x1280','fps':30,'source_seconds':durations,'visual_speed':speed,'looped':False,'independent_scenes':count,'audio_seconds':audio_duration,'audio_tempo':tempo,'full_dialogue_preserved':True,'decode_check':'passed','visual_qa':'pending human/agent review of sampled frames','sha256':hashlib.sha256(target.read_bytes()).hexdigest()})
    print('READY',target,flush=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('stage',choices=['init','plan','cache','characters','images','voices','videos','render','status'])
    parser.add_argument('--config')
    parser.add_argument('--image')
    parser.add_argument('--output')
    parser.add_argument('--batch')
    parser.add_argument('--clip',type=int)
    parser.add_argument('--scene',type=int,choices=range(1,7))
    args=parser.parse_args()
    if args.stage=='init':
        if not all([args.config,args.image,args.output]): parser.error('init requires --config --image --output')
        initialize(args)
        return
    if not args.batch: parser.error('--batch required')
    batch=Path(args.batch).resolve()
    config=read_json(batch/'batch.json')
    validate(config)
    if args.clip is not None and not 1<=args.clip<=len(config['clips']): parser.error('clip index out of bounds')
    selected=[(i,c) for i,c in enumerate(config['clips'],1) if args.clip is None or args.clip==i]
    if any('scenes' in clip for _, clip in selected):
        if not all('scenes' in clip for _, clip in selected):
            parser.error('Select a single workflow type using --clip; do not mix legacy and storyboard clips.')
        import sys
        storyboard_module().execute(sys.modules[__name__], args, batch, config, selected)
        return
    if args.stage=='plan':
        plan(batch, config, selected)
    elif args.stage=='cache':
        warm_cache(batch, config)
    elif args.stage=='voices':
        with ThreadPoolExecutor(max_workers=2) as pool:
            jobs=[pool.submit(voice,batch,config,i,c) for i,c in selected]
            for job in jobs: job.result()
    else:
        for index,clip in selected:
            if args.stage=='images': opening(batch,config,index,clip)
            elif args.stage=='videos':
                count=clip.get('scene_count',config.get('scene_count',2))
                if args.scene is not None and args.scene>count: parser.error('scene exceeds this clip scene_count')
                for number in ([args.scene] if args.scene else range(1,count+1)): shot(batch,config,index,clip,number)
            elif args.stage=='render': render(batch,config,index,clip)
            elif args.stage=='status':
                path=clip_path(batch,index,clip)
                count=clip.get('scene_count',config.get('scene_count',2))
                files=['opening.png','voice.mp3']+[f'scene-{n:02}.mp4' for n in range(1,count+1)]+['final.mp4','verification.json']
                print(path.name,json.dumps({name:(path/name).exists() for name in files}))


if __name__=='__main__': main()
