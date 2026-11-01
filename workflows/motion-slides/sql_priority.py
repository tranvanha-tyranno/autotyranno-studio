"""Render the supplied Vietnamese SQL lesson as a narrated motion-slide video.

Pillow draws deterministic graphics; FFmpeg encodes H.264/AAC. Existing local
ElevenLabs credential handling and content-addressed TTS cache are reused.
No Muse generation is needed for tables, SQL text, or precise data animation.
"""
from __future__ import annotations

import argparse
from functools import lru_cache
import importlib.util
import json
import math
from pathlib import Path
import re
import shutil
import sqlite3
import subprocess
import wave

from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

ROOT = Path(__file__).resolve().parents[2]
FF = imageio_ffmpeg.get_ffmpeg_exe()
W, H, FPS = 1920, 1080, 24
S = W / 1600
BG = "#0a1120"
PANEL = "#131f32"
LINE = "#2a3b53"
WHITE = "#f2f5fc"
MUTED = "#9dadc6"
TEAL = "#61e5c0"
BLUE = "#87b5ff"
ORANGE = "#ffbd78"
RED = "#ff7b87"
ROWS = [
    (101, "open", "app", 30), (102, "open", "web", 70),
    (103, "open", "app", 20), (104, "open", "web", 90),
    (105, "open", "app", 60), (106, "closed", "web", 120),
    (107, "open", "phone", 100), (108, "open", "web", 45),
    (109, "open", "app", 70), (110, "open", "web", 35),
]
VALID = [r for r in ROWS if r[1] == "open" and r[2] in ("app", "web") and r[3] >= 30]
SORTED = sorted(VALID, key=lambda r: (r[3], r[0]), reverse=True)
DURATIONS = [15, 20, 20, 33, 25, 27, 25, 15]
TITLES = [
    "Đủ 3 dòng. Nhưng đã đúng 3 dòng?",
    "Một hàng đợi. Bốn quy tắc.",
    "Lấy bảng nào? Hiển thị cột nào?",
    "Chỉ giữ lại phiếu thỏa mọi điều kiện",
    "Người chờ lâu hơn, được ưu tiên trước",
    "Một danh sách. Nhiều trang.",
    "Viết từ SELECT. Hiểu từ FROM.",
    "Lọc đúng. Sắp xếp đúng. Rồi giới hạn.",
]
LABELS = ["VẤN ĐỀ", "BÀI TOÁN", "SELECT / FROM", "WHERE", "ORDER BY",
          "LIMIT / OFFSET", "THỨ TỰ LOGIC", "GHI NHỚ"]
SQL = [
    "SELECT id, channel, wait_min",
    "FROM tickets",
    "WHERE status = 'open'",
    "  AND channel IN ('app', 'web')",
    "  AND wait_min >= 30",
    "ORDER BY wait_min DESC, id DESC",
    "LIMIT 3 OFFSET 0;",
]


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def ease(t, start=0, length=1):
    x = max(0, min(1, (t-start)/length))
    return x*x*(3-2*x)


@lru_cache(maxsize=128)
def font(size, bold=False, mono=False):
    name = "consola.ttf" if mono else "arialbd.ttf" if bold else "arial.ttf"
    return ImageFont.truetype(str(Path("C:/Windows/Fonts")/name), round(size*S))


class Canvas:
    def __init__(self):
        self.im = Image.new("RGB", (W, H), BG)
        self.d = ImageDraw.Draw(self.im)

    def rect(self, x, y, w, h, fill=PANEL, outline=None, radius=18, width=1):
        self.d.rounded_rectangle(tuple(round(v*S) for v in (x, y, x+w, y+h)),
                                radius=round(radius*S), fill=fill, outline=outline,
                                width=max(1, round(width*S)))

    def text(self, x, y, text, size=26, color=WHITE, bold=False, mono=False):
        self.d.text((round(x*S), round(y*S)), str(text), font=font(size, bold, mono),
                    fill=color, anchor="lt")

    def line(self, points, color=LINE, width=2):
        self.d.line([(round(x*S), round(y*S)) for x,y in points], fill=color,
                    width=round(width*S))

    def wrap(self, x, y, text, width, size=26, color=WHITE, bold=False, gap=1.35):
        lines, current = [], ""
        for word in text.split():
            trial = f"{current} {word}".strip()
            if font(size,bold).getlength(trial) > width*S and current:
                lines.append(current)
                current = word
            else:
                current = trial
        if current:
            lines.append(current)
        for i, line in enumerate(lines):
            self.text(x, y+i*size*gap, line, size, color, bold)
        return len(lines)*size*gap

    def pill(self, x, y, label, color=TEAL, width=None):
        w = width or font(20, True).getlength(label)/S+32
        self.rect(x,y,w,36, "#1b3040", color, 9)
        self.text(x+16,y+7,label,20,color,True)


