"""Bounded evidence plans, visible-text gates and local review source navigation."""
from functools import partial
from http.server import ThreadingHTTPServer
import json
from pathlib import Path
import sys
from threading import Thread
from urllib.request import Request, urlopen

import pytest

sys.path.insert(0, str(Path(__file__).parent))
import business_qa as q
import business_review as r


def data():
    shots = [{'id': name, 'start': i * 90, 'end': (i + 1) * 90,
              'phase': phase, 'layout': layout, 'headline': name,
              'images': [{'file': 'C:/Users/Tyranno/fixture.jpg', 'credit': 'Creator'}]}
             for i, (name, phase, layout) in enumerate([
                 ('h01', 'hook', 'b-photo'), ('d01', 'disclaimer', 'b-question'),
                 ('c01', 'content', 'b-chart'), ('a01', 'cta', 'b-coffee')])]
    return {'fps': 30, 'frames': 360, 'title': 'An original business question',
            'audio': 'C:/Users/Tyranno/audio.wav', 'shots': shots,
            'captions': [{'start': 0, 'end': 2, 'text': 'An original narration clause.'}]}


def test_branding_gate_ignores_paths_but_checks_nested_visible_values():
    value = data()
    assert q.static_gates(value)['brandingPass']
    value['shots'][2]['design'] = {'paper': {'rows': [{'label': 'Tyranno', 'value': '35'}]}}
    with pytest.raises(ValueError, match='Forbidden'):
        q.static_gates(value)


def test_script_brand_and_overwide_caption_are_rejected():
    with pytest.raises(ValueError, match='Forbidden'):
        q.static_gates(data(), 'A spoken Tyranno label')
    value = data()
    value['captions'][0]['text'] = 'W' * 100
    with pytest.raises(ValueError, match='1580'):
        q.static_gates(value)


def test_capture_plan_has_every_midpoint_three_second_grid_and_five_motion_samples():
    plan = q.capture_plan(data())
    assert len(plan['midframes']) == 4
    assert [row['frame'] for row in plan['thumbnails']] == [0, 90, 180, 270]
    assert len(plan['temporal']) == 2
    assert all(len(shot['samples']) == 5 for shot in plan['temporal'])
    assert plan['lastFrame']['frame'] == 359
    assert all(0 <= sample['frame'] < 360 for shot in plan['temporal'] for sample in shot['samples'])


def test_revision_paths_keep_default_and_named_subfolder_inside_root(tmp_path):
    assert q.revision_folder(tmp_path) == tmp_path.resolve()
    assert q.revision_folder(tmp_path, 'r02') == (tmp_path / 'r02').resolve()
    for invalid in ['..', '../other', 'nested/r02', str(tmp_path.resolve())]:
        with pytest.raises(ValueError, match='Revision'):
            q.revision_folder(tmp_path, invalid)


def test_insufficient_explicit_cues_are_reported_without_inventing_alignment():
    value = data()
    value['shots'][2].update({'layout': 'b-split', 'design': {
        'choices': [{'title': 'A'}, {'title': 'B'}, {'title': 'C'}], 'cues': [20, 55]}})
    result = q.static_gates(value)
    assert result['visualCueWarnings'][0]['visibleElements'] == 3
    assert result['visualCueWarnings'][0]['explicitCues'] == 2
    assert result['shotTimelinePass'] is True


def test_review_escapes_sources_exposes_real_links_and_omits_private_brand_metadata(tmp_path):
    value = data()
    content = {'chapters': [{'id': 'one', 'title': 'One chapter', 'beats': [
        {'id': shot['id'], 'text': 'The authored clause.'} for shot in value['shots']]}]}
    sources = [{'sourceSHA256': 'x', 'source': {'id': 'photo', 'creator': '<script>attack</script> Creator',
        'page': 'https://example.com/author-photo', 'license': 'CC BY4.0',
        'licenseURL': 'https://creativecommons.org/licenses/by/4.0/',
        'capturedDate': '2024-01-02', 'location': {'place': 'Vietnam'},
        'inspection': {'doesNotEstablish': 'Does not establish profit.'},
        'visibleBranding': 'No Tyranno branding observed',
        'privatePath': 'C:/Users/Tyranno/sources'}}]
    for filename, payload in [('data.json', value), ('content.json', content),
        ('chapter-timing.json', [{'id': 'one', 'title': 'One chapter', 'startSeconds': 0}]),
        ('source-receipts.json', sources)]:
        (tmp_path / filename).write_text(json.dumps(payload), encoding='utf-8')
    result = r.build(tmp_path)
    page = (tmp_path / 'index.html').read_text(encoding='utf-8')
    assert result['clauses'] == 4 and result['visibleBrandingPass']
    assert 'href="https://example.com/author-photo"' in page
    assert 'href="https://creativecommons.org/licenses/by/4.0/"' in page
    assert '2024-01-02' in page and 'Vietnam' in page and 'Does not establish profit.' in page
    assert '<script>attack</script>' not in page
    assert 'Tyranno' not in page
    assert 'data-time="6.000000"' in page


