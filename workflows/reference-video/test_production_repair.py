"""Offline guarantees for bounded shot repairs and a tiny real FFmpeg splice."""
import json
from pathlib import Path
import subprocess
import sys
import wave

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).parent))
import production_repair as r


@pytest.fixture
def films(tmp_path):
    old, new = tmp_path / 'old/long', tmp_path / 'new/long'
    data = {'direction': 'long', 'fps': 30, 'frames': 120, 'title': 'Original pilot',
        'audio': 'directions/long/mix.wav', 'captions': [{'start': 0, 'end': 3.8, 'text': 'Original words.'}],
        'shots': []}
    assets = []
    for index in range(4):
        key = f'c{index + 1}'
        file = f'directions/long/{key}.jpg'
        data['shots'].append({'id': key, 'start': index * 30, 'end': (index + 1) * 30,
            'phase': 'content', 'phrase': 'Original ' + key, 'narrationClause': 'Original clause ' + key,
            'layout': 'full', 'headline': 'Caption ' + key, 'sourceNote': 'Original example',
            'images': [{'file': file, 'credit': 'Original', 'aspect': 16 / 9, 'focus': [50, 50]}]})
        assets.append({'publicFile': file, 'publicSHA256': ('a' if index % 2 else 'b') * 64})
    for folder in [old, new]:
        (folder / 'audio').mkdir(parents=True)
        for name in ['narration-original.mp3', 'narration-original.alignment.json', 'narration-original.receipt.json', 'final-mix.wav']:
            (folder / 'audio' / name).write_bytes(('identical ' + name).encode())
        (folder / 'script.txt').write_text('Original script.\n', encoding='utf-8')
        (folder / 'data.json').write_text(json.dumps(data), encoding='utf-8')
        (folder / 'render-assets.json').write_text(json.dumps({'assets': assets}), encoding='utf-8')
    (old / 'final.mp4').write_bytes(b'old complete final fixture')
    return old, new


def mutate(folder, change):
    path = folder / 'data.json'
    data = json.loads(path.read_text(encoding='utf-8'))
    change(data)
    path.write_text(json.dumps(data), encoding='utf-8')


def test_interval_includes_transition_tail_and_clips_last_scene(films):
    old, new = films
    plan = r.repair_plan(old, new, ['c2'])
    assert plan['intervals'] == [{'start': 30, 'endExclusive': 67, 'remotionFrames': '30-66', 'frames': 37}]
    assert [(s['kind'], s['start'], s['end']) for s in plan['segments']] == [
        ('previous', 0, 30), ('patch', 30, 67), ('previous', 67, 120)]
    last = r.repair_plan(old, new, ['c4'])
    assert last['intervals'][0]['endExclusive'] == 120
    assert sum(s['frames'] for s in last['segments']) == 120


def test_multiple_disjoint_ranges_keep_all_frames_and_adjacent_ranges_merge(films):
    old, new = films
    disjoint = r.repair_plan(old, new, ['c1', 'c3'])
    assert [(x['start'], x['endExclusive']) for x in disjoint['intervals']] == [(0, 37), (60, 97)]
    assert sum(x['frames'] for x in disjoint['segments']) == 120
    adjacent = r.repair_plan(old, new, ['c2', 'c3'])
    assert [(x['start'], x['endExclusive']) for x in adjacent['intervals']] == [(30, 97)]
    assert r.merge_intervals([(10, 20), (20, 25), (15, 23), (40, 45)]) == [[10, 25], [40, 45]]


def test_unknown_empty_and_duplicate_changed_shots_are_rejected(films):
    old, new = films
    for selected, message in [([], 'unique'), (['c1', 'c1'], 'unique'), (['missing'], 'Unknown')]:
        with pytest.raises(ValueError, match=message):
            r.repair_plan(old, new, selected)


@pytest.mark.parametrize('field,value', [('frames', 121), ('fps', 24), ('title', 'Different title'),
    ('captions', [{'start': 0, 'end': 3.8, 'text': 'Different spoken words.'}])])
def test_whole_timeline_and_captions_must_match(films, field, value):
    old, new = films
    mutate(new, lambda d: d.update({field: value}))
    with pytest.raises(ValueError, match='cannot change timeline'):
        r.repair_plan(old, new, ['c2'])


