import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Arrow,cue,Footer,LabHeading,number,P,progress,Tag} from './common';
import type {BreadLabShot} from './types';

export const PriceLevel: React.FC<{shot:BreadLabShot}> = ({shot}) => {
 const f=useCurrentFrame();const first=cue(shot,0,.12);const second=cue(shot,1,.43);const third=cue(shot,2,.76);
 const p=progress(f,first,Math.min(44,shot.duration*.2));const q=progress(f,second,Math.min(44,shot.duration*.2));
 const pts=[{x:300,y:785,v:20000},{x:938,y:419,v:22000},{x:1580,y:338,v:22440}];
 return <><LabHeading shot={shot} title="Tăng chậm hơn vẫn đi lên" subtitle="Cùng chiếc bánh · Cùng lượng và chất lượng · Đơn vị: đồng"/>
 <svg width={1920} height={1080} style={{position:'absolute',inset:0}}>
  {[20000,21000,22000].map(v=><g key={v}><line x1={260} x2={1710} y1={785-(v-20000)*.183} y2={785-(v-20000)*.183} stroke={P.rule} strokeDasharray="5 9"/><Tag x={97} y={795-(v-20000)*.183} color={P.quiet} size={25}>{number(v)}</Tag></g>)}
  <line x1={260} x2={1710} y1={829} y2={829} stroke={P.ink} strokeWidth={2}/>
  <path d={`M300,785L${300+638*p},${785-366*p}`} fill="none" stroke={P.gold} strokeWidth={8}/>
  <path d={`M938,419L${938+642*q},${419-81*q}`} fill="none" stroke={P.green} strokeWidth={8} opacity={f>=second?1:0}/>
  {pts.map((pt,i)=><g key={i} opacity={i===0?1:i===1?p:q}><circle cx={pt.x} cy={pt.y} r={10} fill={i===2?P.green:P.gold}/><text x={pt.x} y={pt.y-31} textAnchor="middle" fontSize={52} fontWeight={700} fill={P.ink}>{number(pt.v)}</text><text x={pt.x} y={877} textAnchor="middle" fontSize={28} fill={P.quiet}>{['Ban đầu','Kỳ 1','Kỳ 2'][i]}</text></g>)}
  <g opacity={p}><text x={560} y={545} fill={P.gold} fontSize={61} fontWeight={700}>+10%</text></g>
  <g opacity={q}><text x={1240} y={520} fill={P.green} fontSize={61} fontWeight={700}>+2%</text><Arrow x1={1614} y1={767} x2={1614} y2={372} color={P.rust}/><Tag x={1645} y={600} color={P.rust} size={26}>Vẫn cao hơn</Tag></g>
  <g opacity={progress(f,third,9)}><line x1={501} x2={1400} y1={930} y2={930} stroke={P.rule}/><text x={950} y={930} dy={-12} textAnchor="middle" fill={P.ink} fontSize={30} fontWeight={600}>Tốc độ hạ xuống ≠ mặt bằng giá hạ xuống</text></g>
 </svg><Footer>Một mặt hàng chỉ minh họa phép tính; không đại diện mức lạm phát hay CPI cả nước.</Footer></>;
};
