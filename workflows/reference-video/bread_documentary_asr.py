"""Resume independent local ASR on exact documentary narration, one take at a time.

Reads the frozen content and generation plan, never calls a generation provider.
Whisper base must already be cached. Coverage/number/tail flags are diagnostic:
they cannot establish manual listening, performance, or an actual spoken error.
"""
from __future__ import annotations

import argparse
import gc
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time
import wave

for _name in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS',
              'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
    os.environ[_name] = '2'

import economy_story_asr as base

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_BATCH = ROOT / 'videos/2026-11-14-banh-mi-documentary'
PARAMETERS = {**base.PARAMETERS, 'normalizer': base.NORMALIZER_VERSION,
              'source': 'exact individual narration takes; no music',
              'numberCheck': 'explicit illustrative number phrases within each chapter; not exact local alignment'}
NUMBER_PHRASES = {
    'hai-nghin-di-dau': ['hai mươi nghìn', 'mười hai nghìn', 'năm nghìn', 'ba nghìn',
                        'mười bốn nghìn năm trăm', 'hai mươi hai nghìn', 'hai nghìn năm trăm', 'năm trăm'],
    'giam-cai-gi': ['mười phần trăm', 'hai phần trăm', 'hai mươi hai nghìn bốn trăm bốn mươi'],
    'luong-mua-bao-nhieu-banh': ['mười triệu', 'mười triệu rưỡi', 'năm phần trăm',
                               'năm trăm', 'bốn trăm bảy mươi bảy', 'bốn phẩy năm phần trăm'],
}


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def tokens(value):
    # ASR may transcribe the spoken colloquial half-million as decimal digits.
    # Other substitutions are the existing documented Vietnamese number aliases.
    value = value.casefold().replace('mười triệu rưỡi', 'mười phẩy năm triệu')
    return base.normalized_tokens(value)


def contains(sequence, fragment):
    return any(sequence[i:i + len(fragment)] == fragment
               for i in range(max(0, len(sequence) - len(fragment) + 1)))


def lexical_checks(chapter, expected, observed):
    recognized = tokens(observed)
    phrases = []
    for phrase in NUMBER_PHRASES.get(chapter, []):
        # Include only statements actually present in the frozen script.
        if contains(tokens(expected), tokens(phrase)):
            phrases.append({'expectedPhrase': phrase,
                            'foundSomewhereInChapter': contains(recognized, tokens(phrase))})
    sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', expected) if s.strip()]
    tail = sentences[-1] if sentences else expected
    tail_tokens = tokens(tail)
    exact_tail = contains(recognized, tail_tokens)
    diagnostics = base.diagnostics(expected, observed)
    missing = [p['expectedPhrase'] for p in phrases if not p['foundSomewhereInChapter']]
    return {**diagnostics, 'numberPhrases': phrases, 'numberPhrasesNotFound': missing,
            'expectedFinalSentence': tail, 'finalSentenceExactNormalizedMatch': exact_tail,
            'requiresReview': bool(diagnostics['diagnosticFlags'] or missing or not exact_tail),
            'lexicalLimits': 'Number checks search the chapter, not the corresponding speech location. '
                             'A match cannot prove every number was spoken in its intended order; '
                             'a missing phrase can be an ASR mistake. Final-sentence normalization '
                             'can also fail on harmless recognition differences. This is not prosody assessment.'}


