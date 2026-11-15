import React from 'react';
import {AbsoluteFill,useCurrentFrame} from 'remotion';
import {C,type Context,type PacedPlan,q} from './types';
import {Scene} from './scenes';
import {T} from './art';
export type {PacedPlan,PaceShot,PaceSegment} from './types';

/** Sentence-scale physical shots. No title rail, scene card or footer frame.
 * The supplied cut list and exact take determine every state and transition. */
export const FlowPacedFilm:React.FC<{plan:PacedPlan}>=({plan})=>{
 const frame=useCurrentFrame();
 const shot=plan.shots.find(s=>frame>=s.from&&frame<s.from+s.duration)??plan.shots[plan.shots.length-1];
 const s=plan.segments.find(s=>s.id===shot?.beatId);
 if(!s||!shot)return <AbsoluteFill style={{background:C.paper}}/>;
 const local=frame-shot.from,u=q(local,0,Math.max(1,shot.duration-3));
 const c:Context={plan,s,shot,f:local,beatFrame:frame-s.from,u};
 const dark=['buffer','automate','subscribe'].includes(s.kind),bg=dark?'#DDE9DF':s.kind==='dinner'?'#F3DCD0':s.kind==='calendar'?'#E7ECDF':C.paper;
 const wipe=q(local,0,6);
 return <AbsoluteFill style={{background:bg,fontFamily:'Arial, sans-serif',fontVariantNumeric:'tabular-nums'}}>
   <svg width={1920} height={950} viewBox="0 0 1920 950" style={{overflow:'hidden'}}>
    <defs><clipPath id="pace-content"><rect width={1920} height={945}/></clipPath></defs>
    <g clipPath="url(#pace-content)"><Scene {...c}/></g>
    {s.kind!=='subscribe'&&s.kind!=='disclaimer'&&<g opacity={.85}><rect x={1620} y={20} width={256} height={42} rx={18} fill={C.white}/><T x={1748} y={48} size={19} color={C.muted}>SỐ LIỆU MINH HỌA</T></g>}
    {frame>0&&wipe<1&&<g><rect x={1920*wipe} width={1920*(1-wipe)} height={950} fill={bg}/><path d={`M${1920*wipe} 0V950`} stroke={C.green} strokeWidth={14}/></g>}
   </svg>
 </AbsoluteFill>;
};
