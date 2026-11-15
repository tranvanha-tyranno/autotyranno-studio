"""Source-pinned business explainers with exact chapter takes and mixed visual media."""
from __future__ import annotations
import argparse,hashlib,json,math,shutil,subprocess,sys,wave
from pathlib import Path
from PIL import Image,ImageOps
import production
from documentary import FF,duration
from eleven_audio import speech,words

ROOT=Path(__file__).resolve().parents[2]
LAYOUTS={'b-photo','b-paper','b-question','b-chart','b-split','b-coffee','b-closing'}
VOICE='6adFm46eyy74snVn6YrT'
load=production.load
save=production.save
sha=production.sha

def require(value,message):
    if not value:raise ValueError(message)

def visible_strings(value):
    if isinstance(value,str):yield value
    elif isinstance(value,list):
        for row in value:yield from visible_strings(row)
    elif isinstance(value,dict):
        for key,row in value.items():
            if key not in {'file','sourceURL','licenseURL','url','sha256','sourceHash'}:yield from visible_strings(row)

def validate(content):
    require(content.get('schema')=='business-explainer/1','Unsupported content schema')
    require(content.get('fps')==30,'Use30fps exact-take production')
    ids=[]
    for chapter in content['chapters']:
        require(chapter['text']==' '.join(b['text'] for b in chapter['beats']),'Chapter text must cover all beats')
        for beat in chapter['beats']:
            require(beat['layout'] in LAYOUTS,'Unknown business layout')
            require(beat.get('text','').strip(),'Empty narration beat')
            require(beat['phase'] in {'hook','disclaimer','content','cta'},'Invalid phase')
            ids.append(beat['id'])
    require(len(ids)==len(set(ids)),'Beat IDs must be unique')
    require(not any('tyranno' in s.casefold() for s in visible_strings({'title':content['title'],'chapters':content['chapters']})),
            'Forbidden visible/spoken branding in content')
    allbeats=[b for c in content['chapters'] for b in c['beats']]
    phases=[b['phase'] for i,b in enumerate(allbeats) if i==0 or b['phase']!=allbeats[i-1]['phase']]
    require(phases==['hook','disclaimer','content','cta'],'Require hook, disclaimer, main and CTA in order')
    ex=content['example'];unit=ex['price']-ex['variableUnit'];discount=ex['discountPrice']-ex['variableUnit']
    require(unit==20000 and discount==14000,'Example contribution changed; review script/graphics')
    require(ex['fixedMonthly']/unit==2400 and math.ceil(ex['fixedMonthly']/discount)==3429,'Break-even example mismatch')
    return {'beats':len(allbeats),'words':sum(len(c['text'].split()) for c in content['chapters']),
        'exampleChecks':{'unit':unit,'discountUnit':discount,'monthlyBaseUnits':2400,'monthlyDiscountUnitsCeil':3429,
                         'preserve60MillionUnitsCeil':math.ceil(60000000/discount),'cashShortfall':ex['cashOpening']+ex['cashReceipts']-ex['cashDue']}}

def voice(batch):
    batch=Path(batch).resolve();content=load(batch/'content.json');checks=validate(content)
    folder=batch/'audio';folder.mkdir(exist_ok=True)
    plan=[{'id':c['id'],'text':c['text'],'file':f'audio/{i+1:02}-{c["id"]}.mp3','voiceId':VOICE,
           'model':'eleven_v3','language':'vi','speed':1.0} for i,c in enumerate(content['chapters'])]
    save(folder/'voice-plan.json',{'chapterTakes':plan,'validation':checks,'policy':'Natural speech; cached exact takes, no time stretching. No channel branding.'})
    for row in plan:speech(batch/row['file'],row['text'],VOICE)
    return folder

