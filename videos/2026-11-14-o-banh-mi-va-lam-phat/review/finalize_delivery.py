"""Retain delivery metadata; no provider calls or production source edits."""
from pathlib import Path
import hashlib
import json
import shutil
import cv2

BATCH=Path(__file__).resolve().parents[1]
ROOT=BATCH.parents[1]
OUT=BATCH/'r03'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def save(p,v): p.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')

qa=load(OUT/'qa-report.json')
assert qa['technical']=='passed' and qa['decodedFrames']==18671
assert qa['sha256']==sha(OUT/'final.mp4')
early=[OUT/'qa'/f'contact-{i:02}.jpg' for i in range(1,6)]
save(BATCH/'review/r03-final-visual-early.json',{
    'reviewer':'Codex parent','revision':'r03','method':'Opened five contact sheets from final encoded MP4, 75 early/middle/late samples across first25beats',
    'decision':'No blocking visual defect in these sampled frames',
    'observations':['Vietnamese headings/captions remain legible without visible clipped marks',
        'Portrait foreground images remain sharp and contained; flour/fuel/bakery subjects visible',
        'Illustrative price and cost figures match narration; character pose remains fixed in samples'],
    'evidence':[{'file':p.relative_to(BATCH).as_posix(),'sha256':sha(p)} for p in early],
    'continuousAVReview':False,'userApproval':'pending'})

cap=cv2.VideoCapture(str(OUT/'final.mp4'));cap.set(cv2.CAP_PROP_POS_FRAMES,75)
ok,img=cap.read();assert ok;cap.release()
cv2.imwrite(str(OUT/'poster.jpg'),img)

extra=['workflows/reference-video/finance_long_render.py','workflows/reference-video/documentary.py',
       'workflows/reference-video/economy_story_asr.py','workflows/reference-video/economy_story_assets.py',
       'workflows/reference-video/economy-story.profile.json','workflows/reference-video/ECONOMY_STORY.md',
       'workflows/reference-video/SRC_REVIEW_2026-11-14.md','workflows/reference-video/src-review-2026-11-14.json',
       'workflows/reference-video/src-review-finance-2026-11-14.json',
       'workflows/reference-video/src-review-economics-2026-11-14.json',
       'workflows/reference-video/src-review-photos-2026-11-14.json']
receipts=[]
for relative in extra:
    source=ROOT/relative;dest=OUT/'source-supplement'/relative
    dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,dest)
    receipts.append({'source':relative,'sha256':sha(source),'retained':dest.relative_to(BATCH).as_posix()})
save(OUT/'supplemental-source-receipt.json',{'scope':'Additional unchanged helper sources, new local verifier and final guidance captured after render; original frozen render dependencies remain in dependencies.json','files':receipts})

plan=load(OUT/'props.json')['plan']
chapters='\n'.join(f'- {c["from"]//1800:02}:{(c["from"]//30)%60:02} — {c["title"]}' for c in plan['chapters'])
text=f'''# Một ổ bánh mì kể chuyện lạm phát

Bản thử r03: **10 phút 22,37 giây**, Full HD 1920×1080, 30fps.

Video: `r03/final.mp4`. Font Be Vietnam Pro local; nhân vật giữ pose, chỉ xoay nhẹ theo cue lời. Giọng Nhật Phong / eleven_v3, tốc độ tự nhiên 1.0. Không có thương hiệu kênh. Nhân vật và giá/chi phí là giả định; ảnh thật chỉ minh họa bối cảnh.

{chapters}

Kiểm kỹ thuật: đủ 18.671 frame; giải mã tiếng 622,379 giây, giữ câu kết. ASR base cục bộ nhận dạng đủ tám chương, không có cờ chẩn đoán nghi bỏ đoạn. Đã mở 150 khung chọn mẫu của MP4 cuối cùng và chuỗi proof đầu/giữa/cuối; các việc này không phải nghe/xem liên tục hoặc người dùng đã duyệt thẩm mỹ.

Nguồn và phạm vi: `research/sources.json`, `research/photo-sources.json`, `research/clause-photo-selection.json`. Ảnh thật hiện diện khoảng 65,61% thời lượng kể cả disclaimer, 18 nguồn ảnh thực sự được renderer chọn. Không gán người hoặc cửa hàng trong ảnh cho Hạnh hư cấu.

Lịch sử sửa: giữ r01 có lỗi ảnh dọc và r02 đã sửa; r03 xử lý sẵn nền ảnh để giảm chi phí render. Toàn bộ src đã được rà: 145 mã/văn bản đọc đủ, 2 JSON parse dữ liệu, 3 font kiểm CMAP/hash. Các nhánh cũ và phản hồi bị bác vẫn được giữ.

Hồ sơ QA ở `r03/qa-report.json`, kiểm lời `audio/asr-base-review.json`, kiểm hình ở `review/`. Trạng thái: **chờ phản hồi người dùng**.
'''
(BATCH/'README.md').write_text(text,encoding='utf-8')
save(OUT/'delivery.json',{'title':plan['title'],'file':'r03/final.mp4','sha256':sha(OUT/'final.mp4'),
    'bytes':(OUT/'final.mp4').stat().st_size,'durationSeconds':qa['seconds'],'decodedFrames':qa['decodedFrames'],
    'technical':'passed','asr':'all eight exact-mix chapters, diagnostic only',
    'visualReview':'sampled frame and temporal proof review; no continuous AV playback claim',
    'sourceReview':'all150srcfiles accounted','userApproval':'pending',
    'reports':{'technical':'r03/qa-report.json','asr':'audio/asr-base-review.json',
        'integrity':'review/r03-integrity.json','earlyVisual':'review/r03-final-visual-early.json',
        'lateVisual':'review/r03-final-visual-late.json','source':'r03/source-supplement/workflows/reference-video/SRC_REVIEW_2026-11-14.md'}})
print('DELIVERY_RECORDED',qa['seconds'],flush=True)