def header(c, scene, t, duration):
    c.text(64, 36, "SQL / TỪ DỮ LIỆU ĐẾN QUYẾT ĐỊNH", 18, MUTED, True)
    c.text(1360, 36, f"BÀI HỌC  {scene+1:02}/08", 18, MUTED, True)
    c.line([(64,76),(1536,76)])
    dy = 20*(1-ease(t,0,.65))
    c.text(64,104+dy, LABELS[scene], 20, TEAL, True)
    c.text(64,145+dy,TITLES[scene],44,WHITE,True)
    c.line([(64,837),(1536,837)])
    c.text(64,860,"VÍ DỤ MINH HỌA  /  tickets",18,MUTED)
    for i in range(8):
        x = 1060+i*60
        c.rect(x,865,46,5, TEAL if i<scene else LINE, radius=2)
        if i == scene:
            c.rect(x,865,max(.1,46*t/duration),5,TEAL,radius=2)


def code(c, x, y, lines, width=700, active=(), size=26, step=46):
    c.rect(x,y,width,len(lines)*step+72,"#0c1727",LINE)
    c.text(x+24,y+18,"SQL",16,MUTED,True)
    for i, text in enumerate(lines):
        yy = y+54+i*step
        if i in active:
            c.rect(x+12, yy-7, width-24, step-3, "#1c3944", radius=6)
        c.text(x+25,yy,text,size,TEAL if i in active else WHITE,mono=True)


def table(c, x, y, rows, width=790, rowh=43, selected=False, active_ids=(),
          dim_ids=(), title="tickets", highlight_columns=False):
    c.rect(x,y,width,95+rowh*len(rows),PANEL,LINE)
    c.text(x+22,y+17,title,22,WHITE,True)
    c.text(x+width-140,y+19,f"{len(rows)} phiếu",18,MUTED)
    columns = [("id",.04),("status",.22),("channel",.47),("wait_min",.73)]
    for label, frac in columns:
        col = MUTED if selected and label=="status" else TEAL if highlight_columns else MUTED
        c.text(x+width*frac,y+58,label,21,col,mono=True)
    for j,r in enumerate(rows):
        yy = y+91+j*rowh
        if r[0] in active_ids:
            c.rect(x+10, yy-4, width-20,rowh-2,"#21463f",radius=5)
        dim = r[0] in dim_ids
        for k,(_,frac) in enumerate(columns):
            color = "#516078" if dim or (selected and k==1) else WHITE
            if k==3 and not dim: color = ORANGE
            c.text(x+width*frac,yy,str(r[k]),23,color,mono=True)


def ticket(c, x, y, row, width=610, height=60, accent=TEAL, rank=None, dim=False):
    c.rect(x,y,width,height,"#142236" if not dim else "#101a2b", LINE if dim else accent,12)
    color = "#536078" if dim else WHITE
    left = x+20
    if rank is not None:
        c.text(left,y+18,f"{rank:02}",20,MUTED,True)
        left += 55
    c.text(left,y+17,f"#{row[0]}",25,color,True)
    c.text(left+125,y+20,row[2].upper(),20,MUTED)
    c.text(x+width-145,y+15,f"{row[3]} phút",27,accent if not dim else MUTED,True)


