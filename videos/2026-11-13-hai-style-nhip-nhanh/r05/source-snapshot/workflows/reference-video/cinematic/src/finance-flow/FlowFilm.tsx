import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import type {FinancePlan, FinanceSegment} from '../finance-demo/types';
import {Bill, Envelope, Hand, P, Plate, Printer, Receipt, Wallet} from './Objects';
import {arc, clamp, cue, lerp, money, p} from './timing';

type Context={plan:FinancePlan;s:FinanceSegment;f:number};
const FaceText:React.FC<React.PropsWithChildren<{x:number;y:number;size?:number;fill?:string;weight?:number;anchor?:'start'|'middle'|'end';opacity?:number}>>=({x,y,size=44,fill=P.ink,weight=700,anchor='middle',opacity=1,children})=><text x={x} y={y} fill={fill} fontSize={size} fontWeight={weight} textAnchor={anchor} opacity={opacity}>{children}</text>;

const Camera:React.FC<React.PropsWithChildren<{x?:number;y?:number;zoom?:number}>>=({x=960,y=470,zoom=1,children})=><g transform={`translate(960 470) scale(${zoom}) translate(${-x} ${-y})`}>{children}</g>;
const Desk:React.FC=()=> <g><rect x="-1200" y="-1000" width="4400" height="2600" fill={P.paper}/><path d="M-1200 815H3200M-1200 825H3200" stroke={P.line} strokeWidth="3"/><path d="M-1200 815L-900 200M3200 815L2900 200" stroke={P.line} strokeWidth="2"/><ellipse cx="1000" cy="785" rx="900" ry="35" fill={P.ink} opacity=".035"/></g>;
const Pencil:React.FC<{x:number;y:number;rotate?:number;scale?:number}>=({x,y,rotate=-30,scale=1})=><g transform={`translate(${x} ${y}) rotate(${rotate}) scale(${scale})`} stroke={P.ink} strokeWidth="5" strokeLinejoin="round"><path d="M-12-180H12V-10L0 22-12-10Z" fill={P.yellow}/><path d="M-12-10H12L0 22Z" fill={P.paper}/><path d="M-12-164H12M-4-155V-15" fill="none"/><path d="M0 22L-3 12H3Z" fill={P.ink}/></g>;

const Budget:React.FC<Context & {after?:boolean}>=({plan,s,f,after=false})=>{
  const income=cue(plan,s,after?'mười bốn triệu':'lương mười hai triệu',after?36:155);
  const spend=cue(plan,s,after?'chi tới':'chi mười triệu',after?85:200);
  const final=cue(plan,s,after?'tiền dư':'còn hai triệu',after?126:235);
  const look=p(f,0,Math.max(20,income-18));
  const emit=after?2:12;
  const cash:Array<{x:number;y:number;r:number}>=[];
  let inWallet=after?2:0;
  let inSpend=after?10:0;
  for(let i=0;i<emit;i++){
    const start=income+i*(after?7:2);
    if(f<start)continue;
    const arrival=p(f,start,start+28);
    const exit=p(f,spend+i*2,spend+i*2+28);
    const shouldSpend=after||i<10;
    const source:[number,number]=[930+(i%3)*18,255-(i%2)*12];
    const hold:[number,number]=[1395+(i%3)*37,555+Math.floor(i/3)*6];
    const dest:[number,number]=[355+(i%5)*43,525+Math.floor(i/5)*33];
    const pos=arrival<1?arc(source,hold,arrival,120):shouldSpend?arc(hold,dest,exit,185):hold;
    cash.push({x:pos[0],y:pos[1],r:lerp(-15,(i%3-1)*5,arrival)});
    if(arrival>=.96&&(!shouldSpend||exit<.08))inWallet++;
    if(shouldSpend&&exit>=.96)inSpend++;
  }
  return <Camera x={lerp(1260,960,look)} y={lerp(560,470,look)} zoom={lerp(1.45,1.03,look)}>
    <Desk/>
    <g transform={`translate(0 ${lerp(-250,0,p(f,Math.max(0,income-25),income))})`}><Envelope x={960} y={225} label="THU NHẬP" amount={after?'14 triệu':'12 triệu'} fill={P.yellow} open={p(f,income,income+25)}/></g>
    <Envelope x={450} y={585} label="CHI TIÊU" amount={`${inSpend} triệu`} fill={P.paper} open={1}/>
    <Wallet x={1440} y={590} label="CÒN DƯ" amount={`${inWallet} triệu`} open={p(f,0,35)}/>
    {after&&Array.from({length:10},(_,i)=><Bill key={`old${i}`} x={355+(i%5)*43} y={525+Math.floor(i/5)*33} scale={.45} value="1 tr" rotate={(i%3-1)*5}/>)}
    {after&&[0,1].map(i=><Bill key={`held${i}`} x={1395+i*37} y={555} scale={.45} value="1 tr"/>)}
    {cash.map((v,i)=><Bill key={i} {...v} rotate={v.r} scale={.45} value="1 tr"/>)}
    <g opacity={p(f,final,final+15)}><path d="M1270 710Q1440 765 1620 710" stroke={P.green} strokeWidth="8" fill="none"/><FaceText x={1440} y={786} size={45} fill={P.green}>{after?'Vẫn chỉ 2 triệu.':'12 − 10 = 2 triệu'}</FaceText></g>
    {after&&<g opacity={p(f,spend+22,spend+45)}><FaceText x={960} y={400} size={36} fill={P.red}>+2 triệu vừa vào… đã có nơi để đi.</FaceText></g>}
  </Camera>;
};

