import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Arrow,Bread,cue,FlourBag,Footer,LabHeading,P,progress,Tag} from './common';
import type {BreadLabShot} from './types';

export const Inventory:React.FC<{shot:BreadLabShot}> = ({shot})=>{
 const f=useCurrentFrame();const consume=cue(shot,0,.1);const arrives=cue(shot,1,.35);const replace=shot.duration+1;const finish=cue(shot,3,.86);
 const useSpan=Math.max(1,replace-consume);const newSpan=Math.max(1,shot.duration-replace-12);
 return <><LabHeading shot={shot} title="Hóa đơn mới chưa đổi ngay mẻ đang làm" subtitle="Theo dấu lô bột đang được dùng, thay vì chỉ nhìn giá của lô vừa mua"/>
 <svg width={1920} height={1080} style={{position:'absolute',inset:0}}>
  <Tag x={126} y={290} color={P.rust} size={34}>Lô đã mua · giá vốn cũ</Tag>
  <Tag x={1242} y={290} color={P.green} size={34}>Lô mua mới · giá thấp hơn</Tag>
  <path d="M120 540H625M120 556H625M1220 540H1775M1220 556H1775" stroke={P.gray} strokeWidth={4}/>
  {Array.from({length:4},(_,i)=>{
   const x=146+i*110;const p=progress(f,consume+i*useSpan/5,Math.max(12,useSpan/3));
   return <FlourBag key={'old'+i} x={x+(850-x)*p} y={437+(672-437)*p-Math.sin(Math.PI*p)*95} width={83} color="#d9ba8d" opacity={p<.97?1:1-progress(f,consume+i*useSpan/5+useSpan/3-4,8)} label="CŨ"/>;
  })}
  {Array.from({length:4},(_,i)=>{
   const x=1250+i*125;const a=progress(f,arrives+i*4,25);const p=progress(f,replace+i*newSpan/5,Math.max(12,newSpan/3));
   return <FlourBag key={'new'+i} x={x+(850-x)*p} y={437+(672-437)*p-Math.sin(Math.PI*p)*85-(1-a)*110} width={83} color="#b5c9ab" opacity={a*(1-progress(f,replace+i*newSpan/5+newSpan/3-4,8))} label="MỚI"/>;
  })}
  <Arrow x1={586} y1={581} x2={802} y2={720} color={P.rust}/>
  <Arrow x1={1265} y1={583} x2={1022} y2={720} color={P.green} opacity={progress(f,replace,12)}/>
  <path d="M780 754H1040Q1019 905 910 905Q801 905 780 754Z" fill={P.white} stroke={P.ink} strokeWidth={4}/>
  <ellipse cx={910} cy={754} rx={130} ry={21} fill="#ddd5bc" stroke={P.ink} strokeWidth={3}/>
  <Tag x={799} y={953} color={P.quiet} size={29}>Mẻ bánh đang làm</Tag>
  {Array.from({length:15},(_,i)=>{
   const start=consume+i*(shot.duration-consume)/16;const t=progress(f,start,30);return <circle key={i} cx={865+(i%4)*25} cy={671+t*78} r={3} fill={P.white} opacity={t>0&&t<1?.9:0}/>;
  })}
  <g opacity={progress(f,arrives,12)}><Tag x={1281} y={630} color={P.green} size={29}>Giá mua mới đã giảm</Tag><Tag x={1281} y={675} color={P.quiet} size={25}>Lô mới chờ mẻ sau</Tag></g>
  <g opacity={progress(f,finish,8)}><Bread x={1100} y={820} width={145}/><Tag x={1275} y={864} color={P.ink} size={30}>Độ trễ có thể tồn tại</Tag></g>
 </svg><Footer>Minh họa một khả năng dùng hàng tồn; không phải mọi tiệm đều có cùng tồn kho hay cùng phương pháp tính giá vốn.</Footer></>;
};
