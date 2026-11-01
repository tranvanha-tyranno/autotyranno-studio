"""Try one real Muse image-to-video generation for the latest supplied image."""
from __future__ import annotations
import base64, json, re, subprocess, time
from datetime import datetime, timezone
from pathlib import Path
from importlib.util import spec_from_file_location, module_from_spec
import imageio_ffmpeg, requests

ROOT=Path(__file__).resolve().parents[3]
SOURCE=Path(r"C:\Users\tyranno\AppData\Local\Temp\codex-clipboard-dfad4c8b-0371-4a93-8bc5-dc3dd0fe8d48.png")
OUT=ROOT/'videos/2026-10-28-inox-kettle-single-ai15'
BASE='http://127.0.0.1:18610'; FF=imageio_ffmpeg.get_ffmpeg_exe()
sp=spec_from_file_location('runner',ROOT/'workflows/product-video/run.py'); runner=module_from_spec(sp); assert sp.loader; sp.loader.exec_module(runner)
PROMPT='''Create a real AI-generated 15-second vertical 9:16 product video from this exact reference image. Start visible motion immediately: the adult woman carrying the transparent acrylic handled box walks briskly forward through the factory aisle for several steps while the camera tracks with natural background parallax, then makes a small lateral camera move and gentle push-in for the final seconds. Keep the box suspended, front facing camera, with a natural 1–2 cm bob. Preserve the silver stainless-steel 1.8L kettle, black handle and lid, red indicator light, transparent box, hand, nails, factory background, every Vietnamese label and all geometry. Do not spin, flip, morph or place the box on a surface. No face, body, extra hands, extra fingers, new props, new text, subtitles, logos, watermark, music or sound effects. One continuous realistic AI video, no slideshow, no static hold.'''
DIALOGUE='[excited] Ê ê ê! Ấm inox cao cấp 1,8 lít đây nha! Nấu nhanh, tự ngắt điện khi nước sôi, tay cầm cách nhiệt và đế xoay 360 độ. Nhìn gọn mà tiện lắm luôn!'

def dur(p):
    r=subprocess.run([FF,'-hide_banner','-i',str(p)],capture_output=True,text=True,encoding='utf-8',errors='replace'); m=re.search(r'Duration: (\d+):(\d+):(\d+\.\d+)',r.stderr)
    if not m: raise RuntimeError('Cannot measure '+str(p))
    return int(m[1])*3600+int(m[2])*60+float(m[3])

def main():
    OUT.mkdir(parents=True,exist_ok=True); (OUT/'input.png').write_bytes(SOURCE.read_bytes()); (OUT/'video-prompt.txt').write_text(PROMPT,encoding='utf-8'); (OUT/'dialogue.txt').write_text(DIALOGUE,encoding='utf-8')
    (OUT/'cost-plan.json').write_text(json.dumps({'target_seconds':15,'opening_image_calls':0,'planned_provider_calls':{'muse_video':1,'elevenlabs_tts':1},'optional_llm':0},ensure_ascii=False,indent=2),encoding='utf-8')
    task_file=OUT/'muse-task.json'; raw=OUT/'muse-original.mp4'; headers=runner.muse_headers()
    if task_file.exists(): task=json.loads(task_file.read_text(encoding='utf-8')); tid=task['id']
    else:
        payload={'prompt':PROMPT,'duration':15,'size':'9:16','resolution':'720p','reference_image':'data:image/png;base64,'+base64.b64encode(SOURCE.read_bytes()).decode()}
        r=requests.post(BASE+'/v1/videos',headers={**headers,'Content-Type':'application/json'},json=payload,timeout=90); r.raise_for_status(); task=r.json(); task_file.write_text(json.dumps(task,ensure_ascii=False,indent=2),encoding='utf-8'); tid=task['id']
    last=None
    for _ in range(100):
        task=requests.get(BASE+'/v1/videos/'+tid,headers=headers,timeout=35).json(); state=(task.get('status'),task.get('progress'))
        if state!=last: print(tid,state,flush=True); last=state
        if task.get('status')=='failed':
            task_file.write_text(json.dumps(task,ensure_ascii=False,indent=2),encoding='utf-8'); raise RuntimeError(task.get('error') or 'Muse failed')
        if task.get('status')=='completed':
            task_file.write_text(json.dumps(task,ensure_ascii=False,indent=2),encoding='utf-8'); url=task.get('url') or task.get('video',{}).get('url') or task.get('result',{}).get('url'); rr=requests.get(url,headers=headers,timeout=120); rr.raise_for_status(); raw.write_bytes(rr.content); break
        time.sleep(7)
    else: raise RuntimeError('Muse task pending')
    seconds=dur(raw); print('AI_SECONDS',seconds,flush=True)
    if seconds<14.9: raise RuntimeError(f'AI output shorter than 15 seconds: {seconds:.2f}')
    voice=OUT/'voice.mp3'
    r=requests.post('https://api.elevenlabs.io/v1/text-to-speech/pNInz6obpgDQGcFmaJgB',params={'output_format':'mp3_44100_128'},headers={'xi-api-key':runner.eleven_key(),'Accept':'audio/mpeg'},json={'text':DIALOGUE,'model_id':'eleven_v3','language_code':'vi','voice_settings':{'stability':0.5}},timeout=180); r.raise_for_status(); voice.write_bytes(r.content)
    vsec=dur(voice); tempo=max(1.0,vsec/14.5)
    if tempo>1.25: raise RuntimeError(f'Dialogue too long: {vsec:.2f}')
    final=OUT/'final.mp4'; filt=f'[0:v]scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,setsar=1,fps=30[v];[1:a]atempo={tempo:.8f},apad,atrim=duration=15[a]'; subprocess.run([FF,'-y','-i',str(raw),'-i',str(voice),'-filter_complex',filt,'-map','[v]','-map','[a]','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-t','15','-movflags','+faststart',str(final)],capture_output=True,check=True); subprocess.run([FF,'-v','error','-i',str(final),'-f','null','-'],capture_output=True,check=True); subprocess.run([FF,'-y','-i',str(final),'-vf','fps=1,scale=180:320,tile=5x3','-frames:v','1',str(OUT/'contact-sheet.jpg')],capture_output=True,check=True)
    (OUT/'verification.json').write_text(json.dumps({'seconds':dur(final),'resolution':'720x1280','fps':30,'visual_method':'Muse AI image-to-video','decode':'passed','still_fallback':False},ensure_ascii=False,indent=2),encoding='utf-8'); print('READY',final,flush=True)

if __name__=='__main__': main()
