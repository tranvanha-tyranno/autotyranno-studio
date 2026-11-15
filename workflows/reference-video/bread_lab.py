"""Upgrade real bread footage with connected simulations and downloaded Foley.

Can build an explicitly provisional visual preview while OpenAI credentials are
blocked. That preview never claims to contain an OpenAI voice. Each new voice
gets its own exact timeline, mix, plan and immutable output revision.
"""
from __future__ import annotations

import argparse
from collections import Counter
import math
from pathlib import Path
import shutil
import time
import wave

import cv2
import numpy as np

import bread_documentary as base
from bread_openai_voice import BATCH, SOURCE, ROOT, read as load, save, sha
from documentary import FF, duration
from finance_long_render import cli, decoded_frames, sheets

PROJECT = ROOT / 'workflows/reference-video/cinematic'
ENTRY = PROJECT / 'src/bread-lab-entry.tsx'
FPS = 30
PUBLIC = BATCH / 'preview-public'

# A unit has one explanatory job; several states develop inside each simulation.
SIMULATIONS = {
    'b03': ('money_split', {'stage': 'before'}, ['hai mươi nghìn', 'mười hai nghìn', 'năm nghìn', 'ba nghìn']),
    'b04': ('cost_ledger', {'stage': 'not_net_profit'}, ['chưa tính đủ', 'thuế', 'khấu hao', 'công']),
    'b05': ('money_split', {'stage': 'after'}, ['mười bốn nghìn năm trăm', 'hai mươi hai nghìn', 'hai nghìn năm trăm']),
    'b06': ('money_split', {'stage': 'compare'}, ['hai nghìn năm trăm', 'chi phí tăng', 'giá bán đi lên']),
    'b08': ('price_level', {}, ['hai mươi hai nghìn là', 'hai mươi hai nghìn bốn trăm', 'trong phép tính']),
    'b11': ('cost_ledger', {'stage': 'question'}, ['bao bột', 'tiền thuê', 'tiền điện', 'bột mua cho mẻ bánh']),
    'b12': ('inventory', {}, ['lô mua trước', 'hóa đơn mới thấp hơn', 'mẻ bánh hôm nay', 'độ trễ']),
    'b13': ('cost_ledger', {}, ['tiền thuê', 'lương người phụ bán', 'điện', 'một dòng giảm']),
    'b14': ('cost_ledger', {'stage': 'counterexample'}, ['tổng chi phí đã giảm', 'giữ giá', 'khoảng dư có thể tăng', 'không có quy luật']),
    'b15': ('competition', {}, ['bên cạnh', 'cân nhắc mất khách', 'khó chuyển chỗ mua', 'lựa chọn và cạnh tranh']),
    'b17': ('bread_power', {'stage': 'income'}, ['hai mươi lên hai mươi hai nghìn', 'từ mười triệu', 'mười triệu rưỡi', 'giá bữa sáng đã tăng nhanh hơn lương']),
    'b18': ('bread_power', {'stage': 'quantity'}, ['năm trăm ổ', 'bốn trăm bảy mươi bảy', 'không ai cần', 'phép so chỉ hỏi']),
    'b19': ('bread_power', {'stage': 'result'}, ['bốn phẩy năm phần trăm', 'vẫn chiếc bánh', 'quầy bán', 'người làm công']),
    'b20': ('basket_scope', {}, ['không chỉ có bánh mì', 'tiền nhà', 'giỏ chi tiêu', 'không phải chiếc máy']),
    'b21': ('basket_scope', {'stage': 'households'}, ['khoản anh mua nhiều', 'nhà khác chi tiêu khác', 'cảm giác thiếu tiền', 'không bảo đảm']),
    'b22': ('synthesis', {}, ['khách trả thêm', 'tin lạm phát giảm', 'lương tăng', 'ba điều ấy']),
}

