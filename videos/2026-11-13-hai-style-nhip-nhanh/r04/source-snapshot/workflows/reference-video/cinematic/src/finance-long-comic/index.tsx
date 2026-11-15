import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Actor, Arrow, Bag, Bubble, Burst, C, Cash, House, Jar, Note, Phone, Room, T, Table, clamp, lerp, nformat, phase, xy} from './art';
import {getHandAnchors, type CharacterV2Props} from '../finance-cast-v2/CharacterV2';
import {actionScenes, fieldsScene, assumptionsScene} from './variants';

export type LongSegment={id:string;from:number;duration:number;text:string;kind:string;headline:string;cueFrame:number;data?:Record<string,unknown>;chapterId?:string;chapterTitle?:string;resultFrame?:number};
export type LongPlan={fps:number;durationFrames:number;segments:LongSegment[];captions:{from:number;end:number;text:string}[];words?:{start:number;end:number;text:string}[]};
export type SceneProps={s:LongSegment;f:number;d:number;index:number};
const scale=1.22;
const actor=(id:1|2,x:number,f:number,extra:Partial<CharacterV2Props>={}):CharacterV2Props=>({id,x,y:925,scale,frame:f,variant:'comic',pose:id===1?'receive':'give',emotion:id===1?'thinking':'confident',flip:id===2,gaze:'right',...extra});
const num=(s:LongSegment,key:string,fallback:number)=>typeof s.data?.[key]==='number'?Number(s.data[key]):fallback;
const str=(s:LongSegment,key:string,fallback:string)=>typeof s.data?.[key]==='string'?String(s.data[key]):fallback;

const Payday:React.FC<SceneProps>=p=>{
 const {f,d}=p,raise=phase(f,d,.05,.32),gone=phase(f,d,.36,.77),reaction=phase(f,d,.72,.88);
 const a=actor(1,510,f,{pose:gone>.5?'shrug':'celebrate',emotion:gone>.5?'surprised':'happy'});
 return <><Room/><path d="M720 740H1830" stroke={C.ink} strokeWidth={8}/><Actor {...a}/><Jar x={1290} y={658} label="KHOẢN DƯ" value="2 triệu" fill={.3} scale={1.2}/>
 <g opacity={raise}><Note x={936} y={340} w={480} h={172} title="LƯƠNG TĂNG" value="+2 triệu" fill={C.yellow} rotate={lerp(-12,0,raise)}/></g>
 {[0,1].map(i=>{const pos=xy([955+i*120,470],[1570+i*100,690],gone,160);return <Cash key={i} x={pos[0]} y={pos[1]} value="1 tr" scale={.95} rotate={gone*20-i*8}/>;})}
 <g opacity={gone}><Bag x={1630} y={610} scale={.8} label="CHI THÊM"/></g>
 <g opacity={reaction}><Bubble x={120} y={193} width={665} text="Lương tăng. Tiền dư vẫn thế?" fill={C.yellow}/><Burst x={688} y={472} scale={.7}/></g>
 <T x={1290} y={876} size={39} fill={C.red} opacity={gone}>Khoản tăng đã có nơi để đi.</T></>;
};

const Disclaimer:React.FC<SceneProps>=({f,d})=>{
 const a=actor(2,1605,f,{scale:1.3,flip:true,pose:'give',emotion:'neutral'}),h=getHandAnchors(a).right;
 const enter=phase(f,d,0,.16),stamp=phase(f,d,.3,.47);
 return <><Room mode="plain"/><Actor {...a}/><g transform={`translate(${lerp(-600,790,enter)} 537) rotate(${lerp(-11,-2,enter)})`}>
 <rect x={-594} y={-286} width={1188} height={573} rx={15} fill={C.white} stroke={C.ink} strokeWidth={6}/><T x={0} y={-183} size={43}>MIỄN TRỪ TRÁCH NHIỆM</T><path d="M-505-135H505" stroke={C.line} strokeWidth={4}/>
 <T x={0} y={-48} size={54}>Minh, Lan và số tiền là minh họa.</T><T x={0} y={43} size={34} weight={500}>Một cách học về ngân sách và dòng tiền.</T><T x={0} y={108} size={34} weight={500}>Điều chỉnh theo thu nhập, thiết yếu và nghĩa vụ nợ.</T>
 <g transform={`translate(107 209) rotate(-5) scale(${lerp(1.5,1,stamp)})`} opacity={stamp}><rect x={-340} y={-36} width={680} height={73} rx={7} fill="none" stroke={C.red} strokeWidth={6}/><T x={0} y={13} size={29} fill={C.red}>KHÔNG PHẢI TƯ VẤN TÀI CHÍNH CÁ NHÂN</T></g></g>
 <path d={`M${h.x} ${h.y}L1378 578`} stroke={C.ink} strokeWidth={6} opacity={enter}/></>;
};

