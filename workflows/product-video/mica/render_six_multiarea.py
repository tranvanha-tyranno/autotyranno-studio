"""Resumable six-reference, 20-second multi-area batch using existing provider helpers."""
import argparse
import hashlib
import json
import shutil
import time
from pathlib import Path
from product_video_mica_compat import load_runner

r = load_runner()
ROOT = r.PROJECT
BATCH = ROOT/'videos/2026-10-28-six-mica-multiarea-20s'
REFS = [
 ('aea51831-0ba6-4c94-a707-b135a065f0d7', 'inox-factory', 'right', 'terracotta', 'clear acrylic', 'factory production aisle', 'factory quality-inspection aisle', 'factory packing and dispatch aisle'),
 ('e7dc5cf7-8c86-4856-8d48-c2e7cb21a495', 'inox-mall', 'right', 'pink', 'gold-trimmed acrylic', 'mall atrium', 'mall upper-floor gallery', 'mall bright storefront corridor'),
 ('fcb79c98-6d92-4b8c-8f85-e5c0d0586f6a', 'inox-store', 'left', 'burgundy', 'clear acrylic with chrome handle', 'appliance-store kettle aisle', 'appliance-store lighting display aisle', 'appliance-store wide checkout approach'),
 ('3b99d1fe-04a1-43c5-bbf7-21b861548824', 'oral-factory', 'left', 'burgundy', 'clear acrylic', 'factory assembly aisle', 'factory quality-control corridor', 'factory clean packing aisle'),
 ('1d5315b3-bd66-447f-b11d-47e83aaa0dd9', 'oral-mall', 'left', 'pink', 'clear acrylic', 'mall gallery', 'mall skylit atrium walkway', 'mall upper-floor shop corridor'),
 ('25171d51-d048-42b2-87ec-7b7d1bf33f39', 'oral-store', 'right', 'brown', 'clear acrylic with chrome handle', 'appliance-store display aisle', 'appliance-store personal-care display area', 'appliance-store bright front gallery'),
]
DIALOGUES = [
 '[excited] Ê ê ê, xách một vòng xưởng mà em ấm này vẫn nổi bật ghê! [playful] Thân inox sáng, dung tích một phẩy tám lít, tay cầm đen nhìn gọn gàng. Nhãn còn ghi tự ngắt khi nước sôi và đế xoay ba trăm sáu mươi độ. Mấy ní xem kỹ thông tin trước khi chọn nha!',
 '[playful] Các dợ ơi, đi dạo trung tâm thương mại mà cứ tưởng đang xách quà! [excited] Bên trong là ấm inox một phẩy tám lít, vòi rót gọn, tay cầm cách nhiệt theo thông tin trên nhãn. Hộp trong veo nên nhìn được cả nắp lẫn đế. Thích kiểu này thì ghé xem chi tiết nha!',
 '[curious] Mấy ní nhìn một vòng xem em ấm này có hợp góc bếp không? [playful] Thân bạc, nắp đen, tay cầm to, bên dưới có đèn báo đỏ. Nhãn ghi một phẩy tám lít, có nút mở nắp và đế xoay. Cần một chiếc ấm gọn gàng thì tham khảo thêm nha!',
 '[excited] Ê ê ê, nguyên bộ chăm răng nằm gọn trong hộp luôn nè! [playful] Máy tăm nước xanh bạc hà, các đầu thay, dây sạc và túi đựng đều nhìn thấy rõ. Trên máy có ba chế độ để tham khảo. Mấy ní nhớ xem hướng dẫn và thông số đúng mẫu trước khi chọn nha!',
 '[playful] Đi dạo mà xách nguyên bộ tăm nước, nhìn cũng ra dáng quà ghê ha! [excited] Máy xanh nhạt, bình trong, đầu thay, dây USB và túi vải xếp từng ngăn. Nhìn một lượt là thấy phụ kiện đi kèm. Mấy ní thích bộ gọn gàng thì ghé xem thông tin chi tiết nha!',
 '[curious] Một chiếc hộp mà xếp gọn được từng này món luôn hả mấy ní? [excited] Máy tăm nước, đầu thay, dây sạc và túi đựng có ngăn riêng nhìn rất dễ kiểm tra. Mặt máy ghi ba chế độ, bình nước trong thấy rõ bên dưới. Chọn đúng mẫu và đọc hướng dẫn trước khi dùng nha!',
]

