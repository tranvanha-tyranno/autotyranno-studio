"""Receipted real photographs for content-first economic explainers.

Photos show context and visible work/objects, never the identity or finances of
the fictional shop owner. Collection leaves inspection pending until actual
files and proposed crops have been opened and described.
"""
from __future__ import annotations
import argparse, hashlib, io, json, shutil
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import requests
from PIL import Image, ImageOps, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
BATCH = ROOT/'videos/2026-11-14-o-banh-mi-va-lam-phat'
LICENSE = 'https://www.pexels.com/license/'

# IDs and creator names come from primary photo pages reviewed on 2026-11-14.
# Previously receipted sources are copied byte-for-byte when available.
SEEDS = [
 ('vn-filled-banhmi',32961648,'vibrant-vietnamese-banh-mi-sandwich-close-up','Hậu Mai',['bread'],'Filled Vietnamese bánh mì sandwich close-up'),
 ('vn-filled-banhmi-bag',26619988,'a-sandwich-with-meat-and-vegetables-on-top-of-a-paper-bag','Theodore Nguyen',['bread'],'Filled Vietnamese bánh mì on paper bag'),
 ('bread-shelf',11953880,'close-up-photo-of-baguettes','Diana Roşca',['bread'],'Fresh baguettes on shelf'),
 ('bread-rustic',29635018,'rustic-baguette-bread-on-dark-background','Büşra Boduroğlu',['bread'],'Baguette and slices on dark surface'),
 ('bread-display',30826793,'rustic-artisan-baguettes-at-bakery','Magda Ehlers',['bread','shop'],'Bread display in bakery'),
 ('bread-oven',30596422,'freshly-baked-baguettes-in-a-traditional-bakery','Zehra K.',['bread','bakery'],'Baked bread inside bakery'),
 ('bread-basket',30509573,'artisanal-baguettes-in-rustic-bakery-setting','Anna Danilina',['bread','shop'],'Baguettes in basket'),
 ('vn-banhmi-vendor',33885703,'vietnamese-street-food-vendor-serving-banh-mi','Sóc Năng Động',['shop','bread'],'Street vendor at banh mi cart'),
 ('baker-kneading',3218467,'man-preparing-dough-for-bread','Vaibhav Jadhav',['bakery','wages'],'Baker kneading dough'),
 ('baker-work',36445104,'artisan-baker-preparing-fresh-bread-in-bakery','Yasin Onuş',['bakery','wages'],'Baker at work'),
 ('oven-loading',7633904,'a-person-baking-bread','Ilaria M',['bakery'],'Hand loading dough into oven'),
 ('flour-butter',94443,'bakery-flour-cooking-baking','Markus Spiske',['flour'],'Butter and flour on counter'),
 ('flour-sifting',7669733,'person-sifting-flour','Polina Tankilevitch',['flour'],'Person sifting flour into bowl'),
 ('flour-counter',36912597,'close-up-of-dough-and-flour-on-kitchen-counter','Debora Silveira',['flour'],'Flour on work surface'),
 ('oil-bottle',6213754,'olive-oil-in-a-glass-bottle','Vladimir Gladkov',['oil'],'Bottle of culinary oil'),
 ('vn-fuel',19059918,'gas-station-in-vietnam-at-night','Bui Van Dong',['oil','logistics'],'Petrol station and motorbikes in Vietnam'),
 ('delivery-truck',18800465,'truck-in-a-city-center','Matheus Bertelli',['logistics'],'Delivery truck on street'),
 ('cargo-ship',7128920,'stacks-of-shipping-containers-on-a-cargo-ship','Wolf Achim Wiegand',['logistics'],'Container ship'),
 ('vn-market-dalat',35723468,'local-market-scene-in-vietnam-with-vendors-and-shoppers','Kushie In Vietnam',['market'],'Vendors and shoppers at market'),
 ('vn-market-scooters',28463355,'bustling-street-market-scene-in-vietnam','Sam Tan',['market'],'Street market and scooters'),
 ('cash-vnd',34944540,'close-up-of-vietnamese-dong-currency-in-hand','Nguyễn Tiến Thịnh',['money','wages'],'Vietnamese dong banknotes in hand'),
 ('cash-vnd-halong',8089862,'person-holding-a-vietnamese-dong','My Tran',['money'],'Vietnamese dong banknote in hand'),
 ('budget-calculator',4386373,'calculator-and-notepad-placed-over-stack-of-paper-bills','Kaboompics',['household'],'Calculator and household budget materials'),
 ('budget-couple',6964105,'couple-looking-at-their-bills','Mikhail Nilov',['household'],'Adults reviewing paper bills'),
 ('grocery-cart',4971925,'woman-shopping-in-supermarket','Gustavo Fring',['household','market'],'Shopper with trolley in grocery aisle'),
 ('receipt-hands',4959926,'close-up-of-woman-hands-holding-bill','Kaboompics',['household'],'Hands reviewing paper receipt'),
]

