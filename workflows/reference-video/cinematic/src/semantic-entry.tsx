import {Composition, registerRoot} from 'remotion';
import {SemanticFilm} from './semantic';
import type {SemanticTimeline} from './semantic/types';
import raw from '../public/semantic/long/data.json';

const SemanticProduction: React.FC = () => <Composition
  id="SemanticReview"
  component={SemanticFilm}
  width={1920}
  height={1080}
  fps={30}
  durationInFrames={raw.frames}
  defaultProps={{data: raw as unknown as SemanticTimeline}}
  calculateMetadata={({props}) => ({durationInFrames: props.data.frames, fps: props.data.fps})}
/>;

registerRoot(SemanticProduction);
