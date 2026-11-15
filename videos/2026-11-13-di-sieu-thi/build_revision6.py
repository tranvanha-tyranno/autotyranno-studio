"""Apply r05's actual still-review corrections in a fresh retained revision."""
import json
from pathlib import Path
root=Path(__file__).resolve().parent
d=json.loads((root/'production-v5.json').read_text(encoding='utf-8'))
d['id']='di-sieu-thi-vietnam-motion-r06'
shots={s['id']:s for sec in d['sections'] for s in sec['shots']}
assets={a['id']:a for a in d['assets']}
row=next(x for x in json.loads((root/'source-vietnam.json').read_text(encoding='utf-8')) if x['id']=='vn-hue-customer')
asset={'id':row['id'],'file':row['file'],'sha256':row['sha256'],
 'source':{'url':row['page'],'creator':row['creator'],'license':row['license'],'licenseURL':row['licenseURL'].replace('http://creativecommons.org/','https://creativecommons.org/'),'kind':'stock'},
 'location':row['location'],
 'observed':{'subject':'A woman sits beside vegetables and eggs at a Vietnam market; another person holds a grocery bag.','action':'Ordinary market shopping context; no private motives or completed payment inferred.','objects':'Vegetables, eggs, plastic bag and motorbikes.','limits':row['inspection']['doesNotEstablish']},
 'inspection':{'status':'inspected','reviewer':'Codex root','sha256':row['sha256'],'observations':'Opened whole actual960x640 file. Visible vegetable/egg vendor, bag and motorbikes. Handheld paper is not used as proof of payment or personal intent.'},
 'focus':[57,56],'fit':'cover'}
d['assets'].append(asset)
shots['c16']['images']=[asset['id']]
shots['c16']['needToSee']=shots['c16']['supports']='Ordinary fresh-food shopping in a documented Vietnam market; vegetables, eggs and a grocery bag remain visible. This supports the everyday setting, not an inferred motive.'
shots['c16']['sourceNote']=f"Ảnh tư liệu Huế · {row['creator']} · {row['license']} · {row['capturedDate'][:4]}"
shots['c16']['review']['observations']=shots['c16']['needToSee']+' Root opened whole native image; rendered crop still requires inspection.'
shots['c16']['review']['assetHashes']={asset['id']:asset['sha256']}
s=shots['c13'];s['images']=['vn-noodle-aisle'];s['layout']='object3d'
s['motion']={'kind':'basket','revealFrames':[0,55,140]}
s['eyebrow']='THẤY GIỎ ĐẦY / CHƯA BIẾT LÝ DO'
s['headline']='Giỏ đầy chưa nói lên lý do mua.'
s['body']='Định mua gì? Dùng thế nào? Món nào vừa phát sinh?'
s['mediaRole']='mechanism'
s['needToSee']=s['supports']='An original3D basket visibly fills with cartons beside a documented Vietnam aisle. Three questions identify the missing planning/use information; pictured people are not asserted to waste food or overspend.'
s['review']['observations']=s['needToSee']+' The filled basket is explicit original3D illustration, not a claim that the archive photograph shows a full basket.'
s['review']['assetHashes']={'vn-noodle-aisle':assets['vn-noodle-aisle']['sha256']}
s['sourceNote']=shots['c5']['sourceNote']
shots['c6']['sourceNote']='Ảnh: Mike Jones / Pexels · Việt Nam: Kham Tran / CC BY-SA 3.0 / 2007'
shots['c14']['sourceNote']='Ảnh: Pew Nguyen / Pexels · VN: Kham Tran / CC BY-SA 3.0 / 2007; Groupe Casino / CC BY-SA 3.0 / 2013'
(root/'production-v6.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
print('Prepared production-v6.json; r05 remains a retained still-review iteration.')
