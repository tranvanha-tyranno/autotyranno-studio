"""User-authorized consistent Vietnamese replacement after ElevenLabs quota block.

Preserves the two original Nhật Phong takes and the failed request evidence.
Uses provider word timestamps; intra-word character timing is interpolation,
never claimed phoneme alignment. No playback-speed change after synthesis.
"""
from __future__ import annotations

import asyncio
import hashlib
import html
import json
from pathlib import Path
import re
import time
import unicodedata

import edge_tts
import aiohttp

from bread_documentary import BATCH, ROOT, duration, load, save, sha
from editorial_gate import require_for_take

VOICE = 'vi-VN-NamMinhNeural'
RATE = '+8%'
ATTEMPT_TIMEOUT_SECONDS = 150
CONNECT_TIMEOUT_SECONDS = 10
RECEIVE_TIMEOUT_SECONDS = 25
MAX_ATTEMPTS = 6


def normal(text):
    return re.sub(r'[^\w]', '', unicodedata.normalize('NFC', html.unescape(text)).casefold())


def character_alignment(text, boundaries):
    spans = list(re.finditer(r'\S+', text))
    starts, ends = [None] * len(text), [None] * len(text)
    cursor = 0
    for event in boundaries:
        expected = normal(event['text'])
        if not expected:
            continue
        first, combined = cursor, ''
        while cursor < len(spans) and len(combined) < len(expected):
            combined += normal(spans[cursor].group())
            cursor += 1
        if combined != expected:
            raise ValueError(f'Provider words differ from exact script near token {first}: {event["text"]}')
        a, b = spans[first].start(), spans[cursor - 1].end()
        t0, t1 = event['offset'] / 1e7, (event['offset'] + event['duration']) / 1e7
        for i in range(a, b):
            starts[i] = t0 + (t1 - t0) * (i - a) / max(1, b - a)
            ends[i] = t0 + (t1 - t0) * (i + 1 - a) / max(1, b - a)
    if cursor != len(spans):
        raise ValueError('Provider word metadata does not cover all script tokens')
    last = 0.0
    for i in range(len(text)):
        if starts[i] is None:
            starts[i] = ends[i] = last
        else:
            last = ends[i]
    return {'characters': list(text), 'character_start_times_seconds': starts,
            'character_end_times_seconds': ends,
            'timingMethod': 'Original provider word boundaries; character positions inside words interpolated, not phoneme alignment.'}


async def stream_attempt(text, partial):
    """Bound both a silent socket and the entire attempt, including metadata."""
    events = []
    communicator = edge_tts.Communicate(text, VOICE, rate=RATE, pitch='+0Hz', boundary='WordBoundary',
                                       connect_timeout=CONNECT_TIMEOUT_SECONDS,
                                       receive_timeout=RECEIVE_TIMEOUT_SECONDS)
    with partial.open('wb') as stream:
        async for chunk in communicator.stream():
            if chunk['type'] == 'audio':
                stream.write(chunk['data'])
                stream.flush()
            elif chunk['type'] == 'WordBoundary':
                events.append(chunk)
    if not events or not partial.stat().st_size:
        raise edge_tts.exceptions.NoAudioReceived('No complete audio/word-boundary result received.')
    return events


