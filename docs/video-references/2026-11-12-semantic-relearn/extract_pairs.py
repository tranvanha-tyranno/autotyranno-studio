from pathlib import Path
import json, cv2
from PIL import Image, ImageDraw, ImageFont
B=Path(__file__).parent
B.mkdir(parents=True,exist_ok=True)
rows=[]
def add(channel,video,t,phrase,meaning):
    rows.append({'channel':channel,'videoId':video,'frameTime':t,'phrase':phrase,'spokenMeaning':meaning,'url':f'https://www.youtube.com/watch?v={video}&t={int(t)}s'})
add('long','JlfAd_OaFek',3.8,'ảnh AI làm menu','Ảnh món ăn AI được đưa lên thực đơn quán ăn')
add('long','JlfAd_OaFek',8.5,'việc học','Chuyển sang việc học có hỗ trợ AI')
add('long','JlfAd_OaFek',405.8,'viết báo cáo','Một người xử lý dữ liệu rồi làm báo cáo')
add('long','JlfAd_OaFek',410.7,'kiểm tra thông tin','Con người vẫn cần kiểm chứng và đánh giá kết quả')
add('long','JlfAd_OaFek',452.8,'kiểm tra code','Kỹ sư thực sự viết và kiểm tra mã')
add('long','podWgLH4b3M',4.5,'thiên đường mua sắm','Nơi mua quần áo online với nhiều lựa chọn')
add('long','podWgLH4b3M',127,'mẫu mới mỗi ngày','Số lượng mẫu thời trang được tung ra mỗi ngày')
add('long','podWgLH4b3M',200.3,'ngưỡng miễn thuế','Hạn mức cho một gói hàng nhỏ')
add('long','podWgLH4b3M',215,'từng đơn hàng nhỏ','Gửi trực tiếp từng kiện tới người mua')
add('long','podWgLH4b3M',274.8,'Quần áo nữ','Phân biệt nhóm quần áo nữ trong câu chuyện tăng giá')
add('hidden','29B8-FtuC6U',7.8,'năng lực sản xuất','Năng lực sản xuất của nền kinh tế')
add('hidden','29B8-FtuC6U',10.5,'thiếu là sức mua','Nhu cầu mua thay vì năng lực làm ra hàng')
add('hidden','29B8-FtuC6U',27.8,'đầu bếp nấu','Ẩn dụ nhà hàng có nhiều đầu bếp nấu món ăn')
add('hidden','29B8-FtuC6U',36.5,'vài thực khách','Đối lập lượng món ăn với lượng khách ít trong nhà hàng')
add('hidden','29B8-FtuC6U',456,'lao động di cư','Người rời nông thôn ra đô thị làm việc')
add('hidden','5zqAMK2qsfM',3.8,'bấm nút lưu','Hành vi lưu nội dung trên điện thoại')
add('hidden','5zqAMK2qsfM',11.5,'kệ sách','Sách xếp trên kệ trong phòng')
add('hidden','5zqAMK2qsfM',391.8,'ngồi viết','Viết bài cảm nhận sau khi đọc')
add('hidden','5zqAMK2qsfM',517,'viết nó ra giấy','Đưa suy nghĩ ra giấy thành vật thể nhìn thấy')
add('hidden','5zqAMK2qsfM',647,'thuyết trình','Chuẩn bị trình bày cho người nghe cụ thể')
for row in rows:
    base=Path('docs/video-references/2026-11-12-two-directions' if row['channel']=='long' else 'docs/video-references/2026-11-11')/row['videoId']
    src=base/('reference.mp4' if row['channel']=='long' else 'reference-av.mp4')
    cap=cv2.VideoCapture(str(src));cap.set(cv2.CAP_PROP_POS_MSEC,row['frameTime']*1000)
    ok,frame=cap.read();actual=cap.get(cv2.CAP_PROP_POS_MSEC)/1000;cap.release()
    if not ok:raise ValueError(src)
    row.update({'media':str(src).replace('\\','/'),'decodedFrameTime':actual,'file':f"frames/{row['videoId']}-{row['frameTime']:08.3f}.jpg"})
    path=B/row['file'];path.parent.mkdir(exist_ok=True)
    Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)).save(path,quality=96)
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',24)
small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',20)
for channel in ['long','hidden']:
    chosen=[r for r in rows if r['channel']==channel]
    for page in range(2):
        take=chosen[page*5:(page+1)*5]
        sheet=Image.new('RGB',(1500,5*345),'#111923');d=ImageDraw.Draw(sheet)
        for i,r in enumerate(take):
            y=i*345;im=Image.open(B/r['file']);im.thumbnail((820,310));sheet.paste(im,(0,y))
            d.text((850,y+18),r['videoId']+' / '+str(r['frameTime'])+'s',font=small,fill='#94c7c1')
            d.text((850,y+60),r['phrase'],font=font,fill='white')
            line='';lines=[]
            for word in r['spokenMeaning'].split():
                cand=(line+' '+word).strip()
                if d.textlength(cand,font=small)>600:lines.append(line);line=word
                else:line=cand
            lines.append(line)
            for j,line in enumerate(lines):d.text((850,y+115+j*30),line,font=small,fill='#c6ccd0')
        sheet.save(B/f'{channel}-phrase-pairs-{page+1}.jpg',quality=95)
