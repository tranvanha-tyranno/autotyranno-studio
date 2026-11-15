"""Paced finance revision: retain exact main audio, add a requested subscribe outro.

Only voice-outro calls a provider, once through the retained intent/cache helper.
All visual work uses new scene implementations and a batch-isolated timeline.
"""
from pathlib import Path
import argparse,copy,math,shutil,time,wave,hashlib
import numpy as np
import eleven_audio
from finance_long import ROOT,PROJECT,VOICE,FPS,FF,save,load,sha,run

BATCH=ROOT/'videos/2026-11-13-hai-style-nhip-nhanh'
PREVIOUS=ROOT/'videos/2026-11-13-hai-style-10-phut'
OUTRO='Nếu thấy video hữu ích, hãy đăng ký kênh và bật chuông để đón xem những nội dung tiếp theo. Bạn muốn xem lại khoản chi nào trong tháng này? Hãy để lại bình luận nhé.'

def voice_outro():
    BATCH.mkdir(exist_ok=True);target=BATCH/'audio/subscribe.mp3'
    payload={'text':OUTRO,'model_id':'eleven_v3','language_code':'vi','voice_settings':{'stability':.5,'similarity_boost':.8,'speed':1.0}}
    endpoint=f'/v1/text-to-speech/{VOICE}/with-timestamps'
    digest=hashlib.sha256(__import__('json').dumps({'endpoint':endpoint,'body':payload},sort_keys=True,ensure_ascii=False).encode()).hexdigest()
    cached=target.exists() or all((eleven_audio.CACHE/(digest+s)).exists()for s in ['.mp3','.json','.alignment.json'])
    save(BATCH/'generation-plan.json',{'newSpeech':[{'file':'audio/subscribe.mp3','endpoint':endpoint,'payload':payload}],
        'mainNarration':'Reuse exact previous approved-voice takes; no repeated body synthesis','newImageVideoMusicSFXCalls':0})
    began=time.perf_counter();eleven_audio.generate(target,endpoint,payload,timed=True)
    receipt=load(target.with_suffix('.receipt.json'));report=BATCH/'audio/outro-generation.json'
    if not report.exists():save(report,{'cacheHit':cached,'wallSeconds':time.perf_counter()-began,'sha256':sha(target),
        'voice':VOICE,'speed':1,'providerCharacterCost':receipt.get('character_cost'),'newRequestCredits':0 if cached else receipt.get('character_cost'),
        'scope':'Only requested subscribe outro is newly synthesized; provider header is not a USD invoice'})
    prepare()

