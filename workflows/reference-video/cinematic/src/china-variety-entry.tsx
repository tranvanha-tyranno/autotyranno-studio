import {Composition,registerRoot} from 'remotion';
import {VarietyFilm} from './china-v2/VarietyFilm';
const empty={fps:30,frames:30,title:'',audio:'',shots:[],captions:[]};
const Root:React.FC=()=> <Composition id="ChinaPreview" component={VarietyFilm} width={1920} height={1080} fps={30} durationInFrames={30} defaultProps={{data:empty}} calculateMetadata={({props})=>({fps:props.data.fps,durationInFrames:props.data.frames})}/>;
registerRoot(Root);
