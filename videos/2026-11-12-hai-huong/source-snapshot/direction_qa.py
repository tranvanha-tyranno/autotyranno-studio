"""Inspect the actual two-direction MP4s and preserve visual/audio evidence.

Technical checks never assign aesthetic approval. All cuts use measured take timing.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re

import cv2
from PIL import Image, ImageDraw, ImageFont
from documentary import FF, run


def load(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def inspect(batch: Path):
    data = load(batch / 'data.json')
    out = batch / 'qa'
    out.mkdir(exist_ok=True)
    shots = data['shots']
    assert shots[0]['start'] == 0
    assert shots[-1]['end'] == data['frames']
    assert all(s['end'] > s['start'] for s in shots)
    assert all(a['end'] == b['start'] for a, b in zip(shots, shots[1:]))
    phases = list(dict.fromkeys(s['phase'] for s in shots))
    assert phases == ['hook', 'disclaimer', 'content', 'cta'], phases
    assert all(0 <= c['start'] < c['end'] <= data['frames'] / data['fps'] for c in data['captions'])
    public = Path(__file__).parent / 'cinematic/public'
    for shot in shots:
        for img in shot['images']:
            assert (public / img['file']).is_file(), img['file']

    # One image each second, plus every layout midpoint and a temporal strip
    # within each spatial shot. Decode sequentially so frame count is real.
    keyframes = sorted({min(s['end'] - 1, s['start'] + max(1, (s['end'] - s['start']) // 2)) for s in shots})
    spatial = [s for s in shots if s['layout'] == 'gallery3d']
    motion = sorted({s['start'] + round((s['end'] - s['start'] - 1) * p) for s in spatial for p in [.1, .3, .5, .7, .9]})
    seconds = list(range(round(data['fps'] / 2), data['frames'], data['fps']))
    targets = set(keyframes + motion + seconds + [data['frames'] - 1])
    captured = {}
    cap = cv2.VideoCapture(str(batch / 'final.mp4'))
    fps = cap.get(cv2.CAP_PROP_FPS)
    width, height = (int(cap.get(x)) for x in [cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT])
    count = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        if count in targets:
            still = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            if count not in keyframes and count != data['frames'] - 1:
                still.thumbnail((768, 432))
            captured[count] = still
        count += 1
    cap.release()
    font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 18)

    def sheet(keys, cols, size, filename):
        w, h = size
        canvas = Image.new('RGB', (cols * w, ((len(keys) + cols - 1) // cols) * (h + 28)), '#111820')
        draw = ImageDraw.Draw(canvas)
        for i, frame in enumerate(keys):
            if frame not in captured:
                continue
            x, y = i % cols * w, i // cols * (h + 28)
            canvas.paste(captured[frame].resize((w, h)), (x, y))
            draw.text((x + 8, y + h + 3), f'{frame / fps:.2f}s / {frame}', fill='white', font=font)
        canvas.save(out / filename, quality=93)

    for offset in range(0, len(seconds), 30):
        sheet(seconds[offset:offset + 30], 5, (384, 216), f'full-duration-{offset // 30 + 1:02}.jpg')
    for offset in range(0, len(keyframes), 9):
        sheet(keyframes[offset:offset + 9], 3, (640, 360), f'keyframes-{offset // 9 + 1:02}.jpg')
    if motion:
        sheet(motion, 5, (384, 216), 'spatial-motion.jpg')
    for frame in keyframes:
        captured[frame].save(out / f'frame-{frame:05}.jpg', quality=94)
    captured[data['frames'] - 1].save(out / 'last-frame.jpg', quality=94)
    captured[keyframes[0]].save(batch / 'poster.jpg', quality=95)

    result = run([FF, '-hide_banner', '-i', str(batch / 'final.mp4'), '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-'])
    log = result.stderr.decode('utf-8', errors='replace')
    (out / 'audio-measurement.log').write_text(log, encoding='utf-8')
    audio = json.loads(re.findall(r'\{\s*"input_i".*?\}', log, re.S)[-1])
    report = {
        'decodedFrames': count, 'expectedFrames': data['frames'], 'frameCountPass': count == data['frames'],
        'fps': fps, 'seconds': count / fps, 'width': width, 'height': height,
        'phases': phases, 'shots': len(shots),
        'uniqueImages': len({img['file'] for s in shots for img in s['images']}),
        'imageAppearances': sum(len(s['images']) for s in shots),
        'spatialImageSeconds': sum(s['end'] - s['start'] for s in spatial) / fps,
        'audioMeasuredOnFinalMP4': audio,
        'videoSHA256': hashlib.sha256((batch / 'final.mp4').read_bytes()).hexdigest(),
        'visualInspection': 'Evidence generated; write actual observations separately after viewing sheets.',
        'aestheticAcceptance': 'pending user feedback', 'manualAudioListening': 'not performed by this script',
    }
    (out / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False), flush=True)
    if count != data['frames']:
        raise ValueError('Decoded frame count differs from planned exact-take runtime')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--batch', type=Path, required=True)
    inspect(parser.parse_args().batch)