LOCATIONS = {
 'vn-filled-banhmi':('VN','Việt Nam','Primary Pexels photo page location field says Việt Nam.'),
 'vn-filled-banhmi-bag':('VN','Ho Chi Minh City, Vietnam','Primary Pexels photo page location field says Ho Chi Minh City, Ho Chi Minh City, Vietnam.'),
 'vn-banhmi-vendor':('VN','Vietnam','Primary photo page location field says Vietnam.'),
 'vn-fuel':('VN','Vietnam','Primary photo page location field says Vietnam.'),
 'vn-market-dalat':('VN','Dalat, Vietnam','Primary photo page location field says Dalat, Vietnam; photograph is archival (taken 2019).'),
 'vn-market-scooters':('VN','Vietnam','Prior source receipt records primary photo page location field as Vietnam.'),
 'cash-vnd':('VN','Vietnam','Primary photo page location field says Vietnam; visible currency corroborates currency, not place.'),
 'cash-vnd-halong':('VN','Quảng Ninh, Vietnam','Prior source receipt records primary photo page location field as Quảng Ninh, Vietnam.'),
 'baker-kneading':('IN','Pune, India','Primary photo page location field says Pune, MH, India.'),
 'bread-rustic':('TR','Istanbul, Türkiye','Primary photo page location field says İstanbul, Türkiye.'),
 'delivery-truck':('NL','Amsterdam, Netherlands','Primary photo page location field says Amsterdam, Netherlands.'),
 'cargo-ship':('DE','Hamburg, Germany','Primary photo page location field says Hamburg, Germany.'),
 'flour-counter':('BR','RN, Brazil','Primary photo page location field says RN, Brasil.'),
}

