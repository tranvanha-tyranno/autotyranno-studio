import {AbsoluteFill,useCurrentFrame,interpolate} from 'remotion';
import {Stage,Earth,GREEN,bgStyle,ease} from '../World';
import {Type} from '../Type';
export const Closing:React.FC=()=>{
 const f=useCurrentFrame();return <AbsoluteFill style={bgStyle}>
 <div style={{position:'absolute',inset:0,opacity:.38}}><Stage><Earth right/></Stage></div>
 <div style={{position:'absolute',left:120,top:215,fontSize:31,letterSpacing:7,color:GREEN,opacity:ease(f)}}>CÂU HỎI DÀI HẠN</div>
 <Type text="BÁN NHIỀU HƠN," at={62} style={{position:'absolute',left:115,top:320,fontSize:112,fontWeight:700,lineHeight:1.12,letterSpacing:-2}}/>
 <div style={{position:'absolute',left:115,top:465,fontSize:112,fontWeight:700,lineHeight:1.12,letterSpacing:-2,color:GREEN,translate:`0 ${interpolate(ease(f,117,145),[0,1],[45,0])}px`}}><Type text="HAY LÀM CHỦ" at={117}/><Type text="NHIỀU HƠN?" at={138}/></div>
 <div style={{position:'absolute',left:125,bottom:220,fontSize:24,letterSpacing:6,opacity:ease(f,55,80)}}>TYRANNO / EXPLAINED</div>
 </AbsoluteFill>;
};