OVERLAYS = {
    'b01': {'title': 'Khách trả thêm 2.000đ · Tiệm còn ít hơn 500đ', 'items': ['Lạm phát giảm. Sao cả hai vẫn thấy khó hơn?']},
    'b02': {'title': 'Theo dấu tiền của một ổ bánh', 'items': ['Bảng giá của khách', 'Hóa đơn đầu vào của tiệm', 'Thu nhập của người mua']},
    'b07': {'title': 'Vì sao bảng giá chưa về 20.000đ?', 'items': ['Tiệm khác có thể có kết quả khác', 'Cần chi phí và lượng bán thực tế']},
    'b10': {'title': 'Một ổ bánh chưa phải lạm phát cả nước', 'items': ['CPI nhìn nhiều hàng hóa và dịch vụ', 'Giữ cùng lượng và chất lượng khi so']},
    'b09': {'title': 'Tỷ lệ giảm từ 10% xuống 2% · Giá vẫn tăng', 'items': ['20.000đ → 22.000đ → 22.440đ', 'Giảm tốc tăng khác với giảm giá']},
    'b16': {'title': 'Đừng nhìn riêng một hóa đơn', 'items': ['Tổng chi phí đã đổi bao nhiêu?', 'Khách có thể mua ở đâu khác?', 'Thu nhập của người mua đổi ra sao?']},
    'b23': {'title': 'Ba câu hỏi khi nghe tin lạm phát giảm', 'items': ['Giá giảm hay chỉ tăng chậm hơn?', 'So với thời điểm nào?', 'Thu nhập có theo kịp giỏ mình mua?']},
    'b24': {'title': 'Bữa sáng của bạn đã đổi thế nào?', 'items': ['Món gì? So với năm nào?', 'Bình luận · Đăng ký · Bật chuông']},
}


def prepare_preview():
    """Keep original take and timing while producing reviewable visual changes."""
    BATCH.mkdir(parents=True, exist_ok=True)
    for name in ['timeline.json', 'script.txt', 'content.json', 'editorial-map.json']:
        target = BATCH / name
        if not target.exists():
            shutil.copy2(SOURCE / name, target)
    (BATCH / 'audio').mkdir(exist_ok=True)
    target = BATCH / 'audio/narration-provisional.wav'
    if not target.exists():
        shutil.copy2(SOURCE / 'audio/narration.wav', target)
    save(BATCH / 'voice-state.json', {'status': 'OpenAI blocked; visual preview uses retained Nam Minh take',
         'voice': 'vi-VN-NamMinhNeural', 'provisional': True, 'openaiVoiceProduced': False,
         'blocker': 'Two supplied project keys returned401 invalid_api_key; no successful OpenAI audio generated.',
         'originalSource': (SOURCE / 'audio/narration.wav').relative_to(ROOT).as_posix(), 'sha256': sha(target)})


def normalized(value):
    import re
    return re.sub(r'[^\w]', '', value.casefold())


def cues(unit, phrases):
    words = unit['wordTimes']
    tokens = [normalized(w['text']) for w in words]
    result = []
    for phrase in phrases:
        query = [normalized(w) for w in phrase.split()]
        found = next((i for i in range(len(tokens)-len(query)+1) if tokens[i:i+len(query)] == query), None)
        if found is None:
            raise ValueError('Missing exact phrase: ' + unit['id'] + ': ' + phrase)
        frame = round(words[found]['start'] * FPS) - unit['from']
        # Leave the reveal readable. This is a visual emphasis window; actual
        # spoken cue and clipped display cue are retained separately in the map.
        frame = max(0, min(unit['duration'] - 25, frame))
        if result and frame <= result[-1]:
            raise ValueError('Cue phrases are not in actual spoken order: ' + unit['id'])
        result.append(frame)
    return result


