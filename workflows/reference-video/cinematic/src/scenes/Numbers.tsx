import {AbsoluteFill,useCurrentFrame,interpolate} from 'remotion';
import {Stage,Digits,GREEN,bgStyle,ease} from '../World';
export const Numbers:React.FC=()=>{
 const f=useCurrentFrame();return <AbsoluteFill style={bgStyle}>
 <div style={{position:'absolute',inset:0,background:'radial-gradient(ellipse at center,rgba(66,255,210,.07),transparent 65%)'}}/>
 <Stage><Digits/></Stage>
 <div style={{position:'absolute',top:155,left:0,right:0,textAlign:'center',fontSize:25,letterSpacing:12,opacity:ease(f,25,50),color:GREEN}}>QUY MÔ CỦA MỘT DẤU MỐC</div>
 <div style={{position:'absolute',top:700,left:0,right:0,textAlign:'center',fontSize:91,fontWeight:700,letterSpacing:14,opacity:ease(f,17,36),translate:`0 ${interpolate(ease(f,17,36),[0,1],[40,0])}px`}}>TỶ ĐÔ LA</div>
 </AbsoluteFill>;
};