def scene_frame(scene, t, duration):
    c = Canvas()
    header(c,scene,t,duration)
    # Visual beats remain proportional if narration requires a longer scene.
    t = t*DURATIONS[scene]/duration
    if scene == 0:
        c.text(76,248,"ƯU TIÊN XỬ LÝ",22,MUTED,True)
        c.pill(1040,244,"TRUY VẤN CHƯA CÓ ORDER BY",ORANGE)
        for i,r in enumerate([ROWS[0], ROWS[4], ROWS[7]]):
            dy=32*(1-ease(t,.4+i*.2,.6))
            ticket(c,76,296+i*83+dy,r,680,68,BLUE,i+1)
        if t>3:
            ticket(c,76+45*(1-ease(t,3,.7)),580,ROWS[3],680,76,RED)
            c.text(100,681,"90 phút chờ — vẫn nằm ngoài kết quả",27,RED,True)
        c.text(850,325,"3 dòng trả về",42,WHITE,True)
        c.text(850,390,"≠",80,ORANGE,True)
        c.wrap(850,500,"3 người cần hỗ trợ gấp nhất",600,42,WHITE,True)
        if t>7:
            c.pill(850,675,"SQL KHÔNG BÁO LỖI",ORANGE)
        c.text(76,774,"Trả đúng số lượng chưa đủ để chọn đúng đối tượng.",28,TEAL,True)
    elif scene == 1:
        table(c,64,235,ROWS,825,42)
        c.text(955,251,"YÊU CẦU CỦA HỆ THỐNG",24,TEAL,True)
        rules=[("01","Đang mở","status = 'open'"),
               ("02","Từ App hoặc Web","channel IN ('app', 'web')"),
               ("03","Chờ ít nhất 30 phút","wait_min >= 30"),
               ("04","Lâu nhất lên trước","Mỗi trang: 3 phiếu")]
        for i,(num,title,detail) in enumerate(rules):
            if t < i*2: continue
            yy=310+i*112+20*(1-ease(t,i*2,.6))
            c.text(955,yy,num,24,TEAL,True)
            c.text(1010,yy,title,27,WHITE,True)
            c.text(1010,yy+42,detail,21,MUTED,mono=i<3)
    elif scene == 2:
        code(c,64,242,["SELECT id, channel, wait_min","FROM tickets;"],770,
             active=(1,) if t<7 else (0,),size=28,step=58)
        table(c,64,465,ROWS[:5],770,43,selected=t>7,highlight_columns=t>7,
              title="Trích bảng tickets · 5 / 10 dòng")
        c.pill(910,265,"FROM",TEAL)
        c.text(910,325,"Nguồn dữ liệu",38,WHITE,True)
        c.wrap(910,382,"Bảng tickets chứa các phiếu hỗ trợ.",580,28,MUTED)
        if t>6:
            c.pill(910,486,"SELECT",BLUE)
            c.text(910,546,"Các cột cần hiển thị",36,WHITE,True)
            c.text(910,603,"id  /  channel  /  wait_min",26,BLUE,mono=True)
        if t>13:
            c.pill(910,717,"CHƯA LỌC DÒNG",ORANGE)
    elif scene == 3:
        stage=0 if t<3 else 1 if t<9 else 2 if t<15 else 3
        remaining=[r for r in ROWS if (stage<1 or r[1]=="open")
                   and (stage<2 or r[2] in ("app","web"))
                   and (stage<3 or r[3]>=30)]
        # Animate removed rows sideways; remaining rows compact upward.
        c.text(64,236,"BĂNG CHUYỀN DỮ LIỆU",20,MUTED,True)
        prior_stage=max(0,stage-1)
        previous=[r for r in ROWS if (prior_stage<1 or r[1]=="open")
                  and (prior_stage<2 or r[2] in ("app","web"))
                  and (prior_stage<3 or r[3]>=30)]
        progress=ease(t,{0:0,1:3,2:9,3:15}[stage],.9)
        for r in previous:
            old=previous.index(r)
            if r in remaining:
                new=remaining.index(r)
                yy=280+(old+(new-old)*progress)*47
                c.rect(64,yy,590,41,"#18352f",radius=7)
                c.text(80,yy+9,f"#{r[0]}    {r[1]:6}  {r[2]:5}",20,WHITE,mono=True)
                c.text(525,yy+8,f"{r[3]} phút",21,TEAL,True)
            elif progress<1:
                xx=64-700*progress
                if xx > -580:
                    c.rect(xx,280+old*47,590,41,"#442a37",radius=7)
                    c.text(xx+16,289+old*47,f"#{r[0]}    {r[1]}   {r[2]}   {r[3]} phút",20,RED)
        c.pill(64,782,f"CÒN {len(remaining)} / 10 PHIẾU",TEAL)
        code(c,735,239,["WHERE status = 'open'","  AND channel IN ('app', 'web')",
                       "  AND wait_min >= 30"],800,active=(max(0,stage-1),),size=25)
        c.wrap(760,480,"AND: phải đúng tất cả điều kiện.",740,29,TEAL,True)
        if t>20:
            c.text(760,552,"IN tương đương OR có dấu ngoặc:",24,MUTED)
            code(c,735,595,["(channel = 'app' OR channel = 'web')"],
                 800,active=(0,),size=24,step=40)
        if t>27:
            c.text(760,738,"BETWEEN  khoảng giá trị   ·   LIKE  mẫu chuỗi",21,MUTED)
    elif scene == 4:
        c.text(64,234,"7 PHIẾU HỢP LỆ",21,MUTED,True)
        move=ease(t,4,2.2)
        for i,r in enumerate(VALID):
            target=SORTED.index(r)
            yy=277+(i+(target-i)*move)*70
            accent=ORANGE if r[3]==70 and t>13 else TEAL if move==1 else BLUE
            ticket(c,64,yy,r,690,59,accent, target+1 if move==1 else None)
        code(c,815,262,["ORDER BY wait_min DESC,","         id DESC"],720,
             active=(0,) if t<13 else (1,),size=29,step=55)
        c.pill(840,488,"DESC",TEAL)
        c.text(970,489,"Giảm dần",31,WHITE,True)
        c.pill(840,553,"ASC",BLUE)
        c.text(970,554,"Tăng dần",31,WHITE,True)
        if t>13:
            c.wrap(840,646,"Cùng 70 phút?",620,32,ORANGE,True)
            c.wrap(840,697,"#109 đứng trước #102 vì id lớn hơn.",630,28,WHITE)
    elif scene == 5:
        page2=t>=12
        p=ease(t,12,.9) if page2 else ease(t,2,.9)
        start=3 if page2 else 0
        c.text(64,236,"DANH SÁCH ĐÃ SẮP XẾP",20,MUTED,True)
        for i,r in enumerate(SORTED):
            ticket(c,64,280+i*69,r,650,58,TEAL,i+1,dim=page2 and i<3)
            if page2 and i<3:
                c.text(733,298+i*69,"BỎ QUA",18,ORANGE,True)
        c.pill(925,237,f"TRANG {2 if page2 else 1}",TEAL)
        code(c,905,299,[f"LIMIT 3 OFFSET {3 if page2 else 0};"],630,
             active=(0,),size=30,step=46)
        for j,r in enumerate(SORTED[start:start+3]):
            ticket(c,905-65*(1-p),465+j*80,r,630,65,TEAL,start+j+1)
        c.text(925,740,"LIMIT: lấy tối đa 3 dòng",25,WHITE,True)
        c.text(925,781,f"OFFSET: bỏ qua {3 if page2 else 0} dòng đầu",23,MUTED)
        c.text(64,794,"Luôn ORDER BY trước khi phân trang.",24,ORANGE,True)
    elif scene == 6:
        phase=min(5,int(max(0,t-4)/3))
        code(c,64,243,SQL,815,active=({0:1,1:2,2:0,3:5,4:6,5:6}[phase],),
             size=27,step=54)
        stations=[("FROM","Lấy bảng dữ liệu","10 phiếu"),
                  ("WHERE","Lọc dòng hợp lệ","7 phiếu"),
                  ("SELECT","Chọn cột hiển thị","3 cột"),
                  ("ORDER BY","Xếp thứ tự ưu tiên","90 → 70 → 70…"),
                  ("OFFSET","Bỏ qua dòng đầu","Bỏ qua 0"),
                  ("LIMIT","Giới hạn kết quả","Lấy 3 phiếu")]
        for i,(name,desc,val) in enumerate(stations):
            yy=240+i*86
            c.rect(947,yy,590,71,"#21443e" if i==phase else PANEL,
                   TEAL if i==phase else LINE,11)
            c.text(966,yy+14,name,24,TEAL if i==phase else BLUE,True,mono=True)
            c.text(1150,yy+12,desc,23,WHITE)
            c.text(1150,yy+43,val,18,MUTED)
            if i<5: c.text(990,yy+71,"↓",15,MUTED)
        c.text(64,779,"Thứ tự logic của ví dụ này; không phải kế hoạch thực thi vật lý.",25,ORANGE)
    else:
        c.pill(64,241,"ƯU TIÊN XỬ LÝ · ĐÃ ĐÚNG THỨ TỰ",TEAL)
        for i,r in enumerate(SORTED[:3]):
            ticket(c,64+35*(1-ease(t,i*.3,.8)),310+i*88,r,710,73,TEAL,i+1)
        terms=[("SELECT","Chọn cột"),("WHERE","Lọc dòng"),
               ("ORDER BY","Sắp xếp"),("LIMIT / OFFSET","Phân trang")]
        for i,(a,b) in enumerate(terms):
            c.text(890,268+i*78,a,27,TEAL,True,mono=True)
            c.text(1190,268+i*78,b,27,WHITE)
        c.line([(64,631),(1536,631)])
        c.text(64,670,"SQL KHÔNG CHỈ LÀ ĐÚNG CÚ PHÁP.",38,WHITE,True)
        c.text(64,732,"MÀ CÒN LÀ HIỂU ĐÚNG LOGIC.",44,TEAL,True)
    # Short fade-through-dark transitions; text remains crisp at rest.
    fade=min(ease(t,0,.35),1-ease(t,DURATIONS[scene]-.35,.35))
    if fade<1:
        c.im=Image.blend(Image.new("RGB",(W,H),BG),c.im,fade)
    return c.im