def plan():
    prepare_preview()
    data = load(BATCH / 'timeline.json')
    old = load(SOURCE / 'edit-plan.json')
    old_by_unit = {}
    for shot in old['shots']:
        old_by_unit.setdefault(shot['narrationUnit'], []).append(shot)
    (PUBLIC / 'footage').mkdir(parents=True, exist_ok=True)
    shots, registry = [], []
    for unit in data['units']:
        key = unit['id']
        if key in SIMULATIONS:
            simulation, state, phrases = SIMULATIONS[key]
            starts = cues(unit, phrases)
            length = min(unit['duration'], 8*FPS) if key in ['b04', 'b19'] else unit['duration']
            starts = [x for x in starts if x < length-25]
            # These two passages have already explained the relation; clear
            # their retained result back to relevant real action after8seconds.
            # Rendering uses the same exact source/take timing, no audio change.
            # Keep the opening/action/last CTA in real footage; major economic
            # explanations have complete meaningful processes rather than text.
            row = {'id': key, 'from': unit['from'], 'duration': length,
                   'chapterId': unit['chapterId'], 'chapterTitle': unit['chapterTitle'],
                   'media': 'simulation', 'simulation': simulation, 'data': state,
                   'cueFrames': starts, 'sourceStartSeconds': 0, 'narrationUnit': key,
                   'label': 'VÍ DỤ MINH HỌA'}
            if unit.get('headline'):
                row['headline'] = unit['headline']
            shots.append(row)
            registry.append({'unit': key, 'simulation': simulation, 'narration': unit['text'],
                             'exactCuePhrases': phrases, 'cueFrames': starts,
                             'role': 'Original explanatory simulation; all numeric amounts illustrative.'})
            if length < unit['duration']:
                for old_shot in old_by_unit[key]:
                    a = max(unit['from']+length, old_shot['from'])
                    b = min(unit['from']+unit['duration'], old_shot['from']+old_shot['duration'])
                    if b <= a:
                        continue
                    raw = SOURCE / 'render-public-v4' / old_shot['file']
                    target = PUBLIC / 'footage' / raw.name
                    if not target.exists():
                        shutil.copy2(raw, target)
                    part = {**old_shot, 'id': key+'-tail-'+old_shot['id'], 'from': a, 'duration': b-a,
                            'file': 'footage/'+raw.name, 'sourceStartSeconds': (a-old_shot['from'])/FPS,
                            'media': 'video', 'narrationUnit': key}
                    for optional in ['kind','data','headline','emphasis','cueFrames']:
                        part.pop(optional, None)
                    shots.append(part)
        else:
            # Copy retained exact source derivatives, not rejected film pictures
            # with old titles baked in. No footage stretching or looping.
            for index, shot in enumerate(old_by_unit[key]):
                raw = SOURCE / 'render-public-v4' / shot['file']
                target = PUBLIC / 'footage' / raw.name
                if not target.exists():
                    shutil.copy2(raw, target)
                row = {**shot, 'file': 'footage/' + raw.name, 'sourceStartSeconds': 0,
                       'media': 'video', 'narrationUnit': key}
                row.pop('headline', None)
                row.pop('emphasis', None)
                if index == 0:
                    row['overlay'] = OVERLAYS[key]
                shots.append(row)
                registry.append({'unit': key, 'shot': shot['id'], 'sourceId': shot['sourceId'],
                                 'sourceInterval': [shot['rawStartSeconds'], shot['rawStartSeconds']+shot['duration']/FPS],
                                 'fileSHA256': sha(raw), 'narration': unit['text'], 'role': 'Retained licensed illustrative real footage.'})
    expected = 0
    for shot in shots:
        if shot['from'] != expected:
            raise ValueError('Visual preview timeline gap/overlap: ' + shot['id'])
        expected += shot['duration']
    if expected != data['durationFrames']:
        raise ValueError('Visual preview does not cover complete narration')
    save(BATCH / 'lab-plan.json', {'fps': FPS, 'durationFrames': data['durationFrames'],
         'title': data['title'], 'audio': 'mix.wav', 'shots': shots, 'provisionalVoice': True})
    save(BATCH / 'research/simulation-applied-map.json', {'shots': registry,
         'voice': 'Retained Nam Minh pending a working OpenAI key', 'notOpenAIAudio': True})
    print('LAB_PLAN', len(shots), 'shots', len(SIMULATIONS), 'simulation passages', flush=True)


