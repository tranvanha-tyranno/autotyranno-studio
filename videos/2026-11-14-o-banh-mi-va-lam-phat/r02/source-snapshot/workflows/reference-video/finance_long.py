"""Two complete finance films, shared chapter takes and isolated local graphics.

The voice phase is billable and uses the existing fail-closed provider cache.
Visual revisions never call a provider. Existing exports are never overwritten.
"""
from pathlib import Path
import argparse, hashlib, json, math, re, shutil, subprocess, time, wave
import numpy as np
import eleven_audio
from documentary import FF

ROOT = Path(__file__).resolve().parents[2]
BATCH = ROOT / 'videos/2026-11-13-hai-style-10-phut'
PROJECT = ROOT / 'workflows/reference-video/cinematic'
VOICE = '6adFm46eyy74snVn6YrT'
FPS = 30

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p, v):
    p = Path(p); p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(v, ensure_ascii=False, indent=2), encoding='utf-8')
def load(p): return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def run(args):
    result = subprocess.run([str(a) for a in args], capture_output=True)
    if result.returncode: raise RuntimeError(result.stderr.decode('utf-8', errors='replace')[-5000:])
    return result
def content():
    from finance_long_content import CONTENT
    return CONTENT
def prepare():
    c = content(); BATCH.mkdir(parents=True, exist_ok=True)
    target = BATCH/'content.json'
    if target.exists() and load(target) != c: raise ValueError('Content is frozen; use a new batch for another script')
    save(target, c)
    script = '\n\n'.join(b['text'] for ch in c['chapters'] for b in ch['beats'])
    (BATCH/'script.txt').write_text(script, encoding='utf-8')
    requests = []
    for i, ch in enumerate(c['chapters']):
        text = '\n\n'.join(b['text'] for b in ch['beats'])
        if len(text) > 4900: raise ValueError('Chapter exceeds safe V3 input length')
        requests.append({'chapter':ch['id'], 'file':f'audio/{i+1:02}-{ch["id"]}.mp3',
            'endpoint':f'/v1/text-to-speech/{VOICE}/with-timestamps',
            'payload':{'text':text, 'model_id':'eleven_v3', 'language_code':'vi',
                'voice_settings':{'stability':.5, 'similarity_boost':.8, 'speed':1.0}}})
    save(BATCH/'generation-plan.json', {'chapterTakes':requests,'sharedAcrossStyles':True,
        'newImageVideoMusicRequests':0,'retryPolicy':'Retained unresolved intent prevents duplicate paid calls'})
    save(BATCH/'editorial-brief.json', {'title':c['title'], 'audience':'Người đi làm muốn kiểm soát dòng tiền',
        'structure':['hook','brief relevant disclaimer','mechanisms and limits','30-day actionable CTA'],
        'styles':['expressive adult comic','continuous minimal object actions'],
        'comparison':'Two full films with identical narration and audio mix',
        'fiction':'Minh and Lan are fictional adults; all monetary parameters are illustrative, not survey statistics',
        'branding':False,'approval':'Pending feedback on these new full films',
        'wordUnits':len(script.split()),'voice':'Nhật Phong / eleven_v3 / natural speed1.0'})
    save(BATCH/'sources.json', {'consulted':'2026-11-13','allMoneyExamples':'Original fictional illustrative arithmetic',
        'sources':[
            {'url':'https://www.consumerfinance.gov/an-essential-guide-to-building-an-emergency-fund/',
             'publisher':'Consumer Financial Protection Bureau','supports':['Reserve depends on circumstances','Cash flow is timing of receipts/payments','Optional automatic saving with balance monitoring'],
             'scope':'General education only; no US-specific account/legal rules transferred to Vietnam; original paraphrase'},
            {'url':'https://www.consumerfinance.gov/consumer-tools/educator-tools/your-money-your-goals/toolkit/',
             'publisher':'Consumer Financial Protection Bureau','supports':['Spending tracker','Bill calendar','Cash flow budget','Review goals'],
             'scope':'Method context, not evidence for fictional salaries or Vietnamese population statistics'}],
        'artwork':'Original local SVG animation and previously retained fictional-adult rig; no third-party artwork copied'})
    print('PREPARED',len(script.split()),'word units;',len(requests),'shared chapter requests',flush=True)

