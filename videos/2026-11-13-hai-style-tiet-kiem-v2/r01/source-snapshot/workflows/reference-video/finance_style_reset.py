"""Short motion proofs after rejected finance styles. No provider calls.

The original exact take supplies two complete clauses (daily and dinner).
Sources are frozen before bundling; revisions and rejected originals are retained.
"""
from pathlib import Path
import argparse,json,shutil,subprocess,time,hashlib
import cv2
from PIL import Image,ImageDraw,ImageFont
from finance_demo import ROOT,PROJECT,FF,run,save,sha
ORIGINAL=ROOT/'videos/2026-11-13-hai-style-tiet-kiem'
BATCH=ROOT/'videos/2026-11-13-hai-style-tiet-kiem-v2'
ENTRY=PROJECT/'src/finance-reset-entry.tsx'
CLI=PROJECT/'node_modules/@remotion/cli/remotion-cli.js'
START,FRAMES=890,535

def prepare():
    BATCH.mkdir(exist_ok=True)
    plan=json.loads((ORIGINAL/'plan.json').read_text(encoding='utf-8'))
    save(BATCH/'props.json',{'plan':plan,'fromFrame':START,'frames':FRAMES})
    (BATCH/'script-excerpt.txt').write_text('\n\n'.join(s['text'] for s in plan['segments'] if s['visual'] in ['daily','dinner']),encoding='utf-8')
    audio=BATCH/'audio/excerpt.wav';audio.parent.mkdir(exist_ok=True)
    source=ORIGINAL/'audio/final-mix.wav'
    if not audio.exists():run([FF,'-y','-v','error','-i',source,'-af',f'atrim=start={START/30:.9f}:end={(START+FRAMES)/30:.9f},asetpts=PTS-STARTPTS','-ar','48000','-c:a','pcm_s16le',audio])
    save(BATCH/'audio/provenance.json',{'original':str(source.relative_to(ROOT)),'sha256':sha(source),'fromFrame':START,'frames':FRAMES,'fps':30,'speed':1,'excerptSHA256':sha(audio),'newPaidCalls':0,'fullNarrationChanged':False})
    save(BATCH/'brief.json',{'purpose':'Short proof of corrected motion and adult comic character style after user critique','notFullFilm':True,
      'originals':'Original slide-like minimal and unappealing cast retained in previous batch',
      'newCharacterDirection':'Comic biểu cảm mạnh, hơi hài hước — explicit user choice',
      'minimalDirection':'Continuous meaningful object actions and camera continuity instead of static text layouts',
      'libraryPolicy':'Review two leads before expanding to30 again','userApproval':'pending'})

def cli(args,log):
    t=time.perf_counter()
    with log.open('w',encoding='utf-8') as f:code=subprocess.run(['node',str(CLI),*map(str,args)],cwd=PROJECT,stdout=f,stderr=subprocess.STDOUT).returncode
    if code:raise RuntimeError('Render failed; inspect '+str(log))
    return round(time.perf_counter()-t,3)

