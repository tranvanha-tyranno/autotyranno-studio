import {AbsoluteFill, Composition, Sequence, interpolate, registerRoot, useCurrentFrame} from 'remotion';
import {PeopleScene, peopleSceneIds} from './PeopleScenes';
import {font} from '../business/Shared';

const palettes = {
  cream:{paper:'#f4eddd',ink:'#243932',accent:'#c65b3c',quiet:'#687970',rule:'#d5cbb7',soft:'#e6d7b7'},
  rust:{paper:'#923e31',ink:'#fff2db',accent:'#f4c782',quiet:'#f0d3bc',rule:'#ba7861',soft:'#ac5941'},
  sage:{paper:'#dce3d0',ink:'#233b37',accent:'#aa5436',quiet:'#5c7163',rule:'#b9c8ae',soft:'#c4d3b9'},
  slate:{paper:'#253440',ink:'#f9eedb',accent:'#dcb16f',quiet:'#b6cbd1',rule:'#566c78',soft:'#3e535f'},
};
const theme = (s:any) => s.chapter === 'property' ? ['r02','r04','r07'].includes(s.id) ? palettes.cream : palettes.rust
  : s.chapter === 'households' ? ['h03','h06'].includes(s.id) ? palettes.cream : palettes.sage
  : s.chapter === 'demography' ? ['d01','d02'].includes(s.id) ? palettes.slate : palettes.cream : palettes.slate;
const PeoplePreviewScene = ({shot}: {shot:any}) => {
  const frame = useCurrentFrame(), p = theme(shot), title = shot.id === 'h03' ? 'Cùng một khoản thu, ba lựa chọn' : shot.headline;
  return <AbsoluteFill style={{background:p.paper, color:p.ink, overflow:'hidden', opacity:interpolate(frame,[0,8],[0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp'})}}>
    <PeopleScene shot={shot} frame={frame} p={p}/>
    <div style={{position:'absolute',left:100,right:100,top:65}}>
      <div style={{font:'600 18px Arial',letterSpacing:2.4,color:p.quiet,marginBottom:17}}>{['d01','d02'].includes(shot.id)?'DỮ LIỆU · GIỮ ĐÚNG PHẠM VI':null}</div>
      <div style={{fontFamily:font,fontSize:title.length>63?61:title.length>45?69:79,fontWeight:700,lineHeight:1.12,letterSpacing:-1,translate:`0 ${interpolate(frame,[0,20],[13,0],{extrapolateRight:'clamp'})}px`}}>{title}</div>
    </div>
    {['d01','d02'].includes(shot.id)?<div style={{position:'absolute',left:100,right:100,bottom:143,color:p.quiet,font:'18px Arial',lineHeight:1.25}}>{shot.sourceNote}</div>:null}
    <div style={{position:'absolute',left:100,right:100,top:855,height:1,background:p.rule,opacity:.4}}/>
  </AbsoluteFill>;
};
const Preview = ({data}: {data:any}) => {
  const frame=useCurrentFrame(), seconds=frame/data.fps;
  const caption=data.captions.find((r:any)=>seconds>=r.start&&seconds<r.end);
  return <AbsoluteFill>
    {data.shots.filter((s:any)=>peopleSceneIds.includes(s.id)).map((s:any)=><Sequence key={s.id} from={s.start} durationInFrames={s.end-s.start}><PeoplePreviewScene shot={s}/></Sequence>)}
    {caption?<div style={{position:'absolute',left:170,right:170,bottom:45,display:'flex',justifyContent:'center'}}><div style={{maxWidth:1580,padding:'11px 22px 13px',background:'rgba(10,22,26,.93)',color:'#fff2df',font:'34px Arial,sans-serif',lineHeight:1.25,textAlign:'center'}}>{caption.text}</div></div>:null}
  </AbsoluteFill>;
};
const Root = () => <Composition id="PeoplePreview" component={Preview} width={1920} height={1080} fps={30} durationInFrames={17913} defaultProps={{data:{frames:17913,fps:30,shots:[],captions:[]}}}/>;
registerRoot(Root);
