import React from 'react';
import {Character} from '../finance-cast/Character';
import {Stage,Label,rise,ink,coral,gold} from './Stage';
export const DailyScene:React.FC<{visual:string;f:number;speaking:boolean}>=({visual,f,speaking})=>{
 const dinner=visual==='dinner';const filled=Math.floor(rise(f,45,90)*30);
 return <Stage title={dinner?'Thêm một bữa ăn, vừa hết phần tăng':'“Mình có mua gì lớn đâu?”'}>
 <Character id={1} x={260} y={885} scale={1.05} emotion={dinner?'surprised':'thinking'} pose={dinner?'shrug':'talk'} frame={f} speaking={!dinner&&speaking}/>
 <Character id={2} x={1680} y={885} scale={1.05} emotion="confident" pose="point" flip frame={f} speaking={dinner&&speaking}/>
 {!dinner?<g><Label x={960} y={300} size={36} anchor="middle">MỖI NGÀY CHI THÊM 60.000₫</Label>
 {Array.from({length:30},(_,i)=><g key={i} transform={`translate(${590+(i%6)*130} ${355+Math.floor(i/6)*74})`}><rect width={110} height={58} rx={12} fill={i<filled?gold:'#e4dfd0'} stroke={ink} strokeWidth={2}/><Label x={55} y={39} size={25} anchor="middle">{i<filled?'60k':String(i+1).padStart(2,'0')}</Label></g>)}
 <g opacity={rise(f,100,30)}><Label x={960} y={800} size={59} color={coral} anchor="middle">60.000 × 30 = 1.800.000₫</Label></g></g>:
 <g><g opacity={rise(f)}><rect x={620} y={300} width={680} height={235} rx={20} fill="#fffaf0" stroke={ink} strokeWidth={4}/><path d="M655 337H1265" stroke="#ded4c1" strokeWidth={2}/><Label x={680} y={405} size={36}>Chi thêm mỗi ngày</Label><Label x={1230} y={405} size={42} color={coral} anchor="end">1,8 triệu</Label><Label x={680} y={485} size={36}>+ Một bữa ăn</Label><Label x={1230} y={485} size={42} color={coral} anchor="end">0,2 triệu</Label></g>
 <g opacity={rise(f,35)}><path d="M670 580H1250" stroke={ink} strokeWidth={5}/><Label x={960} y={685} size={88} color={coral} anchor="middle">= 2 triệu</Label><Label x={960} y={761} size={33} anchor="middle">VỪA HẾT PHẦN TĂNG LƯƠNG</Label></g></g>}
 </Stage>;
};
