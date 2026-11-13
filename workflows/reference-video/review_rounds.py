"""Sequential, reviewable editorial revisions; existing batches remain intact."""
import argparse,copy,hashlib,html,json,os,shutil,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
import documentary as core
import editorial

ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/'videos/2026-11-11-lang-kinh-editorial-v2'
OUT=ROOT/'videos/2026-11-11-ten-pass-review'
EDITS=[
 ('Màu tổng thể','Cảnh cảng xanh lạnh, cảnh đêm vàng gắt, độ sáng thiếu nhất quán.','Giảm độ bão hòa nhẹ, cân xanh/đỏ và giữ vùng da trung tính.'),
 ('Minh họa xưởng may','Lời nói xưởng may nhưng hình là refinery, bàn phím và phòng thí nghiệm.','Thay hai đoạn ví dụ bằng video thật kim may/vải, giữ voice.'),
 ('Nghĩa của nhãn thương mại','Nhãn hàng bán/mua đặt lên laptop và văn phòng không mô tả trực tiếp thương mại.','Hai nguồn cảng chuyển động, nhãn rõ xuất/nhập; ghi đây là minh họa.'),
 ('Căn hình với lời','Các đoạn cắt theo 3,5/4/5 giây làm câu chuyển ý lệch hình.','Cắt tại mốc câu từ alignment đúng take, tổng vẫn 1500 frame.'),
 ('Giảm phần che hình','Panel giấy ngà che gần 40% khung trong đoạn công nghệ/thương hiệu.','Thu panel và chữ để thấy thêm footage, giữ vùng subtitle riêng.'),
 ('Dễ đọc phụ đề','Chữ nhỏ khi xem cửa sổ và một số caption có hai ý trong cùng cụm.','Tăng chữ, rút độ dài cụm; không tạo thẻ một từ.'),
 ('Chọn hình cho giá trị giữ lại','Cận mắt kính và bàn phím chung chung trong đoạn câu hỏi về giá trị.','Đổi sang hoạt động thương mại và tài khoản tài chính; giữ inset để đa dạng.'),
 ('Nhịp thở và nhận diện','Badge xuất hiện dày, một cảnh split quá ngắn khi căn lời.','Cho một cảnh full-screen không badge, bớt nhận diện lặp ở các cảnh phụ.'),
 ('Căn sound theo ý','Cue âm thanh cũ theo mốc cố định có thể lệch sau khi cắt hình.','Đặt cue theo điểm câu/điểm cắt mới, giữ hiệu ứng dưới giọng.'),
 ('Hoàn thiện và sàng lọc','Luận điểm năng suất trên cảnh cảng sáng thiếu nền đỡ chữ; cần so toàn bộ.','Thêm backplate cục bộ, thống nhất màu giấy/amber dịu, kiểm tra 50s và chọn bản cuối.'),
]

def link_tree(src,dst):
    dst.mkdir(exist_ok=True)
    for p in src.iterdir():
        if not p.is_file():continue
        target=dst/p.name
        if target.exists():continue
        # Only immutable originals are linked. Mutable rendered shots are copied.
        try:os.link(p,target)
        except OSError:shutil.copy2(p,target)

