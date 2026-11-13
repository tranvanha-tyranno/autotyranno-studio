"""Decode every frame and export visual evidence, without aesthetic auto-scoring."""
from pathlib import Path
import argparse,json
import cv2,numpy as np
from PIL import Image,ImageDraw,ImageFont

def inspect(video:Path,out:Path,timeline:Path|None=None):
    out.mkdir(parents=True,exist_ok=True)
    cap=cv2.VideoCapture(str(video));fps=cap.get(cv2.CAP_PROP_FPS)
    width=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH));height=int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    plan=json.loads(timeline.read_text(encoding='utf-8')) if timeline else None
    expected=plan['frames'] if plan else 1500
    targets=([min(c['end']-20,c['start']+c['beats'][1]['at']+30) for c in plan['chapters']]+[c['end']-25 for c in plan['chapters']]) if plan else [int(x*fps) for x in [1.5,7.8,16.5,21.7,29.7,33.5,39.5,46.5,48.6]]
    # Frames within short intervals expose animation geometry / text changes.
    motion=[6,12,18,24,30,36,140,146,152,158,164,170,545,551,557,563,569,575,1420,1426,1432,1438,1444,1450]
    if plan:motion=[c['start']+c['beats'][0]['at']+k for c in plan['chapters'] for k in [6,12,18,24,30,36]]
    wanted=set(targets+motion);frames={};per_second=[];count=0;deltas=[];prev=None
    while True:
        ok,bgr=cap.read()
        if not ok:break
        if count in wanted or count%round(fps)==15:
            im=Image.fromarray(cv2.cvtColor(bgr,cv2.COLOR_BGR2RGB));frames[count]=im if count in wanted else im.resize((384,216))
            if count%round(fps)==15:per_second.append(count)
        if count%3==0:
            small=cv2.resize(bgr,(160,90)).astype(np.float32)
            if prev is not None:deltas.append(float(np.abs(small[:75]-prev[:75]).mean()))
            prev=small
        count+=1
    cap.release()
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
    def sheet(keys,cols,thumb,name):
        w,h=thumb;canvas=Image.new('RGB',(w*cols,(h+30)*((len(keys)+cols-1)//cols)),(10,14,22));d=ImageDraw.Draw(canvas)
        for i,k in enumerate(keys):
            if k not in frames:continue
            x=(i%cols)*w;y=(i//cols)*(h+30);canvas.paste(frames[k].resize(thumb), (x,y));d.text((x+8,y+h+3),f'{k/fps:.2f}s / frame {k}',font=font,fill='white')
        canvas.save(out/name,quality=92)
    if plan:
        for page in range((len(per_second)+49)//50):sheet(per_second[page*50:(page+1)*50],5,(384,216),f'full-duration-{page+1:02}.jpg')
        for page in range((len(targets)+8)//9):sheet(targets[page*9:(page+1)*9],3,(640,360),f'keyframes-{page+1:02}.jpg')
        for page in range((len(motion)+35)//36):sheet(motion[page*36:(page+1)*36],6,(320,180),f'motion-strips-{page+1:02}.jpg')
    else:
        sheet(per_second,5,(384,216),'full-duration.jpg');sheet(targets,3,(640,360),'keyframes.jpg');sheet(motion,6,(320,180),'motion-strips.jpg')
    for k in targets:frames[k].save(out/f'frame-{k:04}.jpg',quality=94)
    report={'file':str(video),'decodedFrames':count,'fps':fps,'seconds':count/fps,'width':width,'height':height,'expectedFrames':expected,'frameCountPass':count==expected,'deltaTopPictureMean':float(np.mean(deltas)),'minimumConsecutiveSampleDelta':min(deltas),'aestheticAcceptance':'not inferred; requires visual review and user feedback','audioListening':'not performed by this script'}
    (out/'decode.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--file',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--timeline',type=Path);a=p.parse_args();inspect(a.file,a.out,a.timeline)
