"""Build an illustration-led revision using exact narration phrase cuts.

Preserves the earlier render/audio and records why each external asset is shown.
"""
from pathlib import Path
import json,shutil,re,hashlib
from PIL import Image

ROOT=Path(__file__).resolve().parents[2]
OLD=ROOT/'videos/2026-11-11-ai-va-cong-viec-5phut'
BATCH=ROOT/'videos/2026-11-12-ai-va-cong-viec-anh-that'
PUB=Path(__file__).parent/'cinematic/public/visual-story'

# Source ID, exact spoken phrase (empty means chapter start), visible purpose.
PLAN={
 'hook':[('v-typing','','Writing starts with an actual keyboard'),('notes','Rất tiện','Draft/notes as tangible work'),('paperwork','Cũng rất đáng lo','Existing staged workload photo, illustrative'),('v-worker','phần nào còn lại','A person at work instead of abstract AI chip'),('team-decision','một công việc thực ra','Work involves decisions and people')],
 'bundle':[('sticky-board','','Task board makes the bundle of tasks concrete'),('notes','Thu thập thông tin','Collecting information and writing notes'),('review-docs','Rồi kiểm tra','Physical document checking'),('client-meeting','trao đổi với khách hàng','Person-to-person client conversation'),('board-team','vài mắt xích','People and real task board')],
 'example':[('v-typing','','Real typing for content draft'),('notes','đề xuất tiêu đề','Notebook and writing draft'),('team-charts','sản phẩm thật sự','Team examining actual materials'),('close-review','hứa quá mức','Checking the claims on paper, illustrative'),('support-agent','Ai nhận phản hồi','Headset worker for customer feedback')],
 'exposure':[('v-office','','A workplace establishes the workforce context'),('support-team','cứ bốn người lao động','Four actual workers for one-in-four exposure graphic'),('colleagues','Từ quan trọng','People still working together, no fake layoffs')],
 'meaning':[('review-docs','','Research needs careful reading'),('folders','không đếm số người','Documents, not identifiable layoffs'),('discussion','biến đổi công việc','People adapting a work discussion'),('review-team','mọi vị trí','Two people checking their work')],
 'physical':[('v-worker','','Actual laptop work'),('close-review','dữ liệu thiếu','Incomplete context illustrated by people checking documents'),('support-agent','khách hàng tức giận','Service worker shown neutrally; no claim about the model person'),('headset','câu trả lời lịch sự','Specific tool used to communicate'),('client-meeting','Hiểu hoàn cảnh','Face-to-face listening and judgment')],
 'economics':[('calculator','','Real calculation for cost/time'),('notes','viết nhanh','Writing a first version'),('review-docs','sửa sai lâu hơn','Checking takes time'),('folders','dữ liệu không được phép','Documents and data handling'),('team-decision','quy trình chạy được','Coordinating a real work process')],
 'forecast':[('v-office','','Employment context'),('g-forecast','một trăm bảy mươi','Only this short measured chart uses 3D'),('interview','Đây là kỳ vọng','Recruiter expectations, not already observed jobs')],
 'context':[('team-charts','','Multiple structural changes'),('solar','chuyển đổi xanh','Solar engineer specifically matches green transition'),('resume','người mất một vị trí','Resume: search for another role; not a claim the pictured person was fired'),('candidate','Khác kỹ năng','Interview illustrates a transition barrier'),('home-learning','khó khăn cá nhân','Learning and preparing as an individual')],
 'review':[('v-reviewer','','Human looking closely at a screen'),('board-team','đặt yêu cầu rõ','Explaining the work goal to someone else'),('review-team','kiểm tra được','Actual joint document review'),('close-review','bản nháp sai ở đâu','Attention to details in a draft'),('calculator','đúng mục tiêu','Check the output instead of generic shapes')],
 'hallucination':[('calculator','','Real financial paperwork for the hypothetical summary'),('review-docs','doanh thu với lợi nhuận','Document detail; no fake data over stock'),('v-typing','gửi đi','Typing/dispatch context'),('close-review','đối chiếu số với bảng gốc','A finger/pencil points to source documents'),('notes','định nghĩa từng cột','Writing down definitions and checking')],
 'map':[('board-team','','Real board introduces self review'),('sticky-board','ba nhóm','Three task labels placed over an actual planning board'),('notes','Nhóm hai','Record what needs human review'),('client-meeting','Nhóm ba','Human relationships and direct responsibility'),('colleagues','nhiệm vụ nào','Discuss the specific task to change')],
 'experiment':[('home-learning','','Small personal trial'),('v-typing','nháp email','A keyboard for writing the draft email'),('notes','mục tiêu, người đọc','Written instructions and constraints'),('review-docs','để so sánh','Actual documents represent before/after review'),('folders','dữ liệu nhạy cảm','Folders/data rather than a decorative AI object'),('review-team','phát hiện và sửa','People review and correct together')],
 'measure':[('v-worker','','Doing the task at a computer'),('notes','Ghi những lỗi','Write down the errors'),('calculator','tiết kiệm thời gian','Evaluate time and benefit'),('board-team','sửa cách giao việc','Refine the instructions on a board'),('colleagues','lặp lại đáng tin cậy','Repeatable collaboration')],
 'skills':[('home-learning','','Learning without needing to become an AI engineer'),('learning','tư duy phân tích','Adult learner coached by another person'),('solar','kỹ năng công nghệ','Technology skill in physical engineering work'),('review-team','hiểu nghề, biết kiểm tra','Human expertise and checking'),('asian-notes','ngay hôm nay','Taking notes and practising today')],
 'portfolio':[('folders','','Keeping work samples'),('notes','trước và sau','Record the original request'),('v-typing','bản nháp của máy','Writing and editing a draft'),('review-docs','phần bạn sửa','Annotated/checked material as contribution'),('team-decision','đóng góp thật','Show the work in a real discussion'),('home-learning','khi nào dùng','Choose when the tool helps')],
 'company':[('v-office','','Responsibility at organization level'),('team-decision','Tổ chức cần','A team plans the process'),('learning','thời gian đào tạo','Real one-to-one training'),('review-team','tiêu chuẩn chất lượng','Joint review for quality'),('file-stack','tạo thêm áp lực','Staged paperwork load, no claim about the pictured worker'),('board-team','đổi cách tổ chức','People reorganize a task board')],
 'closing':[('colleagues','','Human collaboration'),('candidate','Không có một câu trả lời chung','Different people have different needs'),('notes','từng nhiệm vụ','Focus on one written task'),('review-team','sự hiểu biết và trách nhiệm','Knowledge plus careful review'),('home-learning','Ngày mai','Close on an actual person learning and preparing')]
}

