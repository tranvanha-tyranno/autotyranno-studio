"""Sequential, checkpointed chapter rendering from an immutable business bundle."""
import argparse,datetime,json,shutil,subprocess,sys,uuid
from pathlib import Path
import cv2
import business,render_directions
from documentary import FF

WORK=Path(__file__).resolve().parent
PROJECT=WORK/'cinematic'
CLI=PROJECT/'node_modules/@remotion/cli/remotion-cli.js'
save=business.save;load=business.load;sha=business.sha;require=business.require

def decoded(path,expected):
    cap=cv2.VideoCapture(str(path));require(cap.isOpened(),'Undecodable chapter: '+str(path));n=0
    while cap.grab():n+=1
    fps=cap.get(cv2.CAP_PROP_FPS);cap.release()
    require(n==expected and abs(fps-30)<.001,'Chapter frame count differs: '+str(path))
    return {'sha256':sha(path),'frames':n,'fps':fps}

def run(command,log):
    with log.open('w',encoding='utf-8') as out:
        out.write(json.dumps({'argv':list(map(str,command))},ensure_ascii=False)+'\n');out.flush()
        result=subprocess.run(list(map(str,command)),cwd=PROJECT,stdout=out,stderr=subprocess.STDOUT)
    require(result.returncode==0,'Render step failed; retained log: '+str(log))

def render(batch,resume=None):
    batch=Path(batch).resolve();require(not(batch/'final.mp4').exists(),'Final exists; use a new revision')
    data=load(batch/'data.json');business.validate(load(batch/'content.json'));business.validate_media_intervals(data)
    mix=batch/'audio/final-mix.wav';report=load(batch/'audio/mix-report.json')
    require(mix.is_file(),'Complete sound mix before rendering')
    require(sha(mix)==report['mix']['sha256'],'Sound mix differs from pinned source receipt')
    require(sha(batch/'production-public/business/mix.wav')==sha(mix),'Public mix is stale')
    require(shutil.disk_usage(batch).free>2_000_000_000,'Less than2GB storage; preserve data and free capacity first')
    attempt=Path(resume).resolve() if resume else batch/'render-attempts'/datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    if not resume:
        attempt.mkdir(parents=True);snap=attempt/'source-snapshot';snap.mkdir()
        files=[batch/x for x in ['content.json','data.json','props.json','visual-plan.json','source-receipts.json','clip-intervals.json','media-interval-check.json','preflight.json','audio/mix-report.json','audio/narration.receipt.json']]
        records=[]
        for p in files:
            target=snap/'batch'/p.relative_to(batch);target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
            records.append({'file':target.relative_to(snap).as_posix(),'sha256':sha(target)})
        code=[WORK/x for x in ['business.py','business_audio.py','business_render.py','eleven_audio.py','cinematic/src/business-entry.tsx','cinematic/package.json','cinematic/package-lock.json']]
        code+=list((PROJECT/'src/business').rglob('*'))
        for p in code:
            if not p.is_file():continue
            target=snap/'workflow'/p.relative_to(WORK);target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
            records.append({'file':target.relative_to(snap).as_posix(),'sha256':sha(target)})
        save(snap/'hashes.json',records)
        groups=[]
        for shot in data['shots']:
            if not groups or groups[-1]['id']!=shot['chapter']:groups.append({'id':shot['chapter'],'start':shot['start'],'end':shot['end']})
            else:groups[-1]['end']=shot['end']
        state={'status':'preparing','frames':data['frames'],'dataSHA256':sha(batch/'data.json'),'propsSHA256':sha(batch/'props.json'),
             'mixSHA256':sha(mix),'parts':groups,'concurrency':2,'mediaCacheBytes':268435456,'userAcceptance':'pending'}
        save(attempt/'state.json',state)
        run(['node',CLI,'bundle',PROJECT/'src/business-entry.tsx',f'--out-dir={attempt/"bundle"}',f'--public-dir={batch/"production-public"}','--log=error'],attempt/'bundle.log')
        state['bundleFiles']=[{'file':p.relative_to(attempt/'bundle').as_posix(),'sha256':sha(p)} for p in (attempt/'bundle').rglob('*') if p.is_file()]
        save(attempt/'state.json',state)
    state=load(attempt/'state.json')
    require(state['dataSHA256']==sha(batch/'data.json') and state['propsSHA256']==sha(batch/'props.json') and state['mixSHA256']==sha(mix),'Frozen render inputs changed; use new revision')
    for r in state['bundleFiles']:require(sha(attempt/'bundle'/r['file'])==r['sha256'],'Frozen bundle changed')
    for r in load(attempt/'source-snapshot/hashes.json'):require(sha(attempt/'source-snapshot'/r['file'])==r['sha256'],'Source snapshot changed')
    state['status']='running';save(attempt/'state.json',state)
    try:
        for index,part in enumerate(state['parts']):
            target=attempt/f'part-{index:02}.mp4';frames=part['end']-part['start']
            if part.get('complete'):
                require(target.is_file() and sha(target)==part['receipt']['sha256'],'Completed chapter changed')
                decoded(target,frames);print('REUSE',part['id'],frames,flush=True);continue
            if target.exists():target.rename(target.with_name(target.stem+'-failed-'+uuid.uuid4().hex[:6]+target.suffix))
            require(shutil.disk_usage(batch).free>1_500_000_000,'Storage fell below1.5GB; resume after space is available')
            print('RENDER',part['id'],part['start'],part['end']-1,flush=True)
            run(['node',CLI,'render',attempt/'bundle','BusinessPreview',target,f'--props={batch/"props.json"}',
                 f'--frames={part["start"]}-{part["end"]-1}','--muted','--codec=h264','--crf=18',
                 '--concurrency=2','--media-cache-size-in-bytes=268435456','--log=info'],attempt/f'part-{index:02}.log')
            part['receipt']=decoded(target,frames);part['complete']=True;save(attempt/'state.json',state)
        listing=attempt/'concat.txt';listing.write_text('\n'.join("file '"+(attempt/f'part-{i:02}.mp4').as_posix()+"'" for i in range(len(state['parts']))),encoding='utf-8')
        print('JOIN',state['frames'],'frames',flush=True)
        output=attempt/'joined.mp4'
        run([FF,'-y','-v','error','-f','concat','-safe','0','-i',listing,'-i',mix,'-map','0:v:0','-map','1:a:0',
            '-vf','setsar=1,scale=iw:ih:in_range=auto:out_range=tv:out_color_matrix=bt709,format=yuv420p',
            '-c:v','libx264','-preset','fast','-crf','18','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-color_range','tv',
            '-r','30','-c:a','aac','-b:a','192k','-ar','48000','-ac','2','-t',str(state['frames']/30),'-movflags','+faststart',output],attempt/'join.log')
        final=decoded(output,state['frames']);output.replace(batch/'final.mp4');state.update({'status':'completed','final':final})
        save(attempt/'state.json',state);save(batch/'render-receipt.json',{'attempt':str(attempt),'finalSHA256':final['sha256'],
             'frames':state['frames'],'audioMixSHA256':state['mixSHA256'],'concurrency':2,'userAcceptance':'pending'})
        print('COMPLETED',batch/'final.mp4',flush=True)
    except BaseException as e:
        state.update({'status':'failed','errorType':type(e).__name__,'error':str(e)});save(attempt/'state.json',state);raise

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--batch',type=Path,required=True);p.add_argument('--resume',type=Path);a=p.parse_args();render(a.batch,a.resume)
