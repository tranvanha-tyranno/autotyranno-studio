from pathlib import Path
import subprocess,re,json
import imageio_ffmpeg
from PIL import Image,ImageDraw
p=Path(__file__).resolve().parent;ff=imageio_ffmpeg.get_ffmpeg_exe();f=p/'video-hoan-chinh-30s.mp4'
r=subprocess.run([ff,'-hide_banner','-i',str(f)],capture_output=True).stderr.decode('utf8','replace')
print(r[-2200:])
assert '00:00:30.00' in r and '720x1280' in r and '30 fps' in r and 'Audio: aac' in r,r
check=subprocess.run([ff,'-v','error','-i',str(f),'-f','null','-'],capture_output=True)
assert check.returncode==0 and not check.stderr,check.stderr
marks=[.4,2.6,3.9,6.0,9.5,12.9,15.5,18.8,21.1,23.3,27.9,29.4]
sheet=Image.new('RGB',(4*270,3*500),'#202020');d=ImageDraw.Draw(sheet)
for i,t in enumerate(marks):
 q=p/f'qa-{i:02}.jpg';subprocess.run([ff,'-v','error','-y','-ss',str(t),'-i',str(f),'-frames:v','1','-vf','scale=270:480',str(q)],check=True)
 sheet.paste(Image.open(q),(i%4*270,i//4*500+20));d.text((i%4*270+8,i//4*500+4),f'{t}s',fill='white')
sheet.save(p/'qa-contact-sheet.jpg')
levels=subprocess.run([ff,'-hide_banner','-i',str(f),'-vn','-af','volumedetect','-f','null','-'],capture_output=True).stderr.decode('utf8','replace')
print(levels[-600:])
(p/'qa-report.json').write_text(json.dumps({'duration':30,'fps':30,'size':[720,1280],'decode':'passed','source_range':[0,30],'audio':'original speech, cleaned and normalized, original synthesized instrumental bed','references':['2aOboRBg8qr1z9EPrtwyzv4APHO3JY5wW2xuZY3s.mp4','2aOboRBg8qr1z9EPrtwz0VPVYrbCnFHTAFqZDNyK.mp4'],'editing':'tight portrait crops, timed emphasis captions, two illustrated inserts over the long source pause, gentle transitions','asr_note':'Unclear words in the opening are deliberately not subtitled. Clear source phrases received spelling correction.','bytes':f.stat().st_size},ensure_ascii=False,indent=2),encoding='utf8')
