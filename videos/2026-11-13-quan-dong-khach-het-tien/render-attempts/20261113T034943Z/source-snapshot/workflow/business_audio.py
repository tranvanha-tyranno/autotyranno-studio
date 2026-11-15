"""Cached cafe-business score, contextual Foley and exact-take speech-first mix.

Only the explicit generate/all phases contact the provider. Mixing is local and
keeps every original, receipt and stem. Measurement is not claimed listening.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import wave

import numpy as np

from documentary import FF, duration
import eleven_audio

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = 'business-sound-plan/1'
MUSIC = [
    ('coffee-opening', 'Warm observational business documentary opening in a Vietnamese cafe. Muted acoustic guitar, brushed percussion, soft electric piano and a restrained wooden pulse. Curious, human, sophisticated, medium slow tempo. Build gently without a huge climax. Leave a wide clear center for a Vietnamese narrator. Original instrumental only; no vocals, speech, chanting, alarms, dramatic brass or heavy EDM.'),
    ('precise-unit-math', 'Precise, lightly playful documentary underscore for following the economics of one coffee order. Sparse pizzicato strings, warm marimba, felt piano and tiny brushed percussion. Clean space between notes, steady understated momentum, no urgent ticking. Clear center for narration. Original instrumental only; no vocals, speech, alarms or heavy EDM.'),
    ('operating-pulse', 'Calm sophisticated business documentary music about a busy cafe and capacity. Warm bass, dry soft drums, acoustic textures and restrained electric piano. Subtle motion and curiosity, grounded and human, never triumphant. Clear open middle for continuous speech. Original instrumental only; no vocals, speech, alarms, aggressive drums or heavy EDM.'),
    ('cash-tension', 'Quiet reflective documentary underscore about bills coming due before cash arrives. Low felt piano, sparse muted cello, soft granular texture and a very gentle pulse. Thoughtful financial tension, not horror or impending disaster. Few notes and a wide clear center for speech. Original instrumental only; no vocals, speech, alarms, loud impacts, risers or heavy EDM.'),
    ('hopeful-outro', 'Human hopeful ending for an educational cafe business documentary. Warm acoustic guitar, felt piano, brushed drums and a gentle string bed. Practical optimism, patient forward movement, modest emotional payoff. Leave space for a Vietnamese narrator and end with an unhurried soft resolution. Original instrumental only; no vocals, speech, chanting, alarms or heavy EDM.'),
]
SOUNDS = [
    ('cup-set', 2.2, 'One ceramic coffee cup placed gently on a wooden cafe table, soft clean contact and a tiny natural ceramic ring. Close realistic Foley, no music, voices or exaggerated crash.'),
    ('grinder', 4.0, 'A small cafe coffee grinder runs briefly, dry coffee beans grinding with a short natural motor rise and stop. Realistic close Foley, no voices, music or alarm.'),
    ('espresso', 5.0, 'A cafe espresso machine pulls a short shot, gentle pump hum and coffee trickling into a ceramic cup, natural soft finish. Realistic Foley, no voices, music or alarm.'),
    ('milk-steam', 4.0, 'A barista briefly steams milk in a metal pitcher, soft controlled steam hiss that eases out naturally. Realistic quiet cafe Foley, no shouting, voices or music.'),
    ('paper-pen', 4.5, 'A paper receipt is slid across a wooden counter, followed by a few calm pencil writing strokes and a soft pen set down. Intimate dry realistic Foley, no voices or music.'),
    ('coins', 2.8, 'Two or three small coins gently placed and slid on a wooden counter, restrained warm metallic clinks, not a cash register. Realistic close Foley, no voices or music.'),
    ('wood-tick', 1.5, 'One soft dry wooden tap, tactile and minimal, like a fingertip touching a wood counter. No clock rhythm, music, voices or digital alarm.'),
    ('transition', 1.6, 'A restrained warm airy paper swish moving gently from left to right, very short documentary transition, soft fabric and air, no sharp digital swoosh, music or voices.'),
    ('cafe-ambience', 18.0, 'Quiet cafe room ambience with subtle cups far away, a faint espresso machine and gentle room tone. No intelligible words, foreground voices, music, traffic horns or alarms. Warm unobtrusive documentary background.'),
    ('low-hit', 1.8, 'One very soft low wooden resonant tap with a short warm tail, understated reflective documentary punctuation. No cinematic boom, alarm, riser, music or voices.'),
]
REUSED = [
    ('motion-bridge', ROOT / 'videos/2026-11-11-cinematic-reset/audio/motion-score.mp3',
     '28978a359075dc20e8fa1b42a09a00f831abaa2e17c292d4e2b829c1c5c37f96'),
    ('agency-bridge', ROOT / 'videos/2026-11-11-ai-va-cong-viec-5phut/audio/agency-score.mp3',
     'd9e8cd06be749fef38cd66a8d491c0f607d9996c0b914cb34d86e7d643c71b5a'),
]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    result = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            result.update(chunk)
    return result.hexdigest()


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def save(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + '.partial')
    payload = json.dumps(value, ensure_ascii=False, indent=2).encode('utf-8')
    with temporary.open('wb') as stream:
        stream.write(payload)
        stream.flush()
        os.fsync(stream.fileno())
    temporary.replace(path)


def request_hash(endpoint, payload):
    return hashlib.sha256(json.dumps({'endpoint': endpoint, 'body': payload}, sort_keys=True,
                                    ensure_ascii=False).encode()).hexdigest()


def plan(batch):
    batch = Path(batch).resolve()
    music = [{'id': name, 'file': f'audio/music/{name}.mp3', 'endpoint': '/v1/music',
              'payload': {'prompt': prompt, 'music_length_ms': 120000,
                          'force_instrumental': True, 'model_id': 'music_v1'}} for name, prompt in MUSIC]
    sounds = [{'id': name, 'file': f'audio/sfx/{name}.mp3', 'endpoint': '/v1/sound-generation',
               'payload': {'text': prompt, 'duration_seconds': seconds, 'prompt_influence': .5,
                           'model_id': 'eleven_text_to_sound_v3', 'loop': False}}
              for name, seconds, prompt in SOUNDS]
    value = {'schema': SCHEMA, 'music': music, 'sounds': sounds,
             'mixPolicy': {'voiceLUFS': -16, 'musicLUFS': -29, 'foleyLUFS': -32,
                           'ambienceLUFS': -39, 'crossfadeSeconds': 3,
                           'voiceSpeed': 1.0, 'noAudioLooping': True},
             'reuse': [{'id': name, 'file': f'audio/music/{name}.mp3', 'source': str(source),
                        'sha256': digest} for name, source, digest in REUSED],
             'auditoryAcceptance': 'Pending actual listening; generation/measurement is not listening.'}
    path = batch / 'audio/sound-plan.json'
    if path.exists():
        require(load(path) == value, 'Sound plan changed; use a new batch/revision')
    else:
        save(path, value)
    return value


def check_source(path, expected_request=None, expected_sha=None):
    path = Path(path)
    require(path.is_file(), 'Missing audio source: ' + str(path))
    receipt_path = path.with_suffix('.receipt.json')
    require(receipt_path.is_file(), 'Audio source lacks provider receipt: ' + path.name)
    receipt = load(receipt_path)
    digest = sha(path)
    require(digest == receipt.get('sha256'), 'Audio bytes differ from receipt: ' + path.name)
    if expected_request is not None:
        require(receipt.get('request_hash') == expected_request, 'Audio request differs from sound plan: ' + path.name)
    if expected_sha is not None:
        require(digest == expected_sha, 'Pinned approved music changed: ' + path.name)
    return {'file': str(path), 'sha256': digest, 'receiptSHA256': sha(receipt_path),
            'provider': receipt.get('provider'), 'model': receipt.get('model'),
            'requestHash': receipt.get('request_hash'), 'seconds': duration(path)}


def generate(batch):
    """Explicit paid phase; existing matching targets/cache are verified and reused."""
    batch = Path(batch).resolve()
    spec = plan(batch)
    records = []
    for entry in spec['music'] + spec['sounds']:
        path = batch / entry['file']
        digest = request_hash(entry['endpoint'], entry['payload'])
        if path.exists():
            check_source(path, digest)
        elif entry['endpoint'] == '/v1/music':
            eleven_audio.generate(path, entry['endpoint'], entry['payload'])
        else:
            eleven_audio.sound(path, entry['payload']['text'], entry['payload']['duration_seconds'])
        record = check_source(path, digest)
        record.update({'id': entry['id'], 'file': entry['file'], 'kind': 'music' if entry in spec['music'] else 'foley'})
        records.append(record)
        save(batch / 'audio/generation-receipts.json', {'schema': 'business-generated-audio/1',
             'sources': records, 'soundPlanSHA256': sha(batch / 'audio/sound-plan.json'),
             'humanListening': 'Not established by generation'})
    for entry in spec['reuse']:
        target, source = batch / entry['file'], Path(entry['source'])
        check_source(source, expected_sha=entry['sha256'])
        if target.exists():
            require(sha(target) == entry['sha256'], 'Retained reused music changed')
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
            shutil.copy2(source.with_suffix('.receipt.json'), target.with_suffix('.receipt.json'))
        record = check_source(target, expected_sha=entry['sha256'])
        record.update({'id': entry['id'], 'file': entry['file'], 'kind': 'retained-generated-music',
                       'originalSource': entry['source']})
        records.append(record)
    result = {'schema': 'business-generated-audio/1', 'sources': records,
              'soundPlanSHA256': sha(batch / 'audio/sound-plan.json'),
              'humanListening': 'Not established by generation'}
    save(batch / 'audio/generation-receipts.json', result)
    return result


def cue_sheet(data):
    fps, seconds = data['fps'], data['frames'] / data['fps']
    require(fps > 0 and seconds > 0, 'Invalid sound timeline')
    shots = {shot['id']: shot for shot in data['shots']}
    require(len(shots) == len(data['shots']), 'Duplicate beat IDs make Foley timing ambiguous')
    # beat, asset, offset seconds, gain dB after normalization, role
    definitions = [
        ('h01', 'cafe-ambience', 0, 0, 'Establish the audible cafe room'),
        ('h01', 'espresso', .4, -1, 'Machine mentioned in the opening'),
        ('h03', 'cup-set', .25, 0, 'Follow the single hypothetical coffee cup'),
        ('u01', 'transition', 0, -3, 'Move from opening to unit economics'),
        ('u02', 'grinder', .15, -2, 'Ingredients and preparation cost per order'),
        ('u03', 'paper-pen', .25, -1, 'Open the receipt arithmetic'),
        ('b01', 'transition', 0, -3, 'Move to fixed costs and break-even'),
        ('b03', 'wood-tick', .2, -2, 'Mark the break-even step'),
        ('v01', 'cafe-ambience', .1, -2, 'Busy-hours scene context'),
        ('p01', 'paper-pen', .3, -1, 'Change the hypothetical offer price'),
        ('p03', 'coins', .3, -1, 'Different contribution from a discounted cup'),
        ('m01', 'transition', 0, -4, 'Shift from operating result to cash timing'),
        ('u06', 'milk-steam', .3, -3, 'Visible milk-steaming action in the prepared first media slot'),
        ('m07', 'low-hit', .2, -3, 'Quiet emphasis on cash obligations'),
        ('a01', 'transition', 0, -4, 'Move to practical observation'),
        ('a02', 'paper-pen', .2, -1, 'Write the week observation sheet'),
        ('e01', 'cafe-ambience', .2, -2, 'Return to the real cafe context'),
        ('e05', 'cup-set', .4, -1, 'Final callback to the single coffee cup'),
    ]
    cues = []
    for beat, asset, offset, gain, role in definitions:
        require(beat in shots, 'Sound cue beat missing: ' + beat)
        shot = shots[beat]
        at = shot['start'] / fps + offset
        remaining = max(.05, shot['end'] / fps - at)
        available = next(seconds for name, seconds, _ in SOUNDS if name == asset)
        length = min(available, remaining + (1.1 if asset == 'cafe-ambience' else .25), seconds - at)
        require(0 <= at < seconds and length > 0, 'Foley cue falls outside narration')
        cues.append({'beat': beat, 'asset': asset, 'time': round(at, 6), 'duration': round(length, 6),
                     'gainDB': gain, 'role': role, 'ambience': asset == 'cafe-ambience'})
    pivots = []
    for beat in ['p09', 'm08']:
        require(beat in shots, 'Quiet pivot beat missing: ' + beat)
        at = shots[beat]['start'] / fps
        pivots.append({'beat': beat, 'start': max(0, at - .12), 'end': min(seconds, at + 1.4), 'gain': .14})
    return cues, pivots


def run(command):
    result = subprocess.run(command, capture_output=True)
    if result.returncode:
        raise RuntimeError(result.stderr.decode('utf-8', errors='replace')[-3500:])
    return result


def music_sequence(sources, seconds, crossfade=3):
    by_id = {source['id']: source for source in sources}
    names = ['coffee-opening', 'precise-unit-math', 'operating-pulse',
             'motion-bridge', 'cash-tension', 'hopeful-outro']
    def capacity():
        return sum(by_id[name]['seconds'] for name in names) - crossfade * (len(names) - 1)
    if capacity() < seconds:
        names.insert(-1, 'agency-bridge')
    require(capacity() >= seconds, 'Music sources cannot cover the exact take without looping')
    cursor, sections = 0.0, []
    for name in names:
        source = by_id[name]
        sections.append({'id': name, 'file': source['file'], 'sha256': source['sha256'],
                         'start': round(cursor, 6), 'end': round(min(seconds, cursor + source['seconds']), 6),
                         'sourceSeconds': source['seconds']})
        cursor += source['seconds'] - crossfade
    return sections


def _write_stem(command, path, seconds):
    temporary = path.with_name(path.stem + '.partial.wav')
    run(command + ['-t', f'{seconds:.9f}', '-ar', '48000', '-ac', '2', '-c:a', 'pcm_s16le', str(temporary)])
    require(abs(duration(temporary) - seconds) <= .06, 'Audio stem duration differs from exact timeline')
    temporary.replace(path)


def _effects_stem(batch, cues, sources, seconds):
    """Normalize short cues separately and overlap exact PCM on a disk-backed bed.

    Long adelay filters retain silence buffers per cue. This assembly uses one
    short FFmpeg input at a time and never allocates a ten-minute bed in RAM.
    """
    rate, frames = 48000, round(seconds * 48000)
    raw_path = batch / 'audio/sfx-bed.partial.pcm'
    with raw_path.open('wb') as stream:
        stream.truncate(frames * 2 * 2)
    bed = np.memmap(raw_path, dtype='<i2', mode='r+', shape=(frames, 2))
    snippets = batch / 'audio/cue-stems'
    snippets.mkdir(parents=True, exist_ok=True)
    retained = []
    try:
        for index, cue in enumerate(cues):
            target = snippets / f'{index:02}-{cue["beat"]}-{cue["asset"]}.wav'
            level = -39 if cue['ambience'] else -32
            fade = min(.8 if cue['ambience'] else .18, cue['duration'] / 3)
            graph = (f'aresample=48000,aformat=channel_layouts=stereo,atrim=duration={cue["duration"]:.6f},'
                f'asetpts=PTS-STARTPTS,highpass=f=100,loudnorm=I={level}:TP=-9:LRA=5,'
                f'volume={cue["gainDB"]}dB,aresample=48000,'
                f'afade=t=in:d={min(.3, fade):.6f},afade=t=out:st={max(0, cue["duration"]-fade):.6f}:d={fade:.6f},'
                f'asetpts=N/SR/TB,apad=whole_len={round(cue["duration"] * rate)},atrim=end_sample={round(cue["duration"] * rate)}')
            _write_stem([FF, '-y', '-v', 'error', '-i', str(batch / sources[cue['asset']]['file']),
                         '-af', graph], target, cue['duration'])
            with wave.open(str(target), 'rb') as stream:
                require(stream.getnchannels() == 2 and stream.getframerate() == rate
                        and stream.getsampwidth() == 2, 'Foley snippet PCM format differs')
                samples = np.frombuffer(stream.readframes(stream.getnframes()), dtype='<i2').reshape(-1, 2)
            start = round(cue['time'] * rate)
            count = min(len(samples), frames - start)
            combined = bed[start:start + count].astype(np.int32) + samples[:count].astype(np.int32)
            bed[start:start + count] = np.clip(combined, -32768, 32767).astype('<i2')
            retained.append({'file': target.relative_to(batch).as_posix(), 'sha256': sha(target),
                             'atSample': start, 'frames': count, 'normalizedLUFS': level})
        bed.flush()
    finally:
        del bed
    target = batch / 'audio/sfx-stem.wav'
    temporary = target.with_name('sfx-stem.partial.wav')
    with wave.open(str(temporary), 'wb') as output:
        output.setnchannels(2)
        output.setsampwidth(2)
        output.setframerate(rate)
        with raw_path.open('rb') as source:
            while chunk := source.read(1024 * 1024):
                output.writeframesraw(chunk)
    require(abs(duration(temporary) - seconds) <= .03, 'Foley stem does not cover the exact timeline')
    temporary.replace(target)
    raw_path.unlink()
    return target, retained


def mix(batch, *, public=None):
    """Build music/Foley separately, then mix only three inputs with speech ducking."""
    batch = Path(batch).resolve()
    spec = plan(batch)
    data_path = batch / 'data.json'
    require(data_path.is_file(), 'Compile exact narration timing to batch/data.json before mixing')
    data = load(data_path)
    seconds = data['frames'] / data['fps']
    voice = batch / 'audio/narration.wav'
    require(voice.is_file(), 'Missing exact chapter-assembled audio/narration.wav')
    require(duration(voice) <= seconds + .06, 'Narration extends beyond the compiled timeline; refuse truncation')
    generation = load(batch / 'audio/generation-receipts.json')
    require(generation['soundPlanSHA256'] == sha(batch / 'audio/sound-plan.json'), 'Generated sources use another sound plan')
    planned = {item['id']: item for item in spec['music'] + spec['sounds'] + spec['reuse']}
    require(len({item['id'] for item in generation['sources']}) == len(generation['sources']), 'Duplicate generated audio IDs')
    sources = []
    for item in generation['sources']:
        require(item['id'] in planned and item['file'] == planned[item['id']]['file'], 'Generated audio path differs from sound plan')
        entry = planned[item['id']]
        path = batch / item['file']
        record = check_source(path, expected_request=request_hash(entry['endpoint'], entry['payload']) if 'endpoint' in entry else None,
                              expected_sha=entry.get('sha256', item['sha256']))
        require(record['sha256'] == item['sha256'], 'Generated source differs from generation receipt')
        require(record['receiptSHA256'] == item['receiptSHA256'], 'Audio provider receipt changed')
        sources.append({**item, 'seconds': record['seconds']})
    require({item['id'] for item in sources} == {item['id'] for item in spec['music'] + spec['sounds'] + spec['reuse']}, 'Generated audio set is incomplete')
    by_id = {item['id']: item for item in sources}
    cues, pivots = cue_sheet(data)
    sections = music_sequence(sources, seconds)
    fingerprint = {'dataSHA256': sha(data_path), 'narrationSHA256': sha(voice),
                   'generationReceiptSHA256': sha(batch / 'audio/generation-receipts.json'),
                   'seconds': seconds, 'sections': sections, 'cues': cues, 'pivots': pivots}
    report_path, final = batch / 'audio/mix-report.json', batch / 'audio/final-mix.wav'
    if final.exists():
        require(report_path.is_file(), 'Existing mix lacks receipt; use a new revision')
        existing = load(report_path)
        require(existing['inputs'] == fingerprint and existing['mix']['sha256'] == sha(final), 'Existing mix/input changed; use a new revision')
        public = Path(public).resolve() if public else batch / 'production-public/business'
        public.mkdir(parents=True, exist_ok=True)
        target = public / 'mix.wav'
        if not target.exists() or sha(target) != sha(final):
            shutil.copy2(final, target)
        return existing

    inputs = [FF, '-y', '-v', 'error']
    graph = []
    for i, section in enumerate(sections):
        inputs += ['-i', str(batch / section['file'])]
        graph.append(f'[{i}:a]aresample=48000,aformat=channel_layouts=stereo,asetpts=PTS-STARTPTS[m{i}]')
    previous = '[m0]'
    for i in range(1, len(sections)):
        graph.append(f'{previous}[m{i}]acrossfade=d=3:c1=qsin:c2=qsin[mix{i}]')
        previous = f'[mix{i}]'
    gain = '1'
    for pivot in pivots:
        gain += (f'-0.86*clip((t-{pivot["start"]:.6f})/0.16,0,1)'
                 f'*clip(({pivot["end"]:.6f}-t)/0.24,0,1)')
    graph.append(f'{previous}loudnorm=I=-29:TP=-8:LRA=7,aresample=48000,asetpts=N/SR/TB,volume=\'{gain}\':eval=frame,afade=t=in:d=0.8,afade=t=out:st={max(0, seconds-3):.6f}:d=3[music]')
    music_stem = batch / 'audio/music-stem.wav'
    _write_stem(inputs + ['-filter_complex', ';'.join(graph), '-map', '[music]'], music_stem, seconds)

    sfx_stem, snippets = _effects_stem(batch, cues, by_id, seconds)

    graph = (
        '[0:a]aresample=48000,aformat=channel_layouts=stereo,highpass=f=70,loudnorm=I=-16:TP=-2:LRA=8,aresample=48000,asetpts=N/SR/TB,asplit=2[voice][key];'
        '[1:a][key]sidechaincompress=threshold=.025:ratio=3:attack=18:release=260:makeup=1[duck];'
        f'[voice][duck][2:a]amix=inputs=3:duration=longest:normalize=0,alimiter=limit=.89:level=false,apad=whole_dur={seconds:.6f}[out]')
    _write_stem([FF, '-y', '-v', 'error', '-i', str(voice), '-i', str(music_stem), '-i', str(sfx_stem),
                 '-filter_complex', graph, '-map', '[out]'], final, seconds)
    measured = run([FF, '-hide_banner', '-i', str(final), '-af',
                    'loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-'])
    raw = measured.stderr.decode('utf-8', errors='replace')
    matches = re.findall(r'\{\s*"input_i".*?\}', raw, re.S)
    require(matches, 'Mix loudness measurement was not returned')
    loudness = json.loads(matches[-1])
    require(math.isfinite(float(loudness['input_i'])), 'Mix contains no measurable audio')
    public = Path(public).resolve() if public else batch / 'production-public/business'
    public.mkdir(parents=True, exist_ok=True)
    shutil.copy2(final, public / 'mix.wav')
    result = {'schema': 'business-audio-mix/1', 'inputs': fingerprint,
              'mix': {'file': 'audio/final-mix.wav', 'sha256': sha(final), 'seconds': duration(final),
                      'loudnessMeasurement': loudness, 'publicFile': str(public / 'mix.wav')},
              'stems': [{'file': str(path.relative_to(batch)), 'sha256': sha(path)} for path in [music_stem, sfx_stem]],
              'musicSections': sections, 'contextualCues': [{**cue, 'file': by_id[cue['asset']]['file'],
                 'sha256': by_id[cue['asset']]['sha256']} for cue in cues], 'quietPivots': pivots,
              'maximumFFmpegInputs': max(len(sections), 3), 'cueSnippets': snippets,
              'voiceTempo': 1.0, 'manualListening': False,
              'limitation': 'Loudness and duration measured; no continuous human listening or aesthetic acceptance is asserted.'}
    save(report_path, result)
    save(batch / 'audio-sources.json', result)
    save(batch / 'sound-cues.json', result['contextualCues'])
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--batch', type=Path, required=True)
    parser.add_argument('--phase', choices=['plan', 'generate', 'mix', 'all'], required=True)
    parser.add_argument('--public', type=Path)
    args = parser.parse_args()
    if args.phase == 'plan':
        result = plan(args.batch)
    elif args.phase == 'generate':
        result = generate(args.batch)
    elif args.phase == 'mix':
        result = mix(args.batch, public=args.public)
    else:
        generate(args.batch)
        result = mix(args.batch, public=args.public)
    print(json.dumps(result, ensure_ascii=False, indent=2))
