import React from 'react';
import {interpolate, useCurrentFrame} from 'remotion';
import {clamp, palette as P} from './theme';
import type {BreadShot} from './types';

/** A signpost lives over the actual establishing action. No chapter card/cutaway. */
export const ChapterSignpost: React.FC<{title: string; index: number; duration: number}> = ({title, index, duration}) => {
  const frame = useCurrentFrame();
  const end = Math.min(duration - 1, 104);
  if (end < 15 || frame >= end) return null;
  return <div style={{position: 'absolute', top: 78, left: 100, maxWidth: 1180, color: P.white,
    opacity: interpolate(frame, [0, 6, end - 7, end], [0, 1, 1, 0], clamp),
    translate: `0 ${interpolate(frame, [0, 13], [12, 0], clamp)}px`,
    textShadow: '0 2px 18px rgba(0,0,0,.7)'}}>
    <div style={{display: 'flex', alignItems: 'center', gap: 19}}>
      <div style={{width: 42, height: 3, background: P.warm}}/>
      <div style={{fontSize: 21, fontWeight: 600, letterSpacing: 4, color: P.warm}}>PHẦN {String(index + 1).padStart(2, '0')}</div>
    </div>
    <div style={{fontSize: title.length > 44 ? 42 : 51, lineHeight: 1.24, fontWeight: 600, marginTop: 15}}>{title}</div>
  </div>;
};

/** Optional emphasis has a defined reading window, and clears to let the action lead. */
export const EditorialPoint: React.FC<{shot: BreadShot}> = ({shot}) => {
  const frame = useCurrentFrame();
  if (!shot.headline && !shot.emphasis) return null;
  const first = shot.cueFrames?.[0] ?? Math.min(14, Math.floor(shot.duration * .1));
  const end = Math.min(shot.duration - 1, first + 135);
  if (end - first < 16 || frame < first || frame >= end) return null;
  return <div style={{position: 'absolute', left: 102, right: 150, bottom: 106,
    opacity: interpolate(frame, [first, first + 6, end - 6, end], [0, 1, 1, 0], clamp),
    translate: `0 ${interpolate(frame, [first, first + 13], [16, 0], clamp)}px`, color: P.white,
    textShadow: '0 3px 28px rgba(0,0,0,.65)'}}>
    {shot.emphasis && <div style={{fontSize: shot.emphasis.length > 24 ? 77 : 118, lineHeight: 1.12, fontWeight: 700, letterSpacing: -3, maxWidth: 1550}}>{shot.emphasis}</div>}
    {shot.headline && <div style={{fontSize: shot.emphasis ? 37 : shot.headline.length > 70 ? 51 : 65, maxWidth: 1370, lineHeight: 1.24, fontWeight: 600, marginTop: shot.emphasis ? 20 : 0}}>{shot.headline}</div>}
    {shot.label && <div style={{fontSize: 21, color: P.quiet, marginTop: 18}}>{shot.label}</div>}
  </div>;
};
