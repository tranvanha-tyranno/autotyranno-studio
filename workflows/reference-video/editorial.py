"""Mixed editorial video styles, timed ElevenLabs narration, cue-based sound design."""
import argparse, hashlib, json, math, re, subprocess, wave
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import documentary as core
from eleven_audio import words as timed_words

FF=core.FF
INK='#151C25';PAPER='#F5F1E8';AMBER='#FFB347';MINT='#68D8C3'
BRAND='LĂNG KÍNH';SIGNATURE='TYRANNO'

def font(n,bold=False):return ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf' if bold else 'C:/Windows/Fonts/arial.ttf',n)
def text(d,xy,s,n=40,fill=PAPER,bold=False):d.text(xy,s,font=font(n,bold),fill=fill)
def lines(d,xy,rows,n=70,fill=PAPER,gap=1.18,bold=True):
    x,y=xy
    for row in rows:text(d,(x,y),row,n,fill,bold);y+=int(n*gap)

def prepare_audio(b):
    d=core.load(b/'batch.json');original=b/'audio/narration-original.mp3';length=core.duration(original);speed=length/(d['duration_seconds']-1)
    if not .8<=speed<=1.22:raise ValueError('Narration needs a script revision rather than excessive time compression: '+str(length))
    core.run([FF,'-v','error','-y','-i',str(original),'-af',f'atempo={speed:.9f},apad=whole_dur=50,afade=t=out:st=49.7:d=0.3','-t','50',str(b/'narration.wav')])
    a=core.load(original.with_suffix('.alignment.json'));rows=timed_words(a)
    for row in rows:row['start']/=speed;row['end']/=speed
    if rows[-1]['end']>49.7:raise ValueError('Speech would collide with outro fade')
    core.save(b/'aligned-words.json',rows)
    core.save(b/'voice-info.json',{'provider':'ElevenLabs','voice':d['voice'],'original_duration':length,'atempo':speed,'last_word_end':rows[-1]['end'],'timing_source':'provider character alignment of exact take','synthetic':True})
    core.subtitles(b)
    p=b/'captions.ass';s=p.read_text(encoding='utf-8-sig').replace('Arial,40,',f"Arial,{d.get('caption_font_size',43)},").replace('&HADC66A&','&H47B3FF&')
    p.write_text(s,encoding='utf-8-sig')
    print('VOICE_ALIGNED',round(length,2),round(speed,3),flush=True)

