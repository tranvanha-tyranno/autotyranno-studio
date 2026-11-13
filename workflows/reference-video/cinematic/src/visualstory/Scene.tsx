import {AbsoluteFill,CanvasImage,Sequence,staticFile,useCurrentFrame,interpolate} from 'remotion';
import {Video} from '@remotion/media';
import {Objects} from '../longform/Objects';
import {Type} from '../Type';
import {ease,GREEN} from '../World';
import type {Shot,VisualChapter} from './types';

const Lens:React.FC<{shot:Shot}>=({shot:s})=>{
 const f=useCurrentFrame();const n=s.end-s.start;const p=Math.min(1,f/Math.max(1,n-1));
 const zoom=s.pan?1.09-.065*p:1.025+.065*p;
 if(s.type==='graphic')return <AbsoluteFill style={{background:'radial-gradient(ellipse at 70% 50%,#182b43,#080d16 65%)'}}><Objects kind="bars" phase={0} splitAt={0}/>
 <div style={{position:'absolute',left:120,top:210,fontFamily:'Bahnschrift,Arial',color:'#f4f5ef'}}><div style={{fontSize:29,letterSpacing:4,color:GREEN}}>DỰ BÁO ĐẾN NĂM 2030</div><Type text="170 TRIỆU" style={{fontSize:100,fontWeight:700,marginTop:50}}/><Type text="có thể được tạo ra" at={8} style={{fontSize:39,color:GREEN}}/><Type text="92 TRIỆU" at={18} style={{fontSize:100,fontWeight:700,marginTop:35}}/><Type text="có thể bị dịch chuyển" at={26} style={{fontSize:39,color:'#ff7358'}}/></div>
 <div style={{position:'absolute',left:120,bottom:205,fontFamily:'Arial',fontSize:25,color:'#b7c3cd'}}>WEF 2025 · Nhiều xu hướng cơ cấu · Không chỉ do AI</div></AbsoluteFill>;
 const style:React.CSSProperties={width:'100%',height:'100%',objectFit:'cover',objectPosition:`${s.focus[0]}% ${s.focus[1]}%`,scale:zoom,translate:`${(s.pan?-1:1)*(p-.5)*22}px ${(p-.5)*-12}px`,filter:'saturate(.94) contrast(1.025)'};
 if(s.type==='photo'&&s.aspect<1.2)return <AbsoluteFill style={{overflow:'hidden',background:'#121c22'}}>
 <CanvasImage src={staticFile('visual-story/'+s.file)} style={{...style,scale:1.15,filter:'blur(30px) saturate(.85) brightness(.55)'}}/>
 <CanvasImage src={staticFile('visual-story/'+s.file)} style={{position:'absolute',left:0,top:0,width:'100%',height:'100%',objectFit:'contain',scale:1.005+p*.018,filter:'saturate(.96) contrast(1.02)'}}/>
 </AbsoluteFill>;
 return <AbsoluteFill style={{overflow:'hidden',background:'#131b22'}}>
 {s.type==='video'?<Video src={staticFile('visual-story/'+s.file)} muted style={style}/>:<CanvasImage src={staticFile('visual-story/'+s.file)} style={style}/>}
 </AbsoluteFill>;
};

const emphasis:Record<string,{beat:number;hold:number;title?:string}[]>={
 hook:[{beat:1,hold:95}],bundle:[{beat:0,hold:80}],example:[{beat:2,hold:80}],
 exposure:[{beat:0,hold:100,title:'1 TRONG 4'},{beat:2,hold:70}],meaning:[{beat:0,hold:80}],
 physical:[{beat:2,hold:60}],economics:[{beat:1,hold:85}],context:[{beat:2,hold:80}],
 review:[{beat:1,hold:80}],hallucination:[{beat:0,hold:85}],map:[{beat:0,hold:95}],
 experiment:[{beat:1,hold:75}],measure:[{beat:1,hold:90}],skills:[{beat:2,hold:85}],
 portfolio:[{beat:0,hold:80}],company:[{beat:1,hold:95}],closing:[{beat:2,hold:140}]
};

export const VisualScene:React.FC<{chapter:VisualChapter}>=({chapter:c})=>{
 const f=useCurrentFrame();let active=c.shots[0];for(const s of c.shots)if(s.start<=f)active=s;
 const overlays=emphasis[c.id]??[];
 return <AbsoluteFill style={{background:'#080d16',fontFamily:'Bahnschrift,Arial,sans-serif',overflow:'hidden'}}>
 {c.shots.map((s,i)=>{const next=c.shots[i+1];const extra=next?5:6;return <Sequence key={s.start} from={s.start} durationInFrames={s.end-s.start+extra} name={s.purpose}><AbsoluteFill style={{opacity:interpolate(f,[s.start,s.start+5,s.end,s.end+extra],[i===0?1:0,1,1,next?0:1],{extrapolateLeft:'clamp',extrapolateRight:'clamp'})}}><Lens shot={s}/></AbsoluteFill></Sequence>})}
 <div style={{position:'absolute',inset:0,pointerEvents:'none',background:'linear-gradient(0deg,rgba(0,0,0,.90),rgba(0,0,0,.06) 29%,transparent 66%,rgba(0,0,0,.17))'}}/>
 <div style={{position:'absolute',left:110,top:88,color:'#fff',fontSize:24,letterSpacing:3,opacity:1-ease(f,90,110),textShadow:'0 2px 8px #000',borderLeft:'4px solid #42ffd2',paddingLeft:18}}>{c.label}</div>
 {active.type!=='graphic'?<div style={{position:'absolute',left:110,bottom:145,fontFamily:'Arial',fontSize:18,letterSpacing:1,color:'#e8ebed',opacity:.75,textShadow:'0 2px 6px #000'}}>ẢNH MINH HỌA · {active.type==='video'?'MIXKIT':'PEXELS'}</div>:null}
 {active.type!=='graphic'?overlays.map((e,i)=>{const b=c.beats[e.beat];const at=b.at;const until=Math.min(c.end-c.start-10,at+e.hold);const opacity=ease(f,at,at+8)*(1-ease(f,until-10,until));return <Sequence key={i} from={at} durationInFrames={Math.max(1,until-at)} layout="none"><div style={{position:'absolute',left:110,bottom:235,maxWidth:1530,color:'#fff',opacity,textShadow:'0 2px 18px rgba(0,0,0,.95)'}}>
 <Type text={e.title??b.title} at={0} step={2} style={{fontSize:c.id==='exposure'&&e.beat===0?112:65,fontWeight:700,lineHeight:1.1,letterSpacing:-.5}}/>
 {c.id==='exposure'&&e.beat===0?<div style={{fontSize:29,marginTop:14,color:GREEN}}>MỨC TIẾP XÚC VỚI AI TẠO SINH · ILO 2025</div>:null}
 </div></Sequence>}):null}
 {c.id==='forecast'&&active.type!=='graphic'?<div style={{position:'absolute',left:110,bottom:235,color:'#fff',fontSize:29,textShadow:'0 2px 8px #000'}}>Dự báo của nhà tuyển dụng / WEF 2025</div>:null}
 </AbsoluteFill>;
};