def prepare(batch, source):
    batch.mkdir(parents=True,exist_ok=True)
    if not (batch/"source-script.txt").exists():
        shutil.copy2(source,batch/"source-script.txt")
    script=(batch/"source-script.txt").read_text(encoding="utf-8-sig")
    chunks=re.split(r"## Scene \d+",script)[1:]
    if len(chunks)!=8:
        raise ValueError("Expected the supplied eight-scene script.")
    scenes=[]
    for i,chunk in enumerate(chunks):
        # Only spoken paragraphs following a narration label; exclude screen copy.
        voice=re.findall(r"\*Lời dẫn(?: tiếp)?:\*\s*\n\s*“(.*?)”",chunk,re.S)
        if not voice:
            raise ValueError(f"No narration found in scene {i+1}")
        dialogue=" ".join(" ".join(v.split()) for v in voice)
        scenes.append({"slug":f"scene-{i+1:02}","dialogue":dialogue,
                       "duration_seconds":DURATIONS[i],"title":TITLES[i]})
        folder=batch/f"clip-{i+1:02}-scene-{i+1:02}"
        folder.mkdir(exist_ok=True)
        (folder/"dialogue.txt").write_text(dialogue,encoding="utf-8")
    save(batch/"manifest.json",{"title":"SQL: chọn đúng người cần hỗ trợ",
          "size":[W,H],"fps":FPS,"cache":True,"clips":scenes,
          "data":ROWS,"sql":SQL,
          "references":["https://www.postgresql.org/docs/current/sql-select.html"],
          "assumptions":["id is unique and non-null; wait_min is non-null",
                         "Static teaching dataset; no concurrent updates"]})
    con=sqlite3.connect(":memory:")
    con.execute("CREATE TABLE tickets(id INTEGER PRIMARY KEY, status TEXT, channel TEXT, wait_min INTEGER)")
    con.executemany("INSERT INTO tickets VALUES(?,?,?,?)",ROWS)
    actual=con.execute("\n".join(SQL)).fetchall()
    assert [r[0] for r in actual]==[104,109,102]
    page2=con.execute("\n".join(SQL).replace("OFFSET 0","OFFSET 3")).fetchall()
    assert [r[0] for r in page2]==[105,108,110]
    save(batch/"data-check.json",{"engine":"SQLite (shared SELECT syntax)",
          "filtered_rows":len(VALID),"sorted_ids":[r[0] for r in SORTED],
          "page_1":actual,"page_2":page2,"passed":True})
    return scenes


