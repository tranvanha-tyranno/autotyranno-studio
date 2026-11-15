"""Auditable source-interval edit and hybrid FFmpeg/Remotion documentary export."""
from __future__ import annotations

import argparse
import math
from pathlib import Path
import shutil
import time

import cv2

from bread_documentary import BATCH, FPS, PROJECT, ROOT, FF, cli, decoded_frames, load, run, save, sha, sheets

PUBLIC = BATCH / 'render-public-v3'
ENTRY = PROJECT / 'src/bread-documentary-entry.tsx'
REGISTRY = BATCH / 'research/render-footage-sources.json'
MATH_UNITS = {'b03': 20, 'b05': 20, 'b06': 10, 'b08': 20, 'b18': 11}


def allocate(assets, usage, tags, seconds, previous):
    candidates = []
    for asset in assets:
        length = float(asset['durationSeconds'])
        intervals = asset.get('usableIntervals') or [{'start': .35, 'end': length - .15}]
        position = None
        for interval in intervals:
            lower = float(interval.get('startSeconds', interval.get('start', .35)))
            upper = float(interval.get('endSeconds', interval.get('end', length - .15)))
            candidate_start = max(lower, usage.get(asset['id'], lower))
            if upper - candidate_start >= seconds + .02:
                position = candidate_start
                break
        if position is None:
            continue
        matches = set(tags) & set(asset['tags'])
        if not matches:
            continue
        score = sum((len(tags) - i) * 3 for i, tag in enumerate(tags) if tag in matches)
        # Prefer a new subject/action; never recycle source intervals to fill gaps.
        score -= 12 if asset['id'] == previous else 0
        score -= position / 20
        candidates.append((score, asset, position))
    if not candidates:
        raise ValueError(f'No inspected non-overlapping source interval for {tags}, {seconds:.2f}s')
    _, asset, start = max(candidates, key=lambda x: x[0])
    usage[asset['id']] = start + seconds + .18
    return asset, start


def cuts(unit):
    start, end = unit['from'], unit['from'] + unit['duration']
    if unit['id'] in MATH_UNITS:
        prelude = min(45, max(0, unit['duration'] - 5 * FPS))
        result = [(start, start + prelude, False)] if prelude else []
        start += prelude
        length = min(end - start, round(MATH_UNITS[unit['id']] * FPS))
        # Calculations develop with the actual speech, then clear to real action.
        result.append((start, start + length, True))
        start += length
    else:
        result = []
    while end - start > 7 * FPS:
        sentence = [round(w['start'] * FPS) for i, w in enumerate(unit['wordTimes']) if i > 0
                    and unit['wordTimes'][i-1]['text'].endswith(('.', '?', '!'))
                    and start + 3 * FPS <= round(w['start'] * FPS) <= start + 6 * FPS]
        boundary = min(sentence, key=lambda n: abs(n - start - 4.5 * FPS)) if sentence else start + round(4.7 * FPS)
        result.append((start, boundary, False))
        start = boundary
    if end > start:
        if end - start < FPS and result:
            a, _, graphic = result.pop()
            result.append((a, end, graphic))
        else:
            result.append((start, end, False))
    return result