def save(path, value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def collect(batch=BATCH):
    batch=Path(batch);folder=batch/'assets';folder.mkdir(parents=True,exist_ok=True)
    notespath=batch/'research/photo-inspection.json'
    notes=json.loads(notespath.read_text(encoding='utf-8')) if notespath.exists() else {}
    previous=ROOT/'videos/2026-11-14-tai-chinh-anh-that'
    oldpath=previous/'asset-catalog.json'
    old={str(x['pexelsID']):x for x in json.loads(oldpath.read_text(encoding='utf-8'))['assets']} if oldpath.exists() else {}
    def one(seed):
        name,number,slug,author,tags,expected=seed
        page=f'https://www.pexels.com/photo/{slug}-{number}/'
        url=f'https://images.pexels.com/photos/{number}/pexels-photo-{number}.jpeg?auto=compress&cs=tinysrgb&w=2400'
        target=folder/(name+'.jpg');prior=old.get(str(number));reuse=None
        if prior:
            src=previous/prior['file']
            if src.is_file() and sha(src)==prior['sha256']:
                reuse=src
                page=prior.get('sourceURL',page)
        if not target.exists():
            if reuse:shutil.copy2(reuse,target)
            else:
                response=requests.get(url,timeout=45);response.raise_for_status()
                image=Image.open(io.BytesIO(response.content));image.verify()
                target.write_bytes(response.content)
        with Image.open(target) as image:
            width,height=image.size
        if min(width,height)<650:raise ValueError('Photo too small '+name)
        note=notes.get(name,{})
        item={'id':name,'file':'assets/'+target.name,'provider':'Pexels','providerPhotoId':number,
              'sourceURL':page,'downloadURL':url,'creator':author,'license':'Pexels License','licenseURL':LICENSE,
              'sha256':sha(target),'width':width,'height':height,'tags':tags,'credit':f'{author} / Pexels',
              'expectedFromSource':expected,'observed':note.get('observed',''),
              'inspection':note.get('inspection',{'status':'pending_actual_pixels_and_crop'}),
              'fit':note.get('fit','contain'),'focus':note.get('focus',[50,50]),
              'crop':[0,0,1,1], 'medium':'real sourced photograph',
              'role':'context illustration',
              'limits':note.get('limits','Not the fictional Hạnh or her shop; no claims about the pictured person’s income, pricing, profit, employment, behavior or endorsement. Archival source; not evidence of present-day prices.'),
              'reusedSource':str(reuse.relative_to(ROOT)).replace('\\','/') if reuse else None}
        if name in LOCATIONS:
            country,place,evidence=LOCATIONS[name]
            item['location']={'countryCode':country,'place':place,'sourceURL':page,'evidence':evidence}
        if item['inspection'].get('status')=='inspected':
            item['inspection']['sha256']=item['sha256']
        save(batch/'research/photo-receipts'/(name+'.json'),item)
        return item
    with ThreadPoolExecutor(max_workers=6) as pool:items=list(pool.map(one,SEEDS))
    registry={tag:[x for x in items if tag in x['tags']] for tag in ['bread','bakery','flour','oil','logistics','market','shop','money','household','wages']}
    save(batch/'research/photo-sources.json',{'schema':'economy-story-real-photos/1','collectedOn':'2026-11-14',
        'licenseReview':{'sourceURL':LICENSE,'reviewed':'2026-11-14','summary':'Pexels permits free use and modification; no endorsement implied and identifiable people not depicted negatively.'},
        'policy':'Source photography is contextual. None depicts the fictional shop owner or validates the hypothetical price model.',
        'assets':items,'registry':registry,'byTag':registry,'newPaidVisualCalls':0})
    save(batch/'assets.json',registry)
    sheets(batch,items)
    print('STORY_PHOTOS_READY',len(items),'inspected',sum(x['inspection'].get('status')=='inspected' for x in items),flush=True)
    return registry

def sheets(batch,items):
    dest=batch/'assets/inspection';dest.mkdir(exist_ok=True)
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',20)
    for start in range(0,len(items),8):
        sheet=Image.new('RGB',(1920,1120),'#eae2d5');draw=ImageDraw.Draw(sheet)
        for j,item in enumerate(items[start:start+8]):
            x,y=j%4*480,j//4*560
            with Image.open(batch/item['file']) as src:
                src=ImageOps.exif_transpose(src).convert('RGB')
                whole=ImageOps.contain(src,(468,280));sheet.paste(whole,(x+(468-whole.width)//2,y+30))
                proposed=ImageOps.fit(src,(468,220),method=Image.Resampling.LANCZOS)
                sheet.paste(proposed,(x,y+320))
            draw.text((x+5,y+4),item['id'],font=font,fill='#252136')
        sheet.save(dest/f'photo-sheet-{start//8+1:02}.jpg',quality=93)
    save(dest/'sheets.json',{'method':'top original aspect; bottom proposed center crop; renderer must honor fit/focus and final render still needs inspection',
        'files':[{'file':p.relative_to(batch).as_posix(),'sha256':sha(p)} for p in sorted(dest.glob('photo-sheet-*.jpg'))]})

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--batch',type=Path,default=BATCH)
    collect(parser.parse_args().batch)
