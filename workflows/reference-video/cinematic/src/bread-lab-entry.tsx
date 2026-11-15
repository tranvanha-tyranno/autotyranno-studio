import React from 'react';
import {Composition,registerRoot} from 'remotion';
import {BreadLab,validateBreadLabPlan,type BreadLabProps} from './bread-lab';
const defaults:BreadLabProps={plan:{fps:30,durationFrames:300,title:'',shots:[],audio:''}};
const Root:React.FC=()=> <Composition id="BreadLab" component={BreadLab} defaultProps={defaults} width={1920} height={1080} fps={30} durationInFrames={300} calculateMetadata={({props})=>{
 validateBreadLabPlan(props.plan);const from=props.startFrame??0;const n=props.frames??props.plan.durationFrames-from;
 if(!Number.isInteger(from)||from<0||!Number.isInteger(n)||n<1||from+n>props.plan.durationFrames)throw new Error('BreadLab proof outside plan.');return{durationInFrames:n,fps:props.plan.fps};
 }}/>;
registerRoot(Root);
