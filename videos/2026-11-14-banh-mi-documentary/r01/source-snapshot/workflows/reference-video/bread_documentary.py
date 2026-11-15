"""Footage-led bread documentary: exact new speech, short Remotion explanations.

Only `voice` can purchase narration. Editing uses FFmpeg for clean real footage
and Remotion for the short calculation/argument shots, with identical timing.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import shutil
import subprocess
import time
import wave

import cv2
import numpy as np

import eleven_audio
import editorial_gate
from documentary import FF, duration
from finance_long_render import cli, decoded_frames, sheets

ROOT = Path(__file__).resolve().parents[2]
PROJECT = Path(__file__).parent / 'cinematic'
BATCH = ROOT / 'videos/2026-11-14-banh-mi-documentary'
FPS = 30
VOICE = '6adFm46eyy74snVn6YrT'
FONT = PROJECT / 'src/economy-story/fonts/BeVietnamPro-Bold.ttf'


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def save(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def run(args):
    result = subprocess.run(list(map(str, args)), capture_output=True)
    if result.returncode:
        raise RuntimeError(result.stderr.decode(errors='replace')[-2500:])
    return result


def prepare():
    from bread_documentary_content import CONTENT
    BATCH.mkdir(parents=True, exist_ok=True)
    content = json.loads(json.dumps(CONTENT, ensure_ascii=False))
    frozen = BATCH / 'content.json'
    if frozen.exists() and load(frozen) != content:
        raise ValueError('Content already frozen; use a new batch')
    save(frozen, content)
    units = [u for c in content['chapters'] for u in c['units']]
    (BATCH / 'script.txt').write_text('\n\n'.join(u['text'] for u in units), encoding='utf-8')
    takes = []
    for i, chapter in enumerate(content['chapters']):
        text = '\n\n'.join(u['text'] for u in chapter['units'])
        takes.append({'chapter': chapter['id'], 'file': f'audio/{i + 1:02}-{chapter["id"]}.mp3',
                      'endpoint': f'/v1/text-to-speech/{VOICE}/with-timestamps',
                      'payload': {'text': text, 'model_id': 'eleven_v3', 'language_code': 'vi',
                                  'voice_settings': {'stability': .5, 'similarity_boost': .8, 'speed': 1.0}}})
    save(BATCH / 'generation-plan.json', {'chapterTakes': takes, 'newVisualMusicCalls': 0,
         'delivery': 'New concise spoken script, questions and contrast punctuation; natural speed, no atempo.',
         'acceptance': 'New voice still requires listening and user feedback.'})
    document = {'schema': editorial_gate.SCHEMA, 'title': content['title'],
                'structurePolicy': 'no-spoken-disclaimer-user-requested',
                'centralQuestion': content['centralQuestion'], 'thesis': content['thesis'],
                'viewerStake': 'Bản tin giá hạ nhiệt nhưng bữa sáng vẫn nặng tiền với khách lẫn tiệm.',
                'hookPromise': 'Theo một tiệm qua bảng giá, hóa đơn và sức mua để giải nghịch lý.',
                'exclusions': ['Chương chính sách lãi suất', 'Kỳ vọng lạm phát độc lập', 'Mô hình giỏ 100 phần',
                               'Ví dụ shrinkflation', 'Nhân vật hoạt hình', 'Subtitle'],
                'units': [{'id': u['id'], 'phase': u.get('phase', 'content'), 'text': u['text']} for u in units],
                'chapters': [],
                'payoff': {'answer': content['thesis'], 'unitIds': ['b22', 'b23']},
                'review': {'status': 'revision_needed'}}
    for chapter in content['chapters']:
        actual = [u for u in chapter['units'] if u.get('phase', 'content') == 'content']
        highlighted = next((u for u in actual if u.get('emphasis')), actual[-1])
        row = {'id': chapter['id'], 'title': chapter['title'], 'unitIds': [u['id'] for u in actual],
               'question': chapter['question'], 'answer': chapter['answer'], 'mechanism': chapter['mechanism'],
               'whyItMatters': 'Nối vấn đề của cùng tiệm và người mua, thêm một phân biệt cần thiết.',
               'takeaway': chapter['takeaway'],
               'evidenceExamples': [{'kind': 'illustrative', 'detail': chapter['example']}],
               'emphasis': {'spokenQuote': highlighted['text'], 'visualFocus': highlighted.get('emphasis', chapter['takeaway']),
                            'purpose': 'Làm rõ quan hệ của chương bằng một điểm nhấn trên footage.'}}
        if chapter.get('nextQuestion'):
            row['bridge'] = {'reason': chapter['bridgeReason'], 'nextQuestion': chapter['nextQuestion']}
        document['chapters'].append(row)
    map_path = BATCH / 'editorial-map.json'
    if not map_path.exists():
        save(map_path, document)
    elif editorial_gate.content_hash(load(map_path)) != editorial_gate.content_hash(document):
        raise ValueError('Editorial map differs from the frozen source')
    print('PREPARED', len(units), 'units', sum(len(u['text'].split()) for u in units), 'word units', flush=True)


def voice():
    prepare()
    records = []
    for row in load(BATCH / 'generation-plan.json')['chapterTakes']:
        target = BATCH / row['file']
        before = target.exists()
        start = time.perf_counter()
        eleven_audio.generate(target, row['endpoint'], row['payload'], timed=True)
        receipt = load(target.with_suffix('.receipt.json'))
        records.append({'chapter': row['chapter'], 'file': row['file'], 'sha256': sha(target),
                        'wallSeconds': round(time.perf_counter() - start, 3), 'existedBeforeRun': before,
                        'providerCharacterCost': receipt.get('character_cost'), 'seconds': duration(target)})
        save(BATCH / 'audio/voice-runs.json', {'voice': 'Nhật Phong', 'voiceID': VOICE,
             'model': 'eleven_v3', 'naturalSpeed': 1, 'chapters': records,
             'accounting': 'Provider character cost units, not a USD invoice.'})
        print('VOICE_READY', row['chapter'], records[-1]['seconds'], flush=True)


def timeline():
    content = load(BATCH / 'content.json')
    active = BATCH / 'active-generation-plan.json'
    requests = load(active if active.exists() else BATCH / 'generation-plan.json')['chapterTakes']
    cursor = 0
    samples = []
    units, words, chapters = [], [], []
    rate = 48000
    for chapter, request in zip(content['chapters'], requests):
        source = BATCH / request['file']
        aligned = load(source.with_suffix('.alignment.json'))
        original = ''.join(aligned['characters'])
        if original != request['payload']['text']:
            raise ValueError('Alignment differs from exact requested script ' + chapter['id'])
        if sha(source) != load(source.with_suffix('.receipt.json'))['sha256']:
            raise ValueError('Audio source changed')
        wav = source.with_suffix('.wav')
        run([FF, '-y', '-v', 'error', '-i', source, '-ac', '1', '-ar', rate, '-c:a', 'pcm_s16le', wav])
        with wave.open(str(wav), 'rb') as stream:
            raw = stream.readframes(stream.getnframes())
        offset = cursor / rate
        chapters.append({'id': chapter['id'], 'title': chapter['title'], 'from': round(offset * FPS),
                         'seconds': len(raw) / 2 / rate, 'sourceSHA256': sha(source)})
        pos = 0
        for unit in chapter['units']:
            end = pos + len(unit['text'])
            start_time = aligned['character_start_times_seconds'][pos] + offset
            end_time = aligned['character_end_times_seconds'][end - 1] + offset
            local_words = eleven_audio.words({k: v[pos:end] for k, v in aligned.items() if isinstance(v, list)})
            units.append({**unit, 'from': round(start_time * FPS), 'speechEnd': math.ceil(end_time * FPS),
                          'chapterId': chapter['id'], 'chapterTitle': chapter['title'],
                          'wordTimes': [{**w, 'start': w['start'] + offset, 'end': w['end'] + offset} for w in local_words]})
            pos = end + 2
        words.extend([{**w, 'start': w['start'] + offset, 'end': w['end'] + offset}
                      for w in eleven_audio.words(aligned)])
        samples.append(raw)
        cursor += len(raw) // 2
        if chapter != content['chapters'][-1]:
            # 160ms breath between complete chapter takes, not the old long gaps.
            gap = b'\0\0' * round(.16 * rate)
            samples.append(gap)
            cursor += len(gap) // 2
    frames = math.ceil((cursor / rate + 1.1) * FPS)
    units[0]['from'] = 0
    for i, unit in enumerate(units):
        unit['duration'] = (units[i + 1]['from'] if i + 1 < len(units) else frames) - unit['from']
    with wave.open(str(BATCH / 'audio/narration.wav'), 'wb') as output:
        output.setparams((1, 2, rate, 0, 'NONE', 'not compressed'))
        for part in samples:
            output.writeframes(part)
        output.writeframes(b'\0\0' * max(0, math.ceil(frames / FPS * rate) - cursor))
    save(BATCH / 'timeline.json', {'fps': FPS, 'durationFrames': frames, 'title': content['title'],
         'units': units, 'words': words, 'chapters': chapters, 'subtitle': False, 'voiceSpeed': 1,
         'voice': load(active).get('voice') if active.exists() else 'Nhật Phong',
         'timingMethod': 'Exact words from selected provider take; see per-take receipt for word/character method.'})
    print('TIMELINE', frames, round(frames / FPS, 2), 'seconds', flush=True)


def mix():
    data = load(BATCH / 'timeline.json')
    seconds = data['durationFrames'] / FPS
    sound_dir = ROOT / 'videos/2026-11-13-quan-dong-khach-het-tien/audio'
    music_names = ['coffee-opening', 'precise-unit-math', 'cash-tension', 'operating-pulse', 'hopeful-outro']
    blocks, receipts = [], []
    for i, (chapter, name) in enumerate(zip(data['chapters'], music_names)):
        source = sound_dir / 'music' / (name + '.mp3')
        receipt = load(source.with_suffix('.receipt.json'))
        if sha(source) != receipt['sha256']:
            raise ValueError('Music source changed')
        start = chapter['from'] / FPS
        end = data['chapters'][i + 1]['from'] / FPS if i + 1 < len(data['chapters']) else seconds
        length = end - start
        if length > duration(source):
            raise ValueError('Music too short: no looping')
        target = BATCH / 'audio/music' / (name + '.wav')
        target.parent.mkdir(parents=True, exist_ok=True)
        run([FF, '-y', '-v', 'error', '-i', source, '-t', length, '-af',
             f'loudnorm=I=-29:TP=-7:LRA=9,afade=t=in:d=0.6,afade=t=out:st={max(0,length-.8)}:d=0.8',
             '-ar', '48000', '-ac', '2', target])
        blocks.append(target)
        receipts.append({'source': source.relative_to(ROOT).as_posix(), 'sha256': sha(source),
                         'start': start, 'end': end, 'sourceInterval': [0, length]})
    listing = BATCH / 'audio/music-concat.txt'
    listing.write_text('\n'.join("file '" + p.resolve().as_posix() + "'" for p in blocks), encoding='utf-8')
    run([FF, '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', listing, '-t', seconds,
         '-ar', '48000', '-ac', '2', BATCH / 'audio/music-bed.wav'])
    cue_audio = np.zeros((math.ceil(seconds * 48000), 2), dtype=np.float32)
    cues = []
    cue_map = {'b04': 'paper-pen', 'b06': 'low-hit', 'b09': 'low-hit', 'b13': 'paper-pen',
               'b18': 'low-hit', 'b22': 'low-hit'}
    for unit in data['units']:
        if unit['id'] not in cue_map:
            continue
        name = cue_map[unit['id']]
        source = sound_dir / 'sfx' / (name + '.mp3')
        if sha(source) != load(source.with_suffix('.receipt.json'))['sha256']:
            raise ValueError('Changed contextual Foley source')
        raw = run([FF, '-v', 'error', '-i', source, '-t', '1.7', '-af',
                   'loudnorm=I=-32:TP=-8:LRA=5,afade=t=in:d=0.04,afade=t=out:st=1.35:d=0.35',
                   '-ar', '48000', '-ac', '2', '-f', 'f32le', '-']).stdout
        pcm = np.frombuffer(raw, dtype='<f4').reshape(-1, 2)
        at = round(unit['from'] / FPS * 48000)
        length = min(len(pcm), len(cue_audio) - at)
        cue_audio[at:at + length] += pcm[:length]
        cues.append({'unit': unit['id'], 'at': at / 48000, 'source': source.relative_to(ROOT).as_posix(),
                     'sha256': sha(source), 'role': 'Paper handling' if name == 'paper-pen' else 'Restrained argument punctuation'})
    pcm_file = BATCH / 'audio/foley.f32'
    cue_audio.tofile(pcm_file)
    run([FF, '-y', '-v', 'error', '-f', 'f32le', '-ar', '48000', '-ac', '2', '-i', pcm_file,
         '-c:a', 'pcm_s16le', BATCH / 'audio/foley.wav'])
    pcm_file.unlink()
    pauses = [u['from'] / FPS for u in data['units'] if u['id'] in ['b04', 'b09', 'b14', 'b19', 'b22']]
    gain = 'if(' + '+'.join(f'between(t,{max(0,t-.10):.3f},{t+.75:.3f})' for t in pauses) + ',0.22,1)'
    graph = f'[0:a]highpass=f=65,loudnorm=I=-16:TP=-2:LRA=10,asplit=2[v][key];[1:a]volume=\'{gain}\':eval=frame[score];[score][key]sidechaincompress=threshold=.025:ratio=4:attack=15:release=220[m];[v][m][2:a]amix=inputs=3:normalize=0,alimiter=limit=.89:level=false[out]'
    run([FF, '-y', '-v', 'error', '-i', BATCH / 'audio/narration.wav', '-i', BATCH / 'audio/music-bed.wav',
         '-i', BATCH / 'audio/foley.wav',
         '-filter_complex', graph, '-map', '[out]', '-t', seconds, '-ar', '48000', '-ac', '2', BATCH / 'audio/final-mix.wav'])
    save(BATCH / 'audio/mix-receipt.json', {'narrationSHA256': sha(BATCH / 'audio/narration.wav'),
         'mixSHA256': sha(BATCH / 'audio/final-mix.wav'), 'music': receipts, 'foley': cues,
         'musicEmphasisDipsSeconds': pauses, 'newMusicCalls': 0,
         'voiceSpeed': 1, 'continuousListening': False, 'userApproval': 'pending'})
    print('MIX_READY', seconds, flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('phase', choices=['prepare', 'voice', 'timeline', 'mix'])
    args = parser.parse_args()
    globals()[args.phase]()
