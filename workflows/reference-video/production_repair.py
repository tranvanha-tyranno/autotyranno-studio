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
              ['start', 'end', 'phase', 'layout', 'motion', 'eyebrow', 'headline', 'body', 'sourceNote']}
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


def tree_receipt(root):
    root = Path(root)
    require(root.is_dir(), 'Missing retained render tree: ' + str(root))
    return [{'file': path.relative_to(root).as_posix(), 'sha256': sha(path)}
            for path in sorted(root.rglob('*')) if path.is_file()]


def snapshot_integrity(snapshot):
    records = load(snapshot / 'hashes.json')
    require(records, 'Missing source snapshot hashes')
    for record in records:
        file = production.within(snapshot, snapshot / record['file'])
        require(file.is_file() and sha(file) == record['sha256'], 'Retained source snapshot changed: ' + record['file'])
    return records


def validate_bundle_sources(bundle, snapshot, records):
    """Legacy attempts predate bundle hashes: compare original mapped sources first."""
    mapped = {}
    for path in bundle.rglob('*.map'):
        value = load(path)
        for name, content in zip(value.get('sources', []), value.get('sourcesContent', [])):
            if content is not None:
                mapped[name.replace('\\', '/')] = content.replace('\r\n', '\n')
    required = [row for row in records if row['file'].startswith('cinematic/src/')
                and row['file'].endswith(('.ts', '.tsx')) and not row['file'].endswith('/types.ts')]
    require(required, 'Legacy resume lacks retained application source')
    for row in required:
        suffix = row['file'][len('cinematic/'):]
        expected = (snapshot / row['file']).read_text(encoding='utf-8-sig')
        matches = [text for name, text in mapped.items() if name == suffix or name.endswith('/' + suffix)]
        require(matches and all(text == expected for text in matches), 'Frozen bundle source map differs from snapshot: ' + suffix)


def validate_resume(attempt, previous, current, manifest_path, plan, options):
    """Read-only validation; first explicit legacy resume pins newly measured hashes."""
    attempt, previous, current = map(lambda path: Path(path).resolve(), [attempt, previous, current])
    require(attempt.parent == current.parent / 'repair-attempts', 'Resume attempt must belong to this exact new batch')
    state = load(attempt / 'attempt.json')
    require(state.get('attempt') == attempt.name and state.get('status') in ['failed', 'running'], 'Resume requires an unfinished retained attempt')
    require(state.get('plan') == plan, 'Resume plan differs from retained attempt')
    require(state.get('renderOptions') == options, 'Resume render options differ from retained attempt')
    snapshot = attempt / 'source-snapshot'
    records = snapshot_integrity(snapshot)
    snapshot_integrity(attempt / 'previous-source-snapshot')
    batch_records = [row for row in records if row['file'].startswith('batch/' + plan['direction'] + '/')] if 'direction' in plan else [
        row for row in records if row['file'].startswith('batch/' + load(current / 'data.json')['direction'] + '/')]
    required = {'data.json', 'props.json', 'render-assets.json', 'production-manifest.json'}
    require(required <= {Path(row['file']).name for row in batch_records}, 'Resume lacks required prepared batch snapshots')
    for row in batch_records:
        file = current / Path(row['file']).name
        require(file.is_file() and sha(file) == row['sha256'], 'Prepared batch differs from frozen snapshot: ' + file.name)
    receipts = load(attempt / 'source-receipts.json')
    for key, file in {'previousFinal': previous / 'final.mp4', 'previousData': previous / 'data.json',
                      'newManifest': Path(manifest_path).resolve(), 'newData': current / 'data.json',
                      'exactMix': current / 'audio/final-mix.wav'}.items():
        require(Path(receipts[key]['file']).resolve() == file and sha(file) == receipts[key]['sha256'], 'Resume source receipt differs: ' + key)
    require(load(manifest_path) == load(current / 'production-manifest.json'), 'Resume manifest differs from retained snapshot')
    bundle, staged = attempt / 'bundle', attempt / 'public'
    require((bundle / 'index.html').is_file(), 'Frozen repair bundle is missing')
    data = load(current / 'data.json')
    namespace = 'directions/' + data['direction']
    expected = {row['publicFile']: row['publicSHA256'] for row in load(current / 'render-assets.json')['assets']}
    expected.update({namespace + '/data.json': sha(current / 'data.json'), namespace + '/mix.wav': plan['exactMixSHA256']})
    require({row['file']: row['sha256'] for row in tree_receipt(staged)} == expected, 'Staged render assets differ from retained receipts')
    bundle_public = bundle / 'public' if (bundle / 'public').is_dir() else bundle
    for name, digest in expected.items():
        file = production.within(bundle_public, bundle_public / name)
        require(file.is_file() and sha(file) == digest, 'Frozen bundle public asset differs: ' + name)
    fingerprint = {'schema': 'reference-video-repair-resume/1', 'plan': plan, 'renderOptions': options,
        'sourceSnapshotSHA256': sha(snapshot / 'hashes.json'), 'sourceReceiptsSHA256': sha(attempt / 'source-receipts.json'),
        'batchFiles': {Path(row['file']).name: row['sha256'] for row in batch_records},
        'bundleFiles': tree_receipt(bundle), 'stagedFiles': tree_receipt(staged)}
    checkpoint = attempt / 'resume-integrity.json'
    legacy = not checkpoint.exists()
    if legacy:
        require(any(step.get('status') == 'completed' and step.get('returncode') == 0 and 'bundle' in step.get('command', [])
                    for step in state.get('steps', [])), 'Legacy attempt lacks successful bundle completion')
        validate_bundle_sources(bundle, snapshot, records)
    else:
        require(load(checkpoint) == fingerprint, 'Resume frozen bundle/input integrity changed')
    return {'state': state, 'integrity': fingerprint, 'legacyAdopted': legacy}


