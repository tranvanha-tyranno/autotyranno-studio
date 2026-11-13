"""China-specific evidence coverage, visible text and Range review navigation."""
from functools import partial
from http.server import ThreadingHTTPServer
import json
from pathlib import Path
import sys
from threading import Thread
from urllib.request import Request, urlopen

import pytest

sys.path.insert(0, str(Path(__file__).parent))
import china_qa as q
import china_review as r


def fixture_data():
    return {'fps': 30, 'frames': 360, 'title': 'Kinh tế Trung Quốc',
            'shots': [{'id': f'x{i}', 'phase': phase, 'layout': layout,
                       'start': i * 90, 'end': (i + 1) * 90,
                       'images': [], 'headline': f'Ý {i}',
                       'design': {'map': {'note': 'Nguồn địa lý'}}}
                      for i, (phase, layout) in enumerate([
                          ('hook', 'c-map'), ('disclaimer', 'c-flow'),
                          ('content', 'c-sim'), ('cta', 'c-chart')])],
            'captions': [{'start': 0, 'end': 2, 'text': 'Một câu tiếng Việt.'}]}


def test_temporal_plan_covers_every_china_motion_family_without_changing_business_plan():
    value = fixture_data()
    plan = q.capture_plan(value)
    assert len(plan['midframes']) == 4 and len(plan['temporal']) == 4
    assert {row['layout'] for row in plan['temporal']} == {'c-map', 'c-flow', 'c-sim', 'c-chart'}
    assert all(len(row['samples']) == 5 for row in plan['temporal'])
    assert [row['frame'] for row in plan['thumbnails']] == [0, 90, 180, 270]
    assert all(0 <= sample['frame'] < value['frames']
               for row in plan['temporal'] for sample in row['samples'])
    import business_qa
    assert not business_qa.capture_plan(value)['temporal']


def test_nested_map_labels_and_simulation_notes_cannot_hide_visible_branding():
    value = fixture_data()
    value['audio'] = 'C:/Users/Tyranno/private.wav'
    assert q.static_gates(value)['brandingPass']
    value['shots'][1]['design'] = {'flow': {'nodes': [{'label': 'Tyranno'}]}}
    with pytest.raises(ValueError, match='Forbidden'):
        q.static_gates(value)


def test_same_source_hash_cannot_be_repeated_under_another_public_file():
    value = fixture_data()
    value['shots'][0]['images'] = [{'file': 'china/a.jpg', 'sourceHash': 'same'}]
    value['shots'][2]['images'] = [{'file': 'china/b.jpg', 'sourceHash': 'same'}]
    with pytest.raises(ValueError, match='at most once'):
        q.static_gates(value)


def write_review_fixture(folder):
    data = fixture_data()
    payloads = {
        'data.json': data,
        'content.json': {'chapters': [{'title': 'Nhìn cơ chế', 'beats': [
            {'id': shot['id'], 'text': 'Lời dẫn gốc.'} for shot in data['shots']]}],
            'researchSources': [{'title': 'Cơ quan thống kê', 'url': 'https://example.com/nbs'}]},
        'chapter-timing.json': [{'title': 'Nhìn cơ chế', 'startSeconds': 0}],
        'source-receipts.json': [], 'benchmark.json': {'schema': 'video-benchmark/1'},
    }
    for name, value in payloads.items():
        (folder / name).write_text(json.dumps(value, ensure_ascii=False), encoding='utf-8')
    return data


def test_review_is_china_specific_and_exposes_research_and_cost_links(tmp_path):
    write_review_fixture(tmp_path)
    result = r.build(tmp_path)
    page = (tmp_path / 'index.html').read_text(encoding='utf-8')
    assert result['clauses'] == 4 and result['visibleBrandingPass']
    assert 'mô hình cà phê' not in page
    assert 'kinh tế Trung Quốc' in page
    assert 'href="https://example.com/nbs"' in page
    assert 'href="RESEARCH_AND_CREDITS.md"' in page
    assert 'href="publish-description.txt"' in page
    assert 'href="benchmark.json"' in page
    assert 'Thời gian và chi phí' in page


def test_local_review_preserves_mp4_range_requests(tmp_path):
    (tmp_path / 'final.mp4').write_bytes(b'0123456789abcdef')
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(r.ReviewHandler, directory=tmp_path))
    worker = Thread(target=server.serve_forever, daemon=True)
    worker.start()
    try:
        request = Request(f'http://127.0.0.1:{server.server_port}/final.mp4', headers={'Range': 'bytes=3-7'})
        with urlopen(request, timeout=3) as response:
            assert response.status == 206
            assert response.headers['Content-Range'] == 'bytes 3-7/16'
            assert response.read() == b'34567'
    finally:
        server.shutdown()
        server.server_close()
        worker.join(timeout=3)


def test_small_actual_decode_generates_china_temporal_evidence_and_loudness(tmp_path):
    value = fixture_data()
    value['frames'] = 48
    value['captions'][0]['end'] = 1.5
    for i, shot in enumerate(value['shots']):
        shot.update(start=i * 12, end=(i + 1) * 12)
    (tmp_path / 'data.json').write_text(json.dumps(value), encoding='utf-8')
    q.command([q.FF, '-y', '-v', 'error', '-f', 'lavfi', '-i', 'color=c=0x294337:s=1920x1080:r=30',
               '-f', 'lavfi', '-i', 'sine=frequency=440:sample_rate=48000:duration=1.6',
               '-frames:v', '48', '-t', '1.6', '-c:v', 'libx264', '-preset', 'ultrafast',
               '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-ar', '48000', str(tmp_path / 'final.mp4')])
    report = q.inspect(tmp_path)
    assert report['schema'] == 'china-video-qa/1'
    assert report['decodedFrames'] == 48 and report['technicalIntegrity'] == 'passed'
    assert report['evidence']['temporalShots'] == 4
    assert report['captureComplete'] and report['singleUseMediaPass']
    assert (tmp_path / 'qa/china_qa.py').is_file()
    assert (tmp_path / 'qa/temporal/x0-strip.jpg').is_file()
    assert report['manualAudioListening'] == 'Not performed by this script'
