import json,subprocess,hashlib
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import yt_dlp,imageio_ffmpeg
r=Path('docs/video-references/2026-11-11'); ff=imageio_ffmpeg.get_ffmpeg_exe()
def one(p):
 e=json.loads(p.read_text(encoding='utf-8')); folder=p.parent; out=folder/'reference-av.mp4'
 try:
  if not out.exists():
   with yt_dlp.YoutubeDL({'quiet':True,'noprogress':True,'socket_timeout':30,'retries':1,'outtmpl':str(folder/'reference-audio.%(ext)s'),'format':'bestaudio[language=vi]/bestaudio'}) as y:
    y.download([e['url']])
   a=next(x for x in folder.glob('reference-audio.*') if x.suffix in ['.m4a','.webm','.mp4'])
   subprocess.run([ff,'-v','error','-y','-i',str(folder/'reference.mp4'),'-i',str(a),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','96k',str(out)],capture_output=True,check=True)
  # Decode every stream, do not mistake file presence for success.
  subprocess.run([ff,'-v','error','-i',str(out),'-f','null','-'],capture_output=True,check=True)
  e['local_av']={'path':out.name,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'full_decode':'passed'}
  print(e['id'],'AV_OK',flush=True)
 except Exception as ex:
  e['local_av_error']=type(ex).__name__; print(e['id'],'AV_FAILED',type(ex).__name__,flush=True)
 p.write_text(json.dumps(e,ensure_ascii=False,indent=2),encoding='utf-8')
with ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(one,sorted(r.glob('*/evidence.json'))))
