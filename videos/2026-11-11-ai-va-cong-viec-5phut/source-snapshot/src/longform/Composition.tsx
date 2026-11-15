import {AbsoluteFill,staticFile,useCurrentFrame,interpolate} from 'remotion';
import {Audio} from '@remotion/media';
import {TransitionSeries,linearTiming} from '@remotion/transitions';
import {fade} from '@remotion/transitions/fade';
import {slide} from '@remotion/transitions/slide';
import {wipe} from '@remotion/transitions/wipe';
import raw from '../../public/longform/data.json';
import type {Timeline} from './types';
import {scenes} from './registry';
const data=raw as Timeline;

const Captions:React.FC=()=>{
 const t=useCurrentFrame()/30;const c=data.captions.find(c=>t>=c.start&&t<=c.end+.08);
 if(!c)return null;
 return <div style={{position:'absolute',bottom:75,left:110,right:110,textAlign:'center',fontFamily:'Arial',fontSize:36,fontWeight:400,color:'#f6f5f0',textShadow:'0 2px 12px #000,0 1px 3px #000',opacity:interpolate(t,[c.start,c.start+.05,c.end,c.end+.08],[0,1,1,0],{extrapolateLeft:'clamp',extrapolateRight:'clamp'})}}>{c.text}</div>;
};

export const WorkAI:React.FC=()=>{
 const f=useCurrentFrame();return <AbsoluteFill style={{background:'#080d16',overflow:'hidden'}}>
 <TransitionSeries>{data.chapters.flatMap((c,i)=>{
  const Component=scenes[c.id];const last=i===data.chapters.length-1;
  const transition=i%5===0?<TransitionSeries.Transition key={c.id+'-transition'} presentation={slide({direction:'from-right'})} timing={linearTiming({durationInFrames:10})}/>:i%3===0?<TransitionSeries.Transition key={c.id+'-transition'} presentation={wipe({direction:'from-left'})} timing={linearTiming({durationInFrames:10})}/>:<TransitionSeries.Transition key={c.id+'-transition'} presentation={fade()} timing={linearTiming({durationInFrames:10})}/>;
  return [<TransitionSeries.Sequence key={c.id} durationInFrames={c.end-c.start+(last?0:10)} name={c.label}><Component chapter={c}/></TransitionSeries.Sequence>,...(last?[]:[transition])];
 })}</TransitionSeries>
 <div style={{position:'absolute',inset:0,pointerEvents:'none',background:'linear-gradient(0deg,rgba(0,0,0,.85),transparent 17%,transparent 92%,rgba(0,0,0,.12))'}}/>
 <Captions/>
 <Audio src={staticFile('longform/mix.wav')}/>
 <div style={{position:'absolute',bottom:0,left:0,height:3,width:`${100*f/(data.frames-1)}%`,background:'#42ffd2',opacity:.7}}/>
 <div style={{position:'absolute',inset:0,pointerEvents:'none',background:'#000',opacity:interpolate(f,[0,8,data.frames-30,data.frames-1],[1,0,0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp'})}}/>
 </AbsoluteFill>;
};
