"""Diverse original diagrams/maps/data, zero repeated photographic appearances."""
import json,sys
from pathlib import Path
r=Path(__file__).resolve().parent;sys.path.insert(0,str(r.parents[1]/'workflows/reference-video'));import production
d=production.load(r/'content.json');B={b['id']:b for c in d['chapters'] for b in c['beats']}
B['e04']['layout']='c-question'
def flow(sid,labels,edges=None,columns=None):
 nodes=[{'id':str(i),'label':label,'column':columns[i] if columns else i} for i,label in enumerate(labels)]
 links=[{'from':str(i),'to':str(j),'value':1} for i,j in (edges or [(i,i+1) for i in range(len(nodes)-1)])]
 B[sid]['design']['flow']={'nodes':nodes,'links':links,'note':'Sơ đồ cơ chế · Độ rộng liên kết không biểu thị quy mô thống kê.'}
def compare(sid,cols):B[sid]['design']['comparison']={'columns':[{'label':a,'title':b,'body':c} for a,b,c in cols]}
def chart(sid,kind,items,unit,maximum,**kw):B[sid]['design']['chart']={'kind':kind,'items':[{'label':a,'value':b} for a,b in items],'unit':unit,'max':maximum,**kw}
def sim(sid,kind,items,note):B[sid]['design']['simulation']={'kind':kind,'items':[{'label':a,'value':b} for a,b in items],'note':note}
cn=[{'id':'sh','label':'Thượng Hải','lon':121.47,'lat':31.23},{'id':'sz','label':'Thâm Quyến','lon':114.06,'lat':22.54},{'id':'cq','label':'Trùng Khánh','lon':106.55,'lat':29.56},{'id':'bj','label':'Bắc Kinh','lon':116.4,'lat':39.9}]
def map_(sid,nodes=cn,links=None,mode='regions',note='Vị trí địa lý thực; liên kết minh họa, không phải số liệu dòng hàng.'):
 B[sid]['design']['map']={'mode':mode,'nodes':nodes,'links':links or [{'from':'cq','to':'sh'},{'from':'sz','to':'sh'},{'from':'bj','to':'sh'}],'note':note}
