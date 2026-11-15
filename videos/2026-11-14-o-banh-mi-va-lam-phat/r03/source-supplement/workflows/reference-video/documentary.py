"""Real-footage documentary production. Audio-first; no image-loop substitutes."""
import argparse, asyncio, hashlib, json, math, re, subprocess, wave
from pathlib import Path
import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FF = imageio_ffmpeg.get_ffmpeg_exe()

def save(p,d): p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
def load(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def run(cmd):
    r=subprocess.run(cmd,capture_output=True)
    if r.returncode: raise RuntimeError(r.stderr.decode('utf-8',errors='replace')[-2500:])
    return r
def duration(p):
    r=subprocess.run([FF,'-hide_banner','-i',str(p)],capture_output=True,text=True)
    m=re.search(r'Duration: (\d+):(\d+):(\d+\.\d+)',r.stderr)
    if not m: raise ValueError('Cannot measure '+str(p))
    return int(m[1])*3600+int(m[2])*60+float(m[3])

async def voice(b):
    import edge_tts
    d=load(b/'batch.json'); a=b/'narration-original.mp3'; meta=b/'word-boundaries.json'
    if not a.exists() or not meta.exists():
        words=[]
        with a.with_suffix('.partial').open('wb') as f:
            async for c in edge_tts.Communicate(d['script'],'vi-VN-NamMinhNeural',rate='-2%',boundary='WordBoundary').stream():
                if c['type']=='audio':f.write(c['data'])
                elif c['type']=='WordBoundary': words.append({'start':c['offset']/1e7,'end':(c['offset']+c['duration'])/1e7,'text':c['text']})
        if not words:raise RuntimeError('Narration requires real word timestamps')
        a.with_suffix('.partial').replace(a); save(meta,words)
    dur=duration(a); factor=dur/49.0
    if not .8<=factor<=1.22:raise ValueError('Rewrite narration: natural timing does not fit 50 seconds, factor='+str(factor))
    run([FF,'-v','error','-y','-i',str(a),'-af',f'atempo={factor:.8f},apad=whole_dur=50,afade=t=out:st=49.7:d=0.3','-t','50',str(b/'narration.wav')])
    words=load(meta)
    for w in words:w['start']/=factor;w['end']/=factor
    save(b/'aligned-words.json',words)
    save(b/'voice-info.json',{'provider':'Microsoft Edge online TTS','voice':'vi-VN-NamMinhNeural','original_seconds':dur,'atempo':factor,'narration_ends_by_seconds':49,'synthetic_voice':True,'note':'OpenAI credential returned 401; Adam quota insufficient in previous batch. No voice cloning.'})
    print('VOICE',dur,'factor',round(factor,3),flush=True)

def ass_time(t):
    cs=round(t*100);return f'{cs//360000}:{cs//6000%60:02}:{cs//100%60:02}.{cs%100:02}'

def subtitles(b):
    words=load(b/'aligned-words.json'); chunks=[]; current=[]
    caption_settings=load(b/'batch.json').get('caption_settings',{})
    # Edge timestamps omit punctuation. Restore only after exact token matching;
    # never invent timestamps or truncate a multiword metadata event.
    tokens=load(b/'batch.json')['script'].split(); cursor=0
    normal=lambda s: re.sub(r'[^\w]', '', s.casefold())
    for w in words:
        count=len(w['text'].split()); candidate=' '.join(tokens[cursor:cursor+count])
        if normal(candidate)!=normal(w['text']):
            raise ValueError('Narration metadata differs from script at '+w['text'])
        w['text']=candidate;cursor+=count
    if cursor!=len(tokens):raise ValueError('Narration metadata does not cover the whole script')
    for w in words:
        current.append(w)
        text=' '.join(x['text'] for x in current)
        if len(text)>caption_settings.get('max_chars',65) or w['end']-current[0]['start']>caption_settings.get('max_seconds',2.5) or ((len(current)>3 or caption_settings.get('break_sentences_always',False)) and re.search(r'[.!?;:]$',w['text'])):
            chunks.append(current);current=[]
    if current:chunks.append(current)
    # Keep a short sentence ending attached, rather than showing one orphan word.
    for i in range(len(chunks)-1,0,-1):
        if sum(len(x['text'].split()) for x in chunks[i])<=2:
            combined=chunks[i-1]+chunks[i]
            if len(' '.join(x['text'] for x in combined))<=105:
                chunks[i-1]=combined;chunks.pop(i)
    header='''[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2
[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Default,Arial,40,&H00FFFFFF,&H00FFFFFF,&H00202020,&H00000000,0,0,0,0,100,100,0,0,1,2,1,2,130,130,100,1
[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
'''
    srt=[]
    for i,c in enumerate(chunks):
        start=c[0]['start']; end=min(c[-1]['end']+.12,chunks[i+1][0]['start'] if i+1<len(chunks) else 49.6)
        text=' '.join(x['text'] for x in c).replace('{','').replace('}','')
        # A restrained accent on the last phrase, like the reviewed podcast group.
        tokens=text.split(); cut=max(0,len(tokens)-2); text=' '.join(tokens[:cut])+r' {\c&HADC66A&}'+' '.join(tokens[cut:])
        header+=f'Dialogue: 0,{ass_time(start)},{ass_time(end)},Default,,0,0,0,,{{\\fad(70,70)}}{text}\n'
        srt.append({'start':start,'end':end,'text':' '.join(x['text'] for x in c)})
    (b/'captions.ass').write_text(header,encoding='utf-8-sig');save(b/'captions.json',srt)

def identity(b):
    im=Image.new('RGBA',(1920,1080));d=ImageDraw.Draw(im)
    # Transparent gradients retain the real footage rather than blacking it out.
    for y in range(1080):
        a=int(110*max(0,1-y/240)+100*max(0,(y-820)/260))
        d.line((0,y,1920,y),fill=(0,0,0,a))
    f=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',48)
    title='GÓC NHÌN KINH TẾ';box=d.textbbox((0,0),title,font=f)
    d.text(((1920-box[2])/2,80),title,font=f,fill=(255,255,255,235))
    # Original neutral microphone motif; no copied channel identity or logo.
    x,y=960,455
    d.rounded_rectangle((x-22,y-68,x+22,y+5),20,fill=(240,240,240,235))
    for yy in range(y-50,y,12):d.line((x-12,yy,x+12,yy),fill=(60,60,60,210),width=3)
    d.arc((x-36,y-18,x+36,y+30),0,180,fill='white',width=4)
    d.line((x,y+29,x,y+48),fill='white',width=4);d.line((x-22,y+48,x+22,y+48),fill='white',width=4)
    d.line((490,635,1430,635),fill=(255,255,255,120),width=2)
    im.save(b/'identity.png')

def music(b):
    sr=24000;t=np.arange(50*sr)/sr;sig=np.zeros_like(t)
    # Original quiet harmonic bed; never borrowed from the reference audio.
    for n,freq in enumerate([130.8128,155.5635,195.9977]):
        sig+=(.007/(n+1))*np.sin(2*np.pi*freq*t+0.15*np.sin(2*np.pi*.12*t))
        sig+=.003*np.sin(2*np.pi*freq*2*t)*(.6+.4*np.sin(2*np.pi*.1*t))
    for i in range(0,49,3):
        u=t-i;env=np.where(u>=0,np.exp(-np.maximum(u,0)*1.9),0)
        sig+=.009*np.sin(2*np.pi*[261.63,311.13,392,466.16][i//3%4]*u)*env
    sig*=np.minimum(t/2,1)*np.minimum((50-t)/2,1)
    with wave.open(str(b/'original-music.wav'),'wb') as f:
        f.setnchannels(1);f.setsampwidth(2);f.setframerate(sr);f.writeframes((sig*32767).astype('<i2').tobytes())

def render(b):
    d=load(b/'batch.json');subtitles(b);identity(b);music(b);(b/'shots').mkdir(exist_ok=True)
    for i,s in enumerate(d['shots']):
        p=b/s['file']; out=b/'shots'/f'{i+1:02}.mp4'
        if duration(p)<s['in']+s['seconds']-.04:raise ValueError('Footage too short '+str(p))
        if out.exists():continue
        grade=s.get('grade','eq=brightness=-0.09:saturation=0.78:contrast=1.03')
        vf='scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setsar=1,fps=30,'+grade
        run([FF,'-v','error','-y','-ss',str(s['in']),'-i',str(p),'-an','-vf',vf,'-frames:v',str(round(s['seconds']*30)),'-c:v','libx264','-preset','fast','-crf','20',str(out)])
        print('SHOT',i+1,flush=True)
    (b/'concat.txt').write_text('\n'.join("file 'shots/%02d.mp4'"%(i+1) for i in range(len(d['shots']))),encoding='utf-8')
    run([FF,'-v','error','-y','-f','concat','-safe','0','-i',str(b/'concat.txt'),'-c','copy',str(b/'picture.mp4')])
    # Working directory makes ASS path safe on Windows (no drive-colon escaping).
    graph="[0:v][1:v]overlay=0:0[base];[2:a]aformat=channel_layouts=mono,volume=4,showwaves=s=940x90:mode=line:rate=30:colors=white:scale=sqrt:draw=full,format=rgba,colorkey=black:0.1:0.1[w];[base][w]overlay=490:530:shortest=1,ass=captions.ass,fade=t=out:st=49.7:d=0.3[v];[2:a]loudnorm=I=-17:TP=-1.8:LRA=8[vo];[vo][3:a]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.9[a]"
    cmd=[FF,'-v','error','-y','-i','picture.mp4','-i','identity.png','-i','narration.wav','-i','original-music.wav','-filter_complex',graph,'-map','[v]','-map','[a]','-frames:v','1500','-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart','final.mp4']
    r=subprocess.run(cmd,cwd=b,capture_output=True)
    if r.returncode:raise RuntimeError(r.stderr.decode(errors='replace')[-2000:])
    print('RENDERED',flush=True)

def qa(b):
    decode=run([FF,'-v','error','-i',str(b/'final.mp4'),'-f','null','-','-progress','pipe:1'])
    counts=[int(x.split('=')[1]) for x in decode.stdout.decode().splitlines() if x.startswith('frame=')]
    if not counts or counts[-1]!=1500:raise ValueError('Decoded video frame count must be exactly 1500')
    if abs(duration(b/'final.mp4')-50)>.05:raise ValueError('Final must last exactly 50 seconds')
    if load(b/'aligned-words.json')[-1]['end']>49.7:raise ValueError('Last spoken word would be cut by final fade')
    frames=run([FF,'-v','error','-i',str(b/'final.mp4'),'-vf','fps=1,scale=320:180','-pix_fmt','rgb24','-f','rawvideo','pipe:1']).stdout
    n=len(frames)//(320*180*3);sheet=Image.new('RGB',(1600,math.ceil(n/5)*205),'#111111');dr=ImageDraw.Draw(sheet)
    for i in range(n):
        im=Image.frombytes('RGB',(320,180),frames[i*172800:(i+1)*172800]);x=i%5*320;y=i//5*205
        sheet.paste(im,(x,y+23));dr.text((x+4,y+3),str(i)+'s',fill='white')
    sheet.save(b/'full-duration-review.jpg',quality=93)
    save(b/'verification.json',{'full_decode':'passed','container_seconds':duration(b/'final.mp4'),'sampled_frames_1fps':n,'decoded_video_frames':counts[-1],'visual_review':'pending','audio_review':'timing measured; listening review not claimed','footage':'licensed illustrative moving stock; no reference footage reused','notes':'Word captions use provider timestamps; verify important names/numbers by listening.'})
    print('QA_DECODE_OK',n,flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('stage',choices=['voice','render','qa']);p.add_argument('--batch',type=Path,required=True);a=p.parse_args();b=a.batch.resolve()
    if a.stage=='voice':asyncio.run(voice(b))
    elif a.stage=='render':render(b)
    else:qa(b)
