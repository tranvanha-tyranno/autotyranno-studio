"""Reference-inspired paper teaching renderer; preserves v1 and reuses its audio."""
from __future__ import annotations
import argparse
from functools import lru_cache
import hashlib
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
import textwrap

from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg
import sql_priority as lesson

HERE=Path(__file__).resolve().parent
PROFILE=json.loads((HERE/"paper_classroom.json").read_text(encoding="utf-8"))
P=PROFILE["palette"]
W,H,FPS=1080,1350,30
S=1.2
FF=imageio_ffmpeg.get_ffmpeg_exe()


@lru_cache(maxsize=128)
def font(size,bold=False,mono=False):
    filename="consolab.ttf" if mono and bold else "consola.ttf" if mono else "timesbd.ttf" if bold else "times.ttf"
    return ImageFont.truetype(str(Path("C:/Windows/Fonts")/filename),round(size*S))


def ease(t,start=0,length=.7):
    v=max(0,min(1,(t-start)/length))
    return 1-(1-v)**3


class Page:
    def __init__(self):
        self.im=Image.new("RGB",(W,H),P["paper"])
        self.d=ImageDraw.Draw(self.im)
        self.bounds=[]

    def box(self,x,y,w,h,fill=None,stroke=None,r=8,line=1.5):
        self.d.rounded_rectangle([round(z*S) for z in (x,y,x+w,y+h)],
            radius=round(r*S),fill=fill,outline=stroke,width=max(1,round(line*S)))

    def line(self,pts,color=None,width=1.5):
        self.d.line([(round(x*S),round(y*S)) for x,y in pts],
                    fill=color or P["ink"],width=max(1,round(width*S)))

    def txt(self,x,y,text,size=24,color=None,bold=False,mono=False,center=False):
        f=font(size,bold,mono)
        if center:x-=f.getlength(str(text))/S/2
        self.d.text((round(x*S),round(y*S)),str(text),font=f,
                    fill=color or P["text"],anchor="lt")
        self.bounds.append((x,y,f.getlength(str(text))/S,size*1.25,str(text)))

    def wrap(self,x,y,text,width,size=25,color=None,bold=False,center=False):
        lines=[];current=""
        for word in text.split():
            trial=(current+" "+word).strip()
            if current and font(size,bold).getlength(trial)>width*S:
                lines.append(current);current=word
            else:current=trial
        if current:lines.append(current)
        for n,line in enumerate(lines):
            self.txt(x+width/2 if center else x,y+n*size*1.2,line,size,color,bold,center=center)
        return len(lines)*size*1.2

    def arrow(self,x1,y1,x2,y2,progress=1,color=None,bend=0):
        if progress<=0:return
        color=color or P["ink"]
        points=[]
        for i in range(max(2,round(40*progress))):
            t=progress*i/(max(2,round(40*progress))-1)
            x=x1+(x2-x1)*t
            y=y1+(y2-y1)*t+math.sin(math.pi*t)*bend
            points.append((x,y))
        self.line(points,color,1.8)
        x,y=points[-1];px,py=points[-2];angle=math.atan2(y-py,x-px)
        self.line([(x-10*math.cos(angle-.45),y-10*math.sin(angle-.45)),(x,y),
                   (x-10*math.cos(angle+.45),y-10*math.sin(angle+.45))],color,1.8)

    def underline(self,x,y,w,color=None,progress=1):
        self.line([(x,y),(x+w*.5*progress,y+1),(x+w*progress,y-1)],color or P["orange_ink"],2.5)


HEADINGS=[
    "Đúng số dòng — chưa chắc đúng người!",
    "Bài toán ở trung tâm hỗ trợ",
    "SELECT & FROM: chọn dữ liệu",
    "WHERE: đi qua ba bộ lọc",
    "ORDER BY: ai được ưu tiên?",
    "LIMIT / OFFSET: chia trang",
    "Thứ tự viết ≠ thứ tự logic",
    "Từ danh sách đến đúng ưu tiên",
]


