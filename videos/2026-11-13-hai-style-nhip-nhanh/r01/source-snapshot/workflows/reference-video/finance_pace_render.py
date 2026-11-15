"""Render new fast action scenes with immutable snapshots and temporal proofs."""
from pathlib import Path
import argparse,hashlib,shutil,subprocess,time
import cv2
from finance_pace import BATCH,PREVIOUS,ROOT,PROJECT,FPS,FF,save,load,sha,run
from finance_long_render import cli,decoded_frames,sheets

ENTRY=PROJECT/'src/finance-pace-entry.tsx'
STYLES=[('comic','FinancePacedComic'),('flow','FinancePacedFlow')]

def bundle(revision):
    out=BATCH/revision;out.mkdir(exist_ok=True);(out/'empty-public').mkdir(exist_ok=True)
    files=[ENTRY,Path(__file__),ROOT/'workflows/reference-video/finance_pace.py',ROOT/'workflows/reference-video/finance_pace_plan.py',PROJECT/'finance-pace-preflight.cjs',PROJECT/'package.json',PROJECT/'package-lock.json']
    for folder in ['finance-pace-comic','finance-pace-flow','finance-cast-v2','finance-long-comic','finance-flow']:
        files.extend(p for p in (PROJECT/'src'/folder).rglob('*')if p.is_file())
    deps={'sources':{p.relative_to(ROOT).as_posix():sha(p) for p in files},'planSHA256':sha(BATCH/'plan.json'),'mixSHA256':sha(BATCH/'audio/final-mix.wav')}
    guard=out/'dependencies.json'
    if guard.exists() and load(guard)!=deps:raise ValueError('Source/timing frozen; use another revision')
    save(guard,deps);save(out/'props.json',{'plan':load(BATCH/'plan.json')})
    for p in files:
        target=out/'source-snapshot'/p.relative_to(ROOT);target.parent.mkdir(parents=True,exist_ok=True)
        if not target.exists():shutil.copy2(p,target)
    if not(out/'bundle/index.html').exists():
        sec=cli(['bundle',ENTRY,f'--out-dir={out/"bundle"}',f'--public-dir={out/"empty-public"}','--log=error'],out/'bundle.log');save(out/'bundle-timing.json',{'wallSeconds':sec})
    return out

def preflight(revision):
    out=bundle(revision);began=time.perf_counter()
    with (out/'preflight.log').open('w',encoding='utf-8')as log:
        result=subprocess.run(['node',str(PROJECT/'finance-pace-preflight.cjs'),str(out/'bundle'),str(out/'props.json'),str(out)],cwd=PROJECT,stdout=log,stderr=subprocess.STDOUT)
    if result.returncode:raise RuntimeError('Preflight failed; inspect log')
    for style,_ in STYLES:
        folder=out/style/'preflight';sheets(folder,sorted(folder.glob('b*.jpg'))+sorted(folder.glob('subscribe*.jpg')),'sheet')
    save(out/'preflight-timing.json',{'wallSeconds':time.perf_counter()-began})
    print('PACE_PREFLIGHT_READY',flush=True)

def proof(revision):
    out=bundle(revision);plan=load(BATCH/'plan.json');chosen=['b01','b15','b26','b42','subscribe']
    for style,composition in STYLES:
        dest=out/style/'proof';dest.mkdir(parents=True,exist_ok=True);records=[]
        old_records={c['beat']:c for c in load(dest/'receipt.json')['clips']} if (dest/'receipt.json').exists() else {}
        for beat in chosen:
            segment=next(s for s in plan['segments']if s['id']==beat);start=segment['from'];frames=segment['duration']
            file=dest/(beat+'.mp4')
            if not file.exists():
                props=dest/(beat+'-props.json');save(props,{'plan':plan,'fromFrame':start,'frames':frames})
                sec=cli(['render',out/'bundle',composition,dest/(beat+'-silent.mp4'),f'--props={props}','--scale=.6','--codec=h264','--crf=20','--muted','--concurrency=4','--log=error'],dest/(beat+'.log'))
                run([FF,'-y','-v','error','-i',dest/(beat+'-silent.mp4'),'-ss',start/FPS,'-i',BATCH/'audio/final-mix.wav',
                    '-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k','-t',frames/FPS,'-movflags','+faststart',file])
            else:
                sec=old_records.get(beat,{}).get('wallSeconds')
                if beat in old_records and sha(file)!=old_records[beat]['sha256']:raise ValueError('Completed proof bytes changed')
            cap=cv2.VideoCapture(str(file));assert cap.isOpened();size=(int(cap.get(3)),int(cap.get(4)));rate=cap.get(5);count=0
            while cap.grab():count+=1
            cap.release();assert size==(1152,648) and abs(rate-FPS)<.001 and count==frames,(style,beat,size,rate,count,frames)
            records.append({'beat':beat,'from':start,'duration':frames,'decodedFrames':count,'file':str(file.relative_to(BATCH)),'sha256':sha(file),'wallSeconds':sec})
            print('PROOF_READY',style,beat,flush=True)
        save(dest/'receipt.json',{'clips':records,'review':'Pending complete moving-scene review; still samples do not establish pacing.'})

