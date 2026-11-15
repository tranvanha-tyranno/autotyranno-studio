"""Photo-primary finance revisions: immutable real assets, exact retained audio.

This module never calls speech, image, music or video generation providers.
Moving-photo illustration is not claimed to be filmed B-roll.
"""
from pathlib import Path
import argparse, hashlib, json, shutil, subprocess, time, wave
import cv2
from finance_pace import ROOT, PROJECT, BATCH as AUDIO_BATCH, FPS, FF, save, load, sha, run
from finance_long_render import cli, decoded_frames, sheets

BATCH = ROOT/'videos/2026-11-14-tai-chinh-anh-that'
ENTRY = PROJECT/'src/finance-photo-entry.tsx'
STYLES = [('comic','FinancePhotoComic'),('clean','FinancePhotoClean')]
PROOFS = ['b01','b12','b15','b26','b32','b42','subscribe']


def bundle(revision):
    plan = load(BATCH/'photo-plan.json')
    assert plan['durationFrames'] == load(AUDIO_BATCH/'plan.json')['durationFrames']
    assert plan['captions'] == load(AUDIO_BATCH/'plan.json')['captions']
    assert plan['words'] == load(AUDIO_BATCH/'plan.json')['words']
    assert plan['segments'] == load(AUDIO_BATCH/'plan.json')['segments']
    audio = BATCH/'audio/final-mix.wav'; audio.parent.mkdir(exist_ok=True)
    if not audio.exists(): shutil.copy2(AUDIO_BATCH/'audio/final-mix.wav',audio)
    assert sha(audio) == sha(AUDIO_BATCH/'audio/final-mix.wav')
    shots = plan['photoShots']; n = 0
    for shot in shots:
        assert shot['from'] == n and shot['duration'] > 0
        assert shot['mode'] in ['photo','simulation']; n += shot['duration']
        if shot['mode'] == 'photo': assert shot['assets']
    assert n == plan['durationFrames']
    photos = sum(s['duration'] for s in shots if s['mode']=='photo')
    assert photos/n > .65, 'Real photographs must be primary, not decorative inserts'
    assets = plan['assets']
    if isinstance(assets,dict): assets = list(assets.values())
    out = BATCH/revision; out.mkdir(exist_ok=True)
    paths = [ENTRY,Path(__file__),ROOT/'workflows/reference-video/finance_photo_plan.py',
             ROOT/'workflows/reference-video/finance_photo_assets.py',PROJECT/'finance-photo-preflight.cjs',
             PROJECT/'package.json',PROJECT/'package-lock.json']
    for folder in ['finance-photo','finance-pace-comic','finance-pace-flow','finance-cast-v2','finance-long-comic','finance-flow']:
        paths.extend(p for p in (PROJECT/'src'/folder).rglob('*') if p.is_file())
    asset_hashes = {}
    for asset in assets:
        file = BATCH/asset['file']; digest = sha(file)
        assert digest == asset['sha256']; asset_hashes[asset['id']] = digest
        assert asset.get('sourceURL') or asset.get('page') or asset.get('source',{}).get('url')
        assert asset.get('license') or asset.get('source',{}).get('license')
        inspection=asset.get('inspection','pending')
        assert 'pending' not in str(inspection).lower() and asset.get('observed'), 'Actual photo inspection is pending: '+asset['id']
    deps = {'sources':{p.relative_to(ROOT).as_posix():sha(p) for p in paths},
            'planSHA256':sha(BATCH/'photo-plan.json'),'mixSHA256':sha(audio),'assetSHA256':asset_hashes}
    guard = out/'dependencies.json'
    if guard.exists() and load(guard) != deps: raise ValueError('Frozen source/asset/plan changed: use a new revision')
    save(guard,deps); save(out/'props.json',{'plan':plan})
    public = out/'public-assets'; public.mkdir(exist_ok=True)
    for asset in assets:
        target = public/asset['file']; target.parent.mkdir(parents=True,exist_ok=True)
        if not target.exists(): shutil.copy2(BATCH/asset['file'],target)
        assert sha(target) == asset['sha256']
    for p in paths:
        target = out/'source-snapshot'/p.relative_to(ROOT); target.parent.mkdir(parents=True,exist_ok=True)
        if not target.exists(): shutil.copy2(p,target)
    if not (out/'bundle/index.html').exists():
        seconds = cli(['bundle',ENTRY,f'--out-dir={out/"bundle"}',f'--public-dir={public}','--log=error'],out/'bundle.log')
        save(out/'bundle-timing.json',{'wallSeconds':seconds})
    return out


