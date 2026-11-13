import {Composition, registerRoot} from 'remotion';
import {ChinaFilm} from './china';
import type {ChinaTimeline} from './china';

const empty: ChinaTimeline = {fps: 30, frames: 30, title: '', audio: '', shots: [], captions: []};
const Production: React.FC = () => <Composition id="ChinaPreview" component={ChinaFilm} width={1920} height={1080}
  fps={30} durationInFrames={30} defaultProps={{data: empty}}
  calculateMetadata={({props}) => ({durationInFrames: props.data.frames, fps: props.data.fps})}/>;
registerRoot(Production);
