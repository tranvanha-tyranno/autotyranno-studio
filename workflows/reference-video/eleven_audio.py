"""Cached ElevenLabs timed speech and sound effects; credentials never enter receipts."""
import base64, hashlib, importlib.util, json, shutil, unicodedata
from pathlib import Path
import requests

PROJECT=Path(__file__).resolve().parents[2]
CACHE=PROJECT/'.cache/eleven-editorial'

def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
def key():
    spec=importlib.util.spec_from_file_location('product_runner',Path(__file__).parents[1]/'product-video/run.py')
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    return mod.eleven_key()

def generate(target,endpoint,payload,timed=False):
    target=Path(target);target.parent.mkdir(parents=True,exist_ok=True);CACHE.mkdir(parents=True,exist_ok=True)
    digest=hashlib.sha256(json.dumps({'endpoint':endpoint,'body':payload},sort_keys=True,ensure_ascii=False).encode()).hexdigest()
    receipt=target.with_suffix('.receipt.json');alignment=target.with_suffix('.alignment.json');intent=target.with_suffix('.intent.json')
    cached=CACHE/(digest+'.mp3');cm=CACHE/(digest+'.json');ca=CACHE/(digest+'.alignment.json')
    if target.exists():
        if receipt.exists() and json.loads(receipt.read_text())['request_hash']==digest and (not timed or alignment.exists()):return target
        raise ValueError('Existing audio does not match request or lacks receipt; use a new revision')
    if cached.exists() and cm.exists() and (not timed or ca.exists()):
        shutil.copy2(cached,target);shutil.copy2(cm,receipt)
        if timed:shutil.copy2(ca,alignment)
        return target
    if intent.exists():raise RuntimeError('Unresolved prior provider call. Reconcile before retrying '+str(intent))
    secret=key();save(intent,{'request_hash':digest,'endpoint':endpoint,'payload':payload})
    try:r=requests.post('https://api.elevenlabs.io'+endpoint,params={'output_format':'mp3_44100_128'},headers={'xi-api-key':secret,'Content-Type':'application/json'},json=payload,timeout=180)
    except requests.RequestException:raise RuntimeError('Provider transport failed; intent retained to prevent duplicate billing') from None
    if r.status_code!=200:
        try:
            detail=r.json().get('detail',{});detail=detail if isinstance(detail,dict) else {}
        except ValueError:detail={}
        err={'http_status':r.status_code,'type':detail.get('type'),'code':detail.get('code')};save(target.with_suffix('.error.json'),err)
        raise RuntimeError('ElevenLabs request rejected: '+json.dumps(err))
    if timed:
        data=r.json();audio=base64.b64decode(data['audio_base64']);a=data.get('alignment') or data.get('normalized_alignment')
        if not a:raise ValueError('Speech returned without timing; intent retained')
        save(alignment,a);shutil.copy2(alignment,ca)
    else:
        if not r.headers.get('content-type','').startswith('audio/'):raise ValueError('Expected sound audio')
        audio=r.content
    target.with_suffix('.partial').write_bytes(audio);target.with_suffix('.partial').replace(target)
    meta={'provider':'ElevenLabs','model':payload.get('model_id'),'request_hash':digest,'endpoint':endpoint,'character_cost':r.headers.get('character-cost'),'request_id':r.headers.get('request-id'),'sha256':hashlib.sha256(audio).hexdigest(),'bytes':len(audio)}
    save(receipt,meta);shutil.copy2(target,cached);shutil.copy2(receipt,cm);intent.unlink()
    print('AUDIO_OK',target.name,len(audio),'cost',meta['character_cost'],flush=True);return target

def speech(target,text,voice_id,model='eleven_v3',speed=1.0):
    return generate(target,f'/v1/text-to-speech/{voice_id}/with-timestamps',{'text':text,'model_id':model,'language_code':'vi','voice_settings':{'stability':.5,'similarity_boost':.8,'speed':speed}},True)

def sound(target,prompt,seconds):
    return generate(target,'/v1/sound-generation',{'text':prompt,'duration_seconds':seconds,'prompt_influence':.5,'model_id':'eleven_text_to_sound_v3','loop':False})

def words(alignment):
    chars=alignment['characters'];starts=alignment['character_start_times_seconds'];ends=alignment['character_end_times_seconds'];rows=[];part=[]
    for c,s,e in zip(chars,starts,ends):
        if c.isspace():
            if part:rows.append({'text':''.join(x[0] for x in part),'start':part[0][1],'end':part[-1][2]});part=[]
        else:part.append((c,s,e))
    if part:rows.append({'text':''.join(x[0] for x in part),'start':part[0][1],'end':part[-1][2]})
    return rows
