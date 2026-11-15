import requests,re,json
from pathlib import Path
out=Path('videos/2026-11-10-real-estate-10s')
for name,url in [('housing','https://www.pexels.com/video/aerial-view-of-apartment-buildings-in-the-city-15847247/'),('budget','https://www.pexels.com/video/woman-counting-money-7735860/')]:
 r=requests.get(url,timeout=35);print(name,r.status_code,flush=True)
 links=list(dict.fromkeys(re.findall(r'https[^\s"<>]+\.mp4[^\s"<>]*',r.text)))
 (out/f'{name}-links.json').write_text(json.dumps(links),encoding='utf8')
 print(links[:4],flush=True)