def overlay(b,index,shot):
    im=Image.new('RGBA',(1920,1080));dr=ImageDraw.Draw(im);style=shot['style']
    for y in range(820,1080):dr.line((0,y,1920,y),fill=(0,0,0,int(165*(y-820)/260)))
    if style=='hero':
        for x in range(1400):dr.line((x,170,x,820),fill=(15,21,28,int(190*(1-x/1400))))
        text(dr,(115,265),'TIỀN ĐI QUA HAY GIÁ TRỊ Ở LẠI?',30,MINT,True)
        text(dr,(108,322),'1.000',190,PAPER,True);text(dr,(125,540),'TỶ USD',79,AMBER,True)
        dr.rectangle((125,665,625,669),fill=AMBER);text(dr,(125,703),'Xuất + nhập khẩu  /  10 tháng 2026',30,PAPER)
    elif style=='editorial' and index==2:
        dr.rectangle((0,160,695,875),fill=(*ImageColor(INK),245))
        text(dr,(100,250),'01 / ĐỌC ĐÚNG CON SỐ',27,MINT,True)
        lines(dr,(98,345),['QUY MÔ','THƯƠNG MẠI'],69)
        text(dr,(100,545),'≠',120,AMBER,True);text(dr,(102,705),'LỢI NHUẬN',62,PAPER,True)
        text(dr,(1180,185),'DỮ KIỆN  /  BÌNH LUẬN',22,PAPER)
        if shot.get('source_note'):
            dr.rectangle((930,730,1835,850),fill=(*ImageColor(INK),225));text(dr,(960,755),shot['source_note'],25,PAPER)
    elif style=='editorial':
        panel_width=shot.get('panel_width',760)
        dr.rectangle((0,160,panel_width,875),fill=(*ImageColor(PAPER),250))
        text(dr,(100,220),'03 / NĂNG LỰC NỘI SINH',27,INK,True)
        for n,(label,y) in enumerate([('Công nghệ',340),('Thiết kế',480),('Thương hiệu',620)],1):
            text(dr,(100,y),f'0{n}',32,'#887D6D');text(dr,(178,y-10),label,shot.get('panel_font',60),INK,True)
            dr.line((100,y+92,panel_width-80,y+92),fill='#D2CABD',width=2)
    elif style=='split':
        dr.rectangle((947,0,973,900),fill=INK)
        if index==3:
            labels=['HÀNG BÁN RA','HÀNG MUA VÀO']
        else:labels=['DOANH NGHIỆP','GIÁ TRỊ GIỮ LẠI']
        labels=shot.get('labels',labels)
        for x,label in zip([95,1040],labels):
            dr.rounded_rectangle((x,230,x+650,310),12,fill=(*ImageColor(INK),210));text(dr,(x+23,245),label,36,AMBER,True)
        text(dr,(95,800),shot.get('split_note','02 / TỪ DOANH THU ĐẾN GIÁ TRỊ'),24,PAPER)
    elif style=='filmstrip':
        dr.rectangle((0,0,1920,195),fill=INK)
        text(dr,(890,91),'MỘT VÍ DỤ ĐỂ DỄ HÌNH DUNG',29,AMBER,True)
        for x in [56,683,1310]:dr.rectangle((x,235,x+554,796),outline=PAPER,width=3)
        text(dr,(90,828),'Đơn hàng',31,PAPER);text(dr,(718,828),'Đầu vào',31,MINT);text(dr,(1345,828),'Giá trị',31,AMBER)
    elif style=='inset':
        dr.rectangle((80,300,890,740),fill=(*ImageColor(INK),225))
        text(dr,(123,342),'CÂU HỎI CỐT LÕI',27,MINT,True)
        lines(dr,(120,422),['GIỮ LẠI','BAO NHIÊU?'],72)
        dr.rectangle((1030,246,1834,804),outline=AMBER,width=4)
    elif style=='full_bleed' and index==1:
        dr.rounded_rectangle((110,250,850,450),18,fill=(*ImageColor(INK),215))
        text(dr,(150,275),'NHƯNG KHOAN.',62,AMBER,True)
        text(dr,(152,363),'Đó không phải lợi nhuận.',38,PAPER)
    elif style=='full_bleed' and index==5:
        dr.rectangle((85,680,785,825),fill=(*ImageColor(INK),220))
        text(dr,(115,704),'TIỀN ĐI QUA ≠ TIỀN Ở LẠI',35,PAPER,True)
    elif style=='full_bleed' and index==9:
        if shot.get('text_backplate'):
            dr.rounded_rectangle((80,150,860,475),16,fill=(*ImageColor(INK),220))
        text(dr,(110,185),'04 / THƯỚC ĐO DÀI HẠN',25,MINT,True)
        lines(dr,(110,250),['NĂNG SUẤT','VÀ THU NHẬP'],65)
    elif style=='closing':
        dr.rectangle((0,0,1920,1080),fill=(9,16,24,110))
        text(dr,(120,170),BRAND+'  /  '+SIGNATURE,27,MINT,True)
        lines(dr,(117,300),['BÁN NHIỀU HƠN,','HAY LÀM CHỦ','NHIỀU HƠN?'],94)
        dr.line((125,720,600,720),fill=AMBER,width=5)
    # Draw identity last, including over the filmstrip canvas. A dark backplate
    # keeps the light wordmark readable over sky and other bright footage.
    if style not in ['full_bleed','closing'] and not shot.get('hide_badge',False):
        dr.rounded_rectangle((58,54,430,158),12,fill=(*ImageColor(INK),215))
        dr.line((78,80,78,124),fill=AMBER,width=5);dr.line((78,80,104,80),fill=AMBER,width=5)
        text(dr,(116,73),BRAND,31,PAPER,True);text(dr,(119,115),' '.join(SIGNATURE),15,MINT)
    p=b/'overlays'/f'{index+1:02}.png';im.save(p);return p

def ImageColor(color):return tuple(int(color[x:x+2],16) for x in [1,3,5])

