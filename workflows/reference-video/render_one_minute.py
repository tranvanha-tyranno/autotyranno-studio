"""Rejected still-image prototype; use documentary.py for YouTube-reference work."""
from pathlib import Path
import json, math, shutil, subprocess, sys
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

ROOT = Path(__file__).resolve().parents[2]
FF = imageio_ffmpeg.get_ffmpeg_exe()

def font(size, bold=False):
    candidates = ['C:/Windows/Fonts/arialbd.ttf' if bold else 'C:/Windows/Fonts/arial.ttf',
                  'C:/Windows/Fonts/tahoma.ttf']
    for p in candidates:
        if Path(p).exists(): return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def wrap(draw, text, f, width):
    words=text.split(); rows=[]; row=''
    for w in words:
        test=(row+' '+w).strip()
        if draw.textbbox((0,0),test,font=f)[2] > width and row:
            rows.append(row); row=w
        else: row=test
    if row: rows.append(row)
    return rows

def make_card(path, scene):
    W,H=1080,1920; bg=tuple(scene['color']); im=Image.new('RGB',(W,H),bg); d=ImageDraw.Draw(im)
    # subtle grid / glow
    for x in range(0,W,90): d.line((x,0,x,H),fill=tuple(max(0,c-12) for c in bg),width=1)
    for y in range(0,H,90): d.line((0,y,W,y),fill=tuple(max(0,c-12) for c in bg),width=1)
    fsmall=font(38); ftitle=font(68,True); fbody=font(54); fnum=font(150,True)
    d.text((74,82),'TỪ DỮ KIỆN ĐẾN BỨC TRANH LỚN',font=fsmall,fill='#9bb6c9')
    y=180
    for line in wrap(d,scene['label'],ftitle,920):
        d.text((74,y),line,font=ftitle,fill='white'); y += 92
    y += 35
    if scene.get('number'):
        d.text((74,y),scene['number'],font=fnum,fill=scene.get('accent','#61dafb')); y+=210
    for line in wrap(d,scene['body'],fbody,900):
        d.text((74,y),line,font=fbody,fill='#eaf1f6'); y+=78
    # simple visual motif
    if scene['kind']=='bars':
        base=1500; values=[.45,.63,.8,1.0]; labels=['2023','2024','2025','2026']
        for i,v in enumerate(values):
            x=110+i*220; h=int(470*v); d.rounded_rectangle((x,base-h,x+130,base),20,fill=scene['accent']); d.text((x,base+30),labels[i],font=fsmall,fill='white')
    elif scene['kind']=='flow':
        for i in range(4):
            x=120+i*240; d.rounded_rectangle((x,1450,x+150,1600),24,outline=scene['accent'],width=5); d.text((x+42,1500),str(i+1),font=font(62,True),fill=scene['accent'])
            if i<3: d.line((x+155,1525,x+230,1525),fill='#eaf1f6',width=8); d.polygon((x+230,1525,x+208,1510,x+208,1540),fill='#eaf1f6')
    elif scene['kind']=='check':
        d.ellipse((120,1400,340,1620),outline=scene['accent'],width=10); d.line((170,1515,230,1575),fill=scene['accent'],width=14); d.line((230,1575,300,1450),fill=scene['accent'],width=14)
    elif scene['kind']=='question':
        d.ellipse((160,1390,410,1640),outline=scene['accent'],width=10); d.text((240,1430),'?',font=font(170,True),fill=scene['accent'])
    d.text((74,1810),'AUTO TYRANNO · 11/2026',font=fsmall,fill='#7891a3')
    im.save(path,quality=95)

def main(batch):
    batch=Path(batch); data=json.loads((batch/'batch.json').read_text(encoding='utf-8'))
    scenes=data['scenes']; still=batch/'stills'; still.mkdir(exist_ok=True)
    for i,s in enumerate(scenes,1): make_card(still/f'scene-{i:02}.png',s)
    # Keep each card on screen for its timed scene; the cut follows narration.
    inputs=[]; filters=[]
    for i,s in enumerate(scenes):
        inputs += ['-loop','1','-t',str(s['seconds']),'-i',str(still/f'scene-{i+1:02}.png')]
        filters.append(f'[{i}:v]format=yuv420p[v{i}]')
    concat=''.join(f'[v{i}]' for i in range(len(scenes)))
    vf=';'.join(filters)+f';{concat}concat=n={len(scenes)}:v=1:a=0[v]'
    silent=batch/'video-silent.mp4'
    cmd=[FF,'-y']+inputs+['-filter_complex',vf,'-map','[v]','-t',str(data['duration_seconds']),'-an','-c:v','libx264','-pix_fmt','yuv420p','-movflags','+faststart',str(silent)]
    subprocess.run(cmd,check=True,capture_output=True)
    audio=batch/'voice.mp3'; final=batch/'final.mp4'
    subprocess.run([FF,'-y','-i',str(silent),'-i',str(audio),'-map','0:v:0','-map','1:a:0','-t',str(data['duration_seconds']),'-c:v','copy','-c:a','aac','-b:a','160k','-shortest','-movflags','+faststart',str(final)],check=True,capture_output=True)
    subprocess.run([FF,'-v','error','-i',str(final),'-f','null','-'],check=True,capture_output=True)
    (batch/'qa.json').write_text(json.dumps({'result':'passed','duration_seconds':data['duration_seconds'],'scenes':len(scenes),'audio':'voice.mp3','video':'final.mp4','full_decode':'passed'},ensure_ascii=False,indent=2),encoding='utf-8')
    print(final)

if __name__=='__main__': main(sys.argv[1])
