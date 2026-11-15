"""Sentence-driven image/clip assignment, measured non-overlapping stock intervals."""
import json,sys,math
from pathlib import Path
root=Path(__file__).resolve().parent
sys.path.insert(0,str(root.parents[1]/'workflows/reference-video'))
import production
content=production.load(root/'content.json');words=production.load(root/'aligned-words.json')
catalog=production.load(root/'sources-candidates.json');assets={a['id']:a for a in catalog}
beats=[b for c in content['chapters'] for b in c['beats']];starts=[];cursor=0
for b in beats:
 starts.append(0 if not starts else round(words[cursor]['start']*30));cursor+=len(production.normalized_words(b['text']))
last=math.ceil((production.load(root/'audio/narration.receipt.json')['seconds']+1.5)*30)
dur={b['id']:(starts[i+1] if i+1<len(starts) else last)-starts[i] for i,b in enumerate(beats)}
M={
'h01':['clip-busy-cafe','clip-espresso-extract','vn-hue-cafe'],
'h02':['vn-rin-cafe-cup','vn-saigon-coffee-phin','vn-dalat-cafe'],
'h03':['clip-espresso-flow'],
'd01':['vn-rin-cafe-cup'],
'u01':['clip-phone-payment','vn-hanoi-cup'],
'u02':['clip-espresso-grinder','clip-pour-milk','vn-saigon-coffee-food'],
'u03':['vn-hanoi-cup'],
'u04':['vn-saigon-coffee-phin'],
'u05':['global-milk-frothing','global-milk-pour'],
'u06':['clip-steam-milk','global-milk-frothing','vn-saigon-coffee-phin'],
'u07':['clip-pour-milk','vn-saigon-coffee-food','global-milk-pour'],
'u08':['vn-hanoi-cup'],
'u09':['clip-cafe-tables','vn-hue-cafe','vn-rin-cafe-cup'],
'b01':['vn-cafe-tayho'],
'b02':['vn-cafe-tayho','vn-cafe-oxy-tables'],
'b03':['vn-hanoi-cup'],
'b04':['vn-saigon-coffee-phin'],
'b05':[],
'b06':['vn-rin-cafe-cup'],
'b07':[],
'b08':['clip-close-shift','global-milk-frothing','vn-cafe-oxy-tables'],
'v01':['clip-cafe-tables','vn-cafe-oxy-tables','vn-hue-cafe'],
'v02':[],
'v03':['clip-serve-coffee','vn-saigon-coffee-food','vn-rin-cafe-cup'],
'v04':['vn-hue-cafe','vn-cafe-oxy-tables'],
'v05':['clip-steam-milk','global-milk-frothing','clip-espresso-extract'],
'v06':['vn-hanoi-cup'],
'p01':['global-milk-pour'],
'p02':[],
'p03':['vn-hanoi-cup'],
'p04':[],
'p05':['vn-saigon-coffee-phin'],
'p06':['clip-serve-coffee','vn-hanoi-cup','vn-rin-cafe-cup'],
'p07':['vn-rin-cafe-cup','vn-saigon-coffee-food'],
'p08':['vn-cafe-oxy-tables','vn-hue-cafe','vn-rin-cafe-cup'],
'p09':['vn-hanoi-cup'],
'm01':['vn-dalat-cafe'],
'm02':['vn-saigon-coffee-phin','vn-rin-cafe-cup'],
'm03':['coffee-roast-location-unverified'],
'm04':['vn-cafe-tayho'],
'm05':['clip-espresso-flow','clip-espresso-extract','global-espresso-extraction'],
'm06':['vn-hanoi-cup','vn-saigon-coffee-food'],
'm07':[],
'm08':['vn-dalat-cafe'],
'm09':['vn-cafe-oxy-tables'],
'a01':['clip-close-shift','vn-dalat-cafe','vn-cafe-tayho'],
'a02':['vn-hanoi-cup'],
'a03':['clip-serve-coffee','global-milk-frothing','vn-cafe-tayho'],
'a04':['vn-hue-cafe','vn-cafe-oxy-tables','vn-rin-cafe-cup'],
'a05':['clip-espresso-extract','global-milk-pour','vn-saigon-coffee-food'],
'a06':['vn-rin-cafe-cup','vn-hanoi-cup'],
'a07':['vn-cafe-oxy-tables'],
'a08':['clip-espresso-flow','global-milk-frothing','vn-saigon-coffee-phin'],
'e01':['clip-busy-cafe','vn-hue-cafe','vn-rin-cafe-cup'],
'e02':['vn-saigon-coffee-phin'],
'e03':['clip-serve-coffee','global-milk-pour','vn-hanoi-cup'],
'e04':['vn-dalat-cafe'],
'e05':['clip-close-shift','vn-cafe-oxy-tables','vn-hanoi-cup'],
}
# Mechanisms show their relation directly; photographs only carry contextual facts.
byid={b['id']:b for b in beats}
byid['b03']['layout']='b-paper';byid['b03']['design']={'paper':{'title':'CÔNG THỨC HÒA VỐN / GIẢ ĐỊNH','rows':[{'label':'Chi phí cố định/tháng','value':'48.000.000đ'},{'label':'Phần đóng góp/ly','value':'÷20.000đ'}],'total':{'label':'Số ly/tháng','value':'2.400 ly'}}}
byid['m03']['layout']='b-paper';byid['m03']['design']={'paper':{'title':'HAI THỜI ĐIỂM KHÁC NHAU','rows':[{'label':'Trả tiền mua nguyên liệu','value':'Hôm nay'},{'label':'Dùng nguyên liệu để bán','value':'Dần nhiều tuần'}],'total':{'label':'Hàng còn lại','value':'Cần theo dõi'}}}
byid['m06']['layout']='b-split';byid['m06']['design']={'choices':[{'label':'TẠI QUẦY','title':'Tiền thu ngay','body':'Khi thực sự được thanh toán'},{'label':'KÊNH ĐỐI SOÁT','title':'Tiền chuyển về sau','body':'Tùy thỏa thuận cụ thể'}]}
byid['d01']['headline']='Một quán giả định. Một mô hình đơn giản.'
byid['d01']['eyebrow']='MIỄN TRỪ TRÁCH NHIỆM'
byid['d01']['body']='Giá và chi phí đều giả định. Chưa tính thuế, lãi vay, khấu hao. Nội dung giáo dục, không tư vấn riêng cho một cơ sở.'
byid['h01']['eyebrow']='QUÁN GIẢ ĐỊNH / TƯ LIỆU MINH HỌA'
byid['b07']['body']='*Phần dư mô hình, trước thuế, lãi vay và khấu hao.'
byid['m07']['body']='Tình huống tuần riêng biệt — không ghép vào phép tính tháng.'
byid['h03']['body']='35.000đ là giá bán giả định, không phải giá của quán trong ảnh.'
byid['u04']['body']='Còn phải góp trả chi phí cố định của cả tháng.'
byid['b04']['body']='Chỉ bù các chi phí đã đưa vào mô hình.'
byid['e02']['body']='Phần đóng góp · Sản lượng hòa vốn · Lịch thu–chi'
byid['a02']['body']='Tính phí và trợ giá quán chịu đúng một lần; không trừ trùng.'
for b in beats:
 if b['id']!='d01' and b['layout'] in {'b-chart','b-paper','b-coffee'}:b['eyebrow']='MÔ HÌNH GIẢ ĐỊNH'
 if b['layout']=='b-photo':b['design'].setdefault('theme','dark')
 elif b['layout']=='b-chart':b['design'].setdefault('theme','cream')
 elif b['layout']=='b-paper':b['design'].setdefault('theme','cream')

