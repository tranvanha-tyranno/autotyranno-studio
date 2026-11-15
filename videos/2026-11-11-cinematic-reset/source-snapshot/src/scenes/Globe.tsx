import {AbsoluteFill,useCurrentFrame,interpolate} from 'remotion';
import {Stage,Earth,GREEN,bgStyle,ease} from '../World';
import {Type} from '../Type';
export const Globe:React.FC=()=>{
 const f=useCurrentFrame();return <AbsoluteFill style={bgStyle}>
 <Stage><Earth right/></Stage>
 <div style={{position:'absolute',left:120,top:200,color:GREEN,letterSpacing:6,fontSize:27,opacity:ease(f)}}>THƯƠNG MẠI VIỆT NAM</div>
 <div style={{position:'absolute',left:115,top:290,fontSize:172,fontWeight:700,lineHeight:.95,opacity:1-ease(f,130,145),translate:`0 ${-50*ease(f,130,145)}px`}}><Type text="10 THÁNG" at={5}/><Type text="2026" at={14} style={{color:GREEN}}/></div>
 <div style={{position:'absolute',left:115,top:305,fontSize:95,fontWeight:700,lineHeight:1.25}}><Type text="XUẤT KHẨU" at={145}/><Type text="+" at={160} style={{color:GREEN,fontSize:125}}/><Type text="NHẬP KHẨU" at={171}/></div>
 <div style={{position:'absolute',left:120,top:770,fontSize:39,letterSpacing:2,opacity:ease(f,235,255),translate:`0 ${interpolate(ease(f,235,255),[0,1],[30,0])}px`}}>HÀNG ĐI RA. NGUYÊN LIỆU ĐI VÀO.</div>
 <div style={{position:'absolute',right:115,top:125,fontSize:21,letterSpacing:3,opacity:.55}}>MINH HỌA LUỒNG THƯƠNG MẠI</div>
 </AbsoluteFill>;
};
