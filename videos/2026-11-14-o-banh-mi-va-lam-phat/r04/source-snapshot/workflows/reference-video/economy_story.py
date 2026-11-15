"""Content-first economic stories: isolated script, exact take, photos, gentle cast.

Only `voice` contacts a generation provider. Other phases are local and retain
previous batches. The shared exact-take audio helpers do not select old visuals.
"""
from pathlib import Path
import argparse
import hashlib
import json
import math
import re
import shutil
import subprocess
import time
import wave

import cv2
from PIL import Image, ImageEnhance, ImageFilter, ImageFont, ImageOps
import eleven_audio
import finance_long as timed
from finance_long_render import cli, decoded_frames, sheets

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT/'workflows/reference-video/cinematic'
BATCH = ROOT/'videos/2026-11-14-o-banh-mi-va-lam-phat'
ENTRY = PROJECT/'src/economy-story-entry.tsx'
FPS = 30
VOICE = '6adFm46eyy74snVn6YrT'
FF = timed.FF
save, load, sha, run = timed.save, timed.load, timed.sha, timed.run


def prepare():
    from economy_story_content import CONTENT
    content = json.loads(json.dumps(CONTENT, ensure_ascii=False))
    ids = set()
    for chapter in content['chapters']:
        for beat in chapter['beats']:
            if beat['id'] in ids: raise ValueError('Duplicate beat ID')
            ids.add(beat['id'])
            beat.setdefault('cue', beat['text'].split('.')[0][:28].rstrip())
            if beat['cue'] not in beat['text']: raise ValueError('Missing exact cue')
            beat.setdefault('kind', 'audit' if beat['visual']=='graphic' else 'story')
            if beat['visual']=='graphic': beat.setdefault('graphic',beat['kind'])
            if beat['id']=='e02':
                beat['kind']='disclaimer';beat['graphic']='disclaimer'
            if len(beat['headline']) > 80: raise ValueError('Headline too long')
    path = BATCH/'content.json'
    if path.exists() and load(path) != content: raise ValueError('Script frozen: use a new batch')
    save(path, content)
    script = '\n\n'.join(b['text'] for c in content['chapters'] for b in c['beats'])
    (BATCH/'script.txt').write_text(script, encoding='utf-8')
    requests = []
    for i, chapter in enumerate(content['chapters']):
        text = '\n\n'.join(b['text'] for b in chapter['beats'])
        if len(text)>4900: raise ValueError('Chapter too long for V3')
        requests.append({'chapter':chapter['id'],'file':f'audio/{i+1:02}-{chapter["id"]}.mp3',
            'endpoint':f'/v1/text-to-speech/{VOICE}/with-timestamps',
            'payload':{'text':text,'model_id':'eleven_v3','language_code':'vi',
                'voice_settings':{'stability':.5,'similarity_boost':.8,'speed':1.0}}})
    save(BATCH/'generation-plan.json',{'chapterTakes':requests,'newImageVideoMusicRequests':0,
        'retryPolicy':'Retained unresolved intent prevents duplicate provider requests'})
    save(BATCH/'editorial-brief.json',{'title':content['title'],'wordUnits':len(script.split()),
        'audience':'Người xem muốn hiểu giá cả qua một câu chuyện đời thường',
        'structure':['hook','brief relevant disclaimer','causal economic story','practical CTA'],
        'visualPolicy':'Real photographs for context; original graphics for causal relationships and illustrative arithmetic',
        'characterPolicy':'Fixed placement and pose; gentle cue-based turns only. No bobbing, lip motion or acted gestures.',
        'latestUserOverride':'2026-11-14: content-first, adjust font, characters may remain still and turn with dialogue',
        'fiction':'Hạnh and every shop/price/cost example are fictional; stock photographs do not identify her',
        'branding':False,'userApproval':'pending','voiceSpeed':1.0})
    print('PREPARED',len(script.split()),'word units;',len(requests),'chapters',flush=True)


