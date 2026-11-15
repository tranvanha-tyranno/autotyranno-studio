"""Acquire Pexels footage with receipts; no paid generation or competitor media.

Public CDN candidates are probed; only successful real media is retained. The
editor must open the generated contact sheets before setting inspected status.
"""
import argparse, concurrent.futures, hashlib, json, re, subprocess, time
from pathlib import Path
import requests, imageio_ffmpeg
from PIL import Image, ImageDraw

PROJECT=Path(__file__).resolve().parents[2]
BATCH=PROJECT/'videos/2026-11-14-banh-mi-documentary'
FF=imageio_ffmpeg.get_ffmpeg_exe()

def save(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    temp=path.with_suffix(path.suffix+'.tmp');temp.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8');temp.replace(path)

def acquire(spec):
    ident=str(spec['pexelsID']);dst=BATCH/'assets/raw'/f'pexels-{ident}.mp4';dst.parent.mkdir(parents=True,exist_ok=True)
    receipt=BATCH/'research/asset-receipts'/f'pexels-{ident}.json'
    if dst.exists() and receipt.exists(): return json.loads(receipt.read_text(encoding='utf-8'))
    urls=[]
    for fps in spec.get('fps',[25,24,30,50,60,29,23,59]):
        for dim in spec.get('dimensions',['1280_720','720_1280','1920_1080','1080_1920','1366_720','720_1366','4096_2160','2160_4096','3840_2160','2160_3840']):
            qual='hd' if max(map(int,dim.split('_')))<=1920 else 'uhd'
            urls.append(f'https://videos.pexels.com/video-files/{ident}/{ident}-{qual}_{dim}_{fps}fps.mp4')
    chosen=spec.get('downloadURL')
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        def check(url):
            try:
                head=requests.head(url,timeout=12)
                return (url,head.status_code,int(head.headers.get('content-length','0')))
            except requests.RequestException:return (url,None,0)
        for start in range(0,len(urls),16):
            if chosen:break
            hits=[x for x in pool.map(check,urls[start:start+16]) if x[1]==200]
            if hits:
                chosen=sorted(hits,key=lambda x:x[2] or 10**12)[0][0];break
    if not chosen: return {'id':f'pexels-{ident}','status':'download_failed','pageURL':spec['pageURL'],'reason':'No successful public CDN candidate found'}
    started=time.perf_counter();res=requests.get(chosen,timeout=180);res.raise_for_status()
    partial=dst.with_suffix('.partial');partial.write_bytes(res.content);partial.replace(dst)
    proc=subprocess.run([FF,'-hide_banner','-i',str(dst)],capture_output=True,text=True)
    match=re.search(r'Duration: (\d+):(\d+):(\d+\.\d+)',proc.stderr)
    if not match:raise ValueError('Not decodable '+str(dst))
    dur=int(match[1])*3600+int(match[2])*60+float(match[3])
    size=re.search(r'Video:.*?, (\d+)x(\d+)',proc.stderr)
    data={**spec,'id':f'pexels-{ident}','file':dst.relative_to(BATCH).as_posix(),'sha256':hashlib.sha256(res.content).hexdigest(),'bytes':len(res.content),'durationSeconds':dur,'downloadURL':chosen,'license':'Pexels License - free to use/modify; no implied endorsement or standalone resale','licenseURL':'https://www.pexels.com/license/','acquisitionMethod':'Public CDN successful HTTP GET; source page discovered through primary Pexels search result. HTML requests may be Cloudflare 403.','downloadSeconds':round(time.perf_counter()-started,3),'inspection':{'status':'pending','observations':'Contact sheet generated; requires actual visual review.','allOriginalAudioAuditioned':False},'sourceRole':'illustrative stock; does not identify fictional Hạnh or prove her numbers','usableIntervals':[]}
    if size:data['width'],data['height']=map(int,size.groups())
    samples=[round(dur*x,3) for x in [.04,.18,.34,.5,.66,.82,.96]]
    sheet=Image.new('RGB',(4*320,2*204),'#111111');draw=ImageDraw.Draw(sheet)
    for i,sec in enumerate(samples):
        cmd=[FF,'-v','error','-ss',str(sec),'-i',str(dst),'-frames:v','1','-vf','scale=320:180:force_original_aspect_ratio=decrease,pad=320:180:(ow-iw)/2:(oh-ih)/2','-f','image2pipe','-vcodec','mjpeg','pipe:1']
        from io import BytesIO
        frame=Image.open(BytesIO(subprocess.run(cmd,capture_output=True,check=True).stdout)).convert('RGB')
        x=(i%4)*320;y=(i//4)*204;sheet.paste(frame,(x,y+24));draw.text((x+5,y+4),f'{ident} {sec:.2f}s',fill='white')
    sheetpath=BATCH/'research/contact-sheets'/f'pexels-{ident}.jpg';sheetpath.parent.mkdir(parents=True,exist_ok=True);sheet.save(sheetpath,quality=90)
    data['inspection']['contactSheet']=sheetpath.relative_to(BATCH).as_posix()
    save(receipt,data);print('FOOTAGE_DOWNLOADED',ident,dur,len(res.content),flush=True);return data

def main():
    p=argparse.ArgumentParser();p.add_argument('manifest',type=Path);args=p.parse_args()
    specs=json.loads(args.manifest.read_text(encoding='utf-8-sig'))['candidates']
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        for result in pool.map(acquire,specs):
            out=BATCH/'research/footage-sources.json'
            current=json.loads(out.read_text(encoding='utf-8')) if out.exists() else {'schema':'bread-film-footage-sources/1','assets':[],'failed':[]}
            key='failed' if result.get('status')=='download_failed' else 'assets'
            current[key]=[x for x in current[key] if x['id']!=result['id']]+[result]
            save(out,current)
    print('FOOTAGE_MANIFEST',out,flush=True)

if __name__=='__main__':main()
