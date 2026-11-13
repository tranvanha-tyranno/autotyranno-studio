import React from 'react';
import {AbsoluteFill, Sequence, staticFile, useCurrentFrame, interpolate} from 'remotion';
import {Audio} from '@remotion/media';
import {SpatialScene} from './SpatialScenes';
import {PeopleScene} from './PeopleScenes';
import {DataTradeScene} from './DataTradeScenes';
import {StoryScene} from './StoryScenes';
import {font} from '../business/Shared';

const palettes={
 ink:{paper:'#112635',ink:'#f7efdf',accent:'#edb568',quiet:'#bdd0d3',rule:'#3a5969',soft:'#234352'},
 cream:{paper:'#f4eddd',ink:'#243932',accent:'#c65b3c',quiet:'#687970',rule:'#d5cbb7',soft:'#e6d7b7'},
 rust:{paper:'#923e31',ink:'#fff2db',accent:'#f4c782',quiet:'#f0d3bc',rule:'#ba7861',soft:'#ac5941'},
 sage:{paper:'#dce3d0',ink:'#233b37',accent:'#aa5436',quiet:'#5c7163',rule:'#b9c8ae',soft:'#c4d3b9'},
 slate:{paper:'#253440',ink:'#f9eedb',accent:'#dcb16f',quiet:'#b6cbd1',rule:'#566c78',soft:'#3e535f'},
};
const theme=(s:any)=>{
 if(['f07','d05','e04'].includes(s.id))return palettes.ink;
 if(s.chapter==='opening'||s.chapter==='trade')return ['o03','t04'].includes(s.id)?palettes.cream:palettes.ink;
 if(s.chapter==='property')return ['r02','r04','r07'].includes(s.id)?palettes.cream:palettes.rust;
 if(s.chapter==='households')return ['h03','h06'].includes(s.id)?palettes.cream:palettes.sage;
 if(s.chapter==='demography')return ['d01','d02'].includes(s.id)?palettes.slate:palettes.cream;
 if(s.chapter==='policy')return ['p01','p02'].includes(s.id)?palettes.cream:palettes.slate;
 return s.chapter==='ending'?palettes.ink:palettes.cream;
};

const Scene:React.FC<{shot:any}>=({shot})=>{
 const frame=useCurrentFrame(),p=theme(shot);
 const full=['f07','d05','e04'].includes(shot.id);
 const title=shot.headline;
 const long=title.length>63;
 const module=shot.variety.module;
 const component=module==='spatial'?<SpatialScene shot={shot} frame={frame} p={p}/>:module==='people'?<PeopleScene shot={shot} frame={frame} p={p}/>:module==='data'?<DataTradeScene shot={shot} frame={frame} p={p}/>:<StoryScene shot={shot} frame={frame} p={p}/>;
 const opacity=interpolate(frame,[0,8],[0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp'});
 const actualData=['f05','f06','r04','h04','d01','d02','p01','p02'].includes(shot.id);
 return <AbsoluteFill style={{background:p.paper,color:p.ink,overflow:'hidden',opacity}}>
   {component}
   {full?null:<div style={{position:'absolute',left:100,right:100,top:shot.variety.module==='spatial'?66:65,pointerEvents:'none'}}>
    {shot.phase==='disclaimer'?null:<div style={{font:'600 18px Arial',letterSpacing:2.4,color:full?'#edc48a':p.quiet,marginBottom:17}}>{shot.chapter==='opening'?'MỘT CÂU HỎI KINH TẾ':actualData?'DỮ LIỆU · GIỮ ĐÚNG PHẠM VI':shot.phase==='cta'?'CÙNG TÌM HIỂU TIẾP':null}</div>}
    <div style={{fontFamily:font,fontSize:shot.variety.module==='spatial'?(long?58:66):long?61:title.length>45?69:79,fontWeight:700,lineHeight:1.12,letterSpacing:-1,translate:`0 ${interpolate(frame,[0,20],[13,0],{extrapolateRight:'clamp'})}px`}}>{title}</div>
   </div>}
   {shot.sourceNote?<div style={{position:'absolute',left:100,right:100,bottom:143,color:full?'#f5ead9':p.quiet,font:'18px Arial',lineHeight:1.25}}>{actualData?shot.sourceNote:full?shot.images.map((im:any)=>im.credit).join(' · '):shot.id==='r06'?'Nguồn: World Bank 07/2026; IMF, tham vấn 2025, xuất bản 02/2026.':shot.id==='t01'?'Natural Earth · Public domain. Đường nối chỉ minh họa kết nối.':shot.id==='o04'?'Số liệu được đối chiếu đến 13/11/2026.':shot.variety.module==='story'?'Minh họa cơ chế · Không phải dự báo.':null}</div>:null}
   {full?null:<div style={{position:'absolute',left:100,right:100,top:855,height:1,background:p.rule,opacity:.4}}/>}
 </AbsoluteFill>;
};

export const VarietyFilm:React.FC<{data:any}>=({data})=>{
 const frame=useCurrentFrame(),seconds=frame/data.fps;
 const caption=data.captions.find((r:any,i:number)=>seconds>=r.start&&seconds<(i===data.captions.length-1?Math.max(r.end,data.frames/data.fps):r.end));
 return <AbsoluteFill style={{background:'#112635',overflow:'hidden'}}>
  {data.shots.map((s:any,i:number)=><Sequence key={s.id} from={s.start} durationInFrames={Math.min(s.end-s.start+8,data.frames-s.start)} name={`${s.id}: ${s.variety.mechanic}`}><Scene shot={s}/></Sequence>)}
  {caption?<div style={{position:'absolute',left:170,right:170,bottom:45,display:'flex',justifyContent:'center'}}><div style={{maxWidth:1580,padding:'11px 22px 13px',background:'rgba(10,22,26,.93)',color:'#fff2df',font:'34px Arial,sans-serif',lineHeight:1.25,textAlign:'center'}}>{caption.text}</div></div>:null}
  {data.audio?<Audio src={staticFile(data.audio)}/>:null}
 </AbsoluteFill>;
};
