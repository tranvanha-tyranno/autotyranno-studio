"""Measured, checkpointed ChinaPreview rendering and guarded fast chapter concat."""
from __future__ import annotations

import argparse
import ctypes
from datetime import datetime, timezone
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
import uuid

import cv2

import china
import render_directions
from documentary import FF

WORK = Path(__file__).resolve().parent
PROJECT = WORK / 'cinematic'
CLI = PROJECT / 'node_modules/@remotion/cli/remotion-cli.js'
ENTRY = PROJECT / 'src/china-entry.tsx'
save, load, sha, require = china.save, china.load, china.sha, china.require
CACHE_BYTES = 268435456


def utc():
    return datetime.now(timezone.utc).isoformat()


def decoded(path, expected):
    start = time.monotonic()
    cap = cv2.VideoCapture(str(path))
    require(cap.isOpened(), 'Undecodable video: ' + str(path))
    count = 0
    while cap.grab():
        count += 1
    fps = cap.get(cv2.CAP_PROP_FPS)
    width, height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()
    require(count == expected and abs(fps - 30) < .001 and (width, height) == (1920, 1080),
            'Decoded frame count/FPS/dimensions differ: ' + str(path))
    elapsed = time.monotonic() - start
    return {'sha256': sha(path), 'frames': count, 'fps': fps, 'width': width, 'height': height,
            'decodeWallSeconds': round(elapsed, 3), 'decodeFramesPerSecond': round(count / max(.001, elapsed), 3)}


def run(command, log):
    started, clock = utc(), time.monotonic()
    with Path(log).open('x', encoding='utf-8') as output:
        output.write(json.dumps({'argv': list(map(str, command)), 'startedUTC': started}, ensure_ascii=False) + '\n')
        output.flush()
        process = subprocess.Popen(list(map(str, command)), cwd=PROJECT, stdout=output, stderr=subprocess.STDOUT)
        returncode = process.wait()
        cpu_seconds = None
        if sys.platform == 'win32':
            class FileTime(ctypes.Structure):
                _fields_ = [('low', ctypes.c_ulong), ('high', ctypes.c_ulong)]
            created, exited, kernel, user = FileTime(), FileTime(), FileTime(), FileTime()
            if ctypes.windll.kernel32.GetProcessTimes(ctypes.c_void_p(int(process._handle)), ctypes.byref(created),
                    ctypes.byref(exited), ctypes.byref(kernel), ctypes.byref(user)):
                cpu_seconds = ((kernel.high << 32) + kernel.low + (user.high << 32) + user.low) / 10_000_000
    receipt = {'startedUTC': started, 'finishedUTC': utc(), 'wallSeconds': round(time.monotonic() - clock, 3),
               'returncode': returncode, 'log': str(log), 'directProcessCPUSeconds': cpu_seconds,
               'cpuScope': 'Measured direct Node/FFmpeg process CPU on Windows only; browser/encoder descendants are not included. Null if unavailable.'}
    require(returncode == 0, 'Render step failed; retained log: ' + str(log))
    return receipt


def probe_video(path):
    """Read codec metadata without ffprobe or decoding a whole chapter."""
    result = subprocess.run([FF, '-hide_banner', '-i', str(path), '-map', '0:v:0', '-frames:v', '0',
                             '-f', 'null', '-'], capture_output=True)
    require(result.returncode == 0, 'Cannot inspect video parameters: ' + str(path))
    text = result.stderr.decode('utf-8', errors='replace')
    line = next((line.strip() for line in text.splitlines() if 'Video:' in line and 'Stream #0:' in line), '')
    codec = re.search(r'Video:\s*(\w+)\s*(?:\(([^)]+)\))?', line)
    size = re.search(r'\b(\d{2,5})x(\d{2,5})\b', line)
    fps = re.search(r'([\d.]+) fps', line)
    sar = re.search(r'SAR (\d+):(\d+)', line)
    pixel = re.search(r'\b(yuv\w+|nv12|rgb\w+)\b', line)
    require(codec and size and fps and pixel, 'Incomplete codec metadata: ' + str(path))
    colors = re.search(r'\b(tv|pc),\s*([^)]*)\)', line)
    return {'codec': codec[1], 'profile': codec[2], 'width': int(size[1]), 'height': int(size[2]),
            'fps': float(fps[1]), 'pixelFormat': pixel[1],
            'sar': f'{sar[1]}:{sar[2]}' if sar else None,
            'color': colors.group(0) if colors else ('bt709' if 'bt709' in line else None),
            'rawVideoLine': line}


