from pathlib import Path
import json,hashlib,subprocess,cv2,concurrent.futures
import imageio_ffmpeg
from PIL import Image,ImageDraw,ImageOps
root=Path('videos/2026-11-13-di-sieu-thi/long');records=json.loads((root/'video-candidates.json').read_text(encoding='utf-8'));ff=imageio_ffmpeg.get_ffmpeg_exe()
notes={
'clip-choose':{'observed':'Woman with gray/orange shopping cart selects an item, reaches to a high jar shelf, examines a jar, then leans toward cart. See six sampled frames over21.82s.','suggestedIntervals':[{'start':0,'end':3.5,'action':'Selects produce/low-shelf item beside cart'},{'start':6,'end':11,'action':'Reaches toward and takes a jar from shelf'},{'start':13,'end':18.5,'action':'Looks down at jar label'}],'limit':'Do not call choice unplanned or overspending; label price text not independently readable; real stock store may be staged.'},
'clip-aisle':{'observed':'Wide busy supermarket view with Chinese-language department signs, shoppers walking and selecting products. Change of positions across all sampled times shows actual motion.','suggestedIntervals':[{'start':0,'end':5,'action':'Store crowd and browsing context'},{'start':5,'end':10.5,'action':'Continued shopper movement; distinct source interval'}],'limit':'Not evidence of Vietnamese retail, the Swedish study, individual intent or impulse buying. Original sound must be muted under narration unless separately reviewed.'},
'clip-checkout':{'observed':'Customer removes groceries from gray basket while cashier takes/handles products on wooden checkout counter; customer lifts near-empty basket at end.','suggestedIntervals':[{'start':0,'end':5,'action':'Unloading basket at checkout'},{'start':6,'end':11,'action':'Cashier handles produce/packaged goods'},{'start':13,'end':16.8,'action':'Customer finishes unloading/lifts basket'}],'limit':'No actual bank-card/cash payment seen in sampled sequence. Do not claim transaction total or payment method.'}}
def process(r):
 if 'error' in r:return r
 original=root/r['file'];out=root/'assets'/f'{r["id"]}-720p.mp4';poster=root/'assets'/f'{r["id"]}-poster.jpg'
 cmd=[ff,'-v','error','-y','-i',str(original),'-map','0:v:0','-an','-vf','scale=1280:720:flags=lanczos,setsar=1,fps=30,format=yuv420p','-c:v','libx264','-crf','21','-preset','fast','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-color_range','tv','-movflags','+faststart',str(out)]
 if not out.exists():subprocess.run(cmd,check=True,capture_output=True)
 cap=cv2.VideoCapture(str(out));fps=cap.get(cv2.CAP_PROP_FPS);framecount=int(cap.get(cv2.CAP_PROP_FRAME_COUNT));duration=framecount/fps;ok,fr=cap.read()
 if ok:Image.fromarray(cv2.cvtColor(fr,cv2.COLOR_BGR2RGB)).save(poster,quality=90)
 cap.release()
 decoded=subprocess.run([ff,'-v','error','-i',str(out),'-f','null','-'],capture_output=True,text=True)
 assert decoded.returncode==0 and not decoded.stderr.strip()
 r.update({'inspectionStatus':'sampled-motion-frames-inspected','inspection':{'method':'Six source frames across full runtime opened; no continuous playback/listening claim.','sourceFramesAtSeconds':[0,r['durationSeconds']*.2,r['durationSeconds']*.4,r['durationSeconds']*.6,r['durationSeconds']*.8,r['durationSeconds']-.5],**notes[r['id']]},'derivative':{'file':str(out.relative_to(root)).replace('\\','/'),'poster':str(poster.relative_to(root)).replace('\\','/'),'command':cmd,'sourceSHA256':r['sha256'],'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'posterSHA256':hashlib.sha256(poster.read_bytes()).hexdigest(),'bytes':out.stat().st_size,'width':1280,'height':720,'fps':fps,'availableFrames':framecount,'durationSeconds':duration,'fullDecode':'passed','audio':'removed for narration-first mix','loop':False}})
 print(r['id'],framecount,round(duration,3),out.stat().st_size,flush=True)
 return r
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:records=list(pool.map(process,records))
(root/'video-candidates.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