def voice():
    prepare()
    records=[]
    oldpath=BATCH/'audio/voice-runs.json'
    previous={r['chapter']:r for r in load(oldpath)['chapters']} if oldpath.exists() else {}
    for row in load(BATCH/'generation-plan.json')['chapterTakes']:
        target=BATCH/row['file']
        digest=hashlib.sha256(json.dumps({'endpoint':row['endpoint'],'body':row['payload']},sort_keys=True,ensure_ascii=False).encode()).hexdigest()
        cached=target.exists() or all((eleven_audio.CACHE/(digest+ext)).exists() for ext in ['.mp3','.json','.alignment.json'])
        started=time.perf_counter()
        eleven_audio.generate(target,row['endpoint'],row['payload'],timed=True)
        receipt=load(target.with_suffix('.receipt.json'))
        record={'chapter':row['chapter'],'file':row['file'],'cacheHit':cached,
            'wallSeconds':round(time.perf_counter()-started,3),'sha256':sha(target),
            'receiptSHA256':sha(target.with_suffix('.receipt.json')),
            'providerCharacterCost':receipt.get('character_cost'),'newRequestCredits':0 if cached else receipt.get('character_cost')}
        if row['chapter'] in previous:
            if previous[row['chapter']]['sha256']!=sha(target): raise ValueError('Voice source changed')
            record=previous[row['chapter']]
        records.append(record)
        save(oldpath,{'voiceId':VOICE,'speed':1,'chapters':records,
            'accounting':'Confirmed provider character-cost units; not a USD invoice'})
        print('VOICE_CHAPTER',row['chapter'],flush=True)
    timeline()


def timeline():
    timed.BATCH=BATCH
    timed.timeline()
    plan=load(BATCH/'plan.json')
    fontfile=next(iter((PROJECT/'src/economy-story/fonts').glob('*Regular.ttf')),None)
    if fontfile:
        font=ImageFont.truetype(str(fontfile),36)
        for cap in plan['captions']: cap['pixelWidth']=round(font.getlength(cap['text']),2)
    for beat in plan['segments']:
        if beat['id']=='e40': beat.setdefault('data',{})['stage']='income-prices'
        # Sentence starts are taken from the actual speech alignment; never a sine
        # oscillator running throughout a still character shot.
        words=[w for w in plan['words'] if beat['from']/FPS <= w['start'] < (beat['from']+beat['duration'])/FPS]
        cues=[0]
        for i,w in enumerate(words[:-1]):
            if re.search(r'[.!?;:]$',w['text']): cues.append(max(0,round(words[i+1]['start']*FPS)-beat['from']))
        beat['turnCues']=cues
    save(BATCH/'plan.json',plan)


def mix():
    if (BATCH/'audio/final-mix.wav').exists():
        receipt=load(BATCH/'audio/mix-receipt.json')
        if sha(BATCH/'audio/final-mix.wav')!=receipt['mixSHA256']: raise ValueError('Mix changed')
        return
    timed.BATCH=BATCH
    timed.mix()


