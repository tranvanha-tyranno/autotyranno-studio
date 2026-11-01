"""Reusable scene-specific product review workflow learned from real batch QA.

The legacy runner remains compatible. A clip with `scenes` uses separate opening
images and narration takes, explicit timing, original-product video references,
and an image-review gate before any billable video submission.
"""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import hashlib
import math
from pathlib import Path
import re
import importlib.util

PRODUCT_LOCK = (
    "【最终执行规则，覆盖上面自动附加的通用“纯净画面要求”】："
    "忽略上文“清除参考图中的所有文字”及“绝对纯净无字”的要求，"
    "它们是通用模板，本任务不适用。只去掉后加的字幕、水印、签名和背景广告；"
    "必须保留产品本身原有的白色电量数字、刻度、标签及黑色显示窗。"
    "本任务已明确选择保留原机标记，不存在待确认的选项。直接生成所要求的照片。 "
    "Preserve the original physical product geometry, existing factory lettering, "
    "ports, finish and visible display from the product reference. The generic "
    "clean-image instruction applies only to added overlays and watermarks, not "
    "to original product labels or display markings. Add no invented brand, "
    "numbers, charging performance, connectors or extra accessories. Generate "
    "the requested photograph; retain original physical details."
)
LIGHTING_LOCK = (
    "EXPOSURE CONTINUITY: identical bright diffuse studio illumination from the "
    "first to the last frame, locked camera exposure and white balance, no auto "
    "exposure ramp, no fade, vignette, dramatic grading, dimming or moving shadows. "
    "Preserve the opening photograph's product/skin brightness and colors. Camera "
    "motion must not cause the face, clothes or product to gradually darken."
)