const Hook:React.FC<Context>=({plan,s,f})=>{
  const raise=cue(plan,s,'hai triệu',12);
  const gone=cue(plan,s,'chẳng tăng',54);
  const back=cue(plan,s,'ví mình trở về',145);
  const a=p(f,raise,raise+32),b=p(f,gone,gone+40),zoom=p(f,back,back+32);
  return <Camera x={lerp(960,1050,zoom)} y={lerp(480,555,zoom)} zoom={lerp(1.05,1.4,zoom)}><Desk/>
    <Wallet x={1000} y={610} scale={1.6} open={1} label="KHOẢN DƯ" amount="2 triệu"/>
    <FaceText x={1000} y={180} size={72} opacity={1-p(f,back,back+25)}>Lương tăng. Tiền dư đi đâu?</FaceText>
    {[0,1].map(i=>{
      const t=p(f,raise+i*5,raise+32+i*5);
      const initial=arc([690+i*250,-80],[960+i*72,510],t,0);
      const exit=arc([960+i*72,510],[470+i*970,560],b,150);
      return <Bill key={i} x={b>0?exit[0]:initial[0]} y={b>0?exit[1]:initial[1]} rotate={lerp((i?1:-1)*15,0,a)} value="1 triệu" scale={.85}/>;
    })}
    <g opacity={p(f,gone,gone+12)}><Envelope x={390} y={650} scale={.9} label="CHI THÊM" amount="1 triệu"/><Envelope x={1630} y={650} scale={.9} label="CHI THÊM" amount="1 triệu"/></g>
    <g opacity={p(f,back,back+15)}><FaceText x={1035} y={380} size={54} fill={P.red}>Khoản dư vẫn như cũ.</FaceText></g>
  </Camera>;
};

const Disclaimer:React.FC<Context>=({f})=>{
  const inPaper=p(f,0,24),stamp=p(f,31,43);
  return <Camera y={480} zoom={1.02}><Desk/>
    <Wallet x={1560} y={650} scale={.8} label="VÍ DỤ" amount="" open={0}/>
    <g transform={`translate(${lerp(-1100,960,inPaper)} 490) rotate(${lerp(-12,-2,inPaper)})`}>
      <path d="M-610-300H570L610-260V300H-610Z" fill="#FFFEF8" stroke={P.ink} strokeWidth="5"/>
      <path d="M570-300V-260H610" fill="none" stroke={P.ink} strokeWidth="4"/>
      <FaceText x={0} y={-170} size={35} fill={P.muted}>MIỄN TRỪ TRÁCH NHIỆM</FaceText>
      <FaceText x={0} y={-55} size={66}>Tình huống giả định.</FaceText>
      <FaceText x={0} y={28} size={40} weight={400}>Học cách lập ngân sách.</FaceText>
      <FaceText x={0} y={102} size={36} weight={400}>Không phải tư vấn tài chính cá nhân.</FaceText>
      <g transform={`translate(245 209) rotate(-7) scale(${lerp(1.8,1,stamp)})`} opacity={stamp}><rect x="-205" y="-38" width="410" height="76" rx="8" fill="none" stroke={P.red} strokeWidth="6"/><FaceText x={0} y={14} size={36} fill={P.red}>SỐ LIỆU MINH HỌA</FaceText></g>
    </g>
  </Camera>;
};

