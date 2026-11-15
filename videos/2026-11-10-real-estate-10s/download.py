from pathlib import Path
import requests,subprocess,sys,importlib.util,json
out=Path('videos/2026-11-10-real-estate-10s');pub=out/'economics/public';pub.mkdir(parents=True,exist_ok=True)
for name,url in [('housing','https://videos.pexels.com/video-files/15847247/15847247-uhd_3840_2160_24fps.mp4'),('budget','https://videos.pexels.com/video-files/7735860/7735860-hd_1920_1080_25fps.mp4')]:
 p=pub/f'{name}.mp4'
 if p.exists():continue
 r=requests.get(url,timeout=120);r.raise_for_status();p.write_bytes(r.content);print(name,len(r.content),flush=True)
