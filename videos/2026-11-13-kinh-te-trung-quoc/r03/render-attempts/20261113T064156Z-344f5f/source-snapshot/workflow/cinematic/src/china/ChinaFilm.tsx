import {AbsoluteFill, Sequence, staticFile, useCurrentFrame} from 'remotion';
import {Audio} from '@remotion/media';
import {PhotoScene} from '../business/PhotoScene';
import {QuestionScene} from '../business/QuestionScene';
import type {BusinessShot} from '../business/types';
import {MapScene} from './MapScene';
import {FlowScene} from './FlowScene';
import {ChinaChart} from './ChartScene';
import {SimulationScene} from './SimulationScene';
import {CompareScene} from './CompareScene';
import type {ChinaShot, ChinaTimeline} from './types';

const Scene: React.FC<{shot: ChinaShot}> = ({shot}) => {
  const duration = shot.end - shot.start;
  if (shot.layout === 'c-map') return <MapScene shot={shot} duration={duration}/>;
  if (shot.layout === 'c-flow') return <FlowScene shot={shot} duration={duration}/>;
  if (shot.layout === 'c-chart') return <ChinaChart shot={shot} duration={duration}/>;
  if (shot.layout === 'c-sim') return <SimulationScene shot={shot} duration={duration}/>;
  if (shot.layout === 'c-compare') return <CompareScene shot={shot}/>;
  // Reuse only neutral typography/media primitives; no old media or coffee geometry.
  const generic = {...shot, layout: shot.layout === 'c-question' ? 'b-question' : shot.layout === 'c-closing' ? 'b-closing' : 'b-photo'} as BusinessShot;
  if (shot.layout === 'c-question' || shot.phase === 'disclaimer') return <QuestionScene shot={generic} duration={duration}/>;
  return <PhotoScene shot={generic} duration={duration} closing={shot.layout === 'c-closing'}/>;
};

export const ChinaFilm: React.FC<{data: ChinaTimeline}> = ({data}) => {
  const frame = useCurrentFrame(), seconds = frame / data.fps;
  const caption = data.captions.find((row, i) => seconds >= row.start && seconds < (i === data.captions.length - 1 ? Math.max(row.end, data.frames / data.fps) : row.end));
  return <AbsoluteFill style={{background: '#172622', overflow: 'hidden'}}>
    {data.shots.map((shot, i) => <Sequence key={`${shot.id ?? i}-${shot.start}`} from={shot.start} durationInFrames={shot.end - shot.start} name={`${shot.id ?? i}: ${shot.headline ?? shot.layout}`}><Scene shot={shot}/></Sequence>)}
    {caption ? <div style={{position: 'absolute', left: 170, right: 170, bottom: 46, display: 'flex', justifyContent: 'center'}}><div style={{maxWidth: 1580, padding: '11px 22px 13px', background: 'rgba(10,22,16,.90)', color: '#faf0df', font: '34px Arial,sans-serif', lineHeight: 1.25, textAlign: 'center'}}>{caption.text}</div></div> : null}
    {data.audio ? <Audio src={staticFile(data.audio)}/> : null}
  </AbsoluteFill>;
};
