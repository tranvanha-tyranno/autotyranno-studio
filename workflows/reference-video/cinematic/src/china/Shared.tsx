import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {Emphasis, font, rise, themes} from '../business/Shared';
import type {ChinaShot} from './types';

export {font, rise, themes};
export const colorFor = (shot: ChinaShot) => themes[shot.design?.theme ?? 'cream'];
export const cue = (shot: ChinaShot, index: number, fallback: number) => shot.design?.cues?.[index] ?? Math.round(fallback);
export const number = (value: number, digits = 1) => new Intl.NumberFormat('vi-VN', {maximumFractionDigits: digits}).format(value);

export const Frame: React.FC<{shot: ChinaShot; children: React.ReactNode; note?: string}> = ({shot, children, note}) => {
  const frame = useCurrentFrame();
  const p = colorFor(shot);
  return <AbsoluteFill style={{background: p.paper, color: p.ink, overflow: 'hidden'}}>
    <div style={{position: 'absolute', left: 100, right: 100, top: 65}}>
      {shot.eyebrow ? <div style={{font: '700 19px Arial,sans-serif', letterSpacing: 2.8, color: p.accent, marginBottom: 19, textTransform: 'uppercase'}}>{shot.eyebrow}</div> : null}
      {shot.headline ? <div style={{fontFamily: font, fontSize: shot.headline.length > 76 ? 59 : shot.headline.length > 49 ? 70 : 84, lineHeight: 1.09, letterSpacing: -1.4, fontWeight: 700, opacity: rise(frame), translate: `0 ${(1 - rise(frame)) * 23}px`}}><Emphasis text={shot.headline} words={shot.design?.emphasis} color={p.accent}/></div> : null}
    </div>
    {children}
    {shot.body ? <div style={{position: 'absolute', left: 150, right: 150, top: 850, textAlign: 'center', font: '29px Arial,sans-serif', lineHeight: 1.35, color: p.quiet}}>{shot.body}</div> : null}
    {note ? <div style={{position: 'absolute', left: 100, right: 100, bottom: 178, font: '18px Arial,sans-serif', lineHeight: 1.3, color: p.quiet}}>{note}</div> : null}
    {shot.sourceNote ? <div style={{position: 'absolute', left: 100, right: 100, bottom: 144, font: '17px Arial,sans-serif', lineHeight: 1.28, color: p.quiet, opacity: .85}}>{shot.sourceNote}</div> : null}
  </AbsoluteFill>;
};

export const Lines: React.FC<{text: string; x: number; y: number; width?: number; size?: number; color: string; weight?: number}> = ({text, x, y, width = 20, size = 29, color, weight = 400}) => {
  const words = text.split(' ');
  const lines: string[] = [];
  for (const word of words) {
    const last = lines.length - 1;
    if (last < 0 || lines[last].length + word.length + 1 > width) lines.push(word);
    else lines[last] += ' ' + word;
  }
  return <text x={x} y={y} textAnchor="middle" fill={color} fontFamily="Arial,sans-serif" fontSize={size} fontWeight={weight}>{lines.map((line, i) => <tspan key={`${line}-${i}`} x={x} dy={i ? size * 1.18 : 0}>{line}</tspan>)}</text>;
};
