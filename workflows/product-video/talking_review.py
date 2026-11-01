"""Audio-bound talking scenes learned from the user's Viesnap reference.

Prepare inputs at FINAL playback speed, then hand them to a real audio-driven
lip-sync engine. This module does not synthesize mouths or pretend Muse accepts
audio. Rendering requires a reviewed external result bound to these exact inputs.
"""
import hashlib
import importlib.util
from pathlib import Path
import re

STYLE = 'viesnap-talking-review-v1'


def mode(config, clip, scene):
    return scene.get('speech_mode', clip.get('speech_mode', config.get('speech_mode', 'voiceover')))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def validate(config, clip):
    style = config.get('reference_style')
    if style and style != STYLE:
        raise ValueError('Unknown reference_style: '+str(style))
    scenes = clip.get('scenes', [])
    if style and not scenes:
        raise ValueError('Reference talking-review style requires explicit scenes')
    talking_seconds = 0
    for scene in scenes:
        speech_mode = mode(config, clip, scene)
        if speech_mode not in ('voiceover', 'lip_sync'):
            raise ValueError('speech_mode must be voiceover or lip_sync')
        if speech_mode != 'lip_sync':
            continue
        talking_seconds += scene['seconds']
        if clip.get('presentation_mode', 'presenter') != 'presenter' or scene.get('face_visible') is not True:
            raise ValueError('lip_sync requires a clearly visible presenter face')
        prompt = ' '.join([clip.get('presenter', ''), scene['opening_prompt'], scene['video_prompt']]).lower()
        forbidden = (
            r'no speaking', r'no lip[- ]?sync', r'lips? (?:remain |stay )?closed',
            r'lips? relaxed and closed', r'mouth (?:stays? |remain[s]? )?(?:relaxed|closed)',
            r'face (?:is )?outside', r'(?:from|crop(?:ped)? (?:at|below)) (?:below )?(?:the (?:presenter.s )?)?chin',
            r'no (?:music, )?speech',
        )
        if any(re.search(pattern, prompt) for pattern in forbidden):
            raise ValueError('lip_sync prompt conflicts with visible speaking; remove closed-mouth/no-speaking/cropped-face directions')
    if not scenes and mode(config, clip, {}) == 'lip_sync':
        raise ValueError('lip_sync requires explicit storyboard scenes')
    if style:
        if talking_seconds < sum(s['seconds'] for s in scenes)*.6:
            raise ValueError('Reference style requires visible synchronized speech for at least 60% of runtime')
        if scenes[0]['seconds'] > 3 or mode(config, clip, scenes[0]) != 'lip_sync':
            raise ValueError('Reference style opens with a talking hook of at most three seconds')
        for scene in scenes:
            if not scene.get('beat') or not scene.get('visible_action'):
                raise ValueError('Reference style requires a story beat and a visible action per scene')
        if scenes[0]['beat'] != 'hook' or scenes[-1]['beat'] != 'cta':
            raise ValueError('Reference style must begin with hook and finish with cta')
        if not clip.get('marketing'):
            raise ValueError('Reference style requires grounded marketing hook, benefit and CTA')


def direction(config, scene):
    if config.get('reference_style') != STYLE:
        return ''
    return (
        '\nREFERENCE STORY DIRECTION: a concrete surprising reveal, then a clear '
        'product pitch with purposeful gestures. Energy comes from the performer '
        'and story, while the camera, product geometry and lighting stay stable. '
        'Use a fictional adult, never copy the reference performer. '
        'This shot has ONE action, starting immediately: '+scene['visible_action']+
        '. Do not repeat a shell stroke in every shot. No added text or watermark.'
    )


