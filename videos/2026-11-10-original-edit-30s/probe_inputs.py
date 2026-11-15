from pathlib import Path
import subprocess,json,re
import imageio_ffmpeg
from PIL import Image,ImageDraw
out=Path('videos/2026-11-10-original-edit-30s');ff=imageio_ffmpeg.get_ffmpeg_exe()
meta=[]
for n,p in enumerate(sorted(Path('C:/Users/tyranno/Documents/output').glob('2aObo*.mp4'))):
 r=subprocess.run([ff,'-hide_banner','-i',str(p)],capture_output=True).stderr.decode('utf8','replace')
 print(p.name,r[-2200:],flush=True)
 meta.append({'file':str(p),'metadata':r})
 m=re.search(r'Duration: (\d+):(\d+):([\d.]+)',r);d=int(m[1])*3600+int(m[2])*60+float(m[3])
 times=[.1,min(3,d*.2),min(8,d*.4),min(15,d*.6),min(22,d*.8),min(29,d-.2)]
 sheet=Image.new('RGB',(960,600),'#333');dr=ImageDraw.Draw(sheet)
 for i,t in enumerate(times):
  q=out/f'input{n}-{i}.jpg';subprocess.run([ff,'-v','error','-y','-ss',str(t),'-i',str(p),'-frames:v','1','-vf','scale=320:270:force_original_aspect_ratio=decrease',str(q)],check=True)
  im=Image.open(q);sheet.paste(im,(i%3*320,i//3*300+25));dr.text((i%3*320+4,i//3*300+4),f'{t:.1f}s',fill='white')
 sheet.save(out/f'input{n}-sheet.jpg')
(out/'input-metadata.json').write_text(json.dumps(meta,indent=2),encoding='utf8')
