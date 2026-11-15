from pathlib import Path
import subprocess,json
import imageio_ffmpeg
from faster_whisper import WhisperModel
p=Path(__file__).resolve().parent
m=WhisperModel('small',device='cpu',compute_type='int8',cpu_threads=6)
s,_=m.transcribe(str(p/'speech.wav'),language='vi',word_timestamps=True,beam_size=5,condition_on_previous_text=False,initial_prompt='Và sau đây, em xin kể về một câu chuyện, một trải nghiệm. Tôi từng có dịp cùng thầy tôi tham gia một chuyến thiện nguyện tại Bệnh viện Nhi Đồng 2. Chuẩn bị và trao quà cho hơn một trăm em nhỏ đang điều trị bệnh.')
data=[{'start':x.start,'end':x.end,'text':x.text,'words':[{'word':w.word,'start':w.start,'end':w.end} for w in x.words or []]} for x in s]
(p/'transcript-small.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(data,ensure_ascii=True),flush=True)