def prepare():
    if (BATCH/'batch.json').exists():
        return r.read_json(BATCH/'batch.json')
    (BATCH/'input').mkdir(parents=True, exist_ok=False)
    clips=[]
    for i, (uid, slug, side, nails, box, *areas) in enumerate(REFS, 1):
        source=Path.home()/'AppData/Local/Temp'/f'codex-clipboard-{uid}.png'
        ref=BATCH/'input'/f'{i:02}-{slug}.png'
        shutil.copy2(source, ref)
        path=BATCH/f'clip-{i:02}-{slug}'; path.mkdir()
        shutil.copy2(ref,path/'opening.png')
        (path/'dialogue.txt').write_text(DIALOGUES[i-1],encoding='utf-8')
        product=('silver stainless-steel electric kettle, black handle and lid, red indicator and all Vietnamese labels, 1.8L' if i<=3 else 'mint-green oral irrigator, transparent reservoir, four spare tips, black USB cable, brown fabric pouch, all exact labels and their original capacity numbers')
        prompts=[]
        for n,area in enumerate(areas,1):
            location=(f'Remain in the reference {area}, walking past its existing fixtures.' if n==1 else f'Begin from the reference image for identity, then at 0.3 seconds make ONE crisp editorial match cut to a distinct {area} in the same venue. Keep the held box identical across the cut. Do not dissolve or morph the environment. Continue moving immediately after the cut.')
            motion=[
                '0.0-0.3s start walking immediately; 0.3-4.5s walk four purposeful normal steps forward as camera tracks backward; 4.5-9.7s continue along the aisle with clear moving background parallax, 9.7-10s keep walking.',
                '0-0.3s move immediately; after the location cut, 0.3-5s walk four lateral steps past the displays while camera tracks parallel; 5-10s carry on moving with a small natural lift of the forearm, always keeping the complete box visible.',
                '0-0.3s move immediately; after the location cut, 0.3-6s walk diagonally forward along the clear aisle while the camera tracks back; 6-9.5s bring the suspended box a little closer by a natural arm movement, camera compensates to show the whole box; final pause at most 0.5s.'
            ][n-1]
            prompt=f'''Generate a photorealistic 10-second vertical 9:16 image-to-video shot. Shot {n} of a brisk product showcase, not slow motion. {location}
ACTION TIMING: {motion} Action must be clearly visible from the first 0.3 seconds. Real walking and real scene parallax, not a digital zoom on a still image.
IDENTITY: Use ONLY this supplied image for the foreground: preserve the exact {product}; preserve the {box} case, handle material, hinges, rigid geometry, component positions, original printed text and all packaging. Nothing inside moves independently. Keep the original adult woman's single hand with {nails} nails; forearm enters horizontally from frame {side}, same side throughout. One hand only, five anatomically correct fingers. No face, torso, person reflection or second hand. Background people must remain indistinct and not become presenters.
FRAMING: Box always suspended by its handle, front aimed squarely toward camera. No rotation, orbit, flip, placing down, opening the case or activating the device. Natural small 1-3cm walking bob, wrist compensates. Keep entire handle, box and bottom in frame with margin below and at the sides. Camera may step back early to protect framing. Product remains sharp and central; realistic moving soft background, neutral exposure, no glare obscuring labels.
No additional products, missing accessories, changing letters, new claims, captions, logos, watermark, new props, artificial light flashes, music, speech or sound effects. Never freeze, loop or pad. Preserve foreground appearance over unnecessary movement. Distinct unbranded background area: {area}.'''
            (path/f'scene-{n:02}-prompt.txt').write_text(prompt,encoding='utf-8'); prompts.append(prompt)
        clips.append({'slug':slug,'dialogue':DIALOGUES[i-1],'background':areas,'presenter':f'{side} hand, {nails} nails','presentation_mode':'hands_only','shot_prompts':prompts,'reference':str(ref.relative_to(BATCH)),'reference_sha256':hashlib.sha256(ref.read_bytes()).hexdigest()})
    cfg={'profile':'mica-user-override-20s-multiarea','duration_seconds':20,'scene_count':3,'visual_speed':1.5,'cache':{'muse':True,'tts':True},'product_description':'Six independent supplied held-box references in upload order','clips':clips}
    r.save_json(BATCH/'batch.json',cfg)
    return cfg

