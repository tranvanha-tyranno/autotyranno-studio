import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Arrow,Bread,cue,Footer,LabHeading,P,progress,Tag} from './common';
import type {BreadLabShot} from './types';

const Shop:React.FC<{x:number;color:string;title:string;subtitle:string}> = ({x,color,title,subtitle})=><g>
 <rect x={x} y={372} width={400} height={290} rx={4} fill={P.white} stroke={P.ink} strokeWidth={3}/><path d={`M${x-20} 372L${x+30} 304H${x+370}L${x+420} 372Z`} fill={color}/><line x1={x} x2={x+400} y1={568} y2={568} stroke={P.rule} strokeWidth={3}/><Bread x={x+130} y={447} width={145}/><text x={x+200} y={417} fontSize={30} fontWeight={700} fill={P.ink} textAnchor="middle">{title}</text><text x={x+200} y={714} fontSize={28} fill={P.ink} textAnchor="middle">{subtitle}</text>
</g>;

export const Competition:React.FC<{shot:BreadLabShot}>=({shot})=>{
 const f=useCurrentFrame();const alternative=cue(shot,0,.13);const switchAt=cue(shot,1,.36);const pressure=cue(shot,2,.7);
 const weak=shot.data?.stage==='weak_alternative'||f>=pressure;
 return <><LabHeading shot={shot} title="Giá bán còn chịu sức ép từ lựa chọn của khách" subtitle="Hai chiếc bánh tương đương; các điểm chuyển động biểu diễn lượt chọn mua, không phải số khách đo được"/>
 <svg width={1920} height={1080} style={{position:'absolute',inset:0}}>
  <Shop x={240} color={P.gold} title="Tiệm đang xét" subtitle="Giữ giá"/>
  <g opacity={progress(f,alternative,20)}><Shop x={1240} color={P.green} title="Lựa chọn thay thế" subtitle={weak?'Khó đến · không tiện mua':'Tương đương · rẻ hơn · dễ mua'}/></g>
  <line x1={795} y1={910} x2={435} y2={757} stroke={P.gray} strokeWidth={12} strokeLinecap="round"/>
  <path d="M795 910Q1208 941 1440 756" fill="none" stroke={P.green} strokeWidth={10} strokeDasharray={weak?'14 18':undefined} opacity={progress(f,switchAt,24)*(weak?.35:1)}/>
  {Array.from({length:12},(_,i)=>{
   const life=(f+i*17)%132;const t=life/132;const chooseAlt=!weak&&f>=switchAt&&i%4!==0;
   const x=chooseAlt?795+645*t:795-360*t;const y=chooseAlt?910-154*t+65*Math.sin(t*Math.PI):910-153*t;
   return <g key={i} opacity={f>i*2?1:0}><circle cx={x} cy={y} r={13} fill={chooseAlt?P.green:P.gold}/><circle cx={x} cy={y} r={5} fill={P.white}/></g>;
  })}
  <Tag x={710} y={962} color={P.quiet} size={26}>Quyết định mua của khách</Tag>
  <g opacity={progress(f,switchAt,12)}><Arrow x1={1180} y1={484} x2={706} y2={484} color={weak?P.gray:P.rust} dashed={weak}/><text x={950} y={411} textAnchor="middle" fontSize={30} fontWeight={700} fill={weak?P.quiet:P.rust}>{weak?'Sức ép yếu hơn':'Nguy cơ mất khách'}</text><text x={950} y={544} textAnchor="middle" fontSize={25} fill={P.quiet}>Không chỉ là cộng chi phí</text></g>
 </svg><Footer>Luồng chấm là cơ chế định tính, không phải dự báo lượng khách hay thị phần. Chất lượng, khoảng cách và độ tiện mua phải tương đương khi so giá.</Footer></>;
};