def setup(n):
    prev=SOURCE if n==1 else OUT/f'round-{n-1:02}'
    b=OUT/f'round-{n:02}';b.mkdir(parents=True,exist_ok=True)
    if (b/'review.json').exists():raise ValueError('Round already exists; inspect/resume it explicitly')
    d=copy.deepcopy(core.load(prev/'batch.json'));link_tree(SOURCE/'assets',b/'assets');link_tree(SOURCE/'audio',b/'audio');link_tree(OUT/'new-assets',b/'assets')
    if (prev/'shots').exists():shutil.copytree(prev/'shots',b/'shots',dirs_exist_ok=True)
    for name in ['asset-sources.json','fact-source-1.html','fact-source-2.html']:
        if (prev/name).exists():shutil.copy2(prev/name,b/name)
    if n==1:
        d['base_grade']='eq=brightness=-0.015:saturation=0.84:contrast=1.035,colorbalance=gm=-0.012:bm=-0.018:rm=0.006'
        for s in d['shots']:s.pop('grade',None)
    elif n==2:
        d['shots'][4].update(file='assets/mixkit-51012.mp4',style='full_bleed',purpose='Actual needle sewing fabric: explicit workshop analogy',**{'in':0})
        d['shots'][5].update(file='assets/mixkit-51013.mp4',purpose='Fabric and machinery while discussing bought inputs',**{'in':0})
        for k in ['secondary','tertiary']:d['shots'][4].pop(k,None)
        d['shots'][4]['grade']='eq=brightness=-0.005:saturation=0.73:contrast=1.025'
        d['shots'][5]['grade']=d['shots'][4]['grade']
        sources=core.load(b/'asset-sources.json');sources+=core.load(OUT/'new-asset-sources.json');core.save(b/'asset-sources.json',sources)
    elif n==3:
        d['shots'][3].update(file='assets/mixkit-4011.mp4',secondary='assets/mixkit-4450.mp4',secondary_in=2,labels=['XUẤT KHẨU','NHẬP KHẨU'],split_note='CẢNH MINH HỌA HOẠT ĐỘNG THƯƠNG MẠI')
    elif n==4:
        cuts=[0,5,7.5,12.9,16.3,19.4,26.3,28.2,35.1,39.8,45,50]
        for i,s in enumerate(d['shots']):s['seconds']=round(cuts[i+1]-cuts[i],3)
        d['shots'][2]['source_note']='Nguồn: Cục Thống kê / Báo Chính phủ · 03.11.2026'
    elif n==5:d['shots'][8].update(panel_width=650,panel_font=51)
    elif n==6:d.update(caption_font_size=47,caption_settings={'max_chars':54,'max_seconds':2.8,'break_sentences_always':True})
    elif n==7:
        d['shots'][7].update(file='assets/mixkit-4011.mp4',secondary='assets/mixkit-308.mp4',secondary_in=8,purpose='Trade turnover and financial accounts illustrate retained value',**{'in':12})
        d['shots'][8].update(file='assets/mixkit-4707.mp4',purpose='Actual equipment and trained operator for technology capability',**{'in':0})
        d['shots'][3].update(secondary_in=3,**{'in':5})
        d['shots'][9]['in']=11
        d['shots'][10]['in']=26
    elif n==8:
        d['shots'][6]['style']='full_bleed'
        for i in [3,6,7]:d['shots'][i]['hide_badge']=True
    elif n==9:
        for cue,at in zip(d['sound_effects'],[0,7.35,12.75,16.2,19.8,26.15,28.1,35,41.85,44.85]):cue['at']=at
        d['sound_effects'][0]['gain_db']=-18
        d['sound_effects'][4]['gain_db']=-26
        d['sound_effects'][4]['name']='tick' # Sewing replaced keyboard footage.
    elif n==10:
        d['shots'][9]['text_backplate']=True;d['brand']['palette'].update(paper='#F3EFE7',amber='#F1AE55')
    d['review_round']=n;d['parent_batch']=str(prev.relative_to(ROOT));core.save(b/'batch.json',d)
    title,problem,change=EDITS[n-1];core.save(b/'review.json',{'round':n,'focus':title,'problem':problem,'change':change,'parent':str(prev),'visual_review':'pending','decision':'pending','provider_calls':0})
    return b

def evidence(b):
    frames=core.run([core.FF,'-v','error','-i',str(b/'final.mp4'),'-vf','fps=1,scale=320:180','-pix_fmt','rgb24','-f','rawvideo','pipe:1']).stdout
    sheet=Image.new('RGB',(1600,10*204),'#171717');draw=ImageDraw.Draw(sheet);metrics=[]
    for i in range(50):
        arr=np.frombuffer(frames[i*172800:(i+1)*172800],dtype=np.uint8).reshape((180,320,3));im=Image.fromarray(arr);x=i%5*320;y=i//5*204;sheet.paste(im,(x,y+22));draw.text((x+4,y+3),str(i)+'s',fill='white')
        luma=arr@np.array([.2126,.7152,.0722]);metrics.append({'seconds':i,'mean_luma':round(float(luma.mean()),2),'near_black_fraction':round(float((luma<12).mean()),4),'near_white_fraction':round(float((luma>245).mean()),4)})
    sheet.save(b/'review-all.jpg',quality=91);core.save(b/'color-metrics.json',{'scope':'Descriptive measurements, not an aesthetic score. Source scene changes affect luma.','frames':metrics})
    # Large enough to inspect the focal change and its subtitle / adjacent context.
    n=core.load(b/'batch.json')['review_round'];times={1:[1,10,18,28,37,43],2:[16,18,20,22,24,25],3:[12,13,14,15,16,18],4:[5,8,13,17,27,29],5:[35,36,37,38,39,40],6:[8,14,19,24,31,48],7:[28,29,30,32,33,34],8:[13,26,27,28,31,33],9:[5,13,17,20,28,45],10:[1,10,18,31,37,43]}[n]
    detail=Image.new('RGB',(1920,3*566),'#171717');dd=ImageDraw.Draw(detail)
    for j,t in enumerate(times):
        raw=core.run([core.FF,'-v','error','-ss',str(t),'-i',str(b/'final.mp4'),'-frames:v','1','-vf','scale=960:540','-pix_fmt','rgb24','-f','rawvideo','pipe:1']).stdout
        im=Image.frombytes('RGB',(960,540),raw);x=j%2*960;y=j//2*566;detail.paste(im,(x,y+24));dd.text((x+5,y+4),str(t)+'s',fill='white')
    detail.save(b/'review-focus.jpg',quality=94)

