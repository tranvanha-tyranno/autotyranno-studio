import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Arrow,Bread,cue,Footer,LabHeading,P,progress} from './common';
import type {BreadLabShot} from './types';

export const Synthesis:React.FC<{shot:BreadLabShot}>=({shot})=>{
 const f=useCurrentFrame();const cost=cue(shot,0,.1);const prices=cue(shot,1,.32);const wages=cue(shot,2,.57);const connect=cue(shot,3,.8);
 const focus=[{x:470,y:410,name:'BẢNG GIÁ',sub:'Mặt bằng đã tăng',detail:'Tăng chậm ≠ trở lại giá cũ',at:prices,color:P.gold},{x:1425,y:410,name:'HÓA ĐƠN',sub:'Tổng chi phí',detail:'Trả thêm ≠ tiệm giữ thêm',at:cost,color:P.rust},{x:950,y:730,name:'KHOẢN THU',sub:'Đổi được lượng hàng nào?',detail:'Lương tăng ≠ sức mua tăng',at:wages,color:P.green}];
 return <><LabHeading shot={shot} title="Ba phía cùng chịu sức ép, không có gì mâu thuẫn" subtitle="Một chiếc bánh nối giá bán, chi phí tiệm và khả năng mua của người làm công"/>
 <svg width={1920} height={1080} style={{position:'absolute',inset:0}}>
  <path d="M620 452L1275 452M1340 550L1074 716M564 550L828 716" stroke={P.rule} strokeWidth={4} fill="none"/>
  {focus.map((a,i)=><g key={a.name} opacity={progress(f,a.at,20)}>
   <circle cx={a.x} cy={a.y} r={91} fill={P.white} stroke={a.color} strokeWidth={4}/>
   {i===0?<><path d={`M${a.x-47} ${a.y+30}V${a.y-32}H${a.x+47}V${a.y+30}Z`} fill="none" stroke={a.color} strokeWidth={3}/><path d={`M${a.x-31} ${a.y+13}L${a.x-7} ${a.y-3}L${a.x+12} ${a.y-3}L${a.x+32} ${a.y-18}`} fill="none" stroke={a.color} strokeWidth={6}/></>:i===1?<><rect x={a.x-36} y={a.y-47} width={72} height={95} fill={P.paper} stroke={a.color} strokeWidth={3}/>{[0,1,2,3].map(n=><line key={n} x1={a.x-23} x2={a.x+22} y1={a.y-24+n*17} y2={a.y-24+n*17} stroke={a.color} strokeWidth={3}/>)}</>:<><rect x={a.x-51} y={a.y-29} width={102} height={64} rx={6} fill={a.color}/><circle cx={a.x} cy={a.y+3} r={21} fill="none" stroke={P.white} strokeWidth={3}/></>}
   <text x={a.x} y={a.y-125} textAnchor="middle" fill={a.color} fontSize={27} fontWeight={700}>{a.name}</text>
   <text x={a.x} y={a.y+142} textAnchor="middle" fill={P.ink} fontSize={31} fontWeight={700}>{a.sub}</text>
   <text x={a.x} y={a.y+187} textAnchor="middle" fill={P.quiet} fontSize={25}>{a.detail}</text>
  </g>)}
  {Array.from({length:12},(_,i)=>{
   const side=i%3;const t=((f+i*13)%120)/120;const a=focus[side];const b=focus[(side+1)%3];return <circle key={i} cx={a.x+(b.x-a.x)*t} cy={a.y+(b.y-a.y)*t} r={6} fill={a.color} opacity={f>connect?.7:0}/>;
  })}
  <g opacity={progress(f,connect,18)}><Bread x={880} y={469} width={153}/><Arrow x1={955} y1={576} x2={955} y2={669} color={P.green}/></g>
 </svg><Footer>Hãy kiểm tốc độ hay mức giá, mốc so sánh, tổng chi phí và thu nhập thực tế trước khi kết luận ai đang được lợi.</Footer></>;
};
