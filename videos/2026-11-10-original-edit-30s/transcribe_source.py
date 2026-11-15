from pathlib import Path
import subprocess,json
import imageio_ffmpeg
from faster_whisper import WhisperModel
p=Path(__file__).resolve().parent
src=Path('C:/Users/tyranno/Documents/output/2aOboRBgAQPTOVBDeyiJ3DUdElfGnNoIsHObfk48.mp4')
subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-y','-i',str(src),'-t','30','-vn','-ac','1','-ar','16000',str(p/'speech.wav')],check=True)
m=WhisperModel('base',device='cpu',compute_type='int8',cpu_threads=6,local_files_only=True)
s,_=m.transcribe(str(p/'speech.wav'),language='vi',word_timestamps=True,beam_size=5)
data=[{'start':x.start,'end':x.end,'text':x.text,'words':[{'word':w.word,'start':w.start,'end':w.end} for w in x.words or []]} for x in s]
(p/'transcript.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(data,ensure_ascii=True),flush=True)
