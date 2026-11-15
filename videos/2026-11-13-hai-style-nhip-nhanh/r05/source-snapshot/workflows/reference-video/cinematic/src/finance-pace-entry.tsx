import React from 'react';
import {AbsoluteFill,Composition,Sequence,registerRoot,useCurrentFrame} from 'remotion';
import {ComicPacedFilm} from './finance-pace-comic';
import {FlowPacedFilm} from './finance-pace-flow';

type Props={plan:React.ComponentProps<typeof ComicPacedFilm>['plan'];fromFrame?:number;frames?:number};
const empty:Props={plan:{fps:30,durationFrames:18000,segments:[],shots:[],captions:[],words:[]}};
const Captions:React.FC<Props>=({plan,fromFrame=0})=>{
 const f=useCurrentFrame()+fromFrame,c=plan.captions.find(v=>f>=v.from&&f<v.end);
 return c?<div style={{position:'absolute',bottom:29,left:145,right:145,textAlign:'center',font:'500 36px/1.3 Arial',color:'#fff',pointerEvents:'none'}}><span style={{display:'inline-block',maxWidth:1590,background:'#242330ed',padding:'10px 25px',borderRadius:10}}>{c.text}</span></div>:null;
};
const Comic:React.FC<Props>=props=><AbsoluteFill><Sequence from={-(props.fromFrame??0)} durationInFrames={props.plan.durationFrames}><ComicPacedFilm plan={props.plan}/></Sequence><Captions {...props}/></AbsoluteFill>;
const Flow:React.FC<Props>=props=><AbsoluteFill><Sequence from={-(props.fromFrame??0)} durationInFrames={props.plan.durationFrames}><FlowPacedFilm plan={props.plan}/></Sequence><Captions {...props}/></AbsoluteFill>;
const Root:React.FC=()=> <>
 <Composition id="FinancePacedComic" component={Comic} defaultProps={empty} width={1920} height={1080} fps={30} durationInFrames={18000} calculateMetadata={({props})=>({durationInFrames:props.frames??props.plan.durationFrames})}/>
 <Composition id="FinancePacedFlow" component={Flow} defaultProps={empty} width={1920} height={1080} fps={30} durationInFrames={18000} calculateMetadata={({props})=>({durationInFrames:props.frames??props.plan.durationFrames})}/>
</>;
registerRoot(Root);
