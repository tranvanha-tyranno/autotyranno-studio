"""Download newly sourced Freesound CC0 audio with individual HTML/hash receipts.

Uses public HQ MP3 preview derivatives, not authenticated original WAV downloads.
No synthesized sound, credentials, paid calls, or audio-listening claims.
"""
import concurrent.futures, hashlib, json, re, subprocess
from pathlib import Path
import requests, imageio_ffmpeg
from bs4 import BeautifulSoup

PROJECT=Path(__file__).resolve().parents[2]
BATCH=PROJECT/'videos/2026-11-15-banh-mi-mo-phong-openai'
FF=imageio_ffmpeg.get_ffmpeg_exe()

SPECS=[
('bread-cut','BogumilaMerc',835792,'Knife slicing bread at three speeds',['bread','cut','knife'],['b01','b03','b08','b24']),
('bread-crunch','mealwyrm',495813,'Bread crust crunch recording',['bread','crunch'],['b01','b18','b24']),
('oven-door','bolkmar',503477,'Oven door opening and closing',['oven','door'],['b02','b12']),
('receipt-printer','thepodcastdoctor',476011,'Receipt printer in pharmacy',['receipt','printer'],['b04','b05','b13']),
('paper-bag','randbsoundbites',795443,'Scrunching a paper bag',['paper','bag'],['b01','b04','b24']),
('coins-drop','bwarpus99',443858,'Coins dropping on counter',['coin','money'],['b03','b05','b06','b18']),
('money-pickup','LeMudCrab',163451,'Coins contacting other coins',['coin','tick'],['b05','b06','b18']),
('calculator','nodzSound',506529,'Number-key presses on calculator',['calculator','click'],['b03','b05','b17','b18']),
('pen-paper','khenshom',565206,'Close-up pen or marker writing on paper',['pen','paper'],['b04','b13','b23']),
('market-room','SamuelGremaud',544338,'Market ambience in Sault France',['market','ambience'],['b14','b20','b21']),
('short-whoosh','Kinoton',427979,'Short bamboo-stick swings, thirteen versions',['transition','whoosh'],['b07','b11','b16','b22']),
('oven-beeps','sidequesting',580225,'Oven sheet/door handling and button beeps',['oven','beep','tray'],['b02','b12']),
('bread-bag-drop','qubodup',189312,'Loaf in plastic bag dropped onto surface',['bread','bag','drop'],['b01','b24']),
('oven-close','TiesWijnen',455538,'Small oven door slammed shut',['oven','hit'],['b02','b12']),
('calculator-slide','redpanda69',686164,'Calculator sliding into plastic case',['slide','plastic'],['b07','b16','b22']),
('bread-cooling','Erbsland-Music',623368,'Fresh bread crust crackles while cooling; source notes oven fan/clothing noises',['bread','crackle','oven'],['b02','b12'])
 ,('flour-bag-drop','bbrocer',382642,'Bag of flour taken from shelf and dropped onto counter',['flour','bag','drop'],['b02','b05','b11','b12'])
]