def test_review_server_supports_video_byte_ranges_and_hides_directory_listing(tmp_path):
    (tmp_path / 'final.mp4').write_bytes(b'0123456789abcdef')
    (tmp_path / 'index.html').write_text('A review', encoding='utf-8')
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(r.ReviewHandler, directory=tmp_path))
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        request = Request(f'http://127.0.0.1:{server.server_port}/final.mp4', headers={'Range': 'bytes=3-7'})
        with urlopen(request, timeout=3) as response:
            assert response.status == 206
            assert response.headers['Content-Range'] == 'bytes 3-7/16'
            assert response.read() == b'34567'
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=3)


def test_review_revision_uses_new_data_video_and_qa_with_root_sources(tmp_path):
    root_data = data()
    corrected = data()
    corrected['shots'][0]['headline'] = 'Corrected opening title'
    revision = tmp_path / 'r02'
    (revision / 'qa').mkdir(parents=True)
    (revision / 'qa/report.json').write_text('{}', encoding='utf-8')
    (revision / 'poster.jpg').write_bytes(b'poster path fixture')
    content = {'chapters': [{'id': 'one', 'title': 'One chapter', 'beats': [
        {'id': shot['id'], 'text': 'The authored clause.'} for shot in corrected['shots']]}]}
    for filename, payload in [('data.json', root_data), ('content.json', content),
        ('chapter-timing.json', [{'id': 'one', 'title': 'One chapter', 'startSeconds': 0}]),
        ('source-receipts.json', [])]:
        (tmp_path / filename).write_text(json.dumps(payload), encoding='utf-8')
    (revision / 'data.json').write_text(json.dumps(corrected), encoding='utf-8')
    result = r.build(tmp_path, revision='r02')
    page = (tmp_path / 'index.html').read_text(encoding='utf-8')
    assert result['video'] == 'r02/final.mp4'
    assert '<source src="r02/final.mp4"' in page
    assert 'href="r02/qa/report.json"' in page
    assert 'poster="r02/poster.jpg"' in page
    assert 'Corrected opening title' in page
    assert 'href="script.txt"' in page


def test_tiny_real_final_decode_generates_native_frames_sheets_and_audio_measurement(tmp_path):
    value = data()
    value['frames'] = 48
    value['captions'][0]['end'] = 1.5
    for index, shot in enumerate(value['shots']):
        shot.update({'start': index * 12, 'end': (index + 1) * 12})
    (tmp_path / 'data.json').write_text(json.dumps(value), encoding='utf-8')
    (tmp_path / 'script.txt').write_text('An original educational narration.', encoding='utf-8')
    q.command([q.FF, '-y', '-v', 'error', '-f', 'lavfi', '-i', 'color=c=0x294337:s=1920x1080:r=30',
               '-f', 'lavfi', '-i', 'sine=frequency=440:sample_rate=48000:duration=1.6',
               '-frames:v', '48', '-t', '1.6', '-c:v', 'libx264', '-preset', 'ultrafast',
               '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-ar', '48000', str(tmp_path / 'final.mp4')])
    report = q.inspect(tmp_path)
    assert report['decodedFrames'] == 48 and report['frameCountPass']
    assert report['dimensionsPass'] and report['fpsPass'] and report['captureComplete']
    assert report['technicalIntegrity'] == 'passed'
    assert report['evidence']['midframes'] == 4
    assert report['evidence']['temporalShots'] == 2
    assert (tmp_path / 'qa/keyframes-01.jpg').is_file()
    assert (tmp_path / 'qa/tail.mp4').is_file()
    assert (tmp_path / 'poster.jpg').is_file()
    from PIL import Image
    with Image.open(tmp_path / 'qa/last-frame.jpg') as still:
        assert still.size == (1920, 1080)
    assert report['manualAudioListening'] == 'Not performed by this script'
