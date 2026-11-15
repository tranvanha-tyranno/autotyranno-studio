from pathlib import Path
import requests,subprocess,sys,importlib.util,json
out=Path('videos/2026-11-10-real-estate-10s');sys.path.insert(0,str(Path('workflows/product-video').resolve()));import run
text='Nhà giảm giá, sao cả nền kinh tế chậm lại? Vì tài sản teo đi, người dân ngại tiêu tiền. Cửa hàng ít khách, doanh nghiệp có thể cắt việc làm.'
(out/'script.txt').write_text(text,encoding='utf-8')
pub=out/'economics/public';pub.mkdir(parents=True,exist_ok=True)
if not (out/'voice-original.mp3').exists():
 if (out/'tts-request.json').exists():raise RuntimeError('Previous request exists; inspect first')
 (out/'tts-request.json').write_text(json.dumps({'text':text,'voice':'Adam','model':'eleven_v3'},ensure_ascii=False),encoding='utf-8')
 r=requests.post('https://api.elevenlabs.io/v1/text-to-speech/pNInz6obpgDQGcFmaJgB',params={'output_format':'mp3_44100_128'},headers={'xi-api-key':run.eleven_key(),'Accept':'audio/mpeg'},json={'text':text,'model_id':'eleven_v3','language_code':'vi','voice_settings':{'stability':.5}},timeout=180)
 print('TTS HTTP',r.status_code,flush=True)
 if r.status_code!=200:raise RuntimeError('Provider failed HTTP '+str(r.status_code))
 (out/'voice-original.mp3').write_bytes(r.content)
d=run.duration(out/'voice-original.mp3');speed=d/9.45
subprocess.run([run.FF,'-v','error','-y','-i',str(out/'voice-original.mp3'),'-af',f'atempo={speed},adelay=180|180,apad,atrim=duration=10','-ar','44100',str(pub/'voice.wav')],check=True)
(out/'voice-timing.json').write_text(json.dumps({'original_seconds':d,'atempo':speed,'leading_silence':.18,'final_seconds':10},indent=2))
print('VOICE READY',d,speed,flush=True)
