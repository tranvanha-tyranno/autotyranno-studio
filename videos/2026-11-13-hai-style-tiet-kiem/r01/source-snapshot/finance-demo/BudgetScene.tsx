import React from 'react';
import {Character} from '../finance-cast/Character';
import {Stage,Label,Jar,Money,Arrow,rise,ink,coral,green} from './Stage';
export const BudgetScene:React.FC<{visual:string;f:number;speaking:boolean}>=({visual,f,speaking})=>{
 const after=visual==='after',salary=after?'14':'12',cost=after?'12':'10';
 const p=rise(f,25,55);
 return <Stage title={after?'Lương lên. Chi tiêu cũng lên.':'Một tháng trước khi tăng lương'}>
   <Character id={1} x={300} y={885} scale={1.15} frame={f} emotion={after?'worried':'happy'} pose={after?'shrug':'talk'} speaking={speaking}/>
   <Label x={300} y={936} size={26} anchor="middle">MINH</Label>
   <g transform={`translate(680 ${370+(1-rise(f))*35})`} opacity={rise(f)}>
     <Label x={0} y={-60} size={27}>THU NHẬP / THÁNG</Label><Label x={0} y={40} size={110} color={green}>{salary} triệu</Label>
     <Money x={160} y={150} value={salary+'tr'} scale={1.25}/>
   </g>
   <Arrow x1={1000} y1={390} x2={1190} y2={390}/>
   <Label x={1430} y={310} size={27} anchor="middle">CHI TIÊU / THÁNG</Label>
   <Label x={1430} y={410} size={100} color={coral} anchor="middle">{cost} triệu</Label>
   <g opacity={p}><path d="M900 610 Q1120 710 1260 650" fill="none" stroke={green} strokeWidth={5} strokeDasharray="12 10"/>
   <Jar x={1430} y={700} value="2 triệu" level={.35}/></g>
   {after&&<g opacity={rise(f,110)}><rect x={640} y={600} width={510} height={150} rx={22} fill="#f1dbbd"/><Label x={895} y={661} size={31} anchor="middle">TĂNG THU 2 TRIỆU</Label><Label x={895} y={709} size={31} color={coral} anchor="middle">= TĂNG CHI 2 TRIỆU</Label></g>}
 </Stage>;
};