const Allocation:React.FC<SceneProps & {after?:boolean}>=p=>{
 const {f,d,after=false}=p,end=Math.max(72,p.s.resultFrame||d*.5),arrival=phase(f,d,.02,Math.min(.27,end/d*.5)),allocate=phase(f,d,.18,end/d),result=phase(f,d,Math.max(.19,end/d-.035),end/d);
 const n=num(p.s,'income',after?14000000:12000000)/1000000,spend=num(p.s,'expenses',after?12000000:10000000)/1000000,surplus=num(p.s,'surplus',2000000)/1000000;
 const left=actor(1,250,f,{scale:1.05,pose:result>.1&&after?'shrug':'give',emotion:result>.1&&after?'surprised':'thinking'}),right=actor(2,1695,f,{scale:1.05,pose:'point'});
 return <><Room mode="plain"/><Actor {...left}/><Actor {...right}/><Table y={780}/>
 <Note x={960} y={302} w={440} h={153} title={after?'SAU KHI TĂNG LƯƠNG':'TRƯỚC ĐÂY'} value={`${n} triệu`} fill={C.yellow}/>
 <path d="M465 577H1065V755H465Z" fill="#E4BBA1" stroke={C.ink} strokeWidth={5}/><T x={765} y={642} size={35}>CHI TIÊU</T><T x={765} y={703} size={51}>{Math.round(spend*allocate)} triệu</T>
 <Jar x={1360} y={620} scale={.95} fill={.35*allocate} label="CÒN DƯ" value={`${Math.round(surplus*allocate)} triệu`}/>
 {Array.from({length:n},(_,i)=>{const inT=clamp(arrival*n-i),outT=clamp(allocate*n-i);const hold:[number,number]=[807+(i%7)*51,420+Math.floor(i/7)*32];const dest:[number,number]=i<spend?[559+(i%6)*81,532-Math.floor(i/6)*58]:[1320+(i-spend)*76,475];const pos=inT<1?xy([960,318],hold,inT,40):xy(hold,dest,outT,90);return <Cash key={i} x={pos[0]} y={pos[1]} value="1 tr" scale={.48} rotate={(i%3-1)*8}/>;})}
 <T x={960} y={884} size={57} opacity={result} fill={after?C.red:C.green}>{n} − {spend} = {surplus} triệu</T>
 {after&&<g opacity={result}><Burst x={386} y={399} scale={.6} label="?!"/><T x={1300} y={818} size={27}>Vẫn bằng trước đây.</T></g>}</>;
};

const Daily:React.FC<SceneProps>=p=>{
 const {f,d,s}=p,feed=phase(f,d,.03,Math.max(.16,(s.resultFrame||d*.42)/d)),count=Math.min(30,Math.floor(feed*30)),daily=num(s,'daily',num(s,'dailyBefore',60000)-num(s,'dailyAfter',0)),isSaving=typeof s.data?.saved==='number';
 const left=actor(1,290,f,{scale:1.15,pose:'receive',emotion:count>20?'surprised':'thinking'}),hand=getHandAnchors(left).right;
 return <><Room mode="shop"/><Actor {...left} prop="receipt" propLabel={isSaving?'GIẢM MỖI NGÀY':'CHI THÊM / NGÀY'} propValue={nformat(daily)}/>
 <rect x={700} y={330} width={1034} height={465} rx={18} fill={C.white} stroke={C.ink} strokeWidth={6}/><T x={1218} y={397} size={40}>MỘT THÁNG CỦA KHOẢN NHỎ</T>
 {Array.from({length:30},(_,i)=>{const on=i<count;return <g key={i} transform={`translate(${776+i%10*100} ${476+Math.floor(i/10)*106})`}><rect x={-40} y={-35} width={80} height={83} rx={8} fill={on?(isSaving?'#CFE2D5':C.yellow):C.paper} stroke={C.ink} strokeWidth={2}/><T x={0} y={-4} size={24}>{i+1}</T>{on&&<T x={0} y={29} size={17}>{nformat(daily)}</T>}</g>;})}
 {count<30&&feed>0&&<g><Cash x={lerp(hand.x,776+count%10*100,(feed*30)%1)} y={lerp(hand.y,476+Math.floor(count/10)*106,(feed*30)%1)-Math.sin(((feed*30)%1)*Math.PI)*100} value="60k" scale={.45}/></g>}
 <T x={1218} y={872} size={isSaving?43:55} fill={isSaving?C.green:C.red}>{count} × {nformat(daily)} = {nformat(count*daily)}</T>
 {isSaving&&<T x={1218} y={921} size={29} fill={C.green} opacity={phase(f,d,(s.resultFrame||d*.42)/d,Math.min(.99,((s.resultFrame||d*.42)+15)/d))}>Chi 11,4 triệu → dư 2,6 triệu nếu khoản khác giữ nguyên.</T>}
 {count===30&&<Burst x={1745} y={820} scale={.5} label="!"/>}</>;
};

