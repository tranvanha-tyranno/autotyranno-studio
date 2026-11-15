import {AbsoluteFill,Composition,Sequence,registerRoot,useCurrentFrame} from 'remotion';
import {StoryScene} from './StoryScenes';
const p={paper:'#112635',ink:'#f7efdf',accent:'#edb568',quiet:'#bdd0d3',rule:'#3a5969',soft:'#234352'};
const Scene:React.FC<{shot:any}>=({shot})=>{const frame=useCurrentFrame();return <AbsoluteFill style={{background:p.paper}}><StoryScene shot={shot} frame={frame} p={p}/><div style={{position:'absolute',left:100,right:100,top:80,color:p.ink,font:'700 70px Bahnschrift,Arial',lineHeight:1.15}}>{shot.headline}</div></AbsoluteFill>};
const Film:React.FC<{data:any}>=({data})=><AbsoluteFill>{data.shots.filter((s:any)=>s.variety.module==='story').map((s:any)=><Sequence key={s.id} from={s.start} durationInFrames={s.end-s.start}><Scene shot={s}/></Sequence>)}</AbsoluteFill>;
const empty={fps:30,frames:30,shots:[]};
registerRoot(()=> <Composition id="ChinaPreview" component={Film} width={1920} height={1080} fps={30} durationInFrames={30} defaultProps={{data:empty}} calculateMetadata={({props})=>({fps:props.data.fps,durationInFrames:props.data.frames})}/>);
