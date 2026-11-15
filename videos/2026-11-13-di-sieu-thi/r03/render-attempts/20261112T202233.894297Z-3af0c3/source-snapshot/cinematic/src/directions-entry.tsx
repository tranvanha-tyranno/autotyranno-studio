import {Composition, registerRoot} from 'remotion';
import {DirectionFilm} from './directions';
import type {DirectionTimeline} from './directions';
import raw from '../public/directions/long/data.json';

// A small production entry keeps older compositions out of this bundle.
// Pass an exact-take props.json to render either direction or a future topic.
const DirectionProduction: React.FC = () => <Composition
  id="DirectionPreview"
  component={DirectionFilm}
  width={1920}
  height={1080}
  fps={30}
  durationInFrames={raw.frames}
  defaultProps={{data: raw as unknown as DirectionTimeline}}
  calculateMetadata={({props}) => ({durationInFrames: props.data.frames, fps: props.data.fps})}
/>;

registerRoot(DirectionProduction);