const Dinner:React.FC<SceneProps>=({f,d,s})=>{
 const resultEnd=Math.max(50,s.resultFrame||d*.43),slide=phase(f,d,.03,Math.max(.14,(resultEnd-25)/d)),sum=phase(f,d,Math.max(.15,(resultEnd-16)/d),resultEnd/d),a=actor(1,350,f,{pose:'receive',emotion:sum>.1?'surprised':'happy'}),b=actor(2,1570,f,{pose:'give',emotion:'happy'});
 return <><Room mode="night"/><Actor {...a}/><Actor {...b}/><Table y={741}/>
 <g transform={`translate(960 708)`} stroke={C.ink} strokeWidth={5}><ellipse rx={260} ry={53} fill={C.white}/><ellipse rx={205} ry={34} fill="#E4D5AA"/><path d="M-96-8Q-98-88-4-91Q101-82 98-8Z" fill={C.yellow}/><path d="M-30-30L-48-50M11-46L23-62M42-22L61-34" stroke={C.green} strokeWidth={10}/></g>
 <Note x={760} y={415} title="30 NGÀY CHI THÊM" value="1.800.000" w={375} h={175}/><g transform={`translate(${lerp(1910,1198,slide)} ${lerp(168,415,slide)}) rotate(${lerp(14,3,slide)})`}><Note x={0} y={0} title="THÊM MỘT BỮA ĂN" value="200.000" w={335} h={175} fill={C.yellow}/></g>
 <g opacity={sum}><T x={960} y={607} size={67} fill={C.red}>= 2 triệu chi thêm</T><Bubble x={120} y={164} width={642} text="Vừa hết phần tăng lương!" fill={C.yellow}/><Burst x={510} y={430} scale={.6}/></g></>;
};

const Essentials:React.FC<SceneProps>=p=>{
 const {f,d,index,s}=p,pressure=phase(f,d,.05,.52),support=phase(f,d,.57,.93),left=actor(1,440,f,{pose:support>.1?'receive':'shrug',emotion:support>.5?'neutral':'worried'}),right=actor(2,1530,f,{pose:'give',emotion:'thinking'});
 const cats=Array.isArray(s.data?.categories)?s.data.categories:[],labels=[String(cats[0]||str(s,'label1','Nhà ở')),String(cats[1]||str(s,'label2','Ăn uống')),String(cats[2]||str(s,'label3','Đi lại'))];
 return <><Room mode="shop"/><Actor {...left}/><Actor {...right}/>
 <g transform={`translate(960 640) rotate(${lerp(0,-5,pressure)*(1-support)})`}><path d="M-435 80H435L390 141H-390Z" fill={C.purple} stroke={C.ink} strokeWidth={6}/><path d="M-328 130L-358 236M328 130L358 236" stroke={C.ink} strokeWidth={15}/><House x={-263} y={-45} scale={.65} label={labels[0]}/>{labels[1]==='gia đình'?<g transform="translate(0 -70)" stroke={C.ink} strokeWidth={4}><circle cx={-42} cy={-61} r={26} fill="#EAC29C"/><circle cx={40} cy={-61} r={26} fill="#E5B293"/><path d="M-81 52V-11Q-42-44-4-11V52ZM3 52V-11Q41-44 80-11V52Z" fill={C.purple}/><T x={0} y={141} size={29}>{labels[1]}</T></g>:<Bag x={0} y={-62} scale={.69} label={labels[1]}/>} <g transform="translate(260 -40)" stroke={C.ink} strokeWidth={5}><path d="M-105 27L-85-40H62L98 27V92H-108Z" fill={C.blue}/><circle cx={-68} cy={85} r={24} fill={C.ink}/><circle cx={65} cy={85} r={24} fill={C.ink}/><path d="M-67-28H-10V18H-80ZM5-28H52L76 18H5Z" fill={C.white}/><T x={0} y={160} size={28}>{labels[2]}</T></g></g>
 <g opacity={pressure*(1-support)}><Arrow a={[960,264]} b={[960,398]} color={C.red} t={pressure}/><T x={960} y={245} size={40} fill={C.red}>Chi thiết yếu có thể tăng.</T></g>
 <g opacity={support}><Bubble x={950} y={173} width={780} text={index%2?'Giữ nhu cầu thật. Sửa phần linh hoạt.':'Tính lại mức phù hợp với mình.'} fill={C.white}/><T x={960} y={896} size={36} fill={C.green}>Không ép mọi người cùng một mức chi.</T></g></>;
};