def audio(batch, scenes):
    spec=importlib.util.spec_from_file_location("existing_product_runner",
              ROOT/"workflows/product-video/run.py")
    runner=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
    report=[]
    for i,scene in enumerate(scenes):
        runner.voice(batch,{"cache":True},i+1,scene)
        folder=batch/f"clip-{i+1:02}-scene-{i+1:02}"
        raw=folder/"voice-decoded.wav"
        subprocess.run([FF,"-v","error","-y","-i",str(folder/"voice.mp3"),
                        "-ac","1","-ar","48000",str(raw)],check=True)
        with wave.open(str(raw),"rb") as f:
            seconds=f.getnframes()/f.getframerate()
        target=DURATIONS[i]
        # Gently slow brisk takes to suit teaching, leaving a short reading pause.
        tempo=max(.85,seconds/(target-.8))
        # Keep narration intelligible. Extend only if a take is excessively long.
        if tempo>1.22:
            target=math.ceil(seconds/1.22+.8)
            tempo=seconds/(target-.8)
        scene["duration_seconds"]=target
        subprocess.run([FF,"-v","error","-y","-i",str(raw),"-af",
                        f"atempo={tempo:.7f},adelay=350,apad,loudnorm=I=-16:TP=-1.5:LRA=7",
                        "-t",str(target),"-ar","48000","-ac","2",
                        str(folder/"voice-timed.wav")],check=True)
        report.append({"scene":i+1,"raw_seconds":seconds,"target_seconds":target,
                       "tempo":tempo,"lead_in_seconds":.35})
        print(f"AUDIO {i+1}/8: {seconds:.2f}s -> {target}s, tempo={tempo:.3f}",flush=True)
    save(batch/"audio-timing.json",report)
    save(batch/"timed-scenes.json",scenes)
    return scenes