def finish(selected):
    reports=[]
    for n in range(1,11):
        b=OUT/f'round-{n:02}';report=core.load(b/'review.json');verify=core.load(b/'verification.json')
        if report['decision']=='pending' or verify['decoded_video_frames']!=1500:raise ValueError('Every round must have reviewed output and exact frame count')
        verify.update(visual_review=report['visual_review'],user_acceptance='pending');core.save(b/'verification.json',verify)
        report.update(video=f'round-{n:02}/final.mp4',sha256=hashlib.sha256((b/'final.mp4').read_bytes()).hexdigest(),duration=verify['container_seconds'],audio_levels=verify['audio_levels'],selection='selected_final' if n==selected else 'retained_intermediate');reports.append(report)
    if len({r['sha256'] for r in reports})!=10:raise ValueError('Iterations must be distinct outputs')
    shutil.copy2(OUT/f'round-{selected:02}/final.mp4',OUT/'final.mp4')
    core.save(OUT/'summary.json',{'selected_round':selected,'rounds':reports,'provider_calls':0,'scope':'Each full output decoded; visual review uses full-duration sampled frames and enlarged focal sheets, not a claim of continuous audiovisual viewing.'})
    lines=['# Đánh giá và làm lại 10 vòng','',f'Bản được chọn: vòng {selected:02}, 50 giây / 1500 frame / 1920×1080. Giữ cả 10 bản và bản gốc. Không gọi thêm TTS/SFX provider.','', 'Tiêu chí chọn: đúng nghĩa của lời, cảnh thật có chuyển động, màu không ám quá mức, chữ không che ý chính, cắt theo câu, giữ trọn lời kết. Phần đánh giá thẩm mỹ là nhận xét từ khung mẫu và khung lớn; thông số luma không phải điểm chất lượng.','']
    cards=[]
    for r in reports:
        n=r['round'];obs=r['visual_review']['observation'];lines += [f"## Vòng {n:02} — {r['focus']}",'',f"Lỗi: {r['problem']}",f"Thay đổi: {r['change']}",f"Quan sát: {obs}",f"Bản xuất: [MP4](round-{n:02}/final.mp4) · [Khung đánh giá](round-{n:02}/review-focus.jpg)",'']
        cards.append(f'<article><h2>Vòng {n:02} · {html.escape(r["focus"])}</h2><p>{html.escape(obs)}</p><video controls preload="none" src="round-{n:02}/final.mp4"></video><p><a href="round-{n:02}/review-focus.jpg">Khung đánh giá</a> · <a href="round-{n:02}/review.json">Ghi chú</a></p></article>')
    (OUT/'REVIEW_SUMMARY.md').write_text('\n'.join(lines),encoding='utf-8')
    (OUT/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>10 vòng Lăng Kính</title><style>body{background:#151c25;color:#f3efe7;font:17px system-ui;max-width:1100px;margin:40px auto;padding:0 24px}a{color:#f1ae55}article{padding:24px 0;border-top:1px solid #445}video{width:100%;max-height:620px}p{line-height:1.6}</style><h1>10 vòng đánh giá · Lăng Kính / Tyranno</h1>'+f'<p>Đề xuất chọn vòng {selected:02}. 50 giây, giữ nguyên voice take ElevenLabs, không phát sinh provider calls.</p><video controls src="final.mp4"></video><p><a href="REVIEW_SUMMARY.md">Báo cáo đầy đủ</a></p>'+''.join(cards),encoding='utf-8')
    print('TEN_REVIEWED_EXPORTS_SELECTED',selected,flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('stage',choices=['run','evidence','review','finish']);p.add_argument('--round',type=int,required=True);p.add_argument('--note');a=p.parse_args()
    if not 1<=a.round<=10:raise ValueError('Round must be 1..10')
    if a.stage=='finish':finish(a.round);sys.exit(0)
    b=setup(a.round) if a.stage=='run' else OUT/f'round-{a.round:02}'
    if a.stage=='review':
        if not a.note:raise ValueError('An observed review note is required')
        report=core.load(b/'review.json');report.update(visual_review={'scope':'sampled frames across duration plus enlarged focal contact sheet','observation':a.note},decision='keep_for_next_round',technical=core.load(b/'verification.json')['full_decode']);core.save(b/'review.json',report);print('REVIEW_SAVED',a.round);sys.exit(0)
    if a.stage=='run':editorial.render(b);editorial.qa(b)
    evidence(b);print('ROUND_READY',a.round,flush=True)