map_('o01');flow('o02',['Năng lực sản xuất','Thu nhập','Nhu cầu'],[(0,1),(1,2),(2,0)])
compare('o03',[('01','Động cơ sản xuất','Các ngành khác nhịp'),('02','Nhà ở và sức mua','Dòng tiền và niềm tin'),('03','Cấu trúc dài hạn','Thương mại và dân số')])
B['o04']['eyebrow']='MIỄN TRỪ TRÁCH NHIỆM';B['o04']['body']='Số liệu có kỳ đo và nguồn riêng. Mô phỏng giải thích cơ chế; không phải dự báo hoặc khuyến nghị đầu tư.'
map_('f01');sim('f02','factory',[('Linh kiện',3),('Lắp ráp',3),('Kiểm tra',3)],'Dây chuyền minh họa · Chuyển động không đo năng suất thực.')
flow('f03',['Nhà cung cấp','Kỹ năng','Dịch vụ','Cụm sản xuất'],[(0,3),(1,3),(2,3)],[0,0,0,1])
sim('f04','factory',[('Công suất',8),('Đơn hàng',5),('Đầu ra',5)],'Ví dụ giả định · Công suất có thể khác lượng đơn hàng.')
chart('f05','bars',[('Chế tạo',5.6)],'% cùng kỳ · giá so sánh',7)
chart('f06','bars',[('Chế tạo',5.6),('Xây dựng',-4.1),('Dịch vụ',5.2)],'% cùng kỳ · giá so sánh',7,min=-5)
compare('f07',[('SUY QUÁ XA','Một ngành tốt','Không đại diện mọi hộ'),('SUY QUÁ XA','Một ngành khó','Không xóa mọi năng lực')])
flow('f08',['Sản lượng','Tiền lương/thu nhập','Nhu cầu','Đơn hàng'],[(0,1),(1,2),(2,3)])
flow('r01',['Người mua','Chủ đầu tư','Nhà thầu','Ngân hàng','Địa phương'],[(0,1),(3,1),(1,2),(1,4)],[0,1,2,0,2])
sim('r02','property',[('Người mua',1),('Dự án',1),('Nhà thầu',1)],'Minh họa lịch tiền · Không mô tả một dự án/doanh nghiệp cụ thể.')
flow('r03',['Tiền thu dự án','Tiến độ xây dựng','Nhận nhà/niềm tin','Vật liệu/việc làm'],[(0,1),(1,2),(1,3)],[0,1,2,2])
chart('r04','bars',[('Đầu tư phát triển BĐS',-20.6)],'% cùng kỳ · 1–9/2026',5,min=-25)
B['r04']['body']='Chỉ tiêu đầu tư; không phải mức giảm giá của mọi căn nhà.'
sim('r05','household',[('Tiêu dùng',45),('Nghĩa vụ',30),('Dự phòng',25)],'Phân bổ giả định để giải thích lựa chọn · Không phải cơ cấu hộ Trung Quốc.')
flow('r06',['Dự án dở dang','Hoàn thành nghĩa vụ','Xử lý tổn thất','Niềm tin'],[(0,1),(0,2),(1,3),(2,3)],[0,1,1,2])
compare('r07',[('NGHĨA VỤ CŨ','Hoàn thiện dự án','Thực hiện cam kết đã có'),('CAM KẾT MỚI','Xây thêm','Cần nhu cầu và hiệu quả')])
flow('h01',['Doanh nghiệp','Thu nhập hộ','Chi tiêu','Doanh thu'],[(0,1),(1,2),(2,3),(3,0)])
sim('h02','household',[('Tiêu dùng',50),('Nghĩa vụ',30),('Dự phòng',20)],'Minh họa quyết định chi · Không đo tỷ lệ thực tế.')
sim('h03','household',[('Tiêu dùng',50),('Trả nghĩa vụ',25),('Dự phòng',25)],'100 phần thu nhập giả định · Các tỷ trọng không phải số liệu Trung Quốc.')
chart('h04','bars',[('Danh nghĩa',3.6),('Thực',2.7)],'% cùng kỳ · chi tiêu bình quân đầu người',5)
compare('h05',[('THỐNG KÊ','Bình quân','Một số tổng hợp'),('THỰC TẾ HỘ','Khác hoàn cảnh','Phân bố có thể khác xa')])
flow('h06',['Bán lẻ hàng hóa','Phạm vi dịch vụ','Khảo sát hộ','Tiêu dùng trong GDP'],[(0,3),(1,3),(2,3)],[0,0,0,1])
flow('h07',['Thu nhập','An sinh','Niềm tin','Điều kiện để chi'],[(0,3),(1,3),(2,3)],[0,0,0,1])
sim('h08','factory',[('Năng lực',8),('Đơn hàng',4),('Bán được',4)],'Minh họa điểm nghẽn · Giá trị trên hình không phải dữ liệu thực.')
world=[{'id':'cn','label':'Trung Quốc','lon':116,'lat':32},{'id':'vn','label':'Đông Nam Á','lon':106,'lat':15},{'id':'eu','label':'Châu Âu','lon':9,'lat':51},{'id':'us','label':'Bắc Mỹ','lon':-98,'lat':39},{'id':'af','label':'Châu Phi','lon':20,'lat':2}]
links=[{'from':'cn','to':a} for a in ['vn','eu','us','af']]
map_('t01',world,links,'routes','Sơ đồ kết nối thương mại · Không phải tuyến tàu thực hoặc quy mô kim ngạch.')
flow('t02',['Đầu vào nhập khẩu','Sản xuất trong nước','Xuất khẩu','Nhu cầu nội địa'],[(0,1),(1,2),(1,3)],[0,1,2,2])
chart('t03','waterfall',[('Xuất khẩu',10),('Nhập khẩu',-7),('Chênh lệch',3)],'đơn vị giả định',12)
B['t03']['body']='Phép trừ trong cách tính GDP · Nhập khẩu không đồng nghĩa “xấu”.'
chart('t04','waterfall',[('Xuất tăng',10),('Nhập tăng',-7),('Chênh tăng',3)],'đơn vị giả định · không phải đóng góp thực',12)
map_('t05',world,links,'routes','Đa dạng thị trường, điều kiện cạnh tranh · Sơ đồ không đo đơn hàng.')
map_('t06',[cn[0],cn[1],world[1],world[2]],[{'from':'sz','to':'vn'},{'from':'vn','to':'eu'},{'from':'sh','to':'eu'}],'routes','Một cấu hình giả định · Đường nối mới không chứng minh cả chuỗi đã chuyển đi.')
flow('t07',['Kim ngạch gộp','Chi phí/giá trị thêm','Kết quả doanh nghiệp','Thu nhập hộ'],[(0,1),(1,2),(2,3)])
sim('d01','cohorts',[('Dưới 60',77),('Từ 60 trở lên',23)],'Cơ cấu tuổi cuối 2025 theo NBS · 23% là nhóm60+, không phải65+.')
compare('d02',[('MỐC ĐƯỢC DÙNG','60 tuổi trở lên','23% cuối2025'),('MỐC KHÁC','65 tuổi trở lên','Không dùng lại con số23%')])
flow('d03',['Cơ cấu tuổi','Chăm sóc/an sinh','Lao động','Kế hoạch hộ'],[(0,1),(0,2),(0,3)],[0,1,1,1])
sim('d04','factory',[('Kỹ năng',3),('Công cụ',4),('Quy trình',5)],'Minh họa năng suất · Không dự báo sản lượng hay việc làm.')
compare('d05',[('CƠ HỘI','Công nghệ/kỹ năng','Cần hiệu quả thực'),('ĐIỀU KIỆN','Vốn/chuyển đổi','Tác động khác từng ngành')])
flow('d06',['Năng suất','Đào tạo','Hỗ trợ chuyển đổi','Khả năng thích ứng'],[(0,3),(1,3),(2,3)],[0,0,0,1])
chart('p01','bars',[('GDP 9 tháng',4.6)],'% cùng kỳ · giá so sánh',6)
chart('p02','line',[('Q1',5),('Q2',4.3),('Q3',4.5)],'% cùng kỳ · 2026',6,min=0)
flow('p03',['Nguồn hỗ trợ','Đầu tư','Hộ gia đình','Nghĩa vụ cũ','Cầu/hiệu quả'],[(0,1),(0,2),(0,3),(1,4),(2,4),(3,4)],[0,1,1,1,2])
sim('p04','factory',[('Đầu tư',8),('Nhu cầu',5),('Sử dụng',5)],'Tình huống giả định · Không phải dự báo một chính sách.')
sim('p05','household',[('Chi tiêu',55),('Nghĩa vụ',25),('Dự phòng',20)],'Một phân bổ giả định để nói về điều kiện chi tiêu, không phải khuyến nghị tỷ trọng.')
flow('p06',['Nghĩa vụ cũ','Xử lý thực','Chuyển bảng cân đối','Rủi ro còn lại'],[(0,1),(0,2),(2,3)],[0,1,1,2])
compare('p07',[('CẦN ĐỌC','Kỳ đo/điều kiện','Không suy từ một ảnh'),('CẦN ĐỐI CHIẾU','Ngành/địa phương','Không một kết cục duy nhất')])
flow('e01',['Sản xuất','Nhà ở','Thu nhập hộ','Thương mại','Niềm tin'],[(0,2),(1,2),(3,0),(2,4)],[0,0,1,0,2])
sim('e02','household',[('Tiêu dùng',50),('Nghĩa vụ',25),('Dự phòng',25)],'Sơ đồ kết nối khái niệm · Không là cơ cấu thu nhập thực.')
compare('e03',[('01','Kỳ đo nào?','Cùng kỳ hay liền quý'),('02','Giá và đại lượng?','Danh nghĩa/thực; mức/tăng'),('03','Phạm vi nào?','Có đúng điều kết luận?')])
# Each chapter changes tone, not identity. No repeated source frames are filler.
themes=['dark','cream','warm','cream','dark','cream','warm','dark']
plans=[]
for i,c in enumerate(d['chapters']):
 for b in c['beats']:
  b['design'].setdefault('theme',themes[i]);b['eyebrow']=b.get('eyebrow',('SỐ LIỆU CÓ NGUỒN' if b['layout']=='c-chart' or b['id']=='d01' else 'CƠ CHẾ VÀ KẾT NỐI'))
  if b['id'] in {'t03','t04'}:b['eyebrow']='VÍ DỤ SỐ HỌC GIẢ ĐỊNH'
  source='Đồ họa cơ chế gốc · Không biểu thị quy mô thống kê'
  if b['id'] in {'f05','f06','p01','p02'}:source='Nguồn: NBS · 1–9/2026 · Giá so sánh · Ước tính sơ bộ'
  if b['id']=='r04':source='Nguồn: NBS · Đầu tư phát triển BĐS 1–9/2026 · So với cùng kỳ'
  if b['id']=='h04':source='Nguồn: NBS · Chi tiêu bình quân đầu người 1–9/2026 · Danh nghĩa và thực'
  if b['id'] in {'d01','d02'}:source='Nguồn: NBS · Cuối2025 · Nhóm60+ · Phạm vi dân số theo công bố'
  if b['id'] in {'r06','h07'}:source='Tham khảo: World Bank7/2026; IMF ArticleIV2025 công bố2026 · Sơ đồ giải thích'
  if b['id'] in {'t03','t04'}:source='Số học giả định · Không phải số liệu xuất/nhập khẩu hay đóng góp GDP thực'
  plans.append({'id':b['id'],'images':[],'sourceNote':source,'needToSee':'Original authored '+b['layout']+' exactly depicting this narrated mechanism; data facts retain period/unit/source and simulation numbers are explicitly illustrative.'})
