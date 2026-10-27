"""Generate the approved review with Adam/V3 and replace the preview audio.

Requires ELEVENLABS_API_KEY in the process environment. Credentials are never saved.
"""
import base64
import json
import os
from pathlib import Path
import subprocess

import imageio_ffmpeg
import requests

folder = Path(__file__).resolve().parent
key = os.environ['ELEVENLABS_API_KEY']
text = (folder / 'cocobear-review-dialogue.txt').read_text(encoding='utf-8-sig').strip()
voice_id = 'pNInz6obpgDQGcFmaJgB'
model_id = 'eleven_v3'
mp3 = folder / 'cocobear-review-adam-v3.mp3'
video = folder / 'cocobear-review-final-20s.mp4'
output = folder / 'cocobear-review-adam-v3-20s.mp4'
payload = {
    'text': text,
    'model_id': model_id,
    'language_code': 'vi',
    'voice_settings': {'stability': 0.5},
}
response = requests.post(
    f'https://api.elevenlabs.io/v1/text-to-speech/{voice_id}',
    params={'output_format': 'mp3_44100_128'},
    headers={'xi-api-key': key, 'Accept': 'audio/mpeg'},
    json=payload,
    timeout=180,
)
print('tts_http_status', response.status_code, flush=True)
if response.status_code != 200:
    print(response.text[:1600].replace(key, '[REDACTED]'), flush=True)
    raise SystemExit(2)
if len(response.content) < 1000 or not response.headers.get('content-type', '').startswith('audio/'):
    raise RuntimeError('Unexpected TTS response; expected a non-empty audio file')
mp3.write_bytes(response.content)
ff = imageio_ffmpeg.get_ffmpeg_exe()
decoded = subprocess.run([ff, '-v', 'error', '-i', str(mp3), '-ac', '1', '-ar', '44100', '-f', 's16le', 'pipe:1'], capture_output=True, check=True)
seconds = len(decoded.stdout) / (44100 * 2)
speed = max(1, seconds / 19.7)
filters = f'atempo={speed:.8f},apad,atrim=duration=20'
cmd = [ff, '-y', '-i', str(video), '-i', str(mp3), '-map', '0:v:0', '-map', '1:a:0', '-af', filters, '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-t', '20', '-movflags', '+faststart', str(output)]
result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
if result.returncode:
    raise RuntimeError(result.stderr[-1600:])
check = subprocess.run([ff, '-v', 'error', '-i', str(output), '-f', 'null', '-'], capture_output=True, text=True, check=True)
report = {
    'provider': 'ElevenLabs', 'model_id': model_id, 'voice_id': voice_id,
    'voice_name': 'Adam - Dominant, Firm', 'language_code': 'vi',
    'dialogue': text, 'original_audio_seconds': seconds,
    'audio_speed_factor': speed, 'video_seconds': 20,
    'audio_edit': 'Preserve full spoken audio, adjust speed only if needed, then pad with silence.',
    'video_source': str(video), 'output': str(output),
    'request_id': response.headers.get('request-id'),
    'character_cost': response.headers.get('character-cost'),
    'decode_check': 'passed',
}
(folder / 'cocobear-review-adam-v3-check.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k != 'dialogue'}, ensure_ascii=True), flush=True)