/** A continuous thirty-day input tape. The paper crosses the intake once per day;
 * processed receipts leave the output and accumulate in one physical pile. */
const DayTape:React.FC<{feed:number;shown:boolean;valueShown:boolean}>=({feed,shown,valueShown})=>{
  return <g opacity={shown?1:0}>
    <defs><clipPath id="flow-tape-window"><rect x="100" y="450" width="995" height="160"/></clipPath></defs>
    <g clipPath="url(#flow-tape-window)">
      <g transform={`translate(${1090+feed*92} 470)`}>
        <path d={`M${-29*92-80} 0H80V118H${-29*92-80}Z`} fill="#FFFDF4" stroke={P.ink} strokeWidth="4"/>
        {Array.from({length:30},(_,i)=><g key={i} transform={`translate(${-i*92} 0)`}>
          <path d="M-45 0V118" stroke={P.line} strokeWidth="3" strokeDasharray="5 6"/>
          <FaceText x={0} y={38} size={20} weight={400}>NGÀY</FaceText><FaceText x={0} y={77} size={38}>{i+1}</FaceText>
          <FaceText x={0} y={105} size={17} opacity={valueShown?1:0}>+60.000</FaceText>
        </g>)}
      </g>
    </g>
    <path d="M1082 452L1104 452M1082 603L1104 603" stroke={P.ink} strokeWidth="7" strokeLinecap="round"/>
  </g>;
};

const ReceiptPile:React.FC<{count:number;f:number;feedStart:number;feedEnd:number;complete?:boolean}>=({count,f,feedStart,feedEnd,complete=false})=><g>{Array.from({length:30},(_,i)=>{
  const release=feedStart+(i+.6)/30*(feedEnd-feedStart);
  const flight=complete?1:p(f,release,release+17);
  if(!complete&&count<i+1)return null;
  const xy=arc([1300,687],[690+(i%6)*58,690+Math.floor(i/6)*10],flight,70);
  return <Receipt key={i} x={xy[0]} y={xy[1]} rotate={lerp(0,(i%5-2)*7,flight)} scale={.43} day={i+1} label="CHI THÊM" amount="60.000"/>;
})}</g>;

const Magnifier:React.FC<{x:number;y:number;rotate?:number;opacity?:number}>=({x,y,rotate=-25,opacity=1})=><g transform={`translate(${x} ${y}) rotate(${rotate})`} opacity={opacity} stroke={P.ink} fill="none"><path d="M-73 74L-175 188" strokeWidth="31" strokeLinecap="round"/><path d="M-73 74L-175 188" stroke={P.yellow} strokeWidth="18" strokeLinecap="round"/><circle r="113" fill="#FFFEF8" fillOpacity=".1" strokeWidth="10"/><path d="M-73-48A88 88 0 0 1 -12-87" stroke="#fff" strokeWidth="7" strokeLinecap="round"/></g>;

