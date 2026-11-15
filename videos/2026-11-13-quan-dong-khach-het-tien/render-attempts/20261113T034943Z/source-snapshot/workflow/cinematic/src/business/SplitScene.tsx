import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {Header, Media, Source, font, localCue, rise, themeFor} from './Shared';
import type {BusinessShot} from './types';

export const SplitScene: React.FC<{shot: BusinessShot; duration: number}> = ({shot, duration}) => {
  const frame = useCurrentFrame();
  const p = themeFor(shot);
  const count = Math.min(3, Math.max(2, shot.design?.choices?.length ?? 2));
  const panelWidth = count === 3 ? 550 : 820;
  const panelGap = count === 3 ? 35 : 80;
  return <AbsoluteFill style={{background: p.paper, color: p.ink}}>
    <Header shot={shot}/>
    {Array.from({length: count}, (_, index) => index).map(index => {
      const choice = shot.design?.choices?.[index];
      const image = shot.images[index] ?? shot.images[0];
      const entry = rise(frame, localCue(shot, index, index * 17), 20);
      return <div key={index} style={{position: 'absolute', left: 100 + index * (panelWidth + panelGap), top: 280, width: panelWidth, height: 530, background: index === 0 ? p.soft : '#294337', color: index === 0 ? p.ink : '#f7eddb', overflow: 'hidden', opacity: entry, translate: `0 ${(1 - entry) * 40}px`}}>
        {image ? <div style={{position: 'absolute', left: 0, right: 0, top: 0, height: 290}}><Media image={image} duration={duration} reverse={index === 1}/></div> : null}
        <div style={{position: 'absolute', left: 35, right: 35, top: 320}}>
          {choice?.label ? <div style={{font: '700 19px Arial,sans-serif', letterSpacing: 2.5, opacity: .75, marginBottom: 12}}>{choice.label}</div> : null}
          <div style={{fontFamily: font, fontSize: count === 3 ? 40 : 45, lineHeight: 1.13, fontWeight: 700}}>{choice?.title}</div>
          {choice?.body ? <div style={{font: '27px Arial,sans-serif', lineHeight: 1.35, marginTop: 12, opacity: .84}}>{choice.body}</div> : null}
        </div>
      </div>;
    })}
    <Source shot={shot}/>
  </AbsoluteFill>;
};
