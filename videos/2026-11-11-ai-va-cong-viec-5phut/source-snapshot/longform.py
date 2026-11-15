"""Manifest-driven long-form voice, timing and sound preparation.

Keep the approved 50s composition/media intact. New assets live under public/longform.
"""
from pathlib import Path
import argparse,json,re,shutil,unicodedata
from documentary import FF,run,duration
from eleven_audio import generate,words

ROOT=Path(__file__).resolve().parents[2]
PROJECT=Path(__file__).parent/'cinematic'
PUB=PROJECT/'public/longform'
DEFAULT=ROOT/'videos/2026-11-11-ai-va-cong-viec-5phut'

def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def norm(s):return re.sub(r'[^\w]','',unicodedata.normalize('NFC',s).lower())

def plan(b):
    d=load(b/'content.json');preset=load(Path(__file__).parent/'cinematic.profile.json')['audio']['voicePreset']
    voice={'endpoint':f"/v1/text-to-speech/{preset['voice_id']}/with-timestamps",'payload':{'text':'\n\n'.join(c['text'] for c in d['chapters']),'model_id':preset['model_id'],'language_code':'vi','voice_settings':preset['voice_settings']}}
    music=[]
    for name,desc in [('analysis','precise analytical forward motion, gentle marimba-like glass figures, warm analog bass, tight restrained percussion, gradually open the arrangement across two minutes'),('agency','more hopeful human agency, warm piano over subtle arpeggios, restrained bass and brushed electronic percussion, build gently then resolve without an epic climax')]:
        music.append({'file':f'{name}-score.mp3','endpoint':'/v1/music','payload':{'prompt':f'Instrumental score for an intelligent Vietnamese 3D motion design explainer about AI and work. Cohesive premium editorial design-film sound, 112 BPM. {desc}. Plenty of space for narration. No vocals, spoken words, choir, alarms, braams, big risers or aggressive EDM. Musical development, not a repeating four-bar loop. 120 seconds.','music_length_ms':120000,'force_instrumental':True,'model_id':'music_v1'}})
    effects=[{'file':'typing.mp3','endpoint':'/v1/sound-generation','payload':{'text':'Close detailed soft modern computer keyboard typing in a quiet workspace. A few deliberate bursts, tactile and warm. Dry recording, no voices, music, notification tones or ambience wash.','duration_seconds':4,'prompt_influence':.5,'model_id':'eleven_text_to_sound_v3','loop':False}}, {'file':'paper.mp3','endpoint':'/v1/sound-generation','payload':{'text':'One gentle page turn followed by a document laid on a desk, close dry studio foley. Subtle realistic paper detail, no music, voice or cinematic whoosh.','duration_seconds':3,'prompt_influence':.5,'model_id':'eleven_text_to_sound_v3','loop':False}}, {'file':'confirm.mp3','endpoint':'/v1/sound-generation','payload':{'text':'One soft tactile wooden click with a very short warm muted tonal tail. A refined confirmation for an editorial motion graphic. Quiet, understated, dry; no alert, chime cascade, music or voice.','duration_seconds':1,'prompt_influence':.5,'model_id':'eleven_text_to_sound_v3','loop':False}}]
    b.mkdir(exist_ok=True,parents=True);(b/'audio').mkdir(exist_ok=True);PUB.mkdir(exist_ok=True,parents=True)
    save(b/'generation-plan.json',{'voice':voice,'music':music,'effects':effects,'reuseApprovedMusic':'videos/2026-11-11-cinematic-reset/audio/motion-score.mp3','limits':{'newVoiceTakes':1,'newMusicTracks':2,'newEffects':3},'style':'approved cinematic.profile.json','credentials':'Read at call time from encrypted vault; excluded from this file'})

def audio(b,kind):
    p=load(b/'generation-plan.json')
    if kind=='voice':
        a=p['voice'];generate(b/'audio/narration-original.mp3',a['endpoint'],a['payload'],True)
    else:
        for a in p[kind]:generate(b/'audio'/a['file'],a['endpoint'],a['payload'])

def prepare(b):
    d=load(b/'content.json');a=b/'audio/narration-original.mp3';target=d['targetSeconds'];natural=duration(a);factor=natural/(target-2)
    if not .85<=factor<=1.18:raise ValueError(f'Rewrite narration, do not stretch this take: natural {natural}s; tempo {factor}')
    run([FF,'-y','-v','error','-i',str(a),'-af',f'atempo={factor:.10f},apad=whole_dur={target}','-t',str(target),'-ar','48000',str(b/'narration.wav')])
    w=words(load(a.with_suffix('.alignment.json')))
    for x in w:x['start']/=factor;x['end']/=factor
    tokens=[norm(x['text']) for x in w]
    def find(phrase,lo=0):
        q=[norm(x) for x in phrase.split()]
        for i in range(lo,len(tokens)-len(q)+1):
            if tokens[i:i+len(q)]==q:return i
        raise ValueError('Missing actual-take phrase '+phrase)
    chapters=[];cursor=0
    for i,c in enumerate(d['chapters']):
        ix=find(' '.join(c['text'].split()[:7]),cursor);cursor=ix+1
        row={**c,'start':0 if i==0 else round(w[ix]['start']*30),'beats':[]}
        for beat in c['beats']:
            j=find(beat['phrase'],ix);row['beats'].append({**beat,'at':max(0,round(w[j]['start']*30)-row['start'])})
        chapters.append(row)
    for i,c in enumerate(chapters):c['end']=chapters[i+1]['start'] if i<len(chapters)-1 else target*30
    caps=[];part=[]
    for x in w:
        part.append(x)
        if len(part)>=9 or len(' '.join(a['text'] for a in part))>48 or re.search(r'[.!?:]$',x['text']):
            caps.append({'start':part[0]['start'],'end':part[-1]['end'],'text':' '.join(a['text'] for a in part)});part=[]
    if part:caps.append({'start':part[0]['start'],'end':part[-1]['end'],'text':' '.join(a['text'] for a in part)})
    timeline={'title':d['title'],'seconds':target,'fps':30,'frames':target*30,'naturalVoiceSeconds':natural,'tempo':factor,'lastWordEnd':w[-1]['end'],'captions':caps,'chapters':chapters}
    save(b/'aligned-words.json',w);save(b/'timeline.json',timeline);save(PUB/'data.json',timeline)
    print('VOICE',natural,'TEMPO',factor,'LAST',w[-1]['end'],'CHAPTERS',len(chapters),flush=True)