def make_shots(b):
    global INK,PAPER,AMBER,MINT,BRAND,SIGNATURE
    d=core.load(b/'batch.json');palette=d['brand']['palette'];INK=palette['ink'];PAPER=palette['paper'];AMBER=palette['amber'];MINT=palette['mint'];BRAND=d['brand']['name'];SIGNATURE=d['brand']['signature']
    (b/'overlays').mkdir(exist_ok=True);(b/'shots').mkdir(exist_ok=True)
    for i,s in enumerate(d['shots']):
        ov=overlay(b,i,s);source=b/s['file'];target=b/'shots'/f'{i+1:02}.mp4';meta=target.with_suffix('.json')
        source_bytes=source.read_bytes()
        for field in ['secondary','tertiary']:
            if s.get(field):source_bytes+=(b/s[field]).read_bytes()
        sig=hashlib.sha256(json.dumps(s,sort_keys=True).encode()+source_bytes+ov.read_bytes()+Path(__file__).read_bytes()).hexdigest()
        if target.exists() and meta.exists() and core.load(meta).get('hash')==sig:continue
        if core.duration(source)<s['in']+s['seconds']-.04:raise ValueError('Source interval too short')
        inputs=['-ss',str(s['in']),'-i',str(source)]
        secondary=b/s.get('secondary',s['file']);style=s['style']
        if style in ['split','filmstrip','inset']:inputs+=['-ss',str(s.get('secondary_in',0)),'-i',str(secondary)]
        if style=='filmstrip':inputs+=['-ss','0','-i',str(b/s['tertiary'])]
        ov_index=3 if style=='filmstrip' else (2 if style in ['split','inset'] else 1)
        # The alpha fade needs a real overlay timeline. A one-frame image would
        # freeze at alpha=0 and silently hide every brand/typographic layer.
        inputs+=['-loop','1','-framerate','30','-i',str(ov)]
        grade=d.get('base_grade','eq=brightness=-0.035:saturation=0.9:contrast=1.04')
        if '1673' in str(source):grade='eq=brightness=0.01:gamma=1.12:saturation=0.9'
        grade=s.get('grade',grade)
        scale=lambda w,h:f'scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},setsar=1,fps=30,{grade}'
        if style=='split':
            graph=f'[0:v]{scale(960,1080)}[left];[1:v]{scale(960,1080)}[right];[left][right]hstack=inputs=2[bg]'
        elif style=='filmstrip':
            # Three moving windows, not a still collage; timelines remain continuous.
            graph=f"[0:v]{scale(554,558)}[l];[1:v]{scale(554,558)}[m];[2:v]{scale(554,558)}[r];color=c=0x151C25:s=1920x1080:r=30[canvas];[canvas][l]overlay=56:236[v1];[v1][m]overlay=683:236[v2];[v2][r]overlay=1310:236[bg]"
        elif style=='inset':
            graph=f'[0:v]{scale(1920,1080)},gblur=sigma=12[back];[1:v]{scale(800,554)}[front];[back][front]overlay=1032:248[bg]'
        else:graph=f'[0:v]{scale(1920,1080)}[bg]'
        graph+=f';[{ov_index}:v]format=rgba,fade=t=in:st=0:d=0.22:alpha=1[ov];[bg][ov]overlay=0:0,format=yuv420p,setsar=1,setparams=range=tv:color_primaries=bt709:color_trc=bt709:colorspace=bt709[v]'
        core.run([FF,'-v','error','-y']+inputs+['-filter_complex',graph,'-map','[v]','-an','-frames:v',str(round(s['seconds']*30)),'-c:v','libx264','-preset','fast','-crf','20',str(target)])
        core.save(meta,{'hash':sig,'style':style,'frames':round(s['seconds']*30),'sources':[s['file'],str(secondary.relative_to(b))]})
        print('STYLE_SHOT',i+1,style,flush=True)

def pcm(p):
    raw=core.run([FF,'-v','error','-i',str(p),'-f','f32le','-ar','48000','-ac','2','pipe:1']).stdout
    return np.frombuffer(raw,dtype='<f4').reshape((-1,2)).copy()

