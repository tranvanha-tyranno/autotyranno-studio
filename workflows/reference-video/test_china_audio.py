"""Offline cost attribution and topic audio guards; no provider or media calls."""
import importlib
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).parent))
import china_audio as c


def test_account_snapshot_retains_only_numeric_usage_and_plan_not_identity(tmp_path):
    class Response:
        ok = True
        status_code = 200

        def json(self):
            return {'tier': 'starter', 'status': 'active', 'character_count': 100, 'character_limit': 900,
                    'email': 'private@example.test', 'user_id': 'do-not-save', 'open_invoices': ['private'],
                    'next_invoice': {'amount': 3}}

    with patch.object(c.eleven_audio, 'key', return_value='not-output'), patch.object(c.requests, 'get', return_value=Response()):
        result = c.subscription_snapshot(tmp_path, 'start')
    assert result['creditsRemaining'] == 800
    assert not any(name in str(result) for name in ['email', 'private', 'user_id', 'next_invoice'])
    with patch.object(c.requests, 'get', side_effect=AssertionError('must reuse pinned snapshot')):
        assert c.subscription_snapshot(tmp_path, 'start') == result


def test_cached_historical_header_is_not_a_new_request_charge(tmp_path, monkeypatch):
    target = tmp_path / 'audio/test.mp3'
    target.parent.mkdir()
    target.write_bytes(b'audio')
    payload = {'text': 'abc', 'model_id': 'eleven_v3'}
    receipt = {'sha256': c.sha(target), 'character_cost': '87', 'request_id': 'historical-request'}
    c.save(target.with_suffix('.receipt.json'), receipt)
    monkeypatch.setattr(c.eleven_audio, 'generate', lambda *a, **kw: target)
    monkeypatch.setattr(c.core, 'check_source', lambda *a, **kw: {'sha256': c.sha(target), 'receiptSHA256': 'x', 'seconds': 1})
    result = c.monitored_generate(tmp_path, target, '/v1/text-to-speech/pinned/with-timestamps', payload, timed=True)
    assert result['cache_hit'] is True
    assert result['character_cost'] == '87'
    assert result['verifiedNewRequestCredits'] == 0


def test_unknown_new_header_stays_unknown_and_is_not_retried(tmp_path, monkeypatch):
    monkeypatch.setattr(c.eleven_audio, 'CACHE', tmp_path / 'empty-cache')
    calls = []

    def fake(target, *args, **kwargs):
        calls.append(1)
        target.parent.mkdir(parents=True)
        target.write_bytes(b'audio')
        c.save(target.with_suffix('.receipt.json'), {'character_cost': None, 'request_id': None})

    monkeypatch.setattr(c.eleven_audio, 'generate', fake)
    monkeypatch.setattr(c.core, 'check_source', lambda *a, **kw: {'sha256': 'x', 'receiptSHA256': 'y', 'seconds': 2})
    target = tmp_path / 'audio/new.mp3'
    result = c.monitored_generate(tmp_path, target, '/v1/music', {'music_length_ms': 2000, 'model_id': 'music_v1'})
    assert result['cache_hit'] is False and result['verifiedNewRequestCredits'] is None
    assert c.monitored_generate(tmp_path, target, '/v1/music', {'music_length_ms': 2000, 'model_id': 'music_v1'}) == result
    assert len(calls) == 1
    report = c.benchmark(tmp_path)
    assert report['verifiedNewRequestCreditSum'] == 0
    assert len(report['newRequestsMissingCreditHeader']) == 1
    assert report['datedListPriceUSDEstimate']['amount'] == .005


def test_transport_failure_leaves_unresolved_intent_and_blocks_duplicate_attempt(tmp_path, monkeypatch):
    monkeypatch.setattr(c.eleven_audio, 'CACHE', tmp_path / 'empty-cache')
    calls = []

    def fail(*args, **kwargs):
        calls.append(1)
        raise RuntimeError('provider transport failure')

    monkeypatch.setattr(c.eleven_audio, 'generate', fail)
    args = (tmp_path, tmp_path / 'audio/new.mp3', '/v1/music', {'music_length_ms': 1000})
    with pytest.raises(RuntimeError):
        c.monitored_generate(*args)
    with pytest.raises(ValueError, match='Unresolved'):
        c.monitored_generate(*args)
    assert len(calls) == 1


