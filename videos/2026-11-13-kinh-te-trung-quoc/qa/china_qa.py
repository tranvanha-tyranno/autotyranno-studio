"""Decode the complete China economy film and retain bounded visual/audio QA evidence.

This checks technical integrity and generates review material. It does not listen,
assign semantic/aesthetic acceptance or grant user approval.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import shutil
import subprocess

import cv2
from PIL import Image, ImageDraw, ImageFont

from documentary import FF

FONT = Path('C:/Windows/Fonts/arial.ttf')
FORBIDDEN = ('tyranno',)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def save(path, value):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')


def sha(path):
    result = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            result.update(chunk)
    return result.hexdigest()


def safe_name(value):
    return re.sub(r'[^a-zA-Z0-9_-]', '-', str(value))[:80] or 'shot'


def revision_folder(batch, revision=None):
    batch = Path(batch).resolve()
    if revision is None:
        return batch
    relative = Path(revision)
    require(not relative.is_absolute() and len(relative.parts) == 1 and relative.name not in ['.', '..'],
            'Revision must be a single batch subfolder name')
    folder = (batch / relative).resolve()
    require(folder.is_relative_to(batch) and folder != batch, 'Revision must remain inside the named batch')
    return folder


def visible_texts(data):
    """Only visible strings: never infer branding from filesystem usernames."""
    yield data.get('title', '')
    for caption in data.get('captions', []):
        yield caption.get('text', '')
    for shot in data.get('shots', []):
        for key in ['headline', 'eyebrow', 'body', 'sourceNote', 'text']:
            yield shot.get(key, '')
        for image in shot.get('images', []):
            yield image.get('credit', '')
        design = shot.get('design', {})
        # China layouts render labels/notes nested in maps, flows, simulations,
        # comparison tables and chart series. Paths and metadata are not visible.
        def design_texts(value, key=''):
            if isinstance(value, dict):
                for child_key, child in value.items():
                    if child_key not in ['id', 'from', 'to', 'kind', 'mode', 'theme', 'color']:
                        yield from design_texts(child, child_key)
            elif isinstance(value, list):
                for child in value:
                    yield from design_texts(child, key)
            elif isinstance(value, str):
                yield value
        yield from design_texts(design)
        yield from design.get('emphasis', [])
        paper = design.get('paper', {})
        yield paper.get('title', '')
        for row in paper.get('rows', []) + ([paper['total']] if paper.get('total') else []):
            yield row.get('label', '')
            yield row.get('value', '')
        for choice in design.get('choices', []):
            for key in ['label', 'title', 'body']:
                yield choice.get(key, '')
        chart = design.get('chart', {})
        for key in ['unit', 'xLabel']:
            yield chart.get(key, '')
        for item in chart.get('items', []):
            yield item.get('label', '')


def static_gates(data, script='', font_path=FONT):
    frames, fps, shots = data['frames'], data['fps'], data['shots']
    require(isinstance(frames, int) and frames > 0 and fps > 0, 'Invalid compiled video duration')
    require(shots and shots[0]['start'] == 0 and shots[-1]['end'] == frames,
            'Shots do not cover both ends of the exact narration')
    require(all(isinstance(s['start'], int) and isinstance(s['end'], int)
                and 0 <= s['start'] < s['end'] <= frames for s in shots), 'Shot frame bounds invalid')
    require(all(a['end'] == b['start'] for a, b in zip(shots, shots[1:])), 'Shots are not contiguous')
    phases = [shot['phase'] for i, shot in enumerate(shots) if not i or shot['phase'] != shots[i - 1]['phase']]
    require(phases == ['hook', 'disclaimer', 'content', 'cta'], 'Film must retain hook, disclaimer, main and CTA')
    media_keys = [image.get('sourceHash') or image['file']
                  for shot in shots for image in shot.get('images', [])]
    require(len(media_keys) == len(set(media_keys)), 'China context media must appear at most once per film')
    text = '\n'.join([str(value) for value in visible_texts(data)] + [script]).casefold()
    forbidden = [word for word in FORBIDDEN if word in text]
    require(not forbidden, 'Forbidden channel branding in visible text or spoken script')
    font = ImageFont.truetype(str(font_path), 34)
    caption_rows = []
    previous = 0.0
    for index, caption in enumerate(data.get('captions', [])):
        require(0 <= caption['start'] < caption['end'] <= frames / fps + .001,
                'Caption timing extends outside final narration')
        require(caption['start'] >= previous, 'Caption starts move backward')
        previous = caption['start']
        width = float(font.getlength(caption['text']))
        caption_rows.append({'index': index, 'text': caption['text'], 'widthPixels': round(width, 2)})
    widest = max(caption_rows, key=lambda row: row['widthPixels']) if caption_rows else None
    too_wide = [row for row in caption_rows if row['widthPixels'] > 1580]
    require(not too_wide, 'Caption text exceeds1580pixels in Arial34')
    cue_warnings = []
    for shot in shots:
        design, duration_frames = shot.get('design', {}), shot['end'] - shot['start']
        cues = design.get('cues', [])
        require(all(isinstance(cue, int) and not isinstance(cue, bool) and 0 <= cue < duration_frames
                    for cue in cues), 'Visual cue frame falls outside shot')
        expected = None
        if shot['layout'] == 'b-split':
            expected = len(design.get('choices', []))
        elif shot['layout'] == 'c-chart' and design.get('chart', {}).get('kind') in ['bars', 'waterfall']:
            expected = len(design['chart'].get('items', []))
        if cues and expected and len(cues) < expected:
            cue_warnings.append({'shot': shot.get('id'), 'layout': shot['layout'],
                'explicitCues': len(cues), 'visibleElements': expected,
                'risk': 'A later element falls back to a generic reveal frame and can appear before an earlier exact-take cue.'})
    return {'shotTimelinePass': True, 'phases': phases, 'shots': len(shots),
            'singleUseMediaPass': True, 'contextMediaAppearances': len(media_keys),
            'brandingPass': True, 'brandingScope': 'Visible render text and spoken script only; paths and usernames excluded.',
            'captionWidthPass': True, 'captionFont': 'Arial34', 'maximumCaptionTextWidth': 1580,
            'captions': len(caption_rows), 'widestCaption': widest,
            'visualCueWarnings': cue_warnings,
            'visualCueScope': 'Warnings need actual temporal review; equal cue count does not prove semantic alignment.'}


def capture_plan(data):
    """Frame indices only; actual image data is written immediately while decoding."""
    frames, fps = data['frames'], data['fps']
    mids, motion = [], []
    for index, shot in enumerate(data['shots']):
        name = safe_name(shot.get('id', f'shot-{index + 1:02}'))
        frame = min(shot['end'] - 1, (shot['start'] + shot['end']) // 2)
        mids.append({'shot': shot.get('id', name), 'frame': frame, 'seconds': frame / fps,
                     'file': f'midframes/{index + 1:02}-{name}.jpg', 'layout': shot['layout']})
        if shot['layout'] in ['c-map', 'c-flow', 'c-sim', 'c-chart', 'c-compare']:
            samples = [{'frame': shot['start'] + round((shot['end'] - shot['start'] - 1) * fraction),
                        'fraction': fraction, 'file': f'temporal/{name}-{j + 1}.jpg'}
                       for j, fraction in enumerate([.08, .29, .50, .71, .92])]
            motion.append({'shot': shot.get('id', name), 'layout': shot['layout'],
                           'samples': samples, 'strip': f'temporal/{name}-strip.jpg'})
    thumbnails = [{'frame': frame, 'seconds': frame / fps, 'file': f'thumbnails/{index + 1:03}.jpg'}
                  for index, frame in enumerate(range(0, frames, max(1, round(fps * 3))))]
    return {'midframes': mids, 'thumbnails': thumbnails, 'temporal': motion,
            'lastFrame': {'frame': frames - 1, 'file': 'last-frame.jpg'}}


def save_image(image, path, bounds=None, quality=92):
    path.parent.mkdir(parents=True, exist_ok=True)
    if bounds:
        image = image.copy()
        image.thumbnail(bounds, Image.Resampling.LANCZOS)
    image.save(path, quality=quality)


def sheet(rows, root, target, *, columns=3, tile=(640, 360)):
    w, h = tile
    pages = math.ceil(len(rows) / columns)
    canvas = Image.new('RGB', (columns * w, max(1, pages) * (h + 30)), '#16251f')
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.truetype(str(FONT), 18)
    for index, row in enumerate(rows):
        with Image.open(root / row['file']) as image:
            image = image.convert('RGB')
            image.thumbnail(tile, Image.Resampling.LANCZOS)
            x, y = index % columns * w, index // columns * (h + 30)
            canvas.paste(image, (x + (w - image.width) // 2, y + (h - image.height) // 2))
        label = f'{row.get("shot", "")}  {row.get("seconds", 0):.2f}s / f{row["frame"]}'.strip()
        draw.text((x + 9, y + h + 5), label, fill='#f6efdf', font=font)
    target.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(target, quality=92)


def command(arguments):
    result = subprocess.run(arguments, capture_output=True)
    if result.returncode:
        raise RuntimeError(result.stderr.decode('utf-8', errors='replace')[-2500:])
    return result


def inspect(batch, *, video=None, revision=None):
    source_batch = Path(batch).resolve()
    batch = revision_folder(source_batch, revision)
    video = Path(video).resolve() if video else batch / 'final.mp4'
    require(video.is_file(), 'Final MP4 does not exist yet; let the complete render finish')
    data_path = batch / 'data.json'
    data_sha = sha(data_path)
    data = load(data_path)
    script_path = batch / 'script.txt' if (batch / 'script.txt').is_file() else source_batch / 'script.txt'
    script = script_path.read_text(encoding='utf-8-sig') if script_path.is_file() else ''
    gates = static_gates(data, script)
    receipt_path = source_batch / 'source-receipts.json'
    if receipt_path.is_file():
        receipts = {row['publicFile']: row['publicSHA256'] for row in load(receipt_path)}
        referenced = {image['file'] for shot in data['shots'] for image in shot.get('images', [])}
        for key in referenced:
            path = (source_batch / 'production-public' / key).resolve()
            require(path.is_relative_to(source_batch / 'production-public') and path.is_file(),
                    'Referenced batch media missing or outside public folder: ' + key)
            require(key in receipts and sha(path) == receipts[key], 'Referenced public asset differs from source receipt: ' + key)
        gates['publicAssetIntegrity'] = {'checked': len(referenced), 'pass': True,
                                        'source': 'Root batch source-receipts.json and production-public/'}
    plan = capture_plan(data)
    out = batch / 'qa'
    out.mkdir(parents=True, exist_ok=True)
    save(out / 'capture-plan.json', plan)
    targets = {}
    for row in plan['midframes']:
        targets.setdefault(row['frame'], []).append((row['file'], None))
    for row in plan['thumbnails']:
        targets.setdefault(row['frame'], []).append((row['file'], (384, 216)))
    for shot in plan['temporal']:
        for row in shot['samples']:
            targets.setdefault(row['frame'], []).append((row['file'], (960, 540)))
    targets.setdefault(data['frames'] - 1, []).append(('last-frame.jpg', None))

    initial_video = video.stat()
    cap = cv2.VideoCapture(str(video))
    require(cap.isOpened(), 'Final MP4 cannot be opened for sequential decode')
    fps = cap.get(cv2.CAP_PROP_FPS)
    width, height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    count, captured, dimensions_stable = 0, set(), True
    try:
        while True:
            ok, pixels = cap.read()
            if not ok:
                break
            dimensions_stable = dimensions_stable and pixels.shape[:2] == (height, width)
            if count in targets:
                image = Image.fromarray(cv2.cvtColor(pixels, cv2.COLOR_BGR2RGB))
                for relative, bounds in targets[count]:
                    save_image(image, out / relative, bounds)
                captured.add(count)
            count += 1
    finally:
        cap.release()
    final_video = video.stat()
    require((initial_video.st_size, initial_video.st_mtime_ns) ==
            (final_video.st_size, final_video.st_mtime_ns), 'Final MP4 changed during sequential QA decode')
    require(sha(data_path) == data_sha, 'Compiled data changed while QA was decoding')
    count_pass = count == data['frames']
    fps_pass = math.isclose(fps, data['fps'], abs_tol=.001)
    dimensions_pass = (width, height) == (1920, 1080) and dimensions_stable
    report = {'schema': 'china-video-qa/1', **gates,
              'decodedFrames': count, 'expectedFrames': data['frames'], 'frameCountPass': count_pass,
              'fps': fps, 'expectedFPS': data['fps'], 'fpsPass': fps_pass,
              'width': width, 'height': height, 'dimensionsStable': dimensions_stable,
              'dimensionsPass': dimensions_pass, 'seconds': count / fps if fps else None,
              'dataSHA256': data_sha, 'videoSHA256': sha(video), 'qaSourceSHA256': sha(Path(__file__)),
              'revision': revision, 'sourceBatch': str(source_batch),
              'capturedFrameIndices': len(captured), 'targetFrameIndices': len(targets),
              'captureComplete': captured == set(targets),
              'evidence': {'midframes': len(plan['midframes']), 'thumbnailsEveryThreeSeconds': len(plan['thumbnails']),
                           'temporalShots': len(plan['temporal']), 'temporalSamplesPerShot': 5,
                           'temporalLayoutScope': ['c-map', 'c-flow', 'c-sim', 'c-chart', 'c-compare'],
                           'lastFrame': 'last-frame.jpg', 'capturePlan': 'capture-plan.json'},
              'memoryPolicy': 'One decoded frame plus one bounded contact sheet at a time; images retained on disk.',
              'manualAudioListening': 'Not performed by this script', 'visualInspection': 'Evidence generated; actual viewing must be recorded separately.',
              'aestheticAcceptance': 'pending user feedback', 'userAcceptance': 'pending'}
    save(out / 'report.json', report)
    require(count_pass and fps_pass and dimensions_pass and report['captureComplete'],
            'Final MP4 frame count, FPS, dimensions or evidence coverage differs from compiled plan')

    key_sheets, thumb_sheets = [], []
    for offset in range(0, len(plan['midframes']), 9):
        name = f'keyframes-{offset // 9 + 1:02}.jpg'
        sheet(plan['midframes'][offset:offset + 9], out, out / name)
        key_sheets.append(name)
    for offset in range(0, len(plan['thumbnails']), 9):
        name = f'three-second-{offset // 9 + 1:02}.jpg'
        sheet(plan['thumbnails'][offset:offset + 9], out, out / name, tile=(384, 216))
        thumb_sheets.append(name)
    for shot in plan['temporal']:
        rows = [{**row, 'shot': shot['shot'], 'seconds': row['frame'] / data['fps']} for row in shot['samples']]
        sheet(rows, out, out / shot['strip'], columns=5, tile=(384, 216))
    shutil.copy2(out / plan['midframes'][0]['file'], batch / 'poster.jpg')
    report['evidence'].update({'keyframeSheets': key_sheets, 'threeSecondSheets': thumb_sheets})

    measured = command([FF, '-hide_banner', '-i', str(video), '-vn', '-af',
                        'loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-'])
    log = measured.stderr.decode('utf-8', errors='replace')
    (out / 'audio-measurement.log').write_text(log, encoding='utf-8')
    matches = re.findall(r'\{\s*"input_i".*?\}', log, re.S)
    require(matches, 'Final MP4 has no loudness measurement')
    loudness = json.loads(matches[-1])
    report['audioMeasuredOnFinalMP4'] = loudness
    report['audioMeasurementPass'] = math.isfinite(float(loudness['input_i'])) and float(loudness['input_tp']) <= 0
    tail_seconds = min(6, data['frames'] / data['fps'])
    command([FF, '-y', '-v', 'error', '-sseof', f'-{tail_seconds:.6f}', '-i', str(video),
             '-t', f'{tail_seconds:.6f}', '-map', '0:v:0', '-map', '0:a:0',
             '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '21', '-c:a', 'aac', '-b:a', '192k',
             '-movflags', '+faststart', str(out / 'tail.mp4')])
    report['evidence']['tail'] = {'file': 'tail.mp4', 'seconds': tail_seconds,
                                'note': 'Review derivative of the final seconds; no listening is implied.'}
    report['technicalIntegrity'] = 'passed' if report['audioMeasurementPass'] else 'failed'
    save(out / 'report.json', report)
    shutil.copy2(Path(__file__), out / 'china_qa.py')
    require(report['audioMeasurementPass'], 'Final MP4 loudness is missing or true peak exceeds0dBTP')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--batch', type=Path, required=True)
    parser.add_argument('--revision', help='Optional prepared batch subfolder such as r02')
    args = parser.parse_args()
    print(json.dumps(inspect(args.batch, revision=args.revision), ensure_ascii=False, indent=2))