@pytest.mark.parametrize('field,value', [('start', 29), ('end', 61), ('phase', 'cta'),
    ('phrase', 'Other phrase'), ('narrationClause', 'Other clause')])
def test_even_selected_shot_cannot_change_timing_or_spoken_clause(films, field, value):
    old, new = films
    mutate(new, lambda d: d['shots'][1].update({field: value}))
    with pytest.raises(ValueError, match='narration/timing'):
        r.repair_plan(old, new, ['c2'])


@pytest.mark.parametrize('name', ['narration-original.mp3', 'narration-original.alignment.json',
    'narration-original.receipt.json', 'final-mix.wav'])
def test_exact_audio_and_alignment_bytes_are_locked(films, name):
    old, new = films
    (new / 'audio' / name).write_bytes(b'changed take or mix')
    with pytest.raises(ValueError, match='exact narration/mix'):
        r.repair_plan(old, new, ['c2'])


def test_script_and_unselected_appearance_cannot_change(films):
    old, new = films
    mutate(new, lambda d: d['shots'][0].update({'headline': 'Unselected pixels changed'}))
    with pytest.raises(ValueError, match='Unselected shot appearance'):
        r.repair_plan(old, new, ['c2'])
    mutate(new, lambda d: d['shots'][0].update({'headline': 'Caption c1'}))
    (new / 'script.txt').write_text('Changed script', encoding='utf-8')
    with pytest.raises(ValueError, match='spoken script'):
        r.repair_plan(old, new, ['c2'])


def test_batch_paths_can_change_but_unselected_derivative_hashes_cannot(films):
    old, new = films
    mutate(new, lambda d: d['shots'][0]['images'][0].update({'file': 'different-batch/c1.jpg'}))
    path = new / 'render-assets.json'
    receipts = json.loads(path.read_text(encoding='utf-8'))
    receipts['assets'][0]['publicFile'] = 'different-batch/c1.jpg'
    path.write_text(json.dumps(receipts), encoding='utf-8')
    assert r.repair_plan(old, new, ['c2'])['timingUnchanged']
    receipts['assets'][0]['publicSHA256'] = 'c' * 64
    path.write_text(json.dumps(receipts), encoding='utf-8')
    with pytest.raises(ValueError, match='Unselected shot appearance'):
        r.repair_plan(old, new, ['c2'])


def test_image_fit_focus_and_video_trim_are_rendered_appearance(films):
    old, new = films
    for field, value in [('fit', 'contain'), ('focus', [75, 50]), ('trimBeforeFrames', 9)]:
        original = json.loads((new / 'data.json').read_text(encoding='utf-8'))
        mutate(new, lambda d: d['shots'][0]['images'][0].update({field: value}))
        with pytest.raises(ValueError, match='Unselected shot appearance'):
            r.repair_plan(old, new, ['c2'])
        (new / 'data.json').write_text(json.dumps(original), encoding='utf-8')


@pytest.mark.parametrize('motion', [
    {'kind': 'basket', 'revealFrames': [0, 8, 16]},
    {'kind': 'price', 'stage': 'total'},
    {'kind': 'journey'},
])
def test_unselected_object_motion_cannot_change_silently(films, motion):
    old, new = films
    for folder in [old, new]:
        mutate(folder, lambda d: d['shots'][0].update({'layout': 'object3d', 'motion': {'kind': 'price', 'stage': 'unit'}}))
    mutate(new, lambda d: d['shots'][0].update({'motion': motion}))
    with pytest.raises(ValueError, match='Unselected shot appearance'):
        r.repair_plan(old, new, ['c2'])
    assert r.repair_plan(old, new, ['c1'])['changedShots'] == ['c1']


def test_original_files_are_not_modified_and_self_repair_is_rejected(films):
    old, new = films
    before = {p.relative_to(old).as_posix(): r.sha(p) for p in old.rglob('*') if p.is_file()}
    r.repair_plan(old, new, ['c2'])
    after = {p.relative_to(old).as_posix(): r.sha(p) for p in old.rglob('*') if p.is_file()}
    assert after == before
    with pytest.raises(ValueError, match='separate new batch'):
        r.repair_plan(old, old, ['c2'])


