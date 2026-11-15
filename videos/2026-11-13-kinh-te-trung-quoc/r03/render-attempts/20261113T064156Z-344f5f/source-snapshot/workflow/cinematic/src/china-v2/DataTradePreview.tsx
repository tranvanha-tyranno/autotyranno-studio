/** Isolated still-QA entry; the production entry is owned by the parent film. */
import {AbsoluteFill, Composition, registerRoot, useCurrentFrame} from 'remotion';
import {DataTradeScene} from './DataTradeScenes';
import {themes} from '../business/Shared';

const View: React.FC<{shot: any}> = ({shot}) => {
  const frame = useCurrentFrame(), p = themes[(shot.design?.theme ?? 'cream') as keyof typeof themes];
  return <AbsoluteFill style={{background: p.paper, color: p.ink}}>
    <div style={{position: 'absolute', left: 100, top: 72, right: 100, font: '700 67px Bahnschrift,Arial', lineHeight: 1.1}}>{shot.headline}</div>
    <DataTradeScene shot={shot} frame={frame} p={p}/>
    <div style={{position: 'absolute', left: 100, bottom: 142, font: '18px Arial', color: p.quiet}}>{shot.sourceNote}</div>
  </AbsoluteFill>;
};
const empty = {id: 'f05', start: 0, end: 400, design: {theme: 'cream'}};
registerRoot(() => <Composition id="DataTradeCheck" component={View} width={1920} height={1080}
  fps={30} durationInFrames={400} defaultProps={{shot: empty}}
  calculateMetadata={({props}) => ({durationInFrames: props.shot.end - props.shot.start})}/>);