def checklist(p,scene):
    p.box(586,21,276,135,P["yellow"],None,r=0)
    p.box(676,11,78,20,"#b7cde3",None,r=0)
    p.txt(604,35,"Cần trả lời điều gì?",21,P["orange_ink"],True)
    items=["Lọc đúng phiếu","Xếp đúng ưu tiên","Lấy đúng trang"]
    complete=0 if scene<3 else 1 if scene<4 else 2 if scene<5 else 3 if scene==7 else 2
    for i,label in enumerate(items):
        y=67+i*27
        p.box(604,y,17,17,None,P["ink"],r=0,line=1)
        if i<complete:
            p.line([(606,y+8),(611,y+14),(620,y+1)],P["green_ink"],2)
        p.txt(632,y-1,label,21,P["ink"])


def header(p,scene,t,duration):
    p.box(38,25,51,51,P["blue"],P["ink"],r=26)
    p.txt(63.5,40,"SQL",20,P["ink"],True,center=True)
    p.txt(102,29,"HỌC SQL QUA TÌNH HUỐNG",18,P["ink"],True)
    p.txt(102,54,"Từ dữ liệu đến quyết định",18,P["text"])
    p.box(38,99,127,28,None,P["ink"],r=14)
    p.txt(101,105,f"BÀI {scene+1:02} / 08",17,P["ink"],True,center=True)
    p.wrap(38,183,HEADINGS[scene],824,33,P["ink"],True)
    p.underline(39,230,320,P["orange_ink"],ease(t,0,.7))
    checklist(p,scene)
    p.line([(38,1112),(862,1112)],"#deddd7",1)
    p.line([(38,1112),(38+824*(scene+t/duration)/8,1112)],P["green_ink"],2)


def stages(p,items,active):
    width=(824-16*(len(items)-1))/len(items)
    for i,label in enumerate(items):
        x=38+i*(width+16)
        p.box(x,261,width,37,P["ink"] if i==active else P["paper"],P["ink"],r=18)
        p.txt(x+width/2,271,label,19,P["paper"] if i==active else P["ink"],True,center=True)


def table(p,x,y,rows,width=350,cols=(0,2,3),title="tickets",green=False,
          highlights=(),muted=(),rowh=41,highlight_color=None,positions=None):
    color=P["green_ink"] if green else P["ink"]
    fill=P["green"] if green else P["blue"]
    labels={0:"id",1:"status",2:"channel",3:"wait_min"}
    sizes={2:[.5,.5],3:[.25,.35,.4],4:[.19,.27,.24,.30]}[len(cols)]
    xs=[x]
    for f in sizes:xs.append(xs[-1]+width*f)
    tag_w=min(width,max(105,font(21,True).getlength(title)/S+28))
    p.box(x+(width-tag_w)/2,y-27,tag_w,28,color,None,r=0)
    p.txt(x+width/2,y-23,title,21,P["paper"],True,center=True)
    height=38+len(rows)*rowh
    p.box(x,y,width,height,P["paper"],color,r=0)
    p.box(x+1,y+1,width-2,36,fill,None,r=0)
    for j,col in enumerate(cols):
        p.txt((xs[j]+xs[j+1])/2,y+9,labels[col],19,color,True,mono=True,center=True)
    for j,r in enumerate(rows):
        yy=y+38+(positions[j] if positions else j)*rowh
        if r[0] in highlights:
            p.box(x+3,yy+3,width-6,rowh-6,highlight_color or "#f8d5ad",None,r=0)
        for k,col in enumerate(cols):
            p.txt((xs[k]+xs[k+1])/2,yy+10,str(r[col]),22,
                  "#a3a6a6" if r[0] in muted else P["text"],center=True)
        if positions is None:p.line([(x,yy+rowh),(x+width,yy+rowh)],"#aebbc2",.7)
    for xx in xs[1:-1]:p.line([(xx,y),(xx,y+height)],"#aebbc2",.7)
    p.line([(x,y+38),(x+width,y+38)],color,1)
    p.box(x,y,width,height,None,color,r=0)
    return height