def render(revision,chosen='both',concurrency=6):
    out=bundle(revision);plan=load(BATCH/'plan.json');frames=plan['durationFrames']
    review=out/'motion-review.json'
    if not review.exists():raise ValueError('Review complete moving proofs before long render; motion-review.json absent')
    reviewed=load(review)
    if reviewed.get('bundleDependenciesSHA256')!=sha(out/'dependencies.json'):raise ValueError('Temporal review is not linked to this frozen bundle')
    for style,_ in STYLES:
        if chosen!='both'and chosen!=style:continue
        result=reviewed.get('styles',{}).get(style,{})
        if result.get('decision')!='ready_for_long_render' or result.get('method')!='temporal_scene_review' or not result.get('observations'):
            raise ValueError('Complete moving-scene review is pending or rejected for '+style)
        retained=load(out/style/'proof/receipt.json')['clips'];observed={r['beat']:r for r in result.get('clips',[])}
        if {r['beat']for r in retained}!=set(observed):raise ValueError('Temporal review does not cover all representative proofs')
        for clip in retained:
            if observed[clip['beat']].get('sha256')!=clip['sha256'] or sha(BATCH/clip['file'])!=clip['sha256']:
                raise ValueError('Reviewed temporal proof changed')
    for style,composition in STYLES:
        if chosen!='both'and chosen!=style:continue
        dest=out/style;chunks=dest/'chunks';chunks.mkdir(parents=True,exist_ok=True);files=[];timings=[]
        for i,start in enumerate(range(0,frames,1800)):
            end=min(frames,start+1800);file=chunks/f'{i:02}.mp4';receipt=file.with_suffix('.json')
            if file.exists() and not receipt.exists():file.rename(file.with_name(file.stem+f'.incomplete-{time.time_ns()}.mp4'))
            if file.exists():
                if load(receipt)['sha256']!=sha(file):raise ValueError('Completed chunk changed')
            else:
                log=chunks/f'{i:02}.log'
                if log.exists():log.rename(log.with_name(log.stem+f'.retained-{time.time_ns()}.log'))
                sec=cli(['render',out/'bundle',composition,file,f'--props={out/"props.json"}',f'--frames={start}-{end-1}',
                    '--codec=h264','--crf=19',f'--concurrency={concurrency}','--color-space=bt709','--pixel-format=yuv420p','--muted','--log=info'],log)
                count=decoded_frames(file);assert count==end-start
                save(receipt,{'from':start,'endExclusive':end,'decodedFrames':count,'sha256':sha(file),'wallSeconds':sec,'framesPerSecond':count/sec})
            timings.append(load(receipt));files.append(file)
            save(dest/'render-timing.json',{'chunks':timings,'renderWallSeconds':sum(x['wallSeconds']for x in timings),'renderedFrames':sum(x['decodedFrames']for x in timings)})
            print('CHUNK_READY',style,i+1,(frames+1799)//1800,flush=True)
        final=dest/'final.mp4'
        if not final.exists():
            concat=dest/'concat.txt';concat.write_text('\n'.join("file '"+str(p).replace('\\','/')+"'"for p in files),encoding='utf-8')
            run([FF,'-y','-v','error','-f','concat','-safe','0','-i',concat,'-i',BATCH/'audio/final-mix.wav','-map','0:v:0','-map','1:a:0',
                '-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-ac','2','-t',frames/FPS,'-movflags','+faststart',final])
        print('FILM_READY',style,flush=True)

def qa(revision):
    out=BATCH/revision;plan=load(BATCH/'plan.json');records=[]
    for style,_ in STYLES:
        file=out/style/'final.mp4';dest=out/style/'qa';dest.mkdir(exist_ok=True);frames=decoded_frames(file)
        assert frames==plan['durationFrames'];cap=cv2.VideoCapture(str(file));samples=[]
        for shot in plan['shots']:
            f=shot['from']+round(shot['duration']*.65);cap.set(cv2.CAP_PROP_POS_FRAMES,f);ok,bgr=cap.read();assert ok
            target=dest/f'{shot["id"]}-{f:05}.jpg';cv2.imwrite(str(target),bgr);samples.append({'shot':shot['id'],'frame':f,'file':target.name,'sha256':sha(target)})
        cap.release();sheets(dest,sorted(dest.glob('b*.jpg'))+sorted(dest.glob('subscribe*.jpg')),'contact')
        pcm=dest/'audio.pcm';run([FF,'-y','-v','error','-i',file,'-map','0:a:0','-ar','48000','-ac','1','-f','s16le',pcm]);seconds=pcm.stat().st_size/96000;digest=sha(pcm);pcm.unlink()
        assert abs(seconds-frames/FPS)<.1 and seconds>plan['words'][-1]['end']
        loud=run([FF,'-hide_banner','-i',file,'-af','ebur128=peak=true','-f','null','-']).stderr.decode(errors='replace');(dest/'loudness.txt').write_text(loud[-1800:],encoding='utf-8')
        records.append({'style':style,'sha256':sha(file),'decodedFrames':frames,'seconds':frames/FPS,'decodedAudioSeconds':seconds,'audioPCMHash':digest,'lastWordEnd':plan['words'][-1]['end'],'samples':samples})
        print('FULL_QA',style,frames,flush=True)
    assert records[0]['audioPCMHash']==records[1]['audioPCMHash']
    save(out/'qa-report.json',{'technical':'passed','records':records,'sameDecodedAudio':True,'pacing':load(BATCH/'pacing-report.json'),
        'mainMixPrefixPreserved':True,'newOutro':True,'userApproval':'pending','continuousFullAVReview':False,
        'limits':'Technical checks and sampled images are distinct from the temporal proof review and user aesthetic feedback.'})

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('phase',choices=['bundle','preflight','proof','render','qa']);parser.add_argument('--revision',default='r01');parser.add_argument('--style',choices=['both','comic','flow'],default='both');parser.add_argument('--concurrency',type=int,default=6);args=parser.parse_args()
    if args.phase=='render':render(args.revision,args.style,args.concurrency)
    else:globals()[args.phase](args.revision)
