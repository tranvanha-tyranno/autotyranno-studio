"""Repair selected inspected shots in a new batch, keeping the exact narration take.

Only selected frame ranges are rendered again. Final video is normalized and encoded
once from old-before, new-patch and old-after segments. Re-encoded pixels outside the
patch need not be byte-identical to the previous H264. Source batches never change.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import math
from pathlib import Path
import shutil
import subprocess
import sys
import uuid

from documentary import FF
import production
import render_directions as renderer

WORKFLOW = Path(__file__).resolve().parent
ROOT = WORKFLOW.parents[1]
OVERLAP_FRAMES = 7


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load(path):
    return production.load(path)


def save(path, value):
    return production.save(path, value)


def sha(path):
    return production.sha(path)


def canonical_shot(shot, receipts):
    """Use actual derivative hashes instead of per-batch public URL strings."""
    result = {key: shot.get(key) for key in
              ['start', 'end', 'phase', 'layout', 'eyebrow', 'headline', 'body', 'sourceNote']}
    result['images'] = []
    for image in shot['images']:
        require(image['file'] in receipts, 'Missing retained render asset receipt: ' + image['file'])
        record = {key: value for key, value in image.items() if key not in ['file', 'posterFile']}
        record['fileSHA256'] = receipts[image['file']]['publicSHA256']
        if image.get('posterFile'):
            require(image['posterFile'] in receipts, 'Missing retained poster receipt')
            record['posterSHA256'] = receipts[image['posterFile']]['publicSHA256']
        result['images'].append(record)
    return result


def merge_intervals(intervals):
    merged = []
    for start, end in sorted(intervals):
        if merged and start <= merged[-1][1]:
            merged[-1][1] = max(end, merged[-1][1])
        else:
            merged.append([start, end])
    return merged


def segments_for(intervals, total):
    result, cursor = [], 0
    for index, (start, end) in enumerate(intervals):
        require(0 <= cursor <= start < end <= total, 'Patch intervals overlap or leave timeline bounds')
        if cursor < start:
            result.append({'kind': 'previous', 'start': cursor, 'end': start, 'frames': start - cursor})
        result.append({'kind': 'patch', 'patch': index, 'start': start, 'end': end, 'frames': end - start})
        cursor = end
    if cursor < total:
        result.append({'kind': 'previous', 'start': cursor, 'end': total, 'frames': total - cursor})
    require(sum(item['frames'] for item in result) == total, 'Splice segments do not cover the entire exact take')
    return result


def repair_plan(previous, current, changed_shots):
    previous, current = Path(previous).resolve(), Path(current).resolve()
    require(previous != current and not current.is_relative_to(previous), 'Repair must use a separate new batch')
    old, new = load(previous / 'data.json'), load(current / 'data.json')
    for key in ['direction', 'fps', 'frames', 'title', 'captions']:
        require(old.get(key) == new.get(key), 'Repair cannot change timeline/captions/title: ' + key)
    require(old['fps'] == 30, 'Repair is normalized to the retained 30 fps composition')
    require(len(old['shots']) == len(new['shots']), 'Repair cannot add or remove shots')
    for name in ['narration-original.mp3', 'narration-original.alignment.json', 'narration-original.receipt.json', 'final-mix.wav']:
        require(sha(previous / 'audio' / name) == sha(current / 'audio' / name), 'Repair must retain the exact narration/mix: ' + name)
    require((previous / 'script.txt').read_bytes() == (current / 'script.txt').read_bytes(), 'Repair cannot change the spoken script')
    old_assets = {item['publicFile']: item for item in load(previous / 'render-assets.json')['assets']}
    new_assets = {item['publicFile']: item for item in load(current / 'render-assets.json')['assets']}
    selected = set(changed_shots)
    require(selected and len(selected) == len(changed_shots), 'Select unique changed shot ids')
    known, intervals = set(), []
    for old_shot, new_shot in zip(old['shots'], new['shots']):
        key = old_shot.get('id')
        require(key and key == new_shot.get('id'), 'Repair requires stable matching shot ids')
        known.add(key)
        for field in ['start', 'end', 'phase', 'phrase', 'narrationClause']:
            require(old_shot.get(field) == new_shot.get(field), 'Repair changed narration/timing for ' + key + ': ' + field)
        if key in selected:
            intervals.append((old_shot['start'], min(old_shot['end'] + OVERLAP_FRAMES, old['frames'])))
        else:
            require(canonical_shot(old_shot, old_assets) == canonical_shot(new_shot, new_assets),
                    'Unselected shot appearance changed: ' + key)
    require(selected <= known, 'Unknown changed shot ids: ' + ', '.join(sorted(selected - known)))
    intervals = merge_intervals(intervals)
    return {'schema': 'reference-video-repair-plan/1', 'previous': str(previous), 'current': str(current),
        'fps': old['fps'], 'frames': old['frames'], 'changedShots': sorted(selected),
        'intervals': [{'start': start, 'endExclusive': end, 'remotionFrames': f'{start}-{end-1}', 'frames': end-start}
                      for start, end in intervals],
        'segments': segments_for(intervals, old['frames']), 'oldFinalSHA256': sha(previous / 'final.mp4'),
        'exactMixSHA256': sha(current / 'audio/final-mix.wav'), 'captionsUnchanged': True,
        'timingUnchanged': True, 'userAcceptance': 'pending',
        'limitation': 'Splice normalizes and re-encodes the entire video once; unchanged H264 pixels are not asserted byte-identical.'}


def normalized_filter(input_index, start, end, label, fps=30):
    return (f'[{input_index}:v:0]trim=start_frame={start}:end_frame={end},setpts=PTS-STARTPTS,'
            f'fps={fps},setsar=1,scale=iw:ih:in_range=auto:out_range=tv:out_color_matrix=bt709,format=yuv420p,'
            f'setparams=range=limited:color_primaries=bt709:color_trc=bt709:colorspace=bt709[{label}]')


def splice_command(previous_final, patches, mix, plan, output, crf=19):
    arguments = [FF, '-y', '-v', 'error', '-i', str(previous_final)]
    for patch in patches:
        arguments += ['-i', str(patch)]
    mix_input = len(patches) + 1
    arguments += ['-i', str(mix)]
    graph, labels = [], []
    for index, segment in enumerate(plan['segments']):
        label = f's{index}'
        if segment['kind'] == 'previous':
            input_index, start, end = 0, segment['start'], segment['end']
        else:
            input_index, start, end = segment['patch'] + 1, 0, segment['frames']
        graph.append(normalized_filter(input_index, start, end, label, plan['fps']))
        labels.append(f'[{label}]')
    graph.append(''.join(labels) + f'concat=n={len(labels)}:v=1:a=0[outv]')
    arguments += ['-filter_complex', ';'.join(graph), '-map', '[outv]', '-map', f'{mix_input}:a:0',
        '-frames:v', str(plan['frames']), '-c:v', 'libx264', '-crf', str(crf), '-preset', 'medium', '-pix_fmt', 'yuv420p',
        '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709', '-color_range', 'tv', '-r', str(plan['fps']),
        '-t', f'{plan["frames"] / plan["fps"]:.9f}',
        '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-ac', '2', '-movflags', '+faststart', str(output)]
    return arguments


def retain_exact_audio(previous, current):
    require((previous / 'audio-sources.json').is_file(), 'Previous film lacks retained audio source receipt')
    receipt = load(previous / 'audio-sources.json')
    require(sha(previous / 'audio/final-mix.wav') == receipt['mix']['sha256'], 'Previous mix has changed')
    for name in ['narration-original.mp3', 'narration-original.alignment.json', 'narration-original.receipt.json', 'final-mix.wav']:
        source, target = previous / 'audio' / name, current / 'audio' / name
        target.parent.mkdir(parents=True, exist_ok=True)
        require(not target.exists() or sha(target) == sha(source), 'New revision already has different audio: ' + name)
        if not target.exists():
            shutil.copy2(source, target)
    target = current / 'audio-sources.json'
    require(not target.exists() or load(target) == receipt, 'New revision has a different audio receipt')
    if not target.exists():
        shutil.copy2(previous / 'audio-sources.json', target)


def check_decoded(path, frames, fps):
    import cv2
    cap = cv2.VideoCapture(str(path))
    require(cap.isOpened(), 'Cannot decode repaired/patch MP4')
    actual_fps = cap.get(cv2.CAP_PROP_FPS)
    count = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        count += 1
    cap.release()
    require(count == frames and math.isclose(actual_fps, fps, abs_tol=.001), 'Patch/repaired MP4 frame count or FPS differs')
    return {'decodedFrames': count, 'fps': actual_fps, 'sha256': sha(path)}


def repair(previous, manifest_path, batch, changed_shots, guidance=None, memory_profile=None, dry_run=False):
    previous, batch, manifest_path = Path(previous).resolve(), Path(batch).resolve(), Path(manifest_path).resolve()
    manifest = load(manifest_path)
    production.validate_structure(manifest)
    current = production.film_folder(manifest, batch)
    require(not current.is_relative_to(previous) and current != previous, 'Use a separate batch for repairs')
    require(not (current / 'final.mp4').exists(), 'New repair batch already has a final; use another revision')
    public = batch / 'production-public'
    selected_profile = memory_profile or manifest.get('renderOptions', {}).get('memoryProfile', 'default')
    options = renderer.resolved_render_options(1, 19, selected_profile)
    if dry_run:
        require((current / 'data.json').exists(), 'Dry-run requires an already prepared new revision; it never copies or prepares files')
        plan = repair_plan(previous, current, changed_shots)
        plan['renderOptions'] = options
        return plan
    require((previous / 'final.mp4').is_file(), 'Previous final does not exist; let its render/QA finish first')
    previous_qa = load(previous / 'qa/report.json')
    require(previous_qa.get('frameCountPass') is True and previous_qa.get('videoSHA256') == sha(previous / 'final.mp4'),
            'Previous final needs a current full-duration technical QA receipt before repair')
    current.mkdir(parents=True, exist_ok=True)
    retain_exact_audio(previous, current)
    production.prepare(manifest_path, batch, guidance)
    plan = repair_plan(previous, current, changed_shots)
    manifest_copy = current / 'production-manifest.json'
    require(load(manifest_path) == load(manifest_copy), 'New manifest snapshot differs')
    film = renderer.preflight(batch, [manifest['direction']], public)
    attempt_id = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ') + '-repair-' + uuid.uuid4().hex[:6]
    attempt = batch / 'repair-attempts' / attempt_id
    bundle, staged = attempt / 'bundle', attempt / 'public'
    node = shutil.which('node')
    require(node, 'Node.js is unavailable')
    cli = [node, str(renderer.CLI.resolve())]
    with renderer.project_lock(attempt_id):
        attempt.mkdir(parents=True, exist_ok=False)
        state = {'attempt': attempt_id, 'status': 'running', 'steps': [], 'plan': plan,
                 'renderOptions': options, 'memoryAtStart': renderer.memory_snapshot(),
                 'aestheticAcceptance': 'pending user feedback'}
        save(attempt / 'attempt.json', state)
        try:
            renderer.snapshot_sources(attempt / 'source-snapshot', film)
            shutil.copy2(WORKFLOW / 'production_repair.py', attempt / 'source-snapshot/production_repair.py')
            save(attempt / 'source-receipts.json', {'previousFinal': {'file': str(previous / 'final.mp4'), 'sha256': sha(previous / 'final.mp4')},
                'previousData': {'file': str(previous / 'data.json'), 'sha256': sha(previous / 'data.json')},
                'newManifest': {'file': str(manifest_path), 'sha256': sha(manifest_path)},
                'newData': {'file': str(current / 'data.json'), 'sha256': sha(current / 'data.json')},
                'exactMix': {'file': str(current / 'audio/final-mix.wav'), 'sha256': sha(current / 'audio/final-mix.wav')}})
            renderer.stage_public(batch, staged, attempt, film)
            renderer.run_logged(cli + ['bundle', str(renderer.ENTRY.resolve()), f'--out-dir={bundle}', f'--public-dir={staged}', '--log=info'],
                                attempt / 'bundle.log', state, attempt)
            require((bundle / 'index.html').is_file(), 'New persistent repair bundle is missing')
            patches = []
            for index, interval in enumerate(plan['intervals']):
                output = attempt / f'patch-{index:02}.mp4'
                command = cli + ['render', str(bundle), 'DirectionPreview', str(output),
                    *renderer.render_arguments(current / 'props.json', options),
                    f'--frames={interval["remotionFrames"]}', '--muted']
                renderer.run_logged(command, attempt / f'patch-{index:02}.log', state, attempt)
                check_decoded(output, interval['frames'], plan['fps'])
                patches.append(output)
            command = splice_command(previous / 'final.mp4', patches, current / 'audio/final-mix.wav', plan, attempt / 'joined.mp4')
            renderer.run_logged(command, attempt / 'splice.log', state, attempt)
            state['joinedDecode'] = check_decoded(attempt / 'joined.mp4', plan['frames'], plan['fps'])
            require(sha(previous / 'final.mp4') == plan['oldFinalSHA256'], 'Previous final changed during repair')
            require(sha(current / 'audio/final-mix.wav') == plan['exactMixSHA256'], 'Exact mix changed during repair')
            (attempt / 'joined.mp4').replace(current / 'final.mp4')
            renderer.run_logged([sys.executable, str(WORKFLOW / 'direction_qa.py'), '--batch', str(current), '--public-source', str(public)],
                                attempt / 'qa.log', state, attempt)
            state['status'] = 'completed'
            state['finalSHA256'] = sha(current / 'final.mp4')
            save(attempt / 'attempt.json', state)
            save(current / 'repair-receipt.json', {'attempt': str(attempt), 'plan': plan, 'finalSHA256': state['finalSHA256'],
                'technicalQA': 'passed', 'visualAcceptance': 'pending', 'audioListening': 'not established by this script'})
        except BaseException as error:
            state.update({'status': 'failed', 'errorType': type(error).__name__, 'error': str(error)})
            save(attempt / 'attempt.json', state)
            raise
    return {'attempt': str(attempt), 'current': str(current), 'status': 'completed', 'userAcceptance': 'pending'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--previous', type=Path, required=True, help='Previous film directory containing final.mp4 and data.json')
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--batch', type=Path, required=True, help='New revision batch root')
    parser.add_argument('--changed-shot', action='append', required=True, dest='changed_shots')
    parser.add_argument('--guidance', type=Path)
    parser.add_argument('--memory-profile', choices=['default', 'bounded'])
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    print(json.dumps(repair(args.previous, args.manifest, args.batch, args.changed_shots,
        args.guidance, args.memory_profile, args.dry_run), ensure_ascii=False, indent=2))
