"""OpenAI narration with DPAPI credentials, content cache and uncertain-call guard."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess

import requests

PROJECT = Path(__file__).resolve().parents[2]

def api_key():
    if os.environ.get('OPENAI_API_KEY'):
        return os.environ['OPENAI_API_KEY']
    path = PROJECT/'.secrets/openai.dpapi.xml'
    if os.name != 'nt' or not path.exists():
        raise ValueError('Set OPENAI_API_KEY or configure the local DPAPI credential')
    safe = str(path).replace("'", "''")
    result = subprocess.run(['powershell.exe','-NoProfile','-NonInteractive','-Command',
        f"$stored=Import-Clixml -LiteralPath '{safe}'; [System.Net.NetworkCredential]::new('', $stored).Password"],capture_output=True,text=True)
    if result.returncode or not result.stdout.strip():
        raise RuntimeError('Cannot decrypt OpenAI credential for this Windows account')
    return result.stdout.strip()

def payload(text, settings):
    if not text.strip() or len(text) > 4096:
        raise ValueError('Narration must contain 1–4096 characters; split long narration by shot')
    return {'model':settings.get('model','gpt-4o-mini-tts'), 'voice':settings.get('voice','cedar'),
            'input':text,'instructions':settings.get('instructions','Nói tiếng Việt tự nhiên, trầm ấm, rõ chữ. Phong cách bình luận phân tích, nhấn nhẹ từ khóa, có khoảng nghỉ hợp lý. Không đọc như quảng cáo.'),
            'response_format':'mp3','speed':settings.get('speed',1.0)}

def cache_key(body):
    return hashlib.sha256(json.dumps(body,ensure_ascii=False,sort_keys=True).encode()).hexdigest()

def synthesize(text, target, settings):
    target = Path(target)
    target.parent.mkdir(parents=True,exist_ok=True)
    body = payload(text,settings)
    digest = cache_key(body)
    receipt = target.with_suffix('.receipt.json')
    intent = target.with_suffix('.intent.json')
    cached = PROJECT/'.cache/reference-video/tts'/f'{digest}.mp3'
    if target.exists():
        if not receipt.exists() or json.loads(receipt.read_text())['cache_key'] != digest:
            raise ValueError('Existing voice does not match this script/settings; create a new revision')
        return target
    if cached.exists():
        shutil.copy2(cached,target)
        receipt.write_text(json.dumps({'provider':'openai','cache_key':digest,'cache_hit':True}),encoding='utf-8')
        return target
    if intent.exists():
        raise RuntimeError('Previous speech call unresolved; inspect intent/error before retrying')
    key = api_key()
    intent.write_text(json.dumps({'cache_key':digest,'model':body['model'],'voice':body['voice']}),encoding='utf-8')
    try:
        response = requests.post('https://api.openai.com/v1/audio/speech',headers={'Authorization':'Bearer '+key},json=body,timeout=180)
    except requests.RequestException:
        raise RuntimeError('Speech transport failed; intent retained to prevent duplicate billing') from None
    if response.status_code != 200:
        try: error = response.json().get('error',{})
        except ValueError: error = {}
        # Only classified fields, never provider response bodies/headers or credentials.
        failure = {'http_status':response.status_code,'code':error.get('code'),'type':error.get('type')}
        target.with_suffix('.error.json').write_text(json.dumps(failure),encoding='utf-8')
        raise RuntimeError('OpenAI speech failed: '+json.dumps(failure))
    if not response.headers.get('content-type','').startswith('audio/') or len(response.content)<100:
        raise RuntimeError('Speech response is not audio; intent retained')
    pending = target.with_suffix('.partial')
    pending.write_bytes(response.content)
    pending.replace(target)
    cached.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(target,cached)
    receipt.write_text(json.dumps({'provider':'openai','model':body['model'],'voice':body['voice'],'cache_key':digest,'cache_hit':False,'bytes':len(response.content),'sha256':hashlib.sha256(response.content).hexdigest()}),encoding='utf-8')
    intent.unlink()
    return target
