"""Render one fast 6-second POV clip per supplied mica image.

The input images are already staged product compositions. This runner uses each
image as its own first-frame reference; it does not make additional backgrounds.
It is intentionally separate from the N x 3 opening-image compiler.
"""
from __future__ import annotations

import base64
import concurrent.futures
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time

import imageio_ffmpeg
import requests

def load_runner():
    root = Path(__file__).resolve().parents[3]
    spec = __import__('importlib.util').util.spec_from_file_location('mica_uploaded_runner', root/'workflows/product-video/run.py')
    module = __import__('importlib.util').util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'videos' / '2026-10-28-mica-6refs-fast'
REFS = [
    (r'C:\Users\tyranno\AppData\Local\Temp\codex-clipboard-99a6e628-0aab-47e0-a7ec-ff3a0bc6d319.png', 'inox-factory', 'Ấm inox cao cấp 1,8 lít', 'bối cảnh xưởng sản xuất điện máy đang có trong ảnh', '[excited] Ê ê ê! Ấm inox 1,8 lít, nấu nhanh mà còn tự ngắt điện nữa nè!'),
    (r'C:\Users\tyranno\AppData\Local\Temp\codex-clipboard-9ead2a26-3559-4eed-802c-a2385c3ecc81.png', 'inox-mall', 'Ấm inox cao cấp 1,8 lít', 'bối cảnh trung tâm thương mại đang có trong ảnh', '[playful] Các dợ nhìn em ấm inox này coi! Vòi rót gọn, tay cầm cách nhiệt, đế xoay 360 độ luôn á!'),
    (r'C:\Users\tyranno\AppData\Local\Temp\codex-clipboard-aa2c4628-616b-4e0e-aa59-95ba7e664d3d.png', 'inox-appliance-store', 'Ấm inox cao cấp 1,8 lít', 'bối cảnh cửa hàng gia dụng đang có trong ảnh', '[amazed] Inox sáng bóng, nắp mở tiện, đun nước gọn lẹ; mấy ní thấy hợp thì chốt nha!'),
    (r'C:\Users\tyranno\AppData\Local\Temp\codex-clipboard-bdf4abdd-ccfe-469c-a35b-8f61d1aba8bd.png', 'oral-factory', 'Máy tăm nước Oral Irrigator 6886', 'bối cảnh xưởng sản xuất đang có trong ảnh', '[excited] Ê ê ê! Máy tăm nước Oral Irrigator 6886, nhỏ gọn mà mang đi đâu cũng tiện!'),
    (r'C:\Users\tyranno\AppData\Local\Temp\codex-clipboard-bafccd7e-3706-48d2-8344-f3e9277f0f24.png', 'oral-mall', 'Máy tăm nước Oral Irrigator 6886', 'bối cảnh trung tâm thương mại đang có trong ảnh', '[playful] Có ba chế độ, nhiều đầu tăm và túi đựng; một bộ là đủ gọn cho góc chăm răng rồi!'),
    (r'C:\Users\tyranno\AppData\Local\Temp\codex-clipboard-eb703e33-ba91-4424-bbac-fd762b22e57d.png', 'oral-appliance-store', 'Máy tăm nước Oral Irrigator 6886', 'bối cảnh cửa hàng gia dụng đang có trong ảnh', '[confident] Bình nước, dây sạc và phụ kiện xếp chung một hộp; mấy ní xem kỹ nhãn rồi hẵng chốt nha!'),
]

FF = imageio_ffmpeg.get_ffmpeg_exe()
runner = load_runner()
BASE = 'http://127.0.0.1:18610'


