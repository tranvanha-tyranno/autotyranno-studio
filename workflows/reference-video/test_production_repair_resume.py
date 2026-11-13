"""Offline integrity guarantees for explicitly resuming a failed repair attempt.

The fake MP4s are deliberately not videos. Decoder calls are isolated so these
tests cannot accidentally launch a renderer, FFmpeg, or a paid retry.
"""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import shutil
import sys

import pytest

sys.path.insert(0, str(Path(__file__).parent))
import production_repair as r


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')


def write_bytes(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(value)


def digest(value):
    return hashlib.sha256(value).hexdigest()


def snapshot_tree(folder):
    return {path.relative_to(folder).as_posix(): r.sha(path)
            for path in folder.rglob('*') if path.is_file()}


@pytest.fixture
def resume_attempt(tmp_path, monkeypatch):
    """A legacy failed attempt, with two retained source snapshots and a bundle."""
    previous = tmp_path / 'previous/long'
    current = tmp_path / 'revision/long'
    attempt = tmp_path / 'revision/repair-attempts/fixture-repair'
    manifest = tmp_path / 'revision/production.json'
    data = {'direction': 'long', 'fps': 30, 'frames': 120, 'title': 'Resume fixture',
            'audio': 'directions/long/mix.wav', 'captions': [], 'shots': []}
    manifest_data = {'schema': 'reference-video-production/1', 'direction': 'long',
                     'id': 'resume-fixture', 'title': 'Resume fixture'}
    props = {'data': data}
    image = b'inspected source image bytes'
    asset_key = 'directions/long/inspected.jpg'
    assets = {'assets': [{'publicFile': asset_key, 'publicSHA256': digest(image)}]}
    mix = b'exact retained mix bytes'
    audio_sources = {'mix': {'sha256': digest(mix)}}
    old_final = b'previous full-duration MP4 fixture'
    write_json(manifest, manifest_data)
    for folder in (previous, current):
        write_json(folder / 'data.json', data)
        write_json(folder / 'props.json', props)
        write_json(folder / 'profile.json', {'name': 'fixed voice and photo gallery'})
        write_json(folder / 'render-assets.json', assets)
        write_json(folder / 'image-sources.json', {'assets': []})
        write_json(folder / 'audio-sources.json', audio_sources)
        write_json(folder / 'production-manifest.json', manifest_data)
        write_bytes(folder / 'script.txt', b'Unchanged exact spoken script.\n')
        write_bytes(folder / 'audio/final-mix.wav', mix)
    write_bytes(previous / 'final.mp4', old_final)
    write_json(previous / 'qa/report.json', {'frameCountPass': True,
               'decodedFrames': 120, 'videoSHA256': digest(old_final)})

    source = attempt / 'source-snapshot'
    source_files = {
        'cinematic/src/directions/Film.tsx': 'export const Film = () => <div>Original</div>;\n',
        'cinematic/src/directions-entry.tsx': 'export const entry = "DirectionPreview";\n',
        'production_repair.py': '# retained runner before resume support\n',
    }
    for name, text in source_files.items():
        write_bytes(source / name, text.encode('utf-8'))
    for name in ['data.json', 'props.json', 'profile.json', 'script.txt',
                 'render-assets.json', 'image-sources.json', 'audio-sources.json',
                 'production-manifest.json']:
        target = source / 'batch/long' / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(current / name, target)
    write_json(source / 'hashes.json', [
        {'file': name, 'sha256': value} for name, value in sorted(snapshot_tree(source).items())])

    old_snapshot = attempt / 'previous-source-snapshot'
    for name in ['data.json', 'script.txt', 'audio-sources.json', 'render-assets.json', 'qa/report.json']:
        target = old_snapshot / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(previous / name, target)
    write_json(old_snapshot / 'hashes.json', [
        {'file': name, 'sha256': value} for name, value in sorted(snapshot_tree(old_snapshot).items())])
    write_json(attempt / 'source-receipts.json', {
        key: {'file': str(path), 'sha256': r.sha(path)} for key, path in {
            'previousFinal': previous / 'final.mp4', 'previousData': previous / 'data.json',
            'newManifest': manifest, 'newData': current / 'data.json',
            'exactMix': current / 'audio/final-mix.wav',
        }.items()})

    staged = attempt / 'public'
    write_bytes(staged / asset_key, image)
    write_bytes(staged / 'directions/long/mix.wav', mix)
    shutil.copy2(current / 'data.json', staged / 'directions/long/data.json')
    bundle = attempt / 'bundle'
    write_bytes(bundle / 'index.html', b'<script src="bundle.js"></script>')
    write_bytes(bundle / 'bundle.js', b'console.log("retained bundle");\n//# sourceMappingURL=bundle.js.map\n')
    write_json(bundle / 'bundle.js.map', {
        'version': 3, 'file': 'bundle.js', 'names': [], 'mappings': '',
        'sources': ['webpack://cinematic/./src/directions/Film.tsx',
                    'webpack://cinematic/./src/directions-entry.tsx'],
        'sourcesContent': [source_files['cinematic/src/directions/Film.tsx'],
                           source_files['cinematic/src/directions-entry.tsx']],
    })
    shutil.copytree(staged, bundle, dirs_exist_ok=True)

    intervals = [{'start': 0, 'endExclusive': 37, 'remotionFrames': '0-36', 'frames': 37},
                 {'start': 60, 'endExclusive': 97, 'remotionFrames': '60-96', 'frames': 37}]
    plan = {'schema': 'reference-video-repair-plan/1', 'previous': str(previous),
            'current': str(current), 'fps': 30, 'frames': 120,
            'changedShots': ['c1', 'c3'], 'intervals': intervals,
            'segments': r.segments_for([[0, 37], [60, 97]], 120),
            'oldFinalSHA256': r.sha(previous / 'final.mp4'),
            'exactMixSHA256': r.sha(current / 'audio/final-mix.wav'),
            'captionsUnchanged': True, 'timingUnchanged': True, 'userAcceptance': 'pending'}
    options = {'memoryProfile': 'bounded', 'concurrency': 1, 'crf': 19,
               'mediaCacheSizeInBytes': 268435456,
               'scope': 'Decoded media cache only, not a total RAM cap.'}
    steps = [{'command': ['node', 'remotion-cli.js', 'bundle', 'directions-entry.tsx',
                         '--out-dir=' + str(bundle), '--public-dir=' + str(staged)],
              'status': 'completed', 'returncode': 0, 'log': str(attempt / 'bundle.log')}]
    for index, interval in enumerate(intervals):
        patch = attempt / f'patch-{index:02}.mp4'
        write_bytes(patch, f'patch-{index:02}-retained-bytes'.encode())
        steps.append({'command': ['node', 'remotion-cli.js', 'render', str(bundle),
                      'DirectionPreview', str(patch), '--props=' + str(current / 'props.json'),
                      '--frames=' + interval['remotionFrames'], '--muted'],
                      'status': 'completed' if index == 0 else 'failed',
                      'returncode': 0 if index == 0 else 1,
                      'log': str(attempt / f'patch-{index:02}.log')})
    state = {'attempt': attempt.name, 'status': 'failed', 'steps': steps,
             'plan': plan, 'renderOptions': options, 'errorType': 'OSError',
             'error': 'No space left on device', 'aestheticAcceptance': 'pending user feedback'}
    write_json(attempt / 'attempt.json', state)

    def no_subprocess(*args, **kwargs):
        raise AssertionError('Resume integrity tests must not start external processes')

    monkeypatch.setattr(r.subprocess, 'run', no_subprocess)
    return {'root': tmp_path, 'attempt': attempt, 'previous': previous, 'current': current,
            'manifest': manifest, 'plan': plan, 'options': options, 'state': state,
            'source': source, 'staged': staged, 'bundle': bundle, 'assetKey': asset_key}


def validate(fixture, **overrides):
    values = {key: fixture[key] for key in ['attempt', 'previous', 'current', 'plan', 'options']}
    values['manifest_path'] = fixture['manifest']
    values.update(overrides)
    return r.validate_resume(**values)


def test_tree_receipt_is_sorted_relative_and_hashes_actual_bytes(tmp_path):
    write_bytes(tmp_path / 'z.bin', b'last')
    write_bytes(tmp_path / 'nested/a.bin', b'first')
    (tmp_path / 'empty').mkdir()
    assert r.tree_receipt(tmp_path) == [
        {'file': 'nested/a.bin', 'sha256': digest(b'first')},
        {'file': 'z.bin', 'sha256': digest(b'last')},
    ]


def test_valid_legacy_validation_is_read_only(resume_attempt):
    fixture = resume_attempt
    before = snapshot_tree(fixture['root'])
    result = validate(fixture)
    assert result['state'] == fixture['state']
    assert result['legacyAdopted'] is True
    assert result['integrity']
    assert snapshot_tree(fixture['root']) == before


def test_remotion_bundle_public_subdirectory_is_supported(resume_attempt):
    fixture = resume_attempt
    public = fixture['bundle'] / 'public'
    public.mkdir()
    shutil.move(str(fixture['bundle'] / 'directions'), str(public / 'directions'))
    before = snapshot_tree(fixture['root'])
    assert validate(fixture)['legacyAdopted'] is True
    assert snapshot_tree(fixture['root']) == before


@pytest.mark.parametrize('key,relative', [
    ('current', 'data.json'), ('current', 'props.json'), ('current', 'render-assets.json'),
    ('current', 'production-manifest.json'), ('current', 'script.txt'),
    ('previous', 'data.json'), ('previous', 'final.mp4'),
    ('current', 'audio/final-mix.wav'), ('source', 'cinematic/src/directions/Film.tsx'),
    ('staged', 'directions/long/inspected.jpg'), ('staged', 'directions/long/mix.wav'),
    ('bundle', 'directions/long/inspected.jpg'),
])
def test_changed_retained_input_rejected_before_reusing_patches(resume_attempt, key, relative):
    fixture = resume_attempt
    path = fixture[key] / relative
    path.write_bytes(path.read_bytes() + b'changed after failed attempt')
    before = snapshot_tree(fixture['root'])
    with pytest.raises(ValueError):
        validate(fixture)
    assert snapshot_tree(fixture['root']) == before


def test_changed_manifest_input_is_rejected(resume_attempt):
    fixture = resume_attempt
    write_json(fixture['manifest'], {'direction': 'long', 'title': 'Changed externally'})
    with pytest.raises(ValueError):
        validate(fixture)


def test_extra_staged_file_is_not_silently_adopted(resume_attempt):
    fixture = resume_attempt
    write_bytes(fixture['staged'] / 'directions/long/unreceipted.jpg', b'not inspected')
    with pytest.raises(ValueError, match='Staged render assets'):
        validate(fixture)


def test_attempt_from_another_batch_is_rejected(resume_attempt):
    fixture = resume_attempt
    with pytest.raises(ValueError, match='exact new batch'):
        validate(fixture, current=fixture['root'] / 'other-revision/long')


@pytest.mark.parametrize('key', ['plan', 'options'])
def test_resume_cannot_silently_change_plan_or_render_options(resume_attempt, key):
    fixture = resume_attempt
    altered = deepcopy(fixture[key])
    if key == 'plan':
        altered['intervals'][0]['endExclusive'] += 1
    else:
        altered['crf'] += 1
    with pytest.raises(ValueError):
        validate(fixture, **{key: altered})


def test_legacy_adoption_requires_matching_retained_tsx_sources(resume_attempt):
    fixture = resume_attempt
    path = fixture['bundle'] / 'bundle.js.map'
    sourcemap = json.loads(path.read_text(encoding='utf-8'))
    sourcemap['sourcesContent'][0] = 'export const Film = () => <div>Changed</div>;'
    write_json(path, sourcemap)
    with pytest.raises(ValueError):
        validate(fixture)


def test_legacy_adoption_without_a_source_map_is_rejected(resume_attempt):
    fixture = resume_attempt
    (fixture['bundle'] / 'bundle.js.map').unlink()
    with pytest.raises(ValueError):
        validate(fixture)


def test_pinned_resume_integrity_rejects_changed_bundle_bytes(resume_attempt):
    fixture = resume_attempt
    first = validate(fixture)
    write_json(fixture['attempt'] / 'resume-integrity.json', first['integrity'])
    assert validate(fixture)['legacyAdopted'] is False
    path = fixture['bundle'] / 'bundle.js'
    path.write_bytes(path.read_bytes() + b'\nchanged compiled bundle')
    with pytest.raises(ValueError):
        validate(fixture)


def test_completed_patch_is_redecoded_before_reuse(resume_attempt, monkeypatch):
    fixture = resume_attempt
    calls = []

    def decoded(path, frames, fps):
        calls.append((path, frames, fps))
        return {'decodedFrames': frames, 'fps': fps, 'sha256': r.sha(path)}

    monkeypatch.setattr(r, 'check_decoded', decoded)
    interval = fixture['plan']['intervals'][0]
    result = r.validated_patch(fixture['attempt'], 0, interval, 30, fixture['state'])
    assert calls == [(fixture['attempt'] / 'patch-00.mp4', 37, 30)]
    assert result['decodedFrames'] == 37
    assert result['sha256'] == r.sha(fixture['attempt'] / 'patch-00.mp4')


def test_completed_patch_with_bad_frame_count_is_not_reused(resume_attempt, monkeypatch):
    fixture = resume_attempt

    def bad_decode(path, frames, fps):
        raise ValueError('Patch/repaired MP4 frame count or FPS differs')

    monkeypatch.setattr(r, 'check_decoded', bad_decode)
    with pytest.raises(ValueError, match='frame count'):
        r.validated_patch(fixture['attempt'], 0, fixture['plan']['intervals'][0], 30, fixture['state'])


def test_checkpointed_patch_rejects_changed_bytes_before_decode(resume_attempt, monkeypatch):
    fixture = resume_attempt
    path = fixture['attempt'] / 'patch-00.mp4'
    interval = fixture['plan']['intervals'][0]
    state = deepcopy(fixture['state'])
    state['patches'] = {'0': {'file': path.name, 'interval': interval,
                             'decode': {'decodedFrames': 37, 'fps': 30, 'sha256': r.sha(path)}}}
    path.write_bytes(b'changed encoded patch after checkpoint')

    def no_decode(*args, **kwargs):
        raise AssertionError('Changed patch hashes must fail before decode')

    monkeypatch.setattr(r, 'check_decoded', no_decode)
    with pytest.raises(ValueError, match='hash/interval'):
        r.validated_patch(fixture['attempt'], 0, interval, 30, state)


def test_checkpointed_decode_receipt_cannot_claim_wrong_frame_count(resume_attempt, monkeypatch):
    fixture = resume_attempt
    path = fixture['attempt'] / 'patch-00.mp4'
    interval = fixture['plan']['intervals'][0]
    state = deepcopy(fixture['state'])
    state['patches'] = {'0': {'file': path.name, 'interval': interval,
                             'decode': {'decodedFrames': 36, 'fps': 30, 'sha256': r.sha(path)}}}
    monkeypatch.setattr(r, 'check_decoded', lambda *args: {
        'decodedFrames': 37, 'fps': 30, 'sha256': r.sha(path)})
    with pytest.raises(ValueError, match='decode differs'):
        r.validated_patch(fixture['attempt'], 0, interval, 30, state)


def test_completed_log_cannot_be_reused_for_a_different_interval(resume_attempt, monkeypatch):
    fixture = resume_attempt
    state = deepcopy(fixture['state'])
    state['steps'][1]['command'][-2] = '--frames=0-35'

    def no_decode(*args, **kwargs):
        raise AssertionError('Wrong patch interval must fail before decode')

    monkeypatch.setattr(r, 'check_decoded', no_decode)
    with pytest.raises(ValueError, match='interval changed'):
        r.validated_patch(fixture['attempt'], 0, fixture['plan']['intervals'][0], 30, state)


def test_failed_patch_is_not_adopted_even_when_its_file_exists(resume_attempt, monkeypatch):
    fixture = resume_attempt

    def no_decode(*args, **kwargs):
        raise AssertionError('A failed step is not a completed patch')

    monkeypatch.setattr(r, 'check_decoded', no_decode)
    assert r.validated_patch(fixture['attempt'], 1, fixture['plan']['intervals'][1], 30,
                             fixture['state']) is None


def test_incomplete_patch_is_retained_under_a_new_name_before_retry(tmp_path):
    path = tmp_path / 'patch-02.mp4'
    original = b'incomplete encoded bytes are diagnostic evidence'
    path.write_bytes(original)
    archived = r.archive_incomplete(path)
    assert archived.parent == tmp_path
    assert archived.suffix == '.mp4'
    assert archived != path and 'failed-' in archived.name
    assert archived.read_bytes() == original
    assert not path.exists()
    assert r.archive_incomplete(path) is None