def copy_compatible(parameters):
    keys = ['codec', 'profile', 'width', 'height', 'fps', 'pixelFormat', 'sar', 'color']
    return bool(parameters and all(p['codec'] == 'h264' and (p['width'], p['height']) == (1920, 1080)
                and math.isclose(p['fps'], 30, abs_tol=.001) and p['pixelFormat'] == 'yuv420p'
                and p['sar'] == '1:1' and p['color'] and 'bt709' in p['color'] for p in parameters)
                and all(all(p[key] == parameters[0][key] for key in keys) for p in parameters))


def normalize_packet_command(source, target):
    return [FF, '-y', '-v', 'error', '-i', source, '-map', '0:v:0', '-an', '-c:v', 'copy',
            '-bsf:v', 'h264_metadata=sample_aspect_ratio=1/1:video_full_range_flag=0:colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1',
            '-video_track_timescale', '90000', '-color_primaries', 'bt709', '-color_trc', 'bt709',
            '-colorspace', 'bt709', '-color_range', 'tv', '-movflags', '+faststart', target]


def concat_command(listing, mix, frames, output, *, stream_copy):
    command = [FF, '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', listing, '-i', mix,
               '-map', '0:v:0', '-map', '1:a:0']
    if stream_copy:
        command += ['-c:v', 'copy']
    else:
        command += ['-vf', 'setsar=1,scale=1920:1080:in_range=auto:out_range=tv:out_color_matrix=bt709,format=yuv420p',
                    '-c:v', 'libx264', '-preset', 'fast', '-crf', '18', '-r', '30']
    return command + ['-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709',
        '-color_range', 'tv', '-video_track_timescale', '90000', '-frames:v', str(frames),
        '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-ac', '2', '-t', f'{frames/30:.9f}',
        '-movflags', '+faststart', output]