production.save(r/'content.json',d);production.save(r/'visual-plan.json',{'shots':plans,'policy':'No photo repeated; no clip interval repeated; no still/footage loops.'})
if not(r/'sources-candidates.json').exists():production.save(r/'sources-candidates.json',[])
catalog=production.load(r/'sources-candidates.json')
if catalog:
 assets={a['id']:a for a in catalog};planById={p['id']:p for p in plans}
 contexts={'f07':['cn-auto-assembly','cn-toy-assembly-workers'],
  'h05':['cn-clip-guangzhou-retail','cn-shanghai-supermarket'],
  'd05':['cn-industry-robots','cn-silk-suzhou'],
  'e04':['cn-clip-shenzhen-night','cn-shanghai-skyline']}
 for sid,ids in contexts.items():
  B[sid]['layout']='c-closing' if sid=='e04' else 'c-photo'
  planById[sid]['images']=ids
  planById[sid]['sourceNote']='Tư liệu Trung Quốc minh họa · '+'; '.join(assets[k]['creator']+' / '+assets[k]['license'] for k in ids)
  planById[sid]['needToSee']='Actual inspected China context; people/businesses are not asserted to represent average incomes, actual profits, job losses or causal effects. '+ ' | '.join(assets[k]['inspection']['observedSubjectAction'] for k in ids)
 production.save(r/'content.json',d);production.save(r/'visual-plan.json',{'shots':plans,'policy':'Each new photo/clip ID used once; normal video speed; no loop/repeated interval.'})
production.save(r/'clip-intervals.json',{'intervals':[],'policy':'Data graphics first. Any later footage selected once, native speed.'})
print('Authored original designs for',len(plans),'beats.')
