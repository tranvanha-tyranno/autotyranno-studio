import React from 'react';
import {AbsoluteFill,Composition,Sequence,registerRoot,useCurrentFrame} from 'remotion';
import {FlowFilm} from './finance-flow/FlowFilm';
import {ComicProof} from './finance-comic/ComicProof';
import {CandidateSheet} from './finance-cast-v2/CandidateSheet';
import type {FinancePlan} from './finance-demo/types';
type Props={plan:FinancePlan;fromFrame:number;frames:number};
const empty:Props={plan:{durationFrames:2333,segments:[]},fromFrame:890,frames:535};
const Captions:React.FC<Props>=({plan,fromFrame})=>{
 const f=useCurrentFrame()+fromFrame,c=plan.captions?.find(c=>f>=c.from&&f<c.end);
 return c?<div style={{position:'absolute',bottom:35,left:160,right:160,textAlign:'center',font:'600 35px/1.25 Arial',color:'#fff'}}><span style={{display:'inline-block',background:'#252630ed',padding:'11px 26px',borderRadius:10}}>{c.text}</span></div>:null;
};
const Flow:React.FC<Props>=props=><AbsoluteFill><Sequence from={-props.fromFrame} durationInFrames={props.plan.durationFrames}><FlowFilm plan={props.plan}/></Sequence><Captions {...props}/></AbsoluteFill>;
const Comic:React.FC<Props>=props=><AbsoluteFill><Sequence from={-props.fromFrame} durationInFrames={props.plan.durationFrames}><ComicProof plan={props.plan}/></Sequence><Captions {...props}/></AbsoluteFill>;
const Root:React.FC=()=> <>
 <Composition id="FinanceFlowProof" component={Flow} defaultProps={empty} durationInFrames={535} width={1920} height={1080} fps={30} calculateMetadata={({props})=>({durationInFrames:props.frames})}/>
 <Composition id="FinanceComicProof" component={Comic} defaultProps={empty} durationInFrames={535} width={1920} height={1080} fps={30} calculateMetadata={({props})=>({durationInFrames:props.frames})}/>
 <Composition id="FinanceComicSheet" component={CandidateSheet} durationInFrames={1} width={1920} height={1080} fps={30}/>
 </>;
registerRoot(Root);
