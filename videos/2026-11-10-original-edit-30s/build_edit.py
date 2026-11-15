from pathlib import Path
import math,json,wave,subprocess
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageFilter
import imageio_ffmpeg
p=Path(__file__).resolve().parent
W,H=720,1280
ink='#143d42';teal='#197c7e';gold='#efb744';cream='#f6f1e8'
def font(s):return ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',s)
def center(d,xy,text,size,color):
 b=d.textbbox((0,0),text,font=font(size));d.text((xy[0]-(b[2]-b[0])/2,xy[1]),text,font=font(size),fill=color)
def card(kind):
 im=Image.new('RGB',(W,H),cream);d=ImageDraw.Draw(im)
 d.ellipse((-160,-130,430,460),fill='#e3eae0');d.ellipse((500,980,950,1430),fill='#ead9b6')
 d.rounded_rectangle((34,38,686,1240),radius=30,outline='#ced7c9',width=2)
 d.rounded_rectangle((268,103,452,147),radius=22,fill=ink);center(d,(360,112),'CÂU CHUYỆN',20,'white')
 if kind==1:
  center(d,(360,212),'MỘT CHUYẾN',46,ink);center(d,(360,273),'THIỆN NGUYỆN',55,teal)
  # A gift illustration: shadow, box, ribbon and paper bow.
  d.ellipse((147,850,587,923),fill='#dad7cc')
  d.rounded_rectangle((185,610,535,877),radius=20,fill=teal)
  d.rounded_rectangle((161,574,559,651),radius=15,fill='#2f9994')
  d.rectangle((325,574,395,877),fill=gold)
  d.ellipse((244,471,363,589),outline=gold,width=22);d.ellipse((357,471,476,589),outline=gold,width=22)
  d.ellipse((338,554,382,598),fill=gold)
  for x,y in [(125,490),(585,565),(143,790),(578,820)]:
   d.line((x-12,y,x+12,y),fill=gold,width=4);d.line((x,y-12,x,y+12),fill=gold,width=4)
  center(d,(360,1005),'Một câu chuyện.',31,ink);center(d,(360,1055),'Một trải nghiệm.',31,ink)
 else:
  center(d,(360,212),'ĐIỂM ĐẾN',27,teal);center(d,(360,265),'BỆNH VIỆN',48,ink);center(d,(360,326),'NHI ĐỒNG 2',58,teal)
  d.ellipse((121,866,599,928),fill='#dad7cc')
  d.rounded_rectangle((180,540,540,887),radius=20,fill='#d5e8e3')
  d.rectangle((289,467,431,887),fill=teal)
  d.rounded_rectangle((309,487,411,585),radius=16,fill=cream)
  d.rectangle((349,503,370,569),fill=gold);d.rectangle((327,525,391,546),fill=gold)
  for x in [204,464]:
   for y in [591,676,761]:d.rounded_rectangle((x,y,x+51,y+47),radius=7,fill='#79b6af')
  d.rounded_rectangle((321,797,399,887),radius=8,fill=ink)
  center(d,(360,1007),'CHUYẾN ĐI ĐƯỢC KỂ LẠI',28,ink)
  center(d,(360,1060),'Qua lời kể của nhân vật',24,teal)
 im.save(p/f'card-{kind}.png')
card(1);card(2)
# Sparse original instrumental bed, no sampled or externally sourced music.
sr=44100;dur=30;t=np.arange(sr*dur)/sr;music=np.zeros_like(t)
def note(start,length,freq,amp):
 global music
 a=int(start*sr);n=min(int(length*sr),len(music)-a)
 if n<=0:return
 q=np.arange(n)/sr;env=(1-np.exp(-q*45))*np.exp(-q*1.8)*np.minimum(1,(length-q)*5)
 sig=(np.sin(2*np.pi*freq*q)+.23*np.sin(2*np.pi*freq*2*q)+.07*np.sin(2*np.pi*freq*3*q))*env
 music[a:a+n]+=amp*sig
chords=[[261.63,329.63,392.0],[220,261.63,329.63],[174.61,220,261.63],[196,246.94,293.66]]
for bar in range(10):
 start=bar*3.2
 for j,f in enumerate(chords[bar%4]):note(start+j*.29,2.8,f,.12)
 if bar%2==0:note(start+1.6,2.0,chords[bar%4][2]*2,.045)
