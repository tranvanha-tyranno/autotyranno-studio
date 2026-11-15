import {AbsoluteFill} from 'remotion';
import {Stage,Tokens,bgStyle} from '../World';
import {Type} from '../Type';
export const Flow:React.FC=()=>{
 return <AbsoluteFill style={{...bgStyle,background:'radial-gradient(ellipse at 65% 50%,#ffffff,#e6e4d9)',color:'#101e2b'}}>
 <Stage><Tokens/></Stage>
 <div style={{position:'absolute',left:120,top:165,fontSize:27,color:'#007b66',letterSpacing:6}}>TIỀN ĐI QUA. GIÁ TRỊ Ở LẠI.</div>
 <div style={{position:'absolute',top:255,left:120,fontSize:97,fontWeight:700,lineHeight:1.12}}><Type text="KHÔNG CHỈ"/><Type text="THÊM ĐƠN HÀNG." at={10}/></div>
 <div style={{position:'absolute',left:120,bottom:230,right:120,display:'flex',gap:90,fontSize:48,fontWeight:600}}>
 {['CÔNG NGHỆ','THIẾT KẾ','THƯƠNG HIỆU'].map((x,i)=><Type key={x} text={x} at={114+i*22} style={{color:i===2?'#bd442d':'#007b66'}}/>)}
 </div>
 </AbsoluteFill>;
};