def mix(b):
    t=load(b/'timeline.json');seconds=t['seconds'];a=b/'audio';approved=ROOT/'videos/2026-11-11-cinematic-reset/audio/motion-score.mp3'
    # 40 + 120 + 120 + 30 - 3*3.333333 = 300 seconds. Real musical
    # development in two new movements, framed by the approved theme.
    run([FF,'-y','-v','error','-i',str(approved),'-i',str(a/'analysis-score.mp3'),'-i',str(a/'agency-score.mp3'),'-i',str(approved),'-filter_complex',
        '[0:a]atrim=start=0:end=40,asetpts=PTS-STARTPTS[h1];[3:a]atrim=start=10:end=40,asetpts=PTS-STARTPTS[t1];[1:a]atrim=start=0:end=120,asetpts=PTS-STARTPTS[a1];[2:a]atrim=start=0:end=120,asetpts=PTS-STARTPTS[a2];[h1][a1]acrossfade=d=3.333333:c1=qsin:c2=qsin[x];[x][a2]acrossfade=d=3.333333:c1=qsin:c2=qsin[y];[y][t1]acrossfade=d=3.333333:c1=qsin:c2=qsin[out]',
        '-map','[out]','-t',str(seconds),str(a/'score-assembled.wav')])
    if abs(duration(a/'score-assembled.wav')-seconds)>.1:raise ValueError('Music assembly did not cover the requested full duration')
    cues=[]
    byid={c['id']:c for c in t['chapters']}
    for file,id,offset in [('typing.mp3','example',.8),('paper.mp3','hallucination',.8),('confirm.mp3','review',1.0),('typing.mp3','experiment',1.2),('paper.mp3','portfolio',1.0),('confirm.mp3','closing',2.0)]:
        cues.append({'file':file,'time':byid[id]['start']/30+offset,'chapter':id})
    inputs=[FF,'-y','-v','error','-i',str(b/'narration.wav'),'-i',str(a/'score-assembled.wav')]
    graph=['[0:a]highpass=f=70,loudnorm=I=-16:TP=-2:LRA=8,asplit=2[v][key]',f'[1:a]loudnorm=I=-27:TP=-7:LRA=8,afade=t=in:d=0.6,afade=t=out:st={seconds-3}:d=3[m]','[m][key]sidechaincompress=threshold=0.025:ratio=3:attack=18:release=260:makeup=1[duck]']
    labels=['[v]','[duck]']
    for i,c in enumerate(cues):
        inputs+=['-i',str(a/c['file'])];length=duration(a/c['file']);delay=round(c['time']*1000)
        graph.append(f'[{i+2}:a]highpass=f=100,loudnorm=I=-31:TP=-9:LRA=5,afade=t=in:d=0.06,afade=t=out:st={max(.1,length-.25):.4f}:d=0.25,adelay={delay}|{delay}[fx{i}]');labels.append(f'[fx{i}]')
    graph.append(''.join(labels)+f'amix=inputs={len(labels)}:duration=longest:normalize=0,alimiter=limit=0.89:level=false,apad=whole_dur={seconds}[out]')
    target=a/'final-mix.wav';run(inputs+['-filter_complex',';'.join(graph),'-map','[out]','-t',str(seconds),'-ar','48000','-ac','2',str(target)])
    shutil.copy2(target,PUB/'mix.wav');save(b/'sound-cues.json',cues)
    r=run([FF,'-hide_banner','-i',str(target),'-af','loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json','-f','null','-']);s=r.stderr.decode('utf-8',errors='replace');save(a/'mix-report.json',json.loads(re.findall(r'\{\s*"input_i".*?\}',s,re.S)[-1]));print('MIX READY',seconds,flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('action',choices=['plan','voice','music','effects','prepare','mix']);p.add_argument('--batch',type=Path,default=DEFAULT);a=p.parse_args()
    if a.action=='plan':plan(a.batch)
    elif a.action in ('voice','music','effects'):audio(a.batch,a.action)
    elif a.action=='prepare':prepare(a.batch)
    else:mix(a.batch)