def preflight(revision):
    out=bundle(revision); start=time.perf_counter()
    with (out/'preflight.log').open('w',encoding='utf-8') as log:
        result=subprocess.run(['node',str(PROJECT/'finance-photo-preflight.cjs'),str(out/'bundle'),str(out/'props.json'),str(out)],cwd=PROJECT,stdout=log,stderr=subprocess.STDOUT)
    if result.returncode: raise RuntimeError('Photo preflight failed; inspect log')
    for style,_ in STYLES:
        folder=out/style/'preflight'; sheets(folder,sorted(folder.glob('shot-*.jpg')),'sheet')
    save(out/'preflight-timing.json',{'wallSeconds':time.perf_counter()-start})
    print('PHOTO_PREFLIGHT_READY',flush=True)


def proof(revision):
    out=bundle(revision); plan=load(BATCH/'photo-plan.json')
    for style,composition in STYLES:
        dest=out/style/'proof'; dest.mkdir(parents=True,exist_ok=True); records=[]
        old={r['beat']:r for r in load(dest/'receipt.json')['clips']} if (dest/'receipt.json').exists() else {}
        for beat in PROOFS:
            b=next(s for s in plan['segments'] if s['id']==beat); file=dest/(beat+'.mp4')
            if not file.exists():
                props=dest/(beat+'-props.json'); save(props,{'plan':plan,'fromFrame':b['from'],'frames':b['duration']})
                sec=cli(['render',out/'bundle',composition,dest/(beat+'-silent.mp4'),f'--props={props}',
                         '--scale=.6','--codec=h264','--crf=19','--muted','--concurrency=5','--log=error'],dest/(beat+'.log'))
                run([FF,'-y','-v','error','-i',dest/(beat+'-silent.mp4'),'-ss',b['from']/FPS,'-i',BATCH/'audio/final-mix.wav',
                     '-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k','-t',b['duration']/FPS,'-movflags','+faststart',file])
            else:
                sec=old.get(beat,{}).get('wallSeconds')
                if beat in old: assert sha(file)==old[beat]['sha256']
            cap=cv2.VideoCapture(str(file)); count=0
            assert cap.isOpened()
            while cap.grab(): count+=1
            cap.release(); assert count==b['duration']
            records.append({'beat':beat,'from':b['from'],'frames':count,'sha256':sha(file),'file':str(file.relative_to(BATCH)),'wallSeconds':sec})
            save(dest/'receipt.json',{'clips':records,'review':'pending temporal photo/crop/semantic inspection'})
            print('PHOTO_PROOF',style,beat,flush=True)