def norm(s):return re.sub(r'[^\w]','',s.lower())

def build():
    PUB.mkdir(parents=True,exist_ok=True);BATCH.mkdir(parents=True,exist_ok=True)
    for f in ['content.json','script.txt','timeline.json','aligned-words.json','sources.json','RESEARCH.md','sound-cues.json']:
        shutil.copy2(OLD/f,BATCH/f)
    shutil.copytree(OLD/'audio',BATCH/'audio',dirs_exist_ok=True)
    shutil.copy2(OLD/'audio/final-mix.wav',PUB/'mix.wav')
    for p in (BATCH/'assets').glob('*.jpg'):shutil.copy2(p,PUB/p.name)
    # The source has extensive empty wall above the two reviewers. Preserve
    # original bytes; a recorded crop makes faces, hands and documents legible.
    with Image.open(BATCH/'assets/review-team.jpg') as im:
        im.crop((0,1250,2400,3500)).save(BATCH/'assets/review-team-detail.jpg',quality=96)
    shutil.copy2(BATCH/'assets/review-team-detail.jpg',PUB/'review-team-detail.jpg')
    for name,src in [('typing','typing.mp4'),('worker','worker.mp4'),('office','office.mp4'),('reviewer','reviewer.mp4')]:
        shutil.copy2(OLD/'assets'/src,PUB/src);shutil.copy2(OLD/'assets'/src,BATCH/'assets'/src)
    timeline=json.loads((BATCH/'timeline.json').read_text(encoding='utf-8'));w=json.loads((BATCH/'aligned-words.json').read_text(encoding='utf-8'));tokens=[norm(x['text']) for x in w]
    images={x['id']:x for x in json.loads((BATCH/'image-sources.json').read_text(encoding='utf-8'))}
    def find(phrase,c):
        q=[norm(x) for x in phrase.split()]
        for i in range(len(w)-len(q)+1):
            if w[i]['start']*30<c['start']-2 or w[i]['start']*30>=c['end']:continue
            if tokens[i:i+len(q)]==q:return round(w[i]['start']*30)-c['start']
        raise ValueError((c['id'],phrase))
    chapters=[];allshots=[]
    for c in timeline['chapters']:
        shots=[]
        for i,(asset,phrase,purpose) in enumerate(PLAN[c['id']]):
            start=0 if not phrase else find(phrase,c)
            if asset.startswith('g-'):kind='graphic';file=''
            elif asset.startswith('v-'):kind='video';file={'v-typing':'typing.mp4','v-worker':'worker.mp4','v-office':'office.mp4','v-reviewer':'reviewer.mp4'}[asset]
            else:kind='photo';file=asset+'.jpg'
            aspect=images[asset]['width']/images[asset]['height'] if kind=='photo' else 16/9
            if asset=='review-team':file='review-team-detail.jpg';aspect=2400/2250
            shots.append({'asset':asset,'type':kind,'file':file,'start':start,'phrase':phrase,'purpose':purpose,'pan':i%2,'focus':[50,42],'aspect':aspect})
        for i,s in enumerate(shots):s['end']=shots[i+1]['start'] if i+1<len(shots) else c['end']-c['start'];assert s['end']>s['start'];allshots.append({**s,'globalStart':s['start']+c['start'],'globalEnd':s['end']+c['start'],'chapter':c['id']})
        chapters.append({**c,'shots':shots})
    data={**timeline,'chapters':chapters,'direction':'Illustration-led: real internet photographs and footage carry the story. Useful data graphics only, never a full runtime of 3D objects.'}
    (PUB/'data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8');(BATCH/'visual-timeline.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8');(BATCH/'shotlist.json').write_text(json.dumps(allshots,ensure_ascii=False,indent=2),encoding='utf-8')
    frames={k:sum(s['end']-s['start'] for s in allshots if s['type']==k) for k in ['photo','video','graphic']}
    report={'shots':len(allshots),'uniquePhotos':len({s['asset'] for s in allshots if s['type']=='photo'}),'secondsByType':{k:v/30 for k,v in frames.items()},'audioChange':'None: exact previous final mix copied with matching SHA256','audioSHA256':hashlib.sha256((PUB/'mix.wav').read_bytes()).hexdigest(),'sourceRevision':str(OLD.relative_to(ROOT)),'newDirectionRequested':'2026-11-12','userAcceptance':'pending'}
    (BATCH/'direction-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(report),flush=True)
    (BATCH/'derived-assets.json').write_text(json.dumps([{'file':'assets/review-team-detail.jpg','original':'assets/review-team.jpg','cropPixels':[0,1250,2400,3500],'reason':'Remove empty upper wall while keeping both reviewers, hands and papers','sha256':hashlib.sha256((BATCH/'assets/review-team-detail.jpg').read_bytes()).hexdigest()}],indent=2),encoding='utf-8')

if __name__=='__main__':build()
