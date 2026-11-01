"""Create exact-pixel local preview videos when Muse upstream is unavailable.

The still image remains the visual source; FFmpeg supplies a brisk camera push/pan.
This fallback does not claim to animate the physical hand or kettle.
"""
from __future__ import annotations

import base64
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import subprocess

import imageio_ffmpeg
import requests

from importlib.util import spec_from_file_location, module_from_spec

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT/'videos/2026-10-28-mica-6refs-fast'
FF = imageio_ffmpeg.get_ffmpeg_exe()
runner_spec=spec_from_file_location('local_runner',ROOT/'workflows/product-video/run.py');runner=module_from_spec(runner_spec);runner_spec.loader.exec_module(runner)
REFS = [
    (r'C:\Users\tyranno\AppData\Local\Temp\codex-clipboard-99a6e628-0aab-47e0-a7ec-ff3a0bc6d319.png', 'inox-factory', 'Ấm inox cao cấp 1,8 lít', '[excited] Ê ê ê! Ấm inox 1,8 lít, nấu nhanh mà còn tự ngắt điện nữa nè!'),
    (r'C:\Users\tyranno\AppData\Local\Temp\codex-clipboard-9ead2a26-3559-4eed-802c-a2385c3ecc81.png', 'inox-mall', 'Ấm inox cao cấp 1,8 lít', '[playful] Các dợ nhìn em ấm inox này coi! Vòi rót gọn, tay cầm cách nhiệt, đế xoay 360 độ luôn á!'),
    (r'C:\Users\tyranno\AppData\Local\Temp\codex-clipboard-aa2c4628-616b-4e0e-aa59-95ba7e664d3d.png', 'inox-appliance-store', 'Ấm inox cao cấp 1,8 lít', '[amazed] Inox sáng bóng, nắp mở tiện, đun nước gọn lẹ; mấy ní thấy hợp thì chốt nha!'),
    (r'C:\Users\tyranno\AppData\Local\Temp\codex-clipboard-bdf4abdd-ccfe-469c-a35b-8f61d1aba8bd.png', 'oral-factory', 'Máy tăm nước Oral Irrigator 6886', '[excited] Ê ê ê! Máy tăm nước Oral Irrigator 6886, nhỏ gọn mà mang đi đâu cũng tiện!'),
    (r'C:\Users\tyranno\AppData\Local\Temp\codex-clipboard-bafccd7e-3706-48d2-8344-f3e9277f0f24.png', 'oral-mall', 'Máy tăm nước Oral Irrigator 6886', '[playful] Có ba chế độ, nhiều đầu tăm và túi đựng; một bộ là đủ gọn cho góc chăm răng rồi!'),
    (r'C:\Users\tyranno\AppData\Local\Temp\codex-clipboard-eb703e33-ba91-4424-bbac-fd762b22e57d.png', 'oral-appliance-store', 'Máy tăm nước Oral Irrigator 6886', '[confident] Bình nước, dây sạc và phụ kiện xếp chung một hộp; mấy ní xem kỹ nhãn rồi hẵng chốt nha!'),
]


def read_duration(path):
    result=subprocess.run([FF,'-hide_banner','-i',str(path)],capture_output=True,text=True,encoding='utf-8',errors='replace')
    match=re.search(r'Duration: (\d+):(\d+):(\d+\.\d+)',result.stderr)
    if not match:raise RuntimeError('Cannot measure '+str(path))
    return int(match[1])*3600+int(match[2])*60+float(match[3])


def tts(text, target):
    if target.exists():return
    key=runner.eleven_key()
    result=requests.post('https://api.elevenlabs.io/v1/text-to-speech/pNInz6obpgDQGcFmaJgB',params={'output_format':'mp3_44100_128'},headers={'xi-api-key':key,'Accept':'audio/mpeg'},json={'text':text,'model_id':'eleven_v3','language_code':'vi','voice_settings':{'stability':0.5}},timeout=180)
    if result.status_code!=200:raise RuntimeError(f'ElevenLabs HTTP {result.status_code}: {result.text[:300]}')
    target.write_bytes(result.content)


def local_video(source, voice, target):
    # Source remains exact pixels; this is a camera-like push/pan only.
    length=read_duration(voice); tempo=max(1.0,length/5.8)
    if tempo>1.25:raise RuntimeError(f'Voice is too long for six seconds ({length:.2f}s)')
    filters=("[0:v]scale=900:1600:force_original_aspect_ratio=increase," 
             "zoompan=z='min(zoom+0.0007,1.12)':" 
             "x='iw/2-(iw/zoom/2)+sin(on/33)*8':" 
             "y='ih/2-(ih/zoom/2)+cos(on/41)*6':" 
             "d=1:s=720x1280:fps=30,setsar=1[v];" 
             f"[1:a]atempo={tempo:.8f},apad,atrim=duration=6[a]")
    result=subprocess.run([FF,'-y','-loop','1','-i',str(source),'-i',str(voice),'-filter_complex',filters,'-map','[v]','-map','[a]','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-t','6','-movflags','+faststart',str(target)],capture_output=True,text=True,encoding='utf-8',errors='replace')
    if result.returncode:raise RuntimeError(result.stderr[-1000:])
    subprocess.run([FF,'-v','error','-i',str(target),'-f','null','-'],capture_output=True,check=True)


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    manifest={'profile':'uploaded-image-local-exact-preview','created_at':datetime.now(timezone.utc).isoformat(),'source':'Muse upstream failed with no media; local FFmpeg fallback','outputs':[],'provider_calls':{'muse_videos':0,'elevenlabs_tts':0}}
    for index,(source,slug,product,dialogue) in enumerate(REFS,1):
        directory=OUT/f'{index:02}-{slug}';directory.mkdir(exist_ok=True)
        source_path=Path(source);input_path=directory/'input.png';voice=directory/'voice.mp3';final=directory/'local-preview.mp4'
        if not input_path.exists():input_path.write_bytes(source_path.read_bytes())
        (directory/'dialogue.txt').write_text(dialogue,encoding='utf-8')
        (directory/'fallback-note.txt').write_text('Muse upstream returned no media. This preview keeps the supplied still image exact and uses FFmpeg camera push/pan; it does not physically animate the hand or product.',encoding='utf-8')
        tts(dialogue,voice)
        local_video(input_path,voice,final)
        subprocess.run([FF,'-y','-i',str(final),'-vf','fps=1,scale=180:320,tile=3x2','-frames:v','1',str(directory/'contact-sheet.jpg')],capture_output=True,check=True)
        report={'index':index,'slug':slug,'product':product,'seconds':read_duration(final),'resolution':'720x1280','fps':30,'visual_method':'exact supplied still + local FFmpeg zoompan/pan','voice':'Adam eleven_v3','decode':'passed','muse_media':'not generated: upstream 502/text-only error; no retry issued','claims':'Only dialogue claims visible in source image were used.'}
        (directory/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
        manifest['outputs'].append({'index':index,'slug':slug,'product':product,'path':str(final),'source':source})
        manifest['provider_calls']['elevenlabs_tts']+=1
        print('READY',final,flush=True)
    (OUT/'manifest-local-fallback.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')


if __name__=='__main__':main()