def render(revision,chosen='both',concurrency=6):
    out=bundle(revision); plan=load(BATCH/'photo-plan.json'); frames=plan['durationFrames']
    review=load(out/'motion-review.json')
    assert review['bundleDependenciesSHA256']==sha(out/'dependencies.json')
    for style,composition in STYLES:
        if chosen!='both' and chosen!=style: continue
        check=review['styles'][style]; assert check['decision']=='ready_for_long_render' and check['observations']
        observed={r['beat']:r for r in check['clips']}
        proofs=load(out/style/'proof/receipt.json')['clips']
        assert set(observed)==set(PROOFS)
        for r in proofs: assert sha(BATCH/r['file'])==r['sha256']==observed[r['beat']]['sha256']
        dest=out/style; chunks=dest/'chunks'; chunks.mkdir(exist_ok=True); files=[]; timings=[]
        for i,start in enumerate(range(0,frames,1800)):
            end=min(frames,start+1800); file=chunks/f'{i:02}.mp4'; receipt=file.with_suffix('.json')
            if file.exists() and not receipt.exists(): file.rename(file.with_name(file.stem+f'.incomplete-{time.time_ns()}.mp4'))
            if file.exists(): assert load(receipt)['sha256']==sha(file)
            else:
                sec=cli(['render',out/'bundle',composition,file,f'--props={out/"props.json"}',f'--frames={start}-{end-1}',
                         '--codec=h264','--crf=19',f'--concurrency={concurrency}','--color-space=bt709','--pixel-format=yuv420p','--muted','--log=info'],chunks/f'{i:02}.log')
                count=decoded_frames(file); assert count==end-start
                save(receipt,{'from':start,'endExclusive':end,'decodedFrames':count,'sha256':sha(file),'wallSeconds':sec,'framesPerSecond':count/sec})
            files.append(file); timings.append(load(receipt))
            save(dest/'render-timing.json',{'chunks':timings,'renderWallSeconds':sum(x['wallSeconds'] for x in timings),'renderedFrames':sum(x['decodedFrames'] for x in timings)})
            print('PHOTO_CHUNK_READY',style,i+1,11,flush=True)
        final=dest/'final.mp4'
        if not final.exists():
            concat=dest/'concat.txt'; concat.write_text('\n'.join("file '"+str(p).replace('\\','/')+"'" for p in files),encoding='utf-8')
            run([FF,'-y','-v','error','-f','concat','-safe','0','-i',concat,'-i',BATCH/'audio/final-mix.wav','-map','0:v:0','-map','1:a:0',
                 '-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-ac','2','-t',frames/FPS,'-movflags','+faststart',final])
        print('PHOTO_FILM_READY',style,flush=True)


def qa(revision):
    out=BATCH/revision; plan=load(BATCH/'photo-plan.json'); records=[]
    assert sha(BATCH/'audio/final-mix.wav')==sha(AUDIO_BATCH/'audio/final-mix.wav')
    for style,_ in STYLES:
        file=out/style/'final.mp4'; dest=out/style/'qa'; dest.mkdir(exist_ok=True)
        frames=decoded_frames(file); assert frames==plan['durationFrames']
        cap=cv2.VideoCapture(str(file)); samples=[]
        for s in plan['photoShots']:
            f=s['from']+round(s['duration']*.55); cap.set(cv2.CAP_PROP_POS_FRAMES,f); ok,bgr=cap.read(); assert ok
            target=dest/f'shot-{s["id"]}-{f:05}.jpg'; cv2.imwrite(str(target),bgr)
            samples.append({'shot':s['id'],'frame':f,'mode':s['mode'],'assets':s.get('assets',[]),'file':target.name,'sha256':sha(target)})
        cap.release(); sheets(dest,sorted(dest.glob('shot-*.jpg')),'contact')
        pcm=dest/'audio.pcm'; run([FF,'-y','-v','error','-i',file,'-map','0:a:0','-ar','48000','-ac','1','-f','s16le',pcm])
        seconds=pcm.stat().st_size/96000; digest=sha(pcm); pcm.unlink()
        assert abs(seconds-frames/FPS)<.1 and seconds>plan['words'][-1]['end']
        records.append({'style':style,'sha256':sha(file),'bytes':file.stat().st_size,'decodedFrames':frames,'seconds':frames/FPS,
                        'decodedAudioSeconds':seconds,'audioPCMHash':digest,'lastWordEnd':plan['words'][-1]['end'],'samples':samples})
        print('PHOTO_FULL_QA',style,frames,flush=True)
    assert records[0]['audioPCMHash']==records[1]['audioPCMHash']
    save(out/'qa-report.json',{'technical':'passed','records':records,'sameDecodedAudio':True,'exactRetainedMix':True,
                             'photoCoverage':load(BATCH/'photo-coverage.json'),'paidGenerationCalls':0,'userApproval':'pending',
                             'continuousFullAVReview':False,'limits':'All frames decoded and every shot sampled; this is separate from temporal proof inspection and user visual approval.'})


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('phase',choices=['bundle','preflight','proof','render','qa']);p.add_argument('--revision',default='r01')
    p.add_argument('--style',choices=['both','comic','clean'],default='both');p.add_argument('--concurrency',type=int,default=6);a=p.parse_args()
    if a.phase=='render': render(a.revision,a.style,a.concurrency)
    else: globals()[a.phase](a.revision)