cues={
'h02':['Có thể mỗi đơn','hoặc tiền phải chi'],
'u03':['ba mươi lăm trừ','mười lăm','hai mươi nghìn'],
'u04':['Hai mươi nghìn ấy','Tiền thuê nhà','cả tháng'],
'u05':['Nhân viên','làm thêm giờ'],
'b01':['mười tám triệu','hai mươi hai triệu','là tám triệu'],
'b03':['bốn mươi tám triệu','Chia ra','hai nghìn bốn trăm'],
'b04':['Nếu mở đủ','tám mươi ly','chưa bảo đảm'],
'b06':['một trăm lẻ năm','bốn mươi lăm','sáu mươi triệu'],
'b07':['Trả tiếp','Trả tiếp','bốn mươi tám triệu','mười hai triệu'],
'v02':['sáu mươi ly','mười ly','bảy mươi'],
'p01':['hai mươi chín nghìn','mười lăm nghìn','mười bốn nghìn'],
'p02':['hai mươi','mười bốn','ba mươi phần trăm'],
'p03':['sáu mươi triệu','bốn nghìn hai trăm tám mươi lăm','bốn nghìn hai trăm tám mươi sáu'],
'p04':['bốn mươi ba phần trăm'],
'p05':['bốn mươi tám triệu','ba nghìn bốn trăm hai mươi chín','một trăm mười lăm'],
'm02':['Một bên','Bên kia'],
'm03':['tiền ra ngay','hàng vẫn còn trong kho'],
'm04':['Đặt cọc','không đơn giản'],
'm07':['hai mươi triệu','mười lăm triệu','bốn mươi triệu','Thiếu năm triệu'],
'm09':['số dư đầu kỳ','tiền dự kiến thu','khoản phải chi'],
'a02':['giá thực thu','chi phí trực tiếp'],
'a07':['phần đóng góp mỗi đơn','lượng đơn','lịch tiền mặt'],
}
videoCursor={};intervals=[];plan=[]
for b in beats:
 media=M[b['id']];images=[]
 for j,aid in enumerate(media):
  a=assets[aid]
  if a.get('type')=='video':
   slot=dur[b['id']]/len(media) if b['layout'] in {'b-photo','b-closing'} else dur[b['id']]
   start=videoCursor.get(aid,0);length=math.ceil(slot)
   available=math.floor(a['duration']*30)
   if start+length>available:
    fallback={'clip-espresso-flow':'global-espresso-extraction','clip-espresso-extract':'global-espresso-extraction',
      'clip-serve-coffee':'vn-hanoi-cup','clip-busy-cafe':'vn-hue-cafe','clip-cafe-tables':'vn-rin-cafe-cup',
      'clip-steam-milk':'global-milk-frothing','clip-pour-milk':'global-milk-pour','clip-phone-payment':'vn-hanoi-cup','clip-close-shift':'vn-cafe-oxy-tables'}[aid]
    aid=fallback;images.append(aid);continue
   images.append({'id':aid,'trimBeforeFrames':start});videoCursor[aid]=start+length+5
   intervals.append({'shot':b['id'],'asset':aid,'start':start,'end':start+length,'fps':30})
  else:images.append(aid)
 unique=[assets[i if isinstance(i,str) else i['id']] for i in images]
 credits=[]
 for a in unique:
  item=a['creator']+' / '+a['license']
  if item not in credits:credits.append(item)
 note='Tư liệu minh họa · '+'; '.join(credits)
 if b['layout'] in {'b-paper','b-chart','b-coffee','b-split','b-question'}:note='Mô hình minh họa gốc'+(' · Ảnh: '+'; '.join(credits) if credits else '')
 if b['id'] in {'b03','b05'}:note+=' · Công thức: SBA'
 if b['id'] in {'m02','m04','m09'}:note+=' · Tham khảo: Business Queensland / business.gov.au'
 need=('Real source media show only their inspected visible cafe/coffee/service subjects. '+
       'The narration is an explicitly fictional business model; this is not evidence of the photographed business revenue, cost, occupancy trend, failure or customer intent. ')
 if b['design'].get('chart'):need+='Original animated chart must show exact authored values, units and scope: '+json.dumps(b['design']['chart'],ensure_ascii=False)
 elif b['design'].get('paper'):need+='Original animated paper must reveal the written computation/timing relation: '+json.dumps(b['design']['paper'],ensure_ascii=False)
 elif b['design'].get('choices'):need+='Original choices distinguish the spoken concepts: '+json.dumps(b['design']['choices'],ensure_ascii=False)
 else:need+='Context slots: '+' | '.join(a['inspection']['observedSubjectAction'] for a in unique)
 row={'id':b['id'],'images':images,'sourceNote':note,'needToSee':need}
 if b['id'] in cues:row['cuePhrases']=cues[b['id']]
 plan.append(row)
for c in content['chapters']:c['text']=' '.join(b['text'] for b in c['beats'])
production.save(root/'content.json',content)
production.save(root/'visual-plan.json',{'schema':'business-visual-plan/1','shots':plan,'reviewScope':'Root opened all4photo sheets and3video sheets, actual sampled source pixels. Rendered crop/motion inspection remains pending.'})
production.save(root/'clip-intervals.json',{'intervals':intervals,'policy':'Normal playback; no loops, no repeated source interval. Intervals normalized to30fps even if source rate differs.'})
print('Selected',len({x for v in M.values() for x in v}),'source assets;',len(intervals),'non-overlapping clip placements;',round(sum(x['end']-x['start'] for x in intervals)/30,2),'moving seconds.')