def plan():
    timeline = load(BATCH / 'timeline.json')
    registry = load(REGISTRY)
    assets = registry['assets']
    by_id = {a['id']: a for a in assets}
    for asset in assets:
        path = BATCH / asset['file']
        if sha(path) != asset['sha256']:
            raise ValueError('Changed footage: ' + asset['id'])
        if asset.get('inspection', {}).get('status') != 'inspected':
            raise ValueError('Footage not inspected: ' + asset['id'])
    usage, previous, shots, evidence = {}, None, [], []
    for unit in timeline['units']:
        for n, (start, end, graphic) in enumerate(cuts(unit)):
            seconds = (end - start) / FPS
            tags = list(unit['tags'])
            # These passages explain the SAME bread's price/cost relationship;
            # moving bread/process is legitimate context behind the explanation,
            # while foreign banknotes would falsely suggest the modeled VND.
            if unit['id'] == 'b06':
                tags = ['bread', 'receipt', 'bakery']
            elif unit['id'] == 'b10' and n > 0:
                tags = ['bread', 'bakery']
            elif unit['id'] == 'b15':
                tags = ['shop', 'bakery'] if n == 0 else ['bakery', 'bread']
            elif unit['id'] == 'b16':
                tags = ['receipt', 'payment', 'bread'] if n == 0 else ['bread', 'bakery']
            elif unit['id'] == 'b09':
                tags = ['bread', 'bakery']
            eligible = assets
            # Save the actual Vietnamese sandwich preparation's final interval
            # for the callback/CTA; don't spend every hero second in the opening.
            saved = usage.get('pexels-30329515', .1)
            if unit['id'] != 'b24' and saved + seconds > 14:
                eligible = [a for a in assets if a['id'] != 'pexels-30329515']
            # Reserve complete visible baguette actions for the two explanations
            # that explicitly compare the price/quantity of that same bread.
            if unit['id'] < 'b08':
                eligible = [a for a in eligible if a['id'] != 'pexels-8530514']
            if unit['id'] < 'b18' or (unit['id'] == 'b18' and not graphic):
                eligible = [a for a in eligible if a['id'] != 'pexels-3943592']
            forced = {'b03': 'pexels-3943588', 'b05': 'pexels-8176160', 'b08': 'pexels-8530514', 'b18': 'pexels-3943592'}
            if graphic and unit['id'] in forced:
                eligible = [a for a in assets if a['id'] == forced[unit['id']]]
                tags = ['flour'] if unit['id'] == 'b05' else ['bread']
            try:
                asset, source_start = allocate(eligible, usage, tags, seconds, previous)
            except ValueError as error:
                raise ValueError(unit['id'] + ': ' + str(error)) from error
            previous = asset['id']
            sid = unit['id'] + f'-{n + 1:02}'
            row = {'id': sid, 'from': start, 'duration': end - start,
                   'chapterId': unit['chapterId'], 'chapterTitle': unit['chapterTitle'],
                   'media': 'graphic' if graphic else 'video', 'file': 'shots/' + sid + '.mp4',
                   'sourceStartSeconds': 0, 'sourceId': asset['id'], 'rawStartSeconds': source_start,
                   'sourceSHA256': asset['sha256'], 'narrationUnit': unit['id'],
                   'exposure': 1, 'graphicSide': 'right'}
            if graphic:
                row.update(kind=unit['kind'], data=unit['data'], label='Ví dụ minh họa')
                if unit.get('emphasis'):
                    row['emphasis'] = unit['emphasis']
            elif n == 0 and unit.get('headline'):
                row['headline'] = unit['headline']
            elif n == 0 and unit.get('emphasis') and unit['id'] not in MATH_UNITS:
                row['emphasis'] = unit['emphasis']
            if unit['id'] == 'b04' and n == 0:
                row['emphasis'] = '3.000đ chưa phải lãi ròng'
            # Reveal relative to the exact take, within the brief explanation.
            if graphic:
                cue_text = {'b03': ['hai mươi nghìn', 'mười hai nghìn', 'năm nghìn', 'ba nghìn'],
                            'b05': ['mười bốn nghìn năm trăm', 'giữ giá cũ', 'hai mươi hai nghìn', 'hai nghìn năm trăm'],
                            'b06': ['hai nghìn năm trăm', 'hai nghìn tăng thêm', 'giá bán đi lên'],
                            'b08': ['hai mươi', 'hai mươi hai nghìn là', 'hai mươi hai nghìn bốn trăm'],
                            'b18': ['bốn trăm bảy mươi', 'không ai cần', 'phép so']}[unit['id']]
                cue_frames = []
                tokens = [w['text'].strip('.,!?;:').casefold() for w in unit['wordTimes']]
                for phrase in cue_text:
                    q = phrase.split()
                    found = next((i for i in range(len(tokens) - len(q) + 1) if tokens[i:i+len(q)] == q), None)
                    at = round(unit['wordTimes'][found]['start'] * FPS) - start if found is not None else 0
                    at = min(end - start - 10, max(0, at))
                    at = max(at, cue_frames[-1] + 1 if cue_frames else 0)
                    if at < end - start:
                        cue_frames.append(at)
                row['cueFrames'] = cue_frames
            shots.append(row)
            evidence.append({'shot': sid, 'narrationUnit': unit['id'], 'narration': unit['text'],
                             'sourceId': asset['id'], 'rawInterval': [source_start, source_start + seconds],
                             'role': 'Illustrative contextual moving stock; not fictional Hanh or evidence of model amounts.',
                             'observed': asset['inspection'].get('observations'),
                             'source': asset.get('pageURL', asset.get('url')), 'pendingRenderedReview': True})
    result = {'fps': FPS, 'durationFrames': timeline['durationFrames'], 'title': timeline['title'],
              'audio': 'mix.wav', 'shots': shots}
    save(BATCH / 'edit-plan.json', result)
    save(BATCH / 'research/clause-footage-map.json', {'shots': evidence,
         'sourceIntervalsDoNotOverlap': True, 'subtitle': False, 'cartoonCast': False,
         'scope': 'All narration units mapped; final crop/editorial review remains separate.'})
    print('EDIT_PLAN', len(shots), 'shots;', sum(s['duration'] for s in shots if s['media'] == 'graphic') / FPS,
          'seconds of brief calculation overlays', flush=True)


