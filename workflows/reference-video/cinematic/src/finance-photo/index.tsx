import React from 'react';
import {AbsoluteFill, Sequence, useCurrentFrame} from 'remotion';
import {ComicPacedFilm} from '../finance-pace-comic';
import {FlowPacedFilm} from '../finance-pace-flow';
import {CaptionTrack, ContextOverlay, SubscribeOverlay} from './Overlays';
import {PhotoStage} from './PhotoStage';
import {smooth, type FinancePhotoPlan, type FinancePhotoProps, type PhotoShot, type PhotoStyle} from './types';
export type {FinancePhotoPlan, FinancePhotoProps, PhotoAsset, PhotoShot, PhotoStyle} from './types';

const TimelineFilm: React.FC<{plan: FinancePhotoPlan; style: PhotoStyle}> = ({plan, style}) => {
  const frame = useCurrentFrame();
  const index = plan.photoShots.findIndex(v => frame >= v.from && frame < v.from + v.duration);
  const shot = plan.photoShots[index];
  if (!shot) return <AbsoluteFill style={{backgroundColor: '#101c20'}}/>;
  const previous = plan.photoShots[index - 1];
  const segment = plan.segments.find(v => v.id === shot.beatId);
  const entering = index > 0 ? smooth((frame - shot.from) / 6) : 1;
  const paint = (s: PhotoShot, i: number, f: number) => s.mode === 'simulation'
    ? (style === 'comic' ? <ComicPacedFilm plan={plan}/> : <FlowPacedFilm plan={plan}/>)
    : <PhotoStage shot={s} plan={plan} frame={f} index={i} style={style}/>;
  return <AbsoluteFill style={{backgroundColor: '#101c20', fontFamily: 'Arial, sans-serif'}}>
    {entering < 1 && previous?.mode === 'photo' && <AbsoluteFill>{paint(previous, index - 1, previous.from + previous.duration - 1)}</AbsoluteFill>}
    <AbsoluteFill style={{opacity: entering}}>{paint(shot, index, frame)}</AbsoluteFill>
    {shot.mode === 'photo' && <><ContextOverlay shot={shot} frame={frame} style={style} disclaimer={segment?.kind === 'disclaimer'}/><SubscribeOverlay plan={plan} frame={frame} style={style}/></>}
    <CaptionTrack plan={plan} frame={frame}/>
  </AbsoluteFill>;
};

/** Exact-take timing remains global even when rendering a bounded proof interval.
 * Photographs are real source assets; pans do not turn still photos into footage.
 * Original illustrations are mounted only for explicitly selected simulation shots.
 */
export const FinancePhotoFilm: React.FC<FinancePhotoProps & {style: PhotoStyle}> = ({plan, style, fromFrame = 0}) => <Sequence from={-fromFrame} durationInFrames={plan.durationFrames}><TimelineFilm plan={plan} style={style}/></Sequence>;
export const FinancePhotoComic: React.FC<FinancePhotoProps> = props => <FinancePhotoFilm {...props} style="comic"/>;
export const FinancePhotoClean: React.FC<FinancePhotoProps> = props => <FinancePhotoFilm {...props} style="clean"/>;
