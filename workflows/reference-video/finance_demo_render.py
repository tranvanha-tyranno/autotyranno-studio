"""Sequential local rendering, snapshot, full decode and per-scene evidence."""
from pathlib import Path
import argparse, json, shutil, subprocess, time
import cv2
from PIL import Image, ImageDraw, ImageFont
from finance_demo import ROOT,BATCH,PROJECT,FF,sha,save,run

CLI=PROJECT/'node_modules/@remotion/cli/remotion-cli.js'
ENTRY=PROJECT/'src/finance-demo-entry.tsx'

def cli(args,log):
    start=time.perf_counter()
    with Path(log).open('w',encoding='utf-8') as f:
        p=subprocess.run(['node',str(CLI),*map(str,args)],cwd=PROJECT,stdout=f,stderr=subprocess.STDOUT)
    if p.returncode:raise RuntimeError('Remotion failed; inspect '+str(log))
    return round(time.perf_counter()-start,3)

def render(revision='r01',chosen='both'):
    plan=json.loads((BATCH/'plan.json').read_text(encoding='utf-8'))
    if not revision.startswith('r') or not revision[1:].isdigit():raise ValueError('Use r01/r02 revision name')
    out=BATCH/revision;out.mkdir(exist_ok=True)
    (out/'empty-public').mkdir(exist_ok=True)
    props=out/'props.json';save(props,{'plan':plan})
    bundle=out/'bundle'
    timings={}
    dependencies={'plan':sha(BATCH/'plan.json'),'mix':sha(BATCH/'audio/final-mix.wav'),
      'source':{str(p.relative_to(PROJECT)):sha(p) for p in [ENTRY]+[p for folder in ['finance-demo','finance-cast','finance-simple'] for p in (PROJECT/'src'/folder).rglob('*') if p.is_file()]}}
    guard=out/'render-dependencies.json'
    if guard.exists() and json.loads(guard.read_text(encoding='utf-8'))!=dependencies:raise ValueError('Sources changed; use a new revision')
    save(guard,dependencies)
    if not (bundle/'index.html').exists():timings['bundleWallSeconds']=cli(['bundle',ENTRY,f'--out-dir={bundle}',f'--public-dir={out/"empty-public"}','--log=error'],out/'bundle.log')
    for composition,style in [('FinanceCast','nhan-vat'),('FinanceMinimal','toi-gian')]:
        if chosen!='both' and style!=chosen:continue
        target=out/style;target.mkdir(exist_ok=True)
        silent=target/'silent.mp4';final=target/'final.mp4'
        if not silent.exists():
            timings[style]=cli(['render',bundle,composition,silent,f'--props={props}','--codec=h264','--crf=19','--concurrency=2','--color-space=bt709','--pixel-format=yuv420p','--muted','--log=info'],target/'render.log')
        if not final.exists():
            run([FF,'-y','-v','error','-i',silent,'-i',BATCH/'audio/final-mix.wav','-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-ac','2','-t',str(plan['durationFrames']/30),'-movflags','+faststart',final])
        save(out/'timings.json',timings)
        print('RENDERED',style,str(final),flush=True)
    motion=BATCH/'cast-library/gestures.mp4'
    if chosen!='toi-gian' and not motion.exists():timings['castMotion']=cli(['render',bundle,'FinanceCastMotion',motion,'--codec=h264','--crf=20','--concurrency=2','--log=error'],out/'motion-render.log')
    save(out/'timings.json',timings)
    snapshot=out/'source-snapshot';snapshot.mkdir(exist_ok=True)
    for folder in ['finance-demo','finance-cast','finance-simple']:
        if not (snapshot/folder).exists():shutil.copytree(PROJECT/'src'/folder,snapshot/folder)
    for file in [ENTRY,Path(__file__),ROOT/'workflows/reference-video/finance_demo.py',PROJECT/'package.json',PROJECT/'package-lock.json',BATCH/'plan.json']:
        if not (snapshot/file.name).exists():shutil.copy2(file,snapshot/file.name)
    save(out/'source-hashes.json',[{'path':p.relative_to(snapshot).as_posix(),'sha256':sha(p)} for p in snapshot.rglob('*') if p.is_file()])