def render(batch, scenes, only_previews=False):
    preview=batch/"previews"
    preview.mkdir(exist_ok=True)
    thumbnails=[]
    for i,scene in enumerate(scenes):
        duration=scene["duration_seconds"]
        frame=scene_frame(i,duration*.65,duration)
        frame.save(preview/f"scene-{i+1:02}.png")
        thumbnails.append(frame.resize((640,360)))
        if only_previews: continue
        folder=batch/f"clip-{i+1:02}-scene-{i+1:02}"
        target=folder/"scene.mp4"
        if target.exists(): continue
        log=(folder/"render.log").open("w",encoding="utf-8")
        command=[FF,"-hide_banner","-loglevel","warning","-y",
                 "-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}",
                 "-r",str(FPS),"-i","pipe:0","-i",str(folder/"voice-timed.wav"),
                 "-c:v","libx264","-preset","fast","-crf","19","-pix_fmt","yuv420p",
                 "-c:a","aac","-b:a","192k","-t",str(duration),
                 "-movflags","+faststart",str(target)]
        p=subprocess.Popen(command,stdin=subprocess.PIPE,stderr=log)
        try:
            for frame_num in range(round(duration*FPS)):
                p.stdin.write(scene_frame(i,frame_num/FPS,duration).tobytes())
            p.stdin.close()
            result=p.wait()
            if result: raise RuntimeError(f"Render scene {i+1} failed; see render.log")
        finally:
            log.close()
            if p.poll() is None: p.kill()
        print(f"RENDER {i+1}/8: {target.stat().st_size/1e6:.1f} MB",flush=True)
    sheet=Image.new("RGB",(1280,1440),BG)
    for i,im in enumerate(thumbnails):
        sheet.paste(im,((i%2)*640,(i//2)*360))
    sheet.save(batch/"storyboard.jpg",quality=94)
    if only_previews: return
    listing=batch/"concat.txt"
    listing.write_text("".join(
        f"file 'clip-{i+1:02}-scene-{i+1:02}/scene.mp4'\n" for i in range(8)),encoding="utf-8")
    subprocess.run([FF,"-v","error","-y","-f","concat","-safe","0","-i",str(listing),
                    "-c","copy","-movflags","+faststart",str(batch/"SQL-motion-slides.mp4")],check=True)
    # Decode the complete delivery, not just its first frame.
    qa=subprocess.run([FF,"-v","error","-i",str(batch/"SQL-motion-slides.mp4"),
                       "-f","null","-"],capture_output=True,text=True)
    probe=subprocess.run([FF,"-hide_banner","-i",str(batch/"SQL-motion-slides.mp4")],
                         capture_output=True,text=True)
    (batch/"media-info.txt").write_text(probe.stderr,encoding="utf-8")
    save(batch/"qa.json",{"full_decode_passed":qa.returncode==0 and not qa.stderr.strip(),
         "decode_errors":qa.stderr,"expected_duration_seconds":sum(s["duration_seconds"] for s in scenes),
         "dimensions":[W,H],"fps":FPS,"audio":"AAC stereo 48 kHz",
         "dataset_checks":"data-check.json","audio_timing":"audio-timing.json",
         "frames_rendered":sum(round(s["duration_seconds"]*FPS) for s in scenes)})
    if qa.returncode or qa.stderr.strip():
        raise RuntimeError("Final full decode failed; inspect qa.json")
    print("DELIVERY",batch/"SQL-motion-slides.mp4",flush=True)


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--stage",choices=["prepare","audio","previews","render","all"],default="all")
    args=p.parse_args()
    scenes=prepare(args.output,args.source)
    if args.stage in ("audio","all"): scenes=audio(args.output,scenes)
    elif (args.output/"timed-scenes.json").exists():
        scenes=json.loads((args.output/"timed-scenes.json").read_text(encoding="utf-8"))
    if args.stage in ("render","all","previews"):
        render(args.output,scenes,args.stage=="previews")


if __name__=="__main__":
    main()
