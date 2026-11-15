import React from 'react';
import {useCurrentFrame} from 'remotion';
import type {Ctx,PacedPlan} from './types';
import {Background,K,T,p} from './art';
import {Budget,Buffer,Daily,Dinner,Disclaimer,Essentials,Hook,Repair} from './money-scenes';
import {Annual,Audit,Automate,Calendar,EndPlan,Purchase,Recurring,Reimburse,Review,Subscribe} from './decisions';
export type {PacedPlan} from './types';

/** Fresh shot direction: no persistent title/card/stage frame. Each shot has a
 * finite concrete action and an immediate follow-through; speech remains at1x.
 * Scene art is code-native, not generated footage or verified lipsynchronization.
 */
const pick=(c:Ctx):React.FC<Ctx>=>{
 const act=String(c.b.data?.action||'');
 if(c.b.kind==='subscribe'||c.s.stage==='outro')return Subscribe;
 if(act==='match_reimbursement')return Reimburse;
 if(['repair_vs_treat','use_and_replenish_buffer'].includes(act))return Repair;
 if(['total_purchase_cost','discount_vs_need','pause_purchase','useful_vs_unused','income_expense_gap'].includes(act))return Purchase;
 if(act==='installments_on_calendar'||act==='walk_calendar_balance'||act==='monthly_vs_timing'||act==='bridge_due_date_gap')return Calendar;
 if(act==='one_change'||act==='keep_or_reduce')return Recurring;
 if(act==='select_one_receipt')return Audit;
 if(act==='same_total_different_jobs')return Review;
 const map:Record<string,React.FC<Ctx>>={hook:Hook,disclaimer:Disclaimer,budget_before:Budget,budget_after:Budget,daily:Daily,dinner:Dinner,essentials:Essentials,audit:Audit,recurring:Recurring,annual:Annual,calendar:Calendar,buffer:Buffer,choice:Purchase,automate:Automate,review:Review,cta:EndPlan,subscribe:Subscribe};
 return map[c.b.kind]||Review;
};

export const ComicPacedFilm:React.FC<{plan:PacedPlan}>=({plan})=>{
 const frame=useCurrentFrame();let i=plan.shots.findIndex(s=>frame>=s.from&&frame<s.from+s.duration);if(i<0)i=Math.max(0,plan.shots.length-1);
 const s=plan.shots[i];if(!s)return <svg width={1920} height={1080}><rect width={1920} height={1080} fill={K.cream}/></svg>;
 const b=plan.segments.find(v=>v.id===s.beatId);if(!b)return <svg width={1920} height={1080}><Background/></svg>;
 const f=frame-s.from,d=Math.max(1,s.duration),t=Math.min(1,f/Math.max(1,d-1));
 const c:Ctx={plan,b,s,f,d,i,t},Scene=pick(c);
 // Six frames: paper-edge match cut; the cut never holds the previous scene.
 const entering=1-p(f,0,6),outro=b.kind==='subscribe';
 return <svg width={1920} height={1080} viewBox="0 0 1920 1080" style={{fontFamily:'Arial, sans-serif',fontVariantNumeric:'tabular-nums',background:K.cream}}>
  <defs><clipPath id="pace-comic-picture"><rect width={1920} height={950}/></clipPath><pattern id="pace-comic-ink" width={24} height={24} patternUnits="userSpaceOnUse"><circle cx={4} cy={4} r={1} fill={K.ink}/></pattern></defs>
  <g clipPath="url(#pace-comic-picture)"><Scene {...c}/><rect width={1920} height={950} fill="url(#pace-comic-ink)" opacity={.035}/>
   {entering>0&&i>0&&<g transform={`translate(${(1-entering)*2040} 0)`}><path d="M0 0H1920V950H0Z" fill={i%2?K.purple:K.green}/><path d="M0 0V950" stroke={K.yellow} strokeWidth={16}/></g>}
  </g>
  {!outro&&<g transform="translate(1660 38)"><rect x={-168} y={-24} width={336} height={48} rx={10} fill={K.white} opacity={.84}/><T x={0} y={8} size={21} weight={600} fill={K.muted}>SỐ LIỆU MINH HỌA</T></g>}
  <rect x={0} y={950} width={1920} height={130} fill={K.ink}/>
 </svg>;
};
