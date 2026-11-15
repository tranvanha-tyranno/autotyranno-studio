import {AbsoluteFill,Sequence,staticFile,useCurrentFrame,interpolate} from 'remotion';
import {Video} from '@remotion/media';
import {Type} from '../Type';
import {ease,GREEN,WHITE} from '../World';
import {Objects} from './Objects';
import type {Chapter} from './types';

const leads:Record<string,string>={hook:'AI & CÔNG VIỆC',bundle:'TÁCH NHỎ MỘT CÔNG VIỆC',example:'TỪ BẢN NHÁP',exposure:'ẢNH HƯỞNG ĐẾN ĐÂU?',meaning:'HIỂU ĐÚNG CON SỐ',physical:'ĐỜI THỰC PHỨC TẠP HƠN',economics:'BÀI TOÁN HIỆU QUẢ',forecast:'DỰ BÁO ĐẾN 2030',context:'KHOẢNG CÁCH CHUYỂN ĐỔI',review:'GIÁ TRỊ CỦA CON NGƯỜI',hallucination:'MỘT LỖI RẤT NHỎ',map:'NHÌN LẠI VIỆC CỦA BẠN',experiment:'MỘT THỬ NGHIỆM NHỎ',measure:'ĐO CẢ QUY TRÌNH',skills:'CHUẨN BỊ TỪ HÔM NAY',portfolio:'BẰNG CHỨNG TIẾN BỘ',company:'CÙNG CHỊU TRÁCH NHIỆM',closing:'AI SẼ THAY ĐỔI ĐIỀU GÌ?'};
const footage:Record<string,{src:string;at:number;seconds:number}>={example:{src:'typing.mp4',at:0,seconds:6.8},physical:{src:'worker.mp4',at:0,seconds:6},review:{src:'reviewer.mp4',at:0,seconds:5},company:{src:'office.mp4',at:0,seconds:7}};

export const Scene:React.FC<{chapter:Chapter}>=({chapter:c})=>{
 const f=useCurrentFrame();const light=c.theme==='cream';const ink=light?'#102331':WHITE,accent=light?'#007b66':GREEN;
 const sequence=[{phrase:'',title:leads[c.id]??c.label,sub:'',at:0},...c.beats];
 let index=0;for(let i=0;i<sequence.length;i++)if(sequence[i].at<=f)index=i;
 const beat=sequence[index];const local=f-beat.at;
 const next=sequence[index+1]?.at??100000;
 const beatOut=1-ease(f,next-6,next);
 const media=footage[c.id];const footageFrames=media?media.seconds*30:0;const inFootage=!!media&&f<footageFrames;
 const subtitleColor=inFootage?'#ffffff':ink;
 return <AbsoluteFill style={{background:light?'radial-gradient(ellipse at 65% 50%,#ffffff,#e6e4d9)':'radial-gradient(ellipse at 70% 50%,#182b43,#080d16 60%,#05080e)',fontFamily:'Bahnschrift,Arial,sans-serif',color:ink,overflow:'hidden'}}>
 <Objects kind={c.kind} phase={index-1} splitAt={c.beats[1].at}/>
 {media?<Sequence durationInFrames={Math.round(footageFrames)}><Video src={staticFile('longform/'+media.src)} muted style={{width:'100%',height:'100%',objectFit:'cover',filter:'saturate(.72) contrast(1.05)',opacity:1-ease(f,footageFrames-15,footageFrames)}}/><div style={{position:'absolute',inset:0,opacity:1-ease(f,footageFrames-15,footageFrames),background:'linear-gradient(90deg,rgba(2,10,17,.88),rgba(2,10,17,.12))'}}/></Sequence>:null}
 <div style={{position:'absolute',top:150,left:120,right:120,fontSize:27,letterSpacing:4,color:inFootage?GREEN:accent,opacity:ease(f)}}>{c.label}</div>
 <div key={index} style={{position:'absolute',left:115,top:285,width:920,opacity:beatOut}}>
 <Sequence from={beat.at} layout="none"><Type text={beat.title} at={0} step={3} style={{fontSize:92,fontWeight:700,lineHeight:1.14,letterSpacing:-1.5,color:subtitleColor}}/>
 <Type text={beat.sub} at={10} step={2} style={{marginTop:34,fontSize:39,fontWeight:500,lineHeight:1.3,letterSpacing:.8,color:inFootage?GREEN:accent}}/></Sequence>
 </div>
 {c.kind==='bars'?<div style={{position:'absolute',left:1130,top:797,width:620,display:'flex',justifyContent:'space-between',fontSize:27,color:GREEN}}><span>CÓ THỂ TẠO RA</span><span style={{color:'#ff7358'}}>CÓ THỂ DỊCH CHUYỂN</span></div>:null}
 {c.kind==='people'?<div style={{position:'absolute',left:1120,top:775,width:650,fontSize:25,lineHeight:1.35,color:GREEN,opacity:ease(f,c.beats[0].at,c.beats[0].at+20)}}>TIẾP XÚC TIỀM NĂNG / KHÔNG PHẢI SA THẢI</div>:null}
 {c.source?<div style={{position:'absolute',left:120,bottom:195,fontFamily:'Arial',fontSize:25,color:light?'#51616a':'#9daeba',maxWidth:1580}}>{c.source}</div>:null}
 {c.kind==='steps'?<div style={{position:'absolute',right:140,bottom:190,fontSize:23,color:'#9daeba'}}>MINH HỌA NĂNG LỰC / KHÔNG PHẢI DỮ LIỆU XẾP HẠNG</div>:null}
 {c.id==='closing'?<div style={{position:'absolute',left:120,bottom:190,fontSize:23,letterSpacing:6,opacity:interpolate(local,[5,25],[0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp'})}}>TYRANNO / EXPLAINED</div>:null}
 </AbsoluteFill>;
};
