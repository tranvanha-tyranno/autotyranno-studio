import React from 'react';
import {AbsoluteFill,Composition,registerRoot,useCurrentFrame} from 'remotion';
import {ComicLongFilm} from './finance-long-comic';
import {FlowLongFilm} from './finance-long-flow';

type Segment={id:string;from:number;duration:number;text:string;kind:string;headline:string;cueFrame:number;data?:Record<string,unknown>;chapterId?:string;chapterTitle?:string};
type Plan={fps:30;durationFrames:number;segments:Segment[];captions:{from:number;end:number;text:string}[]};
type Props={plan:Plan};
const empty:Props={plan:{fps:30,durationFrames:18000,segments:[],captions:[]}};
const Captions:React.FC<Props>=({plan})=>{
 const f=useCurrentFrame();const c=plan.captions.find(v=>f>=v.from&&f<v.end);
 return c?<div style={{position:'absolute',bottom:29,left:145,right:145,textAlign:'center',font:'500 36px/1.3 Arial',color:'#fff',pointerEvents:'none'}}><span style={{display:'inline-block',maxWidth:1590,background:'#242330ed',padding:'10px 25px',borderRadius:10}}>{c.text}</span></div>:null;
};
const Comic:React.FC<Props>=({plan})=><AbsoluteFill><ComicLongFilm plan={plan}/><Captions plan={plan}/></AbsoluteFill>;
const Flow:React.FC<Props>=({plan})=><AbsoluteFill><FlowLongFilm plan={plan}/><Captions plan={plan}/></AbsoluteFill>;
const Root:React.FC=()=> <>
 <Composition id="FinanceLongComic" component={Comic} defaultProps={empty} width={1920} height={1080} fps={30} durationInFrames={18000} calculateMetadata={({props})=>({durationInFrames:props.plan.durationFrames})}/>
 <Composition id="FinanceLongFlow" component={Flow} defaultProps={empty} width={1920} height={1080} fps={30} durationInFrames={18000} calculateMetadata={({props})=>({durationInFrames:props.plan.durationFrames})}/>
</>;
registerRoot(Root);
