"""Two optional low-cost finance styles; one cached exact take, local vector visuals.

Run prepare, voice, then prepare again. Billable speech is only the explicit voice
command; a retained provider intent prevents duplicate requests after interruption.
"""
from pathlib import Path
import argparse, hashlib, json, math, shutil, subprocess, time
import numpy as np
import eleven_audio
from documentary import FF, duration

ROOT = Path(__file__).resolve().parents[2]
BATCH = ROOT / 'videos/2026-11-13-hai-style-tiet-kiem'
PROJECT = ROOT / 'workflows/reference-video/cinematic'
VOICE = '6adFm46eyy74snVn6YrT'
SEGMENTS = [
 ('hook', 'minh', 'Lương tăng hai triệu, mà tiền dư chẳng tăng. Minh vừa vui được một tháng, đã thấy ví mình trở về chỗ cũ.'),
 ('disclaimer', 'narrator', 'Đây là tình huống giả định để học cách lập ngân sách, không phải tư vấn tài chính cá nhân.'),
 ('before', 'lan', 'Lan hỏi: trước đây cậu chia tiền thế nào? Minh tính: lương mười hai triệu, chi mười triệu, còn hai triệu mỗi tháng.'),
 ('after', 'minh', 'Khi lương lên mười bốn triệu, Minh cũng chi tới mười hai triệu. Tiền dư vẫn chỉ hai triệu. Phần tăng thêm đã đi hết vào chi tiêu.'),
 ('daily', 'minh', 'Minh thắc mắc: mình có mua gì lớn đâu? Lan chỉ ra: nếu mỗi ngày chi thêm sáu mươi nghìn, trong ba mươi ngày đã là một triệu tám.'),
 ('dinner', 'lan', 'Thêm một bữa ăn hai trăm nghìn, tổng chi tăng đúng hai triệu. Mỗi lần thấy nhỏ, nhưng cộng lại vừa hết phần tăng lương.'),
 ('choice', 'narrator', 'Nếu vẫn giữ được mức chi mười triệu, phần dư có thể là bốn triệu. Nhưng chi phí thiết yếu tăng thì phải tính lại, đừng ép mình theo con số này.'),
 ('transfer', 'lan', 'Lan gợi ý: khi lương về, hãy dành trước một khoản phù hợp, sau khi tính tiền nhà, sinh hoạt và nghĩa vụ nợ. Có thể dùng chuyển khoản tự động để đỡ quên.'),
 ('cta', 'minh', 'Minh quyết định xem lại một khoản chi tăng gần đây. Bạn thử chọn một khoản của mình, cộng đủ cả tháng, rồi quyết định giữ hay giảm. Bắt đầu từ một khoản thôi.'),
]

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p, value):
    p=Path(p); p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')
def run(args):
    p=subprocess.run([str(x) for x in args],capture_output=True)
    if p.returncode: raise RuntimeError(p.stderr.decode('utf-8',errors='replace')[-3500:])
    return p