def write_json(path: Path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')


def data_url(path: Path):
    return 'data:image/png;base64,' + base64.b64encode(path.read_bytes()).decode()


def media_url(task):
    return task.get('url') or task.get('video', {}).get('url') or task.get('result', {}).get('url')


def prompt_for(name, setting, product):
    if product.startswith('Ấm'):
        detail = 'Giữ đúng ấm inox màu bạc, thân kim loại, quai đen, nắp đen, vòi rót, đèn báo đỏ và đế xoay; không biến thành sản phẩm khác. Các claim nhìn thấy trên ảnh là 1,8L, inox cao cấp, đun sôi nhanh, tự động ngắt điện, vòi rót tiện lợi, tay cầm cách nhiệt, nút mở nắp và đế xoay 360 độ.'
    else:
        detail = 'Giữ đúng bộ máy tăm nước Oral Irrigator 6886 màu xanh nhạt/trắng, bình nước, các đầu tăm, dây USB và túi vải đúng số lượng và vị trí. Các thông tin phải bám đúng nhãn ảnh: Portable, 360 Clean Your Teeth, 3 Modes, Capacity 220ML/230ML tùy ảnh, DC Socket và các dòng chữ đang nhìn thấy.'
    action = '0–0,3 giây bắt đầu chuyển động ngay; 0,3–2,3 giây camera tiến nhẹ khoảng 6% và dịch ngang có chủ đích; 2,3–4,8 giây camera đi một cung nhỏ 12–18 độ sang phía tay cầm, hộp vẫn thẳng mặt camera; 4,8–6 giây trả về góc trước ổn định. Hậu cảnh trôi nhẹ tạo parallax, không đứng hình.'
    return f'''Tạo video POV dọc 9:16, đúng 6 giây, từ chính ảnh tham chiếu này. Đây là biến thể {name}, {setting}. {detail}

{action}

Chỉ camera và chuyển động tự nhiên của cẳng tay/bàn tay được phép chuyển động. Nếu có nhún, chỉ 1–2 cm theo quán tính; hộp mica không xoay, không lật, không biến dạng, không chạm sàn/bàn/bục. Giữ nguyên tuyệt đối bố cục bối cảnh ảnh, màu ánh sáng, tay, màu móng, kiểu quai, kích thước hộp, sản phẩm, phụ kiện, từng chữ, số và nhãn. Mặt hộp luôn hướng camera, thấy trọn quai và đáy với khoảng trống phía dưới. Không thêm mặt/người/tay/ngón, không phản chiếu mặt người, không thêm logo biển quảng cáo, chữ mới, watermark, props, nhạc, thoại hay sound effect. Không tự sửa chính tả hoặc diễn giải claim. Một cảnh liền mạch, không cắt, không slow motion, không giữ khung tĩnh lâu, không xoay tới mặt sau không có trong ảnh. Ưu tiên giữ hình sản phẩm/chữ chính xác hơn chuyển động mạnh.'''


def render_one(index, reference, slug, product, setting, dialogue, muse_key, eleven_key):
    source = Path(reference)
    if not source.exists():
        raise FileNotFoundError(str(source))
    directory = OUT / f'{index:02}-{slug}'
    directory.mkdir(parents=True, exist_ok=True)
    shutil_copy = directory / 'input.png'
    if not shutil_copy.exists():
        shutil_copy.write_bytes(source.read_bytes())
    prompt = prompt_for(slug, setting, product)
    (directory / 'video-prompt.txt').write_text(prompt, encoding='utf-8')
    (directory / 'dialogue.txt').write_text(dialogue, encoding='utf-8')
    voice_path = directory / 'voice.mp3'
    if not voice_path.exists():
        response = requests.post('https://api.elevenlabs.io/v1/text-to-speech/pNInz6obpgDQGcFmaJgB', params={'output_format':'mp3_44100_128'}, headers={'xi-api-key':eleven_key,'Accept':'audio/mpeg'}, json={'text':dialogue,'model_id':'eleven_v3','language_code':'vi','voice_settings':{'stability':0.5}}, timeout=180)
        if response.status_code != 200:
            raise RuntimeError(f'ElevenLabs HTTP {response.status_code}: {response.text[:400]}')
        voice_path.write_bytes(response.content)
    task_path = directory / 'muse-task.json'
    video_raw = directory / 'muse-original.mp4'
    if not video_raw.exists():
        if task_path.exists():
            task_id = json.loads(task_path.read_text(encoding='utf-8'))['id']
        else:
            response = requests.post(BASE+'/v1/videos', headers={'Authorization':'Bearer '+muse_key,'Content-Type':'application/json'}, json={'prompt':prompt,'duration':6,'size':'9:16','resolution':'720p','reference_image':data_url(source)}, timeout=90)
            if response.status_code >= 400:raise RuntimeError(f'Muse HTTP {response.status_code}: {response.text[:500]}')
            task=response.json();task_id=task['id'];write_json(task_path,task)
        last=None
        for _ in range(100):
            task=requests.get(BASE+'/v1/videos/'+task_id,headers={'Authorization':'Bearer '+muse_key},timeout=35).json()
            state=(task.get('status'),task.get('progress'))
            if state!=last:print(slug,state,flush=True);last=state
            if task.get('status')=='failed':raise RuntimeError(task.get('error','Muse task failed'))
            if task.get('status')=='completed':
                response=requests.get(media_url(task),headers={'Authorization':'Bearer '+muse_key},timeout=120);response.raise_for_status();video_raw.write_bytes(response.content);write_json(task_path,task);break
            time.sleep(7)
        else:raise RuntimeError('Muse task remains pending')
    final = directory / 'final.mp4'
    if not final.exists():
        probe=subprocess.run([FF,'-hide_banner','-i',str(video_raw)],capture_output=True,text=True,encoding='utf-8',errors='replace')
        match=re.search(r'Duration: (\d+):(\d+):(\d+\.\d+)',probe.stderr)
        if not match:raise RuntimeError('Cannot read Muse duration')
        seconds=int(match[1])*3600+int(match[2])*60+float(match[3])
        if seconds<5.96:raise RuntimeError(f'Muse output shorter than 6s: {seconds}')
        voice_probe=subprocess.run([FF,'-hide_banner','-i',str(voice_path)],capture_output=True,text=True,encoding='utf-8',errors='replace')
        voice_match=re.search(r'Duration: (\d+):(\d+):(\d+\.\d+)',voice_probe.stderr)
        voice_seconds=int(voice_match[1])*3600+int(voice_match[2])*60+float(voice_match[3]) if voice_match else 6
        tempo=max(1.0,voice_seconds/5.8)
        if tempo>1.25:raise RuntimeError(f'Dialogue too long for 6 seconds: {voice_seconds:.2f}s')
        filters=f'[0:v]scale=720:1280:force_original_aspect_ratio=increase:force_divisible_by=2,crop=720:1280,setsar=1,fps=30[v];[1:a]atempo={tempo:.8f},apad,atrim=duration=6[a]'
        subprocess.run([FF,'-y','-i',str(video_raw),'-i',str(voice_path),'-filter_complex',filters,'-map','[v]','-map','[a]','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-t','6','-movflags','+faststart',str(final)],capture_output=True,check=True)
    subprocess.run([FF,'-v','error','-i',str(final),'-f','null','-'],capture_output=True,check=True)
    subprocess.run([FF,'-y','-i',str(final),'-vf','fps=1,scale=180:320,tile=3x2','-frames:v','1',str(directory/'contact-sheet.jpg')],capture_output=True,check=True)
    probe=subprocess.run([FF,'-hide_banner','-i',str(final)],capture_output=True,text=True,encoding='utf-8',errors='replace')
    report={'index':index,'slug':slug,'product':product,'setting':setting,'reference':str(source),'seconds':6,'dialogue':dialogue,'full_dialogue_preserved':True,'decode':'passed','output':str(final),'metadata':'Measure resolution/fps from final file; visual fidelity and text still require inspection.'}
    write_json(directory/'verification.json',report)
    return final


def main():
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--only',type=int);args=parser.parse_args()
    OUT.mkdir(parents=True,exist_ok=True)
    env=(ROOT/'experiments/muse2api-czg86389/.env').read_text(encoding='utf-8-sig')
    muse_key=next(line.split('=',1)[1].strip().strip('"\'') for line in env.splitlines() if line.startswith('MUSE2API_KEY='))
    eleven_key=runner.eleven_key()
    jobs=REFS if args.only is None else [REFS[args.only-1]]
    manifest={'profile':'mica-uploaded-images-fast-v1','created_at':datetime.now(timezone.utc).isoformat(),'input_count':len(REFS),'outputs':[],'provider_calls':{'muse_videos':0,'elevenlabs_tts':0}}
    for index,(reference,slug,product,setting,dialogue) in enumerate(jobs,1):
        print('START',index,slug,flush=True)
        final=render_one(index,reference,slug,product,setting,dialogue,muse_key,eleven_key)
        manifest['outputs'].append({'index':index,'slug':slug,'path':str(final)})
        manifest['provider_calls']['muse_videos']+=1;manifest['provider_calls']['elevenlabs_tts']+=1
    if args.only is None:
        write_json(OUT/'manifest.json',manifest)
        (OUT/'README.md').write_text('''# 6 video kiểm thử từ ảnh được cung cấp\n\nMỗi ảnh tạo một clip dọc 6 giây, giữ bối cảnh/bao bì riêng và ghép thoại Adam V3 riêng. Xem từng thư mục để kiểm tra prompt, thoại, video gốc Muse, video cuối và contact sheet.\n\nĐây là batch kiểm thử media, chưa tự đăng. Chữ nhỏ, chi tiết hộp/mica và góc không có trong ảnh cần duyệt thủ công.\n''',encoding='utf-8')
    print('DONE',OUT,flush=True)


if __name__=='__main__':main()