def voice():
    prepare(); records=[]
    previous={v['chapter']:v for v in load(BATCH/'audio/voice-runs.json')['chapters']} if (BATCH/'audio/voice-runs.json').exists() else {}
    for row in load(BATCH/'generation-plan.json')['chapterTakes']:
        target=BATCH/row['file']; already=target.exists(); started=time.perf_counter()
        payload=row['payload']; digest=hashlib.sha256(json.dumps({'endpoint':row['endpoint'],'body':payload},sort_keys=True,ensure_ascii=False).encode()).hexdigest()
        cached=already or all((eleven_audio.CACHE/(digest+suffix)).exists() for suffix in ['.mp3','.json','.alignment.json'])
        eleven_audio.generate(target,row['endpoint'],payload,timed=True)
        receipt=load(target.with_suffix('.receipt.json'))
        record={'chapter':row['chapter'],'file':row['file'],'cacheHit':cached,'wallSeconds':round(time.perf_counter()-started,3),
            'sha256':sha(target),'receiptSHA256':sha(target.with_suffix('.receipt.json')),
            'providerCharacterCost':receipt.get('character_cost'),'newRequestCredits':0 if cached else receipt.get('character_cost')}
        if row['chapter'] in previous:
            if previous[row['chapter']]['sha256']!=sha(target):raise ValueError('Recorded chapter voice changed')
            record=previous[row['chapter']]
        records.append(record)
        save(BATCH/'audio/voice-runs.json',{'voiceId':VOICE,'speed':1.0,'chapters':records,
            'accounting':'Provider character-cost header units only; not an invoice or a dollar conversion'})
        print('VOICE_CHAPTER',row['chapter'],flush=True)
    timeline()