const Daily:React.FC<Context>=({plan,s,f})=>{
  const daily=cue(plan,s,'sáu mươi nghìn',197);
  const month=cue(plan,s,'trong ba mươi ngày',221);
  const total=cue(plan,s,'một triệu tám',265);
  const feedStart=Math.max(daily,month-10),feedEnd=Math.max(feedStart+45,total-3);
  const feed=interpolate(f,[feedStart,feedEnd],[0,30],clamp);
  const count=Math.min(30,Math.floor(feed));
  const reveal=p(f,85,daily-12);
  const small=p(f,daily-20,daily+15);
  const cam=p(f,20,month-20);
  const ticket=arc([550,530],[1100,525],p(f,daily,feedStart-2),55);
  const lensX=lerp(660,550,p(f,0,70));
  return <Camera x={lerp(660,1080,cam)} y={lerp(500,515,cam)} zoom={lerp(1.48,1.10,cam)}><Desk/>
    <Wallet x={185} y={650} scale={.75} label="" amount="" open={1}/>
    <Printer x={1300} y={525} scale={1} frame={f} sum={count?money(count*60000):'0'} count={count} active={feed>0&&feed<30}/>
    <DayTape feed={feed} shown={reveal>.01} valueShown={f>=daily}/>
    <g opacity={1-p(f,feedStart-4,feedStart+2)}><Receipt x={ticket[0]} y={ticket[1]} amount={f>=daily?'60.000':'?'} label="KHOẢN NHỎ" scale={.67} rotate={lerp(-7,0,small)}/></g>
    <Magnifier x={lensX} y={475} rotate={lerp(-20,20,reveal)} opacity={1-p(f,115,daily-15)}/>
    <g opacity={1-p(f,95,130)}><FaceText x={650} y={235} size={45}>“Mình có mua gì lớn đâu?”</FaceText></g>
    <ReceiptPile count={count} f={f} feedStart={feedStart} feedEnd={feedEnd}/>
    <g opacity={p(f,daily,daily+10)}><FaceText x={620} y={315} size={47}>60.000 mỗi ngày</FaceText></g>
    <g opacity={count===30?1:0}><path d="M1200 700Q1360 750 1490 690" fill="none" stroke={P.red} strokeWidth="7"/><FaceText x={1340} y={793} size={58} fill={P.red}>30 ngày → 1,8 triệu</FaceText></g>
  </Camera>;
};

const Dinner:React.FC<Context>=({plan,s,f})=>{
  const meal=cue(plan,s,'bữa ăn',22);
  const add=cue(plan,s,'tổng chi',68);
  const sum=cue(plan,s,'hai triệu',95,true);
  const combine=cue(plan,s,'cộng lại',173);
  const used=cue(plan,s,'hết phần tăng lương',200,true);
  const plateIn=p(f,meal-12,meal+26);
  const mealFlight=p(f,add-12,sum-5);
  const totalTime=p(f,sum-10,sum+3);
  const paperStart=sum+8;
  const paper=p(f,paperStart,paperStart+22);
  const match=p(f,combine,Math.max(combine+25,used-5));
  const finalCamera=p(f,combine,used+5);
  const mealPos=arc([620,430],[1300,525],mealFlight,120);
  // First clear the machine along its bottom edge, then rise beside it. The
  // total paper stays opaque and cannot cover the calculator's numeric display.
  const totalPos:[number,number]=match<.45?[lerp(1300,890,match/.45),767]:arc([890,767],[840,330],(match-.45)/.55,0);
  return <Camera x={lerp(1080,870,finalCamera)} y={lerp(515,455,finalCamera)} zoom={lerp(1.10,1.08,finalCamera)}><Desk/>
    <Printer x={1300} y={525} frame={f} sum={totalTime>.9?'2.000.000':'1.800.000'} count={30} meal={f>=meal} active={mealFlight>0&&mealFlight<1}/>
    <ReceiptPile count={30} f={f} feedStart={0} feedEnd={1} complete/>
    <g transform={`translate(${lerp(-700,0,plateIn)} ${Math.sin(plateIn*Math.PI)*-50})`}>
      <Hand x={390} y={455} rotate={4} scale={1.4}/><Plate x={610} y={395} scale={1.10}/>
    </g>
    <Receipt x={mealPos[0]} y={mealPos[1]} amount="200.000" label="BỮA ĂN THÊM" scale={.66} rotate={lerp(-9,0,mealFlight)} opacity={plateIn*(1-p(f,sum-3,sum+10))}/>
    <g opacity={p(f,meal,meal+18)*(1-p(f,combine-15,combine))}><FaceText x={625} y={205} size={48}>Thêm một bữa ăn.</FaceText></g>
    <g opacity={p(f,combine-12,combine+2)}><Envelope x={500} y={350} scale={1.1} label="PHẦN TĂNG LƯƠNG" amount={match>.9?'Còn lại: 0':'2 triệu'} fill={P.yellow} open={p(f,combine,used)}/></g>
    {match>0?<Receipt x={totalPos[0]} y={totalPos[1]} amount="2.000.000" label="CHI TĂNG CẢ THÁNG" scale={lerp(.7,1.12,match)} rotate={lerp(0,-5,match)}/>:f>=paperStart?<g>
      <defs><clipPath id="flow-total-paper"><rect x="1180" y="687" width="240" height="250"/></clipPath></defs>
      <g clipPath="url(#flow-total-paper)"><Receipt x={1300} y={lerp(607,767,paper)} amount="2.000.000" label="CHI TĂNG CẢ THÁNG" scale={.7}/></g>
    </g>:null}
    {match>.01&&[0,1].map(i=>{
      const xy=arc([460+i*75,275],[1180+i*90,630],p(f,combine+i*6,used+i*2),135);
      return <Bill key={i} x={xy[0]} y={xy[1]} scale={.63} rotate={i?10:-10} value="1 triệu" opacity={1-p(f,used-5,used+10)}/>;
    })}
    <g opacity={p(f,used-5,used+10)}><FaceText x={650} y={615} size={57} fill={P.red}>Vừa hết phần tăng.</FaceText><FaceText x={650} y={683} size={31} weight={400}>1.800.000 + 200.000 = 2.000.000</FaceText></g>
  </Camera>;
};