def prepare():
    from finance_pace_plan import build_shots,audit_shots
    BATCH.mkdir(exist_ok=True);(BATCH/'audio').mkdir(exist_ok=True)
    old=load(PREVIOUS/'plan.json');plan=copy.deepcopy(old)
    body=PREVIOUS/'audio/final-mix.wav';old_receipt=load(PREVIOUS/'audio/mix-receipt.json')
    if sha(body)!=old_receipt['mixSHA256']:raise ValueError('Retained main mix changed')
    audio=BATCH/'audio/subscribe.mp3';alignment=load(audio.with_suffix('.alignment.json'))
    if ''.join(alignment['characters'])!=OUTRO:raise ValueError('Outro alignment is not exact text')
    if sha(audio)!=load(audio.with_suffix('.receipt.json'))['sha256']:raise ValueError('Outro bytes changed')
    # Preserve the complete old PCM body. Append, never time-stretch or truncate it.
    with wave.open(str(body),'rb') as w:
        assert w.getnchannels()==2 and w.getframerate()==48000 and w.getsampwidth()==2
        bodybytes=w.readframes(w.getnframes());body_samples=len(bodybytes)//4
    offset=body_samples/48000
    normalized=BATCH/'audio/subscribe-normalized.wav'
    run([FF,'-y','-v','error','-i',audio,'-af','loudnorm=I=-16:TP=-2:LRA=11','-ar','48000','-ac','2','-c:a','pcm_s16le',normalized])
    with wave.open(str(normalized),'rb') as w:voice=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').reshape(-1,2).astype(np.float32)/32768
    seconds=len(voice)/48000+.9;tail_frames=math.ceil(seconds*FPS);tail_n=tail_frames*1600
    tail=np.zeros((tail_n,2),dtype=np.float32);tail[:len(voice)]=voice
    music=PREVIOUS/'audio/music/hopeful-outro.mp3';receipt=load(music.with_suffix('.receipt.json'))
    if sha(music)!=receipt['sha256']:raise ValueError('Outro music hash changed')
    raw=run([FF,'-v','error','-ss','30','-i',music,'-t',tail_n/48000,'-ar','48000','-ac','2','-f','f32le','-']).stdout
    bed=np.frombuffer(raw,dtype='<f4').reshape(-1,2).copy()
    if len(bed)<tail_n:raise ValueError('Retained outro music excerpt too short')
    bed=bed[:tail_n];bed*=.006/max(float(np.sqrt(np.mean(bed**2))),1e-7)
    fade=np.minimum(np.arange(tail_n)/48000/.6,1)*np.minimum((tail_n-1-np.arange(tail_n))/48000/1.1,1)
    tail+=bed*fade[:,None]
    # Tiny original confirmation cue when the subscribe action begins.
    ws=eleven_audio.words(alignment);subscribe=next((w['start'] for w in ws if w['text'].casefold()=='đăng'),1.2)
    bell=next((w['start'] for w in ws if w['text'].casefold()=='chuông'),3.)
    for at,freq in [(subscribe,720),(bell,1050)]:
        start=round(at*48000);t=np.arange(9600)/48000;cue=np.sin(2*np.pi*freq*t)*np.exp(-30*t)*.02
        end=min(tail_n,start+len(t));tail[start:end]+=cue[:end-start,None]
    tail=np.clip(tail,-.89,.89);tailbytes=(tail*32767).astype('<i2').tobytes()
    final=BATCH/'audio/final-mix.wav'
    if final.exists():
        with wave.open(str(final),'rb') as w:existing=w.readframes(w.getnframes())
        if existing!=bodybytes+tailbytes:raise ValueError('Prepared final mix already frozen with different bytes')
    else:
        with wave.open(str(final),'wb') as w:w.setparams((2,2,48000,0,'NONE','not compressed'));w.writeframes(bodybytes+tailbytes)
    start=old['durationFrames'];duration=tail_frames
    segment={'id':'subscribe','kind':'subscribe','from':start,'duration':duration,'speechStart':start,
        'speechEnd':math.ceil((offset+ws[-1]['end'])*FPS),'text':OUTRO,'headline':'ĐĂNG KÝ KÊNH','cue':'đăng ký kênh',
        'cueFrame':round(subscribe*FPS),'data':{'action':'subscribe_bell_comment'},'chapterId':'dang-ky','chapterTitle':'Hẹn gặp ở video tiếp theo','chapterIndex':11}
    plan['segments'].append(segment);plan['durationFrames']=start+duration
    plan['words'].extend([{**w,'start':w['start']+offset,'end':w['end']+offset}for w in ws])
    plan['chapters'].append({'id':'dang-ky','title':'Đăng ký và để lại bình luận','from':start,'seconds':duration/FPS})
    for i in range(0,len(ws),9):
        group=ws[i:i+9];plan['captions'].append({'from':round((offset+group[0]['start'])*FPS),'end':math.ceil((offset+group[-1]['end'])*FPS),'text':' '.join(w['text']for w in group)})
    plan['shots']=build_shots(plan);summary=audit_shots(plan,plan['shots'])
    plan['revisionPurpose']='Faster evolving actions and phrase-aligned cuts; subscribe outro explicitly requested'
    target=BATCH/'plan.json'
    if target.exists() and load(target)!=plan:raise ValueError('Paced plan is frozen; use another batch for timing changes')
    save(target,plan);save(BATCH/'pacing-report.json',summary)
    shutil.copy2(PREVIOUS/'sources.json',BATCH/'sources.json')
    (BATCH/'script.txt').write_text((PREVIOUS/'script.txt').read_text(encoding='utf-8')+'\n\n'+OUTRO,encoding='utf-8')
    save(BATCH/'audio/mix-receipt.json',{'mainMixSource':str(body.relative_to(ROOT)),'mainMixSHA256':sha(body),
        'mainPCMBytesPreserved':len(bodybytes),'mainPrefixSHA256':hashlib.sha256(bodybytes).hexdigest(),'finalMixSHA256':sha(final),
        'mainSpeechSpeed':1,'outroSpeechSpeed':1,'outroNarrationSHA256':sha(audio),
        'outroMusic':{'file':str(music.relative_to(ROOT)),'sha256':sha(music),'sourceStartSeconds':30,'seconds':tail_n/48000},
        'newMusicCalls':0,'newVisualCalls':0,'bodyTimingUnchanged':True,'sharedAcrossStyles':True})
    save(BATCH/'brief.json',{'requestedChange':'Motion and cuts faster, upgrade both styles, add subscribe/bell/comment outro',
        'previousBatch':str(PREVIOUS.relative_to(ROOT)),'previousUserStatus':'rejected-slide-style','newVisualSources':['finance-pace-comic','finance-pace-flow'],
        'noPersistentSlideHeader':True,'targetShotSeconds':[2.2,4.4],'transitionFrames':8,
        'voice':'Nhật Phong','inventedChannelBranding':False,'userApproval':'pending'})
    print('PACE_PREPARED',plan['durationFrames'],'frames',len(plan['shots']),'shots',flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('phase',choices=['voice-outro','prepare']);args=parser.parse_args()
    {'voice-outro':voice_outro,'prepare':prepare}[args.phase]()