def prepare():
    BATCH.mkdir(parents=True,exist_ok=True)
    original=Path('C:/Users/tyranno/AppData/Local/Temp/codex-clipboard-7576be48-63cd-4540-96a9-7b51ea803c14.png')
    if original.exists() and not (BATCH/'reference/user-style-reference.png').exists():
        (BATCH/'reference').mkdir(exist_ok=True);shutil.copy2(original,BATCH/'reference/user-style-reference.png')
    script='\n\n'.join(x[2] for x in SEGMENTS)
    (BATCH/'script.txt').write_text(script,encoding='utf-8')
    save(BATCH/'editorial-brief.json',{'topic':'Lương tăng, vì sao tiền dư vẫn không tăng?',
      'audience':'Người đi làm muốn hiểu chi tiêu theo thu nhập', 'hook':'Tăng lương 2 triệu nhưng phần dư không tăng',
      'originalScript':True,'styles':['finance-cast','finance-minimal'],'comparison':'Same exact narration take and illustrative arithmetic',
      'sourceStudy':{'input':'User supplied single screenshot, not a video','observed':['Two expressive cartoon adults in a shared stage','Simple outline shapes','Financial/category icons','Dark grid background'],
      'adaptation':'Original cast and warm paper stage; interactions explain arithmetic; no copied characters, logo, frame or source audio',
      'limitations':'No claim about source animation, pacing, lip sync or audio can be made from the screenshot'},
      'costPolicy':{'newVideoImageMusicRequests':0,'speechTakes':1,'reuseVoiceAcrossStyles':True,'renderLocally':True},
      'acceptance':'Pending user feedback'})
    save(BATCH/'sources.json',{'facts':'All salaries, spending and daily arithmetic are fictional illustrative parameters, not Vietnam statistics.',
      'sources':[{'url':'https://www.consumerfinance.gov/an-essential-guide-to-building-an-emergency-fund/',
      'publisher':'Consumer Financial Protection Bureau','consulted':'2026-11-13','supports':'Automatic saving as an optional habit; savings amount depends on situation; manage cash flow',
      'use':'Original paraphrase in transfer segment; no source artwork copied'}]})
    audio=BATCH/'audio/narration.mp3'
    if not audio.exists(): return
    a=json.loads(audio.with_suffix('.alignment.json').read_text(encoding='utf-8'))
    chars=''.join(a['characters'])
    if chars != script: raise ValueError('Alignment character stream differs from exact script')
    offset=0; rows=[];fps=30
    words=eleven_audio.words(a)
    length=duration(audio)
    frames=math.ceil((length+.75)*fps)
    for i,(visual,speaker,text) in enumerate(SEGMENTS):
        start=offset;end=offset+len(text);offset=end+2
        onset=a['character_start_times_seconds'][start]
        speechEnd=a['character_end_times_seconds'][end-1]
        rows.append({'id':f's{i+1:02}','from':0 if i==0 else round(onset*fps),
          'duration':0,'text':text,'kind':'disclaimer' if visual=='disclaimer' else 'main',
          'speaker':speaker,'visual':visual,'speechStart':round(onset*fps),'speechEnd':math.ceil(speechEnd*fps),
          'charStart':start,'charEnd':end})
    for i,row in enumerate(rows): row['duration']=(rows[i+1]['from'] if i+1<len(rows) else frames)-row['from']
    captions=[]
    for row in rows:
        ws=[w for w in words if w['start']>=row['speechStart']/fps-.05 and w['start']<row['speechEnd']/fps]
        for i in range(0,len(ws),8):
            group=ws[i:i+8]
            captions.append({'from':round(group[0]['start']*fps),'end':math.ceil(group[-1]['end']*fps),'text':' '.join(w['text'] for w in group)})
    plan={'fps':fps,'durationFrames':frames,'title':'Lương tăng, tiền dư đi đâu?', 'segments':rows,'captions':captions,
      'words':words,'narrationSHA256':sha(audio),'audioSeconds':length}
    save(BATCH/'plan.json',plan)
    save(PROJECT/'public/finance-demo/plan.json',plan)
    save(BATCH/'clause-coverage.json',[{'id':r['id'],'text':r['text'],'start':r['from']/fps,'end':(r['from']+r['duration'])/fps,
      'castMechanic':{'hook':'Surprised Minh compares raise with unchanged jar','disclaimer':'Separate disclaimer card',
      'before':'Lan asks; Minh allocates monthly income','after':'Minh sees all raise move into spending','daily':'Minh protests; Lan fills 30 daily slots',
      'dinner':'Additional meal completes the extra spending','choice':'Compare illustrative budgets, then essential-cost caveat',
      'transfer':'Lan suggests schedule; funds move after obligations','cta':'Minh selects one monthly expense'}[r['visual']],
      'minimalMechanic':r['visual'],'review':'Pending rendered frame comparison'} for r in rows])

def voice():
    prepare();t=time.perf_counter()
    p=eleven_audio.speech(BATCH/'audio/narration.mp3',(BATCH/'script.txt').read_text(encoding='utf-8'),VOICE)
    save(BATCH/'audio/voice-run.json',{'wallSeconds':time.perf_counter()-t,'file':str(p.relative_to(ROOT)),
      'sha256':sha(p),'settings':{'voice':VOICE,'model':'eleven_v3','speed':1.0,'stability':.5,'similarity_boost':.8},
      'cost':'See provider receipt character_cost; not a dollar invoice','sharedAcrossBothStyles':True})
    prepare()