const Choice:React.FC<Context>=({plan,s,f})=>{
  const keep=cue(plan,s,'mức chi mười triệu',40),four=cue(plan,s,'bốn triệu',105);
  const need=cue(plan,s,'chi phí thiết yếu tăng',142),recalc=cue(plan,s,'tính lại',185);
  const back=p(f,keep,four+10),stop=p(f,need,recalc);
  return <Camera x={lerp(960,1100,p(f,need,recalc+20))} y={485} zoom={1.05}><Desk/>
    <Wallet x={1370} y={570} scale={1.2} label="CÒN DƯ" amount={f<recalc?`${2+Math.round(back*2)} triệu`:'Tính lại'} open={1}/>
    <Envelope x={460} y={560} scale={1.1} label="GIỮ MỨC CHI" amount="10 triệu"/>
    {[0,1].map(i=>{const xy=arc([500+i*70,500],[1320+i*68,505],p(f,keep+i*5,four+i*5),150);return <Bill key={i} x={xy[0]} y={xy[1]} scale={.6} value="1 triệu" rotate={-7+i*14}/>;})}
    <FaceText x={950} y={190} size={56} opacity={1-stop}>Nếu giữ được mức chi ban đầu…</FaceText>
    <g opacity={p(f,four,four+20)*(1-stop)}><FaceText x={1330} y={340} size={65} fill={P.green}>14 − 10 = 4</FaceText></g>
    <g transform={`translate(0 ${lerp(700,0,stop)})`}>
      <Envelope x={905} y={650} scale={1.05} label="CHI PHÍ THIẾT YẾU" amount="Có thể tăng" fill={P.yellow}/>
      <Pencil x={1390} y={510} rotate={lerp(-60,-16,p(f,recalc,recalc+25))}/>
      <FaceText x={1080} y={230} size={52} fill={P.red}>Chi phí tăng? Tính lại.</FaceText>
      <FaceText x={1080} y={300} size={33} weight={400}>Đừng ép mình theo con số giả định.</FaceText>
    </g>
  </Camera>;
};

