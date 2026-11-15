from pathlib import Path
import json
p=Path('videos/2026-11-10-real-estate-10s');pub=p/'economics/public'
raw=json.loads((p/'narration-asr.json').read_text(encoding='utf8'))[:31]
script=(p/'script.txt').read_text(encoding='utf8').split()
parts=[(0,3),(3,10),(10,15),(15,20),(20,24),(24,31)]
cs=[]
for a,b in parts:
 cs.append({'start':max(.18,raw[a]['start']),'end':raw[b]['start'] if b<len(script) else 9.85,'words':[{'text':script[i],'start':max(.18,raw[i]['start'])} for i in range(a,b)]})
(pub/'captions.json').write_text(json.dumps(cs,ensure_ascii=False),encoding='utf8')