def assemble(batch):
    batch=Path(batch).resolve();content=load(batch/'content.json');validate(content)
    audio=batch/'audio';offset=0.;aligned=[];chapters=[];inputs=[];filters=[];pieces=[]
    for i,c in enumerate(content['chapters']):
        source=audio/f'{i+1:02}-{c["id"]}.mp3';receipt=load(source.with_suffix('.receipt.json'))
        require(sha(source)==receipt['sha256'],'Chapter take differs from receipt')
        # Measured decoded samples determine concatenation boundaries, not estimated word rate.
        pcm=source.with_suffix('.wav')
        subprocess.run([FF,'-y','-v','error','-i',str(source),'-ar','48000','-ac','2',str(pcm)],check=True)
        with wave.open(str(pcm),'rb') as w:n=w.getnframes();secs=n/w.getframerate()
        wrows=words(load(source.with_suffix('.alignment.json')))
        require(production.normalized_words(c['text'])==[production.normalized_words(w['text'])[0] for w in wrows],
                'Provider words differ from authored chapter: '+c['id'])
        require(wrows[-1]['end']<=secs+.10,'Timing extends past decoded take')
        chapter={'id':c['id'],'title':c['title'],'startSeconds':offset,'voiceSeconds':secs,
                 'source':source.relative_to(batch).as_posix(),'sha256':sha(source)}
        chapters.append(chapter)
        aligned.extend({**w,'start':w['start']+offset,'end':w['end']+offset,'chapter':c['id']} for w in wrows)
        pieces.append(pcm);offset+=secs
        if i+1<len(content['chapters']):
            silence=audio/f'gap-{i:02}.wav'
            with wave.open(str(silence),'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(48000);w.writeframes(bytes(48000*4//2))
            pieces.append(silence);offset+=.5
    narration=audio/'narration.wav'
    with wave.open(str(narration),'wb') as target:
        target.setnchannels(2);target.setsampwidth(2);target.setframerate(48000)
        for piece in pieces:
            with wave.open(str(piece),'rb') as source:
                while True:
                    chunk=source.readframes(48000)
                    if not chunk:break
                    target.writeframes(chunk)
    require(540<=offset<=690,f'Natural take {offset:.2f}s outside approximate10-minute range; revise writing, not tempo')
    save(batch/'aligned-words.json',aligned)
    save(batch/'chapter-timing.json',chapters)
    save(audio/'narration.receipt.json',{'sha256':sha(narration),'seconds':offset,'speed':1.0,'chapters':chapters,
         'lastWordEnd':aligned[-1]['end'],'tailSeconds':1.5,'manualListening':'Not established by assembly'})
    print('ASSEMBLED',round(offset,3),'seconds,',len(aligned),'words',flush=True)
    return narration

def validate_media_intervals(data):
    intervals={}
    for shot in data['shots']:
        count=len(shot['images']);length=shot['end']-shot['start']
        if shot['layout'] in {'b-photo','b-closing'}:
            require(count>0,'Photographic scene needs actual media: '+shot['id'])
            cues=shot.get('design',{}).get('cues',[])
            starts=[0]+[cues[i-1] if len(cues)>=i else round(length*i/count) for i in range(1,count)]
            require(all(a<b for a,b in zip(starts,starts[1:])),'Photo cuts must be strictly increasing')
            used=shot['images'];ends=starts[1:]+[length]
        elif shot['layout']=='b-split':
            used=shot['images'][:min(3,max(2,len(shot.get('design',{}).get('choices',[]))))];starts=[0]*len(used);ends=[length]*len(used)
        elif shot['layout']=='b-chart':used=[];starts=[];ends=[]
        else:used=shot['images'][:1];starts=[0]*len(used);ends=[length]*len(used)
        for image,start,end in zip(used,starts,ends):
            if image.get('mediaType')!='video':continue
            lo=image.get('trimBeforeFrames',0);hi=lo+end-start
            require(hi<=image['availableFrames'],'Clip would freeze/loop before scene ends: '+shot['id'])
            old=intervals.setdefault(image['file'],[])
            require(all(hi<=a or lo>=b for a,b,_ in old),'Repeated source clip interval: '+shot['id'])
            old.append((lo,hi,shot['id']))
    return {'movingMediaSeconds':sum(b-a for rows in intervals.values() for a,b,_ in rows)/data['fps'],
            'clips':len(intervals),'intervals':intervals,'scope':'Playback bounds and non-overlapping trims only, not semantic/aesthetic approval.'}

def prepare(batch):
    batch=Path(batch).resolve();content=load(batch/'content.json');validation=validate(content)
    aligned=load(batch/'aligned-words.json');receipt=load(batch/'audio/narration.receipt.json')
    require(sha(batch/'audio/narration.wav')==receipt['sha256'],'Narration source changed')
    catalog=load(batch/'sources-candidates.json');catalog=catalog['assets'] if isinstance(catalog,dict) else catalog
    catalog={a['id']:a for a in catalog}
    assignments=load(batch/'visual-plan.json');assignments=assignments.get('shots',assignments)
    assignments={a['id']:a for a in assignments} if isinstance(assignments,list) else assignments
    fps=30;frames=math.ceil((receipt['seconds']+1.5)*fps)
    public=batch/'production-public/business';public.mkdir(parents=True,exist_ok=True)
    rendered={};sources=[];cursor=0;shots=[]
    for c in content['chapters']:
        for beat in c['beats']:
            visual=assignments[beat['id']];images=[]
            for raw_id in visual['images']:
                if isinstance(raw_id,str):aid=raw_id;override={}
                else:aid=raw_id['id'];override={k:v for k,v in raw_id.items() if k!='id'}
                key=aid+('-'+hashlib.sha256(json.dumps(override,sort_keys=True).encode()).hexdigest()[:8] if override else '')
                a=catalog[aid];source=batch/a['file'];digest=a.get('sha256')
                require(source.is_file() and sha(source)==digest,'Source differs/missing: '+aid)
                require(a.get('license') or a.get('source',{}).get('license'),'Asset needs license receipt: '+aid)
                if key not in rendered:
                    video=a.get('mediaType')=='video' or source.suffix.lower()=='.mp4'
                    target=public/(key+('.mp4' if video else '.jpg'))
                    if video:
                        if not target.exists():shutil.copy2(source,target)
                        import cv2
                        cap=cv2.VideoCapture(str(source));n=int(cap.get(cv2.CAP_PROP_FRAME_COUNT));rate=cap.get(cv2.CAP_PROP_FPS)
                        w,h=cap.get(cv2.CAP_PROP_FRAME_WIDTH),cap.get(cv2.CAP_PROP_FRAME_HEIGHT);cap.release()
                        record={'file':'business/'+target.name,'aspect':w/h,'mediaType':'video','trimBeforeFrames':0,
                                'availableFrames':math.floor(n/rate*30),'credit':a.get('creator','')}
                    else:
                        with Image.open(source) as im:
                            im=ImageOps.exif_transpose(im).convert('RGB');crop=override.get('crop',a.get('crop',[0,0,1,1]))
                            require(len(crop)==4 and all(0<=x<=1 for x in crop) and crop[0]<crop[2] and crop[1]<crop[3],'Invalid crop')
                            if crop!=[0,0,1,1]:im=im.crop(tuple(round(v*x) for v,x in zip(crop,[im.width,im.height,im.width,im.height])))
                            im.thumbnail((1920,1280),Image.Resampling.LANCZOS);im.save(target,quality=91)
                            record={'file':'business/'+target.name,'aspect':im.width/im.height,'credit':a.get('creator','')}
                    record['focus']=override.get('focus',a.get('recommendedFocus',[50,50]));record['fit']=override.get('fit',a.get('recommendedFit','cover'))
                    rendered[key]=record;sources.append({'id':key,'source':a,'sourceSHA256':digest,'publicFile':record['file'],'publicSHA256':sha(target),'override':override})
                images.append({**rendered[key],**{k:v for k,v in override.items() if k not in {'crop','fit','focus'}}})
            count=len(production.normalized_words(beat['text']));tokens=[production.normalized_words(w['text'])[0] for w in aligned[cursor:cursor+count]]
            require(tokens==production.normalized_words(beat['text']),'Beat words mismatch: '+beat['id'])
            start=0 if not shots else round(aligned[cursor]['start']*fps)
            design={**beat.get('design',{}),**visual.get('design',{})}
            # Cue phrases refer to the finalized exact chapter take.
            if visual.get('cuePhrases'):
                cues=[];local=aligned[cursor:cursor+count];localtokens=tokens
                for phrase in visual['cuePhrases']:
                    q=production.normalized_words(phrase);matches=[i for i in range(len(localtokens)-len(q)+1) if localtokens[i:i+len(q)]==q]
                    require(len(matches)==1,'Cue phrase missing/ambiguous in '+beat['id']+':'+phrase)
                    cues.append(round(local[matches[0]]['start']*fps)-start)
                design['cues']=cues
            shot={**beat,'start':start,'images':images,'design':design,'chapter':c['id'],
                  'sourceNote':visual.get('sourceNote',''),'needToSee':visual.get('needToSee','')}
            shots.append(shot);cursor+=count
    require(cursor==len(aligned),'Narration coverage incomplete')
    for i,s in enumerate(shots):
        s['end']=shots[i+1]['start'] if i+1<len(shots) else frames
        require(s['end']>s['start'],'Nonpositive beat duration')
        for cue in s['design'].get('cues',[]):require(0<=cue<s['end']-s['start'],'Cue outside shot '+s['id'])
        if s['layout'] in {'b-photo','b-closing'}:
            cues=s['design'].get('cues',[]);slots=[0]+cues if cues else [round(j*(s['end']-s['start'])/len(s['images'])) for j in range(len(s['images']))]
            for j,image in enumerate(s['images']):
                if image.get('mediaType')=='video':
                    slotEnd=slots[j+1] if j+1<len(slots) else s['end']-s['start']
                    require(slotEnd-slots[j]<=image['availableFrames']-image.get('trimBeforeFrames',0),'Clip interval too short: '+s['id'])
    data={'title':content['title'],'fps':fps,'frames':frames,'audio':'business/mix.wav','shots':shots,'captions':production.captions(aligned)}
    media_check=validate_media_intervals(data)
    require(not any('tyranno' in s.casefold() for s in visible_strings(data)),'Forbidden branding in render props')
    save(batch/'data.json',data);save(batch/'props.json',{'data':data});save(public/'data.json',data)
    save(batch/'source-receipts.json',sources)
    save(batch/'media-interval-check.json',media_check)
    save(batch/'preflight.json',{'schema':'business-preflight/1','validation':validation,'frames':frames,'seconds':frames/fps,
        'shots':len(shots),'lastWordEnd':aligned[-1]['end'],'speed':1.0,'chapterTakes':len(content['chapters']),
        'layouts':{x:sum(s['end']-s['start'] for s in shots if s['layout']==x)/fps for x in sorted(LAYOUTS)},
        'brandingGate':'No forbidden text in visible render props or spoken script','userAcceptance':'pending','audioListening':'not claimed'})
    print('PREPARED',frames,'frames',len(shots),'beats',flush=True)
    return data

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('action',choices=['validate','voice','assemble','prepare']);parser.add_argument('--batch',type=Path,required=True);args=parser.parse_args()
    if args.action=='validate':print(json.dumps(validate(load(args.batch/'content.json')),ensure_ascii=False))
    else:globals()[args.action](args.batch)