const BudgetTape:React.FC<{f:number;income:number;needs:number[];auto:number}>=({f,income,needs,auto})=>{
  // One piece of paper is cut into four lengths; the pieces retain their size.
  const portions=[260,240,180,220];
  const origins=portions.map((_,i)=>510+portions.slice(0,i).reduce((a,b)=>a+b,0));
  const targets:[[number,number],[number,number],[number,number],[number,number]]=[[360,615],[750,615],[1110,615],[1550,615]];
  return <g>{portions.map((w,i)=>{
    const alloc=i<3?p(f,needs[i],needs[i]+25):p(f,auto,auto+32);
    const origin:[number,number]=[origins[i]+w/2,340];
    const target=targets[i];
    const xy=arc(origin,target,alloc,70);
    return <g key={i} opacity={p(f,income,income+20)} transform={`translate(${xy[0]} ${xy[1]}) rotate(${lerp(0,i%2?4:-4,alloc)})`}>
      <rect x={-w/2+3} y="-42" width={w-6} height="84" rx="5" fill={P.yellow} stroke={P.ink} strokeWidth="4"/>
      {Array.from({length:Math.floor(w/35)},(_,j)=><path key={j} d={`M${-w/2+20+j*35} -22V22`} stroke={P.ink} strokeWidth="2" opacity=".3"/>)}
    </g>;
  })}</g>;
};

const Transfer:React.FC<Context>=({plan,s,f})=>{
  const income=cue(plan,s,'lương về',64),reserve=cue(plan,s,'khoản phù hợp',110);
  const house=cue(plan,s,'tiền nhà',156),living=cue(plan,s,'sinh hoạt',182),debt=cue(plan,s,'nghĩa vụ nợ',210),auto=cue(plan,s,'chuyển khoản tự động',260);
  const camera=p(f,0,income+25);
  return <Camera x={960} y={lerp(350,470,camera)} zoom={lerp(1.35,1.02,camera)}><Desk/>
    <Envelope x={960} y={240} scale={1.1} label="THU NHẬP VỀ" amount="Phân bổ phù hợp" fill={P.yellow} open={p(f,income,income+20)}/>
    <Envelope x={360} y={680} scale={.9} label="TIỀN NHÀ" amount="" open={p(f,house,house+20)}/>
    <Envelope x={750} y={680} scale={.9} label="SINH HOẠT" amount="" open={p(f,living,living+20)}/>
    <Envelope x={1110} y={680} scale={.9} label="NGHĨA VỤ NỢ" amount="" open={p(f,debt,debt+20)}/>
    <Wallet x={1550} y={680} scale={.9} label="TIẾT KIỆM" amount="Tự chọn mức" open={p(f,auto,auto+20)}/>
    <BudgetTape f={f} income={income} needs={[house,living,debt]} auto={auto}/>
    <g opacity={p(f,reserve,reserve+12)*(1-p(f,house,house+10))}><path d="M1300 330V250L1500 250V330Z" fill={P.green}/><FaceText x={1400} y={284} size={24} fill="#fff">GIỮ MỘT PHẦN</FaceText></g>
    <g transform={`translate(${lerp(2100,1540,p(f,auto-20,auto+10))} 365)`}>
      <circle r="78" fill={P.paper} stroke={P.ink} strokeWidth="5"/><circle r="58" fill="none" stroke={P.line} strokeWidth="2"/>
      <path d={`M0 0L${Math.sin(p(f,auto,auto+38)*Math.PI*2)*46} ${-Math.cos(p(f,auto,auto+38)*Math.PI*2)*46}M0 0L-25-20`} stroke={P.ink} strokeWidth="6" strokeLinecap="round"/>
      <FaceText x={0} y={128} size={30} fill={P.green}>Chuyển tự động</FaceText>
    </g>
  </Camera>;
};

