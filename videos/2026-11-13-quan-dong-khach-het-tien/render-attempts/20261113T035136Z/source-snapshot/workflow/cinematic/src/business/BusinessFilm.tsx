import {AbsoluteFill, Sequence, useCurrentFrame} from 'remotion';
import {Audio} from '@remotion/media';
import {staticFile} from 'remotion';
import {ChartScene} from './ChartScene';
import {CoffeeScene} from './CoffeeScene';
import {PaperScene} from './PaperScene';
import {PhotoScene} from './PhotoScene';
import {QuestionScene} from './QuestionScene';
import {SplitScene} from './SplitScene';
import type {BusinessShot, BusinessTimeline} from './types';

const Scene: React.FC<{shot: BusinessShot}> = ({shot}) => {
  const duration = shot.end - shot.start;
  if (shot.layout === 'b-paper') return <PaperScene shot={shot} duration={duration}/>;
  if (shot.layout === 'b-question' || shot.phase === 'disclaimer') return <QuestionScene shot={shot} duration={duration}/>;
  if (shot.layout === 'b-chart') return <ChartScene shot={shot} duration={duration}/>;
  if (shot.layout === 'b-split') return <SplitScene shot={shot} duration={duration}/>;
  if (shot.layout === 'b-coffee') return <CoffeeScene shot={shot} duration={duration}/>;
  return <PhotoScene shot={shot} duration={duration} closing={shot.layout === 'b-closing'}/>;
};

/** Business-only entry: no channel name, watermark, or legacy brand component. */
export const BusinessFilm: React.FC<{data: BusinessTimeline}> = ({data}) => {
  const frame = useCurrentFrame();
  const seconds = frame / data.fps;
  const caption = data.captions.find((item, index) => seconds >= item.start && seconds < (index === data.captions.length - 1 ? Math.max(item.end, data.frames / data.fps) : item.end));
  return <AbsoluteFill style={{background: '#172622', overflow: 'hidden'}}>
    {data.shots.map((shot, i) => <Sequence key={`${shot.id ?? i}-${shot.start}`} from={shot.start} durationInFrames={shot.end - shot.start} name={`${shot.id ?? i}: ${shot.headline ?? shot.layout}`}><Scene shot={shot}/></Sequence>)}
    {caption ? <div style={{position: 'absolute', left: 170, right: 170, bottom: 46, display: 'flex', justifyContent: 'center'}}><div style={{maxWidth: 1580, padding: '11px 22px 13px', background: 'rgba(10,22,16,.90)', color: '#faf0df', font: '34px Arial,sans-serif', lineHeight: 1.25, textAlign: 'center'}}>{caption.text}</div></div> : null}
    {data.audio ? <Audio src={staticFile(data.audio)}/> : null}
  </AbsoluteFill>;
};
