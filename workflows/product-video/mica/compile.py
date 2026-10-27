"""Compile the user's mica image/video prompts offline. No API calls."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

SCENES = [
    ('mall', 'trung tâm thương mại', 'không gian trung tâm thương mại sáng, hành lang và cửa kính trống không thương hiệu', 'hộp mica chữ nhật góc bo nhỏ, quai cầu trong suốt liền mạch, chân đế mica mỏng', 'hồng nude'),
    ('appliance-store', 'siêu thị gia dụng/điện máy', 'siêu thị gia dụng/điện máy với kệ gọn gàng, vật trưng bày mờ không logo hay nhãn đọc được', 'hộp mica chữ nhật cạnh thẳng, quai vòm oval trong suốt, đế mỏng viền bạc trung tính không chữ', 'đỏ rượu vang'),
    ('factory', 'xưởng sản xuất', 'lối đi xưởng sản xuất sạch, khu lắp ráp yên phía sau, không biển hiệu hay logo, không vận hành máy sát người cầm', 'hộp mica khối chữ nhật tinh gọn với quai vòm rộng trong suốt và đế mỏng trắng ngà', 'be sữa'),
]

IMAGE_PROMPT = '''Tạo MỘT ảnh chân thực dọc 9:16, mục tiêu 2160 × 3840 pixel. Đây là ảnh {image_order}/{image_total} của sản phẩm {product_order}, bối cảnh {scene_name}. Không collage, không chia ô, không trộn với sản phẩm khác.
Nguồn nhận diện duy nhất của sản phẩm này: {reference}. Tên được cấp: {name}. Đặc điểm được cấp: {description}.
ƯU TIÊN NHẬN DIỆN: giữ đúng hình dáng, tỷ lệ, màu, vật liệu, logo, từng chữ, nút, màn hình và số, nắp, cổng, đường viền, phụ kiện và số lượng như ảnh tham chiếu. Không tự thiết kế lại, thêm hay bớt. Không lấy tên hoặc chi tiết của sản phẩm khác.
Đặt đúng sản phẩm đó trong {box}. Hộp mica sáng trong, vừa vặn, đế mỏng hợp lý chịu lực, không xuyên cắt hay làm méo sản phẩm. Vật bên trong cố định tương đối với hộp.
Một cẳng tay nữ TRƯỞNG THÀNH đi NGANG vào từ cạnh {arm_side} khung hình. Chỉ thấy một bàn tay và đoạn cẳng tay, móng sơn {nails}; cổ tay ở tư thế tự nhiên, bàn tay nắm chắc quai và nâng cả hộp lơ lửng trước camera ở độ cao ngang ngực của người cầm ngoài khung. Không mặt, tóc, thân, chân hoặc phản chiếu của người. Không tay thừa hoặc ngón thừa. Không đưa tay từ trên xuống. Thấy nguyên quai, hộp và đáy; hộp không chạm bàn, sàn, bục hoặc bất kỳ giá đỡ nào.
Hộp ở giữa, chiếm 55–65% chiều cao ảnh, mặt trước gần song song camera, còn tối thiểu 8% khung trống dưới đáy và 5% phía trên quai/hai cạnh. Camera nhìn ngang, không cắt quai hoặc đáy. Phần sản phẩm luôn rõ nét; hậu cảnh là {background}, mờ nhẹ để vẫn nhìn ra đúng không gian. Ánh sáng trắng trung tính, màu thật, mica phản xạ nhẹ không lóa che sản phẩm.
Nhãn tên và tính năng ở vùng chân/cạnh hộp được dành riêng, nền nhãn gọn, không đè lên sản phẩm; dùng đầy đủ CHÍNH XÁC nội dung sau, giữ dấu tiếng Việt và thứ tự:
{label_text}
Không thêm claim. Không logo/tên hãng/biển quảng cáo trên toàn bộ hậu cảnh hoặc hàng hóa phụ; GIỮ logo gốc trên sản phẩm chính và nhãn hộp. Không watermark. {staging}'''

LOCK = '''KHÓA NHẬN DIỆN VÀ KHUNG: Dùng đúng ảnh opening của chính clip này; giữ sản phẩm, hộp mica, quai, số lượng, logo, từng chữ/nhãn, số hiển thị, tỷ lệ, màu móng, phía tay vào và hậu cảnh. Hộp cứng, sản phẩm không trượt bên trong; mặt hộp luôn hướng camera, không xoay lật, không orbit rộng, không thay background. Thấy trọn quai và đáy, khoảng trống dưới đáy tối thiểu 8% chiều cao; không mặt/thân/phản chiếu người, không đặt hộp lên mặt đỡ. Không rung giật, biến dạng, chữ trôi, thêm props/chữ hoặc watermark. Không nhạc/thoại/hiệu ứng âm thanh; voice-over ghép riêng nếu được yêu cầu.'''
PACE = '''NHỊP: Video POV 9:16 dài 6 giây. Hành động xuất hiện từ giây đầu, tốc độ đời thường dứt khoát và có chủ đích; hoàn toàn không slow-motion. Camera có chuyển động theo hành động, hậu cảnh tạo parallax rõ; không rung quá đà. Không giữ gần đứng hình nhiều giây. Chuyển động bàn tay/quai và trọng lực phải liền mạch, có tăng/giảm tốc ngắn tự nhiên.'''

# Every action includes observable timing; a larger camera orbit is intentionally
# excluded because the user's held box must keep its front facing the viewer.
ACTIONS = [
    {'id':11,'title':'Bước qua cửa hàng','requires':['doorway'], 'hands':1,
     'action':'0–0,3s bắt đầu bước ngay; 0,3–4,8s đi 3–4 bước tự nhiên, dứt khoát qua đúng lối cửa có trong ảnh, camera theo nhịp bước, hậu cảnh trôi rõ. Hộp nhún theo bước khoảng 1–3 cm, không lắc mạnh; cổ tay bù để mặt hộp hướng camera. 4,8–6s tiếp tục đi thêm một bước ổn định, không dừng tạo dáng. Không thêm cửa mới.'},
    {'id':12,'title':'Dừng lại quan sát','requires':[], 'hands':1,
     'action':'0–3,5s đi ngay 2–3 bước rõ ràng với nhún hộp nhỏ theo bước; 3,5–4,5s dừng chân tự nhiên. 4,5–5,3s hộp đung đưa một nhịp nhỏ giảm dần, camera ổn định theo. 5,3–6s giữ chắc để thấy sản phẩm; không phóng đại dao động hoặc đứng yên phần lớn clip.'},
    {'id':13,'title':'Chuyển hộp sang giữa khung hình','requires':[], 'hands':1,
     'action':'Nếu ảnh mở đầu đã giữa khung, 0–1,2s chuyển hộp sang phải khoảng 8–10% bề ngang khung, vẫn thấy trọn hộp; nếu đã hơi lệch phải thì bắt đầu ngay bước tiếp. 1,2–3,2s đưa hộp ngang về chính giữa với cổ tay tự nhiên, không xoay hộp. 3,2–5,5s camera tiến một nhịp nhỏ khoảng 5% để thấy rõ hơn, vẫn dư khung; 5,5–6s ổn định. Không đứng yên chờ chuyển động.'},
    {'id':14,'title':'Hạ hộp nhẹ xuống','requires':[], 'hands':1,
     'action':'0–0,3s bắt đầu hạ ngay; 0,3–2s hạ cả hộp khoảng 8–10 cm bằng cẳng tay, không đổi chiều dài quai hay hình hộp. Giữ đáy trong khung với khoảng trống. 2–4,8s camera lùi một bước ngắn hoặc mở khoảng cách nhẹ để giữ trọn hộp, góc nhìn vẫn ngang; 4,8–6s bàn tay nắm chắc cho hộp ổn định. Không chĩa xuống đất hay chạm mặt đỡ.'},
    {'id':15,'title':'Đi ngang kệ trưng bày','requires':['shelf'], 'hands':1,
     'action':'0–0,3s bắt đầu bước; 0,3–5,5s đi ngang 3–4 bước qua kệ hàng có sẵn, tốc độ đi bình thường dứt khoát. Hậu cảnh trôi ngang rõ, camera đi cùng tay cầm; hộp giữ ở giữa, mặt hộp hướng camera, nhún nhỏ theo chân. 5,5–6s vẫn chuyển động, không dừng lâu. Không sinh thêm thương hiệu/biển quảng cáo trên kệ.'},
    {'id':16,'title':'Camera lùi một bước','requires':[], 'hands':1,
     'action':'Một shot do người đứng đối diện giữ camera quay ngang ngực, chỉ tay người cầm xuất hiện. Tay giữ hộp ổn định ở vị trí cũ trong không gian; 0–2,5s camera lùi một bước khoảng 30–40 cm theo trục thẳng, bù góc nhìn để hộp còn giữa khung. 2,5–5,5s camera dịch ngang rất nhỏ 5–10 cm, tay bù tư thế để mặt hộp luôn hướng camera; 5,5–6s ổn định. Hộp thu nhỏ theo phối cảnh tự nhiên, không scale riêng sản phẩm hoặc biến độ dài tay.'},
    {'id':17,'title':'Bước chéo sang trái','requires':['left_clearance'], 'hands':1,
     'action':'0–2s người cầm bước chéo trái một bước rõ khoảng 30–40 cm trong đúng lối đi; camera theo cùng chuyển động, hộp giữ giữa và thẳng mặt camera. 2–4,8s bước tiếp một nhịp ngắn về phía trước để hậu cảnh đổi góc tự nhiên. 4,8–6s ổn định dần với nhún nhỏ; không lắc mạnh hoặc xoay hộp, không thêm lối đi mới.'},
    {'id':18,'title':'Tay chỉnh lại quai xách','requires':[], 'hands':2,
     'action':'Tay thứ nhất giữ quai từ đầu đến cuối, không buông hoặc đổi tay. 0,3–1,5s tay thứ hai đi ngang vào từ mép đối diện; 1,5–3s đặt ngón tay nhẹ lên phần quai còn trống và chỉnh vị trí nắm một đoạn rất nhỏ, không bẻ quai, không đẩy ngón tay xuyên tay chính. 3–4s tay thứ hai rút hết ra. 4–5,5s camera tiến khoảng 5%, giữ trọn quai/đáy; 5,5–6s ổn định. Hộp luôn được nâng chắc.'},
    {'id':19,'title':'Đưa hộp ngang cửa kính','requires':['glass_door'], 'hands':1,
     'action':'0–0,3s đi ngay; 0,3–5,5s đi 3 bước bình thường ngang đúng khu cửa kính có sẵn, hậu cảnh dịch ngang thấy rõ. Camera đi cùng người cầm, mặt hộp giữ hướng lens; ánh trắng và phản xạ mica thay đổi nhẹ có lý do theo vị trí, không lóe sáng giả. 5,5–6s còn chuyển động ổn định. Không tạo cửa kính/cảnh mới hay phản chiếu mặt người.'},
    {'id':20,'title':'Bước đi rồi chỉ sản phẩm','requires':[], 'hands':2,
     'action':'0–4s tay chính xách hộp đi ngay 3 bước rõ, camera theo chân, hộp nhún nhỏ và vẫn thẳng mặt lens. 4–4,3s dừng gọn; 4,3–4,8s tay thứ hai vào từ cạnh đối diện, ngón trỏ hướng vào sản phẩm qua khoảng mica trống mà không che logo/chữ. 4,8–5,3s chỉ ngắn rồi 5,3–6s rút tay ra. Tay chính luôn giữ quai; không chạm/kích hoạt nút hoặc buông hộp.'},
]


def image_prompt(product, scene, order, total, index):
    slug,name,background,box,nails=scene
    staging=product.get('scene_staging',{}).get(slug,'')
    return IMAGE_PROMPT.format(image_order=order,image_total=total,product_order=index,reference=product['reference_image'],name=product['name'],description=product.get('description','Chỉ dựa vào ảnh tham chiếu, không suy diễn tính năng.'),scene_name=name,box=box,nails=nails,arm_side=product.get('arm_side','phải'),background=background,label_text='\n'.join([product['name']]+product['features']),staging=staging)


def video_prompt(action):
    hands=('Đúng MỘT tay nữ trưởng thành giữ quai; không có tay thứ hai.' if action['hands']==1 else 'Tối đa ĐÚNG HAI tay nữ trưởng thành: một tay giữ quai liên tục, tay phụ chỉ vào làm động tác đã chỉ định rồi rút ra. Không có tay thứ ba; mỗi tay đúng giải phẫu.')
    return '\n\n'.join([f"PROMPT {action['id']} — {action['title']}",PACE,action['action'],hands,LOCK])


def library_text():
    intro='''# Prompt mica v2 — nhịp rõ, 6 giây

Đây là bản phát triển từ bộ gốc, chưa phải kết quả tạo ảnh/video. Dùng mẫu ảnh với tên/tính năng đã được cấp; xem WORKFLOW.md về độ chính xác sản phẩm, chữ và đo 4K.

## Ảnh mở đầu — template

'''
    return intro+IMAGE_PROMPT+'\n\n## Video — 10 prompt đầy đủ\n\n'+'\n\n---\n\n'.join(video_prompt(a) for a in ACTIONS)+'\n'


def validate_config(config):
    products=config.get('products')
    if not isinstance(products,list) or not products: raise ValueError('products must be a non-empty ordered list')
    ids=set()
    for product in products:
        for key in ['id','name','reference_image','features']:
            if key not in product: raise ValueError('Missing product field: '+key)
        if not isinstance(product['id'],str) or not product['id'] or Path(product['id']).name!=product['id'] or product['id'] in {'.','..'}:
            raise ValueError('Product id must be a simple unique folder name')
        if product['id'] in ids: raise ValueError('Duplicate product id')
        ids.add(product['id'])
        if not isinstance(product['features'],list) or any(not isinstance(v,str) or not v.strip() for v in product['features']):
            raise ValueError('features must be a list of supplied non-empty strings; [] means no claims supplied')
        if product.get('arm_side','phải') not in ['phải','trái']: raise ValueError('arm_side must be phải or trái')
    chosen=config.get('selected_video_prompts',[])
    if not isinstance(chosen,list) or len(chosen)!=len(set(chosen)) or any(type(i)!=int or i not in range(11,21) for i in chosen):
        raise ValueError('selected_video_prompts must contain unique ids 11..20; [] compiles images only')
    for caps in config.get('capabilities',{}).values():
        if not isinstance(caps,list) or any(v not in ['doorway','glass_door','shelf','left_clearance'] for v in caps):
            raise ValueError('Unknown scene capability')


def compile_pack(config,output,config_dir=None):
    validate_config(config)
    output=Path(output)
    if output.exists():raise ValueError('Output exists; select a new directory to keep versions separate')
    output.mkdir(parents=True)
    total=len(config['products'])*3
    jobs=[];images=[];skipped=[]
    for pindex,product in enumerate(config['products'],1):
        for sindex,scene in enumerate(SCENES,1):
            slug=scene[0];order=(pindex-1)*3+sindex
            directory=output/f'{pindex:03}-{product["id"]}'/f'{sindex:02}-{slug}'
            directory.mkdir(parents=True)
            (directory/'image-prompt.txt').write_text(image_prompt(product,scene,order,total,pindex),encoding='utf-8')
            (directory/'label.txt').write_text('\n'.join([product['name']]+product['features']),encoding='utf-8')
            save={'type':'image','order':order,'product_id':product['id'],'reference_image':product['reference_image'],'scene':slug,'target_size':[2160,3840],'opening_image':str((directory/'opening.png').relative_to(output))}
            images.append(save)
            caps=product.get('capabilities',{}).get(slug,config.get('capabilities',{}).get(slug,[]))
            for action in ACTIONS:
                if action['id'] not in config.get('selected_video_prompts',[]):continue
                missing=sorted(set(action['requires'])-set(caps))
                if missing:
                    skipped.append({'product_id':product['id'],'scene':slug,'prompt_id':action['id'],'missing_capabilities':missing})
                    continue
                filename=f'video-{action["id"]}.txt'
                (directory/filename).write_text(video_prompt(action),encoding='utf-8')
                jobs.append({'type':'video','product_id':product['id'],'scene':slug,'prompt_id':action['id'],'seconds':6,'max_hands':action['hands'],'opening_image':save['opening_image'],'prompt_file':str((directory/filename).relative_to(output))})
    report={'profile':'mica-pov-v2','status':'prompts_only_not_generated','input_products':len(config['products']),'image_count':len(images),'expected_images':total,'image_order':images,'selected_video_count':len(jobs),'selected_video_seconds':sum(j['seconds'] for j in jobs),'video_jobs':jobs,'skipped':skipped,'provider_calls_made':0,'configured_video_prompts':config.get('selected_video_prompts',[]),'capability_note':'Capabilities are user/agent declarations; re-check generated opening before any video generation.','quality_note':'Identity locks are targets; generated pixels/text/geometry require inspection. Native 4K must be measured, upscale disclosed.'}
    (output/'plan.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    (output/'source-config.json').write_text(json.dumps(config,ensure_ascii=False,indent=2),encoding='utf-8')
    (output/'optimized-prompts.md').write_text(library_text(),encoding='utf-8')
    return report


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config')
    parser.add_argument('--output')
    parser.add_argument('--library',help='Write only the complete reusable prompt library to this file')
    args=parser.parse_args()
    if args.library:
        path=Path(args.library);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(library_text(),encoding='utf-8');print('Prompt library saved:',path)
    if args.config:
        if not args.output:parser.error('--output required with --config')
        config=json.loads(Path(args.config).read_text(encoding='utf-8-sig'))
        result=compile_pack(config,args.output)
        print(json.dumps({k:result[k] for k in ['input_products','image_count','selected_video_count','provider_calls_made','status']},ensure_ascii=False))
    elif not args.library:parser.error('Provide --library or --config and --output')


if __name__=='__main__':main()
