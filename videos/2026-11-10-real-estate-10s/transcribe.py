import os,json,sys,importlib.util
from pathlib import Path
from faster_whisper import WhisperModel
out=Path('videos/2026-11-10-real-estate-10s')
m=WhisperModel('base',device='cpu',compute_type='int8',cpu_threads=6,local_files_only=True)
s,_=m.transcribe(str(out/'reference-opening.wav'),language='vi',beam_size=3)
t=[{'start':x.start,'end':x.end,'text':x.text} for x in s]
(out/'reference-transcript.json').write_text(json.dumps(t,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(t,ensure_ascii=True))