def materialize():
    data = load(BATCH / 'edit-plan.json')
    assets = {a['id']: a for a in load(REGISTRY)['assets']}
    (PUBLIC / 'shots').mkdir(parents=True, exist_ok=True)
    for shot in data['shots']:
        output = PUBLIC / shot['file']
        receipt = output.with_suffix('.json')
        if output.exists() and receipt.exists():
            old = load(receipt)
            if old['shot'] != shot or old['sha256'] != sha(output):
                raise ValueError('Materialized shot differs: ' + shot['id'])
            continue
        source = BATCH / assets[shot['sourceId']]['file']
        # Crop once before browser rendering; original raw files are retained.
        filt = 'scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setsar=1,fps=30,format=yuv420p,setparams=range=tv:color_primaries=bt709:color_trc=bt709:colorspace=bt709'
        started = time.perf_counter()
        run([FF, '-y', '-v', 'error', '-ss', shot['rawStartSeconds'], '-i', source, '-an', '-vf', filt,
             '-frames:v', shot['duration'], '-c:v', 'libx264', '-preset', 'veryfast', '-threads', '3', '-crf', '20',
             '-profile:v', 'high', '-level', '4.1', '-color_range', 'tv', '-colorspace', 'bt709',
             '-color_primaries', 'bt709', '-color_trc', 'bt709', '-movflags', '+faststart', output])
        if decoded_frames(output) != shot['duration']:
            raise ValueError('Incomplete source interval ' + shot['id'])
        save(receipt, {'shot': shot, 'sha256': sha(output), 'wallSeconds': round(time.perf_counter() - started, 3)})
        print('SHOT_READY', shot['id'], flush=True)
    shutil.copy2(BATCH / 'audio/final-mix.wav', PUBLIC / 'mix.wav')


def bundle(revision='r01'):
    out = BATCH / revision
    out.mkdir(exist_ok=True)
    data = load(BATCH / 'edit-plan.json')
    paths = [ENTRY, Path(__file__), ROOT / 'workflows/reference-video/bread_documentary.py',
             ROOT / 'workflows/reference-video/bread_documentary_content.py', PROJECT / 'package-lock.json']
    paths += [p for p in (PROJECT / 'src/bread-documentary').rglob('*') if p.is_file()]
    deps = {'sources': {p.relative_to(ROOT).as_posix(): sha(p) for p in paths},
            'planSHA256': sha(BATCH / 'edit-plan.json'), 'mixSHA256': sha(PUBLIC / 'mix.wav'),
            'normalizedShots': {s['file']: sha(PUBLIC / s['file']) for s in data['shots']}}
    guard = out / 'dependencies.json'
    if guard.exists() and load(guard) != deps:
        raise ValueError('Frozen export changed: choose a new revision')
    save(guard, deps)
    save(out / 'props.json', {'plan': data})
    for path in paths:
        target = out / 'source-snapshot' / path.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists():
            shutil.copy2(path, target)
    if not (out / 'bundle/index.html').exists():
        elapsed = cli(['bundle', ENTRY, f'--out-dir={out / "bundle"}', f'--public-dir={PUBLIC}', '--log=error'], out / 'bundle.log')
        save(out / 'bundle-timing.json', {'wallSeconds': elapsed})
    return out


def render(revision='r01', proof=False):
    out = bundle(revision)
    data = load(out / 'props.json')['plan']
    dest = out / 'shots'
    dest.mkdir(exist_ok=True)
    chapters = []
    for shot in data['shots']:
        if shot['chapterId'] not in chapters:
            chapters.append(shot['chapterId'])
    chosen = [s for s in data['shots'] if s['narrationUnit'] in ['b01', 'b06', 'b18', 'b24']] if proof else data['shots']
    firsts = {next(s['id'] for s in data['shots'] if s['chapterId'] == ch) for ch in chapters}
    for shot in chosen:
        target = dest / (shot['id'] + '.mp4')
        receipt = target.with_suffix('.json')
        if target.exists() and receipt.exists() and load(receipt)['sha256'] == sha(target):
            continue
        started = time.perf_counter()
        if shot['media'] == 'graphic' or shot.get('headline') or shot.get('emphasis') or shot['id'] in firsts:
            props = out / (shot['id'] + '-props.json')
            save(props, {'plan': data, 'startFrame': shot['from'], 'frames': shot['duration']})
            cli(['render', out / 'bundle', 'BreadDocumentary', target, f'--props={props}',
                 '--codec=h264', '--crf=20', '--concurrency=3',
                 '--color-space=bt709', '--pixel-format=yuv420p', '--muted', '--log=info'], dest / (shot['id'] + '.log'))
        else:
            shutil.copy2(PUBLIC / shot['file'], target)
        count = decoded_frames(target)
        if count != shot['duration']:
            raise ValueError('Rendered shot incomplete ' + shot['id'])
        save(receipt, {'id': shot['id'], 'sha256': sha(target), 'decodedFrames': count,
                       'wallSeconds': round(time.perf_counter() - started, 3)})
        print('RENDERED', shot['id'], flush=True)
    if proof:
        groups = {uid: [s for s in chosen if s['narrationUnit'] == uid] for uid in ['b01', 'b06', 'b18', 'b24']}
        proof_dir = out / 'proof'
        proof_dir.mkdir(exist_ok=True)
        for uid, shots in groups.items():
            concat = proof_dir / (uid + '.txt')
            concat.write_text('\n'.join("file '" + (dest / (s['id'] + '.mp4')).resolve().as_posix() + "'" for s in shots), encoding='utf-8')
            run([FF, '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', concat,
                 '-ss', shots[0]['from'] / FPS, '-i', PUBLIC / 'mix.wav', '-map', '0:v:0', '-map', '1:a:0',
                 '-c:v', 'copy', '-c:a', 'aac', '-t', sum(s['duration'] for s in shots) / FPS,
                 '-movflags', '+faststart', proof_dir / (uid + '.mp4')])
        print('COMPLETE_SCENE_PROOFS_READY', flush=True)
        return
    concat = out / 'concat.txt'
    concat.write_text('\n'.join("file '" + (dest / (s['id'] + '.mp4')).resolve().as_posix() + "'" for s in data['shots']), encoding='utf-8')
    run([FF, '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', concat, '-i', PUBLIC / 'mix.wav',
         '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
         '-ar', '48000', '-ac', '2', '-t', data['durationFrames'] / FPS, '-movflags', '+faststart', out / 'final.mp4'])
    print('FILM_READY', out / 'final.mp4', flush=True)


