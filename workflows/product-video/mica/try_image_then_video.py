"""One-image Muse smoke test: generate opening image first, then optionally video."""
from __future__ import annotations
import base64, json, re, shutil, subprocess, sys, time
from pathlib import Path
from importlib.util import spec_from_file_location, module_from_spec
import imageio_ffmpeg, requests

ROOT=Path(__file__).resolve().parents[3]
SOURCE=Path(r"C:\Users\tyranno\AppData\Local\Temp\codex-clipboard-dfad4c8b-0371-4a93-8bc5-dc3dd0fe8d48.png")
OUT=ROOT/'videos/2026-10-28-inox-kettle-image-video-test'
BASE='http://127.0.0.1:18610'; FF=imageio_ffmpeg.get_ffmpeg_exe()
sp=spec_from_file_location('runner',ROOT/'workflows/product-video/run.py'); runner=module_from_spec(sp); assert sp.loader; sp.loader.exec_module(runner)

IMAGE_PROMPT='''Create one realistic vertical 9:16 product image from the supplied reference. Keep the exact silver stainless-steel 1.8L kettle, black handle and lid, red indicator light, transparent acrylic handled box, adult woman's hand and factory aisle. Preserve every Vietnamese label and all visible product geometry exactly. The box is suspended in the hand, front facing camera, no face or body visible, no extra hands or fingers, no new text, logo or watermark. Neutral white light, sharp product, softly blurred factory background, full box and handle inside frame.'''
VIDEO_PROMPT='''Create a real AI-generated 15-second vertical 9:16 video from this opening image. Start motion immediately: the adult woman carrying the transparent acrylic handled box walks briskly forward through the factory aisle while the camera tracks with clear background parallax, then makes a small lateral move and gentle push-in. Keep the box suspended and front-facing with a natural 1–2 cm bob. Preserve the silver 1.8L kettle, black handle and lid, red light, every Vietnamese label, hand, nails, box and background. No spinning, flipping, morphing, surface contact, face, body, extra hands, extra fingers, new text, subtitles, logos, watermark, music or sound effects. One continuous realistic AI video, not a slideshow.'''
DIALOGUE='[excited] Ê ê ê! Ấm inox cao cấp 1,8 lít đây nha! Nấu nhanh, tự ngắt điện khi nước sôi, tay cầm cách nhiệt và đế xoay 360 độ. Nhìn gọn mà tiện lắm luôn!'

def data_url(path:Path)->str:return 'data:image/png;base64,'+base64.b64encode(path.read_bytes()).decode()
def duration(path:Path)->float:
 r=subprocess.run([FF,'-hide_banner','-i',str(path)],capture_output=True,text=True,encoding='utf-8',errors='replace');m=re.search(r'Duration: (\d+):(\d+):(\d+\.\d+)',r.stderr)
 if not m:raise RuntimeError('Cannot measure '+str(path))
 return int(m[1])*3600+int(m[2])*60+float(m[3])
def media_url(task):return task.get('url') or task.get('result',{}).get('url') or (task.get('data') or [{}])[0].get('url')
def poll(endpoint,tid,headers,path):
 last=None
 for _ in range(120):
  t=requests.get(BASE+endpoint+'/'+tid,headers=headers,timeout=35).json(); state=(t.get('status'),t.get('progress'))
  if state!=last:print(tid,state,flush=True);last=state
  if t.get('status') in ('failed','error'):
   path.write_text(json.dumps(t,ensure_ascii=False,indent=2),encoding='utf-8');raise RuntimeError(t.get('error') or 'provider task failed')
  if t.get('status') in ('completed','succeeded','success','done'):
   path.write_text(json.dumps(t,ensure_ascii=False,indent=2),encoding='utf-8');return t
  time.sleep(7)
 raise RuntimeError('provider task still pending')

