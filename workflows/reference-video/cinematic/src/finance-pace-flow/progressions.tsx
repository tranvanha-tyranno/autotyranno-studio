import React from 'react';
import {C,type Context,action,arc,clamp,lerp,q} from './types';
import {Arrow,Bell,Bill,Button,Calendar,Camera,Cross,Cup,Envelope,Hand,House,Jar,Package,Paper,Path,Pen,Phone,Receipt,Scooter,Scissors,T,Tick,Wallet} from './art';

const caption=(text:string)=><T x={960} y={900} size={39}>{text}</T>;
const after=(c:Context)=>q(c.beatFrame,0,c.s.duration-2);
const writing=(x:number,y:number,label:string,u:number)=><Paper x={x} y={y} w={660} h={480}><T x={0} y={-150} size={35}>{label}</T>{[0,1,2].map(i=><Path key={i} d={`M-240 ${-40+i*87}H${-240+480*clamp(u*3-i*.55)}`} color={i===2?C.green:C.ink} width={6}/>)}</Paper>;

/** Consequences and checks after a short establishing shot. Each branch changes
 * the object state/operation instead of replaying the same entrance animation. */
export const Continuation:React.FC<Context>=c=>{
 const p=c.shot.part,u=c.u,act=action(c),global=after(c);
 if(c.s.id==='b04'){
  if(p===0)return null;
  if(p===1)return <Camera><Scooter x={620} y={490} scale={1.7} broken/><Envelope x={1410} y={485} label="LÚC XE HỎNG" amount="Chưa dành trước" scale={1.5} open={1}/><Cross x={1420} y={420} t={u}/>{caption('Minh muốn có khoảng thở khi cần.')}</Camera>;
  if(p===2)return <Camera><Envelope x={470} y={455} label="TĂNG THU NHẬP" amount="Có thêm" scale={1.5} open={1}/><Cup x={1370} y={465} scale={1.8}/><Bill x={lerp(460,1360,u)} y={270-Math.sin(u*Math.PI)*30} value="Chi thêm" scale={.85}/><Jar x={930} y={670} label="KHOẢNG ĐỆM" amount="Chưa giao việc" scale={.74} fill={0}/>{caption('Phần tăng chưa từng được dành cho việc đó.')}</Camera>;
  return <Camera>{Array.from({length:5},(_,i)=>{const t=q(c.f,i*8,c.shot.duration-3);return <g key={i}><Cup x={400+i*280} y={440} scale={.8}/><Bill x={400+i*280} y={lerp(180,300,t)} value="Lặp lại" scale={.6}/><Path d={`M${400+i*280} 620V${620+130*t}`} color={C.green} width={5}/></g>})}{caption('Khoản tăng dần trở thành thói quen.')}</Camera>;
 }
 if(c.s.id==='b05'){
  if(p===0)return null;
  if(p===1)return <Camera><Envelope x={430} y={420} label="THU" amount="Nhìn đủ" scale={1.15}/><Envelope x={940} y={420} label="CHI" amount="Cộng đủ" scale={1.15}/><Calendar x={1480} y={500} scale={.5} count={0} mark={30}/>{[0,1,2].map(i=>{const t=q(c.f,i*8,c.shot.duration-3);const [x,y]=arc([600+i*100,300],[1390+i*60,700],t,90);return <Receipt key={i} x={x} y={y} label="CẢ THÁNG" amount="Ghi lại" scale={.7}/>})}{caption('Từ phong bì → hóa đơn → kế hoạch 30 ngày.')}</Camera>;
  return <Camera><Receipt x={960} y={440} label="MỘT LỰA CHỌN" amount="Giữ hay đổi?" scale={2}/><Hand x={lerp(1630,1280,u)} y={570} scale={.85}/><Tick x={600} y={710} t={u}/><Cross x={1330} y={710} t={u}/>{caption('Nhìn rõ rồi mới quyết định.')}</Camera>;
 }
 if(c.s.id==='b16'){
  if(p===0)return null;
  if(p===1)return <Camera>{writing(970,465,'NGÀY · KHOẢN CHI · SỐ TIỀN · GHI CHÚ',global)}<Pen x={lerp(660,1240,u)} y={560} r={-30}/>{caption('Viết đủ thông tin để đối chiếu.')}</Camera>;
  return <Camera><Phone x={540} y={460} scale={1.15}><T x={0} y={-150} size={26}>DỮ LIỆU ĐANG CÓ</T><Path d="M-110-50H110M-110 20H110M-110 90H110" color={C.green} width={6}/><Button x={0} y={190} text="ĐÃ LƯU" w={250}/></Phone><Paper x={1380} y={440} w={620} h={480} r={4}><T x={0} y={-120} size={33}>THÊM TIỀN MẶT</T><Path d={`M-220-10H${-220+440*u}`} color={C.green}/><T x={0} y={140} size={36}>Bắt đầu từ dữ liệu thật.</T></Paper><Bill x={lerp(1550,1270,u)} y={lerp(130,300,u)} value="Tiền mặt" scale={.8}/></Camera>;
 }
 if(c.s.kind==='audit'&&p>0&&act!=='remove_duplicate_transfer'){
  if(p===1)return <Camera>{['CẦN GIỮ','KIỂM LẠI','THỬ ĐỔI'].map((l,i)=><g key={l}><Envelope x={430+i*530} y={600} label={l} amount="Gắn nhãn" scale={1.2} open={global}/><Receipt x={lerp(960,430+i*530,u)} y={lerp(160+i*25,440,u)} label="KHOẢN THỰC" amount="Đối chiếu" scale={.8}/></g>)}{caption('Đưa khoản thực vào đúng nhóm.')}</Camera>;
  if(p===2)return <Camera><Receipt x={720} y={460} label="KHOẢN CẦN KIỂM" amount="Công dụng?" scale={2}/><g transform={`translate(${lerp(1530,1190,u)} 430)`}><circle r={145} fill={C.blue} fillOpacity={.15} stroke={C.ink} strokeWidth={10}/><Path d="M-100 105L-210 230" width={30}/><T x={0} y={16} size={36}>TẦN SUẤT</T></g>{caption('Xem công dụng và tần suất, không đoán.')}</Camera>;
  return <Camera><Receipt x={960} y={430} label="CHỌN MỘT KHOẢN" amount="Thử đổi" scale={1.9}/><Cross x={550} y={500} t={u}/><Tick x={1400} y={500} t={u}/><Hand x={lerp(1800,1300,u)} y={670} scale={.8}/>{caption('Một thay đổi có thể kiểm tra.')}</Camera>;
 }
 if(act==='remove_duplicate_transfer'&&p>0){
  if(p===1)return <Camera><Wallet x={480} y={470} label="RÚT TIỀN MẶT" amount="Chưa biết đã mua gì" scale={1.5}/><Bill x={lerp(520,1350,u)} y={350-Math.sin(u*Math.PI)*80} value="Tiền mặt" scale={1.1}/><Envelope x={1410} y={540} label="CHƯA GHI LÀ CHI" amount="Chờ lúc mua thật" open={u} scale={1.3}/>{caption('Rút tiền chưa xác định khoản mua.')}</Camera>;
  return <Camera><Paper x={960} y={460} w={1300} h={540}><T x={-520} y={-130} anchor="start" size={38}>CHUYỂN NỘI BỘ</T><Path d={`M-520-95H${-520+1040*u}`} color={C.red} width={9}/><T x={-520} y={30} anchor="start" size={38}>RÚT TIỀN MẶT</T><Cross x={500} y={-30} t={u}/><T x={-520} y={190} anchor="start" size={38} color={C.green}>GHI KHI THỰC SỰ MUA HÀNG</T></Paper><Pen x={lerp(600,1480,u)} y={700} r={-20}/></Camera>;
 }
 if(act==='match_reimbursement'&&p>0){
  if(p===1)return <Camera><Receipt x={lerp(360,690,u)} y={440} label="TRẢ TRƯỚC" amount="Bữa ăn chung" scale={1.65}/><Receipt x={lerp(1580,1220,u)} y={440} label="HOÀN LẠI" amount="Phần của bạn" scale={1.65}/><Path d={`M690 700H${690+530*u}`} color={C.green} width={8}/>{caption('Ghép đúng hai giao dịch liên quan.')}</Camera>;
  if(p===2)return <Camera><Receipt x={500} y={400} label="ĐÃ TRẢ" amount="Toàn bữa ăn" scale={1.3}/><T x={820} y={450} size={90}>−</T><Receipt x={1130} y={400} label="ĐƯỢC HOÀN" amount="Phần người khác" scale={1.3}/><Arrow a={[1300,570]} b={[1490,720]} t={u}/><Envelope x={1520} y={720} label="PHẦN CỦA MÌNH" amount="Chi thực tế" scale={.9}/></Camera>;
  return <Camera><Wallet x={600} y={470} label="TIỀN HOÀN TRẢ" amount="Đối chiếu nguồn" scale={1.5}/><Receipt x={1420} y={440} label="CHI CỦA MÌNH" amount="Ghi đúng phần" scale={1.8}/><Cross x={960} y={465} t={u}/>{caption('Khoản hoàn trả không tự thành thu nhập mới.')}</Camera>;
 }
 if(act==='select_one_receipt'&&p>0){
  if(p===1)return <Camera>{[0,1,2,3].map(i=><g key={i} opacity={i<2?1:1-u}><Cup x={420+i*360} y={420} scale={.9}/><Receipt x={500+i*360} y={650} label="MỘT LẦN ĐẶT" amount="Xem lại" scale={.6}/></g>)}{caption('Thử bớt một lần hoặc kiểm một dịch vụ.')}</Camera>;
  if(p===2)return <Camera><Receipt x={650} y={430} label="LỜI HỨA CHUNG" amount="Tiết kiệm hơn" scale={1.7}/><Cross x={650} y={510} t={u} scale={1.7}/>{writing(1400,465,'MỘT THAY ĐỔI CỤ THỂ',u)}{caption('Cụ thể thì mới đo được.')}</Camera>;
  return <Camera><Calendar x={960} y={470} scale={1.25} count={0} mark={30}/><Pen x={lerp(500,1450,u)} y={785} r={-30}/>{caption('Đặt mốc kiểm lại thay cho danh sách cấm đoán.')}</Camera>;
 }
 if(act==='annual_calendar'&&p>0){
  if(p===1)return <Camera><House x={460} y={460} scale={1.4}/><Receipt x={1280} y={450} label="KHOẢN ÍT XUẤT HIỆN" amount="Vẫn dự kiến được" scale={1.8}/><Hand x={lerp(1800,1510,u)} y={590} scale={.8}/>{caption('Chưa tới hạn không có nghĩa là bất ngờ.')}</Camera>;
  return <Camera><Calendar x={960} y={470} scale={1.25} annual count={0}/>{['BẢO DƯỠNG','THAY ĐỒ DÙNG','ĐỊNH KỲ'].map((l,i)=>{const t=q(c.f,i*12,c.shot.duration-3);return <Receipt key={l} x={500+i*450} y={lerp(120,440+i%2*170,t)} label={l} amount="Dự kiến" scale={.75}/>})}</Camera>;
 }
 if(act==='reserve_envelope'&&p>0){
  if(p===1)return <Camera><Wallet x={480} y={470} label="ĐANG CÓ" amount="Chọn phần dự trù" scale={1.4}/><Envelope x={1440} y={470} label="THÁNG SAU" amount="Đã có nhãn" scale={1.5} open={1}/>{[0,1,2].map(i=><Bill key={i} x={lerp(480+i*40,1360+i*70,u)} y={260-Math.sin(u*Math.PI)*60} value="Dự trù" scale={.75}/>)}{caption('Tách vào nơi có nhãn rõ.')}</Camera>;
  if(p===2)return <Camera><Envelope x={500} y={450} label="TÚI A" amount="Đang giữ" scale={1.5}/><Envelope x={1400} y={450} label="TÚI B" amount="Đã giao việc" scale={1.5} open={u}/><Arrow a={[800,450]} b={[1110,450]} t={u}/><T x={960} y={735} size={64}>TỔNG TIỀN GIỮ NGUYÊN</T></Camera>;
  return <Camera><Envelope x={660} y={440} label="THÁNG SAU" amount="Tiền có nhiệm vụ" scale={1.5} open={0}/><Hand x={lerp(1630,1250,u)} y={530} scale={.95}/><Cross x={1170} y={530} t={u}/><Tick x={660} y={750} t={u}/>{caption('Có nhãn để tránh tiêu nhầm.')}</Camera>;
 }
 if(act==='walk_calendar_balance'&&p>0){
  if(p===1)return <Camera><Receipt x={450} y={420} label="HÓA ĐƠN TỚI" amount="Phải trả" scale={1.7}/><Wallet x={1390} y={450} label="TIỀN CHƯA VÀO" amount="Dễ thiếu" scale={1.55}/><Path d={`M750 570H${750+370*u}`} color={C.red} width={9}/><Cross x={960} y={570} t={u}/>{caption('Hóa đơn xuất hiện trước tiền vào.')}</Camera>;
  if(p===2)return <Camera><Calendar x={960} y={460} scale={1.25} count={0} mark={5}/><Receipt x={lerp(1800,450,u)} y={lerp(130,440,u)} label="TRẢ TRƯỚC" amount="Đúng ngày" scale={.8}/><Bill x={lerp(160,1520,u)} y={lerp(150,660,u)} value="VỀ SAU" scale={.8}/>{caption('Đây là vấn đề thời điểm.')}</Camera>;
  return <Camera><Paper x={650} y={460} w={720} h={500}><T x={0} y={-160} size={37}>MANG SỐ DƯ TỪNG NGÀY</T>{[0,1,2,3].map(i=><Path key={i} d={`M-240 ${-60+i*80}H${-240+480*clamp(u*4-i*.5)}`} color={i===2?C.red:C.green} width={7}/>)}</Paper><Calendar x={1460} y={475} scale={.43} count={0} mark={25}/><Pen x={lerp(500,850,u)} y={680} r={-20}/>{caption('Theo diễn biến trên lịch để nhận diện chỗ thiếu.')}</Camera>;
 }
 if(act==='bridge_due_date_gap'&&p>0){
  if(p===1)return <Camera><Jar x={570} y={450} label="KHOẢN ĐỆM" amount="Mức phù hợp" scale={1.35} fill={.4}/><Receipt x={1430} y={440} label="NGHĨA VỤ GẦN TỚI" amount="Cần trả" scale={1.65}/><Bill x={lerp(580,1410,u)} y={270-Math.sin(u*Math.PI)*55} value="Minh họa" scale={.8}/>{caption('Khoản đệm giúp bớt phụ thuộc ngay vào tiền mới.')}</Camera>;
  if(p===2)return <Camera><Calendar x={960} y={470} scale={1.25} count={0} mark={5}/><Cross x={lerp(500,1500,u)} y={600} t={1}/><Hand x={lerp(1790,1550,u)} y={750} scale={.7}/>{caption('Chưa tạo được? Nhận diện ngày dễ thiếu trước.')}</Camera>;
  return <Camera><Receipt x={520} y={430} label="LỊCH TRẢ HIỆN TẠI" amount="Đến hạn" scale={1.5}/><Receipt x={1390} y={430} label="CÓ THỂ THƯƠNG LƯỢNG?" amount="Kiểm điều kiện" scale={1.5}/><Arrow a={[790,520]} b={[1100,520]} t={u}/><Pen x={lerp(700,1510,u)} y={720} r={-30}/>{caption('Xem điều kiện, không tự mặc định được dời hạn.')}</Camera>;
 }
 if((c.s.kind==='automate')&&p>0){
  if(p===1)return <Camera><Phone x={510} y={455} scale={1.15}><T x={0} y={-160} size={28}>LỊCH ĐÃ ĐẶT</T><Button x={0} y={70} text="ĐÃ LƯU" w={250}/></Phone><Bell x={1430} y={380} scale={1.2} t={u}/><Envelope x={1430} y={680} label="ĐÚNG HẠN" amount="Có thời gian kiểm" scale={1.1}/><Hand x={lerp(1830,1600,u)} y={550} scale={.7}/></Camera>;
  if(p===2)return <Camera><Wallet x={500} y={470} label="KIỂM SỐ DƯ" amount="Cần đủ tiền" scale={1.5}/><Receipt x={1400} y={420} label="NGHĨA VỤ ĐẾN HẠN" amount="Tính trước" scale={1.7}/><Tick x={960} y={470} t={u} scale={1.5}/><Hand x={lerp(1800,1550,u)} y={650} scale={.8}/>{caption('Chuyển tự động vẫn cần kiểm số dư.')}</Camera>;
  return <Camera><Calendar x={720} y={470} scale={.85} count={0} mark={25}/><Phone x={1530} y={450} scale={.9}><T x={0} y={-145} size={26}>ĐỔI LỊCH?</T><Button x={0} y={60} text="XEM LẠI" w={250} t={u}/></Phone><Pen x={lerp(500,1050,u)} y={710} r={-30}/>{caption('Ngày lương hoặc nghĩa vụ đổi → xem lại lịch chuyển.')}</Camera>;
 }
 if(act==='monthly_vs_timing'&&p>0){
  if(p===1)return <Camera><Calendar x={860} y={470} scale={1.15} count={0} mark={5}/><Wallet x={1560} y={655} label="SẴN ĐÚNG NGÀY?" amount="Cần kiểm" scale={.9}/><Hand x={lerp(1750,1590,u)} y={450} scale={.65}/>{caption('Tới ngày trả, tiền đã sẵn chưa?')}</Camera>;
  if(p===2)return <Camera><Envelope x={480} y={420} label="THU" amount="Cả tháng" scale={1.35}/><Envelope x={1420} y={420} label="CHI" amount="Cả tháng" scale={1.35}/><T x={960} y={470} size={105}>−</T><Path d={`M400 680H${400+1120*u}`} color={C.green} width={8}/><T x={960} y={800} size={48}>KIỂM CÂN ĐỐI</T></Camera>;
  return <Camera><Tick x={650} y={450} t={u} scale={2}/><Tick x={1350} y={450} t={q(u,.25,.95)} scale={2}/><T x={650} y={650} size={50}>ĐỦ TỔNG</T><T x={1350} y={650} size={50}>ĐỦ ĐÚNG NGÀY</T>{caption('Hai phép kiểm khác nhau, hai chỗ có thể sửa.')}</Camera>;
 }
 if(act==='stop_cutting_essentials'&&p>0){
  if(p===1)return <Camera><Scissors x={480} y={470} open={1-u}/><Receipt x={lerp(820,1350,u)} y={450} label="HÓA ĐƠN QUAN TRỌNG" amount="Cần giữ" scale={1.9}/><Hand x={lerp(1740,1570,u)} y={490} scale={.75}/>{caption('Kéo khoản quan trọng ra khỏi chiếc kéo.')}</Camera>;
  if(p===2)return <Camera><Receipt x={560} y={430} label="SỨC KHỎE" amount="Cần giữ" scale={1.8}/><Receipt x={1390} y={430} label="NGHĨA VỤ" amount="Đã cam kết" scale={1.8}/><Tick x={560} y={735} t={u}/><Tick x={1390} y={735} t={u}/>{caption('Chừa chỗ cho các điều buộc phải bảo vệ.')}</Camera>;
  return <Camera><Scissors x={600} y={470} open={1}/><Cross x={600} y={470} t={u} scale={2}/><Envelope x={1400} y={450} label="ĐỪNG CHỈ LÀM ĐẸP SỐ" amount="Tính hệ quả" scale={1.6}/>{caption('Cắt điều cần thiết có thể khiến vấn đề lớn hơn.')}</Camera>;
 }
 if(act==='income_expense_gap'&&p>0)return <Camera>{p===1?<><House x={440} y={400} scale={1.15}/><Paper x={970} y={450} w={360} h={350}><T x={0} y={-65} size={35}>CÔNG VIỆC</T><Path d={`M-110 40H${-110+220*u}`} color={C.green}/></Paper><Envelope x={1510} y={450} label="SẮP XẾP NGHĨA VỤ" amount="Xem điều kiện" scale={1.15}/>{caption('Xem phương án lớn phù hợp với điều kiện thực tế.')}</>:<><Receipt x={550} y={440} label="MỖI PHƯƠNG ÁN" amount="Có điều kiện" scale={1.8}/><Phone x={1370} y={450} scale={1.1}><T x={0} y={-130} size={31}>BẠN QUYẾT ĐỊNH</T><Button x={0} y={60} text="ĐỐI CHIẾU" w={250} t={u}/></Phone><Hand x={lerp(1800,1600,u)} y={610} scale={.7}/></>}</Camera>;
 if(act==='same_total_different_jobs'&&p>0){
  if(p===1)return <Camera><Envelope x={470} y={430} label="CÓ NHIỆM VỤ" amount="Tránh tiêu nhầm" scale={1.5} open={0}/><Hand x={lerp(1750,1110,u)} y={510} scale={1}/><Cross x={1110} y={510} t={u}/><Jar x={1460} y={470} label="DÀNH CHO VIỆC CẦN" amount="Đã chuẩn bị" scale={1}/></Camera>;
  if(p===2)return <Camera><Wallet x={960} y={470} label="VÍ ĐẦU VIDEO" amount="Dư vẫn 2 triệu" scale={2}/><T x={960} y={180} size={58}>Chưa tự trở thành người giàu.</T><Hand x={lerp(1820,1470,u)} y={590} scale={.9}/></Camera>;
  return <Camera>{['TIÊU DÙNG','ĐÚNG HẠN','KHOẢNG ĐỆM'].map((t,i)=><g key={t}><Envelope x={430+i*530} y={520} label={t} amount="Đã có việc" scale={1.25} open={u}/><Bill x={lerp(960,430+i*530,u)} y={lerp(160+i*30,340,u)} value="Minh họa" scale={.75}/></g>)}{caption('Biết đồng nào đang dành cho việc gì.')}</Camera>;
 }
 if(act==='total_purchase_cost'&&p>0){
  if(p===1)return <Camera><Package x={470} y={450} scale={1.7}/><Receipt x={1280} y={lerp(160,430,u)} label="PHỤ KIỆN CẦN MUA" amount="Cộng vào" scale={1.9}/><Hand x={lerp(1850,1580,u)} y={570} scale={.8}/></Camera>;
  if(p===2)return <Camera><Receipt x={570} y={lerp(180,440,u)} label="GIAO NẾU CÓ" amount="Cộng đủ" scale={1.8}/><Receipt x={1390} y={lerp(260,440,u)} label="CHI PHÍ SỬ DỤNG" amount="Dự kiến" scale={1.8}/><T x={960} y={470} size={90}>+</T></Camera>;
  return <Camera><Paper x={960} y={470} w={1340} h={550}><T x={0} y={-170} size={48}>TỔNG TIỀN THỰC SỰ BỎ RA</T>{['Giá mua','Phụ kiện cần','Giao + sử dụng nếu có'].map((t,i)=><g key={t}><T x={-500} y={-55+i*100} size={33} anchor="start">{t}</T><Tick x={480} y={-68+i*100} t={clamp(u*3-i*.4)} scale={.6}/></g>)}</Paper><Pen x={lerp(450,1500,u)} y={760} r={-30}/></Camera>;
 }
 if(act==='installments_on_calendar'&&p>0){
  if(p===1)return <Camera><Receipt x={550} y={420} label="TỔNG TIỀN" amount="Kiểm đủ" scale={1.8}/><Receipt x={1390} y={420} label="PHÍ NẾU CÓ" amount="Đọc điều kiện" scale={1.8}/><T x={960} y={470} size={90}>+</T><Path d={`M350 730H${350+1200*u}`} color={C.green} width={8}/></Camera>;
  if(p===2)return <Camera><Calendar x={960} y={450} scale={1.15} count={0} mark={5}/>{[0,1,2,3].map(i=><Receipt key={i} x={500+i*300} y={lerp(120,420+(i%2)*200,q(c.f,i*9,c.shot.duration-3))} label={`LẦN TRẢ ${i+1}`} amount="Đến hạn" scale={.6}/>)}{caption('Đặt cạnh các nghĩa vụ cũ trên cùng lịch.')}</Camera>;
  return <Camera><Receipt x={560} y={440} label="SỐ NHỎ HÔM NAY" amount="Còn hẹn" scale={1.8}/><Arrow a={[830,480]} b={[1100,480]} t={u}/><Calendar x={1420} y={460} scale={.5} count={0} mark={30}/>{caption('Khoản trả hôm nay vẫn đi cùng lời hẹn phía sau.')}</Camera>;
 }
 if(act==='pause_purchase'&&p>0){
  if(p===1)return <Camera>{writing(720,470,'ĐỐI CHIẾU KẾ HOẠCH',u)}<Package x={1530} y={500} scale={1.2}/><Pen x={lerp(480,920,u)} y={670} r={-25}/>{caption('Khoảng dừng tạo thời gian kiểm lại, không bảo đảm chọn đúng.')}</Camera>;
  return <Camera><Wallet x={550} y={460} label="ĐỦ KHẢ NĂNG?" amount="Kiểm trước" scale={1.5}/><Package x={1430} y={470} scale={1.6}/><Tick x={960} y={480} t={u} scale={1.8}/><Hand x={lerp(1830,1640,u)} y={570} scale={.8}/>{caption('Vẫn cần và đủ khả năng thì mua có thể hợp lý.')}</Camera>;
 }
 if(act==='useful_vs_unused'&&p>0){
  if(p===1)return <Camera><Scooter x={650} y={450} scale={1.6} wheel={u*220}/><Calendar x={1450} y={450} scale={.48} count={Math.round(u*30)}/>{caption('Đồ dùng lâu và giải quyết nhu cầu có thể đáng tiền hơn.')}</Camera>;
  if(p===2)return <Camera><Package x={480} y={450} scale={1.5}/><Cross x={480} y={450} t={u} scale={1.6}/><Scooter x={1410} y={460} scale={1.4} wheel={u*160}/><Tick x={1420} y={740} t={u}/>{caption('Giữ lựa chọn cần thiết, bỏ món không còn muốn.')}</Camera>;
  return <Camera><Envelope x={500} y={450} label="ƯU TIÊN THẬT" amount="Giữ" scale={1.5} open={1}/><Bill x={lerp(1320,500,u)} y={260} value="Dành ra" scale={1}/><Package x={lerp(1390,1740,u)} y={530} scale={1.3}/>{caption('Chủ động chọn ưu tiên của mình.')}</Camera>;
 }
 if(act==='one_change'&&p>0){
  if(p===1)return <Camera>{writing(960,470,'CÁCH ĐỔI + MỐC KIỂM',u)}<Pen x={lerp(650,1200,u)} y={650} r={-30}/></Camera>;
  if(p===2)return <Camera><Cup x={600} y={440} scale={1.3}/><Receipt x={600} y={700} label="MỨC CHI THÊM" amount="Thử thấp hơn" scale={.8}/><Envelope x={1420} y={480} label="BỮA GẶP BẠN" amount="Vẫn giữ" scale={1.5}/><Tick x={1420} y={735} t={u}/></Camera>;
  return <Camera><Receipt x={960} y={450} label="MỘT VIỆC CỤ THỂ" amount="Có thể kiểm" scale={2}/><Tick x={1450} y={500} t={u} scale={1.4}/>{caption('Một lựa chọn cụ thể, thay cho danh sách cấm đoán dài.')}</Camera>;
 }
 if(c.s.kind==='review'&&p>0){
  if(p===1)return <Camera><Phone x={500} y={455} scale={1.1}><T x={0} y={-150} size={27}>THỰC TẾ THÁNG NÀY</T><Path d="M-110-60H110M-110 20H110M-110 100H110" color={C.green}/></Phone>{writing(1380,460,'ĐỐI CHIẾU DỮ LIỆU',u)}<Pen x={lerp(1150,1620,u)} y={650} r={-25}/></Camera>;
  if(p===2)return <Camera><Receipt x={550} y={430} label="CHỖ CHÊNH LỆCH" amount="Tìm nguyên nhân" scale={1.8}/><Envelope x={1420} y={440} label="GIẢ ĐỊNH CẦN SỬA" amount="Cập nhật" scale={1.5} open={u}/><Arrow a={[810,520]} b={[1110,520]} t={u}/>{caption('Dữ liệu mới giúp sửa kế hoạch, không chấm điểm bản thân.')}</Camera>;
  return <Camera><Calendar x={960} y={450} scale={1.17} count={0} mark={30}/><Pen x={lerp(380,1450,u)} y={760} r={-30}/>{caption('Điều chỉnh rồi đặt ngày xem lại.')}</Camera>;
 }
 return null;
};

export const hasContinuation=(c:Context)=>c.shot.part>0&&(
 ['b04','b05','b16'].includes(c.s.id)||
 (c.s.kind==='audit'&&!Array.isArray(c.s.data?.fields))||
 ['match_reimbursement','select_one_receipt','annual_calendar','reserve_envelope','walk_calendar_balance','bridge_due_date_gap','monthly_vs_timing','stop_cutting_essentials','income_expense_gap','same_total_different_jobs','total_purchase_cost','installments_on_calendar','pause_purchase','useful_vs_unused','one_change'].includes(action(c))||
 c.s.kind==='automate'||c.s.kind==='review'
);