def sql(p,x,y,lines,width=824,active=(),size=23,rowh=35):
    p.box(x,y,width,26+len(lines)*rowh,P["blue"],P["ink"],r=6)
    for i,line in enumerate(lines):
        if i in active:p.box(x+8,y+7+i*rowh,width-16,rowh,P["yellow"],None,r=1)
        p.txt(x+17,y+13+i*rowh,line,size,P["ink"],mono=True,bold=i in active)


def takeaway(p,text,y=935,color=None):
    size=26
    if font(size,True).getlength(text)/S>810:size=23
    width=font(size,True).getlength(text)/S
    p.box(450-width/2-6,y+14,width+12,17,"#fbe5a9",None,r=0)
    p.txt(450,y,text,size,color or P["ink"],True,center=True)


def caption(p,t,cues):
    p.box(38,1001,824,94,"#f8f7f0","#e4e1d8",r=4,line=.7)
    p.box(69,990,66,17,"#f1cfb6",None,r=0)
    p.box(761,990,65,17,"#f1cfb6",None,r=0)
    current=next((c["text"] for c in cues if c["start"]<=t<c["end"]),None)
    if current:
        p.wrap(62,1019,current,776,26,P["text"],center=True)
    else:
        p.txt(450,1032,"•  •  •",23,"#a8aba7",center=True)


def beat(cues,needle,default):
    needle=needle.casefold()
    words=[w for cue in cues for w in cue.get("words",[])]
    normalize=lambda s:re.sub(r"[^\w]","",s.casefold())
    wanted=[normalize(w) for w in needle.split()]
    for i in range(len(words)-len(wanted)+1):
        if [normalize(w["text"]) for w in words[i:i+len(wanted)]]==wanted:
            return words[i]["start"]
    # Find tokens in concatenated cues, including phrases straddling cue boundaries.
    for i,cue in enumerate(cues):
        combined=" ".join(c["text"] for c in cues[i:i+2]).casefold()
        if needle in combined:return cue["start"]
    return default


def person(p,x,y,t):
    """Original simple support-agent illustration, not reference artwork."""
    p.box(x+25,y+100,108,130,P["blue"],P["ink"],r=35)
    p.box(x+40,y+26,80,93,"#f5ddc8",P["ink"],r=40)
    p.box(x+38,y+17,84,38,P["ink"],None,r=20)
    p.box(x+42,y+37,72,25,"#f5ddc8",None,r=10)
    for xx in (x+64,x+97):p.box(xx,y+65,4,5,P["ink"],None,r=2)
    p.line([(x+72,y+90),(x+80,y+94),(x+90,y+90)],P["orange_ink"],2)
    p.line([(x+36,y+60),(x+27,y+67),(x+27,y+94),(x+53,y+102)],P["ink"],3)
    p.box(x+20,y+74,15,27,P["ink"],None,r=5)
    p.box(x+60,y+137,43,60,P["paper"],P["ink"],r=3)
    p.txt(x+81,y+154,"?",24,P["ink"],True,center=True)
    p.txt(x+80,y+250,"Bộ phận hỗ trợ",23,P["ink"],True,center=True)


