"""Immutable sequential chapter-sized rendering and full-duration technical QA."""
from pathlib import Path
import argparse, math, shutil, subprocess, time, hashlib
import cv2
from PIL import Image, ImageDraw, ImageFont
from finance_long import ROOT,BATCH,PROJECT,FPS,FF,save,load,sha,run
ENTRY=PROJECT/'src/finance-long-entry.tsx'
CLI=PROJECT/'node_modules/@remotion/cli/remotion-cli.js'
STYLES=[('comic','FinanceLongComic'),('flow','FinanceLongFlow')]

def reject_unchanged_slide_sources(chosen):
    """A new revision or new audio must not re-enable explicitly rejected visuals.

    This detects exact source reuse only. Modified source still needs actual
    temporal editorial review; hashes cannot establish acceptable animation.
    QA and diagnostic preflight of retained work remain available.
    """
    policy=ROOT/'workflows/reference-video/finance-rejected-visuals.json'
    if not policy.is_file():raise ValueError('Missing retained finance visual rejection policy')
    record=load(policy)
    if record.get('schema')!='rejected-finance-visuals/1':raise ValueError('Invalid finance visual rejection policy')
    for style,_ in STYLES:
        if chosen!='both' and style!=chosen:continue
        blocked=record['styles'].get(style)
        if not blocked:continue
        if not blocked.get('sources'):raise ValueError('Rejected visual source fingerprints are empty')
        unchanged=True
        for relative,digest in blocked['sources'].items():
            source=(ROOT/relative).resolve()
            if not source.is_relative_to(PROJECT/'src'):raise ValueError('Visual rejection source outside cinematic/src')
            if not source.is_file() or sha(source)!=digest:unchanged=False
        if unchanged:
            raise ValueError(f'{style}: unchanged visual sources were rejected by the user as slide videos. '
                'Rewrite scene progression and inspect complete moving scenes before another long render. '
                'Changing revision, narration or audio does not resolve this feedback. See FINANCE_STYLES.md.')

def cli(args,log):
    start=time.perf_counter();Path(log).parent.mkdir(parents=True,exist_ok=True)
    with Path(log).open('w',encoding='utf-8') as f:
        code=subprocess.run(['node',str(CLI),*map(str,args)],cwd=PROJECT,stdout=f,stderr=subprocess.STDOUT).returncode
    if code:raise RuntimeError('Remotion failed; inspect '+str(log))
    return round(time.perf_counter()-start,3)

def bundle(revision):
    out=BATCH/revision;out.mkdir(exist_ok=True);(out/'empty-public').mkdir(exist_ok=True)
    paths=[ENTRY,Path(__file__),ROOT/'workflows/reference-video/finance_long.py',ROOT/'workflows/reference-video/finance_long_content.py',PROJECT/'finance-long-preflight.cjs',PROJECT/'package.json',PROJECT/'package-lock.json']
    for folder in ['finance-long-comic','finance-long-flow','finance-cast-v2','finance-flow']:
        paths += [p for p in (PROJECT/'src'/folder).rglob('*') if p.is_file()]
    deps={'sources':{str(p.relative_to(ROOT)):sha(p) for p in paths},'planSHA256':sha(BATCH/'plan.json'),'mixSHA256':sha(BATCH/'audio/final-mix.wav')}
    guard=out/'dependencies.json'
    if guard.exists() and load(guard)!=deps:raise ValueError('Frozen render sources changed; use a new revision')
    save(guard,deps);save(out/'props.json',{'plan':load(BATCH/'plan.json')})
    snapshot=out/'source-snapshot'
    for p in paths:
        target=snapshot/p.relative_to(ROOT);target.parent.mkdir(parents=True,exist_ok=True)
        if not target.exists():shutil.copy2(p,target)
    if not (out/'bundle/index.html').exists():
        sec=cli(['bundle',ENTRY,f'--out-dir={out/"bundle"}',f'--public-dir={out/"empty-public"}','--log=error'],out/'bundle.log')
        save(out/'bundle-timing.json',{'wallSeconds':sec})
    return out

