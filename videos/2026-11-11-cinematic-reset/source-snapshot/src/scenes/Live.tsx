import {AbsoluteFill,Sequence,staticFile,useCurrentFrame,interpolate} from 'remotion';
import {Video} from '@remotion/media';
import {ease,GREEN} from '../World';
export const Live:React.FC<{duration:number}>=({duration})=>{
 const f=useCurrentFrame();const cut=Math.round(duration*.42);return <AbsoluteFill style={{background:'#080d16'}}>
 <Sequence durationInFrames={cut}><Video src={staticFile('sewing-a.mp4')} muted style={{width:'100%',height:'100%',objectFit:'cover',filter:'saturate(.72) contrast(1.08)'}}/></Sequence>
 <Sequence from={cut}><Video src={staticFile('sewing-b.mp4')} muted style={{width:'100%',height:'100%',objectFit:'cover',filter:'saturate(.72) contrast(1.08)'}}/></Sequence>
 <div style={{position:'absolute',inset:0,background:'linear-gradient(90deg,rgba(0,0,0,.5),transparent 70%),linear-gradient(0deg,rgba(0,0,0,.65),transparent 45%)'}}/>
 <div style={{position:'absolute',left:120,top:190,fontSize:29,letterSpacing:6,color:GREEN,fontFamily:'Bahnschrift',opacity:ease(f,0,20)}}>NHÌN TỪ MỘT ĐƯỜNG MAY</div>
 {['VẢI','MÁY MÓC','THIẾT KẾ'].map((v,i)=>{const start=[99,118,141][i];return <div key={v} style={{position:'absolute',left:120,top:300+i*115,fontSize:90,fontWeight:700,fontFamily:'Bahnschrift',color:'#fff',opacity:interpolate(f,[start,start+13],[0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp'}),translate:`${interpolate(ease(f,start,start+18),[0,1],[-60,0])}px 0`}}>{v}</div>})}
 </AbsoluteFill>;
};