def pcm(p):
    return np.frombuffer(run([FF,'-v','error','-i',p,'-f','f32le','-acodec','pcm_f32le','-ac','2','-ar','48000','-']).stdout,dtype='<f4').reshape(-1,2)
def mix():
    plan=json.loads((BATCH/'plan.json').read_text(encoding='utf-8'));seconds=plan['durationFrames']/30
    n=round(seconds*48000);speech=pcm(BATCH/'audio/narration.mp3');out=np.zeros((n,2),dtype=np.float32)
    # A local loudness pass preserves speech speed/timing.
    run([FF,'-y','-v','error','-i',BATCH/'audio/narration.mp3','-af','loudnorm=I=-16:TP=-2:LRA=11','-ar','48000',BATCH/'audio/voice-normalized.wav'])
    speech=pcm(BATCH/'audio/voice-normalized.wav');out[:min(n,len(speech))]+=speech[:n]
    source=ROOT/'videos/2026-11-13-quan-dong-khach-het-tien/audio/music/precise-unit-math.mp3'
    receipt=json.loads(source.with_suffix('.receipt.json').read_text(encoding='utf-8'))
    if sha(source)!=receipt['sha256']: raise ValueError('Music source hash mismatch')
    target=BATCH/'audio/music-reused.mp3'
    shutil.copy2(source,target);shutil.copy2(source.with_suffix('.receipt.json'),target.with_suffix('.receipt.json'))
    music=pcm(source)
    if len(music)<n: raise ValueError('Music too short; no looping')
    music=music[:n].copy();rms=max(1e-7,float(np.sqrt(np.mean(music**2))))
    music*=.013/rms
    fade=np.minimum(np.arange(n)/48000/1.2,1)*np.minimum((n-1-np.arange(n))/48000/1.5,1)
    # Envelope-based ducking (30ms blocks) protects speech without adding new calls.
    activity=np.zeros(n)
    mono=np.mean(np.abs(speech),axis=1)
    for i in range(0,n,1440): activity[i:i+1440]=.45 if np.max(mono[i:min(i+1440,len(mono))],initial=0)>.02 else .8
    out+=music*(fade*activity)[:,None]
    cues=[]
    for segment in plan['segments']:
        if segment['visual'] not in ['before','after','dinner','transfer']:continue
        at=segment['speechStart']/30+.2;start=round(at*48000)
        # Original synthesized soft wooden/pluck cue; no external sample/license.
        t=np.arange(10080)/48000
        cue=(np.sin(2*np.pi*650*t)+.3*np.sin(2*np.pi*975*t))*np.exp(-t*34)*.017
        out[start:start+min(len(cue),n-start)]+=cue[:min(len(cue),n-start),None]
        cues.append({'at':at,'purpose':segment['visual'],'source':'Original local synthesized soft pluck'})
    peak=float(np.max(np.abs(out)));out*=min(1,.85/max(peak,1e-6))
    raw=BATCH/'audio/mix.f32';out.astype('<f4').tofile(raw)
    run([FF,'-y','-v','error','-f','f32le','-ar','48000','-ac','2','-i',raw,'-c:a','pcm_s16le',BATCH/'audio/final-mix.wav'])
    raw.unlink()
    save(BATCH/'audio/mix-receipt.json',{'narrationSHA256':sha(BATCH/'audio/narration.mp3'),'mixSHA256':sha(BATCH/'audio/final-mix.wav'),
      'music':{'source':str(source.relative_to(ROOT)),'sha256':sha(source),'providerReceiptSHA256':sha(source.with_suffix('.receipt.json')),'newPaidCall':False},
      'speechSpeed':1,'sharedAcrossStyles':True,'cues':cues,'peakBeforeLimiter':peak,'listening':'Not established by measurement'})

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('phase',choices=['prepare','voice','mix']);a=p.parse_args()
    {'prepare':prepare,'voice':voice,'mix':mix}[a.phase]()