def quality_module():
    spec = importlib.util.spec_from_file_location('product_video_quality', Path(__file__).with_name('quality.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def talking_module():
    spec = importlib.util.spec_from_file_location('product_video_talking', Path(__file__).with_name('talking_review.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def local_reference(batch, name):
    path = (batch/name).resolve()
    if not path.is_relative_to(batch.resolve()):
        raise ValueError('Reference must stay inside its batch')
    return path


def character_path(batch, config):
    return local_reference(batch, config['character'].get('reference', 'character/portrait.png'))


def asset_review_valid(runner, image):
    receipt = image.with_name(image.stem+'-review.json')
    if not image.exists() or not receipt.exists():
        return False
    review = runner.read_json(receipt)
    return review.get('result') == 'accepted' and review.get('sha256') == hashlib.sha256(image.read_bytes()).hexdigest()


def require_character(runner, batch, config):
    image = character_path(batch, config)
    if not asset_review_valid(runner, image):
        raise ValueError('Generate and inspect canonical character portrait before scene images/videos: '+str(image))
    return image


def characters(runner, batch, config):
    character = config.get('character')
    if not character:
        raise ValueError('characters stage requires a canonical character prompt in batch.json')
    path = character_path(batch, config)
    path.parent.mkdir(parents=True, exist_ok=True)
    (path.with_name('portrait-prompt.txt')).write_text(character['prompt'], encoding='utf-8')
    runner.task_media(batch, config, path.parent, path, '/v1/images/tasks',
                      {'prompt': character['prompt'], 'size': '9:16', 'timeout': 600})


def validate_scenes(config, clip):
    if config.get('recipe_version', 0) >= 5 and clip.get('presentation_mode', 'presenter') == 'presenter' and not config.get('character'):
        raise ValueError('Presenter storyboard version 5 requires a canonical character before scene images')
    if config.get('character') and not config['character'].get('prompt', '').strip():
        raise ValueError('Canonical character requires a nonempty prompt')
    if not isinstance(clip.get('text_overlays', config.get('text_overlays', False)), bool):
        raise ValueError('text_overlays must be true or false')
    scenes = clip['scenes']
    if not isinstance(scenes, list) or not 1 <= len(scenes) <= 6:
        raise ValueError('scenes must contain one to six independent scenes')
    total = 0
    for scene in scenes:
        if not isinstance(scene.get('revision', 1), int) or scene.get('revision', 1) < 1:
            raise ValueError('Scene revision must be a positive integer')
        for field in ('dialogue', 'opening_prompt', 'video_prompt'):
            if not isinstance(scene.get(field), str) or not scene[field].strip():
                raise ValueError('Each scene requires nonempty '+field)
        seconds = scene.get('seconds', 0)
        speed = scene.get('visual_speed', clip.get('visual_speed', config.get('visual_speed', 1.5)))
        start = scene.get('source_start', 0)
        if not isinstance(seconds, (int, float)) or not math.isfinite(seconds) or seconds <= 0:
            raise ValueError('Each scene needs a positive finite seconds value')
        if not isinstance(speed, (int, float)) or not math.isfinite(speed) or not 1 <= speed <= 2:
            raise ValueError('Scene visual_speed must be between 1 and 2')
        if not isinstance(start, (int, float)) or not math.isfinite(start) or start < 0 or start + seconds*speed > 10.001:
            raise ValueError('Scene requests more than ten seconds of independent source footage')
        if 'audio_segments' in scene:
            segments = scene['audio_segments']
            if not isinstance(segments, list) or not segments:
                raise ValueError('audio_segments must be nonempty measured speech-preserving ranges')
            last_end = 0
            for segment in segments:
                if (not isinstance(segment, list) or len(segment) != 2
                        or any(not isinstance(value, (float, int)) or not math.isfinite(value) for value in segment)
                        or not last_end <= segment[0] < segment[1]):
                    raise ValueError('audio_segments must be ordered, nonoverlapping positive ranges')
                last_end = segment[1]
        total += seconds
    if abs(total-config.get('duration_seconds', 20)) > .001:
        raise ValueError('Scene durations must sum to duration_seconds')
    if clip['dialogue'].strip() != '\n\n'.join(s['dialogue'].strip() for s in scenes):
        raise ValueError('clip dialogue must match the scene narration exactly')
    marketing = clip.get('marketing')
    if marketing:
        for field in ('hook', 'cta', 'buyer_benefit', 'reason_to_believe'):
            if not isinstance(marketing.get(field), str) or not marketing[field].strip():
                raise ValueError('Marketing requires '+field)
        if not 0 < marketing.get('hook_seconds', 0) <= 3:
            raise ValueError('Marketing hook must fit the first three seconds')
        speech = lambda text: re.sub(r'\[[^\]]*\]\s*', '', text).strip()
        if not speech(scenes[0]['dialogue']).startswith(marketing['hook'].strip()):
            raise ValueError('First narration must start with the marketing hook')
        if not speech(scenes[-1]['dialogue']).endswith(marketing['cta'].strip()):
            raise ValueError('Last narration must end with the purchase CTA')
    talking_module().validate(config, clip)


def folder(runner, batch, index, clip, number):
    revision = clip['scenes'][number-1].get('revision', 1)
    suffix = f'-r{revision:02}' if revision > 1 else ''
    return runner.clip_path(batch, index, clip)/f'scene-{number:02}{suffix}'


def tts_clip(scene):
    return {'slug': 'narration', 'dialogue': scene['dialogue']}


def voice_folder(runner, path):
    return runner.clip_path(path, 1, {'slug': 'narration'})


def voice_payload(scene):
    return {'text': scene['dialogue'], 'model_id': 'eleven_v3', 'language_code': 'vi',
            'voice_settings': {'stability': .5}, 'voice_id': 'pNInz6obpgDQGcFmaJgB',
            'output_format': 'mp3_44100_128'}


def opening_payload(runner, batch, config, index, clip, number):
    scene = clip['scenes'][number-1]
    # Only the selected product crop goes to the provider if available. Do not
    # re-introduce all four color variants from the source collage.
    refs = [batch/config['references'][0]]
    if config.get('character'):
        refs.append(require_character(runner, batch, config))
    elif number > 1:
        anchor = folder(runner, batch, index, clip, 1)/'opening.png'
        if not anchor.exists():
            raise ValueError('Scene one opening image is needed for presenter continuity')
        refs.append(anchor)
    return {'prompt': scene['opening_prompt']+talking_module().direction(config, scene), 'size': '9:16', 'timeout': 600,
            'images': [{'url': runner.image_url(ref)} for ref in refs],
            'extra': PRODUCT_LOCK}


def video_payload(runner, batch, config, path, scene):
    references = [path/'opening.png', batch/config['references'][0]]
    if config.get('character'):
        references.append(require_character(runner, batch, config))
    elif scene.get('presenter_reference'):
        anchor = (batch/scene['presenter_reference']).resolve()
        if not anchor.is_relative_to(batch.resolve()) or not anchor.is_file():
            raise ValueError('presenter_reference must name an existing image inside this batch')
        references.append(anchor)
    prompt = scene['video_prompt']+talking_module().direction(config, scene)
    if config.get('quality', {}).get('lock_exposure'):
        prompt += '\n'+LIGHTING_LOCK
    return {'prompt': prompt, 'duration': 10, 'size': '9:16',
            'resolution': '720p', 'images': [{'url': runner.image_url(ref)} for ref in references]}


def approval_valid(runner, path):
    image = path/'opening.png'
    receipt = path/'opening-review.json'
    return image.exists() and receipt.exists() and (
        runner.read_json(receipt).get('sha256') == hashlib.sha256(image.read_bytes()).hexdigest()
        and runner.read_json(receipt).get('result') == 'accepted'
    )


def require_approval(runner, path):
    if not approval_valid(runner, path):
        raise ValueError('Inspect opening image and save opening-review.json with result=accepted, notes and matching sha256 before creating video: '+str(path))


def available(runner, config, target, endpoint, payload):
    if target.exists():
        return 'ready'
    if payload and runner.cache_enabled(config, 'tts' if endpoint == 'elevenlabs-tts' else 'muse'):
        root = runner.TTS_CACHE if endpoint == 'elevenlabs-tts' else runner.MUSE_CACHE
        suffix = '.mp3' if endpoint == 'elevenlabs-tts' else target.suffix
        key = runner.request_key(endpoint, payload)
        if (root/f'{key}{suffix}').exists():
            return 'cache_hit'
    return 'call'


def plan(runner, batch, config, selected):
    rows, calls, hits, pending = [], {'tts_calls': 0, 'character_image_calls': 0, 'opening_image_calls': 0, 'video_scene_calls': 0, 'optional_llm_calls': 0}, 0, 0
    character_ready = not config.get('character') or asset_review_valid(runner, character_path(batch, config))
    if config.get('character'):
        target = character_path(batch, config)
        payload = {'prompt': config['character']['prompt'], 'size': '9:16', 'timeout': 600}
        state_file = target.with_name(target.stem+'-task.json')
        state = 'resume_saved_task' if not target.exists() and state_file.exists() else available(runner, config, target, '/v1/images/tasks', payload)
        calls['character_image_calls'] = int(state == 'call')
        pending += int(state == 'resume_saved_task')
    for index, clip in selected:
        for number, scene in enumerate(clip['scenes'], 1):
            path = folder(runner, batch, index, clip, number)
            vf = voice_folder(runner, path)
            image_payload = None
            if character_ready and (config.get('character') or number == 1 or (folder(runner, batch, index, clip, 1)/'opening.png').exists()):
                image_payload = opening_payload(runner, batch, config, index, clip, number)
            vp = video_payload(runner, batch, config, path, scene) if character_ready and (path/'opening.png').exists() else None
            row = {'clip': index, 'scene': number, 'seconds': scene['seconds'],
                   'opening_reviewed': approval_valid(runner, path)}
            if talking_module().mode(config, clip, scene) == 'lip_sync':
                row['lip_sync'] = 'requires_actual_audio_driven_engine_and_review'
                row['lip_sync_provider_cost'] = 'unknown; excluded from Muse/TTS submission counts'
            for name, target, endpoint, payload, key in [
                ('tts', vf/'voice.mp3', 'elevenlabs-tts', voice_payload(scene), 'tts_calls'),
                ('image', path/'opening.png', '/v1/images/tasks', image_payload, 'opening_image_calls'),
                ('video', path/'source.mp4', '/v1/videos', vp, 'video_scene_calls'),
            ]:
                state_file = target.with_name(target.stem+'-task.json')
                if not target.exists() and state_file.exists():
                    state = runner.read_json(state_file).get('status')
                    row[name] = 'failed_saved_task' if state == 'failed' else 'resume_saved_task'
                    pending += 1
                else:
                    row[name] = available(runner, config, target, endpoint, payload)
                    calls[key] += int(row[name] == 'call')
                    hits += int(row[name] == 'cache_hit')
            rows.append(row)
    report = {'provider_calls_if_run_now': sum(calls.values()), 'provider_calls_by_kind': calls,
              'canonical_character_reviewed': character_ready if config.get('character') else None,
              'saved_tasks_to_resume_or_inspect': pending, 'cache_hits': hits,
              'scenes': rows, 'unknown_dependent_keys': 'Future opening/video inputs are conservatively counted as calls until reference bytes exist.',
              'money': 'Counts are provider submissions, not a currency estimate.',
              'generated_at': datetime.now().astimezone().isoformat()}
    if any(row.get('lip_sync') for row in rows):
        report['lip_sync'] = {
            'required_scenes': sum(bool(row.get('lip_sync')) for row in rows),
            'engine_status': 'external_audio_driven_engine_not_connected',
            'additional_calls_and_cost': 'unknown; excluded from provider_calls_if_run_now',
            'ready_to_deliver': False,
        }
    runner.save_json(batch/'cost-plan.json', report)
    print(__import__('json').dumps(report, ensure_ascii=False, indent=2), flush=True)
    return report


def warm_cache(runner, batch, config, selected):
    count = 0
    for index, clip in selected:
        for number, scene in enumerate(clip['scenes'], 1):
            vf = voice_folder(runner, folder(runner, batch, index, clip, number))
            target = vf/'voice.mp3'
            # Only attribute an old voice to this exact script when its saved
            # script agrees; do not mislabel stale audio after manifest edits.
            if target.exists() and (vf/'dialogue.txt').read_text(encoding='utf-8').strip() == scene['dialogue'].strip():
                key = runner.request_key('elevenlabs-tts', voice_payload(scene))
                media, meta = runner.cache_paths(runner.TTS_CACHE, key, '.mp3')
                if not media.exists():
                    __import__('shutil').copy2(target, media)
                    runner.save_json(meta, {'cache_key': key, 'source': str(target), 'warmed_without_provider_call': True})
                    count += 1
    runner.save_json(batch/'cache-index.json', {'tts_indexed': count, 'provider_calls': 0})
    print('CACHE', count, flush=True)


def voice(runner, batch, config, index, clip, number):
    scene = clip['scenes'][number-1]
    path = folder(runner, batch, index, clip, number)
    vf = voice_folder(runner, path)
    vf.mkdir(parents=True, exist_ok=True)
    text = vf/'dialogue.txt'
    if text.exists() and text.read_text(encoding='utf-8').strip() != scene['dialogue'].strip():
        raise ValueError('Narration changed: use a new revision folder rather than reuse stale voice')
    text.write_text(scene['dialogue'], encoding='utf-8')
    runner.voice(path, config, 1, tts_clip(scene))
    print('VOICE', number, runner.duration(vf/'voice.mp3'), flush=True)


def opening(runner, batch, config, index, clip, number):
    path = folder(runner, batch, index, clip, number)
    path.mkdir(parents=True, exist_ok=True)
    payload = opening_payload(runner, batch, config, index, clip, number)
    runner.task_media(batch, config, path, path/'opening.png', '/v1/images/tasks', payload)


def shot(runner, batch, config, index, clip, number):
    path = folder(runner, batch, index, clip, number)
    require_approval(runner, path)
    runner.task_media(batch, config, path, path/'source.mp4', '/v1/videos',
                      video_payload(runner, batch, config, path, clip['scenes'][number-1]))
    if runner.duration(path/'source.mp4') < 9.96:
        raise ValueError('Provider returned less than ten seconds; do not loop or slow footage')
    runner.run_ff([runner.FF, '-y', '-i', str(path/'source.mp4'), '-vf',
                   'fps=1/2,scale=216:384,tile=5x1', '-frames:v', '1', str(path/'contact-sheet.jpg')])
    runner.run_ff([runner.FF, '-y', '-i', str(path/'source.mp4'), '-vf',
                   'fps=2,scale=216:384,tile=5x4', '-frames:v', '1', str(path/'action-sheet.jpg')])
    print('SCENE_READY', number, flush=True)


def caption_card(path, scene):
    """Draw crisp Vietnamese titles locally, keeping the provider out of text."""
    from PIL import Image, ImageDraw, ImageFont
    card = Image.new('RGBA', (720, 1280))
    draw = ImageDraw.Draw(card)
    label = scene.get('on_screen', {})
    title = label.get('title', '')
    subtitle = label.get('subtitle', '')
    if title or subtitle:
        top = 90 if label.get('position') == 'top' else 1020
        font_path = Path('C:/Windows/Fonts/arialbd.ttf')
        fallback = Path('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf')
        font_path = font_path if font_path.exists() else fallback
        def wrapped(text, size):
            font = ImageFont.truetype(str(font_path), size)
            lines = ['']
            for word in text.split():
                candidate = (lines[-1]+' '+word).strip()
                if draw.textbbox((0, 0), candidate, font=font)[2] > 610 and lines[-1]:
                    lines.append(word)
                else:
                    lines[-1] = candidate
            return lines, font
        title_lines, title_font = wrapped(title, 34)
        sub_lines, sub_font = wrapped(subtitle, 22)
        height = len(title_lines)*43 + (len(sub_lines)*29+12 if subtitle else 0)+36
        if top+height > 1240:
            top = 1240-height
        draw.rounded_rectangle((30, top, 690, top+height), radius=22, fill=(20, 15, 44, 231))
        y = top+16
        for text in title_lines:
            draw.text((54, y), text, font=title_font, fill=(255, 241, 148))
            y += 43
        if subtitle:
            y += 10
            for text in sub_lines:
                draw.text((54, y), text, font=sub_font, fill='white')
                y += 29
    target = path/'caption.png'
    card.save(target)
    return target


def render(runner, batch, config, index, clip):
    if config.get('character'):
        require_character(runner, batch, config)
    path = runner.clip_path(batch, index, clip)
    scenes, filters, audio_filters, sources, audios, timings, cards = clip['scenes'], [], [], [], [], [], []
    count = len(scenes)
    overlays = clip.get('text_overlays', config.get('text_overlays', False))
    exposure_settings = config.get('quality', {}).get('exposure_lock')
    exposure_reports = []
    for number, scene in enumerate(scenes, 1):
        sf = folder(runner, batch, index, clip, number)
        source = sf/'source.mp4'
        audio = voice_folder(runner, sf)/'voice.mp3'
        require_approval(runner, sf)
        reviewed_interval = None
        if config.get('quality', {}).get('require_video_review'):
            review_path = sf/'video-review.json'
            if not review_path.exists():
                raise ValueError('Inspect generated motion and save video-review.json before rendering: '+str(sf))
            review = runner.read_json(review_path)
            if not review.get('result', '').startswith('accepted') or review.get('source_sha256') != hashlib.sha256(source.read_bytes()).hexdigest():
                raise ValueError('Video review rejected or stale: '+str(sf))
            reviewed_interval = review.get('reviewed_interval_seconds')
        script = audio.with_name('dialogue.txt')
        if not script.exists() or script.read_text(encoding='utf-8').strip() != scene['dialogue'].strip():
            raise ValueError(f'Scene {number} audio script is stale or missing; regenerate that narration before rendering')
        source_seconds, audio_seconds = runner.duration(source), runner.duration(audio)
        speed = scene.get('visual_speed', clip.get('visual_speed', config.get('visual_speed', 1.5)))
        start = scene.get('source_start', 0)
        seconds = scene['seconds']
        if source_seconds < 9.96 or start+seconds*speed > source_seconds+.02:
            raise ValueError('Insufficient independent footage; never slow or loop to fill')
        if reviewed_interval is not None:
            if (not isinstance(reviewed_interval, list) or len(reviewed_interval) != 2
                    or not 0 <= reviewed_interval[0] < reviewed_interval[1] <= source_seconds+.02
                    or start < reviewed_interval[0]-.001
                    or start+seconds*speed > reviewed_interval[1]+.001):
                raise ValueError('Scene extends beyond the visually accepted source interval: '+str(sf))
        audio_segments = scene.get('audio_segments', [[0, audio_seconds]])
        if any(end > audio_seconds+.001 for _, end in audio_segments):
            raise ValueError('audio_segments exceed original narration duration')
        used_audio_seconds = sum(end-begin for begin, end in audio_segments)
        tempo = max(1.0, used_audio_seconds/(seconds-.06))
        if tempo > 1.25:
            raise ValueError(f'Scene {number} narration too long ({audio_seconds}s); revise only that scene or extend its duration')
        n = number-1
        exposure = None
        speech_mode = talking_module().mode(config, clip, scene)
        if speech_mode == 'lip_sync':
            # Speed changes, pause cleanup and grading happen BEFORE mouth sync.
            # Render uses the exact timed audio and never retimes a synced mouth.
            source, audio = talking_module().require_synced(
                runner, runner.storyboard_module(), batch, config, index, clip, number)
            speed, start, tempo, audio_segments = 1., 0., 1., [[0, seconds]]
        if exposure_settings is not None and speech_mode != 'lip_sync':
            exposure_scene = dict(scene, visual_speed=speed)
            exposure = quality_module().exposure_plan(runner.FF, source, sf/'opening.png', exposure_scene, exposure_settings)
            runner.save_json(sf/'exposure-plan.json', exposure)
            exposure_reports.append({'scene': number, 'report': str((sf/'exposure-plan.json').relative_to(batch)),
                                     'end_to_opening_ratio': exposure['end_to_opening_ratio'],
                                     'needs_attention': exposure['needs_attention']})
        # Fit inside the vertical canvas rather than cropping product margins.
        # A synchronized scene is already 30 fps on the final audio timeline.
        # Running fps a second time can drop its endpoint frame.
        fps_filter = '' if speech_mode == 'lip_sync' else ',fps=30:eof_action=pass'
        filters.append(
            f'[{n}:v]trim=start={start:.8f}:duration={seconds*speed:.8f},setpts=(PTS-STARTPTS)/{speed:.8f},'
            'scale=720:1280:force_original_aspect_ratio=decrease:force_divisible_by=2,'
            f'pad=720:1280:(ow-iw)/2:(oh-ih)/2,setsar=1{fps_filter}[ungraded{n}]')
        if exposure is not None:
            filters.extend(quality_module().exposure_filters(
                f'ungraded{n}', f'base{n}', exposure, f'exposure{n}_'))
        else:
            filters.append(f'[ungraded{n}]null[base{n}]')
        if overlays:
            overlay_seconds = scene.get('on_screen', {}).get('seconds', seconds)
            filters.append(
                f'[{count*2+n}:v]format=rgba[card{n}];'
                f"[base{n}][card{n}]overlay=0:0:shortest=1:enable='between(t,0,{overlay_seconds:.8f})'[v{n}]")
            cards.append(caption_card(sf, scene))
        else:
            filters.append(f'[base{n}]null[v{n}]')
        if 'audio_segments' in scene and speech_mode != 'lip_sync':
            audio_filters.append(f'[{count+n}:a]asplit={len(audio_segments)}'+''.join(f'[as{n}_{j}]' for j in range(len(audio_segments))))
            for j, (begin, end) in enumerate(audio_segments):
                audio_filters.append(f'[as{n}_{j}]atrim=start={begin:.8f}:end={end:.8f},asetpts=PTS-STARTPTS[ac{n}_{j}]')
            audio_filters.append(''.join(f'[ac{n}_{j}]' for j in range(len(audio_segments)))+f'concat=n={len(audio_segments)}:v=0:a=1[asource{n}]')
            audio_label = f'asource{n}'
        else:
            audio_label = f'{count+n}:a'
        audio_filters.append(
            f'[{audio_label}]asetpts=PTS-STARTPTS,atempo={tempo:.8f},'
            f'apad,atrim=duration={seconds:.8f},aresample=48000[a{n}]')
        sources.append(source)
        audios.append(audio)
        timings.append({'scene': number, 'seconds': seconds, 'source_seconds': source_seconds,
                        'source_start': start, 'used_source_seconds': seconds*speed,
                        'visual_speed': speed, 'voice_seconds': audio_seconds, 'audio_tempo': tempo,
                        'audio_segments': audio_segments, 'used_audio_seconds': used_audio_seconds,
                        'speech_mode': speech_mode})
    filters.extend(audio_filters)
    filters.append(''.join(f'[v{n}]' for n in range(count))+f'concat=n={count}:v=1:a=0[v]')
    filters.append(''.join(f'[a{n}]' for n in range(count))+f'concat=n={count}:v=0:a=1,loudnorm=I=-16:TP=-1.5:LRA=9[a]')
    command = [runner.FF, '-y']
    for source in sources+audios:
        command += ['-i', str(source)]
    for card in cards:
        command += ['-loop', '1', '-i', str(card)]
    target = path/'final.mp4'
    seconds = config['duration_seconds']
    command += ['-filter_complex', ';'.join(filters), '-map', '[v]', '-map', '[a]',
                '-c:v', 'libx264', '-crf', '18', '-preset', 'fast', '-pix_fmt', 'yuv420p',
                '-c:a', 'aac', '-b:a', '192k', '-t', str(seconds),
                '-movflags', '+faststart', str(target)]
    runner.run_ff(command)
    qa = runner.run_ff([runner.FF, '-hide_banner', '-i', str(target), '-vf',
                        'blackdetect=d=0.2:pix_th=0.1,freezedetect=n=-45dB:d=1',
                        '-af', 'volumedetect', '-f', 'null', '-'])
    if abs(runner.duration(target)-seconds) > .1:
        raise ValueError('Final duration does not match storyboard')
    frame_counts = re.findall(r'\bframe=\s*(\d+)', qa.stderr)
    video_frames = int(frame_counts[-1]) if frame_counts else None
    if video_frames is None or abs(video_frames-round(seconds*30)) > 1:
        raise ValueError('Final video frame count does not cover the full narration timeline')
    runner.run_ff([runner.FF, '-y', '-i', str(target), '-vf',
                   f'fps=1/2,scale=180:320,tile=5x{math.ceil(seconds/10)}',
                   '-frames:v', '1', str(path/'contact-sheet.jpg')])
    runner.run_ff([runner.FF, '-y', '-ss', str(seconds-.2), '-i', str(target), '-frames:v', '1', str(path/'last-frame.jpg')])
    runner.save_json(path/'verification.json', {
        'final_seconds': runner.duration(target), 'resolution': '720x1280', 'fps': 30,
        'video_frame_count': video_frames, 'video_seconds': video_frames/30,
        'independent_scenes': count, 'looped': False, 'slowed_to_fill': False,
        'full_scene_dialogue_preserved': True, 'scene_timings': timings,
        'decode_check': 'passed',
        'audio_levels_db': {key: float(re.search(key+r':\s*([-\d.]+)', qa.stderr)[1]) for key in ('mean_volume', 'max_volume')},
        'black_or_freeze_alerts': [line for line in qa.stderr.splitlines() if 'black_start:' in line or 'freeze_start:' in line],
        'visual_qa': 'pending final sampled-frame review',
        'text_overlays': overlays, 'exposure_reports': exposure_reports,
        'sha256': hashlib.sha256(target.read_bytes()).hexdigest(),
    })
    print('READY', target, flush=True)


def execute(runner, args, batch, config, selected):
    jobs = [(index, clip, number) for index, clip in selected
            for number in range(1, len(clip['scenes'])+1) if args.scene is None or args.scene == number]
    if args.scene is not None and not jobs:
        raise ValueError('scene exceeds storyboard scene count')
    if args.stage == 'cache':
        warm_cache(runner, batch, config, selected)
    elif args.stage == 'plan':
        plan(runner, batch, config, selected)
    elif args.stage == 'characters':
        characters(runner, batch, config)
    elif args.stage == 'voices':
        with ThreadPoolExecutor(max_workers=2) as pool:
            tasks = [pool.submit(voice, runner, batch, config, index, clip, number) for index, clip, number in jobs]
            for task in tasks:
                task.result()
    elif args.stage in ('images', 'videos'):
        for index, clip, number in jobs:
            (opening if args.stage == 'images' else shot)(runner, batch, config, index, clip, number)
    elif args.stage == 'render':
        for index, clip in selected:
            render(runner, batch, config, index, clip)
    elif args.stage == 'status':
        for index, clip, number in jobs:
            sf = folder(runner, batch, index, clip, number)
            print(index, number, {'image': (sf/'opening.png').exists(),
                                 'reviewed': approval_valid(runner, sf),
                                 'video': (sf/'source.mp4').exists(),
                                 'voice': (voice_folder(runner, sf)/'voice.mp3').exists(),
                                 'speech_mode': talking_module().mode(config, clip, clip['scenes'][number-1]),
                                 'speech_inputs_present': (sf/'speech/input.json').exists(),
                                 'synced_asset_present': (sf/'speech/synced.mp4').exists(),
                                 'sync_review_present': (sf/'speech/sync-review.json').exists()})
