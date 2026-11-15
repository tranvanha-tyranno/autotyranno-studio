import React from 'react';
import {AbsoluteFill,Composition,registerRoot,useCurrentFrame} from 'remotion';
import {CastFilm} from './finance-demo/CastFilm';
import {Minimal} from './finance-simple/Minimal';
import {CastSheet,CastMotion} from './finance-cast/CastSheet';
import type {FinancePlan} from './finance-demo/types';
const empty:FinancePlan={durationFrames:30,segments:[],captions:[]};
const Film:React.FC<{plan:FinancePlan;style:'cast'|'minimal'}>=({plan,style})=>{
 const f=useCurrentFrame();const cap=plan.captions?.find(c=>f>=c.from&&f<c.end);
 return <AbsoluteFill>{style==='cast'?<CastFilm plan={plan}/>:<Minimal plan={plan}/>}{cap&&<div style={{position:'absolute',left:160,right:160,bottom:38,textAlign:'center',fontFamily:'Arial',fontSize:35,fontWeight:600,color:'#fff',lineHeight:1.3}}><span style={{display:'inline-block',padding:'12px 28px',borderRadius:12,background:'#20342fF2'}}>{cap.text}</span></div>}</AbsoluteFill>
};
const Root:React.FC=()=> <>
 <Composition id="FinanceCast" component={Film} width={1920} height={1080} fps={30} durationInFrames={30} defaultProps={{plan:empty,style:'cast' as const}} calculateMetadata={({props})=>({durationInFrames:props.plan.durationFrames})}/>
 <Composition id="FinanceMinimal" component={Film} width={1920} height={1080} fps={30} durationInFrames={30} defaultProps={{plan:empty,style:'minimal' as const}} calculateMetadata={({props})=>({durationInFrames:props.plan.durationFrames})}/>
 <Composition id="FinanceCastSheet" component={CastSheet} width={1920} height={1080} fps={30} durationInFrames={1}/>
 <Composition id="FinanceCastMotion" component={CastMotion} width={1920} height={1080} fps={30} durationInFrames={360}/>
 </>;
registerRoot(Root);