const Audit:React.FC<SceneProps>=p=>{
 const {f,d,s}=p,sort=phase(f,d,.08,.86),scan=phase(f,d,.08,.9),a=actor(2,1560,f,{scale:1.16,pose:'point',emotion:'thinking'}),values=Array.isArray(s.data?.labels)?s.data.labels.map(String):s.data?.action==='sort_receipts'?['CẦN THIẾT','CÓ THỂ CHỌN','KIỂM LẠI']:['NHÀ / SINH HOẠT','LINH HOẠT','ĐỊNH KỲ'];
 return <><Room mode="desk"/><Actor {...a}/><g transform={`translate(650 600) rotate(-4)`}><rect x={-460} y={-330} width={920} height={610} rx={16} fill={C.white} stroke={C.ink} strokeWidth={5}/><T x={0} y={-260} size={39}>{str(s,'label','GOM KHOẢN CHI THẬT')}</T>
 {values.map((label,i)=><g key={i}><rect x={-410+i*282} y={-206} width={256} height={385} rx={10} fill={[C.yellow,'#E8D9E9','#D1E1D7'][i]} opacity={.5}/><T x={-282+i*282} y={-157} size={23}>{label}</T></g>)}
 {Array.from({length:9},(_,i)=>{const t=clamp(sort*12-i*.5),pos=xy([50+(i%3-1)*75,-27+(Math.floor(i/3)-1)*60],[-320+(i%3)*282,-60+Math.floor(i/3)*63],t,15);return <g key={i} transform={`translate(${pos[0]} ${pos[1]}) rotate(${lerp((i%3-1)*18,0,t)})`}><rect x={-74} y={-19} width={148} height={43} rx={4} fill={C.white} stroke={C.ink} strokeWidth={2}/><T x={0} y={9} size={16}>{['Hóa đơn','Sao kê','Tiền mặt'][i%3]}</T></g>;})}
 <path d={`M-385 222H${-385+770*scan}`} stroke={C.green} strokeWidth={10} strokeLinecap="round"/></g>
 <g transform={`translate(${lerp(350,1180,scan)} ${510+Math.sin(scan*Math.PI)*70}) rotate(-25)`}><circle r={93} fill="#FFFFFF" fillOpacity={.25} stroke={C.ink} strokeWidth={10}/><path d="M-68 69L-161 165" stroke={C.ink} strokeWidth={28} strokeLinecap="round"/></g>
</>;
};

