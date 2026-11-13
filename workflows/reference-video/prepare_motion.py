from pathlib import Path
import sys,json,shutil,re,argparse
sys.path.insert(0,'workflows/reference-video');from documentary import FF,run,duration;from eleven_audio import words
p=argparse.ArgumentParser();p.add_argument('--batch',type=Path,default=Path('videos/2026-11-11-cinematic-reset'));p.add_argument('--skip-media',action='store_true');args=p.parse_args()
b=args.batch;pub=Path(__file__).parent/'cinematic/public';d=json.loads((b/'batch.json').read_text(encoding='utf-8'));a=b/d.get('voiceAsset','audio/narration-v2.mp3');factor=duration(a)/49
if not .8<=factor<=1.22:raise ValueError('Rewrite script: natural timing outside allowed tempo range')
if not args.skip_media:run([FF,'-v','error','-y','-i',str(a),'-af',f'atempo={factor:.9f},apad=whole_dur=50','-t','50',str(b/'narration.wav')])
w=words(json.loads(a.with_suffix('.alignment.json').read_text(encoding='utf-8')))
for row in w:row['start']/=factor;row['end']/=factor
(b/'aligned-words.json').write_text(json.dumps(w,ensure_ascii=False,indent=2),encoding='utf-8')
norm=lambda s:re.sub(r'[^\w]','',s.lower())
def find(phrase):
 q=[norm(x) for x in phrase.split()]
 for i in range(len(w)-len(q)+1):
  if [norm(x['text']) for x in w[i:i+len(q)]]==q:return round(w[i]['start']*30)
 raise ValueError(phrase)
cuts=[0,find('Nhưng khoan'),find('Mười tháng'),find('Hãy nhìn'),find('Với nền kinh tế'),find('Nhưng câu hỏi'),1500]
caps=[];chunk=[]
for row in w:
 chunk.append(row)
 if len(chunk)>=9 or len(' '.join(x['text'] for x in chunk))>48 or re.search(r'[.!?:]$',row['text']):
  caps.append({'start':chunk[0]['start'],'end':row['end'],'text':' '.join(x['text'] for x in chunk)})
  chunk=[]
if chunk:caps.append({'start':chunk[0]['start'],'end':chunk[-1]['end'],'text':' '.join(x['text'] for x in chunk)})
data={'cuts':cuts,'captions':caps,'narrationFactor':factor,'source':'Provider alignment of exact Nhật Phong v3 take','sewingStart':cuts[3]/30}
(pub/'data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8');(b/'timeline.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8');print('CUTS',cuts,'ATEMPO',factor)
for name,id in ([] if args.skip_media else [('sewing-a',51012),('sewing-b',51013)]):
 src=Path('videos/2026-11-11-ten-pass-review/new-assets')/f'mixkit-{id}.mp4';run([FF,'-v','error','-y','-i',str(src),'-an','-vf','fps=30,scale=1920:1080,setsar=1,setparams=range=tv:color_primaries=bt709:color_trc=bt709:colorspace=bt709','-c:v','libx264','-preset','fast','-crf','19',str(pub/f'{name}.mp4')])
shutil.copy2(b/'narration.wav',pub/'narration.wav')