def bundle(revision):
    plan=load(BATCH/'plan.json')
    registry=load(BATCH/'research/photo-sources.json')
    assets=registry.get('byTag',registry.get('assetsByTag',registry))
    for tag,rows in assets.items():
        if not isinstance(rows,list): continue
        for asset in rows:
            file=BATCH/asset['file']
            if sha(file)!=asset['sha256']: raise ValueError('Photo changed '+str(file))
            if 'pending' in str(asset.get('inspection','pending')).lower(): raise ValueError('Photo not inspected '+str(file))
    for beat in plan['segments']:
        if beat['visual']=='photo' and not assets.get(beat['assetTag']): raise ValueError('Missing photo tag '+beat['assetTag'])
    plan['assets']=assets
    # Choosing by clause prevents a random tag rotation from using a fuel photo
    # for cooking oil, a printed foreign shop price for our fictional price, or
    # a receipt clause with generic banknotes. These are contextual illustrations.
    catalog={a['id']:a for a in registry.get('assets',[]) if isinstance(a,dict)}
    curated={
        'e01':['vn-filled-banhmi','vn-filled-banhmi-bag'],
        'e03':['baker-kneading','flour-butter'],
        'e04':['bread-basket','receipt-hands'],
        'e06':['vn-filled-banhmi-bag','vn-filled-banhmi'],
        'e07':['vn-market-dalat','grocery-cart'],
        'e13':['receipt-hands','cash-vnd'],
        'e14':['baker-kneading','flour-counter'],
        'e19':['flour-butter','flour-sifting'],
        'e20':['vn-fuel','delivery-truck'],
        'e21':['bread-basket','vn-market-dalat'],
        'e22':['bread-oven','oven-loading'],
        'e23':['baker-kneading','oven-loading'],
        'e25':['cash-vnd','receipt-hands'],
        'e26':['baker-kneading','cash-vnd'],
        'e27':['vn-market-dalat','vn-market-scooters'],
        'e28':['delivery-truck','vn-fuel'],
        'e29':['receipt-hands','bread-basket'],
        'e30':['flour-counter','flour-butter'],
        'e31':['vn-market-dalat','bread-basket'],
        'e32':['vn-market-scooters','grocery-cart'],
        'e34':['budget-couple','receipt-hands'],
        'e35':['cash-vnd','grocery-cart'],
        'e36':['grocery-cart','receipt-hands'],
        'e39':['budget-couple','grocery-cart'],
        'e43':['delivery-truck','cargo-ship'],
        'e44':['cash-vnd','receipt-hands'],
        'e45':['bread-basket','receipt-hands'],
        'e46':['baker-kneading','oven-loading'],
        'e47':['bread-shelf','bread-rustic'],
        'e48':['vn-market-dalat','delivery-truck'],
        'e49':['budget-couple','grocery-cart'],
        'e51':['receipt-hands'],
        'e52':['cash-vnd','receipt-hands'],
        'e53':['bread-basket','vn-filled-banhmi'],
        'e55':['vn-filled-banhmi','vn-filled-banhmi-bag'],
        'e56':['vn-filled-banhmi','vn-filled-banhmi-bag'],
    }
    photo_review=[]
    for beat in plan['segments']:
        if beat['visual']!='photo' or beat['id'] not in curated: continue
        ids=[i for i in curated[beat['id']] if i in catalog]
        if not ids: raise ValueError('No curated contextual photo for '+beat['id'])
        key='clause-'+beat['id'];assets[key]=[catalog[i] for i in ids]
        photo_review.append({'beat':beat['id'],'narration':beat['text'],'assets':ids,
            'role':'context','limits':'Photographs illustrate visible subjects only, not fictional identity, amounts, business condition or causal proof'})
        beat['assetTag']=key
    save(BATCH/'research/clause-photo-selection.json',photo_review)
    # Bake the soft backing once. A 35px browser filter over a full-HD photo on
    # every frame made the measured portrait proof several times slower.
    backgrounds={}
    for rows in assets.values():
        for asset in rows:
            if asset.get('fit')!='contain': continue
            source=BATCH/asset['file']
            file=f'assets/derived/{source.stem}-{asset["sha256"][:10]}-backing.jpg'
            target=BATCH/file;target.parent.mkdir(parents=True,exist_ok=True)
            if file not in backgrounds:
                if not target.exists():
                    with Image.open(source) as raw:
                        image=ImageOps.fit(ImageOps.exif_transpose(raw).convert('RGB'),(1280,720))
                        image=ImageEnhance.Brightness(image.filter(ImageFilter.GaussianBlur(23.333))).enhance(.5)
                        image.save(target,quality=90)
                backgrounds[file]={'file':file,'sha256':sha(target),'sourceSHA256':asset['sha256'],
                    'method':'Original photograph, center-cover1280x720, GaussianBlur23.333px, brightness0.5; decorative backing only'}
            asset['backgroundFile']=file;asset['backgroundSHA256']=backgrounds[file]['sha256']
    save(BATCH/'research/derived-backgrounds.json',list(backgrounds.values()))
    out=BATCH/revision
    out.mkdir(parents=True,exist_ok=True)
    save(out/'props.json',{'plan':plan})
    public=out/'public-assets'
    public.mkdir(exist_ok=True)
    for rows in assets.values():
        if not isinstance(rows,list): continue
        for asset in rows:
            dest=public/asset['file']; dest.parent.mkdir(parents=True,exist_ok=True)
            if not dest.exists(): shutil.copy2(BATCH/asset['file'],dest)
            if sha(dest)!=asset['sha256']: raise ValueError('Public photo changed')
            if asset.get('backgroundFile'):
                dest=public/asset['backgroundFile'];dest.parent.mkdir(parents=True,exist_ok=True)
                if not dest.exists(): shutil.copy2(BATCH/asset['backgroundFile'],dest)
                if sha(dest)!=asset['backgroundSHA256']: raise ValueError('Decorative photo backing changed')
    paths=[Path(__file__),ROOT/'workflows/reference-video/economy_story_content.py',ENTRY,
        ROOT/'workflows/reference-video/finance_long.py',ROOT/'workflows/reference-video/eleven_audio.py',
        PROJECT/'economy-story-preflight.cjs',PROJECT/'package.json',PROJECT/'package-lock.json']
    paths+=list(p for p in (PROJECT/'src/economy-story').rglob('*') if p.is_file())
    paths+=list(p for p in (PROJECT/'src/finance-cast-v2').rglob('*') if p.is_file())
    deps={'sources':{p.relative_to(ROOT).as_posix():sha(p) for p in paths},
        'propsSHA256':sha(out/'props.json'),'mixSHA256':sha(BATCH/'audio/final-mix.wav'),
        'photoCatalogSHA256':sha(BATCH/'research/photo-sources.json'),
        'derivedBackgrounds':backgrounds,'researchSourcesSHA256':sha(BATCH/'research/sources.json')}
    guard=out/'dependencies.json'
    if guard.exists() and load(guard)!=deps: raise ValueError('Frozen render dependencies changed: use new revision')
    save(guard,deps)
    for file in paths:
        target=out/'source-snapshot'/file.relative_to(ROOT);target.parent.mkdir(parents=True,exist_ok=True)
        if not target.exists(): shutil.copy2(file,target)
    if not (out/'bundle/index.html').exists():
        seconds=cli(['bundle',ENTRY,f'--out-dir={out/"bundle"}',f'--public-dir={public}','--log=error'],out/'bundle.log')
        save(out/'bundle-timing.json',{'wallSeconds':seconds})
    return out