const Recurring:React.FC<SceneProps>=p=>{
 const {f,d,s}=p,uncover=phase(f,d,.08,.42),decision=phase(f,d,.52,.9),cost=num(s,'amount',num(s,'monthly',0)),a=actor(1,420,f,{pose:'give',emotion:decision>.5?'confident':'surprised'});
 const selected=str(s,'label','Khoản lặp lại');
 return <><Room/><Actor {...a} prop="phone" propLabel="CHI ĐỊNH KỲ"/>
 <Phone x={1010} y={578} scale={1.08} title="KIỂM TRA GIA HẠN" lines={['Tên dịch vụ','Ngày gia hạn','Mức dùng thực tế','Giữ / đổi / dừng']} checked={Math.floor(uncover*3)}/>
 <g opacity={uncover}><Note x={1550} y={392} w={360} h={180} title={selected} value={cost?`${nformat(cost)} / tháng`:'Xem lại gia hạn'} fill={C.yellow}/><path d="M1502 489Q1440 540 1459 665" fill="none" stroke={C.ink} strokeWidth={6}/>
 <Jar x={1510} y={745} scale={.65} fill={.3} label="LẶP LẠI" value="Mỗi kỳ"/></g>
 <g opacity={decision}><rect x={1280} y={542} width={500} height={90} rx={20} fill={C.white} stroke={C.green} strokeWidth={5}/><T x={1530} y={600} size={33} fill={C.green}>Dựa vào mức dùng thật.</T><Arrow a={[1184,680]} b={[1280,588]} color={C.green} t={decision}/></g>
 <T x={1010} y={912} size={30}>{cost?`${nformat(cost)} × 12 = ${nformat(cost*12)} / năm · Kiểm điều kiện hủy và hoàn tiền.`:'Không xóa bừa dịch vụ đang cần.'}</T></>;
};

const Annual:React.FC<SceneProps>=p=>{
 const {f,d,s}=p,split=phase(f,d,.03,Math.max(.15,(s.resultFrame||s.cueFrame||d*.4)/d)),annual=num(s,'annual',num(s,'total',1200000)),monthly=annual/12;
 const a=actor(2,1760,f,{pose:'give',emotion:'confident'});
 return <><Room mode="plain"/><Actor {...a}/><Note x={960} y={296} w={560} h={160} title={str(s,'label','KHOẢN KHÔNG ĐẾN HẰNG THÁNG')} value={`${nformat(annual)} / năm`} fill={C.yellow}/>
 <g transform="translate(225 428)">{Array.from({length:12},(_,i)=>{const filled=split*12>i;return <g key={i} transform={`translate(${i%6*226} ${Math.floor(i/6)*203})`}><path d="M0 0H186V158H0Z" fill={C.white} stroke={C.ink} strokeWidth={4}/><path d="M0 0H186V39H0Z" fill={filled?C.green:C.purple}/><T x={93} y={28} size={22} fill={C.white}>THÁNG {i+1}</T><Jar x={93} y={101} scale={.33} fill={filled?.5:0} label="ĐỂ RIÊNG" value={filled?nformat(monthly):''}/></g>;})}</g>
 <T x={850} y={910} size={45} fill={C.green}>{nformat(annual)} ÷ 12 = {nformat(monthly)} mỗi tháng</T></>;
};

const CashCalendar:React.FC<SceneProps>=p=>{
 const {f,d,s}=p,travel=phase(f,d,.1,.85),payday=num(s,'payday',25),billday=num(s,'billday',5),a=actor(1,302,f,{scale:1.15,pose:'receive',emotion:travel>.6?'worried':'thinking'});
 const position=lerp(625,1670,travel),shortfall=travel>.36&&travel<.67;
 return <><Room mode="plain"/><Actor {...a}/><g transform="translate(650 430)"><T x={530} y={-69} size={38}>TIỀN ĐẾN VÀ TIỀN PHẢI ĐI</T><path d="M0 70H1060" stroke={C.ink} strokeWidth={9}/>{[1,billday,15,payday,30].map((day,i)=><g key={i} transform={`translate(${i*265} 70)`}><path d="M0-13V18" stroke={C.ink} strokeWidth={5}/><T x={0} y={64} size={30}>Ngày {day}</T></g>)}
 <Note x={265} y={226} w={220} h={130} title="HÓA ĐƠN ĐẾN" value={`Ngày ${billday}`} fill={C.red}/><Note x={795} y={226} w={220} h={130} title="LƯƠNG VỀ" value={`Ngày ${payday}`} fill={C.yellow}/></g>
 <g transform={`translate(${position} 398)`}><path d="M-70 0Q0-50 70 0V70H-70Z" fill={shortfall?C.red:C.green} stroke={C.ink} strokeWidth={4}/><T x={0} y={45} size={24} fill={C.white}>{shortfall?'CHƯA CÓ':'SỐ DƯ'}</T><path d="M0 79L-12 99H12Z" fill={C.ink}/></g>
 <T x={1165} y={825} size={43} fill={C.red} opacity={phase(f,d,.48,.68)}>Có dư cả tháng ≠ đủ tiền đúng ngày.</T>
 <g opacity={phase(f,d,.7,.92)}><T x={1165} y={891} size={31}>Giữ phần cho hóa đơn sắp tới.</T></g></>;
};

