import {AbsoluteFill,useCurrentFrame,interpolate} from 'remotion';
import {Stage,Containers,GREEN,ORANGE,bgStyle,ease} from '../World';
import {Type} from '../Type';
export const Thesis:React.FC=()=>{
 const f=useCurrentFrame();return <AbsoluteFill style={bgStyle}>
 <div style={{position:'absolute',width:1920,height:1080,left:450,top:0,opacity:.8}}><Stage><Containers/></Stage></div>
 <div style={{position:'absolute',left:120,top:245,fontSize:39,letterSpacing:5,color:GREEN,opacity:ease(f)}}>NHƯNG KHOAN.</div>
 <Type text="KIM NGẠCH" at={35} style={{position:'absolute',left:115,top:335,fontSize:114,fontWeight:700,letterSpacing:-3}}/>
 <div style={{position:'absolute',left:130,top:490,fontSize:148,color:ORANGE,scale:interpolate(ease(f,22,40),[0,1],[.3,1]),transformOrigin:'left'}}>≠</div>
 <Type text="LỢI NHUẬN" at={80} style={{position:'absolute',left:120,top:675,fontSize:105,fontWeight:700,letterSpacing:-2}}/>
 <div style={{position:'absolute',right:110,top:720,fontSize:34,color:GREEN,opacity:ease(f,125,145)*(1-ease(f,180,195))}}>QUY MÔ GIAO DỊCH</div>
 <div style={{position:'absolute',right:110,top:720,fontSize:34,color:ORANGE,opacity:ease(f,185,205)}}>SAU KHI TRỪ CHI PHÍ</div>
 </AbsoluteFill>;
};
