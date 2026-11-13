"""Rejected still-image prototype; use documentary.py for YouTube-reference work."""
from pathlib import Path
import json, math, random, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import imageio_ffmpeg

FF=imageio_ffmpeg.get_ffmpeg_exe()

def ft(size,bold=False):
    p=Path('C:/Windows/Fonts/arialbd.ttf' if bold else 'C:/Windows/Fonts/arial.ttf')
    return ImageFont.truetype(p,size) if p.exists() else ImageFont.load_default()

def noise_layer(size,seed):
    random.seed(seed); w,h=size
    im=Image.new('RGBA',size,(0,0,0,0)); d=ImageDraw.Draw(im)
    for _ in range(80):
        x=random.randrange(w); y=random.randrange(h); r=random.randrange(10,130)
        c=random.choice([(30,70,90,45),(130,60,40,38),(180,160,100,25),(20,120,130,30)])
        d.ellipse((x-r,y-r,x+r,y+r),fill=c)
    return im.filter(ImageFilter.GaussianBlur(45))

def background(size,scene):
    w,h=size; base=tuple(scene['base']); im=Image.new('RGB',size,base); d=ImageDraw.Draw(im)
    # Cinematic low-key B-roll abstractions: all original, no reference footage reused.
    kind=scene['kind']
    if kind=='containers':
        for i in range(8):
            x=80+i*230; y=500+(i%2)*90
            d.rectangle((x,y,x+250,y+150),fill=scene['accent'],outline=(20,30,35),width=5)
            d.line((x+30,y+30,x+220,y+30),fill=(220,210,180),width=3)
        d.polygon([(0,780),(w,650),(w,h),(0,h)],fill=(8,15,20))
    elif kind=='factory':
        for x in range(80,w,180):
            d.rectangle((x,390,x+110,800),fill=(34,47,54)); d.rectangle((x+28,320,x+78,390),fill=(40,55,60))
            for yy in range(450,760,70): d.rectangle((x+25,yy,x+83,yy+28),fill=scene['accent'])
        d.rectangle((0,800,w,h),fill=(8,13,17))
    elif kind=='city':
        for i in range(18):
            x=i*115+random.randrange(-30,30); top=random.randrange(300,720)
            d.rectangle((x,top,x+95,850),fill=(25,35,48))
            for yy in range(top+35,820,55):
                if random.random()>.25:d.rectangle((x+18,yy,x+32,yy+12),fill=(214,172,92))
        d.rectangle((0,850,w,h),fill=(7,11,16))
    elif kind=='paper':
        d.polygon([(350,300),(1570,230),(1730,820),(500,900)],fill=(170,165,145));
        for y in range(410,800,85): d.line((500,y,1550,y-65),fill=(75,75,75),width=3)
        for x in range(600,1500,210): d.line((x,360,x+100,850),fill=(90,90,90),width=3)
    elif kind=='map':
        for i in range(12):
            x=random.randrange(50,w-80); y=random.randrange(320,850)
            d.ellipse((x,y,x+18,y+18),fill=scene['accent']); d.line((x+9,y+9,w//2,550),fill=(120,160,170),width=2)
        d.arc((200,230,1700,1000),190,350,fill=(100,150,160),width=4)
    elif kind=='person':
        d.ellipse((780,250,1120,590),fill=(50,45,45)); d.rectangle((680,560,1220,1000),fill=(35,42,48)); d.ellipse((450,680,650,880),fill=(70,50,40)); d.rectangle((430,840,690,1010),fill=(30,36,42))
    im=Image.alpha_composite(im.convert('RGBA'),noise_layer(size,scene['seed'])).convert('RGB')
    # Strong dark vignette like the samples.
    vig=Image.new('RGBA',size,(0,0,0,0)); vd=ImageDraw.Draw(vig)
    for n in range(18): vd.rectangle((n*18,n*12,w-n*18,h-n*12),outline=(0,0,0,max(0,80-n*4)),width=24)
    return Image.alpha_composite(im.convert('RGBA'),vig).convert('RGB')

def card(path,scene):
    im=background((1920,1080),scene); d=ImageDraw.Draw(im)
    white=(240,243,242); muted=(180,190,190)
    d.text((70,42),'AUTO TYRANNO  ·  KINH TẾ TRONG 60 GIÂY',font=ft(28,True),fill=muted)
    d.line((70,92,1850,92),fill=(220,220,220),width=2)
    # Original podcast identity: a simple mic + waveform line, kept subtle.
    cx,cy=960,520; d.rounded_rectangle((cx-22,cy-90,cx+22,cy+30),20,outline=white,width=5); d.arc((cx-58,cy-20,cx+58,cy+75),0,180,fill=white,width=5); d.line((cx,cy+75,cx,cy+110),fill=white,width=5); d.line((cx-35,cy+110,cx+35,cy+110),fill=white,width=5)
    random.seed(scene['seed']); pts=[]
    for x in range(440,1480,8):
        amp=random.randint(5,42)*(1+0.3*math.sin(x/33)); pts.append((x,cy+math.sin(x/12)*amp))
    d.line(pts,fill=white,width=3)
    d.line((420,cy,1500,cy),fill=(210,220,220),width=2)
    # Caption block, matching placement and scale of the references.
    d.rectangle((0,905,1920,1080),fill=(0,0,0,150))
    f=ft(38); lines=[]
    for word in scene['caption'].split():
        t=(lines[-1]+' '+word).strip() if lines else word
        if d.textbbox((0,0),t,font=f)[2]>1750: lines.append(word)
        elif lines: lines[-1]=t
        else: lines=[t]
    y=935
    for line in lines[:2]: d.text((90,y),line,font=f,fill=white); y+=52
    im.save(path,quality=94)

def main(batch):
    batch=Path(batch); data=json.loads((batch/'batch.json').read_text(encoding='utf-8')); still=batch/'reference-stills'; still.mkdir(exist_ok=True)
    for i,s in enumerate(data['scenes'],1): card(still/f'scene-{i:02}.jpg',s)
    ins=[]; filt=[]
    for i,s in enumerate(data['scenes']):
        ins += ['-loop','1','-t',str(s['seconds']),'-i',str(still/f'scene-{i+1:02}.jpg')]
        filt.append(f'[{i}:v]format=yuv420p[v{i}]')
    vf=';'.join(filt)+';'+''.join(f'[v{i}]' for i in range(len(filt)))+f'concat=n={len(filt)}:v=1:a=0[v]'
    silent=batch/'reference-style-silent.mp4'; final=batch/'final-reference-style.mp4'
    subprocess.run([FF,'-y']+ins+['-filter_complex',vf,'-map','[v]','-t','60','-an','-c:v','libx264','-pix_fmt','yuv420p',str(silent)],check=True,capture_output=True)
    # Overlay the narration waveform from the actual audio, as in the samples.
    graph='[1:a]showwaves=s=1100x120:mode=line:colors=white,format=rgba[wave];[0:v][wave]overlay=410:460:format=auto[v]'
    subprocess.run([FF,'-y','-i',str(silent),'-i',str(batch/'voice.mp3'),'-filter_complex',graph,'-map','[v]','-map','1:a:0','-t','60','-c:v','libx264','-c:a','aac','-b:a','128k','-pix_fmt','yuv420p','-movflags','+faststart',str(final)],check=True,capture_output=True)
    subprocess.run([FF,'-v','error','-i',str(final),'-f','null','-'],check=True,capture_output=True)
    (batch/'qa-reference-style.json').write_text(json.dumps({'result':'passed','style':'horizontal documentary/podcast B-roll','duration_seconds':60,'resolution':'1920x1080','full_decode':'passed','waveform':'actual narration overlay'},ensure_ascii=False,indent=2),encoding='utf-8')
    print(final)

if __name__=='__main__': main(sys.argv[1])