def test_repair_refuses_an_existing_destination_final_before_writing(films, monkeypatch):
    old, new = films
    manifest = new.parent / 'manifest.json'
    manifest.write_text(json.dumps({'direction': 'long'}), encoding='utf-8')
    monkeypatch.setattr(r.production, 'validate_structure', lambda value: None)
    sentinel = new / 'final.mp4'
    sentinel.write_bytes(b'retain this output')
    with pytest.raises(ValueError, match='already has a final'):
        r.repair(old, manifest, new.parent, ['c2'])
    assert sentinel.read_bytes() == b'retain this output'


@pytest.mark.parametrize('wrong', ['replaced-final', 'short-qa'])
def test_actual_repair_rejects_old_final_or_frame_qa_mismatch_before_copying(films, monkeypatch, wrong):
    old, new = films
    manifest = new.parent / 'manifest.json'
    manifest.write_text(json.dumps({'direction': 'long'}), encoding='utf-8')
    monkeypatch.setattr(r.production, 'validate_structure', lambda value: None)
    qa = {'frameCountPass': True, 'videoSHA256': r.sha(old / 'final.mp4'),
          'decodedFrames': 120, 'expectedFrames': 120}
    if wrong == 'replaced-final':
        (old / 'final.mp4').write_bytes(b'replaced after QA')
    else:
        qa['decodedFrames'] = 119
    (old / 'qa').mkdir()
    (old / 'qa/report.json').write_text(json.dumps(qa), encoding='utf-8')
    copied = []
    monkeypatch.setattr(r, 'retain_exact_audio', lambda *args: copied.append('should not reach mutation'))
    before = {p.relative_to(new).as_posix(): r.sha(p) for p in new.rglob('*') if p.is_file()}
    with pytest.raises(ValueError, match='QA|frame'):
        r.repair(old, manifest, new.parent, ['c2'])
    assert copied == []
    assert before == {p.relative_to(new).as_posix(): r.sha(p) for p in new.rglob('*') if p.is_file()}


def test_tiny_real_splice_uses_correct_frame_boundaries_and_keeps_audio_input(tmp_path):
    import cv2

    old, patch, mix, out = [tmp_path / name for name in ['old.mp4', 'patch.mp4', 'mix.wav', 'joined.mp4']]

    def encode(path, frames):
        pixels = np.concatenate([np.full((54, 96, 3), colour, dtype=np.uint8) for colour in frames], axis=0)
        subprocess.run([r.FF, '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
            '-s', '96x54', '-r', '30', '-i', 'pipe:0', '-frames:v', str(len(frames)),
            '-c:v', 'libx264', '-crf', '12', '-pix_fmt', 'yuv420p', str(path)], input=pixels.tobytes(), check=True, capture_output=True)

    encode(old, [(230, 10, 10)] * 6 + [(10, 10, 230)] * 6)
    encode(patch, [(10, 230, 10)] * 4)
    samples = (np.sin(np.arange(19200) * 2 * np.pi * 440 / 48000) * 5000).astype('<i2')
    with wave.open(str(mix), 'wb') as sound:
        sound.setnchannels(1)
        sound.setsampwidth(2)
        sound.setframerate(48000)
        sound.writeframes(samples.tobytes())
    plan = {'fps': 30, 'frames': 12, 'segments': r.segments_for([[4, 8]], 12)}
    before = r.sha(old), r.sha(mix)
    command = r.splice_command(old, [patch], mix, plan, out)
    subprocess.run(command, check=True, capture_output=True)
    assert before == (r.sha(old), r.sha(mix))
    assert r.check_decoded(out, 12, 30)['decodedFrames'] == 12
    cap = cv2.VideoCapture(str(out))
    colours = []
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        colours.append(np.mean(frame, axis=(0, 1)))  # OpenCV BGR.
    cap.release()
    assert all(np.argmax(c) == 2 for c in colours[:4])
    assert all(np.argmax(c) == 1 for c in colours[4:8])
    assert all(np.argmax(c) == 0 for c in colours[8:])
    audio = subprocess.run([r.FF, '-v', 'error', '-i', str(out), '-map', '0:a:0',
        '-f', 's16le', '-ar', '48000', '-ac', '1', 'pipe:1'], check=True, capture_output=True).stdout
    decoded = np.frombuffer(audio, dtype='<i2').astype(float)
    assert len(decoded) >= len(samples) - 1024
    assert np.max(np.abs(decoded)) > 1000
    assert np.corrcoef(samples.astype(float), decoded[:len(samples)])[0, 1] > .98