def timeline():
    c=load(BATCH/'content.json'); requests=load(BATCH/'generation-plan.json')['chapterTakes']
    segments=[]; allwords=[]; chapter_rows=[]; cursor_samples=0; pieces=[]
    rate=48000; gap_samples=round(.45*rate)
    silence=BATCH/'audio/chapter-gap.wav'
    with wave.open(str(silence),'wb') as w:
        w.setparams((1,2,rate,0,'NONE','not compressed'));w.writeframes(b'\0\0'*gap_samples)
    for i,(ch,row) in enumerate(zip(c['chapters'],requests)):
        source=BATCH/row['file']; a=load(source.with_suffix('.alignment.json'))
        text=row['payload']['text']
        if ''.join(a['characters'])!=text: raise ValueError('Alignment differs from exact script '+ch['id'])
        receipt=load(source.with_suffix('.receipt.json'))
        if sha(source)!=receipt['sha256']: raise ValueError('Voice source changed')
        wav=source.with_suffix('.wav')
        run([FF,'-y','-v','error','-i',source,'-ac','1','-ar',rate,'-c:a','pcm_s16le',wav])
        with wave.open(str(wav),'rb') as w: samples=w.getnframes()
        offset=cursor_samples/rate; pieces.append(wav)
        words=eleven_audio.words(a)
        allwords.extend([{**w,'start':w['start']+offset,'end':w['end']+offset} for w in words])
        char=0; ch_start=round(offset*FPS)
        for beat in ch['beats']:
            start=char;end=start+len(beat['text']);char=end+2
            at=a['character_start_times_seconds'][start]+offset
            until=a['character_end_times_seconds'][end-1]+offset
            cuepos=beat['text'].casefold().find(beat['cue'].casefold())
            if cuepos<0:raise ValueError('Cue phrase absent '+beat['id'])
            cue_at=a['character_start_times_seconds'][start+cuepos]+offset
            segments.append({**beat,'from':round(at*FPS),'duration':0,'speechStart':round(at*FPS),
                'speechEnd':math.ceil(until*FPS),'cueFrame':round(cue_at*FPS)-round(at*FPS),
                'chapterId':ch['id'],'chapterTitle':ch['title'],'chapterIndex':i+1})
        chapter_rows.append({'id':ch['id'],'title':ch['title'],'from':ch_start,
            'seconds':samples/rate,'sourceSHA256':sha(source),'alignmentSHA256':sha(source.with_suffix('.alignment.json'))})
        cursor_samples+=samples
        if i<len(c['chapters'])-1:pieces.append(silence);cursor_samples+=gap_samples
    frames=math.ceil((cursor_samples/rate+1.2)*FPS)
    segments[0]['cueFrame']+=segments[0]['from'];segments[0]['from']=0
    for i,s in enumerate(segments):s['duration']=(segments[i+1]['from'] if i+1<len(segments) else frames)-s['from']
    captions=[]; group=[]
    from PIL import ImageFont
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',36)
    def flush():
        if not group:return
        t=' '.join(w['text'] for w in group)
        captions.append({'from':round(group[0]['start']*FPS),'end':math.ceil(group[-1]['end']*FPS),
            'text':t,'startMs':round(group[0]['start']*1000),'endMs':round(group[-1]['end']*1000),
            'timestampMs':None,'confidence':None,'pixelWidth':round(font.getlength(t),2)})
        group.clear()
    for w in allwords:
        candidate=' '.join(x['text'] for x in group+[w])
        if group and (len(group)>=10 or font.getlength(candidate)>1490 or w['end']-group[0]['start']>3.5):flush()
        group.append(w)
        if re.search(r'[.!?;:]$',w['text']):flush()
    flush()
    plan={'fps':FPS,'durationFrames':frames,'title':c['title'],'segments':segments,'captions':captions,
        'words':allwords,'chapters':chapter_rows,'voiceSpeed':1.0}
    save(BATCH/'plan.json',plan)
    save(BATCH/'captions.json',[{k:v for k,v in cap.items() if k in ['text','startMs','endMs','timestampMs','confidence']} for cap in captions])
    concat=BATCH/'audio/concat.txt'
    concat.write_text('\n'.join("file '"+str(p.resolve()).replace('\\','/')+"'" for p in pieces),encoding='utf-8')
    run([FF,'-y','-v','error','-f','concat','-safe','0','-i',concat,'-af',f'apad=whole_dur={frames/FPS}',
        '-t',frames/FPS,'-ar',rate,'-ac','1','-c:a','pcm_s16le',BATCH/'audio/narration.wav'])
    save(BATCH/'clause-coverage.json',[{'id':s['id'],'text':s['text'],'from':s['from'],'end':s['from']+s['duration'],
        'kind':s['kind'],'cue':s['cue'],'cueFrame':s['cueFrame'],'review':'Pending actual rendered samples'} for s in segments])
    print('TIMELINE',frames,'frames',round(frames/FPS,3),'seconds',flush=True)