def mix():
    prepare_preview()
    timeline = load(BATCH / 'timeline.json')
    seconds = timeline['durationFrames'] / FPS
    rate = 48000
    assets = {a['id']: a for a in load(BATCH / 'research/sfx-sources.json')['assets']}
    # Source trims are chosen at short energy onsets, not random file starts.
    # No claim that waveform selection constitutes human auditory review.
    score = SOURCE / 'audio/music-bed.wav'
    shutil.copy2(score, BATCH / 'audio/music-bed-retained.wav')
    events = [
        ('b01', 'bread-bag-drop', .0, 1.0), ('b02', 'paper-bag', .2, 1.1),
        ('b03', 'coins-drop', .3, .8), ('b03', 'calculator', 5.4, .55),
        ('b04', 'pen-paper', .4, 1.5), ('b05', 'calculator', .25, .9),
        ('b05', 'coins-drop', 8.5, .8), ('b06', 'money-pickup', .2, .8),
        ('b07', 'short-whoosh', .05, .32), ('b08', 'calculator-slide', .3, .75),
        ('b09', 'calculator', .2, .45), ('b10', 'paper-bag', .5, .8),
        ('b11', 'pen-paper', .2, .9), ('b12', 'oven-door', .1, .9),
        ('b12', 'paper-bag', 5.2, 1.0), ('b13', 'receipt-printer', .1, 1.7),
        ('b14', 'calculator', .3, .8), ('b15', 'short-whoosh', .1, .34),
        ('b15', 'money-pickup', 5.0, .8), ('b16', 'receipt-printer', .1, 1.1),
        ('b17', 'calculator-slide', .4, .7), ('b18', 'bread-cut', .1, .65),
        ('b18', 'coins-drop', 7.0, .8), ('b19', 'bread-crunch', .2, .55),
        ('b20', 'paper-bag', .3, .9), ('b21', 'pen-paper', .2, .85),
        ('b22', 'oven-close', .15, 1.2), ('b23', 'calculator', .1, .65),
        ('b24', 'bread-bag-drop', .15, .8),
    ]
    units = {u['id']: u for u in timeline['units']}
    audio = np.zeros((math.ceil(seconds*rate), 2), dtype=np.float32)
    receipts = []
    cached = {}
    for uid, asset_id, offset, wanted in events:
        if asset_id not in assets:
            continue
        asset = assets[asset_id]
        source = BATCH / asset['file']
        if sha(source) != asset['sha256']:
            raise ValueError('Downloaded Foley changed: ' + asset_id)
        if asset_id not in cached:
            raw = base.run([FF, '-v', 'error', '-i', source, '-ar', rate, '-ac', '1', '-f', 'f32le', '-']).stdout
            pcm = np.frombuffer(raw, dtype='<f4').copy()
            window = max(1, int(.025*rate))
            energy = np.array([np.mean(pcm[i:i+window]**2) for i in range(0, len(pcm), window)])
            # First meaningful onset at >=14% of the asset's maximum energy.
            found = np.flatnonzero(energy >= max(1e-8, energy.max()*.14))
            onset = max(0, int(found[0]*window)-int(.03*rate)) if len(found) else 0
            cached[asset_id] = (pcm, onset)
        pcm, start = cached[asset_id]
        count = min(round(wanted*rate), len(pcm)-start)
        part = pcm[start:start+count].copy()
        peak = max(.00001, float(np.max(np.abs(part))))
        rms = max(.00001, float(np.sqrt(np.mean(part**2))))
        target_db = -31 if asset_id not in ['short-whoosh','receipt-printer'] else -34
        gain = min(10**(target_db/20)/rms, .11/peak)
        part *= gain
        fade = min(len(part)//3, round(.025*rate))
        part[:fade] *= np.linspace(0,1,fade)
        part[-fade:] *= np.linspace(1,0,fade)
        at = round((units[uid]['from']/FPS+offset)*rate)
        until = min(at+len(part), len(audio))
        pan = .12 if len(receipts)%2 else -.12
        audio[at:until, 0] += part[:until-at]*(1-pan)
        audio[at:until, 1] += part[:until-at]*(1+pan)
        receipts.append({'unit': uid, 'asset': asset_id, 'atSeconds': at/rate,
                         'sourceInterval': [start/rate,(start+count)/rate], 'sourceSHA256': asset['sha256'],
                         'sourceURL': asset['sourceURL'], 'license': asset['license'],
                         'selection': 'source description + decoded energy onset; not auditory audition',
                         'targetRmsDbFS': target_db, 'peakLimitDbFS': -19.17})
    raw_file = BATCH / 'audio/downloaded-foley.f32'
    audio.tofile(raw_file)
    base.run([FF, '-y', '-v', 'error', '-f', 'f32le', '-ar', rate, '-ac', '2', '-i', raw_file,
              '-c:a', 'pcm_s16le', BATCH / 'audio/downloaded-foley.wav'])
    raw_file.unlink()
    # Don't use the source market bed: intelligible foreign conversation is
    # disclosed in its source description. No alarms at arbitrary chapter cuts.
    graph = ('[0:a]highpass=f=65,loudnorm=I=-16:TP=-2:LRA=10,asplit=2[v][key];'
             '[1:a][key]sidechaincompress=threshold=0.025:ratio=4:attack=15:release=220[m];'
             '[v][m][2:a]amix=inputs=3:normalize=0,alimiter=limit=0.89:level=false,'
             f'apad=whole_dur={seconds}[out]')
    base.run([FF, '-y', '-v', 'error', '-i', BATCH / 'audio/narration-provisional.wav',
              '-i', score, '-i', BATCH / 'audio/downloaded-foley.wav', '-filter_complex', graph,
              '-map', '[out]', '-t', seconds, '-ar', rate, '-ac', '2', BATCH / 'audio/final-mix.wav'])
    save(BATCH / 'audio/sfx-cue-map.json', {'cues': receipts, 'downloadedTypesUsed': sorted({r['asset'] for r in receipts}),
         'downloadedSourceCount': len(assets), 'musicSHA256': sha(score), 'mixSHA256': sha(BATCH / 'audio/final-mix.wav'),
         'voiceProvisional': True, 'voice': 'Retained Nam Minh; OpenAI401 invalid_api_key',
         'excludedFromMix': ['market-room has foreign conversation', 'oven-beeps irrelevant alarm', 'bread-cooling may include fan/clothing'],
         'manualListening': False, 'noNewPaidMusicSfx': True})
    print('DOWNLOADED_FOLEY_MIX_READY', len(receipts), 'cues', len({r['asset'] for r in receipts}), 'types', flush=True)


def bundle(revision):
    out = BATCH / revision
    out.mkdir(exist_ok=True)
    data = load(BATCH / 'lab-plan.json')
    shutil.copy2(BATCH / 'audio/final-mix.wav', PUBLIC / 'mix.wav')
    paths = [ENTRY, Path(__file__), PROJECT / 'package-lock.json']
    paths += [p for p in (PROJECT / 'src/bread-lab').rglob('*') if p.is_file()]
    dependencies = {'sources': {p.relative_to(ROOT).as_posix(): sha(p) for p in paths},
                    'planSHA256': sha(BATCH / 'lab-plan.json'), 'mixSHA256': sha(PUBLIC / 'mix.wav')}
    guard = out / 'dependencies.json'
    if guard.exists() and load(guard) != dependencies:
        raise ValueError('Frozen upgrade sources changed; use a new revision')
    save(guard, dependencies)
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


def render(revision, proof=False):
    out = bundle(revision)
    data = load(out / 'props.json')['plan']
    dest = out / 'shots'
    dest.mkdir(exist_ok=True)
    chosen = [s for s in data['shots'] if s.get('narrationUnit') in ['b05', 'b12', 'b18']] if proof else data['shots']
    for shot in chosen:
        target = dest / (shot['id'] + '.mp4')
        receipt = target.with_suffix('.json')
        if target.exists() and receipt.exists() and load(receipt)['sha256'] == sha(target):
            continue
        started = time.perf_counter()
        props = out / (shot['id'] + '-props.json')
        save(props, {'plan': data, 'startFrame': shot['from'], 'frames': shot['duration']})
        raw = target.with_suffix('.remotion.mp4')
        cli(['render', out / 'bundle', 'BreadLab', raw, f'--props={props}', '--codec=h264',
             '--crf=20', '--concurrency=3', '--color-space=bt709', '--pixel-format=yuv420p',
             '--muted', '--log=info'], target.with_suffix('.log'))
        base.run([FF, '-y', '-v', 'error', '-i', raw, '-an', '-c:v', 'copy',
                  '-video_track_timescale', '15360', '-movflags', '+faststart', target])
        count = decoded_frames(target)
        if count != shot['duration']:
            raise ValueError('Incomplete rendered upgrade scene')
        save(receipt, {'id': shot['id'], 'sha256': sha(target), 'frames': count,
                       'wallSeconds': round(time.perf_counter()-started, 3)})
        print('LAB_RENDERED', shot['id'], flush=True)
    if proof:
        proof_dir = out / 'proof'
        proof_dir.mkdir(exist_ok=True)
        for shot in chosen:
            target = proof_dir / (shot['id'] + '.mp4')
            base.run([FF, '-y', '-v', 'error', '-i', dest / (shot['id'] + '.mp4'),
                 '-ss', shot['from']/FPS, '-i', PUBLIC / 'mix.wav', '-map', '0:v:0', '-map', '1:a:0',
                 '-c:v', 'copy', '-c:a', 'aac', '-t', shot['duration']/FPS, '-movflags', '+faststart', target])
        return
    listing = out / 'concat.txt'
    listing.write_text('\n'.join("file '" + (dest / (s['id']+'.mp4')).resolve().as_posix() + "'" for s in data['shots']), encoding='utf-8')
    base.run([FF, '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', listing, '-i', PUBLIC / 'mix.wav',
              '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
              '-ar', '48000', '-ac', '2', '-t', data['durationFrames']/FPS, '-movflags', '+faststart', out / 'visual-preview.mp4'])
    print('VISUAL_PREVIEW_READY', flush=True)


def qa(revision):
    out = BATCH / revision
    plan = load(out / 'props.json')['plan']
    final = out / 'visual-preview.mp4'
    count = decoded_frames(final)
    if count != plan['durationFrames']:
        raise ValueError('Incomplete full simulation preview')
    dest = out / 'qa'
    dest.mkdir(exist_ok=True)
    cap = cv2.VideoCapture(str(final))
    samples = []
    for shot in plan['shots']:
        for n, fraction in enumerate([.15, .5, .88]):
            frame = min(count-1, shot['from']+round(shot['duration']*fraction))
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame)
            ok, im = cap.read()
            if not ok:
                raise ValueError('Unreadable upgrade sample')
            target = dest / f'{shot["id"]}-{n}.jpg'
            cv2.imwrite(str(target), im)
            samples.append({'id': shot['id'], 'frame': frame, 'file': target.name})
    cap.release()
    sheets(dest, sorted(dest.glob('*.jpg')), 'contact')
    save(out / 'qa-report.json', {'technical': 'passed', 'frames': count, 'seconds': count/FPS,
         'sha256': sha(final), 'samples': samples, 'simulationPassages': len(SIMULATIONS),
         'simulationFamilies': sorted(set(s['simulation'] for s in plan['shots'] if s.get('simulation'))),
         'voice': 'Retained Nam Minh; OpenAI invalid_api_key blocker unresolved',
         'openaiNarrationProduced': False, 'visualPreviewOnly': True, 'userApproval': 'pending',
         'continuousAVReview': False, 'manualAudioListening': False})


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('phase', choices=['prepare', 'plan', 'mix', 'bundle', 'proof', 'render', 'qa'])
    parser.add_argument('--revision', default='r01')
    args = parser.parse_args()
    if args.phase == 'prepare':
        prepare_preview()
    elif args.phase == 'plan':
        plan()
    elif args.phase == 'mix':
        mix()
    elif args.phase == 'proof':
        render(args.revision, True)
    else:
        globals()[args.phase](args.revision)