music*=np.minimum(t/1.2,1)*np.minimum((30-t)/1.1,1)
# Quiet under the original voice, slightly fuller in the source's long pause.
gain=np.where((t>7.4)&(t<17.6),.52,.26);music*=gain
st=np.stack([music,np.roll(music,int(sr*.018))],axis=1)
with wave.open(str(p/'music-original.wav'),'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(sr);w.writeframes((np.clip(st,-1,1)*32767).astype('<i2').tobytes())
# Only legible emphasis phrases where the source words are clear; no invented verbatim ASR.
head='''[Script Info]
ScriptType: v4.00+
PlayResX: 720
PlayResY: 1280
WrapStyle: 2
ScaledBorderAndShadow: yes
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Main,Arial,40,&H00FFFFFF,&H0000FFFF,&H0013262B,&H64000000,-1,0,0,0,100,100,0,0,1,3,1,2,35,35,204,1
Style: Top,Arial,26,&H00FFFFFF,&H0000FFFF,&H0013262B,&H64000000,-1,0,0,0,100,100,1,0,1,2,0,8,30,30,94,1
Style: Big,Arial,53,&H0044D3FF,&H0000FFFF,&H0013262B,&H64000000,-1,0,0,0,100,100,0,0,1,4,1,2,30,30,211,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
def tm(x):return f'{int(x)//3600}:{int(x)//60%60:02}:{int(x)%60:02}.{int(round(x%1*100)):02}'
rows=[]
def cue(a,b,txt,style='Main'):
 rows.append(f'Dialogue: 2,{tm(a)},{tm(b)},{style},,0,0,0,,{{\\fad(100,100)}}{txt}')
cue(.1,7.4,'MỘT CÂU CHUYỆN • MỘT TRẢI NGHIỆM','Top')
cue(1.96,3.45,'Em xin kể về\\Nmột câu chuyện')
cue(3.52,4.6,'MỘT TRẢI NGHIỆM','Big')
# Use a thematic card instead of guessing the unclear end of the opening sentence.
cue(18,19.84,'Tôi từng có dịp\\Ncùng thầy tôi')
cue(19.84,22.12,'MỘT CHUYẾN\\NTHIỆN NGUYỆN','Big')
cue(22.12,24.1,'BỆNH VIỆN\\NNHI ĐỒNG 2','Big')
cue(24.58,25.88,'Nơi chúng tôi chuẩn bị')
cue(25.88,27.48,'và trao quà cho')
cue(27.48,28.9,'HƠN 100 EM NHỎ','Big')
cue(28.9,30,'đang điều trị bệnh')
(p/'emphasis.ass').write_text(head+'\n'.join(rows)+'\n',encoding='utf-8-sig')
src='C:/Users/tyranno/Documents/output/2aOboRBgAQPTOVBDeyiJ3DUdElfGnNoIsHObfk48.mp4'
# Framing changes retain exact source timestamps and audio/video synchronization.
filt="""[0:v]trim=duration=30,setpts=PTS-STARTPTS,crop=648:1152:36:108,scale=1440:2560,zoompan=z='if(between(on,57,224),1.09,if(between(on,540,659),1.065,if(between(on,824,899),1.10,1.0)))':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=720x1280:fps=30,eq=brightness=0.012:saturation=1.045:contrast=1.025[base];
[1:v]scale=1440:2560,zoompan=z='1+0.000045*on':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=720x1280:fps=30,format=rgba,fade=t=in:st=8.1:d=0.28:alpha=1,fade=t=out:st=12.55:d=0.28:alpha=1[c1];
[base][c1]overlay=enable='between(t,8.1,12.83)':eof_action=pass[v1];
[2:v]scale=1440:2560,zoompan=z='1+0.00004*on':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=720x1280:fps=30,format=rgba,fade=t=in:st=12.7:d=0.28:alpha=1,fade=t=out:st=17.45:d=0.3:alpha=1[c2];
[v1][c2]overlay=enable='between(t,12.7,17.75)':eof_action=pass,ass=emphasis.ass,format=yuv420p,fade=t=out:st=29.8:d=0.2[v];
[0:a]atrim=duration=30,asetpts=PTS-STARTPTS,highpass=f=90,afftdn=nr=6:nf=-38,loudnorm=I=-16:TP=-1.5:LRA=9[voice];
[voice][3:a]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.94:level=false,afade=t=out:st=29.85:d=0.15[a]"""
(p/'filtergraph.txt').write_text(filt,encoding='utf8')
cmd=[imageio_ffmpeg.get_ffmpeg_exe(),'-hide_banner','-y','-i',src,'-loop','1','-i','card-1.png','-loop','1','-i','card-2.png','-i','music-original.wav','-filter_complex_script','filtergraph.txt','-map','[v]','-map','[a]','-t','30','-r','30','-c:v','libx264','-preset','medium','-crf','18','-c:a','aac','-b:a','192k','-ar','44100','-movflags','+faststart','video-hoan-chinh-30s.mp4']
with (p/'render.log').open('w',encoding='utf8') as log:r=subprocess.run(cmd,cwd=p,stdout=log,stderr=subprocess.STDOUT)
print('render exit',r.returncode,flush=True)
if r.returncode: print((p/'render.log').read_text(encoding='utf8')[-4000:]);raise SystemExit(r.returncode)