def test_benchmark_uses_per_request_cost_not_account_delta(tmp_path):
    folder = tmp_path / 'benchmark/audio-requests'
    c.save(folder / 'a.json', {'outcome': 'completed', 'cache_hit': False, 'verifiedNewRequestCredits': 17,
        'elapsedSeconds': 2, 'endpoint': '/v1/text-to-speech/id/with-timestamps', 'inputCharacters': 100})
    c.save(folder / 'b.json', {'outcome': 'completed', 'cache_hit': True, 'verifiedNewRequestCredits': 0,
        'character_cost': 900, 'elapsedSeconds': .1, 'endpoint': '/v1/music'})
    c.save(tmp_path / 'benchmark/subscription-start.json', {'character_count': 0})
    c.save(tmp_path / 'benchmark/subscription-end.json', {'character_count': 2000})
    report = c.benchmark(tmp_path)
    assert report['verifiedNewRequestCreditSum'] == 17
    assert report['completedNewProviderCalls'] == 1 and report['cacheHits'] == 1
    assert report['newProviderElapsedSeconds'] == 2


def test_context_cues_reject_cafe_defaults_and_out_of_shot_offsets():
    data = {'fps': 30, 'frames': 300, 'shots': [{'id': 'f1', 'start': 0, 'end': 150}]}
    with pytest.raises(ValueError, match='topic asset'):
        c.cue_sheet(data, {'cues': [{'beat': 'f1', 'asset': 'espresso', 'role': 'wrong topic'}]})
    with pytest.raises(ValueError, match='outside'):
        c.cue_sheet(data, {'cues': [{'beat': 'f1', 'asset': 'factory-hum', 'offsetSeconds': 6, 'role': 'factory shown'}]})
    cues, pivots = c.cue_sheet(data, {'cues': [{'beat': 'f1', 'asset': 'factory-hum', 'role': 'factory shown'}]})
    assert cues[0]['ambience'] is True and cues[0]['duration'] == 5.8


def test_music_coverage_cannot_fill_missing_time_with_a_loop():
    sources = [{'id': name, 'seconds': 120, 'file': name + '.mp3', 'sha256': 'x'} for name in [
        'industrial-networks', 'analytical-detail', 'balance-sheet-friction', 'quiet-finance',
        'operating-network', 'adaptation-horizon']]
    with pytest.raises(ValueError, match='without looping'):
        c.music_sequence(sources, 710)
    rows = c.music_sequence(sources, 600)
    assert rows[-1]['end'] == 600 and len({row['id'] for row in rows}) == len(rows)


def test_visual_only_data_edits_reuse_exact_mix_but_timing_edits_stop(tmp_path, monkeypatch):
    data = {'fps': 30, 'frames': 300, 'captions': [],
            'shots': [{'id': 'f1', 'start': 0, 'end': 300, 'headline': 'First visual'}]}
    c.save(tmp_path / 'data.json', data)
    c.save(tmp_path / 'audio/generation-receipts.json', {'sources': []})
    c.save(tmp_path / 'audio/cue-plan.json', {'cues': []})
    (tmp_path / 'audio/narration.wav').write_bytes(b'narration')
    pinned = c.pin_mix_dependencies(tmp_path)
    final = tmp_path / 'audio/final-mix.wav'
    final.write_bytes(b'pinned exact mix')
    report = {'inputs': {'dataSHA256': pinned['firstDataSHA256']}, 'mix': {'sha256': c.sha(final)}}
    c.save(tmp_path / 'audio/mix-report.json', report)
    data['shots'][0]['headline'] = 'Different photographic design'
    c.save(tmp_path / 'data.json', data)
    monkeypatch.setattr(c.importlib.util, 'spec_from_file_location', lambda *a: pytest.fail('must not load mixing engine'))
    assert c.mix(tmp_path) == report
    assert final.read_bytes() == b'pinned exact mix'
    assert list((tmp_path / 'benchmark').glob('mix-visual-equivalence-*.json'))
    data['shots'][0]['end'] = 299
    c.save(tmp_path / 'data.json', data)
    with pytest.raises(ValueError, match='timing/sources/cue plan changed'):
        c.mix(tmp_path)