def audio_decoded(path, seconds, last_word):
    started = time.monotonic()
    process = subprocess.Popen([FF, '-v', 'error', '-i', str(path), '-map', '0:a:0', '-ar', '48000', '-ac', '1',
                                '-f', 's16le', '-'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    count = 0
    while block := process.stdout.read(1024 * 1024):
        count += len(block)
    error = process.stderr.read()
    require(process.wait() == 0, 'Final AAC cannot decode: ' + error.decode('utf-8', errors='replace')[-500:])
    actual = count / (48000 * 2)
    require(actual >= last_word and abs(actual - seconds) <= .12, 'Final audio duration truncates exact narration or differs from timeline')
    return {'decodedSamplesMono48000': count // 2, 'seconds': actual, 'lastWordEnd': last_word,
            'wallSeconds': round(time.monotonic() - started, 3), 'manualListening': False}


def tree(root):
    return [{'file': p.relative_to(root).as_posix(), 'sha256': sha(p)} for p in sorted(root.rglob('*')) if p.is_file()]


def snapshot(batch, destination):
    destination.mkdir()
    files = [batch / name for name in ['content.json', 'data.json', 'props.json', 'visual-plan.json',
        'source-receipts.json', 'preflight.json', 'chapter-timing.json', 'audio/mix-report.json',
        'audio/narration.receipt.json', 'audio/cue-plan.json', 'audio/mix-dependencies.json']]
    code = [WORK / name for name in ['china.py', 'china_audio.py', 'china_render.py', 'eleven_audio.py',
        'cinematic/src/china-entry.tsx', 'cinematic/package.json', 'cinematic/package-lock.json', 'cinematic/remotion.config.ts']]
    code += list((PROJECT / 'src/china').rglob('*'))
    records = []
    for source, prefix, base in [(p, 'batch', batch) for p in files] + [(p, 'workflow', WORK) for p in code]:
        if not source.is_file():
            continue
        target = destination / prefix / source.relative_to(base)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        records.append({'file': target.relative_to(destination).as_posix(), 'sha256': sha(target)})
    save(destination / 'hashes.json', records)


def render(batch, resume=None, concurrency=None):
    batch = Path(batch).resolve()
    require(not (batch / 'final.mp4').exists(), 'Final exists; use a new revision or run QA separately')
    data = load(batch / 'data.json')
    china.validate(load(batch / 'content.json'))
    china.validate_media_intervals(data)
    require(data['fps'] == 30 and data['frames'] > 0, 'Invalid China timeline')
    mix = batch / 'audio/final-mix.wav'
    report = load(batch / 'audio/mix-report.json')
    require(sha(mix) == report['mix']['sha256'] == sha(batch / 'production-public/china/mix.wav'), 'Pinned/public mix differs')
    for row in load(batch / 'source-receipts.json'):
        source = batch / 'production-public' / row['publicFile']
        require(source.is_file() and sha(source) == row['publicSHA256'], 'Prepared public visual source changed')
    require(shutil.disk_usage(batch).free > 2_000_000_000, 'Less than2GB storage; preserve artifacts and restore capacity first')
    attempt = Path(resume).resolve() if resume else batch / 'render-attempts' / (datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '-' + uuid.uuid4().hex[:6])
    require(attempt.parent == batch / 'render-attempts', 'Resume attempt must belong to this batch')
    options = concurrency or (load(attempt / 'state.json')['concurrency'] if resume else 2)
    require(options in [1, 2, 4], 'Concurrency must be1,2or4')
    with render_directions.project_lock(attempt.name):
        started = time.monotonic()
        if not resume:
            attempt.mkdir(parents=True)
            snapshot(batch, attempt / 'source-snapshot')
            groups = []
            for shot in data['shots']:
                if not groups or groups[-1]['id'] != shot['chapter']:
                    groups.append({'id': shot['chapter'], 'start': shot['start'], 'end': shot['end']})
                else:
                    groups[-1]['end'] = shot['end']
            require(groups[0]['start'] == 0 and groups[-1]['end'] == data['frames']
                    and all(a['end'] == b['start'] for a, b in zip(groups, groups[1:])), 'Chapter groups do not exactly partition timeline')
            state = {'schema': 'china-render-attempt/1', 'status': 'preparing', 'startedUTC': utc(), 'frames': data['frames'],
                'dataSHA256': sha(batch / 'data.json'), 'propsSHA256': sha(batch / 'props.json'), 'mixSHA256': sha(mix),
                'parts': groups, 'concurrency': options, 'mediaCacheBytes': CACHE_BYTES, 'memoryAtStart': render_directions.memory_snapshot(),
                'diskAtStart': shutil.disk_usage(batch)._asdict(), 'userAcceptance': 'pending'}
            save(attempt / 'state.json', state)
            state['bundleTiming'] = run(['node', CLI, 'bundle', ENTRY, f'--out-dir={attempt/"bundle"}',
                f'--public-dir={batch/"production-public"}', '--log=error'], attempt / 'bundle.log')
            state['bundleFiles'] = tree(attempt / 'bundle')
            save(attempt / 'state.json', state)
        state = load(attempt / 'state.json')
        require(state['concurrency'] == options and state['mediaCacheBytes'] == CACHE_BYTES, 'Frozen render options changed')
        require(state['dataSHA256'] == sha(batch / 'data.json') and state['propsSHA256'] == sha(batch / 'props.json')
                and state['mixSHA256'] == sha(mix), 'Frozen render inputs changed; use a new attempt/revision')
        require(state['bundleFiles'] == tree(attempt / 'bundle'), 'Frozen bundle bytes changed')
        for row in load(attempt / 'source-snapshot/hashes.json'):
            require(sha(attempt / 'source-snapshot' / row['file']) == row['sha256'], 'Frozen source snapshot changed')
        state['status'] = 'running'
        session = uuid.uuid4().hex[:8]
        save(attempt / 'state.json', state)
        try:
            parts = []
            for index, part in enumerate(state['parts']):
                target = attempt / f'part-{index:02}.mp4'
                frames = part['end'] - part['start']
                if part.get('complete'):
                    require(target.is_file() and sha(target) == part['receipt']['sha256'], 'Completed chapter changed')
                    decoded(target, frames)
                    parts.append(target)
                    print('REUSE', part['id'], frames, flush=True)
                    continue
                if target.exists():
                    target.rename(target.with_name(target.stem + '-failed-' + uuid.uuid4().hex[:6] + target.suffix))
                require(shutil.disk_usage(batch).free > 1_500_000_000, 'Storage below1.5GB; explicit resume after restoring capacity')
                print('RENDER', part['id'], frames, 'frames', flush=True)
                timing = run(['node', CLI, 'render', attempt / 'bundle', 'ChinaPreview', target,
                    f'--props={batch/"props.json"}', f'--frames={part["start"]}-{part["end"]-1}', '--muted', '--codec=h264',
                    '--crf=18', '--color-space=bt709', '--pixel-format=yuv420p', f'--concurrency={options}',
                    f'--media-cache-size-in-bytes={CACHE_BYTES}', '--log=info'], attempt / f'part-{index:02}-{session}.log')
                part['receipt'] = decoded(target, frames)
                part['renderTiming'] = {**timing, 'frames': frames, 'renderFramesPerSecond': round(frames / max(.001, timing['wallSeconds']), 3),
                                         'videoSecondsPerWallSecond': round((frames / 30) / max(.001, timing['wallSeconds']), 4)}
                part['complete'] = True
                save(attempt / 'state.json', state)
                parts.append(target)
            parameters = [probe_video(path) for path in parts]
            state['originalPartParameters'] = parameters
            safe_shape = all(p['codec'] == 'h264' and (p['width'], p['height']) == (1920, 1080)
                             and abs(p['fps'] - 30) < .001 and p['pixelFormat'] == 'yuv420p' for p in parameters)
            normalized = []
            if safe_shape:
                try:
                    for index, source in enumerate(parts):
                        target = attempt / f'normalized-{index:02}-{session}.mp4'
                        run(normalize_packet_command(source, target), attempt / f'normalize-{index:02}-{session}.log')
                        normalized.append(target)
                    parameters = [probe_video(path) for path in normalized]
                except (ValueError, RuntimeError):
                    state['normalizationFallback'] = 'Packet metadata normalization failed; retain files/logs and use normalized encode.'
                    normalized = []
            state['normalizedPartParameters'] = parameters
            stream_copy = bool(normalized and copy_compatible(parameters))
            listing = attempt / f'concat-{session}.txt'
            listing.write_text('\n'.join("file '" + str(p.as_posix()).replace("'", "'\\''") + "'" for p in (normalized if stream_copy else parts)), encoding='utf-8')
            output = attempt / f'joined-{session}.mp4'
            print('JOIN', 'stream-copy' if stream_copy else 'normalized-encode', state['frames'], flush=True)
            join_clock = time.monotonic()
            try:
                state['joinTiming'] = run(concat_command(listing, mix, state['frames'], output, stream_copy=stream_copy), attempt / f'join-{session}.log')
                final = decoded(output, state['frames'])
            except (ValueError, RuntimeError):
                if not stream_copy:
                    raise
                if output.exists():
                    output.rename(output.with_name(output.stem + '-failed-copy.mp4'))
                state['copyFallback'] = 'Stream-copy command or full decode failed; retained result and encoded normalized final.'
                state['joinTiming'] = run(concat_command(listing, mix, state['frames'], output, stream_copy=False), attempt / f'join-fallback-{session}.log')
                final = decoded(output, state['frames'])
                stream_copy = False
            state['joinAndDecodeWallSeconds'] = round(time.monotonic() - join_clock, 3)
            narration = load(batch / 'audio/narration.receipt.json')
            state['audioDecode'] = audio_decoded(output, state['frames'] / 30, narration['lastWordEnd'])
            require(sha(mix) == state['mixSHA256'], 'Mix changed while rendering')
            require(not (batch / 'final.mp4').exists(), 'A final appeared; retain joined output without overwriting')
            output.replace(batch / 'final.mp4')
            state.update({'status': 'completed', 'finishedUTC': utc(), 'final': final, 'joinMode': 'stream-copy' if stream_copy else 'normalized-encode',
                          'thisSessionWallSeconds': round(time.monotonic() - started, 3)})
            save(attempt / 'state.json', state)
            render_wall = sum(part['renderTiming']['wallSeconds'] for part in state['parts'])
            summary = {'schema': 'china-render-benchmark/1', 'attempt': str(attempt), 'startedUTC': state['startedUTC'], 'finishedUTC': state['finishedUTC'],
                'bundle': state['bundleTiming'], 'chapters': [{'id': p['id'], **p['renderTiming']} for p in state['parts']],
                'chapterRenderWallSeconds': render_wall, 'aggregateRenderFramesPerSecond': state['frames'] / max(.001, render_wall),
                'join': state['joinTiming'], 'joinMode': state['joinMode'], 'finalDecode': final, 'finalAudioDecode': state['audioDecode'],
                'concurrency': options, 'mediaCacheBytes': CACHE_BYTES, 'memoryAtStart': state['memoryAtStart'],
                'scope': 'Measured wall time and throughput only; no guessed machine/electricity USD cost, audio listening or user acceptance.'}
            save(batch / 'benchmark/render-stage.json', summary)
            save(batch / 'render-receipt.json', {'attempt': str(attempt), 'finalSHA256': final['sha256'], 'frames': state['frames'],
                'audioMixSHA256': state['mixSHA256'], 'concurrency': options, 'joinMode': state['joinMode'],
                'fullFrameDecode': 'passed', 'audioEndDecode': 'passed', 'userAcceptance': 'pending'})
            print('COMPLETED', batch / 'final.mp4', flush=True)
            return summary
        except BaseException as error:
            state.update({'status': 'failed', 'errorType': type(error).__name__, 'error': str(error)})
            save(attempt / 'state.json', state)
            raise


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--batch', type=Path, required=True)
    parser.add_argument('--resume', type=Path)
    parser.add_argument('--concurrency', type=int, choices=[1, 2, 4])
    args = parser.parse_args()
    print(json.dumps(render(args.batch, args.resume, args.concurrency), ensure_ascii=False, indent=2))
