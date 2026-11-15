"""Prepare an isolated visual rewrite, preserving the exact China narration and mix."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import collections
import hashlib
import json
import shutil

from PIL import Image, ImageOps
import china

SPATIAL = 'o01 f01 f02 f03 f04 r01 r02 r03 d04 p04'.split()
PEOPLE = 'r05 r07 h01 h02 h03 h05 h06 h07 h08 d01 d02 d03 d06 p05'.split()
DATA = 'f05 f06 r04 h04 t02 t03 t04 t05 t06 t07 p01 p02 p06'.split()
STORY = 'o02 o03 o04 f07 f08 r06 t01 d05 p03 p07 e01 e02 e03 e04'.split()
MECHANICS = {
 'o01':'port, rail and domestic-life spatial juxtaposition', 'o02':'two engines and a balance of production and demand',
 'o03':'folded chapter atlas', 'o04':'brief educational scope disclaimer',
 'f01':'industrial city with infrastructure and districts', 'f02':'exploded product parts assembling and inspection',
 'f03':'supplier cluster neighborhood', 'f04':'warehouse inventory and order tickets',
 'f05':'statistical ruler and manufacturing source extract', 'f06':'diverging sector markers',
 'f07':'two different industrial contexts with limits of inference', 'f08':'pulling and braking economic engines',
 'r01':'sectional housing project with stakeholder places', 'r02':'escrow, payment calendar and waiting contractor',
 'r03':'construction floors and materials response', 'r04':'investment comparison index, not house price',
 'r05':'family postponing a purchase at a decision desk', 'r06':'source documents and unfinished-obligations board',
 'r07':'complete old apartment versus new empty foundation',
 'h01':'payroll and purchases in an actual store vignette', 'h02':'family calendar and financial protection objects',
 'h03':'100 illustrative coins allocated to three physical jars', 'h04':'nominal-to-real price-adjustment lens',
 'h05':'different household baskets behind an average', 'h06':'nested goods and service measurement scopes',
 'h07':'income and safety-net bridge towards a store', 'h08':'warehouse and shopping demand bottleneck',
 't01':'geographic trade atlas and actual port photograph', 't02':'imports, local assembly, export and domestic sale',
 't03':'domestic-value ledger excluding foreign input', 't04':'hypothetical unit blocks, ten minus seven',
 't05':'trade obstacles acting on a container', 't06':'partial supply-chain relocation with parts remaining',
 't07':'gross receipts, costs, profits and household income ledger',
 'd01':'100 people with 23 aged-60-plus pictograms', 'd02':'age ruler with distinct 60 and 65 thresholds',
 'd03':'life-course care, work and family spaces', 'd04':'human skills, tools and process at a workbench',
 'd05':'automation and worker contexts in a moving photographic aperture', 'd06':'multi-year education and training staircase',
 'p01':'nine-month GDP statistical book and growth scale', 'p02':'three quarterly year-on-year calendar markers',
 'p03':'policy plumbing with three different destinations', 'p04':'effective productive project versus empty construction',
 'p05':'household income security and store orders', 'p06':'moving a liability versus actually settling it',
 'p07':'reading a claim through a moving scope lens',
 'e01':'a layered economic landscape showing simultaneous pressures', 'e02':'meaningful callback to a town income-demand cycle',
 'e03':'four-question source inspection with a page magnifier', 'e04':'moving China context and an actionable three-topic closing',
}
MEDIA = {
 'f07':['cn-engine-mianyang','cn-panzhihua-steel'],
 'r06':['cn-shenzhen-residential'],
 't01':['cn-yangshan-port'],
 'd03':['cn-beijing-seniors'],
 'd05':['cn-industry-robots','cn-toy-assembly-workers'],
 'p07':['cn-nanjing-shoppers'],
 'e04':['cn-clip-china-market','cn-shanghai-skyline'],
}
HEADLINES={'o01':'Sản xuất mạnh. Sức mua mắc ở đâu?', 'o02':'Làm ra hàng khác với tìm được người mua', 'o03':'Ba góc nhìn về một nền kinh tế',
 'f05':'Chế tạo tăng 5,6% trong chín tháng', 'r04':'Đầu tư BĐS giảm 20,6% — giá nhà là chỉ tiêu khác',
 'h03':'Cùng một khoản thu, ba lựa chọn', 't03':'Vì sao GDP trừ nhập khẩu?',
 'e03':'Bốn câu hỏi trước khi kết luận'}

def prepare(batch, revision='r03'):
    batch=Path(batch).resolve(); out=batch/revision
    china.require(not (out/'data.json').exists() and not (out/'final.mp4').exists(), 'Prepared revision exists; preserve it')
    out.mkdir(exist_ok=True)
    data=china.load(batch/'r02/data.json')
    before=china.sha(batch/'r02/final.mp4')
    for name in ['content.json','chapter-timing.json','aligned-words.json','script.txt','sources-candidates.json','preflight.json']:
        src=batch/('r02/content.json' if name=='content.json' else name)
        shutil.copy2(src,out/name)
    (out/'audio').mkdir(exist_ok=True); (out/'benchmark').mkdir(exist_ok=True)
    for name in ['final-mix.wav','mix-report.json','narration.receipt.json','cue-plan.json','mix-dependencies.json']:
        shutil.copy2(batch/'audio'/name,out/'audio'/name)
    catalog={a['id']:a for a in china.load(batch/'sources-candidates.json')}
    public=out/'production-public/china';public.mkdir(parents=True,exist_ok=True)
    shutil.copy2(batch/'audio/final-mix.wav',public/'mix.wav')
    receipts=[]; plan=[]
    groups={**dict.fromkeys(SPATIAL,'spatial'),**dict.fromkeys(PEOPLE,'people'),**dict.fromkeys(DATA,'data'),**dict.fromkeys(STORY,'story')}
    china.require(len(groups)==51 and set(groups)=={s['id'] for s in data['shots']},'Every shot needs an authored treatment')
    for i,s in enumerate(data['shots']):
        if s['id']=='h05':s['layout']='c-sim'
        s['headline']=HEADLINES.get(s['id'],s['headline'])
        s['variety']={'module':groups[s['id']],'mechanic':MECHANICS[s['id']], 'index':i,
                      'revision':'r03', 'titleMode':'compact' if groups[s['id']]=='spatial' else 'standard'}
        s['images']=[]
        for aid in MEDIA.get(s['id'],[]):
            a=catalog[aid];src=batch/a['file'];china.require(china.sha(src)==a['sha256'],'Source changed: '+aid)
            ext='.mp4' if a['type']=='video' else '.jpg';target=public/(aid+ext)
            if ext=='.mp4':shutil.copy2(src,target)
            else:
                with Image.open(src) as im:
                    im=ImageOps.exif_transpose(im).convert('RGB');im.thumbnail((2048,2048));im.save(target,quality=93)
            image={'file':'china/'+target.name,'credit':a['creator'],'sourceHash':a['sha256'],'fit':'cover','focus':[50,50],
                   'aspect':a.get('width',16)/a.get('height',9)}
            if ext=='.mp4':image.update(mediaType='video',availableFrames=270,trimBeforeFrames=0)
            s['images'].append(image)
            receipts.append({'id':aid,'sourceFile':a['file'],'sourceSHA256':a['sha256'],'publicFile':image['file'],
                             'publicSHA256':china.sha(target),'page':a['page'],'creator':a['creator'],'license':a['license'],
                             'licenseURL':a['licenseURL'],'use':s['id'],'source':a,'scope':a['inspection'].get('limits',a['inspection'])})
        if s['id']=='e04':
            s['design']['cues']=[min(194,(s['end']-s['start'])//2)]
        plan.append({'id':s['id'],'module':groups[s['id']],'mechanic':MECHANICS[s['id']],'images':MEDIA.get(s['id'],[]),
                     'text':s['text'],'start':s['start'],'end':s['end']})
    old=china.load(batch/'r02/data.json')
    china.require(data['captions']==old['captions'] and data['audio']==old['audio'] and data['frames']==old['frames'],'Audio/captions changed')
    china.require([(s['id'],s['start'],s['end'],s['text']) for s in data['shots']]==[(s['id'],s['start'],s['end'],s['text']) for s in old['shots']],'Exact narration structure changed')
    media_hashes=[i['sourceHash'] for s in data['shots'] for i in s['images']]
    china.require(len(media_hashes)==len(set(media_hashes)),'Media source repeated')
    china.validate_media_intervals(data)
    china.save(out/'data.json',data);china.save(out/'props.json',{'data':data})
    china.save(public/'data.json',data);china.save(out/'source-receipts.json',receipts)
    china.save(out/'visual-plan.json',plan)
    report={'schema':'china-variety-revision/1','preparedUTC':datetime.now(timezone.utc).isoformat(),'revision':revision,
       'feedback':'User rejected repetitive templates; content-specific physical, people, data and editorial treatments replace template substitution.',
       'baselineFinalSHA256':before,'shots':51,'moduleCounts':dict(collections.Counter(groups.values())),
       'exactSameNarration':True,'exactSameCaptions':True,'exactSameTiming':True,'newPaidCalls':0,
       'uniqueContextSources':len(media_hashes),'mixSHA256':china.sha(out/'audio/final-mix.wav'),
       'diversityScope':'Authored per-shot mechanisms and later actual sequence viewing; counting IDs/modules alone does not establish visual variety or acceptance.',
       'userAcceptance':'pending'}
    china.save(out/'revision-receipt.json',report)
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--batch',type=Path,required=True);p.add_argument('--revision',default='r03')
    a=p.parse_args();print(json.dumps(prepare(a.batch,a.revision),ensure_ascii=False,indent=2))