def prepare_audio(source, directory, ffmpeg):
    source_hash = base.sha(source)
    key = base.signature({'sourceSHA256': source_hash, 'sampleRate': 16000,
                          'channels': 1, 'sampleWidthBytes': 2})
    target = directory / (source.stem + '-' + key[:16] + '.wav')
    receipt = target.with_suffix('.json')
    if target.exists() and receipt.exists():
        info = read(receipt)
        if info.get('sourceSHA256') == source_hash and info.get('sha256') == base.sha(target):
            return target, info
        raise ValueError('Cached audio has changed')
    directory.mkdir(parents=True, exist_ok=True)
    partial = target.with_suffix('.partial.wav')
    result = subprocess.run([ffmpeg, '-y', '-v', 'error', '-threads', '2', '-filter_threads', '2',
                             '-i', str(source), '-map', '0:a:0', '-ac', '1', '-ar', '16000',
                             '-c:a', 'pcm_s16le', str(partial)], capture_output=True, timeout=120)
    if result.returncode:
        raise RuntimeError(result.stderr.decode(errors='replace')[-1500:])
    with wave.open(str(partial), 'rb') as audio:
        if (audio.getframerate(), audio.getnchannels(), audio.getsampwidth()) != (16000, 1, 2):
            raise ValueError('ASR requires 16kHz mono signed16 WAV')
        seconds = audio.getnframes() / 16000
    partial.replace(target)
    info = {'sourceSHA256': source_hash, 'sha256': base.sha(target), 'seconds': seconds,
            'sampleRate': 16000, 'channels': 1, 'sampleWidthBytes': 2,
            'scope': 'Complete individual take resampled, no time stretching or mix.'}
    base.save(receipt, info)
    return target, info


