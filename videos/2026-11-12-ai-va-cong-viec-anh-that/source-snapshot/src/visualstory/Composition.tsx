import {AbsoluteFill,staticFile,useCurrentFrame,interpolate} from 'remotion';
import {Audio} from '@remotion/media';
import {TransitionSeries,linearTiming} from '@remotion/transitions';
import {fade} from '@remotion/transitions/fade';
import raw from '../../public/visual-story/data.json';
import type {VisualTimeline} from './types';
import {VisualScene} from './Scene';
const data=raw as VisualTimeline;

export const VisualWorkAI:React.FC=()=>{
 const f=useCurrentFrame(),t=f/30;const caption=data.captions.find(c=>t>=c.start&&t<=c.end+.07);
 return <AbsoluteFill style={{background:'#080d16',overflow:'hidden'}}>
 <TransitionSeries>{data.chapters.flatMap((c,i)=>[
 <TransitionSeries.Sequence key={c.id} durationInFrames={c.end-c.start+(i<data.chapters.length-1?6:0)} name={c.label}><VisualScene chapter={c}/></TransitionSeries.Sequence>,
 ...(i===data.chapters.length-1?[]:[<TransitionSeries.Transition key={c.id+'-t'} presentation={fade()} timing={linearTiming({durationInFrames:6})}/>])
 ])}</TransitionSeries>
 {caption?<div style={{position:'absolute',left:110,right:110,bottom:65,fontFamily:'Arial',fontSize:36,fontWeight:400,color:'#fff',textAlign:'center',textShadow:'0 2px 8px #000,0 1px 3px #000',opacity:interpolate(t,[caption.start,caption.start+.05,caption.end,caption.end+.07],[0,1,1,0],{extrapolateLeft:'clamp',extrapolateRight:'clamp'})}}>{caption.text}</div>:null}
 <Audio src={staticFile('visual-story/mix.wav')}/>
 <div style={{position:'absolute',inset:0,pointerEvents:'none',background:'#000',opacity:interpolate(f,[0,7,data.frames-25,data.frames-1],[1,0,0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp'})}}/>
 </AbsoluteFill>;
};
