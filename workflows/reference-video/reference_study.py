"""Download playable references and make a continuous, auditable study index.

Contact sheets are sampled visual evidence, not a claim of continuous AV viewing.
Raw YouTube captions stay intact; their timing is ASR timing, not forced alignment.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import math
from pathlib import Path
import subprocess

import cv2
import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw
import requests
import yt_dlp


IDS = ['w3z43Hlzq3c', '1OGwWLvasIk', 'gNznfzAUiLw', '3JUxxp2sIDM']


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')


class Quiet:
    def debug(self, msg): pass
    def warning(self, msg): pass
    def error(self, msg): pass


def captions(folder):
    raw_path = folder / 'captions.json3'
    lang = 'vi'
    if not raw_path.exists():
        with yt_dlp.YoutubeDL({'quiet': True, 'logger': Quiet(), 'skip_download': True,
                               'socket_timeout': 30, 'retries': 2}) as ydl:
            info = ydl.extract_info(f'https://www.youtube.com/watch?v={folder.name}', download=False)
        tracks = info.get('subtitles') or info.get('automatic_captions') or {}
        lang = next((key for key in ['vi-orig', 'vi', 'en-orig', 'en'] if key in tracks), None)
        if not lang:
            raise RuntimeError('No usable caption track')
        track = next(t for t in tracks[lang] if t['ext'] == 'json3')
        response = requests.get(track['url'], timeout=60)
        response.raise_for_status()
        response.json()
        raw_path.write_bytes(response.content)
    raw = json.loads(raw_path.read_text(encoding='utf-8'))
    rows, words = [], []
    for event in raw.get('events', []):
        text = ''.join(s.get('utf8', '') for s in event.get('segs', [])).strip()
        if not text:
            continue
        start = event.get('tStartMs', 0) / 1000
        rows.append({'start': start, 'duration': event.get('dDurationMs', 0) / 1000, 'text': text})
        for seg in event.get('segs', []):
            if seg.get('utf8', '').strip():
                words.append({'start': round(start + seg.get('tOffsetMs', 0) / 1000, 3),
                              'text': seg['utf8']})
    save(folder / 'transcript.json', rows)
    save(folder / 'caption-word-offsets.json', words)
    (folder / 'transcript.txt').write_text('\n'.join(f"[{r['start']:07.2f}] {r['text']}" for r in rows), encoding='utf-8')
    save(folder / 'caption-receipt.json', {'source': 'YouTube JSON3 captions', 'language': lang,
        'rows': len(rows), 'sha256': hashlib.sha256(raw_path.read_bytes()).hexdigest(),
        'limitation': 'Automatic captions can contain recognition errors and overlapping display durations. Word offsets are supplied ASR offsets, not independently measured exact speech boundaries.'})
    print(json.dumps({'captions_ready': folder.name, 'rows': len(rows)}), flush=True)


def download(folder):
    target = folder / 'reference.mp4'
    if not target.exists():
        # 360p AVC + original low-bandwidth AAC keeps all references playable locally.
        opts = {'quiet': True, 'noprogress': True, 'logger': Quiet(), 'socket_timeout': 35,
                'retries': 3, 'fragment_retries': 3, 'concurrent_fragment_downloads': 1,
                'ffmpeg_location': imageio_ffmpeg.get_ffmpeg_exe(), 'format': '134+139',
                'merge_output_format': 'mp4', 'outtmpl': str(target)}
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([f'https://www.youtube.com/watch?v={folder.name}'])
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    probe = subprocess.run([ff, '-hide_banner', '-i', str(target)], capture_output=True, text=True)
    streams = [s.strip() for s in probe.stderr.splitlines() if 'Stream #' in s]
    if not any('Video:' in s for s in streams) or not any('Audio:' in s for s in streams):
        raise RuntimeError('Playable reference must contain both video and audio')
    check = subprocess.run([ff, '-v', 'error', '-i', str(target), '-map', '0:v:0',
                            '-map', '0:a:0', '-f', 'null', '-'], capture_output=True, text=True)
    if check.returncode or check.stderr.strip():
        raise RuntimeError('Full decode reported errors: ' + check.stderr[-500:])
    save(folder / 'media-receipt.json', {'url': f'https://www.youtube.com/watch?v={folder.name}',
        'file': target.name, 'bytes': target.stat().st_size,
        'sha256': hashlib.sha256(target.read_bytes()).hexdigest(), 'streams': streams,
        'full_av_decode': 'passed', 'purpose': 'Private reference analysis; not licensed for reuse in outputs'})
    print(json.dumps({'media_ready': folder.name, 'bytes': target.stat().st_size}), flush=True)


def stamp(seconds):
    return f'{int(seconds)//60:02}:{int(seconds)%60:02}.{int(seconds*10)%10}'


def study(folder):
    meta = json.loads((folder / 'metadata.json').read_text(encoding='utf-8'))
    rows = json.loads((folder / 'transcript.json').read_text(encoding='utf-8'))
    duration = meta['duration']
    evidence_dir = folder / 'sheets'
    evidence_dir.mkdir(exist_ok=True)
    blocks = []
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    proc = subprocess.Popen([ff, '-v', 'error', '-i', str(folder / 'reference.mp4'),
        '-t', str(duration), '-an', '-vf', 'fps=2,scale=480:270', '-f', 'rawvideo',
        '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    previous = None
    selected, previous_selected = [], -100
    current_block = 0
    all_samples = []

    def flush(number, samples):
        start, end = number * 60, min((number + 1) * 60, duration)
        sheet_files = []
        for page in range((len(samples) + 11) // 12):
            subset = samples[page * 12:(page + 1) * 12]
            sheet = Image.new('RGB', (1440, 4 * 294 + 30), '#17191e')
            draw = ImageDraw.Draw(sheet)
            draw.text((8, 7), f'{folder.name} | {stamp(start)} - {stamp(end)} | page {page+1}', fill='white')
            for n, sample in enumerate(subset):
                x, y = n % 3 * 480, n // 3 * 294 + 30
                draw.text((x + 6, y + 4), f'{stamp(sample[0])} | {sample[2]}', fill='white')
                sheet.paste(Image.fromarray(sample[1]), (x, y + 24))
            name = f'sheets/{number:02}-{page+1:02}.jpg'
            sheet.save(folder / name, quality=82, optimize=True)
            sheet_files.append(name)
        block_rows = [r for r in rows if start <= r['start'] < end]
        blocks.append({'index': number, 'start': start, 'end': end,
                       'transcript': block_rows, 'sheets': sheet_files,
                       'frames': [{'time': x[0], 'reason': x[2]} for x in samples]})

    i = 0
    while True:
        data = proc.stdout.read(480 * 270 * 3)
        if len(data) < 480 * 270 * 3:
            break
        t = i / 2
        block = int(t // 60)
        if block != current_block:
            flush(current_block, selected)
            selected = []
            current_block = block
        rgb = np.frombuffer(data, dtype=np.uint8).reshape(270, 480, 3)
        small = cv2.resize(rgb, (160, 90)).astype(np.float32)
        change = float(np.abs(small - previous).mean()) if previous is not None else 0
        cadence = i % 10 == 0
        # Approximate cut evidence: may include fast motion; not a semantic shot detector.
        cut = change >= 26 and t - previous_selected >= 1.5
        if cadence or cut:
            reason = '5s cadence' if cadence else f'change {change:.1f}'
            selected.append((t, rgb.copy(), reason))
            all_samples.append({'time': t, 'change': round(change, 2), 'reason': reason})
            previous_selected = t
        previous = small
        i += 1
    if selected:
        flush(current_block, selected)
    proc.stdout.close()
    error = proc.stderr.read().decode('utf-8', errors='replace')
    proc.wait()
    if proc.returncode:
        raise RuntimeError('Study-frame extraction failed: ' + error[-500:])
    if len(blocks) != math.ceil(duration / 60):
        raise RuntimeError('Study did not cover all consecutive minute blocks')
    save(folder / 'study-blocks.json', blocks)
    save(folder / 'sampling-receipt.json', {'duration': duration, 'sampled_at_fps': 2,
        'selected_frames': len(all_samples), 'blocks': len(blocks), 'samples': all_samples,
        'coverage': 'Every consecutive 60-second interval; 5-second cadence plus large frame-change candidates.',
        'limits': 'Sampled contact-sheet inspection does not establish continuous watching, auditory judgment, exact edit timing, or coverage of every sub-0.5-second shot. Cut detector may also flag motion.'})
    print(json.dumps({'study_ready': folder.name, 'blocks': len(blocks), 'frames': len(all_samples)}), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--phase', choices=['captions', 'media', 'study', 'all'], default='all')
    parser.add_argument('--ids', nargs='+', default=IDS)
    args = parser.parse_args()
    folders = [args.root / x for x in args.ids]
    if args.phase in ['captions', 'all']:
        with ThreadPoolExecutor(max_workers=3) as pool:
            list(pool.map(captions, folders))
    if args.phase in ['media', 'all']:
        for folder in folders:
            download(folder)
    if args.phase in ['study', 'all']:
        for folder in folders:
            study(folder)
