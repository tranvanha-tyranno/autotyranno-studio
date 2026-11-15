import React from 'react';
import {AbsoluteFill,useCurrentFrame} from 'remotion';
import {Character} from '../finance-cast/Character';
import type {FinancePlan} from './types';
import {Stage,Label,Money,Arrow,rise,green,coral} from './Stage';
import {BudgetScene} from './BudgetScene';
import {DailyScene} from './DailyScene';
import {DecisionScene} from './DecisionScene';
export const CastFilm:React.FC<{plan:FinancePlan}>=({plan})=>{
 const frame=useCurrentFrame();
 const s=plan.segments.find(s=>frame>=s.from&&frame<s.from+s.duration)??plan.segments[plan.segments.length-1];
 if(!s)return null;
 const f=frame-s.from; const speaking=Boolean(plan.words?.some(w=>frame/30>=w.start&&frame/30<w.end));
 const v=s.visual;
 if(v==='disclaimer')return <AbsoluteFill style={{background:'#23372f',color:'#fff6df',justifyContent:'center',padding:'0 240px',fontFamily:'Arial'}}><div style={{fontSize:27,letterSpacing:4,color:'#efc453',marginBottom:35}}>MIỄN TRỪ TRÁCH NHIỆM</div><div style={{fontSize:65,fontWeight:700,lineHeight:1.25}}>Tình huống giả định.<br/>Số tiền để minh họa.</div><div style={{fontSize:36,marginTop:45,lineHeight:1.5}}>Nội dung giáo dục về ngân sách.<br/>Không phải tư vấn tài chính cá nhân.</div></AbsoluteFill>;
 if(v==='before'||v==='after')return <BudgetScene visual={v} f={f} speaking={speaking}/>;
 if(v==='daily'||v==='dinner')return <DailyScene visual={v} f={f} speaking={speaking}/>;
 if(v==='choice'||v==='transfer'||v==='cta')return <DecisionScene visual={v} f={f} speaking={speaking}/>;
 return <Stage title="Lương tăng. Sao tiền dư không tăng?">
 <Character id={1} x={380} y={885} scale={1.25} frame={f} emotion={f<65?'happy':'surprised'} pose={f<65?'celebrate':'shrug'} speaking={speaking}/>
 <Character id={2} x={1530} y={885} scale={1.25} frame={f} emotion="thinking" pose="point" flip/>
 <g opacity={rise(f)}><Label x={960} y={340} size={33} anchor="middle">TĂNG LƯƠNG</Label><Label x={960} y={445} size={104} color={green} anchor="middle">+2 triệu</Label><Money x={960} y={550} value="+2tr" scale={1.3}/></g>
 <g opacity={rise(f,65)}><Arrow x1={960} y1={625} x2={960} y2={690} color={coral}/><Label x={960} y={775} size={55} color={coral} anchor="middle">TIỀN DƯ: KHÔNG TĂNG</Label><Label x={960} y={835} size={30} anchor="middle">Niềm vui tăng lương đi đâu mất?</Label></g>
 </Stage>;
};