def save(p,data):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def get_one(spec):
    ident,creator,sound_id,description,tags,units=spec
    page=f'https://freesound.org/people/{creator}/sounds/{sound_id}/'
    response=requests.get(page,timeout=40);response.raise_for_status()
    html=response.text;soup=BeautifulSoup(html,'html.parser')
    links=[a.get('href','') for a in soup.find_all('a')]
    license_urls=[x for x in links if 'creativecommons.org/publicdomain/zero/1.0' in x]
    if not license_urls:raise ValueError(f'{ident}: source is not individual CC0')
    candidates=re.findall(r'https://cdn\.freesound\.org/previews/[^"\s<>]+-hq\.mp3',html)
    if not candidates:raise ValueError(f'{ident}: no public HQ MP3 exposed')
    url=candidates[0].replace('&amp;','&')
    result=requests.get(url,timeout=90);result.raise_for_status()
    if len(result.content)<1000:raise ValueError('Small/invalid sound payload')
    dst=BATCH/'audio/sfx/downloaded'/(ident+'.mp3');dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(result.content)
    capture=subprocess.run([FF,'-hide_banner','-i',str(dst)],capture_output=True,text=True)
    m=re.search(r'Duration: (\d+):(\d+):(\d+\.\d+)',capture.stderr)
    if not m:raise ValueError('Undecodable media')
    dur=int(m[1])*3600+int(m[2])*60+float(m[3])
    check=subprocess.run([FF,'-v','error','-i',str(dst),'-f','null','-'],capture_output=True)
    if check.returncode:raise ValueError('Full decode failed')
    source_path=BATCH/'research/sfx-source-pages'/(ident+'.html');source_path.parent.mkdir(parents=True,exist_ok=True);source_path.write_bytes(response.content)
    textpath=source_path.with_suffix('.txt');textpath.write_text(soup.get_text(' ',strip=True),encoding='utf-8')
    title=soup.find('h1')
    a={'id':ident,'file':dst.relative_to(BATCH).as_posix(),'sha256':hashlib.sha256(result.content).hexdigest(),'bytes':len(result.content),'durationSeconds':dur,'sourceURL':page,'downloadURL':url,'creator':creator,'sourceTitle':title.get_text(' ',strip=True) if title else description,'license':'CC0 1.0 Universal','licenseURL':'https://creativecommons.org/publicdomain/zero/1.0/','individualLicenseObserved':license_urls[0],'observedDescription':description,'descriptionBasis':'Description and individual CC0 license read on the source page; audio has not been auditioned.','tags':tags,'cueRecommendations':[{'narrationUnit':x,'role':'Contextual foley for the corresponding visible process/object or restrained calculation/transition cue; align to exact final narration and visible action.'} for x in units],'sourceReceipt':{'html':source_path.relative_to(BATCH).as_posix(),'htmlSHA256':hashlib.sha256(response.content).hexdigest(),'text':textpath.relative_to(BATCH).as_posix(),'checkedDateLocal':'2026-11-15','httpStatus':response.status_code},'inspection':{'method':'individual_source_description_license_and_complete_ffmpeg_decode','status':'downloaded_decoded_not_auditioned','limits':'No listening performed. Semantic label follows source description. Final editor must audition/select trim and avoid audible foreign speech/music in ambience. HQ MP3 is a provider-hosted public derivative, not original WAV.'},'derivedFrom':'Public HQ MP3 preview, downloaded byte-for-byte; originals on Freesound require login.','attributionSuggested':f'{description} by {creator}, Freesound #{sound_id}, CC0 1.0: {page}'}
    if ident=='market-room':a['mixCaution']='French market recording, not Vietnamese location evidence. Use very quietly only if speech is unintelligible; no location claim.'
    if ident=='bread-cooling':a['mixCaution']='Source discloses oven fan and clothing noises. Audition isolated crackles before use; no clean-foley claim.'
    save(BATCH/'research/sfx-receipts'/(ident+'.json'),a)
    print('SFX_DOWNLOADED',ident,len(result.content),dur,flush=True)
    return a

def main():
    results=[];failed=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        futures={pool.submit(get_one,spec):spec for spec in SPECS}
        for f in concurrent.futures.as_completed(futures):
            spec=futures[f]
            try:results.append(f.result())
            except Exception as e:
                failed.append({'id':spec[0],'sourceURL':f'https://freesound.org/people/{spec[1]}/sounds/{spec[2]}/','reason':str(e)})
                print('SFX_FAILED',spec[0],type(e).__name__,flush=True)
            save(BATCH/'research/sfx-sources.json',{'schema':'bread-film-internet-sfx/1','dateLocal':'2026-11-15','assets':sorted(results,key=lambda x:x['id']),'failed':failed,'auditioned':False,'paidCalls':0,'oldProviderSoundsReused':False,'rightsScope':'Each asset individual page contains CC0 1.0 link, retained HTML and hash. No category-wide license assumption.','overallStatus':'downloaded_and_decoded_pending_listening_mix_review'})
    print('SFX_COMPLETE',len(results),'failed',len(failed),flush=True)

if __name__=='__main__':main()
