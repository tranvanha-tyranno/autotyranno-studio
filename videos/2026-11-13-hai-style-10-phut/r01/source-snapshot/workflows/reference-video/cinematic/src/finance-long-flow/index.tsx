import React from 'react';
import {AbsoluteFill, Easing, interpolate, useCurrentFrame} from 'remotion';
import {Bill, Envelope, Hand, P, Plate, Receipt, Wallet} from '../finance-flow/Objects';

/** Content is supplied by the exact-take long-form planner. This renderer never
 * estimates narration timing from character count and never owns the audio. */
export type LongSegment = {
  id:string; from:number; duration:number; text:string; kind:string;
  headline:string; cueFrame:number; data?:Record<string,unknown>;
  chapterId?:string; chapterTitle?:string;
};
export type LongPlan = {
  fps:number; durationFrames:number; segments:LongSegment[];
  captions:{from:number;end:number;text:string}[];
  words?:{start:number;end:number;text:string}[];
};
type Ctx={s:LongSegment;f:number;index:number};
const ink=P.ink, cream=P.paper, green=P.green, red=P.red, gold=P.yellow;
const smooth=Easing.bezier(.36,0,.24,1);
const q=(f:number,a:number,b:number)=>interpolate(f,[a,Math.max(a+1,b)],[0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp',easing:smooth});
const lerp=(a:number,b:number,t:number)=>a+(b-a)*t;
const phase=({f,s}:Ctx,a:number,b:number)=>q(f,s.duration*a,s.duration*b);
const cue=({f,s}:Ctx,span=.4)=>q(f,s.cueFrame,Math.min(s.duration*.96,s.cueFrame+s.duration*span));
const arc=(a:[number,number],b:[number,number],t:number,h=90):[number,number]=>[lerp(a[0],b[0],t),lerp(a[1],b[1],t)-Math.sin(Math.PI*t)*h];
const value=(s:LongSegment,key:string,fallback:number)=>typeof s.data?.[key]==='number'?s.data[key] as number:fallback;
const action=(s:LongSegment)=>String(s.data?.action??'');
const millions=(n:number)=>money(n/1000000);
const money=(n:number)=>Math.round(n).toLocaleString('vi-VN');
const Text:React.FC<React.PropsWithChildren<{x:number;y:number;size?:number;fill?:string;weight?:number;anchor?:'start'|'middle'|'end';opacity?:number}>>=({x,y,size=36,fill=ink,weight=700,anchor='middle',opacity=1,children})=><text x={x} y={y} fontSize={size} fill={fill} fontWeight={weight} textAnchor={anchor} opacity={opacity}>{children}</text>;
const Stroke:React.FC<{d:string;stroke?:string;width?:number;opacity?:number;dash?:string}>=({d,stroke=ink,width=5,opacity=1,dash})=><path d={d} fill="none" stroke={stroke} strokeWidth={width} strokeLinecap="round" strokeLinejoin="round" opacity={opacity} strokeDasharray={dash}/>;
const Camera:React.FC<React.PropsWithChildren<{x?:number;y?:number;scale?:number}>>=({x=960,y=470,scale=1,children})=><g transform={`translate(960 470) scale(${scale}) translate(${-x} ${-y})`}>{children}</g>;
const Check:React.FC<{x:number;y:number;scale?:number;fill?:string}>=({x,y,scale=1,fill=green})=><g transform={`translate(${x} ${y}) scale(${scale})`}><circle r="33" fill={fill}/><Stroke d="M-17 0L-3 14L19-16" stroke={cream} width={7}/></g>;
const Pencil:React.FC<{x:number;y:number;r?:number;scale?:number}>=({x,y,r=28,scale=1})=><g transform={`translate(${x} ${y}) rotate(${r}) scale(${scale})`} stroke={ink} strokeWidth={4}><path d="M-13-174H13V-17L0 15-13-17Z" fill={gold}/><path d="M-13-17H13L0 15Z" fill={cream}/><path d="M-13-150H13M0-140V-23" fill="none"/><path d="M-4 6L0 15 4 6" fill={ink}/></g>;
const Tag:React.FC<{x:number;y:number;label:string;fill?:string;width?:number}>=({x,y,label,fill=cream,width=250})=><g transform={`translate(${x} ${y})`}><path d={`M${-width/2}-31H${width/2-22}L${width/2} 0 ${width/2-22} 31H${-width/2}Z`} fill={fill} stroke={ink} strokeWidth={3}/><Text x={-4} y={9} size={22}>{label}</Text></g>;
const Tray:React.FC<{x:number;y:number;label:string;fill?:string;width?:number}>=({x,y,label,fill=cream,width=340})=><g transform={`translate(${x} ${y})`}><path d={`M${-width/2}-40L${-width/2+28} 54H${width/2-28}L${width/2}-40Z`} fill={fill} stroke={ink} strokeWidth={4}/><Text x={0} y={104} size={27}>{label}</Text></g>;
const Phone:React.FC<React.PropsWithChildren<{x:number;y:number;scale?:number;dark?:boolean}>>=({x,y,scale=1,dark=false,children})=><g transform={`translate(${x} ${y}) scale(${scale})`}><rect x="-162" y="-271" width="324" height="542" rx="40" fill={ink}/><rect x="-146" y="-251" width="292" height="500" rx="27" fill={dark?'#28433E':'#FFFDF7'}/><rect x="-51" y="-244" width="102" height="15" rx="7" fill={ink}/>{children}<path d="M-44 231H44" stroke={dark?cream:ink} strokeWidth="7" strokeLinecap="round"/></g>;
const Jar:React.FC<{x:number;y:number;amount?:string;fillLevel?:number;dark?:boolean;label?:string;scale?:number}>=({x,y,amount='',fillLevel=0,dark=false,label='KHOẢN ĐỆM',scale=1})=><g transform={`translate(${x} ${y}) scale(${scale})`}><defs><clipPath id={`jar-${x}-${y}`}><path d="M-104-150V-118Q-143-94-143-52V145Q-143 179-108 179H108Q143 179 143 145V-52Q143-94 104-118V-150Z"/></clipPath></defs><path d="M-104-150V-118Q-143-94-143-52V145Q-143 179-108 179H108Q143 179 143 145V-52Q143-94 104-118V-150Z" fill={dark?'#345B50':'#FFFEF8'} stroke={dark?cream:ink} strokeWidth={5}/><g clipPath={`url(#jar-${x}-${y})`}><rect x="-150" y={180-fillLevel*300} width="300" height={fillLevel*300} fill={gold}/>{Array.from({length:Math.floor(fillLevel*18)},(_,i)=><ellipse key={i} cx={-86+(i%5)*43} cy={150-Math.floor(i/5)*26} rx="24" ry="11" fill={gold} stroke={ink} strokeWidth={2}/>)}</g><rect x="-114" y="-176" width="228" height="32" rx="8" fill={dark?cream:green} stroke={dark?cream:ink} strokeWidth={4}/><path d="M-75-168V-151M-20-168V-151M35-168V-151M85-168V-151" stroke={dark?ink:cream} strokeWidth={2}/><rect x="-124" y="-20" width="248" height="102" rx="3" fill={dark?'#203B33':cream}/><Text x={0} y={12} size={21} fill={dark?cream:ink}>{label}</Text><Text x={0} y={58} size={38} fill={dark?cream:ink}>{amount}</Text></g>;
const House:React.FC<{x:number;y:number;scale?:number}>=({x,y,scale=1})=><g transform={`translate(${x} ${y}) scale(${scale})`} stroke={ink} strokeWidth={5} strokeLinejoin="round"><path d="M-104-16L0-100 104-16" fill={gold}/><path d="M-79-23V95H79V-23L0-86Z" fill={cream}/><path d="M-24 95V16H24V95" fill={green}/><path d="M-58-9H-37V17H-58ZM37-9H58V17H37Z" fill={gold}/></g>;
const Package:React.FC<{x:number;y:number;scale?:number}>=({x,y,scale=1})=><g transform={`translate(${x} ${y}) scale(${scale})`} stroke={ink} strokeWidth={5} strokeLinejoin="round"><path d="M-105-60L0-112 105-60V75L0 125-105 75Z" fill={gold}/><path d="M-105-60L0-8 105-60M0-8V125M-55-85L54-34V10" fill="none"/><path d="M-78 40L-30 63M-78 57L-44 73" strokeWidth={3}/></g>;
const Scooter:React.FC<{x:number;y:number;scale?:number;broken?:boolean}>=({x,y,scale=1,broken=false})=><g transform={`translate(${x} ${y}) scale(${scale})`} stroke={ink} strokeWidth={5} strokeLinejoin="round"><circle cx={-113} cy={72} r={45} fill={cream}/><circle cx={120} cy={72} r={45} fill={cream}/><circle cx={-113} cy={72} r={14} fill={ink}/><circle cx={120} cy={72} r={14} fill={ink}/><path d="M-145 53Q-123-25-60-37H28L60 39H97L52-86H25M52-86H92M-60-37L-22 37H-106" fill={green}/><path d="M-80-45H23" strokeWidth={15} strokeLinecap="round"/>{broken&&<path d="M-28 7L-7-28 0-7 27-45 14 6-2-2-18 32Z" fill={red} stroke={red} strokeWidth={2}/>}</g>;
const Scissors:React.FC<{x:number;y:number;open?:number;scale?:number}>=({x,y,open=1,scale=1})=><g transform={`translate(${x} ${y}) scale(${scale})`} stroke={ink} strokeWidth={6} fill={cream}><g transform={`rotate(${-25*open})`}><ellipse cx="-95" cy="-35" rx="46" ry="31" fill={red}/><path d="M-59-34L164 0-58 10Z" fill="#BEC7BD"/></g><g transform={`rotate(${25*open})`}><ellipse cx="-95" cy="35" rx="46" ry="31" fill={gold}/><path d="M-59 34L164 0-58-10Z" fill="#D7DCD2"/></g><circle r="12" fill={ink}/></g>;

const Hook:React.FC<Ctx>=(c)=>{
  const move=phase(c,.04,.72),gone=cue(c,.3),pull=phase(c,.6,.96);
  return <Camera x={lerp(930,1060,pull)} scale={lerp(1.12,1.28,pull)}>
    <Wallet x={980} y={575} scale={1.6} label="TIỀN DƯ" amount="2 triệu" open={1}/>
    {[0,1].map(i=>{const t=q(c.f,c.s.duration*(.08+i*.08),c.s.duration*(.5+i*.08));const [x,y]=arc([700+i*380,150],[930+i*120,480],t,30);const [ex,ey]=arc([930+i*120,480],[390+i*1140,600],gone,180);return <Bill key={i} x={gone>0?ex:x} y={gone>0?ey:y} value="1 triệu" rotate={lerp(i?12:-12,0,t)} scale={.82}/>;})}
    <Envelope x={375} y={665} label="CHI THÊM" amount="" scale={.9} open={move}/><Envelope x={1575} y={665} label="CHI THÊM" amount="" scale={.9} open={move}/>
    <Text x={980} y={270} size={70}>+2 triệu lương</Text>
    <g opacity={gone}><Stroke d="M815 328H1145" stroke={red} width={7}/><Text x={980} y={375} size={34} fill={red}>Khoản dư vẫn đứng yên.</Text></g>
  </Camera>;
};
const Disclaimer:React.FC<Ctx>=(c)=>{
 const paper=phase(c,0,.22),stamp=cue(c,.12),slide=phase(c,.7,.97);
 return <Camera><g transform={`translate(${lerp(-700,960,paper)} ${lerp(470,455,slide)}) rotate(${lerp(-9,-1,paper)})`}>
   <path d="M-685-263H646L685-223V273H-685Z" fill="#FFFDF6" stroke={ink} strokeWidth={4}/><path d="M646-263V-223H685" fill="none" stroke={ink} strokeWidth={3}/>
   <Text x={0} y={-169} size={32} fill={green}>MIỄN TRỪ TRÁCH NHIỆM</Text>
   <Text x={0} y={-65} size={60}>Minh và Lan là nhân vật hư cấu.</Text>
   <Text x={0} y={22} size={40} weight={400}>Số tiền dùng để minh họa cách suy nghĩ.</Text>
   <Text x={0} y={89} size={37} weight={400}>Không phải tư vấn tài chính cá nhân.</Text>
   <g opacity={stamp} transform={`translate(255 193) rotate(-5) scale(${lerp(1.4,1,stamp)})`}><rect x="-245" y="-37" width="490" height="74" rx="5" stroke={red} strokeWidth={4} fill="none"/><Text x={0} y={12} size={31} fill={red}>ĐIỀU CHỈNH THEO HOÀN CẢNH</Text></g>
 </g><Pencil x={lerp(1860,1580,slide)} y={lerp(800,718,slide)} r={-25}/></Camera>;
};
const Budget:React.FC<Ctx & {after?:boolean}>=(c)=>{
 const iv=value(c.s,'income',value(c.s,'baselineIncome',c.after?14000000:12000000));
 const ev=value(c.s,'expenses',value(c.s,'baselineExpense',c.after?12000000:10000000));
 const sv=value(c.s,'surplus',value(c.s,'baselineSurplus',iv-ev));
 const income=iv/1000000,spent=ev/1000000,surplus=sv/1000000;
 const feed=phase(c,.04,.44),allocate=cue(c,.5),finish=phase(c,.7,.98);
 return <Camera x={lerp(1075,960,feed)} y={470} scale={lerp(1.22,1,feed)}>
   <Envelope x={960} y={300} label="THU NHẬP" amount={`${income} triệu`} open={feed} scale={1.06}/>
   <Tray x={440} y={680} label="CHI TRONG THÁNG" fill="#E5C1AD" width={470}/>
   <Wallet x={1480} y={660} scale={1.12} open={allocate} label="CÒN DƯ" amount={allocate>.95?`${surplus} triệu`:'…'}/>
   {Array.from({length:Math.floor(income)},(_,i)=>{const arrive=q(c.f,c.s.duration*(.03+i*.013),c.s.duration*(.28+i*.013));const leave=q(c.f,c.s.cueFrame+i*3,Math.min(c.s.duration*.96,c.s.cueFrame+c.s.duration*.38+i*3));const hold:[number,number]=[870+(i%7)*28,450+Math.floor(i/7)*30];const end:[number,number]=i<Math.floor(spent)?[265+(i%6)*56,610+Math.floor(i/6)*33]:[1450+(i-Math.floor(spent))*65,560];const first=arc([900+(i%4)*40,295],hold,arrive,50),last=arc(hold,end,leave,150);return <Bill key={i} x={leave?last[0]:first[0]} y={leave?last[1]:first[1]} scale={.5} value={Number.isInteger(spent)?'1 tr':'minh họa'} opacity={arrive} rotate={lerp(0,(i%3-1)*5,leave)}/>;})}
   <Text x={440} y={798} size={54} fill={red} opacity={finish}>{spent} triệu</Text>
   <g opacity={finish}><Text x={960} y={790} size={45}>{millions(iv)} − {millions(ev)} = {millions(sv)}</Text><Stroke d="M1265 790H1665" stroke={green} width={6}/></g>
   {c.s.data?.conditional===true&&<g opacity={finish}><Tag x={960} y={365} label="GIẢ ĐỊNH KHÁC ĐỔI? TÍNH LẠI." fill={gold} width={650}/></g>}
 </Camera>;
};
const Daily:React.FC<Ctx>=(c)=>{
 const saving=typeof c.s.data?.saved==='number';
 const roll=cue(c,.65),count=Math.floor(roll*30),look=phase(c,0,.9),amount=saving?value(c.s,'dailyBefore',60000)-value(c.s,'dailyAfter',40000):value(c.s,'daily',60000);
 return <Camera x={lerp(820,1040,look)} scale={lerp(1.15,1.03,look)}>
  <defs><clipPath id="long-receipt-window"><rect x="170" y="345" width="1570" height="390" rx="9"/></clipPath></defs>
  <g clipPath="url(#long-receipt-window)"><rect x="170" y="345" width="1570" height="390" fill="#FFFDF7"/>
   {Array.from({length:30},(_,i)=>{const x=1750+i*130-roll*30*130;return <g key={i} transform={`translate(${x} 375)`}><path d="M-65 0V270" stroke={P.line} strokeWidth={2} strokeDasharray="6 7"/><Text x={0} y={50} size={22} fill={P.muted}>NGÀY</Text><Text x={0} y={116} size={52}>{i+1}</Text><Text x={0} y={190} size={24}>{saving?'−':'+'}{money(amount)}</Text><Stroke d="M-38 225H38" stroke={green} width={3}/></g>;})}
  </g><rect x="170" y="345" width="1570" height="390" rx="9" fill="none" stroke={ink} strokeWidth={4}/>
  <g transform="translate(960 750)"><path d="M-25 0L0-32 25 0Z" fill={red}/><Text x={0} y={51} size={24} fill={red}>TỪNG NGÀY ĐI QUA → TỔNG CHI LỚN LÊN</Text></g>
  <Text x={960} y={255} size={64} fill={saving?green:ink}>{saving?'GIẢM ĐƯỢC: ':''}{money(count*amount)} đồng</Text>
  <g opacity={phase(c,.73,.94)}><Tag x={1570} y={245} label={saving?'DƯ CÓ THỂ: 2,6 TRIỆU':'30 NGÀY = 1,8 TRIỆU'} fill={gold} width={saving?430:350}/></g>
 </Camera>;
};
const Dinner:React.FC<Ctx>=(c)=>{
 const take=phase(c,.04,.48),combine=cue(c,.43),last=phase(c,.78,.98);const xy=arc([1430,530],[1030,595],combine,70);
 return <Camera scale={lerp(1,1.09,last)}>
   <Plate x={lerp(1780,1430,take)} y={565} scale={1.3}/>
   <Receipt x={680} y={510} scale={1.5} amount="1.800.000" label="30 NGÀY" rotate={-5}/>
   <Receipt x={xy[0]} y={xy[1]} scale={.82} amount="200.000" label="BỮA ĂN" rotate={lerp(8,0,combine)} opacity={take}/>
   <Hand x={lerp(1970,1535,take)} y={450} rotate={-22} scale={.68}/>
   <Text x={980} y={265} size={58} fill={red} opacity={combine}>1,8 triệu + 0,2 triệu</Text>
   <Stroke d={`M600 760H${600+780*last}`} stroke={green} width={7}/><Text x={990} y={835} size={58} opacity={last}>= 2 triệu chi thêm</Text>
 </Camera>;
};
const Essentials:React.FC<Ctx>=(c)=>{
 const allocate=phase(c,.05,.82),protect=cue(c,.35),adjust=phase(c,.6,.98);
 const labels=Array.isArray(c.s.data?.categories)?c.s.data.categories.map(v=>String(v).toLocaleUpperCase('vi-VN')):['NHÀ Ở','SINH HOẠT','NGHĨA VỤ NỢ'];
 return <Camera x={lerp(1000,950,adjust)} scale={lerp(1.04,1.08,adjust)}>
   <g transform="translate(960 520)"><path d="M-720-220H720V100Q720 300 0 350Q-720 300-720 100Z" fill="#E1EADB" stroke={ink} strokeWidth={4}/><path d={`M-700-200H${-700+1400*protect}`} stroke={green} strokeWidth={13} fill="none" strokeLinecap="round"/></g>
   {[480,960,1440].map((x,i)=><g key={i}><Envelope x={x} y={645} label={labels[i]} amount="TÍNH TRƯỚC" open={q(allocate,i*.2,i*.2+.4)} scale={.98}/><Bill x={x} y={lerp(310,552,q(allocate,i*.2,i*.2+.4))} value="Ưu tiên" scale={.68}/>{i===0?<House x={x} y={390} scale={.72}/>:labels[i]==='ĐI LẠI'?<Scooter x={x} y={390} scale={.62}/>:i===1?<Plate x={x} y={390} scale={.6}/>:<Tag x={x} y={390} label="ĐÚNG HẠN" fill={gold} width={230}/>}</g>)}
   <Text x={960} y={245} size={43}>Thiết yếu thay đổi → tính lại phần có thể để dành.</Text>
   <g opacity={adjust}><Stroke d="M760 804L814 845 906 756" stroke={green} width={10}/><Text x={1155} y={827} size={33}>Không ép một mức cho tất cả.</Text></g>
 </Camera>;
};
const Audit:React.FC<Ctx>=(c)=>{
 const sort=cue(c,.6),scan=phase(c,.03,.9),which=c.index%3;
 const labels=Array.isArray(c.s.data?.labels)?c.s.data.labels.map(v=>String(v).toLocaleUpperCase('vi-VN')):['CẦN THIẾT','CÓ THỂ CHỈNH','CHƯA RÕ'];
 return <Camera scale={1.02}>
  <Phone x={350} y={495} scale={.9}><Text x={0} y={-166} size={23}>LỊCH SỬ GIAO DỊCH</Text>{Array.from({length:6},(_,i)=><g key={i} opacity={phase(c,i*.045,.25+i*.045)}><Stroke d={`M-104 ${-108+i*54}H32`} stroke={P.line} width={7}/><Text x={111} y={-101+i*54} anchor="end" size={22}>{['−60k','−200k','−?'][i%3]}</Text></g>)}<rect x="-119" y={-126+scan*265} width="238" height="48" rx="5" fill={gold} opacity=".25"/></Phone>
  {[850,1220,1590].map((x,i)=><Tray key={i} x={x} y={680} label={labels[i]} fill={i===which?'#E3EABB':cream} width={310}/>)}
  {Array.from({length:9},(_,i)=>{const dest=i%3;const t=q(sort,i*.066,i*.066+.35);const xy=arc([570,365+i*19],[765+dest*370+(i%2)*60,565+Math.floor(i/3)*26],t,130);return <Receipt key={i} x={xy[0]} y={xy[1]} scale={.49} label={['ĐI LẠI','ĂN UỐNG','ĐỊNH KỲ'][i%3]} amount="Ghi đủ" rotate={lerp(-4,(i%3-1)*6,t)}/>;})}
  <Pencil x={lerp(720,1150,scan)} y={245} scale={.7} r={36}/>
  <Text x={1240} y={295} size={38}>Ghi đúng. Cộng đủ. Rồi mới chọn.</Text>
 </Camera>;
};
const Recurring:React.FC<Ctx>=(c)=>{
 if(typeof c.s.data?.monthly==='number')return <RecurringMath {...c}/>;
 const walk=phase(c,.03,.94),cut=cue(c,.3),labels=['GIA HẠN','SỬ DỤNG?','GIỮ / DỪNG'];
 return <Camera x={lerp(870,1090,walk)} scale={1.06}>
  <Stroke d="M280 470H1640" stroke={P.line} width={8}/>
  {[420,960,1500].map((x,i)=><g key={i}><circle cx={x} cy={470} r={17} fill={i<walk*3?green:P.line}/><Tag x={x} y={300} label={labels[i]} fill={i===1?gold:cream}/><Text x={x} y={755} size={27}>{['Đến kỳ lại trừ','Có còn cần không?','Đọc điều kiện trước'][i]}</Text></g>)}
  {Array.from({length:5},(_,i)=>{const t=q(walk,i*.075,i*.075+.6);const x=lerp(220,1620,t);return <Receipt key={i} x={x} y={530+(i%2)*17} scale={.62} amount="Hàng tháng" label="CHI ĐỊNH KỲ" rotate={(i%3-1)*5} opacity={1-q(cut,.45+i*.1,.65+i*.1)}/>;})}
  <g transform={`translate(${lerp(1900,1500,cut)} 560)`}><Stroke d="M-104-100L98 100M-104 100L98-100" stroke={red} width={12}/><Text x={0} y={153} size={27} fill={red}>Chỉ dừng khoản thật sự không cần.</Text></g>
 </Camera>;
};
const RecurringMath:React.FC<Ctx>=(c)=>{
 const monthly=value(c.s,'monthly',120000),months=value(c.s,'months',12),annual=value(c.s,'annual',monthly*months),t=cue(c,.6),count=Math.floor(t*months);
 return <Camera scale={lerp(1.08,1,phase(c,.3,.98))}>
  <Phone x={340} y={525} scale={.9}><Text x={0} y={-160} size={25}>DỊCH VỤ GIẢ ĐỊNH</Text><Text x={0} y={-55} size={41}>{money(monthly)}</Text><Text x={0} y={0} size={27}>đồng / tháng</Text><Tag x={0} y={115} label="CÒN DÙNG?" fill={gold} width={235}/></Phone>
  {Array.from({length:12},(_,i)=><g key={i} transform={`translate(${740+(i%4)*245} ${350+Math.floor(i/4)*142})`} opacity={q(t,i/15,(i+3)/15)}><Receipt x={0} y={0} amount={money(monthly)} label={`THÁNG ${i+1}`} scale={.57}/></g>)}
  <Text x={1180} y={800} size={49} fill={green}>{count} × {money(monthly)} = {money(count*monthly)}</Text>
  <Text x={1180} y={864} size={28} weight={400} opacity={phase(c,.65,.97)}>Tổng năm: {money(annual)} đ • Đã trả không chắc được hoàn.</Text>
 </Camera>;
};
const Annual:React.FC<Ctx>=(c)=>{
 const build=cue(c,.65),count=Math.floor(build*12),reveal=phase(c,.65,.98),total=value(c.s,'annual',1200000),per=value(c.s,'monthly',total/12);
 return <Camera scale={lerp(1.08,1,reveal)}>
  <Envelope x={1470} y={580} label="KHOẢN THEO NĂM" amount={money(total)} open={build} scale={1.5}/>
  <g transform="translate(225 350)">{Array.from({length:12},(_,i)=>{const x=(i%4)*190,y=Math.floor(i/4)*140;const t=q(build,i/13,(i+1.6)/13);const xy=arc([x,y],[1150,190],phase(c,.7+i*.012,.86+i*.01),80);return <g key={i} transform={`translate(${xy[0]} ${xy[1]})`} opacity={t}><rect x="-70" y="-51" width="144" height="105" rx="7" fill={gold} stroke={ink} strokeWidth={3}/><Text x={0} y={-12} size={23}>THÁNG {i+1}</Text><Text x={0} y={27} size={27}>{money(per)}</Text></g>;})}</g>
  <Text x={595} y={235} size={46}>12 khoản nhỏ</Text><Text x={1470} y={293} size={31}>{/hạn đã gần/.test(c.s.text.toLowerCase())?'Gần hạn? Tính lại phần còn thiếu.':'Dự kiến để chủ động chuẩn bị.'}</Text>
  <Text x={960} y={818} size={48} fill={green}>{count} × {money(per)} = {money(count*per)}</Text>
 </Camera>;
};
const Calendar:React.FC<Ctx>=(c)=>{
 const go=phase(c,.03,.94),income=cue(c,.24),day=Math.min(30,1+Math.floor(go*29)),salaryLate=/trước.*lương|lương.*sau|đầu tháng/.test(c.s.text.toLowerCase());
 const payday=salaryLate?25:5;
 return <Camera x={lerp(875,1040,go)} scale={1.06}>
  <g transform="translate(285 320)">{Array.from({length:30},(_,i)=>{const x=(i%10)*150,y=Math.floor(i/10)*145,active=i+1===day;return <g key={i} transform={`translate(${x} ${y})`}><rect x="-62" y="-44" width="126" height="112" rx="6" fill={active?gold:(i+1===payday?'#DCE9DB':cream)} stroke={active?ink:P.line} strokeWidth={active?4:2}/><Text x={0} y={4} size={33}>{i+1}</Text>{[1,10,20].includes(i+1)&&<Text x={0} y={45} size={17} fill={red}>ĐẾN HẠN</Text>}{i+1===payday&&<Text x={0} y={45} size={17} fill={green}>LƯƠNG VỀ</Text>}</g>;})}</g>
  <Wallet x={430} y={805} scale={.68} label="SỐ DƯ ĐẦU KỲ" amount="Cần tính"/>
  <Bill x={lerp(1720,1450,income)} y={lerp(160,700,income)} value="Thu nhập" scale={.87} rotate={lerp(15,0,income)}/>
  <Text x={1180} y={800} size={38} fill={salaryLate?red:green}>Cùng tổng tiền, khác ngày đến hạn.</Text>
 </Camera>;
};
const Buffer:React.FC<Ctx>=(c)=>{
 const fund=cue(c,.6),shock=phase(c,.65,.97),count=Math.floor(fund*8);
 return <Camera scale={lerp(1,1.13,phase(c,.3,.98))}>
  {Array.from({length:8},(_,i)=>{const t=q(fund,i*.08,i*.08+.32),xy=arc([440+i*42,285],[995+(i%4)*30,365],t,70);return <Bill key={i} x={xy[0]} y={xy[1]} scale={.43} value="Góp dần" opacity={(i<=count?1:0)*(1-q(t,.85,1))} rotate={i%2?5:-5}/>;})}
  <Jar x={1040} y={570} amount={typeof c.s.data?.amount==='number'?`${money(c.s.data.amount)} đ`:'Tùy khả năng'} fillLevel={fund*.7} dark scale={1.36}/>
  <g transform={`translate(${lerp(1980,1485,shock)} 405) rotate(${lerp(25,0,shock)})`}><Receipt x={0} y={0} scale={1.1} amount="Đột xuất" label="SỬA CHỮA"/><Stroke d="M-68-31L68 31" stroke={red} width={5}/></g>
  <Stroke d={`M1370 300V${300+455*shock}`} stroke={gold} width={12}/>
  <Text x={440} y={515} size={45} fill={cream}>Một lớp đệm.</Text><Text x={440} y={575} size={29} weight={400} fill={cream}>Để bất ngờ bớt xô lệch</Text><Text x={440} y={620} size={29} weight={400} fill={cream}>những khoản đã có lịch.</Text>
  <Text x={1040} y={850} size={27} fill={cream}>Số tiền, vị trí giữ và ưu tiên tùy hoàn cảnh.</Text>
 </Camera>;
};
const Choice:React.FC<Ctx>=(c)=>{
 const weigh=phase(c,.04,.9),total=cue(c,.5),swap=/bốn triệu|giữ.*mười triệu/.test(c.s.text.toLowerCase());
 const tilt=lerp(-13,10,total);
 return <Camera scale={1.04}>
  <path d="M960 440L850 790H1070Z" fill={green} stroke={ink} strokeWidth={4}/><circle cx={960} cy={435} r={29} fill={gold} stroke={ink} strokeWidth={4}/>
  <g transform={`translate(960 435) rotate(${tilt})`}><Stroke d="M-575 0H575" width={12}/><Stroke d="M-520 0V180M520 0V180" width={4}/><path d="M-695 180Q-520 330-345 180ZM345 180Q520 330 695 180Z" fill={cream} stroke={ink} strokeWidth={4}/><Receipt x={-520} y={120} label={swap?'GIỮ MỨC CHI':'GIÁ MUA'} amount={swap?'10 triệu':'Cần cộng'} scale={.9}/><g transform={`translate(520 ${lerp(-220,110,total)})`} opacity={total}><Receipt x={0} y={0} label={swap?'THIẾT YẾU TĂNG':'CHI PHÍ KÈM'} amount={swap?'Tính lại':'Dùng + sửa'} scale={.9}/></g></g>
  <Text x={960} y={258} size={46}>{swap?'Mỗi hoàn cảnh có một phép tính.':'So cả chi phí sau lúc thanh toán.'}</Text>
  <Pencil x={lerp(1840,1430,weigh)} y={800} r={-38} scale={.7}/>
 </Camera>;
};
const Automate:React.FC<Ctx>=(c)=>{
 const schedule=phase(c,.03,.4),send=cue(c,.5),done=phase(c,.8,.98);
 return <Camera scale={lerp(1.08,1,done)}>
  <Phone x={470} y={530} scale={1.03}><Text x={0} y={-165} size={25}>LỊCH CHUYỂN</Text><Text x={0} y={-80} size={43}>Lương về</Text><Text x={0} y={-28} size={22}>Sau khoản phải trả</Text><rect x="-111" y="18" width="222" height="68" rx="15" fill={green}/><Text x={0} y={61} size={26} fill={cream}>{typeof c.s.data?.amount==='number'?`${money(c.s.data.amount)} đ`:'Mức phù hợp'}</Text><circle cx={65} cy={139} r={25} fill={schedule>.7?gold:P.line}/><Text x={-21} y={148} anchor="end" size={23}>BẬT LỊCH</Text></Phone>
  <Jar x={1510} y={590} amount="Góp đều" fillLevel={send*.6} scale={1.05}/>
  <Stroke d="M700 520C850 290 1120 290 1330 500" stroke={P.line} width={5} dash="10 13"/>
  {[0,1,2,3].map(i=>{const t=q(send,i*.12,i*.12+.5);const xy=arc([680,550],[1490+i*10,390],t,180);return <Bill key={i} x={xy[0]} y={xy[1]} value="Tự chọn" scale={.52} opacity={(send>i*.12?1:0)*(1-q(t,.85,1))} rotate={lerp(-13,0,t)}/>;})}
  <Hand x={lerp(930,535,schedule)} y={lerp(790,680,schedule)} rotate={-50} scale={.52}/>
  <g opacity={done}><Check x={1510} y={275} scale={1.3}/><Text x={1050} y={818} size={36}>Tự động giúp nhớ. Vẫn cần kiểm tra số dư.</Text></g>
 </Camera>;
};
const Review:React.FC<Ctx>=(c)=>{
 const reveal=phase(c,.04,.8),reconcile=cue(c,.35),mark=phase(c,.7,.97);
 const rows=[['THU NHẬP','Ghi đủ'],['CHI THỰC TẾ','Cộng đủ'],['ĐỂ DÀNH','Đối chiếu']];
 return <Camera x={lerp(860,1030,reveal)} scale={lerp(1.16,1.02,reveal)}>
  <g transform="translate(930 510)"><path d="M-620-285H560L620-225V300H-620Z" fill="#FFFDF6" stroke={ink} strokeWidth={4}/><path d="M560-285V-225H620" fill="none" stroke={ink} strokeWidth={3}/><Text x={0} y={-205} size={37}>ĐỐI CHIẾU CUỐI KỲ</Text>
   {rows.map(([label,amount],i)=><g key={label} opacity={q(reveal,i*.2,i*.2+.25)}><Stroke d={`M-525 ${-120+i*133}H525`} stroke={P.line} width={2}/><Text x={-510} y={-55+i*133} size={29} anchor="start">{label}</Text><Text x={255} y={-55+i*133} size={37} anchor="end" fill={i===2?green:ink}>{amount}</Text>{reconcile>i*.23&&<Check x={435} y={-68+i*133} scale={.85}/>}</g>)}
  </g><Pencil x={lerp(1700,1410,mark)} y={lerp(775,734,mark)} r={-30}/>
  <Text x={930} y={875} size={28} fill={green}>Còn trong tài khoản ≠ đã có thể dùng hết.</Text>
 </Camera>;
};
const CTA:React.FC<Ctx>=(c)=>{
 const travel=phase(c,.02,.95),take=cue(c,.55),stops=[[330,660],[750,405],[1190,660],[1600,405]];
 const labels=['GHI LẠI','CHỌN 1 KHOẢN','THỬ ĐIỀU CHỈNH','XEM LẠI'];
 const x=lerp(330,1600,travel),y=lerp(660,405,travel)-Math.sin(travel*Math.PI*3)*100;
 return <Camera scale={lerp(1.02,1.06,travel)}>
  <Stroke d="M330 660C450 660 550 405 750 405S1050 660 1190 660 1450 405 1600 405" stroke={P.line} width={12}/>
  {stops.map(([sx,sy],i)=><g key={i}><circle cx={sx} cy={sy} r={48} fill={travel>=i/3?green:cream} stroke={ink} strokeWidth={4}/><Text x={sx} y={sy+13} size={37} fill={travel>=i/3?cream:ink}>{i===0?'1':i===3?'30':i===1?'7':'14'}</Text><Text x={sx} y={sy+(i%2?-95:110)} size={28}>{labels[i]}</Text></g>)}
  <g transform={`translate(${x} ${y-58}) rotate(${lerp(-5,5,travel)})`}><Receipt x={0} y={0} scale={.65} label="MỘT KHOẢN" amount={take>.8?'Bắt đầu':'Chọn đi'}/></g>
  <Text x={960} y={235} size={53}>30 ngày. Một thay đổi có thể kiểm tra.</Text>
  <g opacity={phase(c,.78,.98)}><Check x={775} y={850}/><Text x={1035} y={862} size={36} fill={green}>Bắt đầu từ giao dịch gần nhất.</Text></g>
 </Camera>;
};

/** Some beats share a broad topic but make a different claim. These overrides
 * bind the visible action to that claim instead of merely relabelling a stage. */
const specific=(c:Ctx):React.ReactNode=>{
 const a=phase(c,.03,.42),t=cue(c,.55),b=phase(c,.58,.97);
 const act=action(c.s);
 if(c.s.id==='b05')return <Camera>
  <Envelope x={450} y={540} label="THU NHẬP" amount="" open={a} scale={1.35}/><Envelope x={960} y={540} label="CHO TỪNG VIỆC" amount="" open={t} scale={1.35}/>
  {Array.from({length:4},(_,i)=>{const xy=arc([450,420],[900+i*40,450],q(t,i*.1,i*.1+.6),90);return <Bill key={i} x={xy[0]} y={xy[1]} scale={.55} value="Giao việc" opacity={a}/>;})}
  <g transform={`translate(${lerp(2000,1500,b)} 535)`}><rect x="-155" y="-190" width="310" height="380" rx="12" fill={cream} stroke={ink} strokeWidth={4}/><rect x="-155" y="-190" width="310" height="75" rx="12" fill={green}/><Text x={0} y={-140} size={27} fill={cream}>KẾ HOẠCH</Text><Text x={0} y={35} size={105}>30</Text><Text x={0} y={105} size={30}>NGÀY</Text></g>
  <Text x={960} y={825} size={35}>Nhìn rõ lựa chọn trước khi giữ hay đổi.</Text>
 </Camera>;
 if(act==='spread_receipts')return <Camera x={lerp(960,1060,b)} scale={lerp(1.05,1.2,b)}>
  {Array.from({length:12},(_,i)=>{const tt=q(a,i*.033,.5+i*.033);return <Receipt key={i} x={lerp(390,420+(i%6)*200,tt)} y={lerp(600,410+Math.floor(i/6)*250,tt)} scale={.77} label="KHOẢN NHỎ" amount="?" rotate={lerp(-25,(i%5-2)*6,tt)}/>;})}
  <g transform={`translate(${lerp(550,1370,t)} 465) rotate(-18)`}><circle r="120" fill={cream} fillOpacity=".15" stroke={ink} strokeWidth={10}/><Stroke d="M-85 85L-170 170" stroke={green} width={31}/><Text x={0} y={17} size={45}>Cộng đủ</Text></g>
 </Camera>;
 if(act==='remove_duplicate_transfer')return <Camera>
  <Wallet x={440} y={480} label="TÀI KHOẢN A" amount="Của mình" open={1}/><Wallet x={1450} y={480} label="TÀI KHOẢN B" amount="Của mình" open={1}/>
  <Stroke d="M660 400Q960 220 1250 400" stroke={P.line} width={6} dash="10 14"/>
  {[0,1,2].map(i=>{const xy=arc([530,400],[1350,400],q(a,i*.1,i*.1+.65),150);return <Bill key={i} x={xy[0]} y={xy[1]} value="Nội bộ" scale={.63}/>;})}
  <Receipt x={760} y={720} label="LẦN RÚT / CHUYỂN" amount="Chưa rõ chi" scale={.9}/><Receipt x={1150} y={720} label="LẦN MUA THẬT" amount="Ghi đúng" scale={.9}/>
  <g opacity={t}><Stroke d="M655 600L860 830M860 600L655 830" stroke={red} width={9}/><Text x={960} y={265} size={44}>Đừng đếm hai lần cùng một khoản.</Text></g>
 </Camera>;
 if(c.s.data?.fields)return <Camera>
  <g transform="translate(960 510)"><rect x="-770" y="-230" width="1540" height="520" rx="12" fill="#FFFDF6" stroke={ink} strokeWidth={4}/>{['NGÀY','KHOẢN CHI','SỐ TIỀN','GHI CHÚ'].map((label,i)=><g key={label}><rect x={-770+i*385} y="-230" width="385" height="88" fill={i%2?green:ink}/><Text x={-575+i*385} y={-174} size={31} fill={cream}>{label}</Text>{[0,1,2].map(j=><g key={j} opacity={q(t,j*.16,j*.16+.35)}><Text x={-575+i*385} y={-50+j*110} size={27} weight={400}>{[['01','02','03'],['Đi lại','Ăn uống','Tiền mặt'],['Ghi thật','Ghi thật','Ghi thật'],['Nội dung','Lý do','Nhớ bổ sung']][i][j]}</Text><Stroke d={`M${-730+i*385} ${-12+j*110}H${-425+i*385}`} stroke={P.line} width={2}/></g>)}</g>)}</g>
  <Pencil x={lerp(1800,1570,b)} y={790} r={-25}/>
 </Camera>;
 if(act==='match_reimbursement')return <Camera>
  <Receipt x={lerp(400,650,a)} y={510} label="TRẢ TRƯỚC" amount="Ăn chung" scale={1.5} rotate={-4}/><Receipt x={lerp(1700,1270,t)} y={510} label="BẠN HOÀN LẠI" amount="Ghép đúng" scale={1.5} rotate={4}/>
  <Stroke d={`M770 720Q960 ${lerp(850,765,b)} 1150 720`} stroke={green} width={8}/>
  <Text x={960} y={276} size={45}>Ghép hai dòng của cùng một việc.</Text><Text x={960} y={844} size={39} fill={green} opacity={b}>Chỉ giữ phần chi thực sự của mình.</Text>
 </Camera>;
 if(act==='repair_vs_treat'||act==='use_and_replenish_buffer'){
  const use=act==='use_and_replenish_buffer';
  return <Camera>
   {use?<Jar x={530} y={520} amount="Đã chuẩn bị" fillLevel={lerp(.72,.3,t)+b*.18} scale={1.2}/>:<Plate x={470} y={600} scale={1.4}/>}
   <Scooter x={1450} y={575} scale={1.45} broken={t<.8}/>
   <Envelope x={960} y={570} label={use?'DÙNG ĐÚNG VIỆC':'KHOẢNG THỞ'} amount="" open={a} scale={1.05}/>
   {[0,1,2].map(i=>{const xy=arc(use?[560,370]:[440,430],[1320+i*55,450],q(t,i*.08,i*.08+.65),120);return <Bill key={i} x={xy[0]} y={xy[1]} scale={.55} value={use?'Sửa xe':'Dành trước'} opacity={a}/>;})}
   {use&&[0,1,2].map(i=>{const xy=arc([1040+i*70,750],[500+i*35,350],q(b,i*.08,i*.08+.7),100);return <Bill key={i} x={xy[0]} y={xy[1]} scale={.45} value="Bù dần" opacity={b*(1-q(b,.9,1))}/>;})}
   <Text x={470} y={820} size={34}>{use?'Xem khả năng bổ sung từng bước.':'Niềm vui hôm nay'}</Text><Text x={1450} y={820} size={34} fill={green}>{use?'Khoản đệm đang làm đúng việc.':'Xe hỏng vẫn cần xử lý.'}</Text>
  </Camera>;
 }
 if(act==='keep_or_reduce')return <Camera>
  <Text x={565} y={280} size={41}>Giữ điều đáng tiền</Text><Text x={1400} y={280} size={41}>Đổi tần suất</Text>
  <Plate x={530} y={570} scale={1.55}/><Check x={530} y={805} scale={1.25}/>
  {Array.from({length:6},(_,i)=><g key={i} opacity={i%2?1-q(t,i*.08,i*.08+.45):1} transform={`translate(${1120+(i%3)*210} ${440+Math.floor(i/3)*210})`}><Plate x={0} y={0} scale={.54}/><Receipt x={73} y={45} scale={.36} amount="Thêm" label="TẦN SUẤT"/></g>)}
  <Text x={1400} y={825} size={31} fill={green} opacity={b}>Không cần cắt đều mọi thứ.</Text>
 </Camera>;
 if(act==='select_one_receipt')return <Camera>
  {Array.from({length:7},(_,i)=>{const chosen=i===3;return <Receipt key={i} x={lerp(340+i*200,chosen?960:340+i*200,t)} y={lerp(570+(i%2)*30,chosen?450:655,t)} scale={chosen?lerp(.82,1.45,t):.82} opacity={chosen?1:1-t*.75} rotate={chosen?lerp(-5,0,t):(i%3-1)*9} label={chosen?'MỘT KHOẢN':'GIAO DỊCH'} amount={chosen?'Thử thay đổi':'?'}/>;})}
  <Pencil x={lerp(1740,1200,b)} y={690} r={-30}/><Text x={960} y={800} size={39} fill={green} opacity={b}>Ghi rõ việc làm và ngày kiểm lại.</Text>
 </Camera>;
 if(act==='annual_calendar')return <Camera>
  <g transform="translate(1040 530)"><rect x="-690" y="-250" width="1380" height="525" rx="12" fill="#FFFDF6" stroke={ink} strokeWidth={4}/><rect x="-690" y="-250" width="1380" height="70" fill={green}/><Text x={0} y={-201} size={32} fill={cream}>KHOẢN DỰ KIẾN TRONG NĂM</Text>{Array.from({length:12},(_,i)=><g key={i} transform={`translate(${-555+(i%6)*220} ${-85+Math.floor(i/6)*220})`}><Text x={0} y={-25} size={26}>THÁNG {i+1}</Text><rect x="-87" y="-7" width="174" height="113" fill={cream} stroke={P.line} strokeWidth={2}/>{[2,6,10].includes(i)&&<g opacity={q(t,(i/12)*.5,(i/12)*.5+.4)}><Tag x={0} y={47} label={i===2?'BẢO DƯỠNG':i===6?'THAY ĐỒ DÙNG':'ĐỊNH KỲ'} width={160} fill={gold}/></g>}</g>)}</g>
  <Pencil x={lerp(300,1450,b)} y={740} r={33}/>
 </Camera>;
 if(act==='reserve_envelope')return <Camera>
  <Wallet x={440} y={560} label="TÀI KHOẢN" amount="Đang có" open={1} scale={1.2}/><Envelope x={1390} y={560} label="DỰ TRÙ THÁNG SAU" amount="Đã có việc" open={t} scale={1.65}/>
  {Array.from({length:5},(_,i)=>{const xy=arc([450+i*28,450],[1310+i*35,420],q(t,i*.08,i*.08+.55),150);return <Bill key={i} x={xy[0]} y={xy[1]} value="Dự trù" scale={.58}/>;})}
  <g opacity={b}><Tag x={1390} y={790} label="CHƯA PHẢI TIỀN RẢNH" fill={gold} width={500}/><Text x={450} y={805} size={34} fill={cream}>Tổng tiền không tự tăng.</Text></g>
 </Camera>;
 if(act==='bridge_due_date_gap')return <Camera>
  <Text x={410} y={300} size={35} fill={cream}>NGÀY PHẢI TRẢ</Text><Text x={1500} y={300} size={35} fill={cream}>NGÀY THU NHẬP VỀ</Text>
  <path d="M150 600H710V850H150ZM1230 600H1790V850H1230Z" fill="#466B55"/>
  <Receipt x={430} y={470} label="NGHĨA VỤ" amount="Đến hạn" scale={1.15}/><Envelope x={1490} y={470} label="THU NHẬP" amount="Về sau" open={a} scale={1.2}/>
  <g transform={`translate(960 ${lerp(1000,590,t)})`}><rect x="-260" y="-33" width="520" height="66" rx="8" fill={gold} stroke={cream} strokeWidth={4}/><Text x={0} y={12} size={31}>KHOẢNG ĐỆM PHÙ HỢP</Text></g>
  <Bill x={lerp(1460,460,b)} y={500} value="Đúng hạn" scale={.8} opacity={b}/>
  <Text x={960} y={885} size={29} fill={cream}>Chưa tạo được? Nhận diện ngày thiếu và xem lịch có thể thương lượng.</Text>
 </Camera>;
 if(act==='schedule_reminder'||act==='assign_and_schedule')return <Camera>
  <Phone x={540} y={520} scale={1.12}><Text x={0} y={-168} size={25}>NHẮC TRƯỚC HẠN</Text><g transform={`rotate(${lerp(-12,0,t)} 0 -65)`}><path d="M-47-35V-90Q-47-155 0-155Q47-155 47-90V-35L65-15H-65Z" fill={gold} stroke={ink} strokeWidth={4}/><circle cx={0} cy={4} r={13} fill={ink}/></g><Text x={0} y={80} size={28}>Kiểm số dư</Text><Text x={0} y={130} size={28}>Kiểm ngày lương</Text><g opacity={b}><Check x={0} y={180} scale={.7}/></g></Phone>
  <Envelope x={1370} y={520} label={act==='assign_and_schedule'?'KHOẢN DỰ TRÙ':'ĐÚNG NGÀY PHẢI TRẢ'} amount="Đã lên lịch" open={a} scale={1.55}/><Tag x={1370} y={800} label="NHẮC VIỆC KHÔNG TẠO RA TIỀN" fill={gold} width={650}/>
  <Hand x={lerp(1000,615,t)} y={lerp(900,700,t)} rotate={-65} scale={.6}/>
 </Camera>;
 if(act==='monthly_vs_timing')return <Camera>
  <g transform="translate(500 510)"><rect x="-300" y="-250" width="600" height="520" rx="14" fill="#FFFDF6" stroke={ink} strokeWidth={4}/><Text x={0} y={-165} size={36}>CẢ THÁNG ĐỦ KHÔNG?</Text><Text x={0} y={-60} size={56}>THU − CHI</Text><Wallet x={0} y={100} scale={.8} label="CÂN ĐỐI" amount="Kiểm tổng"/></g>
  <g transform={`translate(${lerp(1950,1390,t)} 510)`}><rect x="-300" y="-250" width="600" height="520" rx="14" fill="#FFFDF6" stroke={ink} strokeWidth={4}/><Text x={0} y={-165} size={36}>ĐẾN HẠN CÓ TIỀN?</Text><Text x={0} y={-65} size={56}>ĐÚNG NGÀY</Text><Receipt x={0} y={105} label="LỊCH DÒNG TIỀN" amount="Kiểm ngày" scale={1.02}/></g>
  <g opacity={b}><Check x={500} y={835}/><Check x={1390} y={835}/></g>
 </Camera>;
 if(act==='walk_calendar_balance'){
  const x=lerp(290,1670,phase(c,.03,.96));
  const y=interpolate(x,[290,600,850,1200,1360,1670],[420,460,690,710,350,410]);
  return <Camera>
   <Stroke d="M235 730H1725" stroke={red} width={3} dash="8 12"/><Text x={215} y={740} size={24} fill={red} anchor="end">ĐÁY</Text>
   <Stroke d="M290 420L600 460 850 690 1200 710 1360 350 1670 410" stroke={P.line} width={8}/>
   <defs><clipPath id="cash-balance-reveal"><rect x="230" y="250" width={1445*phase(c,.03,.96)} height="520"/></clipPath></defs>
   <g clipPath="url(#cash-balance-reveal)"><Stroke d="M290 420L600 460 850 690 1200 710 1360 350 1670 410" stroke={green} width={9}/></g>
   <circle cx={x} cy={y} r={15} fill={gold} stroke={ink} strokeWidth={4}/>
   <Receipt x={850} y={350} amount="Trả trước" label="HÓA ĐƠN" scale={.8}/><Envelope x={1390} y={190} amount="Về sau" label="THU NHẬP" scale={.73} open={a}/>
   <Text x={600} y={835} size={31}>Mang số dư hôm trước sang hôm sau.</Text><Text x={1420} y={835} size={31} fill={red}>Lệch ngày tạo chỗ thiếu.</Text>
   <Text x={960} y={895} size={20} weight={400}>Đường diễn biến tượng trưng, không phải chuỗi số dư thực tế.</Text>
  </Camera>;
 }
 if(act==='installments_on_calendar')return <Camera>
  <Package x={370} y={480} scale={1.6}/><Text x={370} y={760} size={33}>Tổng giá vẫn cần trả.</Text>
  <Stroke d="M650 530H1700" stroke={P.line} width={7}/>
  {Array.from({length:4},(_,i)=>{const tt=q(t,i*.13,i*.13+.4);return <g key={i} transform={`translate(${800+i*270} ${lerp(250,480,tt)})`}><Receipt x={0} y={0} label={`LẦN TRẢ ${i+1}`} amount="Còn hẹn" scale={.85}/><Text x={0} y={200} size={23}>ĐÚNG HẠN</Text></g>;})}
  <g opacity={b}><Tag x={1220} y={800} label="CẠNH CẢ NGHĨA VỤ CŨ + PHÍ NẾU CÓ" fill={gold} width={800}/></g>
  <Text x={1230} y={300} size={30}>Kiểm từng hạn, cộng lại tổng tiền.</Text>
 </Camera>;
 if(act==='total_purchase_cost')return <Camera>
  <Package x={365} y={520} scale={1.85}/>
  <Receipt x={790} y={530} label="GIÁ MUA" amount="Bắt đầu" scale={1.3}/>
  {['PHỤ KIỆN CẦN','PHÍ GIAO NẾU CÓ','CHI PHÍ SỬ DỤNG'].map((l,i)=>{const tt=q(t,i*.16,i*.16+.4);return <g key={l} transform={`translate(${lerp(1940,1130+i*270,tt)} ${470+i%2*100})`}><Receipt x={0} y={0} label={l} amount="Cộng đủ" scale={.88}/></g>;})}
  <g opacity={b}><Stroke d="M670 760H1775" stroke={green} width={7}/><Text x={1210} y={835} size={41} fill={green}>So tổng tiền phải bỏ ra.</Text></g>
 </Camera>;
 if(act==='one_change')return <Camera>
  <Text x={580} y={285} size={40}>Bớt một khoản lặp lại</Text><Text x={1440} y={285} size={40}>Giữ bữa gặp bạn</Text>
  {Array.from({length:5},(_,i)=><Receipt key={i} x={290+i*150} y={510+(i%2)*45} label="CHI THÊM" amount="Xem lại" scale={.66} opacity={i%2?1-q(t,i*.08,i*.08+.4):1} rotate={(i%3-1)*7}/>)}
  <Plate x={1440} y={545} scale={1.7}/><g opacity={b}><Check x={1440} y={790} scale={1.2}/><Pencil x={900} y={795} r={-30}/><Text x={580} y={855} size={31} fill={green}>Ghi cách đổi và mốc kiểm.</Text></g>
 </Camera>;
 if(act==='stop_cutting_essentials')return <Camera>
  <Receipt x={850} y={540} label="SỨC KHỎE" amount="Cần giữ" scale={1.5}/><Receipt x={1250} y={540} label="ĐÃ CAM KẾT" amount="Nghĩa vụ" scale={1.5}/>
  <Scissors x={lerp(320,680,a)*(1-t)+lerp(680,250,t)*t} y={560} open={lerp(1,.15,a)*(1-t)+.75*t} scale={1.2}/>
  <Hand x={lerp(1800,1280,t)} y={400} rotate={-10} scale={.65}/>
  <g opacity={b}><Stroke d="M705 745Q1040 870 1395 745" stroke={green} width={9}/><Text x={1040} y={865} size={38} fill={green}>Đừng làm đẹp con số bằng cách cắt điều cần giữ.</Text></g>
 </Camera>;
 if(act==='income_expense_gap')return <Camera>
  <Envelope x={470} y={580} label="THU NHẬP" amount="Có giới hạn" open={1} scale={1.25}/><g transform={`translate(${lerp(1530,1400,t)} 570) scale(${lerp(1.1,1.55,t)})`}><Envelope x={0} y={0} label="CHI THIẾT YẾU" amount="Đã vượt" open={1}/></g>
  <Text x={960} y={300} size={48} fill={red}>Thiết yếu &gt; thu nhập</Text>
  <g opacity={b}>{['NHÀ Ở','CÔNG VIỆC','SẮP XẾP NGHĨA VỤ'].map((l,i)=><Tag key={l} x={480+i*480} y={825} label={l} fill={i===1?gold:cream} width={400}/>)}</g>
 </Camera>;
 if(act==='own_progress'||act==='compare_and_adjust')return <Camera>
  <g transform="translate(960 540)"><path d="M-720-265H-20V275H-720ZM20-265H720V275H20Z" fill="#FFFDF6" stroke={ink} strokeWidth={4}/><Stroke d="M-20-265Q0-290 20-265M-20 275Q0 300 20 275" width={3}/>
   <Text x={-365} y={-185} size={33}>{act==='own_progress'?'MÌNH THÁNG TRƯỚC':'KẾ HOẠCH'}</Text><Text x={365} y={-185} size={33}>{act==='own_progress'?'MÌNH THÁNG NÀY':'THỰC TẾ'}</Text>
   {['Khoản chi rõ hơn','Ít quên hạn hơn','Nhận diện chỗ thiếu'].map((l,i)=><g key={l}><Text x={-600} y={-65+i*115} anchor="start" size={29} weight={400}>{l}</Text><Stroke d={`M180 ${-75+i*115}H580`} stroke={P.line} width={3}/><g opacity={q(t,i*.18,i*.18+.35)}><Check x={595} y={-78+i*115} scale={.75}/></g></g>)}
  </g><Pencil x={lerp(1810,1510,b)} y={820} r={-30}/>
  <Text x={960} y={875} size={29} fill={green}>{act==='own_progress'?'So với dữ liệu của chính mình.':'Chênh lệch → tìm nguyên nhân → sửa giả định.'}</Text>
 </Camera>;
 if(act==='same_total_different_jobs')return <Camera>
  <Wallet x={410} y={530} label="TRƯỚC" amount="Cùng tổng" open={1} scale={1.2}/>
  {[1000,1450].map((x,i)=><Envelope key={i} x={x} y={580} label={i?'KHOẢN DỰ TRÙ':'KHOẢNG ĐỆM'} amount="Có nhiệm vụ" open={a} scale={1.15}/>)}
  {Array.from({length:6},(_,i)=>{const xy=arc([385+(i%3)*35,415],[935+(i%2)*450+(i%3)*28,450],q(t,i*.065,i*.065+.55),120);return <Bill key={i} x={xy[0]} y={xy[1]} scale={.5} value="Cùng tiền"/>;})}
  <Text x={960} y={285} size={49}>Đổi chỗ ≠ sinh thêm tiền</Text><Text x={1190} y={825} size={36} fill={green} opacity={b}>Đổi cách nhận diện việc của từng đồng.</Text>
 </Camera>;
 if(act==='discount_vs_need'||act==='pause_purchase')return <Camera>
  <Package x={lerp(1400,1280,a)} y={500} scale={1.65}/><Tag x={1320} y={285} label={act==='discount_vs_need'?'GIẢM GIÁ':'CHƯA CẦN NGAY'} fill={gold} width={390}/>
  <Phone x={490} y={530} scale={1.05}><Text x={0} y={-160} size={26}>{act==='discount_vs_need'?'MÌNH CÓ CẦN?':'LƯU XEM SAU'}</Text><Package x={0} y={-5} scale={.58}/><rect x="-108" y="110" width="216" height="70" rx="15" fill={t>.6?green:P.line}/><Text x={0} y={154} size={25} fill={cream}>{act==='discount_vs_need'?'ĐỐI CHIẾU':'ĐÃ LƯU'}</Text></Phone>
  <Hand x={lerp(2000,1410,t)} y={480} rotate={-10} scale={.67}/>
  <g opacity={b}><Text x={1210} y={785} size={38} fill={green}>{act==='discount_vs_need'?'Chênh trên nhãn ≠ tiền dư thật.':'Dừng một nhịp. Xem lại kế hoạch.'}</Text><Text x={1210} y={842} size={28} weight={400}>Cần và đủ khả năng? Có thể mua hợp lý.</Text></g>
 </Camera>;
 if(act==='useful_vs_unused')return <Camera>
  <Package x={500} y={490} scale={1.6}/><Scooter x={1430} y={565} scale={1.5}/>
  <g opacity={t}><Stroke d="M320 310L680 710M680 310L320 710" stroke={red} width={11}/><Check x={1430} y={775} scale={1.3}/></g>
  <Text x={500} y={820} size={36}>Không còn muốn</Text><Text x={1430} y={865} size={36} fill={green}>Giải quyết nhu cầu thật</Text><Text x={960} y={265} size={43}>Công dụng + thời gian dùng + nhu cầu</Text>
 </Camera>;
 return null;
};

const Scenes:React.FC<Ctx>=(c)=>{
 const custom=specific(c);
 if(custom)return <>{custom}</>;
 switch(c.s.kind){
  case 'hook': return <Hook {...c}/>;
  case 'disclaimer': return <Disclaimer {...c}/>;
  case 'budget_before':return <Budget {...c}/>;
  case 'budget_after':return <Budget {...c} after/>;
  case 'daily':return <Daily {...c}/>;
  case 'dinner':return <Dinner {...c}/>;
  case 'essentials':return <Essentials {...c}/>;
  case 'audit':return <Audit {...c}/>;
  case 'recurring':return <Recurring {...c}/>;
  case 'annual':return <Annual {...c}/>;
  case 'calendar':return <Calendar {...c}/>;
  case 'buffer':return <Buffer {...c}/>;
  case 'choice':return <Choice {...c}/>;
  case 'automate':return <Automate {...c}/>;
  case 'review':return <Review {...c}/>;
  default:return <CTA {...c}/>;
 }
};

/** Sixteen distinct actions, not a deck of entrance-animated cards. Scene motion
 * is finite, causal and continues through late narration; no decorative loops. */
export const FlowLongFilm:React.FC<{plan:LongPlan}>=({plan})=>{
 const frame=useCurrentFrame();
 const index=Math.max(0,plan.segments.findIndex(s=>frame>=s.from&&frame<s.from+s.duration));
 const s=plan.segments[index];
 if(!s)return <AbsoluteFill style={{background:cream}}/>;
 const c={s,index,f:frame-s.from};
 const dark=s.kind==='buffer';
 const background=dark?'#19392F':s.kind==='calendar'?'#E8ECDD':s.kind==='dinner'?'#F2E2D5':cream;
 const entrance=q(c.f,0,Math.min(14,s.duration*.07));
 const previous=index?plan.segments[index-1]:null;
 const previousDark=previous?.kind==='buffer';
 const prevBg=previousDark?'#19392F':previous?.kind==='calendar'?'#E8ECDD':previous?.kind==='dinner'?'#F2E2D5':cream;
 return <AbsoluteFill style={{background,fontFamily:'Arial, sans-serif',fontVariantNumeric:'tabular-nums'}}>
   <svg width="1920" height="940" viewBox="0 0 1920 940" style={{position:'absolute',top:0,left:0,overflow:'hidden'}} aria-label="Minh họa dòng tiền bằng chuyển động vật thể nguyên bản">
    <path d="M90 906H1830" fill="none" stroke={dark?'#527264':P.line} strokeWidth={2}/>
    <Text x={90} y={68} anchor="start" size={23} fill={dark?'#B4CDBA':green}>{s.chapterTitle??'HIỂU DÒNG TIỀN CỦA MÌNH'}</Text>
    <Text x={90} y={128} anchor="start" size={47} fill={dark?cream:ink}>{s.kind==='disclaimer'?'Đọc trước khi áp dụng':s.headline}</Text>
    <Scenes {...c}/>
    <rect x="0" y="906" width="1920" height="34" fill={background}/>
    <Text x={90} y={931} size={19} weight={400} anchor="start" fill={dark?'#B4CDBA':P.muted}>SỐ LIỆU MINH HỌA • Nhân vật hư cấu • Điều chỉnh theo hoàn cảnh cá nhân</Text>
    <Text x={1825} y={931} size={19} weight={400} anchor="end" fill={dark?'#B4CDBA':P.muted}>{String(index+1).padStart(2,'0')} / {plan.segments.length}</Text>
    <rect x="90" y="905" width={1740*frame/plan.durationFrames} height="3" fill={dark?gold:green}/>
    {previous&&entrance<1&&<g opacity={1-entrance}><rect x={lerp(0,1940,entrance)} y="0" width="1920" height="940" fill={prevBg}/><path d={`M${lerp(0,1940,entrance)} 0V940`} stroke={dark?gold:green} strokeWidth={7}/></g>}
   </svg>
 </AbsoluteFill>;
};
