from pathlib import Path
from faster_whisper import WhisperModel
import subprocess,json,imageio_ffmpeg
p=Path(__file__).resolve().parent
subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-y','-i',str(p/'speech.wav'),'-ss','4.1','-t','3.4',str(p/'unclear.wav')],check=True)
m=WhisperModel('small',device='cpu',compute_type='int8',cpu_threads=6,local_files_only=True)
s,_=m.transcribe(str(p/'unclear.wav'),language='vi',beam_size=7,condition_on_previous_text=False)
print([(x.start,x.end,x.text) for x in s])