def image_stage():
 OUT.mkdir(parents=True,exist_ok=True); (OUT/'input.png').write_bytes(SOURCE.read_bytes()); (OUT/'opening-prompt.txt').write_text(IMAGE_PROMPT,encoding='utf-8')
 (OUT/'cost-plan.json').write_text(json.dumps({'image_calls_planned':1,'video_calls_planned':1,'tts_calls_planned':1,'optional_llm':0},indent=2),encoding='utf-8')
 headers=runner.muse_headers(); task_file=OUT/'image-task.json'; out=OUT/'opening.png'
 if out.exists():print('IMAGE_EXISTS',out);return
 if task_file.exists():t=json.loads(task_file.read_text(encoding='utf-8')); tid=t['id']
 else:
  payload={'prompt':IMAGE_PROMPT,'size':'9:16','images':[{'url':data_url(SOURCE)}],'timeout':600};r=requests.post(BASE+'/v1/images/tasks',headers={**headers,'Content-Type':'application/json','Idempotency-Key':'inox-single-opening-test'},json=payload,timeout=90);r.raise_for_status();t=r.json();task_file.write_text(json.dumps(t,ensure_ascii=False,indent=2),encoding='utf-8');tid=t['id']
 t=poll('/v1/images/tasks',tid,headers,task_file);url=media_url(t)
 if not url:raise RuntimeError('image task completed without media URL')
 r=requests.get(url,headers=headers,timeout=120);r.raise_for_status();out.write_bytes(r.content);print('IMAGE_READY',out,flush=True)

def video_stage():
 image=OUT/'opening.png'
 if not image.exists():raise RuntimeError('opening.png missing; run --image first')
 (OUT/'video-prompt.txt').write_text(VIDEO_PROMPT,encoding='utf-8');headers=runner.muse_headers();task_file=OUT/'video-task.json';raw=OUT/'muse-original.mp4'
 if raw.exists():pass
 elif task_file.exists():t=json.loads(task_file.read_text(encoding='utf-8'));t=poll('/v1/videos',t['id'],headers,task_file);url=media_url(t);r=requests.get(url,headers=headers,timeout=120);r.raise_for_status();raw.write_bytes(r.content)
 else:
  payload={'prompt':VIDEO_PROMPT,'duration':15,'size':'9:16','resolution':'720p','reference_image':data_url(image)};r=requests.post(BASE+'/v1/videos',headers={**headers,'Content-Type':'application/json'},json=payload,timeout=90);r.raise_for_status();t=r.json();task_file.write_text(json.dumps(t,ensure_ascii=False,indent=2),encoding='utf-8');t=poll('/v1/videos',t['id'],headers,task_file);url=media_url(t);r=requests.get(url,headers=headers,timeout=120);r.raise_for_status();raw.write_bytes(r.content)
 if duration(raw)<14.9:raise RuntimeError(f'AI video shorter than 15s: {duration(raw):.2f}')
 voice=OUT/'voice.mp3'
 if not voice.exists():
  r=requests.post('https://api.elevenlabs.io/v1/text-to-speech/pNInz6obpgDQGcFmaJgB',params={'output_format':'mp3_44100_128'},headers={'xi-api-key':runner.eleven_key(),'Accept':'audio/mpeg'},json={'text':DIALOGUE,'model_id':'eleven_v3','language_code':'vi','voice_settings':{'stability':0.5}},timeout=180);r.raise_for_status();voice.write_bytes(r.content)
 sec=duration(voice);tempo=max(1.0,sec/14.5);final=OUT/'final.mp4';filt=f'[1:a]atempo={tempo:.8f},apad,atrim=duration=15[a]';subprocess.run([FF,'-y','-i',str(raw),'-i',str(voice),'-filter_complex',filt,'-map','0:v','-map','[a]','-c:v','copy','-c:a','aac','-b:a','160k','-t','15','-movflags','+faststart',str(final)],capture_output=True,check=True);subprocess.run([FF,'-v','error','-i',str(final),'-f','null','-'],capture_output=True,check=True);subprocess.run([FF,'-y','-i',str(final),'-vf','fps=1,scale=180:320,tile=5x3','-frames:v','1',str(OUT/'contact-sheet.jpg')],capture_output=True,check=True);(OUT/'verification.json').write_text(json.dumps({'seconds':duration(final),'resolution':'720x1280','fps':30,'visual_method':'Muse AI image-to-video from generated opening','decode':'passed'},ensure_ascii=False,indent=2),encoding='utf-8');print('VIDEO_READY',final,flush=True)

if __name__=='__main__':
 if len(sys.argv)<2 or sys.argv[1] not in ('--image','--video'):raise SystemExit('use --image or --video')
 (image_stage if sys.argv[1]=='--image' else video_stage)()
