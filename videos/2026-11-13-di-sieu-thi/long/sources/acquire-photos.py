from pathlib import Path
import json,hashlib,requests,concurrent.futures
from PIL import Image,ImageOps,ImageDraw
root=Path('videos/2026-11-13-di-sieu-thi/long');(root/'assets').mkdir(parents=True,exist_ok=True);(root/'sources').mkdir(exist_ok=True)
rows=[
('cart-browse',4971925,'woman-shopping-in-supermarket','Gustavo Fring','Woman choosing groceries beside a full shopping cart'),
('cart-full',4971949,'woman-with-cart-grocery-shopping-in-supermarket','Gustavo Fring','Woman behind cart among produce'),
('basket-full',8422688,'smiling-woman-carrying-a-grocery-basket','Kampus Production','Woman carrying basket of fresh produce'),
('phone-list',27175517,'woman-looking-at-a-shopping-list-in-a-supermarket','Helena Lopes','Woman with grocery basket checking smartphone; text on screen is not readable'),
('groceries-home',5842506,'bags-of-food-on-a-white-table','Kaboompics.com','Mesh bags containing produce on white table'),
('vegetables-home',7890015,'assorted-vegetables-in-a-basket-and-on-a-wooden-table','MART PRODUCTION','Vegetables unpacked on wooden table'),
('choose-produce',7990381,'a-woman-in-a-grocery-store','Ivan S','Woman choosing produce in a grocery store'),
('checkout-wide',36772947,'cashier-at-supermarket-checkout-counter','Radik 2707','Products and cashier at supermarket checkout'),
('checkout-couple',4199489,'couple-buying-groceries-at-a-supermarket','Jack Sparrow','Couple and cashier at grocery checkout'),
('fridge-check',8805274,'a-woman-opening-a-fridge','Mike Jones','Woman looking inside open refrigerator'),
('fridge-kitchen',36671734,'woman-exploring-fridge-in-cozy-kitchen','Pew Nguyen','Woman checks refrigerator in home kitchen'),
('sale-shelf',9592528,'assorted-labeled-boxes-on-white-shelf','Erik Mclean','Snack shelf with sale labels and prices'),
('milk-shelf',7451957,'shelves-with-various-milk-boxes','Nothing Ahead','Multiple milk cartons displayed with shelf price labels'),
('phone-plan-couple',4047288,'muslim-couple-buying-groceries','Jack Sparrow','Couple checks phone while choosing groceries'),
('phone-basket',4971909,'happy-woman-grocery-shopping-in-supermarket','Gustavo Fring','Woman with basket examining phone or grocery'),
('plum-price',40914715,'fresh-plums-on-display-at-grocery-store','Andri Arbianto','Plums displayed with price tag')]
def one(row):
 name,photoid,slug,author,desc=row
 page=f'https://www.pexels.com/photo/{slug}-{photoid}/'
 url=f'https://images.pexels.com/photos/{photoid}/pexels-photo-{photoid}.jpeg?auto=compress&cs=tinysrgb&w=1920'
 target=root/'assets'/f'{name}.jpg'
 if not target.exists():
  r=requests.get(url,timeout=45);r.raise_for_status();assert r.headers.get('content-type','').startswith('image/');target.write_bytes(r.content)
 with Image.open(target) as im: im.verify()
 with Image.open(target) as im: wh=im.size
 return dict(id=name,providerPhotoId=photoid,file=f'assets/{name}.jpg',page=page,download=url,creator=author,sourceDescription=desc,license='Pexels License',licenseURL='https://www.pexels.com/license/',bytes=target.stat().st_size,width=wh[0],height=wh[1],sha256=hashlib.sha256(target.read_bytes()).hexdigest(),role='Illustrative stock photograph; no depicted person is asserted to overspend or endorse this video.',inspectionStatus='pending-root-inspection',sourcePageVerifiedVia='web.run search/open on 2026-11-13')
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:records=list(pool.map(one,rows))
(root/'source-candidates.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
for pi in range((len(records)+7)//8):
 sub=records[pi*8:(pi+1)*8];sheet=Image.new('RGB',(1600,1080),'#13161a');d=ImageDraw.Draw(sheet)
 for n,r in enumerate(sub):
  x=n%4*400;y=n//4*540
  with Image.open(root/r['file']) as im:
   thumb=ImageOps.contain(im.convert('RGB'),(392,485));sheet.paste(thumb,(x+(400-thumb.width)//2,y+35+(485-thumb.height)//2))
  d.text((x+8,y+8),r['id']+' / '+str(r['providerPhotoId']),fill='white')
 sheet.save(root/f'sources/candidates-{pi+1}.jpg',quality=85)
print(json.dumps({'photos':len(records),'bytes':sum(r['bytes'] for r in records),'largest':max(r['bytes'] for r in records)},ensure_ascii=False))