def input_identity(runner, storyboard, batch, config, index, clip, number):
    scene = clip['scenes'][number-1]
    path = storyboard.folder(runner, batch, index, clip, number)
    voice = storyboard.voice_folder(runner, path)/'voice.mp3'
    script = voice.with_name('dialogue.txt')
    if not script.exists() or script.read_text(encoding='utf-8').strip() != scene['dialogue'].strip():
        raise ValueError('Prepare speech only from the current exact narration take')
    return {
        'source_sha256': sha(path/'source.mp4'),
        'voice_sha256': sha(voice),
        'opening_sha256': sha(path/'opening.png'),
        'dialogue': scene['dialogue'],
        'seconds': scene['seconds'],
        'source_start': scene.get('source_start', 0),
        'visual_speed': scene.get('visual_speed', clip.get('visual_speed', config.get('visual_speed', 1.5))),
        'audio_segments': scene.get('audio_segments'),
        'exposure_lock': config.get('quality', {}).get('exposure_lock'),
        'format': '720x1280/30fps/48000Hz/v1',
    }


def prepare(runner, storyboard, batch, config, index, clip, number):
    scene = clip['scenes'][number-1]
    if mode(config, clip, scene) != 'lip_sync':
        return
    path = storyboard.folder(runner, batch, index, clip, number)
    storyboard.require_approval(runner, path)
    identity = input_identity(runner, storyboard, batch, config, index, clip, number)
    target = path/'speech'
    if target.exists():
        receipt = target/'input.json'
        if receipt.exists() and runner.read_json(receipt).get('identity') == identity:
            old = runner.read_json(receipt)
            if all((target/name).is_file() and sha(target/name) == old.get(field)
                   for name, field in [('video.mp4', 'video_sha256'), ('voice.wav', 'audio_sha256')]):
                print('SPEECH_INPUTS_READY', target, flush=True)
                return
        raise ValueError('Speech inputs changed or incomplete; keep this attempt and use a new scene revision')
    source = path/'source.mp4'
    voice = storyboard.voice_folder(runner, path)/'voice.mp3'
    seconds, speed, start = identity['seconds'], identity['visual_speed'], identity['source_start']
    if start+seconds*speed > runner.duration(source)+.02:
        raise ValueError('Insufficient independent source for speech preparation')
    audio_seconds = runner.duration(voice)
    segments = scene.get('audio_segments', [[0, audio_seconds]])
    if any(end > audio_seconds+.001 for _, end in segments):
        raise ValueError('Speech segments exceed the actual voice take')
    tempo = max(1., sum(end-begin for begin, end in segments)/(seconds-.06))
    if tempo > 1.25:
        raise ValueError('Talking scene narration is too long; revise speech before lip-sync')
    target.mkdir()
    audio_filters = []
    if len(segments) > 1:
        audio_filters.append(f'[0:a]asplit={len(segments)}'+''.join(f'[s{n}]' for n in range(len(segments))))
    for n, (begin, end) in enumerate(segments):
        label = f's{n}' if len(segments) > 1 else '0:a'
        audio_filters.append(f'[{label}]atrim=start={begin:.8f}:end={end:.8f},asetpts=PTS-STARTPTS[a{n}]')
    audio_filters.append(''.join(f'[a{n}]' for n in range(len(segments)))+
                         f'concat=n={len(segments)}:v=0:a=1,atempo={tempo:.8f},'
                         f'apad,atrim=duration={seconds:.8f},aresample=48000[a]')
    runner.run_ff([runner.FF, '-y', '-i', str(voice), '-filter_complex', ';'.join(audio_filters),
                   '-map', '[a]', '-c:a', 'pcm_s16le', str(target/'voice.wav')])
    video_filters = [
        f'[0:v]trim=start={start:.8f}:duration={seconds*speed:.8f},setpts=(PTS-STARTPTS)/{speed:.8f},'
        'scale=720:1280:force_original_aspect_ratio=decrease:force_divisible_by=2,'
        'pad=720:1280:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30:eof_action=pass[base]'
    ]
    if identity['exposure_lock'] is not None:
        exposure = storyboard.quality_module().exposure_plan(
            runner.FF, source, path/'opening.png', dict(scene, visual_speed=speed), identity['exposure_lock'])
        runner.save_json(target/'exposure-plan.json', exposure)
        video_filters.extend(storyboard.quality_module().exposure_filters('base', 'v', exposure, 'speech_'))
    else:
        video_filters.append('[base]null[v]')
    runner.run_ff([runner.FF, '-y', '-i', str(source), '-filter_complex', ';'.join(video_filters),
                   '-map', '[v]', '-an', '-c:v', 'libx264', '-crf', '18', '-preset', 'fast',
                   '-pix_fmt', 'yuv420p', '-t', str(seconds), str(target/'video.mp4')])
    runner.save_json(target/'input.json', {
        'identity': identity, 'audio_tempo_before_sync': tempo,
        'video_sha256': sha(target/'video.mp4'), 'audio_sha256': sha(target/'voice.wav'),
        'status': 'prepared_only_engine_not_connected',
        'next': 'Run an actual audio-driven lip-sync engine on video.mp4 + voice.wav. '
                'Save synced.mp4 and sync-review.json after audiovisual review. Never just remux audio.',
    })
    print('SPEECH_INPUTS_PREPARED', target, flush=True)


