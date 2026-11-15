import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Bread,cue,Footer,LabHeading,P,progress,Tag} from './common';
import type {BreadLabShot} from './types';

export const BasketScope:React.FC<{shot:BreadLabShot}>=({shot})=>{
 const f=useCurrentFrame();const zoom=cue(shot,0,.1);const expand=cue(shot,1,.34);const weight=cue(shot,2,.64);const end=cue(shot,3,.85);
 const categories=[{name:'Ăn uống',x:510,y:423,color:'#b89753'},{name:'Nhà ở',x:1040,y:423,color:'#648c7c'},{name:'Đi lại',x:1510,y:423,color:'#b07863'},{name:'Y tế · học tập',x:1090,y:754,color:'#7f91a1'}];
 if(shot.data?.stage==='households')return <><LabHeading shot={shot} title="Cùng một bản tin, hai cơ cấu chi tiêu" subtitle="Giỏ minh họa định tính: cùng biến động giá nhưng phần một hộ thường mua có thể khác hộ khác"/>
 <svg width={1920} height={1080} style={{position:'absolute',inset:0}}>
  {[0,1].map(i=>{const x=180+i*930;return <g key={i} opacity={progress(f,i===0?zoom:expand,18)}><text x={x+270} y={303} fontSize={40} fontWeight={700} textAnchor="middle" fill={P.ink}>Giỏ {i===0?'A':'B'}</text><path d={`M${x} 391H${x+550}L${x+495} 821H${x+55}Z`} fill={P.white} stroke={P.ink} strokeWidth={4}/><path d={`M${x+138} 394Q${x+275} 268 ${x+412} 394`} fill="none" stroke={P.ink} strokeWidth={4}/><rect x={x+77} y={i===0?520:680} width={i===0?370:180} height={i===0?150:70} rx={8} fill={P.gold}/><rect x={x+77} y={i===0?699:499} width={i===0?180:370} height={i===0?70:150} rx={8} fill={P.green}/><Bread x={x+128} y={i===0?554:686} width={100}/><path d={`M${x+110} ${i===0?722:540}L${x+145} ${i===0?695:513}L${x+180} ${i===0?722:540}V${i===0?752:570}H${x+110}Z`} fill={P.white}/><text x={x+275} y={883} fontSize={29} fontWeight={600} textAnchor="middle" fill={P.ink}>{i===0?'Nhạy hơn với nhóm thường mua':'Cơ cấu khác → áp lực khác'}</text></g>;})}
  {Array.from({length:8},(_,i)=>{const t=progress(f,zoom+i*9,50);return <circle key={i} cx={455+(i%2?930:0)} cy={346+t*120} r={7} fill={i%2?P.green:P.gold} opacity={t>0&&t<1?.9:0}/>;})}
  <g opacity={progress(f,weight,15)}><text x={945} y={554} textAnchor="middle" fill={P.quiet} fontSize={46}>≠</text><text x={945} y={612} textAnchor="middle" fill={P.quiet} fontSize={24}>Khác trải nghiệm</text></g>
  <g opacity={progress(f,end,12)}><text x={959} y={947} textAnchor="middle" fill={P.ink} fontSize={32} fontWeight={600}>Cảm giác thiếu tiền không tự chứng minh bản tin sai.</text></g>
 </svg><Footer>Diện tích nhóm chỉ minh họa cơ cấu khác nhau, không phải quyền số CPI hay tỷ lệ chi tiêu đã đo; không thêm giá trị tiền mới.</Footer></>;
 return <><LabHeading shot={shot} title="Một chiếc bánh không phải cả giỏ đời sống" subtitle="Phạm vi khác nhau → trải nghiệm giá có thể khác nhau"/>
 <svg width={1920} height={1080} style={{position:'absolute',inset:0}}>
  <Bread x={120+progress(f,zoom,Math.max(20,expand-zoom))*325} y={472-progress(f,zoom,Math.max(20,expand-zoom))*65} width={220-progress(f,zoom,Math.max(20,expand-zoom))*120}/><Tag x={130} y={648} size={31}>Một mặt hàng</Tag>
  <path d="M415 312H1740L1640 886H540Z" fill="none" stroke={P.ink} strokeWidth={5}/>
  <path d="M600 315Q655 218 765 289M1450 315Q1380 218 1250 289" fill="none" stroke={P.ink} strokeWidth={5}/>
  <line x1={940} x2={940} y1={337} y2={850} stroke={P.rule} strokeWidth={3}/><line x1={465} x2={1698} y1={631} y2={631} stroke={P.rule} strokeWidth={3}/>
  {categories.map((c,i)=>{
   const p=progress(f,expand+i*8,25);const size=i===0?85:i===1?105:i===2?65:80;
   return <g key={c.name} opacity={p} transform={`translate(0,${(1-p)*50})`}>
    <rect x={c.x-size/2} y={c.y-56} width={size} height={112} rx={8} fill={c.color}/>
    {i===0?<Bread x={c.x-53} y={c.y-16} width={100}/>:i===1?<path d={`M${c.x-37} ${c.y}L${c.x} ${c.y-35}L${c.x+37} ${c.y}V${c.y+35}H${c.x-37}Z`} fill={P.white}/>:i===2?<><circle cx={c.x-20} cy={c.y+22} r={12} fill={P.white}/><circle cx={c.x+20} cy={c.y+22} r={12} fill={P.white}/><path d={`M${c.x-33} ${c.y+12}L${c.x-15} ${c.y-22}H${c.x+19}L${c.x+34} ${c.y+12}Z`} fill={P.white}/></>:<path d={`M${c.x-8} ${c.y-28}H${c.x+8}V${c.y-8}H${c.x+28}V${c.y+8}H${c.x+8}V${c.y+28}H${c.x-8}V${c.y+8}H${c.x-28}V${c.y-8}H${c.x-8}Z`} fill={P.white}/>}
    <text x={c.x} y={c.y+99} textAnchor="middle" fontSize={29} fontWeight={600} fill={P.ink}>{c.name}</text>
   </g>;
  })}
  <g opacity={progress(f,zoom,20)}><path d="M365 510Q425 510 470 470" fill="none" stroke={P.gold} strokeWidth={4} strokeDasharray="8 8"/></g>
  <g opacity={progress(f,weight,16)}><rect x={1435} y={700} width={271} height={120} rx={8} fill={P.white}/><Tag x={1460} y={746} size={24}>Cân theo chi tiêu</Tag><Tag x={1460} y={787} color={P.green} size={23}>Mỗi hộ có giỏ khác</Tag></g>
  {Array.from({length:9},(_,i)=>{
   const start=weight+i*6;const t=progress(f,start,Math.max(30,shot.duration-weight));return <circle key={i} cx={610+i*95} cy={890-(t*43)} r={5} fill={P.gold} opacity={f>=start?.6:0}/>;
  })}
  <g opacity={progress(f,end,10)}><text x={118} y={946} fontSize={31} fontWeight={600} fill={P.ink}>So cùng lượng, chất lượng và cùng kỳ; không kết luận cả gia đình từ giá một món.</text></g>
 </svg><Footer>Minh họa phạm vi và nhóm chi tiêu; kích thước các vật không phải quyền số CPI. Không thêm một rổ giá giả định mới.</Footer></>;
};
