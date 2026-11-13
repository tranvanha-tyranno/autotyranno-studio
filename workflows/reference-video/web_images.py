"""Fetch reviewed source photographs for an illustration-led video.

Only downloads explicitly listed photo IDs; retains source/license metadata and hashes.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import argparse,json,hashlib,requests
from PIL import Image,ImageOps,ImageDraw,ImageFont

CATALOG=[
 ('notes',6829535,'a-person-writing-on-a-notebook','Kampus Production','Hands writing notes with laptop and charts'),
 ('asian-notes',8101724,'a-man-writing-in-the-notebook','Mikhail Nilov','Asian man taking notes in an office meeting'),
 ('colleagues',4623351,'people-in-office-working-on-laptop','Ketut Subiyanto','Two colleagues discussing a laptop at a desk'),
 ('headset',8867202,'a-person-holding-a-headset','Yan Krukau','Close-up of headset held in office'),
 ('support-team',8866791,'people-wearing-headset-at-the-office','Yan Krukau','Customer service team collaborating'),
 ('support-agent',7709155,'a-working-wearing-headphones-while-working','MART PRODUCTION','Call-center agent with laptop and headphones'),
 ('calculator',33175651,'financial-analysis-with-calculator-and-documents','Bia Limova','Calculator and financial document analysis'),
 ('learning',7983591,'elderly-learning-computer-skills','Kampus Production','Adult learner and teacher at a computer'),
 ('review-docs',7735697,'people-reading-documents','Mikhail Nilov','Two professionals reviewing charts on paper'),
 ('sticky-board',29521529,'creative-brainstorming-session-with-sticky-notes','Jakub Zerdzicki','Planning with sticky notes'),
 ('board-team',39219857,'team-brainstorming-with-sticky-notes-on-chalkboard','Vitaly Gariev','Two colleagues brainstorming on chalkboard'),
 ('overload',6964351,'a-stressed-woman-looking-at-the-papers-on-a-wooden-desk','Mikhail Nilov','Woman working through documents at a desk'),
 ('paperwork',8278873,'man-stressed-at-work','ANTONI SHKRABA production','Office worker with paperwork'),
 ('typing-photo',7075408,'a-person-typing-on-a-laptop','Firmbee.com','Hands typing on a laptop'),
 ('interview',36733328,'professional-job-interview-in-modern-office-setting','Vitaly Gariev','Professional job interview'),
 ('solar',19895867,'engineer-standing-among-solar-panels','ThisIsEngineering','Engineer inspecting rooftop solar panels'),
 ('candidate',7644155,'a-woman-in-business-attire-getting-a-job-interview','MART PRODUCTION','Interview with documents at a table'),
 ('review-team',8512387,'women-checking-on-documents-at-work','Artem Podrez','Two colleagues checking documents'),
 ('team-decision',7875989,'a-woman-showing-documents-to-her-coworkers','Kaboompics.com','Business team discussing documents'),
 ('close-review',8730980,'a-close-up-shot-of-people-reviewing-documents','Mikhail Nilov','Hands discussing documents and tablet'),
 ('client-meeting',9870157,'social-worker-sitting-at-table-with-documents-folder-in-front-of-her','Ron Lach','Professional discussing a folder with clients'),
 ('discussion',8730125,'a-man-and-woman-having-a-meeting-together','Mikhail Nilov','Two professionals discussing paperwork'),
 ('team-charts',5324937,'woman-at-table-with-documents-during-meeting-with-colleagues','Anna Shvets','Team working with charts and documents'),
 ('home-learning',12911676,'woman-taking-notes-studying-on-laptop-at-home','Mizuno K','Adult learning at home with notebook and laptop'),
 ('resume',3205566,'woman-holding-clipboard','cottonbro studio','Recruiter reviewing a resume on a clipboard'),
 ('folders',16978372,'black-folders-with-documents-and-contracts-isolated-on-a-white-background-segregated-with-stickers-in-the-shape-of-arrows-workflow-direction-office-work-and-household-bills','Jakub Zerdzicki','Organized ring binders with labels'),
 ('file-stack',8468119,'man-holding-pile-of-documents','cottonbro studio','Worker carrying a stack of office files'),
]

def fetch(batch:Path):
    assets=batch/'assets';sources=batch/'sources';assets.mkdir(exist_ok=True,parents=True);sources.mkdir(exist_ok=True)
    def one(row):
        name,id,slug,author,subject=row;p=assets/(name+'.jpg');url=f'https://images.pexels.com/photos/{id}/pexels-photo-{id}.jpeg?auto=compress&cs=tinysrgb&w=2400'
        if not p.exists():
            r=requests.get(url,timeout=45);r.raise_for_status()
            if not r.headers.get('content-type','').startswith('image/'):raise ValueError('Not image '+name)
            p.write_bytes(r.content)
        with Image.open(p) as im:im.verify()
        with Image.open(p) as im:w,h=im.size
        record={'id':name,'providerPhotoId':id,'file':'assets/'+p.name,'page':f'https://www.pexels.com/photo/{slug}-{id}/','download':url,'creator':author,'description':subject,'license':'Pexels License','licenseURL':'https://www.pexels.com/license/','role':'Illustrative source photo; not documentary evidence of an individual using AI, losing employment or endorsing this video','width':w,'height':h,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}
        (sources/(name+'.json')).write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
        return record
    with ThreadPoolExecutor(max_workers=6) as pool:rows=list(pool.map(one,CATALOG))
    (batch/'image-sources.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',21)
    for page in range((len(rows)+11)//12):
        sheet=Image.new('RGB',(1600,4*270),(9,15,24));draw=ImageDraw.Draw(sheet)
        for i,r in enumerate(rows[page*12:(page+1)*12]):
            x=i%4*400;y=i//4*270
            with Image.open(batch/r['file']) as im:thumb=ImageOps.fit(im.convert('RGB'),(400,225));sheet.paste(thumb,(x,y))
            draw.text((x+10,y+234),r['id'],font=font,fill='white')
        sheet.save(batch/f'asset-review-{page+1:02}.jpg',quality=93)
    print('SOURCE PHOTOS',len(rows),'downloaded and decoded',flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--batch',type=Path,required=True);fetch(p.parse_args().batch)