const Buffer:React.FC<SceneProps>=p=>{
 const {f,d,s}=p,rain=phase(f,d,.05,.75),shelter=phase(f,d,.38,.7),a=actor(1,460,f,{pose:shelter>.3?'give':'shrug',emotion:shelter>.3?'confident':'worried'}),b=actor(2,1570,f,{pose:'give',emotion:'thinking'});
 return <><Room mode="plain"/><Actor {...a}/><Actor {...b}/><Jar x={1010} y={743} scale={1.17} label={str(s,'label','KHOẢN ĐỆM')} value={num(s,'amount',0)?nformat(num(s,'amount',0)):'Phù hợp'} fill={.38*phase(f,d,.35,.93)}/>
 {Array.from({length:8},(_,i)=>{const progress=clamp(rain*1.5-i*.08),pos=xy([720+(i%4)*190,200],[730+(i%4)*185,675],progress);return <g key={i} opacity={progress<.98?1:0}><path d={`M${pos[0]} ${pos[1]}L${pos[0]-10} ${pos[1]+24}`} stroke={C.blue} strokeWidth={8} strokeLinecap="round"/></g>;})}
 <g transform={`translate(${lerp(1660,1010,shelter)} ${lerp(160,448,shelter)}) rotate(${lerp(25,0,shelter)})`}><path d="M-342 0Q-302-237 0-246Q302-237 342 0Q230-57 120 0Q0-57-110 0Q-224-57-342 0Z" fill={C.yellow} stroke={C.ink} strokeWidth={6}/><path d="M0-249V150Q0 199 52 177" fill="none" stroke={C.ink} strokeWidth={10}/><path d="M0-246Q-140-127-110 0M0-246Q140-127 120 0" fill="none" stroke={C.ink} strokeWidth={4}/></g>
</>;
};

const PurchaseChoice:React.FC<SceneProps>=p=>{
 const {f,d,s}=p,unpack=phase(f,d,.12,.73),decide=phase(f,d,.74,.94),a=actor(1,350,f,{pose:'receive',emotion:unpack>.4?'thinking':'happy'}),b=actor(2,1630,f,{pose:'point',emotion:'confident'});
 const price=num(s,'price',num(s,'amount',500000)),extra=num(s,'extra',num(s,'fee',50000));
 return <><Room mode="shop"/><Actor {...a}/><Actor {...b}/><Table y={787}/>
 <g transform={`translate(${lerp(1100,861,unpack)} 657)`} stroke={C.ink} strokeWidth={6}><path d="M-160-151H160V120H-160Z" fill={C.yellow}/><path d="M-160-151L0-89 160-151M0-89V120" fill="none" strokeWidth={5}/><T x={-75} y={21} size={28}>MÓN ĐỒ</T></g>
 <Note x={818} y={362} w={345} h={144} title="GIÁ NIÊM YẾT" value={nformat(price)}/>
 <g opacity={unpack}><Note x={1240} y={508} w={310} h={144} title="PHÍ / PHỤ KIỆN" value={`+ ${nformat(extra)}`} rotate={lerp(18,3,unpack)} fill={C.white}/><Arrow a={[1100,391]} b={[1240,424]} t={unpack}/><T x={1110} y={898} size={44} fill={C.red}>Tổng cần trả: {nformat(price+extra)}</T></g>
 <g opacity={decide}><Bubble x={113} y={177} width={630} text="Tính đủ rồi mới quyết định." fill={C.yellow}/></g></>;
};

const Automate:React.FC<SceneProps>=p=>{
 const {f,d,s}=p,check=phase(f,d,.08,.43),transfer=phase(f,d,.42,.9),a=actor(2,400,f,{pose:'give',emotion:'confident'}),amount=num(s,'amount',num(s,'save',0));
 return <><Room/><Actor {...a} prop="phone" propLabel="LỊCH CHUYỂN"/><Phone x={990} y={571} scale={1.1} title="TRƯỚC KHI ĐẶT LỊCH" lines={['Thu nhập dự kiến','Chi thiết yếu','Hóa đơn / nợ đến hạn','Khoản phù hợp']} checked={Math.floor(check*4)}/>
 <Jar x={1585} y={689} scale={.92} label="ĐỂ RIÊNG" value={transfer>.92?(amount?nformat(amount):'Phù hợp'):''} fill={transfer*.45}/>
 <Arrow a={[1165,590]} b={[1460,590]} t={transfer} color={C.green}/>{[0,1,2].map(i=>{const t=clamp(transfer*2-i*.25),pos=xy([1150,587],[1585,544],t,100);return <Cash key={i} x={pos[0]} y={pos[1]} scale={.45} value="phần nhỏ" fill={C.yellow}/>;})}
 <T x={1288} y={919} size={38} fill={C.green}>Chỉ tự động khi đủ tiền cho nghĩa vụ trước.</T></>;
};

