import React,{useEffect,useState} from 'react';
import {Audio,Video} from '@remotion/media';
import {AbsoluteFill,cancelRender,continueRender,delayRender,interpolate,Sequence,staticFile,useCurrentFrame} from 'remotion';
import {BasketScope} from './BasketScope';
import {BreadPower} from './BreadPower';
import {Competition} from './Competition';
import {CostLedger} from './CostLedger';
import {Inventory} from './Inventory';
import {MoneySplit} from './MoneySplit';
import {PriceLevel} from './PriceLevel';
import {Synthesis} from './Synthesis';
import {clamp,font,P} from './common';
import type {BreadLabPlan,BreadLabProps,BreadLabShot} from './types';
import './fonts.css';
export type {BreadLabPlan,BreadLabProps,BreadLabShot,BreadSimulation} from './types';

const LocalFonts:React.FC=()=>{
 const [handle]=useState(()=>delayRender('Load local BreadLab Vietnamese fonts'));
 useEffect(()=>{Promise.all([400,600,700].map(w=>document.fonts.load(`${w} 30px "Bread Lab Vietnam"`,'Tiếng Việt Ắ ầ ệ Ữ ỹ'))).then(()=>document.fonts.ready).then(()=>continueRender(handle)).catch(cancelRender);},[handle]);return null;
};
export const validateBreadLabPlan=(plan:BreadLabPlan)=>{
 if(plan.fps!==30||!Number.isInteger(plan.durationFrames)||plan.durationFrames<1)throw new Error('BreadLab requires30fps and positive integer duration.');
 let expected=0;const ids=new Set<string>();
 for(const s of plan.shots){
  if(ids.has(s.id))throw new Error(`Duplicate BreadLab shot ${s.id}`);ids.add(s.id);
  if(s.from!==expected||!Number.isInteger(s.duration)||s.duration<16)throw new Error(`Invalid BreadLab timeline at ${s.id};expected from${expected}.`);
  if(!s.simulation&&!s.file)throw new Error(`Video interlude${s.id}needs actualfile.`);
  if(!Number.isFinite(s.sourceStartSeconds)||s.sourceStartSeconds<0)throw new Error(`Invalid sourceStartSeconds${s.id}`);
  if(s.cueFrames?.some((n,i,a)=>!Number.isInteger(n)||n<0||n>=s.duration||(i>0&&n<=a[i-1])))throw new Error(`Invalid exact local cues${s.id}`);
  expected+=s.duration;
 }
 if(plan.shots.length&&expected!==plan.durationFrames)throw new Error(`BreadLab timeline covers${expected},expected${plan.durationFrames}`);
};

const Interlude:React.FC<{shot:BreadLabShot;fps:number;chapterStart:boolean;chapterIndex:number}>=({shot,fps,chapterStart,chapterIndex})=>{
 const f=useCurrentFrame();const items=shot.overlay?.items?.slice(0,3)??[];
 const title=shot.overlay?.title??shot.headline;
 const end=Math.min(shot.duration-1,135);const enter=shot.cueFrames?.[0]??8;
 const visible=end>enter+12?interpolate(f,[enter,enter+6,end-6,end],[0,1,1,0],clamp):0;
 return <AbsoluteFill>
  <Video src={staticFile(shot.file!)} trimBefore={Math.round(shot.sourceStartSeconds*fps)} muted objectFit="cover" style={{position:'absolute',inset:0,width:'100%',height:'100%'}}/>
  {(title||shot.emphasis||items.length>0||chapterStart)&&<AbsoluteFill style={{background:'linear-gradient(180deg,rgba(0,0,0,.5),transparent 38%,transparent 47%,rgba(0,0,0,.8))'}}/>}
  {chapterStart&&f<105&&<div style={{position:'absolute',top:58,left:100,right:110,color:'#fffaf0',opacity:interpolate(f,[0,7,94,104],[0,1,1,0],clamp)}}><div style={{fontSize:20,letterSpacing:3,color:'#edc98e',marginBottom:12}}>PHẦN {chapterIndex+1}</div><div style={{fontSize:43,fontWeight:600,lineHeight:1.2}}>{shot.chapterTitle}</div></div>}
  <div style={{position:'absolute',left:100,right:130,bottom:105,color:'#fffaf0',opacity:visible,textShadow:'0 2px 18px rgba(0,0,0,.6)'}}>
   {shot.overlay?.kicker&&<div style={{fontSize:20,color:'#edc98e',letterSpacing:1.7,marginBottom:16}}>{shot.overlay.kicker}</div>}
   {shot.emphasis&&<div style={{fontSize:shot.emphasis.length>28?65:91,fontWeight:700,lineHeight:1.15,marginBottom:20}}>{shot.emphasis}</div>}
   {title&&<div style={{fontSize:items.length>0?44:55,maxWidth:1500,fontWeight:600,lineHeight:1.22}}>{title}</div>}
   {items.map((item,i)=><div key={item} style={{fontSize:28,maxWidth:1470,marginTop:15,lineHeight:1.25,opacity:interpolate(f,[shot.cueFrames?.[i+1]??enter+15+i*12,(shot.cueFrames?.[i+1]??enter+15+i*12)+7],[0,1],clamp)}}><span style={{color:'#edc98e',marginRight:18}}>—</span>{item}</div>)}
  </div>
 </AbsoluteFill>;
};

const LabShot:React.FC<{shot:BreadLabShot;fps:number;chapterStart:boolean;chapterIndex:number}>=({shot,fps,chapterStart,chapterIndex})=>{
 if(!shot.simulation)return <Interlude shot={shot} fps={fps} chapterStart={chapterStart} chapterIndex={chapterIndex}/>;
 return <AbsoluteFill style={{background:P.paper,color:P.ink,overflow:'hidden'}}>
  <AbsoluteFill style={{background:'radial-gradient(ellipse at 25% 25%,rgba(255,255,255,.48),transparent 65%)'}}/>
  {shot.simulation==='money_split'?<MoneySplit shot={shot}/>:shot.simulation==='price_level'?<PriceLevel shot={shot}/>:shot.simulation==='inventory'?<Inventory shot={shot}/>:shot.simulation==='cost_ledger'?<CostLedger shot={shot}/>:shot.simulation==='competition'?<Competition shot={shot}/>:shot.simulation==='bread_power'?<BreadPower shot={shot}/>:shot.simulation==='basket_scope'?<BasketScope shot={shot}/>:<Synthesis shot={shot}/>}
 </AbsoluteFill>;
};

export const BreadLab:React.FC<BreadLabProps>=({plan,startFrame=0,frames})=>{
 validateBreadLabPlan(plan);const length=frames??plan.durationFrames-startFrame;const chapters=[...new Set(plan.shots.map(s=>s.chapterId))];
 return <AbsoluteFill style={{background:P.paper,fontFamily:font,fontVariantNumeric:'tabular-nums',overflow:'hidden'}}><LocalFonts/>
 {plan.shots.filter(s=>s.from<startFrame+length&&s.from+s.duration>startFrame).map(s=>{const i=plan.shots.findIndex(x=>x.id===s.id);return <Sequence key={s.id} from={s.from-startFrame} durationInFrames={s.duration} premountFor={30} name={`${s.chapterId}/${s.id}`}><LabShot shot={s} fps={plan.fps} chapterStart={i===0||plan.shots[i-1].chapterId!==s.chapterId} chapterIndex={chapters.indexOf(s.chapterId)}/></Sequence>;})}
 {plan.audio&&<Audio src={staticFile(plan.audio)} trimBefore={startFrame} durationInFrames={length}/>}
 </AbsoluteFill>;
};