def sound_design(b):
    d=core.load(b/'batch.json');sr=48000;mix=np.zeros((50*sr,2),np.float32);events=[]
    def lay(name,at,gain_db,seconds=None):
        x=pcm(b/'audio'/f'{name}.mp3')
        if seconds:x=x[:int(seconds*sr)]
        peak=max(float(np.max(np.abs(x))),.001);x=x/peak*10**(gain_db/20)
        fade=min(int(.04*sr),len(x)//2);x[:fade]*=np.linspace(0,1,fade)[:,None];x[-fade:]*=np.linspace(1,0,fade)[:,None]
        a=int(at*sr);n=min(len(x),len(mix)-a);mix[a:a+n]+=x[:n]
        events.append({'file':f'audio/{name}.mp3','at':at,'peak_gain_db':gain_db,'used_seconds':n/sr})
    for cue in d['sound_effects']:lay(cue['name'],cue['at'],cue['gain_db'])
    lay('port',0,-30,3.4);lay('port',45,-33,4.8)
    with wave.open(str(b/'effects.wav'),'wb') as f:
        f.setnchannels(2);f.setsampwidth(2);f.setframerate(sr);f.writeframes((np.clip(mix,-.95,.95)*32767).astype('<i2').tobytes())
    core.save(b/'sound-cue-sheet.json',{'events':events,'effects_bus_peak_db':20*math.log10(max(float(np.max(abs(mix))),1e-9)),'music_source':'original locally synthesized harmonic bed; rebalanced and ducked','voice_priority':True})
    core.music(b)

def render(b):
    prepare_audio(b);make_shots(b);sound_design(b);d=core.load(b/'batch.json')
    (b/'concat.txt').write_text('\n'.join("file 'shots/%02d.mp4'"%(i+1) for i in range(len(d['shots']))),encoding='utf-8')
    core.run([FF,'-v','error','-y','-f','concat','-safe','0','-i',str(b/'concat.txt'),'-c','copy',str(b/'picture.mp4')])
    graph="[0:v]ass=captions.ass,fade=t=out:st=49.7:d=0.3[v];[1:a]loudnorm=I=-16:TP=-2:LRA=8,asplit=2[voice][key];[2:a]volume=0.72,aresample=48000[m];[m][key]sidechaincompress=threshold=0.025:ratio=6:attack=12:release=240[duck];[voice][duck][3:a]amix=inputs=3:normalize=0:duration=first,alimiter=limit=0.89:level=false,afade=t=out:st=49.6:d=0.4[a]"
    cmd=[FF,'-v','error','-y','-i','picture.mp4','-i','narration.wav','-i','original-music.wav','-i','effects.wav','-filter_complex',graph,'-map','[v]','-map','[a]','-frames:v','1500','-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart','final.mp4']
    r=subprocess.run(cmd,cwd=b,capture_output=True)
    if r.returncode:raise RuntimeError(r.stderr.decode(errors='replace')[-2000:])
    core.save(b/'render-profile.json',{'name':'Lăng Kính / Tyranno','styles':list(dict.fromkeys(x['style'] for x in d['shots'])),'mic':False,'waveform':False,'frames':1500,'sound_cues':len(d['sound_effects']),'version':2})
    print('RENDERED_MIXED_EDITORIAL',flush=True)

def qa(b):
    core.qa(b)
    r=subprocess.run([FF,'-hide_banner','-i',str(b/'final.mp4'),'-vn','-af','loudnorm=I=-16:TP=-1:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True)
    matches=re.findall(r'\{[^{}]*"input_i"[^{}]*\}',r.stderr,re.S)
    if not matches:raise ValueError('No final audio loudness measurement')
    levels=json.loads(matches[-1]);core.save(b/'audio-levels.json',levels)
    if float(levels['input_tp'])>-.7:raise ValueError('Audio peak exceeds headroom')
    q=core.load(b/'verification.json');q.update(render_profile=core.load(b/'render-profile.json'),audio_levels=levels,user_acceptance='pending');core.save(b/'verification.json',q)
    print('FINAL_AUDIO',levels['input_i'],'LUFS',levels['input_tp'],'dBTP',flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('stage',choices=['render','qa']);p.add_argument('--batch',type=Path,required=True);a=p.parse_args()
    (render if a.stage=='render' else qa)(a.batch.resolve())
