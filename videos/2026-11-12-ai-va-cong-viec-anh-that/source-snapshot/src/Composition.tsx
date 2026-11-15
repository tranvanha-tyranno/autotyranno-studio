import {AbsoluteFill,Sequence,useCurrentFrame,interpolate} from 'remotion';
import {TransitionSeries,linearTiming} from '@remotion/transitions';
import {fade} from '@remotion/transitions/fade';
import {slide} from '@remotion/transitions/slide';
import {wipe} from '@remotion/transitions/wipe';
import {Audio} from '@remotion/media';
import {staticFile} from 'remotion';
import {Numbers} from './scenes/Numbers';
import {Thesis} from './scenes/Thesis';
import {Globe} from './scenes/Globe';
import {Live} from './scenes/Live';
import {Flow} from './scenes/Flow';
import {Closing} from './scenes/Closing';
import data from '../public/data.json';

const Caption:React.FC=()=>{
 const frame=useCurrentFrame();const t=frame/30;
 const c=data.captions.find(c=>t>=c.start&&t<=c.end+.08);
 if(!c)return null;
 return <div style={{position:'absolute',bottom:76,left:105,right:105,textAlign:'center',fontFamily:'Arial',fontSize:36,fontWeight:400,color:'#f6f5f0',textShadow:'0 2px 12px #000,0 1px 3px #000',opacity:interpolate(t,[c.start,c.start+.05,c.end,c.end+.08],[0,1,1,0],{extrapolateLeft:'clamp',extrapolateRight:'clamp'})}}>{c.text}</div>;
};

export const Motion3D:React.FC=()=>{
 const f=useCurrentFrame();const c=data.cuts;const n=(i:number)=>c[i+1]-c[i]+(i<5?8:0);
 return <AbsoluteFill style={{background:'#080d16',overflow:'hidden'}}>
 <TransitionSeries>
  <TransitionSeries.Sequence durationInFrames={n(0)} name="Số liệu 3D"><Numbers/></TransitionSeries.Sequence>
  <TransitionSeries.Transition presentation={slide({direction:'from-right'})} timing={linearTiming({durationInFrames:8})}/>
  <TransitionSeries.Sequence durationInFrames={n(1)} name="Đối lập khái niệm"><Thesis/></TransitionSeries.Sequence>
  <TransitionSeries.Transition presentation={fade()} timing={linearTiming({durationInFrames:8})}/>
  <TransitionSeries.Sequence durationInFrames={n(2)} name="Địa cầu và luồng hàng"><Globe/></TransitionSeries.Sequence>
  <TransitionSeries.Transition presentation={fade()} timing={linearTiming({durationInFrames:8})}/>
  <TransitionSeries.Sequence durationInFrames={n(3)} name="Chi tiết đường may"><Live duration={n(3)}/></TransitionSeries.Sequence>
  <TransitionSeries.Transition presentation={wipe({direction:'from-left'})} timing={linearTiming({durationInFrames:8})}/>
  <TransitionSeries.Sequence durationInFrames={n(4)} name="Dòng giá trị"><Flow/></TransitionSeries.Sequence>
  <TransitionSeries.Transition presentation={fade()} timing={linearTiming({durationInFrames:8})}/>
  <TransitionSeries.Sequence durationInFrames={n(5)} name="Câu hỏi kết"><Closing/></TransitionSeries.Sequence>
 </TransitionSeries>
 <div style={{position:'absolute',inset:0,pointerEvents:'none',background:'linear-gradient(0deg,rgba(0,0,0,.85),transparent 16%,transparent 88%,rgba(0,0,0,.14))'}}/>
 <Sequence from={0}><Caption/></Sequence>
 <Audio src={staticFile('mix.wav')}/>
 <div style={{position:'absolute',inset:0,pointerEvents:'none',background:'#000',opacity:interpolate(f,[0,7,1484,1499],[1,0,0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp'})}}/>
 </AbsoluteFill>;
};