def verify(batch, ffmpeg, available_only=False):
    content_path, plan_path = batch / 'content.json', batch / 'generation-plan.json'
    active_plan = batch / 'active-generation-plan.json'
    if active_plan.exists():
        plan_path = active_plan
    content, plan = read(content_path), read(plan_path)
    chapters, takes = content['chapters'], plan['chapterTakes']
    if [c['id'] for c in chapters] != [t['chapter'] for t in takes]:
        raise ValueError('Frozen chapters and narration requests differ')
    directory = batch / 'audio/asr-base-chapters'
    directory.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()
    run_key = base.signature({'contentSHA256': base.sha(content_path), 'planSHA256': base.sha(plan_path),
                              'parameters': PARAMETERS, 'runtimeVersions': base.runtime_versions()})
    progress = {'schema': 'bread-documentary-asr-progress/1', 'runKey': run_key,
                'status': 'running', 'completedChapters': [], 'skippedChapters': [],
                'continuousListening': False, 'parameters': PARAMETERS}
    progress_path = directory / 'progress.json'
    base.save(progress_path, progress)
    model = None
    try:
        for chapter, take in zip(chapters, takes):
            expected = '\n\n'.join(u['text'] for u in chapter['units'])
            if take['payload']['text'] != expected:
                raise ValueError('Requested take differs from frozen script: ' + chapter['id'])
            source = (batch / take['file']).resolve()
            if not source.is_relative_to(batch.resolve()):
                raise ValueError('Narration source must stay inside its batch')
            if not source.is_file():
                if available_only:
                    progress['skippedChapters'].append(chapter['id'])
                    continue
                raise FileNotFoundError('Narration take not ready: ' + take['file'])
            provider_receipt = source.with_suffix('.receipt.json')
            if not provider_receipt.is_file() or read(provider_receipt).get('sha256') != base.sha(source):
                raise ValueError('Exact take missing or different from provider receipt: ' + chapter['id'])
            progress['currentChapter'] = {'chapter': chapter['id'], 'phase': 'preparing'}
            base.save(progress_path, progress)
            audio, meta = prepare_audio(source, directory / 'chunks', ffmpeg)
            request = {'sourceSHA256': meta['sourceSHA256'], 'audioSHA256': meta['sha256'],
                       'scriptSHA256': hashlib.sha256(expected.encode('utf-8')).hexdigest(),
                       'parameters': PARAMETERS, 'runtimeVersions': base.runtime_versions()}
            request_hash = base.signature(request)
            cache = directory / 'cache' / (request_hash + '.json')
            if cache.exists():
                record = read(cache)
                if record['requestHash'] != request_hash or record['request'] != request:
                    raise ValueError('ASR cache request does not match')
                record = {**record, 'cacheHit': True}
            else:
                if model is None:
                    progress['currentChapter']['phase'] = 'loading-local-base'
                    base.save(progress_path, progress)
                    from faster_whisper import WhisperModel
                    model = WhisperModel('base', device='cpu', compute_type='int8', cpu_threads=2,
                                         num_workers=1, local_files_only=True)
                progress['currentChapter']['phase'] = 'recognizing'
                progress['currentChapter']['partialSegments'] = []
                base.save(progress_path, progress)
                chapter_start = time.perf_counter()
                stream, info = model.transcribe(str(audio), language='vi', beam_size=1, best_of=1,
                    word_timestamps=False, condition_on_previous_text=False, vad_filter=False, temperature=0)
                segments = []
                for segment in stream:
                    segments.append({'start': segment.start, 'end': segment.end, 'text': segment.text})
                    progress['currentChapter']['partialSegments'] = segments
                    base.save(progress_path, progress)
                observed = ' '.join(s['text'].strip() for s in segments)
                record = {'schema': 'bread-documentary-chapter-asr/1', 'requestHash': request_hash,
                          'request': request, 'chapter': chapter['id'], 'expected': expected,
                          'recognized': observed, 'segments': segments, 'language': info.language,
                          'wallSeconds': round(time.perf_counter() - chapter_start, 3),
                          'chapterAudio': audio.relative_to(batch).as_posix(), 'audio': meta,
                          'diagnostics': lexical_checks(chapter['id'], expected, observed),
                          'cacheHit': False, 'continuousListening': False, 'aestheticApproval': False}
                base.save(cache, record)
                del stream, info
            progress['completedChapters'].append(record)
            progress['currentChapter'] = None
            progress['wallSeconds'] = round(time.perf_counter() - started, 3)
            base.save(progress_path, progress)
            print('ASR_CHAPTER', chapter['id'], record['diagnostics']['tokenSimilarity'],
                  'requires-review' if record['diagnostics']['requiresReview'] else 'no-diagnostic-flag', flush=True)
            gc.collect()
    except Exception as error:
        progress['status'] = 'failed-resumable'
        progress['error'] = {'type': type(error).__name__, 'message': str(error)}
        base.save(progress_path, progress)
        raise
    report = {'schema': 'bread-documentary-asr-review/1', 'runKey': run_key,
              'status': 'partial-available-takes' if progress['skippedChapters'] else 'complete-asr-diagnostics',
              'contentSHA256': base.sha(content_path), 'planSHA256': base.sha(plan_path),
              'parameters': PARAMETERS, 'chapters': progress['completedChapters'],
              'skippedChapters': progress['skippedChapters'],
              'wallSeconds': round(time.perf_counter() - started, 3),
              'flaggedChapters': [c['chapter'] for c in progress['completedChapters'] if c['diagnostics']['requiresReview']],
              'continuousListening': False, 'aestheticApproval': False, 'userApproval': 'pending',
              'limits': 'Independent ASR of exact dry narration, not final mix. Recognition flags need comparison '
                        'with actual audio and can be false positives. No voice/emphasis quality judgment.',
              'memoryScope': 'One base CPU/int8 model; one16k mono chapter at a time; two threads, one worker. '
                             'This is not a total-RAM cap. Avoid running alongside full render if memory is constrained.'}
    base.save(directory / 'review.json', report)
    progress['status'] = report['status']
    base.save(progress_path, progress)
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--batch', type=Path, default=DEFAULT_BATCH)
    parser.add_argument('--ffmpeg')
    parser.add_argument('--available-only', action='store_true', help='Diagnose ready takes and label missing chapters partial')
    args = parser.parse_args()
    result = verify(args.batch.resolve(), base.resolve_ffmpeg(args.ffmpeg), args.available_only)
    print('ASR_READY', result['status'], len(result['chapters']), 'chapters', flush=True)