def preflight(revision):
    out=bundle(revision)
    with (out/'preflight.log').open('w',encoding='utf-8') as log:
        result=subprocess.run(['node',str(PROJECT/'economy-story-preflight.cjs'),str(out/'bundle'),str(out/'props.json'),str(out)],cwd=PROJECT,stdout=log,stderr=subprocess.STDOUT)
    if result.returncode: raise RuntimeError('Preflight failed; read preflight.log')
    folder=out/'preflight'
    sheets(folder,sorted(folder.glob('beat-*.jpg')),'sheet')
    print('PREFLIGHT_READY',out,flush=True)


def proof(revision,concurrency=4):
    out=bundle(revision);plan=load(out/'props.json')['plan']; beats=plan['segments']
    chosen=[beats[0],beats[len(beats)//2],beats[-1]]
    dest=out/'proof';dest.mkdir(exist_ok=True);rows=[]
    for beat in chosen:
        file=dest/(beat['id']+'.mp4')
        start=beat['from'];end=start+beat['duration']
        if not file.exists():
            elapsed=cli(['render',out/'bundle','EconomyStory',file,f'--props={out/"props.json"}',
                f'--frames={start}-{end-1}','--codec=h264','--crf=20',f'--concurrency={concurrency}','--muted','--log=info'],dest/(beat['id']+'.log'))
            rows.append({'id':beat['id'],'from':start,'end':end,'sha256':sha(file),'wallSeconds':elapsed})
        # A/V proof keeps the relevant exact-take sound, no speech regeneration.
        av=dest/(beat['id']+'-av.mp4')
        if not av.exists():
            run([FF,'-y','-v','error','-i',file,'-ss',start/FPS,'-i',BATCH/'audio/final-mix.wav',
                '-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-t',(end-start)/FPS,'-movflags','+faststart',av])
    save(dest/'proof-receipts.json',rows)
    print('PROOFS_READY',flush=True)


def render(revision,concurrency=4):
    out=bundle(revision);plan=load(out/'props.json')['plan'];n=plan['durationFrames']
    dest=out/'chunks';dest.mkdir(exist_ok=True);records=[];files=[]
    for i,start in enumerate(range(0,n,1800)):
        end=min(n,start+1800);file=dest/f'{i:02}.mp4';receipt=file.with_suffix('.json')
        if file.exists() and not receipt.exists(): file.rename(file.with_name(file.stem+f'.incomplete-{time.time_ns()}.mp4'))
        if file.exists() and sha(file)!=load(receipt)['sha256']: raise ValueError('Rendered chunk changed')
        if not file.exists():
            elapsed=cli(['render',out/'bundle','EconomyStory',file,f'--props={out/"props.json"}',
                f'--frames={start}-{end-1}','--codec=h264','--crf=19',f'--concurrency={concurrency}',
                '--color-space=bt709','--pixel-format=yuv420p','--muted','--log=info'],dest/f'{i:02}.log')
            count=decoded_frames(file)
            if count!=end-start: raise ValueError('Incomplete rendered chunk')
            save(receipt,{'from':start,'endExclusive':end,'decodedFrames':count,'wallSeconds':elapsed,
                'framesPerSecond':count/elapsed,'sha256':sha(file)})
        records.append(load(receipt));files.append(file)
        save(out/'render-timing.json',{'chunks':records,'renderWallSeconds':sum(r['wallSeconds'] for r in records),
            'renderedFrames':sum(r['decodedFrames'] for r in records)})
        print('CHUNK_READY',i+1,math.ceil(n/1800),flush=True)
    final=out/'final.mp4'
    if not final.exists():
        listing=out/'concat.txt'
        listing.write_text('\n'.join("file '"+str(f.resolve()).replace('\\','/')+"'" for f in files),encoding='utf-8')
        run([FF,'-y','-v','error','-f','concat','-safe','0','-i',listing,'-i',BATCH/'audio/final-mix.wav',
            '-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-ac','2',
            '-t',n/FPS,'-movflags','+faststart',final])
    print('FILM_READY',final,flush=True)


def qa(revision):
    out=BATCH/revision;plan=load(out/'props.json')['plan'];file=out/'final.mp4'
    dest=out/'qa';dest.mkdir(exist_ok=True)
    count=decoded_frames(file)
    if count!=plan['durationFrames']: raise ValueError('Final frame count mismatch')
    cap=cv2.VideoCapture(str(file));samples=[]
    for beat in plan['segments']:
        for name,t in [('early',.14),('middle',.5),('late',.85)]:
            frame=beat['from']+int(beat['duration']*t)
            cap.set(cv2.CAP_PROP_POS_FRAMES,frame);ok,img=cap.read()
            if not ok: raise ValueError('Unreadable frame')
            target=dest/f'{beat["id"]}-{name}-{frame:05}.jpg';cv2.imwrite(str(target),img)
            samples.append({'id':beat['id'],'frame':frame,'file':target.name})
    cap.release();sheets(dest,sorted(dest.glob('*.jpg')),'contact')
    pcm=dest/'decoded-audio.pcm'
    run([FF,'-y','-v','error','-i',file,'-map','0:a:0','-ac','1','-ar','48000','-f','s16le',pcm])
    seconds=pcm.stat().st_size/96000;digest=sha(pcm);pcm.unlink()
    if seconds<plan['words'][-1]['end'] or abs(seconds-count/FPS)>.1: raise ValueError('Incomplete audio')
    loud=run([FF,'-hide_banner','-i',file,'-af','ebur128=peak=true','-f','null','-']).stderr.decode(errors='replace')
    (dest/'loudness.txt').write_text(loud[-1800:],encoding='utf-8')
    save(out/'qa-report.json',{'technical':'passed','sha256':sha(file),'decodedFrames':count,'seconds':count/FPS,
        'decodedAudioSeconds':seconds,'audioPCMHash':digest,'lastWordEnd':plan['words'][-1]['end'],
        'voiceSpeed':1,'voice':'Nhật Phong','captionMaxPixelWidth':max(c['pixelWidth'] for c in plan['captions']),
        'samples':samples,'newPaidImageVideoMusicCalls':0,'userApproval':'pending',
        'continuousAVReview':False,'limits':'Full decode and sampled frames do not establish continuous watching/listening or user aesthetic approval'})
    print('FULL_QA',count,round(count/FPS,2),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('phase',choices=['prepare','voice','timeline','mix','bundle','preflight','proof','render','qa'])
    parser.add_argument('--revision',default='r01');parser.add_argument('--concurrency',type=int,default=4)
    args=parser.parse_args()
    if args.phase in ['prepare','voice','timeline','mix']: globals()[args.phase]()
    elif args.phase in ['render','proof']: globals()[args.phase](args.revision,args.concurrency)
    else: globals()[args.phase](args.revision)