def validated_patch(attempt, index, interval, fps, state):
    output = Path(attempt) / f'patch-{index:02}.mp4'
    receipt = state.get('patches', {}).get(str(index))
    if receipt:
        require(receipt.get('file') == output.name and receipt.get('interval') == interval
                and output.is_file() and sha(output) == receipt['decode']['sha256'], 'Completed patch hash/interval changed: ' + output.name)
        decoded = check_decoded(output, interval['frames'], fps)
        require(decoded == receipt['decode'], 'Completed patch decode differs: ' + output.name)
        return decoded
    steps = [step for step in state.get('steps', []) if str(output) in step.get('command', [])]
    if not output.exists() or not steps or steps[-1].get('status') != 'completed' or steps[-1].get('returncode') != 0:
        return None
    require('--frames=' + interval['remotionFrames'] in steps[-1]['command'], 'Completed patch command interval changed')
    return check_decoded(output, interval['frames'], fps)


def archive_incomplete(path):
    path = Path(path)
    if not path.exists():
        return None
    target = path.with_name(path.stem + '.failed-' + uuid.uuid4().hex[:10] + path.suffix)
    require(not target.exists(), 'Failed artifact archive already exists')
    path.rename(target)
    return target


def repair(previous, manifest_path, batch, changed_shots, guidance=None, memory_profile=None, dry_run=False, resume_from_attempt=None):
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
        if resume_from_attempt:
            resumed = validate_resume(resume_from_attempt, previous, current, manifest_path, plan, options)
            plan['resumeAttempt'] = str(Path(resume_from_attempt).resolve())
            plan['reusablePatches'] = [index for index, interval in enumerate(plan['intervals'])
                if validated_patch(Path(resume_from_attempt).resolve(), index, interval, plan['fps'], resumed['state'])]
        plan['renderOptions'] = options
        return plan
    require((previous / 'final.mp4').is_file(), 'Previous final does not exist; let its render/QA finish first')
    previous_qa = load(previous / 'qa/report.json')
    require(previous_qa.get('frameCountPass') is True
            and previous_qa.get('decodedFrames') == load(previous / 'data.json')['frames']
            and previous_qa.get('videoSHA256') == sha(previous / 'final.mp4'),
            'Previous final needs a current full-duration technical QA receipt before repair')
    if not resume_from_attempt:
        current.mkdir(parents=True, exist_ok=True)
        retain_exact_audio(previous, current)
        production.prepare(manifest_path, batch, guidance)
    plan = repair_plan(previous, current, changed_shots)
    manifest_copy = current / 'production-manifest.json'
    require(load(manifest_path) == load(manifest_copy), 'New manifest snapshot differs')
    film = renderer.preflight(batch, [manifest['direction']], public)
    attempt_id = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ') + '-repair-' + uuid.uuid4().hex[:6]
    attempt = Path(resume_from_attempt).resolve() if resume_from_attempt else batch / 'repair-attempts' / attempt_id
    if resume_from_attempt:
        attempt_id = attempt.name
    bundle, staged = attempt / 'bundle', attempt / 'public'
    node = shutil.which('node')
    require(node, 'Node.js is unavailable')
    cli = [node, str(renderer.CLI.resolve())]
    with renderer.project_lock(attempt_id):
        resume_id = uuid.uuid4().hex[:10] if resume_from_attempt else None
        if resume_from_attempt:
            resumed = validate_resume(attempt, previous, current, manifest_path, plan, options)
            state = resumed['state']
            save(attempt / f'attempt-before-resume-{resume_id}.json', state)
            if resumed['legacyAdopted']:
                save(attempt / 'resume-integrity.json', resumed['integrity'])
            state.setdefault('resumeSessions', []).append({'id': resume_id, 'startedUTC': datetime.now(timezone.utc).isoformat(),
                'legacyHashesAdoptedAfterSourceMapAndAssetValidation': resumed['legacyAdopted'],
                'integrityScope': 'Legacy attempts lack original bundle/patch byte hashes. First resume checks retained mapped sources, '
                    'asset receipts, successful command records and decoded patch frames, then pins current bytes. '
                    'Subsequent resumes require those pinned SHA-256 hashes; historical byte identity before the first pin is not established.',
                'controllerSHA256': sha(WORKFLOW / 'production_repair.py')})
            shutil.copy2(WORKFLOW / 'production_repair.py', attempt / f'resume-controller-{resume_id}.py')
            state['status'] = 'running'
            state.pop('errorType', None)
            state.pop('error', None)
        else:
            attempt.mkdir(parents=True, exist_ok=False)
            state = {'attempt': attempt_id, 'status': 'running', 'steps': [], 'plan': plan,
                     'renderOptions': options, 'memoryAtStart': renderer.memory_snapshot(),
                     'aestheticAcceptance': 'pending user feedback'}
        save(attempt / 'attempt.json', state)
        try:
            if not resume_from_attempt:
                renderer.snapshot_sources(attempt / 'source-snapshot', film)
                repair_source = WORKFLOW / 'production_repair.py'
                shutil.copy2(repair_source, attempt / 'source-snapshot/production_repair.py')
                snapshot_hashes = load(attempt / 'source-snapshot/hashes.json')
                snapshot_hashes.append({'file': 'production_repair.py', 'sha256': sha(repair_source)})
                save(attempt / 'source-snapshot/hashes.json', snapshot_hashes)
                old_snapshot = attempt / 'previous-source-snapshot'
                old_snapshot.mkdir()
                old_records = []
                for name in ['data.json', 'script.txt', 'audio-sources.json', 'render-assets.json', 'qa/report.json']:
                    target = old_snapshot / name
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(previous / name, target)
                    old_records.append({'file': name, 'sha256': sha(target)})
                save(old_snapshot / 'hashes.json', old_records)
                save(attempt / 'source-receipts.json', {'previousFinal': {'file': str(previous / 'final.mp4'), 'sha256': sha(previous / 'final.mp4')},
                    'previousData': {'file': str(previous / 'data.json'), 'sha256': sha(previous / 'data.json')},
                    'newManifest': {'file': str(manifest_path), 'sha256': sha(manifest_path)},
                    'newData': {'file': str(current / 'data.json'), 'sha256': sha(current / 'data.json')},
                    'exactMix': {'file': str(current / 'audio/final-mix.wav'), 'sha256': sha(current / 'audio/final-mix.wav')}})
                renderer.stage_public(batch, staged, attempt, film)
                renderer.run_logged(cli + ['bundle', str(renderer.ENTRY.resolve()), f'--out-dir={bundle}', f'--public-dir={staged}', '--log=info'],
                                    attempt / 'bundle.log', state, attempt)
                require((bundle / 'index.html').is_file(), 'New persistent repair bundle is missing')
                save(attempt / 'resume-integrity.json', validate_resume(attempt, previous, current, manifest_path, plan, options)['integrity'])
            patches = []
            for index, interval in enumerate(plan['intervals']):
                output = attempt / f'patch-{index:02}.mp4'
                decoded = validated_patch(attempt, index, interval, plan['fps'], state) if resume_from_attempt else None
                if decoded:
                    state.setdefault('patches', {})[str(index)] = {'file': output.name, 'interval': interval, 'decode': decoded}
                    state.setdefault('reusedPatches', []).append({'resumeId': resume_id, 'index': index, 'decode': decoded})
                    save(attempt / 'attempt.json', state)
                    patches.append(output)
                    continue
                if output.exists():
                    archived = archive_incomplete(output)
                    state.setdefault('failedArtifacts', []).append({'original': output.name, 'retained': archived.name, 'sha256': sha(archived)})
                    save(attempt / 'attempt.json', state)
                command = cli + ['render', str(bundle), 'DirectionPreview', str(output),
                    *renderer.render_arguments(current / 'props.json', options),
                    f'--frames={interval["remotionFrames"]}', '--muted']
                log_name = f'patch-{index:02}-resume-{resume_id}.log' if resume_id else f'patch-{index:02}.log'
                renderer.run_logged(command, attempt / log_name, state, attempt)
                decoded = check_decoded(output, interval['frames'], plan['fps'])
                state.setdefault('patches', {})[str(index)] = {'file': output.name, 'interval': interval, 'decode': decoded}
                save(attempt / 'attempt.json', state)
                patches.append(output)
            if (attempt / 'joined.mp4').exists():
                archive_incomplete(attempt / 'joined.mp4')
            command = splice_command(previous / 'final.mp4', patches, current / 'audio/final-mix.wav', plan, attempt / 'joined.mp4')
            renderer.run_logged(command, attempt / (f'splice-resume-{resume_id}.log' if resume_id else 'splice.log'), state, attempt)
            state['joinedDecode'] = check_decoded(attempt / 'joined.mp4', plan['frames'], plan['fps'])
            require(sha(previous / 'final.mp4') == plan['oldFinalSHA256'], 'Previous final changed during repair')
            require(sha(current / 'audio/final-mix.wav') == plan['exactMixSHA256'], 'Exact mix changed during repair')
            (attempt / 'joined.mp4').replace(current / 'final.mp4')
            renderer.run_logged([sys.executable, str(WORKFLOW / 'direction_qa.py'), '--batch', str(current), '--public-source', str(public)],
                                attempt / (f'qa-resume-{resume_id}.log' if resume_id else 'qa.log'), state, attempt)
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
    parser.add_argument('--resume-from-attempt', type=Path, help='Explicitly resume this frozen attempt after validating retained inputs and completed patches')
    args = parser.parse_args()
    print(json.dumps(repair(args.previous, args.manifest, args.batch, args.changed_shots,
        args.guidance, args.memory_profile, args.dry_run, args.resume_from_attempt), ensure_ascii=False, indent=2))
