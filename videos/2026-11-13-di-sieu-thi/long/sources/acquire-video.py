from pathlib import Path
import requests,json,hashlib,concurrent.futures,subprocess
import imageio_ffmpeg
root=Path('videos/2026-11-13-di-sieu-thi/long');(root/'assets').mkdir(parents=True,exist_ok=True)
rows=[
('clip-choose',5104001,'customer-picking-food-items-from-a-supermarket','Gustavo Fring','https://videos.pexels.com/video-files/5104001/5104001-uhd_3840_2160_30fps.mp4'),
('clip-aisle',10901926,'customers-shopping-at-supermarket','Suika Chan','https://videos.pexels.com/video-files/10901926/10901926-hd_1920_1080_30fps.mp4'),
('clip-checkout',5103988,'woman-getting-things-out-of-grocery-basket-at-billing-counter','Gustavo Fring','https://videos.pexels.com/video-files/5103988/5103988-uhd_3840_2160_30fps.mp4'),
('clip-cart',35226314,'pov-shopping-in-a-busy-supermarket','Engin Akyurt','https://videos.pexels.com/video-files/35226314/14924151_3840_2160_30fps.mp4')]
def one(row):
 name,vid,slug,creator,url=row;path=root/'assets'/f'{name}.mp4'
 if not path.exists():
  r=requests.get(url,stream=True,timeout=45);r.raise_for_status()
  if int(r.headers.get('content-length','0'))>300_000_000:return dict(id=name,error='Source larger than300MB; skipped')
  partial=path.with_suffix('.download')
  with partial.open('wb') as f:
   for chunk in r.iter_content(1024*1024):f.write(chunk)
  partial.replace(path)
 log=subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-hide_banner','-i',str(path)],capture_output=True,text=True).stderr
 d={'id':name,'providerVideoId':vid,'file':f'assets/{name}.mp4','page':f'https://www.pexels.com/video/{slug}-{vid}/','download':url,'creator':creator,'license':'Pexels License','licenseURL':'https://www.pexels.com/license/','bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'streams':[x.strip() for x in log.splitlines() if 'Stream #' in x],'inspectionStatus':'pending','role':'Illustrative real stock footage; no depicted person asserted to overspend; foreign store not evidence of Vietnamese store.'}
 return d
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:rows=list(pool.map(one,rows))
(root/'video-candidates.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(rows,ensure_ascii=False,indent=2))
