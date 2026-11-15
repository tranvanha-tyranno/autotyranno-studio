import React from 'react';
import {interpolate} from 'remotion';
import type {BreadLabShot} from './types';

export const P = {paper: '#eee9dc', white: '#fffdf5', ink: '#1b2926', quiet: '#65706a', green: '#285e4c', gold: '#b77a30', rust: '#ad4b35', gray: '#8d958b', rule: '#c9cbbd', light: '#dddccf'};
export const font = '"Bread Lab Vietnam", sans-serif';
export const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
export const number = (n: number, digits = 0) => n.toLocaleString('vi-VN', {maximumFractionDigits: digits});
export const money = (n: number) => `${number(n)} đ`;
export const cue = (s: BreadLabShot, i: number, fraction: number) => s.cueFrames?.[i] ?? Math.round(s.duration * fraction);
export const progress = (f: number, start: number, length: number) => interpolate(f, [start, start + Math.max(1, length)], [0, 1], clamp);
export const value = (s: BreadLabShot, key: string, fallback: number) => typeof s.data?.[key] === 'number' ? Number(s.data[key]) : fallback;

export const Bread: React.FC<{x: number; y: number; width?: number; opacity?: number; color?: string}> = ({x, y, width = 120, opacity = 1, color = '#c88c49'}) => <g opacity={opacity} transform={`translate(${x},${y}) scale(${width / 120})`}>
  <path d="M4 40C4 13 26 1 58 5L88 7C108 9 119 22 116 40L113 52C109 63 94 67 73 65L24 63C10 62 3 54 4 40Z" fill={color} stroke={P.ink} strokeWidth={2.5}/>
  <path d="M32 10L23 32M56 9L46 35M80 12L70 37M100 21L92 41" stroke="#f6d49b" strokeWidth={6} strokeLinecap="round"/>
</g>;

export const FlourBag: React.FC<{x: number; y: number; width?: number; color?: string; opacity?: number; label?: string}> = ({x, y, width = 100, color = '#d8bf94', opacity = 1, label}) => <g transform={`translate(${x},${y}) scale(${width / 100})`} opacity={opacity}>
  <path d="M13 8L86 8L81 22L94 113Q94 123 82 124L18 124Q6 123 7 112L19 22Z" fill={color} stroke={P.ink} strokeWidth={2}/>
  <path d="M13 8L86 8M20 23L80 23" stroke={P.ink} strokeWidth={3}/>
  <path d="M50 45V86M50 57Q32 56 33 42Q47 43 50 57M50 70Q69 69 68 55Q55 57 50 70M50 82Q32 82 32 69Q47 69 50 82" fill="none" stroke={P.gold} strokeWidth={3}/>
  {label && <text x={50} y={107} fontSize={13} textAnchor="middle" fontWeight={700} fill={P.ink}>{label}</text>}
</g>;

export const MoneyToken: React.FC<{x: number; y: number; color?: string; opacity?: number}> = ({x, y, color = P.green, opacity = 1}) => <g transform={`translate(${x},${y})`} opacity={opacity}>
  <rect width={60} height={30} rx={3} fill={color} stroke={P.white} strokeWidth={1.3}/>
  <circle cx={30} cy={15} r={9} fill="none" stroke="rgba(255,255,255,.45)"/>
  <text x={30} y={19.5} fontSize={12} fill={P.white} fontWeight={700} textAnchor="middle">500</text>
</g>;

export const Arrow: React.FC<{x1: number; y1: number; x2: number; y2: number; color?: string; dashed?: boolean; opacity?: number}> = ({x1, y1, x2, y2, color = P.quiet, dashed, opacity = 1}) => {
  const angle = Math.atan2(y2 - y1, x2 - x1); const size = 13;
  return <g opacity={opacity}><line x1={x1} y1={y1} x2={x2} y2={y2} stroke={color} strokeWidth={3} strokeDasharray={dashed ? '8 8' : undefined}/><path d={`M${x2 - size * Math.cos(angle - .5)},${y2 - size * Math.sin(angle - .5)}L${x2},${y2}L${x2 - size * Math.cos(angle + .5)},${y2 - size * Math.sin(angle + .5)}`} fill="none" stroke={color} strokeWidth={3}/></g>;
};

export const LabHeading: React.FC<{shot: BreadLabShot; title: string; subtitle?: string}> = ({shot, title, subtitle}) => <>
  <div style={{position: 'absolute', left: 95, top: 60, right: 100, display: 'flex', justifyContent: 'space-between', fontSize: 20, letterSpacing: 1.5, color: P.quiet}}><span>{shot.overlay?.kicker ?? shot.chapterTitle}</span><span>{shot.label ?? 'MÔ HÌNH MINH HỌA'}</span></div>
  <div style={{position: 'absolute', left: 95, top: 109, right: 110, fontSize: 49, lineHeight: 1.2, fontWeight: 700, letterSpacing: -1.2}}>{shot.overlay?.title ?? shot.headline ?? title}</div>
  {subtitle && <div style={{position: 'absolute', left: 98, top: 181, right: 105, fontSize: 25, lineHeight: 1.3, color: P.quiet}}>{subtitle}</div>}
</>;

export const Footer: React.FC<{children: React.ReactNode}> = ({children}) => <div style={{position: 'absolute', left: 98, right: 98, bottom: 47, paddingTop: 18, borderTop: `1px solid ${P.rule}`, fontSize: 21, lineHeight: 1.35, color: P.quiet}}>{children}</div>;

export const Tag: React.FC<{x: number; y: number; children: React.ReactNode; color?: string; size?: number}> = ({x,y,children,color=P.ink,size=28}) => <text x={x} y={y} fill={color} fontSize={size} fontWeight={600}>{children}</text>;
