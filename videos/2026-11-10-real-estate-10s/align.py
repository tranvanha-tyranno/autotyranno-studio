from pathlib import Path
import json,wave,numpy as np
from faster_whisper import WhisperModel
out=Path('videos/2026-11-10-real-estate-10s');pub=out/'economics/public'
m=WhisperModel('base',device='cpu',compute_type='int8',cpu_threads=6,local_files_only=True)
segments,_=m.transcribe(str(pub/'voice.wav'),language='vi',word_timestamps=True,beam_size=5,initial_prompt=(out/'script.txt').read_text(encoding='utf8'))
words=[{'word':w.word.strip(),'start':w.start,'end':w.end} for s in segments for w in s.words or []]
(out/'narration-asr.json').write_text(json.dumps(words,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(words,ensure_ascii=True),flush=True)
# Match exact script spelling to recognized word starts; captions never rewrite the script.
import sys
sys.path.insert(0,str(Path('workflows/motion-slides').resolve()));from align_narration import align
cues,matched=align((out/'script.txt').read_text(encoding='utf8'),words,10)
# Compact five to eight syllable caption phrases, using recognized timings.
original=(out/'script.txt').read_text(encoding='utf8').split();flat=[w for c in cues for w in c['words']]
parts=[(0,3),(3,10),(10,15),(15,20),(20,24),(24,len(original))]
cs=[]
for a,b in parts:
 cs.append({'start':flat[a]['start'],'end':flat[b]['start'] if b<len(flat) else 9.85,'words':flat[a:b]})
(pub/'captions.json').write_text(json.dumps(cs,ensure_ascii=False),encoding='utf8')
w=wave.open(str(pub/'voice.wav'));a=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(float)/32768;a=a.reshape(-1,w.getnchannels()).mean(1);rate=w.getframerate();step=int(rate*.01)
env=[float(np.sqrt(np.mean(a[i:i+step]**2))) for i in range(0,len(a),step)];peak=max(env)
(pub/'waveform.json').write_text(json.dumps([round((v/peak)**.65,4) for v in env]))
print('captions and waveform ready; matched',matched,flush=True)