def main():
    ap=argparse.ArgumentParser();ap.add_argument('stage',choices=['plan','voices','videos','render','watch-render','report']);ap.add_argument('--clip',type=int);ap.add_argument('--scene',type=int);a=ap.parse_args()
    cfg=prepare(); selected=[(i,c) for i,c in enumerate(cfg['clips'],1) if not a.clip or i==a.clip]
    if a.stage=='report':
        cards=[];reports=[]
        for i,c in selected:
            p=r.clip_path(BATCH,i,c)
            reports.append(r.read_json(p/'verification.json'))
            cards.append(f'<article><h2>{i:02} — {c["slug"]}</h2><video controls preload="metadata" poster="{p.name}/opening.png" src="{p.name}/final.mp4"></video><p><a href="{p.name}/verification.json">QA report</a></p></article>')
        html='''<!doctype html><meta charset="utf-8"><title>6 video sản phẩm — 20 giây</title><style>body{background:#111;color:#eee;font:16px system-ui;margin:32px}main{display:grid;grid-template-columns:repeat(3,minmax(220px,1fr));gap:24px}video{width:100%;max-height:75vh;background:#222}a{color:#7cf}h2{font-size:18px}@media(max-width:800px){main{grid-template-columns:1fr}}</style><h1>6 video riêng — mỗi video 20 giây</h1><p>Ba cảnh mới mỗi video, hình 1,5×, giọng Adam V3. AI có thể làm thay đổi chữ nhỏ, chi tiết hộp và nền; xem QA từng bản.</p><main>'''+''.join(cards)+'</main>'
        (BATCH/'index.html').write_text(html,encoding='utf-8')
        r.save_json(BATCH/'verification-summary.json',{'outputs':reports,'completed':len(reports),'provider_video_calls':18,'tts_calls':6,'published':False})
        print('REPORT READY',BATCH,flush=True)
        return
    if a.stage=='plan':
        r.warm_cache(BATCH,cfg)
        r.plan(BATCH,cfg,selected)
        return
    for i,c in selected:
        path=r.clip_path(BATCH,i,c)
        if a.stage=='watch-render':
            while not all((path/f'scene-{n:02}-contact-sheet.jpg').exists() for n in range(1,4)):
                time.sleep(10)
            if not (path/'final.mp4').exists():r.render(BATCH,cfg,i,c)
        if a.stage=='voices': r.voice(BATCH,cfg,i,c)
        if a.stage=='videos':
            for n,prompt in enumerate(c['shot_prompts'],1):
                if a.scene and a.scene!=n:continue
                target=path/f'scene-{n:02}.mp4'
                r.task_media(BATCH,cfg,path,target,'/v1/videos',{'prompt':prompt,'duration':10,'size':'9:16','resolution':'720p','reference_image':r.image_url(path/'opening.png')})
                if r.duration(target)<9.96:raise RuntimeError('Provider returned insufficient footage; no padding permitted')
                r.run_ff([r.FF,'-y','-i',str(target),'-vf','fps=1,scale=180:320,tile=5x2','-frames:v','1',str(path/f'scene-{n:02}-contact-sheet.jpg')])
        if a.stage=='render': r.render(BATCH,cfg,i,c)

if __name__=='__main__':main()