def frame(scene,t,duration,cues):
    p=Page()
    header(p,scene,t,duration)
    if scene==0:
        stages(p,["1 · Yêu cầu","2 · Kết quả","3 · Vấn đề"],min(2,int(t/4)))
        p.wrap(75,340,"Lấy 3 khách hàng cần hỗ trợ gấp nhất.",750,31,P["ink"],True,True)
        table(p,80,445,[lesson.ROWS[0],lesson.ROWS[4],lesson.ROWS[7]],340,
              title="Hệ thống trả về",highlights=(101,))
        p.txt(665,433,"Nhưng còn phiếu này?",25,P["red"],True,center=True)
        reveal=ease(t,beat(cues,"90 phút",4),.8)
        if reveal>0:
            y=491+30*(1-reveal)
            p.box(510,y,310,99,"#fff0ed",P["red"])
            p.txt(665,y+16,"#104  ·  WEB",25,P["red"],True,center=True)
            p.txt(665,y+54,"ĐÃ CHỜ 90 PHÚT",27,P["red"],True,center=True)
            p.arrow(510,545,431,545,reveal,P["red"],-22)
        if t>5:
            p.txt(450,723,"TRẢ ĐÚNG 3 DÒNG",33,P["ink"],True,center=True)
            p.txt(450,772,"≠",49,P["orange_ink"],True,center=True)
            p.txt(450,837,"CHỌN ĐÚNG 3 DÒNG",33,P["ink"],True,center=True)
        takeaway(p,"SQL không báo lỗi. Vậy sai ở đâu?")
    elif scene==1:
        stages(p,["Tình huống","Điều kiện","Mục tiêu"],1)
        person(p,62,335,t)
        rules=[("Đang mở","status = 'open'",P["blue"],P["ink"]),
               ("App hoặc Web","channel IN (...)",P["orange"],P["orange_ink"]),
               ("Chờ ít nhất 30 phút","wait_min >= 30",P["green"],P["green_ink"])]
        for i,(title,detail,fill,col) in enumerate(rules):
            if t<i*2:continue
            yy=338+i*103+22*(1-ease(t,i*2))
            p.box(310,yy,515,85,fill,col)
            p.txt(332,yy+15,f"{i+1}. {title}",27,col,True)
            p.txt(332,yy+51,detail,20,col,mono=True)
        if t>5:
            table(p,115,728,lesson.ROWS[:3],670,cols=(0,1,2,3),title="tickets · trích 3 / 10 dòng",rowh=36)
        takeaway(p,"Chờ lâu hơn → ưu tiên trước · 3 phiếu / trang")
    elif scene==2:
        change=beat(cues,"Còn SELECT",5)
        stages(p,["FROM · bảng nguồn","SELECT · chọn cột"],0 if t<change else 1)
        sql(p,38,332,["SELECT id, channel, wait_min","FROM tickets;"],active=(1,) if t<change else (0,),size=25,rowh=40)
        table(p,50,520,lesson.ROWS[:4],405,cols=(0,1,2,3),title="Bảng tickets",rowh=46)
        if t>change:
            progress=ease(t,change)
            p.arrow(469,608,512,608,progress)
            table(p,525+25*(1-progress),520,lesson.ROWS[:4],325,
                  title="Cột được chọn",green=True,rowh=46)
            p.box(520,790,330,65,P["green"],P["green_ink"])
            p.txt(685,812,"id  ·  channel  ·  wait_min",22,P["green_ink"],True,center=True)
        p.txt(250,790,"Các dòng vẫn giữ nguyên",24,P["ink"],center=True)
        takeaway(p,"SELECT chọn cột — chưa lọc dòng!")
    elif scene==3:
        starts=[beat(cues,"Dấu bằng",3),beat(cues,"IN giúp",7),beat(cues,"lớn hơn",12)]
        stage=sum(t>=x for x in starts)
        stages(p,["1 · Trạng thái","2 · Kênh","3 · Thời gian"],max(0,stage-1))
        sql(p,38,329,["WHERE status = 'open'","  AND channel IN ('app', 'web')",
                     "  AND wait_min >= 30"],active=(max(0,stage-1),),size=24,rowh=37)
        remaining=[r for r in lesson.ROWS if (stage<1 or r[1]=="open")
                   and (stage<2 or r[2] in ("app","web")) and (stage<3 or r[3]>=30)]
        table(p,55,532,lesson.ROWS,450,cols=(0,1,2,3),title="10 phiếu đầu vào",rowh=31,
              muted=tuple(r[0] for r in lesson.ROWS if r not in remaining),
              highlights=tuple(r[0] for r in lesson.ROWS if r not in remaining),highlight_color="#f1eeee")
        p.arrow(520,660,581,660,ease(t,starts[max(0,stage-1)]),P["green_ink"])
        p.box(605,551,234,153,P["green"],P["green_ink"])
        p.txt(722,571,str(len(remaining)),56,P["green_ink"],True,center=True)
        p.txt(722,643,"phiếu còn lại",26,P["green_ink"],True,center=True)
        p.wrap(575,740,"AND: thỏa tất cả điều kiện.",285,27,P["ink"],True,True)
        if t>beat(cues,"tương đương",22):
            p.box(535,820,327,82,P["orange"],P["orange_ink"])
            p.txt(698,833,"IN ↔ (… OR …)",25,P["orange_ink"],True,center=True)
            p.txt(698,870,"BETWEEN · LIKE",20,P["orange_ink"],center=True)
        takeaway(p,"Ghép OR với AND? Nhớ dấu ngoặc.")
    elif scene==4:
        order=beat(cues,"sắp xếp số phút",6)
        tie=beat(cues,"Nếu hai phiếu",12)
        stages(p,["7 phiếu hợp lệ","Sắp xếp","Tiêu chí phụ"],0 if t<order else 1 if t<tie else 2)
        sql(p,38,332,["ORDER BY wait_min DESC, id DESC"],active=(0,),size=25,rowh=40)
        table(p,55,500,lesson.VALID,340,title="Sau WHERE",rowh=47)
        progress=ease(t,order,1.3)
        positions=[i+(lesson.SORTED.index(r)-i)*progress for i,r in enumerate(lesson.VALID)]
        table(p,505,500,lesson.VALID if progress<1 else lesson.SORTED,340,
              title="Thứ tự ưu tiên",green=True,rowh=47,
              highlights=(109,102) if t>=tie else (),positions=positions if progress<1 else None)
        for i,r in enumerate(lesson.VALID):
            if progress>0:
                p.arrow(401,561+i*47,498,561+lesson.SORTED.index(r)*47,progress,
                        P["purple_ink"] if r[3]==70 else "#9bb1bf",bend=-10)
        if t>=tie:
            p.txt(450,895,"Cùng 70 phút: #109 đứng trước #102.",26,P["orange_ink"],True,center=True)
        takeaway(p,"DESC: giảm dần · ASC: tăng dần")
    elif scene==5:
        switch=beat(cues,"Sang trang hai",12)
        page2=t>=switch
        stages(p,["1 · Sắp xếp","2 · Bỏ qua","3 · Lấy tối đa 3"],1 if page2 else 2)
        sql(p,38,331,[f"LIMIT 3 OFFSET {3 if page2 else 0};"],active=(0,),size=28,rowh=43)
        table(p,58,499,lesson.SORTED,337,title="Danh sách ưu tiên",rowh=46,
              muted=(104,109,102) if page2 else (),
              highlights=(104,109,102) if not page2 else (105,108,110),
              highlight_color=P["green"])
        start=3 if page2 else 0
        prog=ease(t,switch if page2 else 2,1)
        table(p,516+20*(1-prog),499,lesson.SORTED[start:start+3],330,
              title=f"Trang {2 if page2 else 1}",green=True,rowh=46)
        for j in range(3):
            p.arrow(405,560+(start+j)*46,507,560+j*46,prog,P["green_ink"],-15)
        p.wrap(510,739,"Bỏ qua 3 phiếu đầu." if page2 else "Không bỏ qua dòng nào.",335,27,P["orange_ink"],True,True)
        p.wrap(510,825,"Lấy tối đa 3 phiếu tiếp theo.",335,27,P["green_ink"],True,True)
        takeaway(p,"Xác định thứ tự trước khi phân trang!")
    elif scene==6:
        starts=[0,beat(cues,"lọc các dòng",8),beat(cues,"chọn các cột",10),
                beat(cues,"sắp xếp",12),beat(cues,"bỏ qua",14),beat(cues,"giới hạn",16)]
        phase=max(i for i,b in enumerate(starts) if t>=b)
        stages(p,["Cách viết SQL","Cách hiểu logic"],1)
        sql(p,38,337,lesson.SQL,width=824,
            active=({0:1,1:2,2:0,3:5,4:6,5:6}[phase],),size=24,rowh=38)
        names=["FROM","WHERE","SELECT","ORDER BY","OFFSET","LIMIT"]
        desc=["Lấy bảng","Lọc dòng","Chọn cột","Sắp xếp","Bỏ qua","Giới hạn"]
        for i,(name,label) in enumerate(zip(names,desc)):
            x=55+(i%3)*284;y=693+(i//3)*112
            fill=P["green"] if i==phase else P["purple"] if i<phase else P["paper"]
            color=P["green_ink"] if i==phase else P["purple_ink"]
            p.box(x,y,222,78,fill,color)
            p.txt(x+111,y+13,name,25,color,True,mono=True,center=True)
            p.txt(x+111,y+48,label,22,P["text"],center=True)
            if i in (0,1,3,4):p.arrow(x+228,y+38,x+272,y+38,ease(t,starts[i]),color)
        p.arrow(788,778,167,796,ease(t,starts[3]),P["purple_ink"],14)
        takeaway(p,"Thứ tự logic ≠ kế hoạch thực thi vật lý",color=P["orange_ink"])
    else:
        stages(p,["1 · Lọc đúng","2 · Xếp đúng","3 · Chọn đúng"],2)
        table(p,240,383,lesson.SORTED[:3],420,title="Đúng người cần ưu tiên",green=True,rowh=48)
        summaries=[("SELECT","Chọn cột",P["blue"],P["ink"]),
                   ("WHERE","Lọc dòng",P["orange"],P["orange_ink"]),
                   ("ORDER BY","Sắp xếp",P["purple"],P["purple_ink"]),
                   ("LIMIT / OFFSET","Phân trang",P["green"],P["green_ink"])]
        for i,(name,label,fill,color) in enumerate(summaries):
            if t<i*.65:continue
            yy=620+i*59+15*(1-ease(t,i*.65))
            p.box(113,yy,674,48,fill,color)
            p.txt(139,yy+12,name,23,color,True,mono=True)
            p.txt(605,yy+11,label,25,color,center=True)
        p.txt(450,897,"Không chỉ đúng cú pháp — phải hiểu đúng logic.",27,P["ink"],True,center=True)
        takeaway(p,"Lọc đúng → Sắp xếp đúng → Giới hạn")
    caption(p,t,cues)
    # Do not fade the caption/header between slides: classroom reference uses cuts.
    return p


def srt_time(seconds):
    millis=round(seconds*1000)
    return f"{millis//3600000:02}:{millis//60000%60:02}:{millis//1000%60:02},{millis%1000:03}"


def build(args):
    out=args.output;out.mkdir(parents=True,exist_ok=True)
    scenes=json.loads((args.source/"timed-scenes.json").read_text(encoding="utf-8"))
    captions=json.loads((out/"alignment/captions.json").read_text(encoding="utf-8"))
    shutil.copy2(HERE/"paper_classroom.json",out/"style-profile.json")
    for name in ("source-script.txt","manifest.json","data-check.json","audio-timing.json"):
        shutil.copy2(args.source/name,out/name)
    previews=out/"previews";previews.mkdir(exist_ok=True)
    sheet=Image.new("RGB",(1080,2700),P["paper"])
    timing_offset=0;subtitles=[];bounds=[]
    for i,scene in enumerate(scenes):
        d=scene["duration_seconds"];cues=captions[i]["cues"]
        folder=out/f"scene-{i+1:02}";folder.mkdir(exist_ok=True)
        audio_source=args.source/f"clip-{i+1:02}-scene-{i+1:02}"/"voice-timed.wav"
        if not (folder/"narration.wav").exists():shutil.copy2(audio_source,folder/"narration.wav")
        for cue in cues:
            subtitles.append(f"{len(subtitles)+1}\n{srt_time(timing_offset+cue['start'])} --> "
                f"{srt_time(timing_offset+cue['end'])}\n{cue['text']}\n")
        timing_offset+=d
        preview_t=d*.7
        page=frame(i,preview_t,d,cues)
        page.im.save(previews/f"scene-{i+1:02}.png")
        sheet.paste(page.im.resize((540,675)),((i%2)*540,(i//2)*675))
        for t in [0.5,d*.25,d*.5,d*.75,d-.5]:
            sample=frame(i,t,d,cues)
            for x,y,w,h,text in sample.bounds:
                if x<0 or y<0 or x+w>900.5 or y+h>1125:
                    bounds.append({"scene":i+1,"time":t,"text":text,"bounds":[x,y,w,h]})
        if args.previews:continue
        target=folder/"scene.mp4"
        if target.exists() and not args.force:continue
        with (folder/"render.log").open("w",encoding="utf-8") as log:
            process=subprocess.Popen([FF,"-hide_banner","-loglevel","warning","-y",
                "-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","pipe:0",
                "-i",str(folder/"narration.wav"),"-c:v","libx264","-preset","fast",
                "-crf","18","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k",
                "-t",str(d),"-movflags","+faststart",str(target)],stdin=subprocess.PIPE,stderr=log)
            try:
                for n in range(round(d*FPS)):
                    process.stdin.write(frame(i,n/FPS,d,cues).im.tobytes())
                process.stdin.close()
                if process.wait():raise RuntimeError(f"Scene {i+1} encoding failed")
            finally:
                if process.poll() is None:process.kill()
        print("RENDERED",i+1,flush=True)
    sheet.save(out/"storyboard-v2.jpg",quality=95)
    (out/"subtitles-vi.srt").write_text("\n".join(subtitles),encoding="utf-8-sig")
    (out/"layout-check.json").write_text(json.dumps({"overflow":bounds,"samples":40},ensure_ascii=False,indent=2),encoding="utf-8")
    if bounds:raise ValueError(f"{len(bounds)} text bounds overflows; inspect layout-check.json")
    if args.previews:return
    (out/"concat.txt").write_text("".join(f"file 'scene-{i+1:02}/scene.mp4'\n" for i in range(8)),encoding="utf-8")
    delivery=out/"SQL-paper-classroom-v2.mp4"
    subprocess.run([FF,"-v","error","-y","-f","concat","-safe","0","-i",str(out/"concat.txt"),
                    "-c","copy","-movflags","+faststart",str(delivery)],check=True)
    check=subprocess.run([FF,"-v","error","-i",str(delivery),"-f","null","-"],capture_output=True,text=True)
    probe=subprocess.run([FF,"-hide_banner","-i",str(delivery)],capture_output=True,text=True)
    (out/"media-info.txt").write_text(probe.stderr,encoding="utf-8")
    qa={"decode_passed":check.returncode==0 and not check.stderr.strip(),"decode_errors":check.stderr,
        "dimensions":[W,H],"fps":FPS,"planned_duration":timing_offset,"layout_overflows":len(bounds),
        "tts_calls":0,"muse_calls":0,"reused_narration":True,
        "caption_method":"Local ASR timestamps mapped to approved script; unmatched words interpolated",
        "model_weights_trained":False,"style_profile":"style-profile.json"}
    (out/"qa.json").write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding="utf-8")
    if not qa["decode_passed"]:raise RuntimeError("Final decode failed")
    print("COMPLETE",delivery,flush=True)


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--source",type=Path,required=True)
    parser.add_argument("--output",type=Path,required=True)
    parser.add_argument("--previews",action="store_true")
    parser.add_argument("--force",action="store_true")
    build(parser.parse_args())
