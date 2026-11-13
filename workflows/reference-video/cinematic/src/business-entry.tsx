import {Composition, registerRoot} from 'remotion';
import {BusinessFilm} from './business';
import type {BusinessTimeline} from './business';

const empty: BusinessTimeline = {fps: 30, frames: 30, title: '', audio: '', shots: [], captions: []};
const BusinessProduction: React.FC = () => <Composition id="BusinessPreview" component={BusinessFilm}
  width={1920} height={1080} fps={30} durationInFrames={30} defaultProps={{data: empty}}
  calculateMetadata={({props}) => ({durationInFrames: props.data.frames, fps: props.data.fps})}/>;
registerRoot(BusinessProduction);
