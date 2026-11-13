"""Offline cafe sound planning plus a small real local three-stem mix."""
import hashlib
import json
from pathlib import Path
import sys
import wave

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).parent))
import business_audio as a


def timeline(seconds=48):
    ids = ['h01', 'h03', 'u01', 'u02', 'u03', 'u06', 'b01', 'b03', 'v01', 'p01', 'p03',
           'p09', 'm01', 'm05', 'm07', 'm08', 'a01', 'a02', 'e01', 'e05']
    frames = round(seconds * 30)
    shots = [{'id': key, 'start': round(i * frames / len(ids)),
              'end': round((i + 1) * frames / len(ids))} for i, key in enumerate(ids)]
    return {'fps': 30, 'frames': frames, 'audio': 'business/mix.wav', 'shots': shots}


def test_plan_has_five_distinct_instrumentals_and_ten_context_sounds_without_provider(tmp_path, monkeypatch):
    monkeypatch.setattr(a.eleven_audio, 'generate', lambda *args, **kwargs: pytest.fail('Planning contacted provider'))
    spec = a.plan(tmp_path)
    assert len(spec['music']) == 5 and len(spec['sounds']) == 10
    assert len({entry['payload']['prompt'] for entry in spec['music']}) == 5
    assert all(entry['payload']['music_length_ms'] == 120000 and entry['payload']['force_instrumental']
               and entry['payload']['model_id'] == 'music_v1' for entry in spec['music'])
    assert a.plan(tmp_path) == spec


def test_cues_follow_exact_shot_frames_and_remain_inside_timeline():
    data = timeline()
    cues, pivots = a.cue_sheet(data)
    by_id = {shot['id']: shot for shot in data['shots']}
    assert len({cue['asset'] for cue in cues}) == 10
    assert all(0 <= cue['time'] < 48 and cue['time'] + cue['duration'] <= 48 for cue in cues)
    assert next(cue for cue in cues if cue['beat'] == 'u03')['time'] == pytest.approx(by_id['u03']['start'] / 30 + .25)
    assert [pivot['beat'] for pivot in pivots] == ['p09', 'm08']
    assert [cue['beat'] for cue in cues if cue['ambience']] == ['h01', 'v01', 'e01']


def test_missing_or_duplicate_beats_are_not_guessed():
    data = timeline()
    data['shots'][1]['id'] = 'h01'
    with pytest.raises(ValueError, match='Duplicate'):
        a.cue_sheet(data)
    data = timeline()
    data['shots'] = [shot for shot in data['shots'] if shot['id'] != 'p09']
    with pytest.raises(ValueError, match='pivot'):
        a.cue_sheet(data)


def test_milk_steam_foley_follows_the_visible_steam_beat_not_equipment_purchase():
    data = timeline()
    cues, _ = a.cue_sheet(data)
    steam = [cue for cue in cues if cue['asset'] == 'milk-steam']
    assert len(steam) == 1 and steam[0]['beat'] == 'u06'
    shot = next(shot for shot in data['shots'] if shot['id'] == 'u06')
    assert steam[0]['time'] == pytest.approx(shot['start'] / data['fps'] + .3)
    assert all(cue['asset'] != 'milk-steam' for cue in cues if cue['beat'] == 'm05')


def score_sources(seconds=120):
    return [{'id': name, 'file': name + '.mp3', 'sha256': 'a' * 64,
             'seconds': 50 if name == 'motion-bridge' else seconds}
            for name in [name for name, _ in a.MUSIC] + ['motion-bridge', 'agency-bridge']]


def test_long_take_selects_additional_retained_score_before_outro_without_looping():
    sections = a.music_sequence(score_sources(), 650)
    assert sections[-1]['id'] == 'hopeful-outro'
    assert sections[-2]['id'] == 'agency-bridge'
    assert len({section['id'] for section in sections}) == len(sections)
    with pytest.raises(ValueError, match='without looping'):
        a.music_sequence(score_sources(), 900)


