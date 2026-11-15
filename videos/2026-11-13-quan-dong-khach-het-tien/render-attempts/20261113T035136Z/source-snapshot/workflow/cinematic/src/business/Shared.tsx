import type {CSSProperties} from 'react';
import {AbsoluteFill, CanvasImage, interpolate, staticFile, useCurrentFrame} from 'remotion';
import {Video} from '@remotion/media';
import type {DirectionImage} from '../directions/types';
import type {BusinessShot, BusinessTheme} from './types';

export const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
export const themes = {
  cream: {paper: '#f3ecdf', ink: '#202824', accent: '#c75131', quiet: '#6a7167', rule: '#d8cdbb', soft: '#e5d6bb'},
  dark: {paper: '#172622', ink: '#f5eddf', accent: '#e5af6c', quiet: '#b2c1b5', rule: '#43554b', soft: '#293d33'},
  warm: {paper: '#b64e32', ink: '#fff3dd', accent: '#f4d091', quiet: '#f2d9c6', rule: '#dca183', soft: '#a4412b'},
} as const;
export const font = 'Bahnschrift,Arial,sans-serif';
export const rise = (frame: number, start = 0, duration = 14) => interpolate(frame, [start, start + duration], [0, 1], {...clamp, easing: t => 1 - (1 - t) ** 3});
export const localCue = (shot: BusinessShot, index: number, fallback: number) => shot.design?.cues?.[index] ?? Math.round(fallback);
export const themeFor = (shot: BusinessShot, fallback: BusinessTheme = 'cream') => themes[shot.design?.theme ?? fallback];

export const Media: React.FC<{image: DirectionImage; duration: number; reverse?: boolean; style?: CSSProperties}> = ({image, duration, reverse, style}) => {
  const frame = useCurrentFrame();
  const [x, y] = image.focus ?? [50, 50];
  const contain = image.fit === 'contain';
  const imageStyle: CSSProperties = {width: '100%', height: '100%', objectFit: contain ? 'contain' : 'cover', objectPosition: `${x}% ${y}%`};
  return <AbsoluteFill style={{overflow: 'hidden', background: '#1b2620', ...style}}>
    {image.mediaType === 'video' ? <Video src={staticFile(image.file)} muted trimBefore={image.trimBeforeFrames ?? 0} style={imageStyle}/> : <CanvasImage src={staticFile(image.file)} style={{...imageStyle, scale: contain ? 1 : interpolate(frame, [0, Math.max(1, duration - 1)], reverse ? [1.065, 1.015] : [1.015, 1.075], clamp), translate: contain ? undefined : `${interpolate(frame, [0, Math.max(1, duration - 1)], reverse ? [-7, 7] : [7, -7], clamp)}px 0`}}/>}
  </AbsoluteFill>;
};

export const Emphasis: React.FC<{text?: string; words?: string[]; color: string}> = ({text = '', words = [], color}) => {
  if (!words.length) return <>{text}</>;
  const escaped = words.filter(Boolean).map(word => word.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'));
  if (!escaped.length) return <>{text}</>;
  const expression = new RegExp(`(${escaped.join('|')})`, 'giu');
  const lookup = new Set(words.map(word => word.toLocaleLowerCase('vi')));
  return <>{text.split(expression).map((piece, index) => lookup.has(piece.toLocaleLowerCase('vi')) ? <span key={index} style={{color}}>{piece}</span> : <span key={index}>{piece}</span>)}</>;
};

export const Header: React.FC<{shot: BusinessShot; light?: boolean; style?: CSSProperties}> = ({shot, light, style}) => {
  const frame = useCurrentFrame();
  const p = themeFor(shot);
  const ink = light ? '#fff4e2' : p.ink;
  return <div style={{position: 'absolute', left: 100, right: 100, top: 76, color: ink, ...style}}>
    {shot.eyebrow ? <div style={{font: '700 20px Arial,sans-serif', letterSpacing: 2.8, color: light ? '#ebc08e' : p.accent, textTransform: 'uppercase', marginBottom: 23}}>{shot.eyebrow}</div> : null}
    {shot.headline ? <div style={{fontFamily: font, fontSize: shot.headline.length > 76 ? 57 : shot.headline.length > 47 ? 67 : 83, lineHeight: 1.09, letterSpacing: -1.4, fontWeight: 700, opacity: rise(frame, 0), translate: `0 ${(1 - rise(frame)) * 25}px`}}><Emphasis text={shot.headline} words={shot.design?.emphasis} color={light ? '#efba7c' : p.accent}/></div> : null}
  </div>;
};

export const Source: React.FC<{shot: BusinessShot; light?: boolean; style?: CSSProperties}> = ({shot, light, style}) => {
  const text = shot.sourceNote ?? [...new Set(shot.images.map(image => image.credit).filter(Boolean))].join(' / ');
  return text ? <div style={{position: 'absolute', left: 100, right: 100, bottom: 153, color: light ? '#e0e7dc' : themeFor(shot).quiet, font: '17px Arial,sans-serif', lineHeight: 1.3, opacity: .82, overflowWrap: 'anywhere', ...style}}>{text}</div> : null;
};
