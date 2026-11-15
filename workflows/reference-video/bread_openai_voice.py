"""Cached, credential-free receipts for the user-authorized OpenAI bread narration.

The API key stays in a task-specific Windows DPAPI file or OPENAI_API_KEY.
No automatic retry of an uncertain paid request. Original films/takes retained.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import time

import requests

from documentary import duration
from editorial_gate import require_for_take

ROOT = Path(__file__).resolve().parents[2]
BATCH = ROOT / 'videos/2026-11-15-banh-mi-mo-phong-openai'
SOURCE = ROOT / 'videos/2026-11-14-banh-mi-documentary'
SECRET = ROOT / '.secrets/openai-bread-2026-11-15.dpapi.xml'
MODEL = 'gpt-4o-mini-tts'
VOICE = 'cedar'
INSTRUCTIONS = (
    'Speak entirely in fluent natural Vietnamese as a professional Vietnamese economic storyteller. '
    'Use neutral clear Vietnamese pronunciation, warm grounded tone and lively conversational phrasing. '
    'Read the supplied Vietnamese text exactly without adding, omitting, translating or repeating words. '
    'Make the opening question curious and engaging. Emphasize contrasts and consequences: trả thêm versus '
    'giữ lại thêm, tăng chậm hơn versus giảm giá, tiền lương versus sức mua. Vary sentence rhythm and pitch; '
    'avoid a flat classroom lecture or exaggerated advertising voice. Clearly articulate number phrases '
    'and brief pauses around calculations, without spelling individual letters or dragging syllables. '
    'Use a brisk but unhurried native conversational pace. Slightly lower the voice for the conclusion, '
    'and end questions naturally. No music, sound effects, laughter or extra commentary.'
)


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def save(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def key():
    if os.environ.get('OPENAI_API_KEY'):
        return os.environ['OPENAI_API_KEY']
    safe = str(SECRET).replace("'", "''")
    code = f"$taskSecret=Import-Clixml -LiteralPath '{safe}'; [System.Net.NetworkCredential]::new('', $taskSecret).Password"
    result = subprocess.run(['powershell.exe', '-NoProfile', '-NonInteractive', '-Command', code],
                            capture_output=True, text=True)
    if result.returncode or not result.stdout.strip():
        raise ValueError('Task OpenAI credential unavailable')
    return result.stdout.strip()


def prepare():
    BATCH.mkdir(parents=True, exist_ok=True)
    for name in ['content.json', 'script.txt', 'editorial-map.json']:
        source, target = SOURCE / name, BATCH / name
        if target.exists() and sha(source) != sha(target):
            raise ValueError('Source script/map differs from frozen upgrade: ' + name)
        if not target.exists():
            shutil.copy2(source, target)
    takes = []
    for i, chapter in enumerate(read(BATCH / 'content.json')['chapters']):
        text = '\n\n'.join(u['text'] for u in chapter['units'])
        takes.append({'chapter': chapter['id'], 'file': f'audio/openai/{i+1:02}-{chapter["id"]}.mp3',
                      'endpoint': '/v1/audio/speech', 'payload': {'model': MODEL, 'voice': VOICE,
                      'input': text, 'instructions': INSTRUCTIONS, 'response_format': 'mp3', 'speed': 1.0}})
    path = BATCH / 'openai-generation-plan.json'
    value = {'voice': VOICE, 'provider': 'OpenAI', 'model': MODEL, 'chapterTakes': takes,
             'postSynthesisSpeedChange': False, 'credentialInPlan': False,
             'docs': 'https://developers.openai.com/api/docs/guides/text-to-speech',
             'disclosure': 'Final viewer/description labels narrator as AI-generated.'}
    if path.exists() and read(path) != value:
        raise ValueError('OpenAI generation plan frozen')
    save(path, value)
    return value


def generate(limit=None):
    plan = prepare()
    records = []
    for row in plan['chapterTakes'][:limit]:
        target = BATCH / row['file']
        target.parent.mkdir(parents=True, exist_ok=True)
        payload = row['payload']
        digest = hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
        receipt, intent = target.with_suffix('.receipt.json'), target.with_suffix('.intent.json')
        if target.exists():
            if not receipt.exists() or read(receipt).get('request_hash') != digest or read(receipt).get('sha256') != sha(target):
                raise ValueError('Existing OpenAI audio differs from requested take')
        else:
            if intent.exists():
                raise RuntimeError('Prior OpenAI request unresolved; inspect retained intent/error before retry')
            editorial = require_for_take(target, payload['input'], ROOT)
            secret = key()
            save(intent, {'request_hash': digest, 'endpoint': row['endpoint'], 'payload': payload, 'editorial': editorial})
            start = time.perf_counter()
            try:
                response = requests.post('https://api.openai.com' + row['endpoint'],
                    headers={'Authorization': 'Bearer ' + secret}, json=payload, timeout=(20, 180))
            except requests.RequestException:
                raise RuntimeError('OpenAI speech transport failed; intent retained without paid retry') from None
            finally:
                secret = None
            if response.status_code != 200:
                try:
                    error = response.json().get('error', {})
                except ValueError:
                    error = {}
                failure = {'httpStatus': response.status_code, 'code': error.get('code'), 'type': error.get('type')}
                save(target.with_suffix('.error.json'), failure)
                raise RuntimeError('OpenAI rejected narration: ' + json.dumps(failure))
            if not response.headers.get('content-type', '').startswith('audio/') or len(response.content) < 1000:
                raise RuntimeError('Expected narration audio; intent retained')
            pending = target.with_suffix('.partial.mp3')
            pending.write_bytes(response.content)
            seconds = duration(pending)
            if seconds < 2:
                raise RuntimeError('Narration unexpectedly short; intent retained')
            pending.replace(target)
            save(receipt, {'provider': 'OpenAI', 'model': MODEL, 'voice': VOICE, 'request_hash': digest,
                 'sha256': sha(target), 'bytes': target.stat().st_size, 'seconds': seconds,
                 'requestID': response.headers.get('x-request-id'), 'wallSeconds': round(time.perf_counter()-start, 3),
                 'editorial': editorial, 'outputCostUSD': 'Not supplied by this endpoint; no invoice inferred.'})
            intent.unlink()
        records.append({'chapter': row['chapter'], 'file': row['file'], 'seconds': duration(target), 'sha256': sha(target)})
        save(BATCH / 'audio/openai/voice-runs.json', {'provider': 'OpenAI', 'model': MODEL, 'voice': VOICE,
             'chapters': records, 'manualListening': False, 'userApproval': 'pending'})
        print('OPENAI_TAKE_READY', row['chapter'], records[-1]['seconds'], flush=True)
    if limit is None:
        save(BATCH / 'active-generation-plan.json', {'provider': 'OpenAI', 'voice': VOICE, 'model': MODEL,
             'chapterTakes': [{**r, 'payload': {'text': r['payload']['input']}}
                              for r in plan['chapterTakes']]})


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('phase', choices=['prepare', 'generate'])
    parser.add_argument('--limit', type=int)
    args = parser.parse_args()
    if args.phase == 'prepare':
        prepare()
    else:
        generate(args.limit)
