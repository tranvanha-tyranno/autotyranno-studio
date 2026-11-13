"""Repair one visual headline from the frozen China bundle; preserve source film."""
import argparse
import copy
from datetime import datetime, timezone
from pathlib import Path
import shutil
import time

import china
import china_render as renderer
import production_repair as splice
import render_directions

load, save, sha, require = china.load, china.save, china.sha, china.require


def headline_repair(batch, base_attempt, shot_id, headline, revision='r02'):
    batch, base = Path(batch).resolve(), Path(base_attempt).resolve()
    out = batch / revision
    require(base.parent == batch / 'render-attempts' and not out.exists(), 'Use retained base attempt and a new revision folder')
    old = load(batch / 'data.json')
    data = copy.deepcopy(old)
    selected = [shot for shot in data['shots'] if shot['id'] == shot_id]
    require(len(selected) == 1 and headline.strip(), 'Select exactly one known headline')
    selected[0]['headline'] = headline
    for before, after in zip(old['shots'], data['shots']):
        expected = copy.deepcopy(before)
        if before['id'] == shot_id:
            expected['headline'] = headline
        require(after == expected, 'Repair changed an unselected visual field')
    require({k: v for k, v in old.items() if k != 'shots'} == {k: v for k, v in data.items() if k != 'shots'}, 'Repair changed audio/captions/timeline')
    state = load(base / 'state.json')
    require(state['status'] == 'completed' and sha(batch / 'final.mp4') == state['final']['sha256'], 'Base final is not completed/current')
    require(sha(batch / 'data.json') == state['dataSHA256'] and sha(batch / 'props.json') == state['propsSHA256'], 'Base prepared inputs changed')
    require(renderer.tree(base / 'bundle') == state['bundleFiles'], 'Frozen base bundle changed')
    for row in load(base / 'source-snapshot/hashes.json'):
        require(sha(base / 'source-snapshot' / row['file']) == row['sha256'], 'Base source snapshot changed')
    mix = batch / 'audio/final-mix.wav'
    require(sha(mix) == state['mixSHA256'], 'Exact mix changed')
    before_final, before_data = sha(batch / 'final.mp4'), sha(batch / 'data.json')
    started, clock = datetime.now(timezone.utc).isoformat(), time.monotonic()
    out.mkdir()
    save(out / 'data.json', data)
    save(out / 'props.json', {'data': data})
    for name in ['content.json', 'visual-plan.json']:
        authored = copy.deepcopy(load(batch / name))
        if name == 'content.json':
            for chapter in authored['chapters']:
                for beat in chapter['beats']:
                    if beat['id'] == shot_id:
                        beat['headline'] = headline
        else:
            rows = authored.get('shots', authored) if isinstance(authored, dict) else authored
            if isinstance(rows, dict):
                if shot_id in rows and 'headline' in rows[shot_id]:
                    rows[shot_id]['headline'] = headline
            else:
                for row in rows:
                    if row['id'] == shot_id and 'headline' in row:
                        row['headline'] = headline
        save(out / name, authored)
    snap = out / 'source-snapshot'
    snap.mkdir()
    shutil.copy2(Path(__file__), snap / 'china_repair.py')
    shutil.copy2(batch / 'audio/mix-report.json', snap / 'mix-report.json')
    save(snap / 'hashes.json', renderer.tree(snap))
    # ChinaFilm currently uses hard Sequence cuts with no overlap. Seven frames
    # of the following unchanged scene are retained as a conservative seam tail.
    shot = selected[0]
    start, end = shot['start'], min(data['frames'], shot['end'] + 7)
    interval = {'start': start, 'endExclusive': end, 'frames': end - start}
    plan = {'fps': data['fps'], 'frames': data['frames'], 'segments': splice.segments_for([[start, end]], data['frames'])}
    receipt = {'schema': 'china-visual-repair/1', 'status': 'running', 'startedUTC': started, 'changedShot': shot_id,
        'oldHeadline': next(s['headline'] for s in old['shots'] if s['id'] == shot_id), 'newHeadline': headline,
        'interval': interval, 'baseFinalSHA256': before_final, 'baseDataSHA256': before_data,
        'newDataSHA256': sha(out / 'data.json'), 'exactMixSHA256': sha(mix), 'baseAttempt': str(base),
        'sameSpokenTake': True, 'sameCaptions': True, 'sameTiming': True, 'unselectedAppearanceUnchanged': True,
        'userAcceptance': 'pending', 'limitation': 'Normalized full-video encode at splice; unselected decoded pixels are not asserted byte-identical.'}
    save(out / 'repair-receipt.json', receipt)
    with render_directions.project_lock('china-' + revision + '-' + shot_id):
        patch = out / 'patch.mp4'
        receipt['patchRender'] = renderer.run(['node', renderer.CLI, 'render', base / 'bundle', 'ChinaPreview', patch,
            f'--props={out/"props.json"}', f'--frames={start}-{end-1}', '--muted', '--codec=h264', '--crf=18',
            '--color-space=bt709', '--pixel-format=yuv420p', '--concurrency=2', '--media-cache-size-in-bytes=268435456',
            '--log=info'], out / 'patch.log')
        receipt['patchDecode'] = renderer.decoded(patch, end - start)
        save(out / 'repair-receipt.json', receipt)
        command = splice.splice_command(batch / 'final.mp4', [patch], mix, plan, out / 'final.mp4', crf=18)
        command[command.index('-preset') + 1] = 'fast'
        receipt['spliceTiming'] = renderer.run(command, out / 'splice.log')
        receipt['finalDecode'] = renderer.decoded(out / 'final.mp4', data['frames'])
        last = load(batch / 'audio/narration.receipt.json')['lastWordEnd']
        receipt['audioDecode'] = renderer.audio_decoded(out / 'final.mp4', data['frames'] / data['fps'], last)
        require(sha(batch / 'final.mp4') == before_final and sha(batch / 'data.json') == before_data and sha(mix) == receipt['exactMixSHA256'], 'Source film/data/mix changed during repair')
        receipt.update({'status': 'completed', 'finishedUTC': datetime.now(timezone.utc).isoformat(),
                        'wallSeconds': round(time.monotonic() - clock, 3), 'finalSHA256': receipt['finalDecode']['sha256']})
        save(out / 'repair-receipt.json', receipt)
        save(out / 'render-receipt.json', {'attempt': str(out), 'finalSHA256': receipt['finalSHA256'], 'frames': data['frames'],
             'audioMixSHA256': receipt['exactMixSHA256'], 'sameSpokenTake': True, 'sameWordTiming': True,
             'sameCaptions': True, 'changedShots': [shot_id], 'userAcceptance': 'pending'})
    return receipt


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--batch', type=Path, required=True)
    p.add_argument('--base-attempt', type=Path, required=True)
    p.add_argument('--shot', required=True)
    p.add_argument('--headline', required=True)
    p.add_argument('--revision', default='r02')
    a = p.parse_args()
    result = headline_repair(a.batch, a.base_attempt, a.shot, a.headline, a.revision)
    print('REPAIR_COMPLETE', result['finalSHA256'], result['wallSeconds'], flush=True)