def test_mix_rejects_voice_extending_beyond_compiled_timeline_before_generation_lookup(tmp_path, monkeypatch):
    a.save(tmp_path / 'data.json', timeline(10))
    (tmp_path / 'audio').mkdir(exist_ok=True)
    (tmp_path / 'audio/narration.wav').write_bytes(b'fixture')
    monkeypatch.setattr(a, 'duration', lambda path: 10.2)
    with pytest.raises(ValueError, match='refuse truncation'):
        a.mix(tmp_path)


def test_source_bytes_must_match_retained_provider_receipt(tmp_path, monkeypatch):
    path = tmp_path / 'music.mp3'
    path.write_bytes(b'altered audio')
    a.save(path.with_suffix('.receipt.json'), {'sha256': hashlib.sha256(b'original audio').hexdigest()})
    monkeypatch.setattr(a, 'duration', lambda path: 120)
    with pytest.raises(ValueError, match='differ from receipt'):
        a.check_source(path)


def make_wave(path, seconds, frequency, amplitude=.10):
    path.parent.mkdir(parents=True, exist_ok=True)
    rate = 48000
    samples = (np.sin(np.arange(round(seconds * rate)) * 2 * np.pi * frequency / rate)
               * amplitude * 32767).astype('<i2')
    with wave.open(str(path), 'wb') as stream:
        stream.setnchannels(1)
        stream.setsampwidth(2)
        stream.setframerate(rate)
        stream.writeframes(samples.tobytes())


def test_small_real_mix_preserves_narration_and_reports_three_stems(tmp_path):
    spec = a.plan(tmp_path)
    data = timeline()
    a.save(tmp_path / 'data.json', data)
    make_wave(tmp_path / 'audio/narration.wav', 47.5, 220, .16)
    voice_sha = a.sha(tmp_path / 'audio/narration.wav')
    records = []
    for i, entry in enumerate(spec['music'] + spec['sounds'] + spec['reuse']):
        path = tmp_path / entry['file']
        seconds = 12 if entry in spec['music'] else 5 if entry['id'] == 'motion-bridge' else 12 if entry['id'] == 'agency-bridge' else entry['payload']['duration_seconds']
        make_wave(path, seconds, 300 + i * 19, .05)
        # The retained fixtures are local synthetic test inputs, never provider output.
        if entry in spec['reuse']:
            entry['sha256'] = a.sha(path)
        receipt = {'sha256': a.sha(path), 'provider': 'offline synthetic fixture',
                   'model': 'test', 'request_hash': a.request_hash(entry['endpoint'], entry['payload']) if 'endpoint' in entry else 'reused-fixture'}
        a.save(path.with_suffix('.receipt.json'), receipt)
        records.append({'id': entry['id'], 'file': entry['file'], 'sha256': a.sha(path),
                        'receiptSHA256': a.sha(path.with_suffix('.receipt.json'))})
    # Pin fixture-only reuse hashes without changing production constants or files.
    original_plan = a.plan
    try:
        a.plan = lambda batch: spec
        a.save(tmp_path / 'audio/generation-receipts.json', {
            'sources': records, 'soundPlanSHA256': a.sha(tmp_path / 'audio/sound-plan.json')})
        result = a.mix(tmp_path)
        assert result['inputs']['narrationSHA256'] == voice_sha
        assert a.sha(tmp_path / 'audio/narration.wav') == voice_sha
        assert abs(result['mix']['seconds'] - 48) <= .06
        assert len(result['stems']) == 2
        assert result['maximumFFmpegInputs'] == 6
        assert len(result['cueSnippets']) == 18
        assert float(result['mix']['loudnessMeasurement']['input_tp']) < 0
        assert result['manualListening'] is False
        assert a.sha(tmp_path / 'production-public/business/mix.wav') == result['mix']['sha256']
        # Re-run verifies the pinned result and restores a missing public copy.
        (tmp_path / 'production-public/business/mix.wav').unlink()
        assert a.mix(tmp_path)['mix']['sha256'] == result['mix']['sha256']
        assert (tmp_path / 'production-public/business/mix.wav').is_file()
    finally:
        a.plan = original_plan