const CTA:React.FC<Context>=({plan,s,f})=>{
  const choose=cue(plan,s,'chọn một khoản',120),month=cue(plan,s,'cộng đủ cả tháng',163),decide=cue(plan,s,'giữ hay giảm',225),one=cue(plan,s,'một khoản thôi',285);
  const take=p(f,choose,choose+30),sum=p(f,month,month+38),decision=p(f,decide,decide+28);
  return <Camera x={960} y={470} zoom={lerp(1.0,1.18,p(f,one,one+27))}><Desk/>
    {Array.from({length:8},(_,i)=><Receipt key={i} x={450+i*120} y={550+(i%2)*35} rotate={(i%3-1)*9} scale={.7} label={['ĐI LẠI','ĂN UỐNG','MUA SẮM'][i%3]} amount="?" opacity={i===3?0:1-take*.75}/>)}
    <g transform={`translate(${lerp(810,960,take)} ${lerp(585,445,take)}) rotate(${lerp(-9,0,take)})`}>
      <Receipt x={0} y={0} scale={lerp(.7,1.22,take)} label="MỘT KHOẢN CỦA BẠN" amount={sum>.9?'Cả tháng':'?'}/>
      <g opacity={sum}><path d="M-94-90H94M-94-40H94M-94 10H94" stroke={P.line} strokeWidth="4"/><FaceText x={0} y={80} size={35}>CỘNG ĐỦ</FaceText></g>
    </g>
    <Hand x={lerp(1600,1060,take)} y={lerp(790,500,take)} rotate={-90} scale={.85}/>
    <g opacity={decision}><path d="M860 645L720 735M1060 645L1200 735" stroke={P.ink} strokeWidth="5" fill="none"/><FaceText x={660} y={786} size={52} fill={P.green}>GIỮ</FaceText><FaceText x={1260} y={786} size={52} fill={P.red}>GIẢM</FaceText></g>
    <FaceText x={960} y={180} size={60} opacity={1-p(f,choose,choose+20)}>Xem lại một khoản đang lớn lên.</FaceText>
    <g opacity={p(f,one,one+16)}><circle cx="1200" cy="300" r="78" fill={P.yellow} stroke={P.ink} strokeWidth="5"/><FaceText x={1200} y={327} size={82}>1</FaceText></g>
  </Camera>;
};

/** Physical object explainer. Exact-take cues determine money, paper and tool actions.
 * Audio/captions belong to the host wrapper for direct comparison with other styles.
 * All moving objects are original code-native SVG; no paid visual-generation calls. */
export const FlowFilm:React.FC<{plan:FinancePlan}>=({plan})=>{
  const frame=useCurrentFrame();
  const s=plan.segments.find(v=>frame>=v.from&&frame<v.from+v.duration)??plan.segments[plan.segments.length-1];
  if(!s)return <AbsoluteFill style={{background:P.paper}}/>;
  const ctx={plan,s,f:frame-s.from};
  let scene:React.ReactNode;
  switch(s.visual){
    case'hook':scene=<Hook {...ctx}/>;break;
    case'disclaimer':scene=<Disclaimer {...ctx}/>;break;
    case'before':scene=<Budget {...ctx}/>;break;
    case'after':scene=<Budget {...ctx} after/>;break;
    case'daily':scene=<Daily {...ctx}/>;break;
    case'dinner':scene=<Dinner {...ctx}/>;break;
    case'choice':scene=<Choice {...ctx}/>;break;
    case'transfer':scene=<Transfer {...ctx}/>;break;
    default:scene=<CTA {...ctx}/>;
  }
  const note=s.visual==='transfer'?'Phân bổ tượng trưng • Tỷ lệ và số tiền cần phù hợp hoàn cảnh cá nhân':s.visual==='before'||s.visual==='after'?'Số liệu giả định • Mỗi tờ tiền minh họa tương ứng 1 triệu đồng':'Tình huống và số liệu giả định để minh họa';
  return <AbsoluteFill style={{background:P.paper,fontFamily:'Arial, sans-serif',fontVariantNumeric:'tabular-nums'}}>
    <svg width="1920" height="940" viewBox="0 0 1920 940" style={{position:'absolute',top:0,left:0,overflow:'hidden'}} aria-label="Mô phỏng tài chính bằng đồ vật chuyển động">
      {scene}
      {s.visual!=='disclaimer'&&<g><rect x="0" y="848" width="1920" height="92" fill={P.paper}/><path d="M90 853H1830" stroke={P.line} strokeWidth="2"/><FaceText x={90} y={896} anchor="start" size={22} weight={400} fill={P.muted}>{note}</FaceText></g>}
    </svg>
  </AbsoluteFill>;
};
