"""China-economy documentary audio and task-scoped provider-cost accounting.

Plan/account/benchmark are read-only at the provider. Only explicit generate or
voice contacts a billable endpoint. Receipts retain cache provenance and measured
time; account deltas are never attributed solely to this task.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import importlib.util
import json
import math
from pathlib import Path
import shutil
import time

import requests

import business_audio as core
import eleven_audio

ROOT = Path(__file__).resolve().parents[2]
VOICE = '6adFm46eyy74snVn6YrT'
SCHEMA = 'china-sound-plan/1'
require, load, save, sha = core.require, core.load, core.save, core.sha
MUSIC = [
    ('industrial-networks', 'Original instrumental analytical documentary underscore about interconnected manufacturing, ports, rail and supply chains. Restrained piano ostinato, muted synth pulse, subtle mallet percussion and a quiet warm bass. Measured forward motion, curious and precise, no dramatic triumph or threat. Leave a clear open middle for continuous Vietnamese speech. No vocals, speech, anthems, national stereotypes, alarms, booms or aggressive drums.'),
    ('balance-sheet-friction', 'Original instrumental economic documentary underscore about property debt, household saving and cash-flow feedback. Sparse low felt piano, muted cello, gentle granular atmosphere and a very quiet irregular pulse. Thoughtful uncertainty and room to think, never horror or imminent-collapse music. Wide clear center for narration. No vocals, speech, alarms, cinematic booms, risers or national stereotypes.'),
    ('adaptation-horizon', 'Original instrumental analytical documentary ending about policy trade-offs, demographic change and adaptation. Warm restrained piano, soft mallets, modest acoustic textures and an airy low string bed. Patient practical curiosity, calm forward motion, no heroic victory. Wide clear space for continuous Vietnamese speech and a soft resolved ending. No vocals, speech, anthems, stereotypes, alarms, loud impacts or heavy drums.'),
]
SOUNDS = [
    ('port-ambience', 14.0, 'Distant container-port ambience: low ship machinery, quiet coastal air and far-away loading equipment. Restrained realistic documentary Foley, no horn, intelligible voices, music, alarms or shouting. This is illustrative sound design, not location recording.'),
    ('crane-set', 4.5, 'One restrained container crane handling movement: quiet mechanical cable motor, a soft heavy metal contact and natural brief settling. Realistic distant industrial Foley, no dramatic crash, horn, music, voices or alarms.'),
    ('rail-pass', 6.0, 'A freight train passes at moderate distance, low rolling wheels and a soft rhythmic rail texture, rising gently then fading. Natural documentary Foley, no horn, music, intelligible speech, alarms or dramatic impact.'),
    ('factory-hum', 10.0, 'Soft steady factory production-floor ambience: low electric motors, a few distant repetitive mechanical clicks and subdued room tone. Realistic quiet documentary bed, no workers speaking, alarms, music, crashes or grinding spectacle.'),
    ('pencil-paper', 4.5, 'A page gently turns and a pencil writes three short calm strokes on paper, close dry tactile sound, then natural silence. Restrained documentary Foley, no money sounds, cafe sounds, voices or music.'),
    ('low-pulse', 2.2, 'One very soft rounded low acoustic pulse with a short warm tail, minimal thoughtful documentary punctuation. No cinematic boom, alarm, riser, drum rhythm, music or voices.'),
]
REUSE_BATCH = ROOT / 'videos/2026-11-13-quan-dong-khach-het-tien/audio'
REUSED = [
    ('analytical-detail', 'music/precise-unit-math.mp3', 'music', 'd5b5fbba86486be356298b9b1e89c8ad60c182989483a10d11ca035f0863a94b'),
    ('quiet-finance', 'music/cash-tension.mp3', 'music', '3625a05819765d346c4bc8d0f054ff26d8c9a01bcf8fed1f4ded82485e862ec7'),
    ('operating-network', 'music/operating-pulse.mp3', 'music', '3a13ebd5aca1d21221ad0544f04666619c90ab3e00b0eea9e7607de365c8c119'),
    ('wood-tick', 'sfx/wood-tick.mp3', 'foley', None),
    ('transition', 'sfx/transition.mp3', 'foley', None),
]


def utc():
    return datetime.now(timezone.utc).isoformat()


def subscription_snapshot(batch, label):
    require(label in {'start', 'end'}, 'Account snapshot must be start or end')
    path = Path(batch) / 'benchmark' / ('subscription-' + label + '.json')
    if path.exists():
        return load(path)
    response = requests.get('https://api.elevenlabs.io/v1/user/subscription',
                            headers={'xi-api-key': eleven_audio.key()}, timeout=30)
    # Never write complete account JSON, error body, identity or payment details.
    data = response.json() if response.ok else {}
    selected = {key: data[key] for key in ['tier', 'status', 'character_count', 'character_limit'] if key in data}
    if isinstance(data.get('character_count'), int) and isinstance(data.get('character_limit'), int):
        selected['creditsRemaining'] = data['character_limit'] - data['character_count']
    value = {'schema': 'audio-account-snapshot/1', 'capturedUTC': utc(), 'endpoint': '/v1/user/subscription',
             'httpStatus': response.status_code, **selected,
             'scope': 'Read-only sanitized account observation; changes may include concurrent jobs and are not task charges.'}
    save(path, value)
    return value


def plan(batch):
    batch = Path(batch).resolve()
    music = [{'id': name, 'file': f'audio/music/{name}.mp3', 'endpoint': '/v1/music',
              'payload': {'prompt': prompt, 'music_length_ms': 120000, 'force_instrumental': True, 'model_id': 'music_v1'}}
             for name, prompt in MUSIC]
    sounds = [{'id': name, 'file': f'audio/sfx/{name}.mp3', 'endpoint': '/v1/sound-generation',
               'payload': {'text': prompt, 'duration_seconds': seconds, 'prompt_influence': .5,
                           'model_id': 'eleven_text_to_sound_v3', 'loop': False}}
              for name, seconds, prompt in SOUNDS]
    reused = []
    for name, source_name, kind, digest in REUSED:
        source = REUSE_BATCH / source_name
        receipt = core.check_source(source, expected_sha=digest)
        reused.append({'id': name, 'file': f'audio/{"music" if kind == "music" else "sfx"}/{name}.mp3',
                       'source': str(source), 'sha256': receipt['sha256'], 'kind': kind,
                       'sourceReceiptSHA256': receipt['receiptSHA256'], 'seconds': receipt['seconds']})
    value = {'schema': SCHEMA, 'topic': 'China economy mechanisms, not cafe sound design', 'music': music,
             'sounds': sounds, 'reuse': reused,
             'mixPolicy': {'voiceLUFS': -16, 'musicLUFS': -29, 'foleyLUFS': -32, 'ambienceLUFS': -39,
                           'crossfadeSeconds': 3, 'voiceSpeed': 1.0, 'noAudioLooping': True},
             'cuePlan': 'audio/cue-plan.json; explicit beat/asset/role cues selected against the final narration and visuals',
             'auditoryAcceptance': 'No actual listening or aesthetic approval established by generation/measurement.'}
    path = batch / 'audio/sound-plan.json'
    if path.exists():
        require(load(path) == value, 'Sound plan changed; retain the old batch and use a revision')
    else:
        save(path, value)
    return value


def _cost(value):
    try:
        number = float(value)
        return number if math.isfinite(number) and number >= 0 else None
    except (TypeError, ValueError):
        return None


def monitored_generate(batch, target, endpoint, payload, *, timed=False, asset_id=None):
    """Observe the existing fail-closed cache/provider helper; no paid retry."""
    batch, target = Path(batch).resolve(), Path(target).resolve()
    digest = core.request_hash(endpoint, payload)
    events = batch / 'benchmark/audio-requests'
    event_path = events / (digest + '.json')
    if event_path.exists():
        previous = load(event_path)
        require(previous['outcome'] == 'completed', 'Unresolved measured provider request; reconcile before retrying')
        core.check_source(target, expected_request=digest)
        return previous
    cache_hit = target.is_file() or ((eleven_audio.CACHE / (digest + '.mp3')).is_file()
                                   and (eleven_audio.CACHE / (digest + '.json')).is_file()
                                   and (not timed or (eleven_audio.CACHE / (digest + '.alignment.json')).is_file()))
    entry = {'schema': 'task-audio-request/1', 'id': asset_id or target.stem, 'endpoint': endpoint,
             'model': payload.get('model_id'), '_requestHash': digest, 'request_hash': digest,
             'file': target.relative_to(batch).as_posix(), 'startedUTC': utc(), 'cache_hit': cache_hit,
             'route': 'verified-cache' if cache_hit else 'new-provider-call', 'outcome': 'started',
             'inputCharacters': len(payload.get('text', '')) if timed else None,
             'requestedSeconds': payload.get('music_length_ms', 0) / 1000 if endpoint == '/v1/music' else payload.get('duration_seconds')}
    save(event_path, entry)
    started = time.monotonic()
    try:
        eleven_audio.generate(target, endpoint, payload, timed=timed)
        verified = core.check_source(target, expected_request=digest)
        receipt = load(target.with_suffix('.receipt.json'))
        entry.update({'outcome': 'completed', 'finishedUTC': utc(), 'elapsedSeconds': round(time.monotonic() - started, 3),
                      'sha256': verified['sha256'], 'receiptSHA256': verified['receiptSHA256'], 'seconds': verified['seconds'],
                      'request_id': receipt.get('request_id'), 'character_cost': receipt.get('character_cost'),
                      'verifiedNewRequestCredits': 0 if cache_hit else _cost(receipt.get('character_cost')),
                      'creditEvidence': 'Cache reuse incurs no new provider request; historical header is not a new charge.' if cache_hit
                          else 'Provider character-cost response header; null means usage not exposed by this receipt.'})
    except BaseException as error:
        entry.update({'outcome': 'unresolved', 'finishedUTC': utc(), 'elapsedSeconds': round(time.monotonic() - started, 3),
                      'errorType': type(error).__name__, 'retryPolicy': 'No automatic retry; inspect retained intent/error receipts.'})
        save(event_path, entry)
        raise
    save(event_path, entry)
    return entry


def voice(batch):
    batch = Path(batch).resolve()
    content = load(batch / 'content.json')
    rows = []
    for index, chapter in enumerate(content['chapters']):
        payload = {'text': chapter['text'], 'model_id': 'eleven_v3', 'language_code': 'vi',
                   'voice_settings': {'stability': .5, 'similarity_boost': .8, 'speed': 1.0}}
        rows.append(monitored_generate(batch, batch / f'audio/{index+1:02}-{chapter["id"]}.mp3',
            f'/v1/text-to-speech/{VOICE}/with-timestamps', payload, timed=True, asset_id=chapter['id']))
    save(batch / 'audio/voice-cost-receipts.json', {'chapterTakes': rows, 'voiceId': VOICE, 'tempo': 1.0})
    return rows


def generate(batch):
    batch = Path(batch).resolve()
    spec, records = plan(batch), []
    for entry in spec['music'] + spec['sounds']:
        cost = monitored_generate(batch, batch / entry['file'], entry['endpoint'], entry['payload'], asset_id=entry['id'])
        record = core.check_source(batch / entry['file'], core.request_hash(entry['endpoint'], entry['payload']))
        records.append({**record, 'id': entry['id'], 'file': entry['file'],
                        'kind': 'music' if entry['endpoint'] == '/v1/music' else 'foley', 'accounting': cost})
        save(batch / 'audio/generation-receipts.json', {'schema': 'china-generated-audio/1', 'sources': records,
             'soundPlanSHA256': sha(batch / 'audio/sound-plan.json'), 'humanListening': 'Not established by generation'})
    for entry in spec['reuse']:
        source, target = Path(entry['source']), batch / entry['file']
        verified = core.check_source(source, expected_sha=entry['sha256'])
        require(verified['receiptSHA256'] == entry['sourceReceiptSHA256'], 'Retained source receipt changed')
        if target.exists():
            core.check_source(target, expected_sha=entry['sha256'])
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
            shutil.copy2(source.with_suffix('.receipt.json'), target.with_suffix('.receipt.json'))
        record = core.check_source(target, expected_sha=entry['sha256'])
        records.append({**record, 'id': entry['id'], 'file': entry['file'], 'kind': 'retained-generated-' + entry['kind'],
                        'originalSource': entry['source'], 'cache_hit': True, 'verifiedNewRequestCredits': 0})
    result = {'schema': 'china-generated-audio/1', 'sources': records,
              'soundPlanSHA256': sha(batch / 'audio/sound-plan.json'), 'humanListening': 'Not established by generation'}
    save(batch / 'audio/generation-receipts.json', result)
    return result


def cue_sheet(data, cue_plan):
    fps, seconds = data['fps'], data['frames'] / data['fps']
    shots = {shot['id']: shot for shot in data['shots']}
    allowed = {name: (length, name in {'port-ambience', 'factory-hum'}) for name, length, _ in SOUNDS}
    allowed.update({'wood-tick': (1.5, False), 'transition': (1.6, False)})
    cues = []
    for row in cue_plan.get('cues', []):
        require(row['beat'] in shots and row['asset'] in allowed and isinstance(row.get('role'), str)
                and row['role'].strip(), 'Cue must identify an actual beat, topic asset and meaningful visual/editorial role')
        shot = shots[row['beat']]
        offset, gain = row.get('offsetSeconds', 0), row.get('gainDB', 0)
        require(all(isinstance(x, (int, float)) and math.isfinite(x) for x in [offset, gain]) and offset >= 0 and -20 <= gain <= 3,
                'Invalid cue offset/gain')
        at = shot['start'] / fps + offset
        require(at < shot['end'] / fps, 'Sound cue falls outside its named beat')
        available, ambience = allowed[row['asset']]
        requested = row.get('durationSeconds', available)
        require(isinstance(requested, (int, float)) and math.isfinite(requested) and 0 < requested <= available,
                'Cue duration must be positive and fit the retained source')
        length = min(requested, shot['end'] / fps - at + (.8 if ambience else .25), seconds - at)
        cues.append({'beat': row['beat'], 'asset': row['asset'], 'time': at, 'duration': length,
                     'gainDB': gain, 'role': row['role'], 'ambience': ambience})
    pivots = []
    for row in cue_plan.get('quietPivots', []):
        require(row['beat'] in shots, 'Unknown quiet pivot beat')
        at = shots[row['beat']]['start'] / fps
        pivots.append({'beat': row['beat'], 'start': max(0, at - .12), 'end': min(seconds, at + 1.4), 'gain': .14})
    require(cues, 'An explicit meaningful cue plan is required; no cafe defaults')
    return cues, pivots


def music_sequence(sources, seconds, crossfade=3):
    by_id = {row['id']: row for row in sources}
    names = ['industrial-networks', 'analytical-detail', 'balance-sheet-friction',
             'quiet-finance', 'operating-network', 'adaptation-horizon']
    require(sum(by_id[name]['seconds'] for name in names) - crossfade * (len(names) - 1) >= seconds,
            'Selected music cannot cover exact take without looping; revise plan before another paid generation')
    cursor, result = 0., []
    for name in names:
        if cursor >= seconds:
            break
        source = by_id[name]
        result.append({'id': name, 'file': source['file'], 'sha256': source['sha256'], 'start': cursor,
                       'end': min(seconds, cursor + source['seconds']), 'sourceSeconds': source['seconds']})
        cursor += source['seconds'] - crossfade
    return result


def mix_dependencies(batch):
    batch = Path(batch)
    data = load(batch / 'data.json')
    timing = {'fps': data['fps'], 'frames': data['frames'], 'captions': data['captions'],
              'shots': [{key: shot[key] for key in ['id', 'start', 'end']} for shot in data['shots']]}
    return {'schema': 'china-audio-dependencies/1', 'timing': timing,
            'narrationSHA256': sha(batch / 'audio/narration.wav'),
            'generationReceiptSHA256': sha(batch / 'audio/generation-receipts.json'),
            'cuePlanSHA256': sha(batch / 'audio/cue-plan.json')}


def pin_mix_dependencies(batch):
    batch = Path(batch)
    value = mix_dependencies(batch)
    path = batch / 'audio/mix-dependencies.json'
    if path.exists():
        require(load(path)['audioDependencies'] == value, 'Audio timing/sources/cue plan changed; use a new mix revision')
        return load(path)
    pinned = {'audioDependencies': value, 'firstDataSHA256': sha(batch / 'data.json'), 'capturedUTC': utc()}
    save(path, pinned)
    return pinned


def mix(batch, public=None):
    """Isolated adapter reuses the tested PCM/stem engine without cafe globals."""
    batch = Path(batch).resolve()
    pinned = pin_mix_dependencies(batch)
    cue_plan = load(batch / 'audio/cue-plan.json')
    final, report_path = batch / 'audio/final-mix.wav', batch / 'audio/mix-report.json'
    if final.exists() and report_path.exists():
        existing = load(report_path)
        if existing['inputs']['dataSHA256'] != sha(batch / 'data.json'):
            require(existing['inputs']['dataSHA256'] == pinned['firstDataSHA256'],
                    'Existing mix is not linked to the first frozen audio dependency timeline')
            require(sha(final) == existing['mix']['sha256'], 'Existing mix bytes changed')
            for source in load(batch / 'audio/generation-receipts.json')['sources']:
                verified = core.check_source(batch / source['file'], expected_sha=source['sha256'])
                require(verified['receiptSHA256'] == source['receiptSHA256'], 'Audio source receipt changed')
            target = Path(public) if public else batch / 'production-public/china'
            target.mkdir(parents=True, exist_ok=True)
            if not (target / 'mix.wav').exists() or sha(target / 'mix.wav') != sha(final):
                shutil.copy2(final, target / 'mix.wav')
            receipt_id = sha(batch / 'data.json')[:16]
            save(batch / f'benchmark/mix-visual-equivalence-{receipt_id}.json', {
                'schema': 'china-mix-visual-equivalence/1', 'newDataSHA256': sha(batch / 'data.json'),
                'originalDataSHA256': pinned['firstDataSHA256'], 'dependenciesSHA256': sha(batch / 'audio/mix-dependencies.json'),
                'mixSHA256': sha(final), 'status': 'reused-identical-mix',
                'scope': 'Exact narration/caption/beat timing, generation receipts and cue plan unchanged; visual-only edits do not require another mix.'})
            return existing
    module_spec = importlib.util.spec_from_file_location('china_mix_engine', Path(core.__file__))
    engine = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(engine)
    engine.plan = plan
    engine.cue_sheet = lambda data: cue_sheet(data, cue_plan)
    engine.music_sequence = music_sequence
    began, started = utc(), time.monotonic()
    cached_mix = (batch / 'audio/final-mix.wav').exists()
    result = engine.mix(batch, public=public or batch / 'production-public/china')
    save(batch / 'benchmark/mix-stage.json', {'schema': 'audio-local-mix-benchmark/1', 'startedUTC': began,
        'finishedUTC': utc(), 'elapsedSeconds': round(time.monotonic() - started, 3), 'cache_hit': cached_mix,
        'outputSHA256': result['mix']['sha256'], 'seconds': result['mix']['seconds'],
        'scope': 'Measured local audio mixing/checking; no provider request or cash/CPU-power estimate.'})
    return result


def benchmark(batch):
    batch = Path(batch).resolve()
    requests_ = [load(path) for path in sorted((batch / 'benchmark/audio-requests').glob('*.json'))]
    completed = [row for row in requests_ if row['outcome'] == 'completed']
    new = [row for row in completed if not row['cache_hit']]
    unknown = [row for row in new if row.get('verifiedNewRequestCredits') is None]
    verified = sum(row['verifiedNewRequestCredits'] for row in new if row.get('verifiedNewRequestCredits') is not None)
    snapshots = {name: load(batch / 'benchmark' / ('subscription-' + name + '.json')) for name in ['start', 'end']
                 if (batch / 'benchmark' / ('subscription-' + name + '.json')).exists()}
    estimate = 0.
    for row in new:
        if row['endpoint'].startswith('/v1/text-to-speech/'):
            estimate += row['inputCharacters'] * .08 / 1000
        else:
            estimate += row.get('requestedSeconds', 0) / 60 * (.15 if row['endpoint'] == '/v1/music' else .12)
    generation = load(batch / 'audio/generation-receipts.json') if (batch / 'audio/generation-receipts.json').exists() else {}
    reused = [row for row in generation.get('sources', []) if row.get('originalSource')]
    result = {'schema': 'china-audio-cost-benchmark/1', 'updatedUTC': utc(), 'requestCount': len(requests_),
        'completedNewProviderCalls': len(new), 'cacheHits': sum(row['cache_hit'] for row in completed),
        'explicitReusedAudioAssets': len(reused), 'verifiedNewRequestCreditSum': verified,
        'newRequestsMissingCreditHeader': [{'id': row['id'], 'endpoint': row['endpoint'], '_requestHash': row['_requestHash']} for row in unknown],
        'newProviderElapsedSeconds': sum(row['elapsedSeconds'] for row in new), 'accountSnapshots': snapshots,
        'datedListPriceUSDEstimate': {'amount': round(estimate, 6), 'checkedDate': '2026-11-13',
            'source': 'https://elevenlabs.io/pricing/api', 'ttsV3USDPer1000InputCharacters': .08,
            'musicUSDPerGeneratedMinute': .15, 'soundEffectsUSDPerGeneratedMinute': .12,
            'basis': 'New completed task requests only, requested duration and input characters; not an invoice, credit-to-dollar conversion, plan allocation or actual cash charge. Taxes excluded.'},
        'limitations': ['Only numeric character-cost response headers from our new requests are summed.',
            'Account usage delta may include other jobs, rollover or adjustments; do not attribute it all to this task.',
            'Missing headers remain unknown; cached historical character_cost values are not newly spent credits.',
            'No account identity, payment details, key or complete account response is retained.',
            'Timing is measured provider-call wall time, not total project production time or listening approval.'],
        'requests': requests_}
    save(batch / 'benchmark/audio-cost-summary.json', result)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--batch', type=Path, required=True)
    parser.add_argument('--phase', required=True, choices=['plan', 'account-start', 'account-end', 'voice', 'generate', 'mix', 'benchmark'])
    parser.add_argument('--public', type=Path)
    args = parser.parse_args()
    if args.phase.startswith('account-'):
        result = subscription_snapshot(args.batch, args.phase.split('-')[1])
    elif args.phase == 'mix':
        result = mix(args.batch, args.public)
    else:
        result = globals()[args.phase](args.batch)
    print(json.dumps(result, ensure_ascii=False, indent=2))