const Review:React.FC<SceneProps>=p=>{
 const {f,d,s}=p,write=phase(f,d,.08,.84),a=actor(1,1660,f,{scale:1.2,pose:'point',emotion:write>.8?'confident':'thinking'});
 const labels=[str(s,'label1','Khoản nào tăng?'),str(s,'label2','Điều gì đáng giữ?'),str(s,'label3','Sửa một điều tuần tới.')];
 return <><Room mode="desk"/><Actor {...a}/><g transform={`translate(808 572) rotate(-3)`}><path d="M-620-300H-12Q0-290 12-300H620V300H12Q0 289-12 300H-620Z" fill={C.white} stroke={C.ink} strokeWidth={6}/><path d="M0-285V284" stroke={C.line} strokeWidth={5}/><T x={-305} y={-222} size={41}>NHÌN LẠI</T><T x={305} y={-222} size={41}>BƯỚC TIẾP THEO</T>
 {labels.map((label,i)=><g key={i}><path d={`M-560 ${-137+i*116}H-56`} stroke={C.line} strokeWidth={2}/><T x={-533} y={-153+i*116} anchor="start" size={29} weight={500}>{label}</T><rect x={49} y={-185+i*116} width={51} height={51} rx={7} fill={C.paper} stroke={C.ink} strokeWidth={3}/><g opacity={clamp(write*3-i)}><path d={`M59 ${-159+i*116}L72 ${-146+i*116}L91 ${-174+i*116}`} fill="none" stroke={C.green} strokeWidth={6}/><path d={`M127 ${-155+i*116}H${127+Math.min(390,clamp(write*3-i)*390)}`} stroke={C.purple} strokeWidth={9} strokeLinecap="round"/></g></g>)}</g>
 <g transform={`translate(${lerp(658,1340,write)} ${lerp(409,741,write)}) rotate(35)`}><path d="M-12-109H12V-6L0 27-12-6Z" fill={C.yellow} stroke={C.ink} strokeWidth={4}/><path d="M-12-6H12L0 27Z" fill={C.white} stroke={C.ink} strokeWidth={3}/></g>
 <T x={909} y={916} size={34} fill={C.green}>Đo lại để biết cách nào hợp với mình.</T></>;
};

const Action:React.FC<SceneProps>=p=>{
 const {f,d,s}=p,select=phase(f,d,.1,.44),progress=phase(f,d,.34,.9),a=actor(1,395,f,{pose:progress>.7?'celebrate':'give',emotion:'confident'}),b=actor(2,1535,f,{pose:progress>.7?'celebrate':'give',emotion:'happy'});
 return <><Room mode="plain"/><Actor {...a}/><Actor {...b}/><g transform="translate(960 568)"><rect x={-346} y={-290} width={692} height={596} rx={25} fill={C.white} stroke={C.ink} strokeWidth={6}/><path d="M-346-290H346V-210H-346Z" fill={C.yellow}/><T x={0} y={-235} size={40}>{str(s,'label','THỬ TRONG 30 NGÀY')}</T>
 {Array.from({length:30},(_,i)=><g key={i} transform={`translate(${-274+(i%6)*109} ${-138+Math.floor(i/6)*80})`}><rect x={-38} y={-29} width={76} height={59} rx={9} fill={i<progress*30?'#CFE2D5':C.paper} stroke={C.ink} strokeWidth={2}/><T x={0} y={9} size={24}>{i+1}</T>{i<progress*30&&<path d="M-21 1L-8 13 24-13" stroke={C.green} strokeWidth={4} fill="none"/>}</g>)}
 </g><g opacity={select}><Bubble x={74} y={158} width={675} text="Chọn một khoản. Bắt đầu hôm nay." fill={C.yellow}/></g><T x={960} y={924} size={35} fill={C.green}>Ghi lại → cộng đủ → chọn giữ hoặc giảm → xem lại.</T></>;
};