def require_synced(runner, storyboard, batch, config, index, clip, number):
    path = storyboard.folder(runner, batch, index, clip, number)/'speech'
    required = ['input.json', 'video.mp4', 'voice.wav', 'synced.mp4', 'sync-review.json']
    if not all((path/name).is_file() for name in required):
        raise ValueError('lip_sync requires prepared inputs, actual synced.mp4 and audiovisual sync-review.json: '+str(path))
    inputs, review = runner.read_json(path/'input.json'), runner.read_json(path/'sync-review.json')
    if inputs.get('identity') != input_identity(runner, storyboard, batch, config, index, clip, number):
        raise ValueError('Lip-sync input identity is stale; prepare a new scene revision')
    checks = {
        'audio_sha256': sha(path/'voice.wav'),
        'video_sha256': sha(path/'video.mp4'),
        'synced_sha256': sha(path/'synced.mp4'),
    }
    if (inputs.get('audio_sha256') != checks['audio_sha256']
            or inputs.get('video_sha256') != checks['video_sha256']
            or any(review.get(key) != value for key, value in checks.items())
            or review.get('result') != 'accepted'
            or not isinstance(review.get('engine'), str) or not review['engine'].strip()
            or not isinstance(review.get('notes'), str) or not review['notes'].strip()
            or review.get('mouth_audio_reviewed') is not True
            or review.get('product_face_hands_reviewed') is not True):
        raise ValueError('Lip-sync review is stale, rejected or lacks actual mouth/audio/product review')
    seconds = clip['scenes'][number-1]['seconds']
    intervals = review.get('reviewed_interval_seconds')
    if intervals != [0, seconds]:
        raise ValueError('Lip-sync review must cover the full final-speed scene')
    if abs(runner.duration(path/'synced.mp4')-seconds) > .08:
        raise ValueError('Synced scene duration differs from final audio timeline')
    decoded = runner.run_ff([runner.FF, '-hide_banner', '-i', str(path/'synced.mp4'),
                             '-i', str(path/'voice.wav'), '-map', '0:v:0', '-map', '1:a:0',
                             '-f', 'null', '-'])
    frame_counts = re.findall(r'\bframe=\s*(\d+)', decoded.stderr)
    if (not frame_counts or int(frame_counts[-1]) != round(seconds*30)
            or not re.search(r'Video:.*\b30 fps\b', decoded.stderr)):
        raise ValueError('Reviewed lip-sync result must contain the exact final 30fps frame count')
    return path/'synced.mp4', path/'voice.wav'


def main():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--batch', required=True)
    parser.add_argument('--clip', type=int)
    parser.add_argument('--scene', type=int)
    args = parser.parse_args()
    spec = importlib.util.spec_from_file_location('product_runner', Path(__file__).with_name('run.py'))
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
    batch = Path(args.batch).resolve()
    config = runner.read_json(batch/'batch.json')
    runner.validate(config)
    if args.clip is not None and not 1 <= args.clip <= len(config['clips']):
        parser.error('clip index out of bounds')
    for i, clip in enumerate(config['clips'], 1):
        if args.clip is not None and args.clip != i:
            continue
        if args.scene is not None and not 1 <= args.scene <= len(clip['scenes']):
            parser.error('scene index out of bounds')
        for number in range(1, len(clip['scenes'])+1):
            if args.scene is None or args.scene == number:
                prepare(runner, runner.storyboard_module(), batch, config, i, clip, number)


if __name__ == '__main__':
    main()
