import {AbsoluteFill, Sequence, interpolate, useCurrentFrame} from 'remotion';
import {Emphasis, Header, Media, Source, clamp, font, localCue, rise, themeFor} from './Shared';
import type {BusinessShot} from './types';

/** Two or three contextual cuts. Media movement never stretches or loops video. */
export const PhotoScene: React.FC<{shot: BusinessShot; duration: number; closing?: boolean}> = ({shot, duration, closing}) => {
  const frame = useCurrentFrame();
  const p = themeFor(shot, 'dark');
  const deck = shot.images.slice(0, 3);
  const starts = deck.map((_, index) => index === 0 ? 0 : localCue(shot, index - 1, duration * index / deck.length));
  return <AbsoluteFill style={{background: '#172622'}}>
    {deck.map((image, i) => <Sequence key={`${image.file}-${i}`} from={starts[i]} durationInFrames={Math.max(1, (starts[i + 1] ?? duration) - starts[i])}>
      <Media image={image} duration={(starts[i + 1] ?? duration) - starts[i]} reverse={i % 2 === 1}/>
    </Sequence>)}
    <AbsoluteFill style={{background: closing ? 'linear-gradient(90deg,rgba(10,23,17,.93),rgba(10,23,17,.71) 57%,rgba(10,23,17,.12))' : 'linear-gradient(0deg,rgba(9,20,14,.95),rgba(9,20,14,.58) 31%,rgba(9,20,14,.07) 70%)'}}/>
    {closing ? <>
      <Header shot={shot} light style={{top: 185, right: 500}}/>
      {shot.body ? <div style={{position: 'absolute', top: 520, left: 100, width: 1140, color: '#e5eade', font: '36px Arial,sans-serif', lineHeight: 1.43, opacity: rise(frame, 10)}}>{shot.body}</div> : null}
      <div style={{position: 'absolute', top: 734, left: 100, width: interpolate(frame, [12, 35], [0, 120], clamp), height: 5, background: '#e9b779'}}/>
    </> : <>
      {shot.eyebrow ? <div style={{position: 'absolute', left: 100, top: 75, font: '700 21px Arial,sans-serif', letterSpacing: 3, color: '#f4e7d0', borderLeft: '4px solid #e9b779', paddingLeft: 20}}>{shot.eyebrow}</div> : null}
      <div style={{position: 'absolute', left: 100, right: 140, bottom: 245, color: '#fff3df', opacity: rise(frame, 2), translate: `0 ${(1 - rise(frame, 2)) * 26}px`}}>
        {shot.headline ? <div style={{fontFamily: font, fontSize: shot.headline.length > 70 ? 62 : shot.headline.length > 45 ? 75 : 92, fontWeight: 700, letterSpacing: -1.8, lineHeight: 1.08, maxWidth: 1520}}><Emphasis text={shot.headline} words={shot.design?.emphasis} color='#efbd81'/></div> : null}
        {shot.body ? <div style={{font: '34px Arial,sans-serif', lineHeight: 1.38, maxWidth: 1450, marginTop: 23, color: '#e5eade'}}>{shot.body}</div> : null}
      </div>
    </>}
    <Source shot={shot} light/>
    <div style={{position: 'absolute', bottom: 0, left: 0, height: 3, width: `${Math.min(100, frame / Math.max(1, duration) * 100)}%`, background: p.accent, opacity: .45}}/>
  </AbsoluteFill>;
};