async def generate():
    original = load(BATCH / 'generation-plan.json')
    output = BATCH / 'audio/nam-minh'
    output.mkdir(parents=True, exist_ok=True)
    requests = []
    records = []
    for row in original['chapterTakes']:
        text = row['payload']['text']
        target = output / Path(row['file']).name
        request = {'provider': 'Microsoft Edge online TTS', 'voice': VOICE, 'rate': RATE,
                   'pitch': '+0Hz', 'text': text}
        request_hash = hashlib.sha256(json.dumps(request, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
        receipt = target.with_suffix('.receipt.json')
        alignment = target.with_suffix('.alignment.json')
        metadata = target.with_suffix('.word-boundaries.json')
        if target.exists():
            if not receipt.exists() or load(receipt).get('request_hash') != request_hash or sha(target) != load(receipt)['sha256']:
                raise ValueError('Existing alternative voice differs from frozen request')
            if not alignment.exists() or not metadata.exists() or ''.join(load(alignment)['characters']) != text:
                raise ValueError('Existing alternative take has missing/stale timing metadata')
        else:
            editorial = require_for_take(target, text, ROOT)
            events = []
            started = time.perf_counter()
            partial = target.with_suffix('.partial')
            previous_attempts = [int(p.stem.rsplit('-', 1)[-1]) for p in
                                 target.parent.glob(target.stem + '.attempt-*.json')]
            attempt_base = max(previous_attempts, default=0)
            for attempt in range(1, MAX_ATTEMPTS + 1):
                events = []
                attempt_id = attempt_base + attempt
                attempt_started = time.perf_counter()
                try:
                    events = await asyncio.wait_for(stream_attempt(text, partial),
                                                    timeout=ATTEMPT_TIMEOUT_SECONDS)
                    break
                except (edge_tts.exceptions.NoAudioReceived, asyncio.TimeoutError, aiohttp.ClientError) as error:
                    # The upstream documents intermittent Vietnamese voice
                    # failures. This endpoint makes no paid provider request.
                    save(target.with_suffix(f'.attempt-{attempt_id}.json'),
                         {'error': type(error).__name__, 'message': str(error)[:300],
                          'receivedBytes': partial.stat().st_size if partial.exists() else 0,
                          'paidCalls': 0, 'attempt': attempt_id,
                          'wallSeconds': round(time.perf_counter() - attempt_started, 3),
                          'attemptTimeoutSeconds': ATTEMPT_TIMEOUT_SECONDS,
                          'receiveTimeoutSeconds': RECEIVE_TIMEOUT_SECONDS})
                    if partial.exists() and partial.stat().st_size:
                        partial.replace(target.with_suffix(f'.attempt-{attempt_id}.partial.mp3'))
                    print('VOICE_RETRY', row['chapter'], attempt_id, type(error).__name__, flush=True)
                    if attempt == MAX_ATTEMPTS:
                        raise
                    await asyncio.sleep(min(attempt * 2, 8))
            if not events or not partial.stat().st_size:
                raise RuntimeError('TTS returned incomplete audio or missing word timestamps')
            aligned = character_alignment(text, events)
            save(metadata, events)
            save(alignment, aligned)
            partial.replace(target)
            save(receipt, {**{k: v for k, v in request.items() if k != 'text'},
                 'request_hash': request_hash, 'sha256': sha(target), 'editorial': editorial,
                 'wallSeconds': round(time.perf_counter() - started, 3), 'wordBoundaryCount': len(events),
                 'postSynthesisTimeStretch': False, 'paidElevenLabsCalls': 0})
        active = {**row, 'file': target.relative_to(BATCH).as_posix(), 'endpoint': 'Microsoft Edge online TTS',
                  'payload': {'text': text}, 'voice': VOICE, 'synthesisRate': RATE}
        requests.append(active)
        records.append({'chapter': row['chapter'], 'file': active['file'], 'sha256': sha(target), 'seconds': duration(target)})
        print('NAM_MINH_READY', row['chapter'], records[-1]['seconds'], flush=True)
    save(BATCH / 'active-generation-plan.json', {'chapterTakes': requests, 'voice': VOICE,
         'source': 'User explicitly selected a different Vietnamese voice after the quota block.',
         'originalElevenLabsPlanRetained': 'generation-plan.json', 'synthesisRate': RATE,
         'postSynthesisTimeStretch': False})
    save(BATCH / 'audio/voice-selection.json', {'selected': VOICE, 'chapters': records,
         'userInstruction': 'Dùng giọng Việt khác cho bản mới',
         'reason': 'ElevenLabs quota_exceeded on chapter3 after two valid new Nhật Phong takes.',
         'consistency': 'All final chapters use this one alternative voice; no narrator switch inside film.',
         'rejectedRequestEvidenceRetained': 'audio/03-hoa-don-nao-giam.error.json',
         'voiceQualityAcceptance': 'Pending actual listener/user feedback; metadata is not listening.'})


if __name__ == '__main__':
    asyncio.run(generate())