(B/'reference-pairs.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print('EXTRACTED',len(rows),'actual reference frames + 4 phrase sheets')

rejected=[]
for direction,t in [('long',1.0),('long',3.8),('long',19.8),('long',31.3),('long',49.5),('long',61.2),('long',75.5),('hidden',.8),('hidden',40.5),('hidden',43.5),('hidden',48.5),('hidden',69.8),('hidden',77.0)]:
    batch=Path('videos/2026-11-12-hai-huong')/direction
    data=json.loads((batch/'data.json').read_text(encoding='utf-8'))
    shot=next(s for s in data['shots'] if s['start']/30<=t<s['end']/30)
    words=json.loads((batch/'aligned-words.json').read_text(encoding='utf-8'))
    spoken=' '.join(w['text'] for w in words if shot['start']/30-.025<=w['start']<shot['end']/30-.025)
    cap=cv2.VideoCapture(str(batch/'final.mp4'));cap.set(cv2.CAP_PROP_POS_MSEC,t*1000);ok,frame=cap.read();cap.release()
    if not ok:raise ValueError((direction,t))
    file=f'rejected/{direction}-{t:06.2f}.jpg';p=B/file;p.parent.mkdir(exist_ok=True)
    Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)).save(p,quality=96)
    rejected.append({'direction':direction,'frameTime':t,'shotStart':shot['start']/30,'shotEnd':shot['end']/30,'spoken':spoken,'anchor':shot['phrase'],'images':[i['file'] for i in shot['images']],'file':file})
for page in range((len(rejected)+3)//4):
    take=rejected[page*4:(page+1)*4];sheet=Image.new('RGB',(1600,4*350),'#111923');d=ImageDraw.Draw(sheet)
    for i,r in enumerate(take):
        y=i*350;im=Image.open(B/r['file']);im.thumbnail((830,320));sheet.paste(im,(0,y))
        d.text((855,y+16),r['direction']+' / '+str(r['frameTime'])+'s',font=small,fill='#f58b73')
        text=r['spoken'];line='';lines=[]
        for word in text.split():
            cand=(line+' '+word).strip()
            if d.textlength(cand,font=small)>710:lines.append(line);line=word
            else:line=cand
        lines.append(line)
        for j,line in enumerate(lines):d.text((855,y+60+j*29),line,font=small,fill='white')
    sheet.save(B/f'rejected-pairs-{page+1}.jpg',quality=95)
(B/'rejected-pairs.json').write_text(json.dumps(rejected,ensure_ascii=False,indent=2),encoding='utf-8')
print('EXTRACTED',len(rejected),'rejected MP4 phrase/frame pairs')