def mix():
    p=load(BATCH/'plan.json'); seconds=p['durationFrames']/FPS
    voicefile=BATCH/'audio/voice-normalized.wav'
    run([FF,'-y','-v','error','-i',BATCH/'audio/narration.wav','-af','loudnorm=I=-16:TP=-2:LRA=11',
        '-ar','48000','-ac','2','-c:a','pcm_s16le',voicefile])
    names=['coffee-opening','precise-unit-math','cash-tension','operating-pulse','agency-bridge','hopeful-outro']
    music=[]; provenance=[]
    source_dir=ROOT/'videos/2026-11-13-quan-dong-khach-het-tien/audio/music'
    for name in names:
        source=source_dir/(name+'.mp3'); receipt=load(source.with_suffix('.receipt.json'))
        if sha(source)!=receipt['sha256']:raise ValueError('Music receipt mismatch '+name)
        target=BATCH/'audio/music'/source.name;target.parent.mkdir(exist_ok=True)
        if not target.exists():shutil.copy2(source,target);shutil.copy2(source.with_suffix('.receipt.json'),target.with_suffix('.receipt.json'))
        if sha(target)!=receipt['sha256'] or sha(target.with_suffix('.receipt.json'))!=sha(source.with_suffix('.receipt.json')):raise ValueError('Reused music target changed '+name)
        music.append(target);provenance.append({'source':str(source.relative_to(ROOT)),'sha256':sha(source),'receiptSHA256':sha(source.with_suffix('.receipt.json'))})
    args=[FF,'-y','-v','error']
    for file in music:args+=['-i',file]
    filters=[]
    for i in range(len(music)):filters.append(f'[{i}:a]aresample=48000,aformat=channel_layouts=stereo,asetpts=PTS-STARTPTS[m{i}]')
    previous='m0'
    for i in range(1,len(music)):
        label='x'+str(i);filters.append(f'[{previous}][m{i}]acrossfade=d=3:c1=tri:c2=tri[{label}]');previous=label
    filters.append(f'[{previous}]atrim=duration={seconds},asetpts=PTS-STARTPTS,loudnorm=I=-30:TP=-8:LRA=7,afade=t=in:d=1,afade=t=out:st={seconds-2}:d=2[music]')
    run(args+['-filter_complex',';'.join(filters),'-map','[music]','-ar','48000','-c:a','pcm_s16le',BATCH/'audio/music-bed.wav'])
    with wave.open(str(BATCH/'audio/music-bed.wav'),'rb') as w:
        if w.getnframes()/w.getframerate()<seconds-.05:raise ValueError('Selected music cannot cover exact take without looping')
    # Original, deterministic short physical cues; no outside samples or paid calls.
    n=round(seconds*48000); cue_audio=np.zeros(n,dtype=np.float32); cues=[];rng=np.random.default_rng(1311)
    kinds={'budget_before','budget_after','daily','dinner','audit','recurring','annual','calendar','buffer','choice','automate','review','cta'}
    for s in p['segments']:
        if s['kind'] not in kinds:continue
        at=(s['from']+s['cueFrame'])/FPS; start=round(at*48000);t=np.arange(12000)/48000
        if s['kind'] in {'audit','annual','review'}:
            wavelet=rng.normal(0,1,len(t)).astype(np.float32)*np.sin(np.pi*np.minimum(t/.25,1))**2*.006
            role='short paper movement at inspection / calendar / review cue'
        elif s['kind'] in {'recurring','automate','calendar','cta'}:
            wavelet=(np.sin(2*np.pi*700*t)+.3*np.sin(2*np.pi*1050*t))*np.exp(-t*40)*.024
            role='soft button / date selection cue'
        else:
            wavelet=(np.sin(2*np.pi*1050*t)+.4*np.sin(2*np.pi*1550*t))*np.exp(-t*28)*.017
            role='light coin or receipt landing emphasizes modeled arithmetic'
        end=min(n,start+len(t));cue_audio[start:end]+=wavelet[:end-start]
        cues.append({'beat':s['id'],'at':at,'role':role,'source':'original deterministic local synthesis'})
    f32=BATCH/'audio/cues.f32';cue_audio.tofile(f32)
    run([FF,'-y','-v','error','-f','f32le','-ar','48000','-ac','1','-i',f32,'-c:a','pcm_s16le',BATCH/'audio/cues.wav'])
    f32.unlink()
    final=BATCH/'audio/final-mix.wav'
    if final.exists():raise ValueError('Mix already frozen; use new mix revision')
    run([FF,'-y','-v','error','-i',voicefile,'-i',BATCH/'audio/music-bed.wav','-i',BATCH/'audio/cues.wav',
        '-filter_complex','[0:a]asplit=2[v][sc];[1:a][sc]sidechaincompress=threshold=0.025:ratio=5:attack=15:release=260[duck];[v][duck][2:a]amix=inputs=3:normalize=0,alimiter=limit=0.89:level=false[mix]',
        '-map','[mix]','-t',seconds,'-ar','48000','-ac','2','-c:a','pcm_s16le',final])
    save(BATCH/'audio/mix-receipt.json',{'narrationSHA256':sha(BATCH/'audio/narration.wav'),'mixSHA256':sha(final),
        'music':provenance,'crossfadeSeconds':3,'newMusicProviderCalls':0,'speechSpeed':1,'sharedAcrossStyles':True,'cues':cues,
        'listening':'Measurement and frame inspection do not establish continuous listening'})
    print('MIX_READY',seconds,flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('phase',choices=['prepare','voice','timeline','mix']);args=parser.parse_args()
    globals()[args.phase]()