def render(revision='r01',stills_only=False):
    prepare();out=BATCH/revision;out.mkdir(exist_ok=True);(out/'empty-public').mkdir(exist_ok=True)
    paths=[ENTRY,Path(__file__),PROJECT/'package.json',PROJECT/'package-lock.json']+[p for folder in ['finance-flow','finance-comic','finance-cast-v2','finance-demo'] for p in (PROJECT/'src'/folder).rglob('*') if p.is_file()]
    deps={'source':{str(p.relative_to(ROOT)):sha(p) for p in paths},'props':sha(BATCH/'props.json'),'audio':sha(BATCH/'audio/excerpt.wav')}
    guard=out/'dependencies.json'
    if guard.exists() and json.loads(guard.read_text(encoding='utf-8'))!=deps:raise ValueError('Source changed; use a new revision')
    save(guard,deps);snapshot=out/'source-snapshot';snapshot.mkdir(exist_ok=True)
    for p in paths:
        target=snapshot/p.relative_to(ROOT);target.parent.mkdir(parents=True,exist_ok=True)
        if not target.exists():shutil.copy2(p,target)
    bundle=out/'bundle';timings={}
    if not (bundle/'index.html').exists():timings['bundle']=cli(['bundle',ENTRY,f'--out-dir={bundle}',f'--public-dir={out/"empty-public"}','--log=error'],out/'bundle.log')
    (out/'comic').mkdir(exist_ok=True)
    if not (out/'comic/character-sheet.png').exists():timings['sheet']=cli(['still',bundle,'FinanceComicSheet',out/'comic/character-sheet.png','--log=error'],out/'sheet.log')
    if stills_only:
        for style,composition,frame in [('flow','FinanceFlowProof',280),('flow','FinanceFlowProof',440),('comic','FinanceComicProof',280),('comic','FinanceComicProof',440)]:
            d=out/style;d.mkdir(exist_ok=True);target=d/f'preflight-{frame}.png'
            if not target.exists():cli(['still',bundle,composition,target,f'--props={BATCH/"props.json"}',f'--frame={frame}','--log=error'],d/f'preflight-{frame}.log')
        save(out/'preflight-timings.json',timings);return
    for style,composition in [('flow','FinanceFlowProof'),('comic','FinanceComicProof')]:
        d=out/style;d.mkdir(exist_ok=True);silent=d/'silent.mp4';final=d/'final.mp4'
        if not silent.exists():timings[style]=cli(['render',bundle,composition,silent,f'--props={BATCH/"props.json"}','--muted','--codec=h264','--crf=19','--concurrency=2','--color-space=bt709','--pixel-format=yuv420p','--log=info'],d/'render.log')
        if not final.exists():run([FF,'-y','-v','error','-i',silent,'-i',BATCH/'audio/excerpt.wav','-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-ac','2','-t',str(FRAMES/30),'-movflags','+faststart',final])
        save(out/'timings.json',timings);print('DONE',style,flush=True)

def qa(revision='r01'):
    out=BATCH/revision;records=[];font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
    for style in ['flow','comic']:
        file=out/style/'final.mp4';dest=out/style/'qa';dest.mkdir(exist_ok=True)
        cap=cv2.VideoCapture(str(file));assert cap.isOpened();fps=cap.get(5);w,h=int(cap.get(3)),int(cap.get(4));count=0
        while cap.grab():count+=1
        assert count==FRAMES and abs(fps-30)<.001 and (w,h)==(1920,1080)
        sheet=Image.new('RGB',(1600,2*265),'#e8dfca');draw=ImageDraw.Draw(sheet);samples=[]
        for row,(start,length) in enumerate([(0,298),(298,237)]):
            for i,t in enumerate([.1,.3,.5,.7,.9]):
                f=start+int(length*t);cap.set(cv2.CAP_PROP_POS_FRAMES,f);ok,bgr=cap.read();assert ok
                p=dest/f'frame-{f:04}.png';cv2.imwrite(str(p),bgr);samples.append({'frame':f,'file':p.name})
                image=Image.fromarray(cv2.cvtColor(bgr,cv2.COLOR_BGR2RGB));image.thumbnail((320,180));x,y=i*320,row*265;sheet.paste(image,(x,y));draw.text((x+10,y+188),f'{f/30:.2f}s / original {(START+f)/30:.2f}s',font=font,fill='#28362d')
        sheet.save(dest/'contact-sheet.jpg',quality=95);cap.release()
        audio=run([FF,'-v','error','-i',file,'-map','0:a:0','-ac','1','-ar','48000','-f','s16le','-']).stdout
        seconds=len(audio)/96000;assert abs(seconds-FRAMES/30)<.1
        records.append({'style':style,'sha256':sha(file),'decodedFrames':count,'fps':fps,'size':[w,h],'decodedAudioSeconds':seconds,'audioPCMHash':hashlib.sha256(audio).hexdigest(),'samples':samples})
    assert records[0]['audioPCMHash']==records[1]['audioPCMHash']
    save(out/'qa.json',{'technical':'passed','proofExcerptSeconds':FRAMES/30,'fullOriginalNarrationSeconds':2333/30,'sameDecodedAudio':True,'newPaidCalls':0,'records':records,'editorialReview':'Pending actual rendered review; frame counts are not aesthetic acceptance','continuousAVReview':False,'userApproval':'pending'})
    print('QA_OK: two535-frame proofs with identical decoded audio',flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('phase',choices=['prepare','preflight','render','qa']);p.add_argument('--revision',default='r01');a=p.parse_args()
    if a.phase=='prepare':prepare()
    elif a.phase=='preflight':render(a.revision,stills_only=True)
    else:{'render':render,'qa':qa}[a.phase](a.revision)