def qa(revision='r01'):
    out = BATCH / revision
    data = load(out / 'props.json')['plan']
    final = out / 'final.mp4'
    count = decoded_frames(final)
    if count != data['durationFrames']:
        raise ValueError(f'Final decoded {count}, expected {data["durationFrames"]}')
    dest = out / 'qa'
    dest.mkdir(exist_ok=True)
    capture = cv2.VideoCapture(str(final))
    frames = []
    for shot in data['shots']:
        for suffix, frac in [('early', .12), ('middle', .5), ('late', .88)]:
            frame = shot['from'] + min(shot['duration'] - 1, round(shot['duration'] * frac))
            capture.set(cv2.CAP_PROP_POS_FRAMES, frame)
            ok, image = capture.read()
            if not ok:
                raise ValueError('Unreadable final frame')
            path = dest / f'{shot["id"]}-{suffix}.jpg'
            cv2.imwrite(str(path), image)
            frames.append({'shot': shot['id'], 'frame': frame, 'file': path.name})
    capture.release()
    sheets(dest, sorted(dest.glob('*.jpg')), 'contact')
    run([FF, '-y', '-v', 'error', '-i', final, '-map', '0:a:0', '-ac', '1', '-ar', '48000', '-f', 's16le', dest / 'decoded-audio.pcm'])
    audio_seconds = (dest / 'decoded-audio.pcm').stat().st_size / 96000
    last_word = load(BATCH / 'timeline.json')['words'][-1]['end']
    if audio_seconds < last_word or abs(audio_seconds - count / FPS) > .1:
        raise ValueError('Truncated speech/audio duration mismatch')
    measured = run([FF, '-hide_banner', '-i', final, '-af', 'ebur128=peak=true', '-f', 'null', '-']).stderr.decode(errors='replace')
    (dest / 'loudness.txt').write_text(measured[-2000:], encoding='utf-8')
    save(out / 'qa-report.json', {'technical': 'passed', 'file': final.relative_to(ROOT).as_posix(),
         'sha256': sha(final), 'decodedFrames': count, 'seconds': count / FPS,
         'audioSeconds': audio_seconds, 'lastWordEnd': last_word, 'shotCount': len(data['shots']),
         'sourceCount': len({s['sourceId'] for s in data['shots']}),
         'realMovingFootageBackgroundSeconds': count / FPS,
         'calculationOverlaySeconds': sum(s['duration'] for s in data['shots'] if s['media'] == 'graphic') / FPS,
         'subtitles': False, 'cartoonCast': False, 'speechSpeed': 1, 'frames': frames,
         'continuousAVReview': False, 'manualAudioListening': False, 'userApproval': 'pending',
         'limits': 'Technical decode, measured sound and sampled-frame reviews do not establish full audiovisual or user approval.'})
    print('QA_READY', count, count / FPS, flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('phase', choices=['plan', 'materialize', 'bundle', 'proof', 'render', 'qa'])
    parser.add_argument('--revision', default='r01')
    args = parser.parse_args()
    if args.phase in ['plan', 'materialize']:
        globals()[args.phase]()
    elif args.phase == 'proof':
        render(args.revision, True)
    else:
        globals()[args.phase](args.revision)