def sheets(folder,files,stem):
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
    for page in range(math.ceil(len(files)/15)):
        sheet=Image.new('RGB',(1440,5*300),'#eee7db');d=ImageDraw.Draw(sheet)
        for j,file in enumerate(files[page*15:(page+1)*15]):
            im=Image.open(file).convert('RGB');im.thumbnail((480,270));x,y=(j%3)*480,(j//3)*300
            sheet.paste(im,(x,y));d.text((x+8,y+273),file.stem[:65],font=font,fill='#252330')
        sheet.save(folder/f'{stem}-{page+1:02}.jpg',quality=92)

def preflight(revision):
    out=bundle(revision);log=out/'preflight.log';start=time.perf_counter()
    with log.open('w',encoding='utf-8') as f:
        code=subprocess.run(['node',str(PROJECT/'finance-long-preflight.cjs'),str(out/'bundle'),str(out/'props.json'),str(out)],cwd=PROJECT,stdout=f,stderr=subprocess.STDOUT).returncode
    if code:raise RuntimeError('Preflight failed; inspect '+str(log))
    for style,_ in STYLES:
        folder=out/style/'preflight';sheets(folder,sorted(folder.glob('b*.jpg')), 'sheet')
    save(out/'preflight-timing.json',{'wallSeconds':round(time.perf_counter()-start,3)})
    print('PREFLIGHT_READY',flush=True)

def decoded_frames(file):
    cap=cv2.VideoCapture(str(file));assert cap.isOpened(),str(file)
    size=(int(cap.get(3)),int(cap.get(4)));fps=cap.get(5);count=0
    while cap.grab():count+=1
    cap.release();assert size==(1920,1080) and abs(fps-FPS)<.001,(size,fps)
    return count

def render(revision,chosen='both',concurrency=4):
    reject_unchanged_slide_sources(chosen)
    out=bundle(revision);p=load(BATCH/'plan.json');n=p['durationFrames']
    for style,composition in STYLES:
        if chosen!='both' and style!=chosen:continue
        dest=out/style;dest.mkdir(exist_ok=True);chunks=dest/'chunks';chunks.mkdir(exist_ok=True)
        files=[]; timings=[]
        for i,start in enumerate(range(0,n,1800)):
            end=min(n,start+1800);file=chunks/f'{i:02}.mp4';receipt=file.with_suffix('.json')
            if file.exists():
                if not receipt.exists():
                    file.rename(file.with_name(file.stem+f'.incomplete-{time.time_ns()}.mp4'))
                elif load(receipt)['sha256']!=sha(file):raise ValueError('Completed chunk bytes changed')
            if not file.exists():
                seconds=cli(['render',out/'bundle',composition,file,f'--props={out/"props.json"}',f'--frames={start}-{end-1}',
                    '--codec=h264','--crf=19',f'--concurrency={concurrency}','--color-space=bt709','--pixel-format=yuv420p','--muted','--log=info'],chunks/f'{i:02}.log')
                count=decoded_frames(file);assert count==end-start,(file,count,end-start)
                save(receipt,{'from':start,'endExclusive':end,'decodedFrames':count,'sha256':sha(file),'wallSeconds':seconds,'framesPerSecond':count/seconds})
            timings.append(load(receipt));files.append(file)
            save(dest/'render-timing.json',{'chunks':timings,'renderWallSeconds':sum(t['wallSeconds'] for t in timings),'renderedFrames':sum(t['decodedFrames'] for t in timings)})
            print('CHUNK_READY',style,i+1,math.ceil(n/1800),flush=True)
        final=dest/'final.mp4'
        if not final.exists():
            concat=dest/'concat.txt';concat.write_text('\n'.join("file '"+str(f.resolve()).replace('\\','/')+"'" for f in files),encoding='utf-8')
            run([FF,'-y','-v','error','-f','concat','-safe','0','-i',concat,'-i',BATCH/'audio/final-mix.wav',
                '-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-ac','2','-t',n/FPS,'-movflags','+faststart',final])
        print('FILM_READY',style,flush=True)

def qa(revision):
    out=BATCH/revision;p=load(BATCH/'plan.json');records=[]
    for style,_ in STYLES:
        file=out/style/'final.mp4';dest=out/style/'qa';dest.mkdir(exist_ok=True)
        n=decoded_frames(file);assert n==p['durationFrames'],(style,n,p['durationFrames'])
        cap=cv2.VideoCapture(str(file));samples=[]
        for s in p['segments']:
            for label,f in [('early',s['from']+int(s['duration']*.16)),('cue',s['from']+s['cueFrame']+10),('late',s['from']+int(s['duration']*.82))]:
                f=min(n-1,s['from']+s['duration']-1,f);cap.set(cv2.CAP_PROP_POS_FRAMES,f);ok,img=cap.read();assert ok
                target=dest/f'{s["id"]}-{label}-{f:05}.jpg';cv2.imwrite(str(target),img)
                samples.append({'beat':s['id'],'frame':f,'file':target.name})
        cap.release();sheets(dest,sorted(dest.glob('b*.jpg')),'contact')
        pcm=dest/'decoded-audio.pcm'
        run([FF,'-y','-v','error','-i',file,'-map','0:a:0','-ac','1','-ar','48000','-f','s16le',pcm])
        seconds=pcm.stat().st_size/96000;digest=sha(pcm);pcm.unlink()
        assert seconds>=p['words'][-1]['end'] and abs(seconds-n/FPS)<.1
        loud=run([FF,'-hide_banner','-i',file,'-af','ebur128=peak=true','-f','null','-']).stderr.decode(errors='replace')
        (dest/'loudness.txt').write_text(loud[-1800:],encoding='utf-8')
        records.append({'style':style,'file':str(file.relative_to(ROOT)),'sha256':sha(file),'decodedFrames':n,'seconds':n/FPS,
            'decodedAudioSeconds':seconds,'audioPCMHash':digest,'lastWordEnd':p['words'][-1]['end'],'samples':samples})
        print('FULL_QA',style,n,flush=True)
    assert records[0]['audioPCMHash']==records[1]['audioPCMHash'],'Styles have different decoded audio'
    credits=load(BATCH/'audio/voice-runs.json')
    save(out/'qa-report.json',{'technical':'passed','records':records,'sameDecodedAudio':True,'captionMaxPixelWidth':max(c['pixelWidth'] for c in p['captions']),
        'speechSpeed':1,'voice':'Nhật Phong','voiceReceipts':credits,
        'newPaidVisualMusicCalls':0,'userApproval':'pending','continuousAVReview':False,
        'limits':'Full decode, measured loudness and sampled rendered-frame inspection do not establish continuous watching/listening or aesthetic approval'})

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('phase',choices=['bundle','preflight','render','qa'])
    parser.add_argument('--revision',default='r01');parser.add_argument('--style',default='both',choices=['both','comic','flow']);parser.add_argument('--concurrency',type=int,default=4)
    a=parser.parse_args()
    if a.phase=='render':render(a.revision,a.style,a.concurrency)
    else:globals()[a.phase](a.revision)
