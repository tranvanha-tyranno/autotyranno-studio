from pathlib import Path
import subprocess,re,json
import imageio_ffmpeg
from PIL import Image,ImageDraw
src=next(Path('C:/Users/tyranno/Documents/output').glob('*NCl_PG00oa4*mp4'))
out=Path('videos/2026-11-10-real-estate-10s');ff=imageio_ffmpeg.get_ffmpeg_exe()
r=subprocess.run([ff,'-hide_banner','-i',str(src)],capture_output=True).stderr.decode('utf-8','replace')
(out/'reference-metadata.txt').write_text(r,encoding='utf-8')
m=re.search(r'Duration: (\d+):(\d+):([\d.]+)',r);d=int(m[1])*3600+int(m[2])*60+float(m[3]);print('duration',d);print(r[-2500:])
times=[0,2,5,10,15,20,30,45,60,d*.25,d*.5,d*.75]
sheet=Image.new('RGB',(4*480,3*300),'#ddd');dr=ImageDraw.Draw(sheet)
for i,t in enumerate(times):
 p=out/f'ref-{i:02}.jpg'
 subprocess.run([ff,'-v','error','-y','-ss',str(t),'-i',str(src),'-frames:v','1','-vf','scale=480:-1',str(p)],check=True)
 im=Image.open(p);im.thumbnail((480,270));sheet.paste(im,(i%4*480,i//4*300+25));dr.text((i%4*480+10,i//4*300+5),str(round(t,1))+'s',fill='black')
sheet.save(out/'reference-sheet.jpg')
subprocess.run([ff,'-v','error','-y','-i',str(src),'-t','45','-vn','-ac','1','-ar','16000',str(out/'reference-opening.wav')],check=True)