const scenes:Record<string,React.FC<SceneProps>>={hook:Payday,disclaimer:Disclaimer,budget_before:p=><Allocation {...p}/>,budget_after:p=><Allocation {...p} after/>,daily:Daily,dinner:Dinner,essentials:Essentials,audit:Audit,recurring:Recurring,annual:Annual,calendar:CashCalendar,buffer:Buffer,choice:PurchaseChoice,automate:Automate,review:Review,cta:Action};

/** A long-form, code-native comic. Mouth motion belongs to the stylized rig and
 * is intentionally not represented as verified phoneme-level lip synchronization.
 * Source takes, exact clause timing, captions and final mix are provided by plan.
 */
export const ComicLongFilm:React.FC<{plan:LongPlan}>=({plan})=>{
 const frame=useCurrentFrame();let index=plan.segments.findIndex(s=>frame>=s.from&&frame<s.from+s.duration);if(index<0)index=Math.max(0,plan.segments.length-1);
 const base=plan.segments[index];if(!base)return <svg width={1920} height={1080}><rect width={1920} height={1080} fill={C.paper}/></svg>;
 const clean=(text:string)=>text.toLocaleLowerCase('vi-VN').replace(/[^\p{L}\p{N}]+/gu,' ').trim();
 const target=base.kind==='annual'?'một trăm nghìn mỗi tháng':base.kind==='budget_before'?'còn hai triệu':base.kind==='budget_after'?'vẫn còn hai triệu':base.kind==='dinner'?'vừa hết hai triệu':base.kind==='daily'?(typeof base.data?.saved==='number'?'sáu trăm nghìn':'một triệu tám'):'';
 const ws=(plan.words||[]).filter(w=>w.start*plan.fps>=base.from-1&&w.start*plan.fps<base.from+base.duration);
 const parts=target.split(' ');const wi=target?ws.findIndex((_,i)=>clean(ws.slice(i,i+parts.length).map(w=>w.text).join(' '))===target):-1;
 const s:LongSegment={...base,resultFrame:wi>=0?Math.max(1,Math.round(ws[wi].start*plan.fps-base.from)):base.resultFrame};
 const f=frame-s.from,d=Math.max(s.duration,1),action=typeof s.data?.action==='string'?s.data.action:'',Scene=s.data?.conditional===true?assumptionsScene:Array.isArray(s.data?.fields)?fieldsScene:actionScenes[action]||scenes[s.kind]||Review;
 const drift=.012*phase(f,d,.04,.94),entry=phase(f,d,0,Math.min(.035,10/d));
 const chapter=(s.chapterTitle||'Lương tăng, tiền dư đi đâu?');
 return <svg viewBox="0 0 1920 1080" width={1920} height={1080} style={{fontFamily:'Arial, sans-serif',fontVariantNumeric:'tabular-nums',background:C.paper}}>
 <defs><pattern id="finance-long-dots" width={25} height={25} patternUnits="userSpaceOnUse"><circle cx={4} cy={4} r={1.2} fill={C.ink}/></pattern><clipPath id="finance-long-stage"><rect y={146} width={1920} height={813}/></clipPath></defs>
 <rect width={1920} height={1080} fill={C.paper}/><g clipPath="url(#finance-long-stage)"><g transform={`translate(960 600) scale(${1+drift}) translate(-960 -600)`} opacity={entry}><Scene s={s} f={f} d={d} index={index}/></g><rect width={1920} height={960} fill="url(#finance-long-dots)" opacity={.04} pointerEvents="none"/></g>
 <path d="M0 0H1920V148H0Z" fill={C.paper}/><T x={76} y={47} size={23} fill={C.muted} anchor="start">{chapter.toLocaleUpperCase('vi-VN')}</T><T x={76} y={112} size={Math.min(48,1640/((s.headline||'').length*.57||1))} anchor="start">{s.headline}</T>
 <rect x={1577} y={20} width={267} height={43} rx={10} fill={C.white} stroke={C.line} strokeWidth={2}/><T x={1710} y={49} size={20} fill={C.muted}>SỐ LIỆU MINH HỌA</T>
 <path d="M76 139H1844" stroke={C.line} strokeWidth={3}/><path d={`M76 139H${76+1768*clamp(frame/Math.max(1,plan.durationFrames-1))}`} stroke={C.purple} strokeWidth={4}/>
 <rect x={0} y={960} width={1920} height={120} fill={C.ink}/></svg>;
};
