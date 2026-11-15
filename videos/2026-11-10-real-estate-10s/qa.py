from pathlib import Path
import json,re,subprocess
import imageio_ffmpeg
from PIL import Image,ImageDraw
p=Path(__file__).resolve().parent;f=p/'bat-dong-san-10s.mp4';ff=imageio_ffmpeg.get_ffmpeg_exe()
r=subprocess.run([ff,'-hide_banner','-i',str(f)],capture_output=True).stderr.decode('utf8','replace')
m=re.search(r'Duration: (\d+):(\d+):([\d.]+)',r);sec=int(m[1])*3600+int(m[2])*60+float(m[3])
assert abs(sec-10)<.08,(sec,r)
assert '1920x1080' in r and '30 fps' in r and 'Audio: aac' in r,r
check=subprocess.run([ff,'-v','error','-i',str(f),'-f','null','-'],capture_output=True)
assert check.returncode==0 and not check.stderr,check.stderr
sheet=Image.new('RGB',(4*480,2*290),'#202020');draw=ImageDraw.Draw(sheet)
for i,t in enumerate([.5,1.8,3.5,4.6,5.7,7.0,8.6,9.6]):
 q=p/f'qa-{i:02}.jpg'
 subprocess.run([ff,'-v','error','-y','-ss',str(t),'-i',str(f),'-frames:v','1','-vf','scale=480:270',str(q)],check=True)
 sheet.paste(Image.open(q),(i%4*480,i//4*290+20));draw.text((i%4*480+10,i//4*290+3),str(t)+'s',fill='white')
sheet.save(p/'final-qa-sheet.jpg')
levels=subprocess.run([ff,'-hide_banner','-i',str(f),'-vn','-af','volumedetect','-f','null','-'],capture_output=True).stderr.decode('utf8','replace')
(p/'audio-qa.txt').write_text(levels,encoding='utf8')
report={'duration_seconds':sec,'width':1920,'height':1080,'fps':30,'frames':300,'audio':'AAC, new Vietnamese Adam narration','full_decode':'passed','sampled_times':[.5,1.8,3.5,4.6,5.7,7.0,8.6,9.6],'file_bytes':f.stat().st_size,'subtitle_timing':'Whisper word timestamps, exact script text, six phrase groups','limitations':'General economic mechanism; illustrative stock scenes are not asserted to show China or a particular market event. No copied channel branding, footage, or original narration.'}
(p/'qa-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(report,ensure_ascii=True))