def qa(revision='r01',chosen='both'):
    plan=json.loads((BATCH/'plan.json').read_text(encoding='utf-8'));out=BATCH/revision;records=[]
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',19)
    audiohashes=[]
    for style in ['nhan-vat','toi-gian']:
        if chosen!='both' and style!=chosen:continue
        final=out/style/'final.mp4';dest=out/style/'qa';dest.mkdir(exist_ok=True)
        cap=cv2.VideoCapture(str(final));assert cap.isOpened()
        w,h,fps=int(cap.get(3)),int(cap.get(4)),cap.get(5);count=0
        while cap.grab():count+=1
        assert (w,h)==(1920,1080) and abs(fps-30)<.001 and count==plan['durationFrames'],(style,count)
        samples=[]
        sheet=Image.new('RGB',(1440,3*310),'#e7e1d4');draw=ImageDraw.Draw(sheet)
        for i,s in enumerate(plan['segments']):
            for t,portion in enumerate([.18,.5,.84]):
                frame=min(count-1,s['from']+int(s['duration']*portion));cap.set(cv2.CAP_PROP_POS_FRAMES,frame)
                ok,bgr=cap.read();assert ok
                name=f'{s["id"]}-{t+1}-{frame:04}.jpg';cv2.imwrite(str(dest/name),bgr)
                samples.append({'segment':s['id'],'frame':frame,'file':name})
                if t==1:
                    img=Image.fromarray(cv2.cvtColor(bgr,cv2.COLOR_BGR2RGB));img.thumbnail((480,270))
                    x,y=(i%3)*480,(i//3)*310;sheet.paste(img,(x,y));draw.text((x+9,y+276),f'{s["id"]} {s["visual"]} {frame/30:.1f}s',font=font,fill='#193133')
        sheet.save(dest/'contact-sheet.jpg',quality=94);cap.release()
        # Full audio decode checks complete duration, not only container metadata.
        decoded=run([FF,'-v','error','-i',final,'-map','0:a:0','-ar','48000','-ac','1','-f','s16le','-']).stdout
        seconds=len(decoded)/96000
        assert seconds>=plan['words'][-1]['end'] and abs(seconds-count/30)<.1
        import hashlib
        digest=hashlib.sha256(decoded).hexdigest();audiohashes.append(digest)
        records.append({'style':style,'file':str(final.relative_to(ROOT)),'sha256':sha(final),'decodedFrames':count,'fps':fps,
          'size':[w,h],'decodedAudioSeconds':seconds,'lastWordEnd':plan['words'][-1]['end'],'audioPCMHash':digest,'samples':samples})
    assert len(set(audiohashes))==1,'Different audio in comparison styles'
    receipt=json.loads((BATCH/'audio/narration.receipt.json').read_text(encoding='utf-8'))
    save(out/'qa-report.json',{'technical':'passed','videos':records,'sameDecodedAudio':True if len(audiohashes)==2 else 'Only one style in this revision',
      'newProviderRequests':{'voice':1,'image':0,'video':0,'music':0,'sfx':0},'voiceCharacterCostHeader':receipt['character_cost'],
      'costLimits':'Header units are provider reported; no USD invoice inferred. Local rendering uses time/electricity.',
      'castAssets':len(list((BATCH/'cast-library').glob('*.svg'))),'userApproval':'pending',
      'visualReview':'Pending actual sample viewing; full decode is not aesthetic or motion acceptance',
      'continuousAudiovisualReview':False})

def repair_cast():
    """Re-render only the two budget scenes; preserve the rejected original."""
    plan=json.loads((BATCH/'plan.json').read_text(encoding='utf-8'))
    selected=[s for s in plan['segments'] if s['visual'] in ['before','after']]
    start=selected[0]['from'];end=selected[-1]['from']+selected[-1]['duration']
    out=BATCH/'r03';out.mkdir(exist_ok=True);(out/'empty-public').mkdir(exist_ok=True)
    target=out/'nhan-vat';target.mkdir(exist_ok=True)
    props=out/'props.json';save(props,{'plan':plan})
    snapshot=out/'source-snapshot';snapshot.mkdir(exist_ok=True)
    for folder in ['finance-demo','finance-cast','finance-simple']:
        if not (snapshot/folder).exists():shutil.copytree(PROJECT/'src'/folder,snapshot/folder)
    dependencies={'sourceVideoSHA256':sha(BATCH/'r01/nhan-vat/silent.mp4'),'planSHA256':sha(BATCH/'plan.json'),
      'mixSHA256':sha(BATCH/'audio/final-mix.wav'),'budgetSourceSHA256':sha(PROJECT/'src/finance-demo/BudgetScene.tsx'),
      'startFrame':start,'endFrameExclusive':end,'reason':'Move red allocation arrow below the salary numeral instead of across it'}
    guard=out/'repair-plan.json'
    if guard.exists() and json.loads(guard.read_text(encoding='utf-8'))!=dependencies:raise ValueError('Repair dependencies changed')
    save(guard,dependencies)
    bundle=out/'bundle';timings={}
    if not (bundle/'index.html').exists():timings['bundle']=cli(['bundle',ENTRY,f'--out-dir={bundle}',f'--public-dir={out/"empty-public"}','--log=error'],out/'bundle.log')
    patch=target/'budget-patch.mp4'
    if not patch.exists():timings['patch']=cli(['render',bundle,'FinanceCast',patch,f'--props={props}',f'--frames={start}-{end-1}',
      '--codec=h264','--crf=19','--concurrency=2','--color-space=bt709','--pixel-format=yuv420p','--muted','--log=info'],target/'patch-render.log')
    final=target/'final.mp4'
    if not final.exists():
        t=time.perf_counter()
        filters=f'[0:v]trim=start_frame=0:end_frame={start},setpts=PTS-STARTPTS[a];[1:v]setpts=PTS-STARTPTS[b];[0:v]trim=start_frame={end}:end_frame={plan["durationFrames"]},setpts=PTS-STARTPTS[c];[a][b][c]concat=n=3:v=1:a=0,setsar=1,format=yuv420p[v]'
        run([FF,'-y','-v','error','-i',BATCH/'r01/nhan-vat/silent.mp4','-i',patch,'-i',BATCH/'audio/final-mix.wav',
          '-filter_complex',filters,'-map','[v]','-map','2:a:0','-c:v','libx264','-preset','fast','-crf','19','-r','30',
          '-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-color_range','tv',
          '-c:a','aac','-b:a','192k','-ar','48000','-ac','2','-frames:v',str(plan['durationFrames']),'-t',str(plan['durationFrames']/30),'-movflags','+faststart',final])
        timings['spliceEncode']=round(time.perf_counter()-t,3)
    save(out/'timings.json',timings)
    save(out/'source-hashes.json',[{'path':p.relative_to(snapshot).as_posix(),'sha256':sha(p)} for p in snapshot.rglob('*') if p.is_file()])
    qa('r03','nhan-vat')
    print('REPAIRED',str(final),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('phase',choices=['render','qa','repair-cast']);p.add_argument('--revision',default='r01');p.add_argument('--style',choices=['both','nhan-vat','toi-gian'],default='both');args=p.parse_args()
    if args.phase=='repair-cast':repair_cast()
    else:{'render':render,'qa':qa}[args.phase](args.revision,args.style)
