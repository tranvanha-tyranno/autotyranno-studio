import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {Emphasis, Media, Source, font, rise, themeFor} from './Shared';
import type {BusinessShot} from './types';

export const QuestionScene: React.FC<{shot: BusinessShot; duration: number}> = ({shot, duration}) => {
  const frame = useCurrentFrame();
  const p = themeFor(shot, 'dark');
  return <AbsoluteFill style={{background: p.paper, color: p.ink}}>
    {shot.images[0] ? <div style={{position: 'absolute', right: -80, top: 0, bottom: 0, width: 850, opacity: .52}}><Media image={shot.images[0]} duration={duration}/><AbsoluteFill style={{background: `linear-gradient(90deg,${p.paper},transparent 80%)`}}/></div> : null}
    <div style={{position: 'absolute', left: 100, top: shot.phase === 'disclaimer' ? 172 : 161, width: 1470}}>
      {shot.eyebrow || shot.phase === 'disclaimer' ? <div style={{font: '700 22px Arial,sans-serif', letterSpacing: 3.2, color: p.accent, marginBottom: 43}}>{shot.eyebrow ?? 'MIỄN TRỪ TRÁCH NHIỆM'}</div> : null}
      <div style={{fontFamily: font, fontSize: (shot.headline?.length ?? 0) > 95 ? 80 : (shot.headline?.length ?? 0) > 58 ? 100 : 128, fontWeight: 700, lineHeight: 1.06, letterSpacing: -2.7, opacity: rise(frame, 1, 18), translate: `0 ${(1 - rise(frame, 1, 18)) * 45}px`, maxWidth: 1450}}><Emphasis text={shot.headline} words={shot.design?.emphasis} color={p.accent}/></div>
      {shot.body ? <div style={{font: '36px Arial,sans-serif', lineHeight: 1.45, color: p.quiet, marginTop: 43, maxWidth: 1330, opacity: rise(frame, 14)}}>{shot.body}</div> : null}
      <div style={{width: rise(frame, 7, 24) * 140, height: 5, marginTop: 44, background: p.accent}}/>
    </div>
    <Source shot={shot} light={(shot.design?.theme ?? 'dark') !== 'cream'}/>
  </AbsoluteFill>;
};
