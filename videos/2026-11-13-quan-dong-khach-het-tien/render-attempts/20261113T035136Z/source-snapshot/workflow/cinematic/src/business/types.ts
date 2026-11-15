import type {DirectionImage} from '../directions/types';

export type BusinessTheme = 'cream' | 'dark' | 'warm';
export type BusinessChart = {
  kind: 'bars' | 'waterfall' | 'line' | 'breakeven';
  items: {label: string; value: number; x?: number; color?: string}[];
  unit?: string;
  max?: number;
  /** A marked vertical value for bars/line, or fixed cost for breakeven. */
  target?: number;
  highlight?: number;
  /** Fixed cost, in the same units as items[].value. */
  fixed?: number;
  xLabel?: string;
};
export type BusinessDesign = {
  theme?: BusinessTheme;
  /** Exact-take cue frames, relative to this shot. */
  cues?: number[];
  emphasis?: string[];
  chart?: BusinessChart;
  paper?: {title?: string; rows: {label: string; value: string}[];
    total?: {label: string; value: string}};
  choices?: {label: string; title: string; body?: string}[];
  coffee?: {kind: 'cup' | 'cost' | 'flow'};
};
export type BusinessShot = {
  id?: string;
  start: number;
  end: number;
  phase: 'hook' | 'disclaimer' | 'content' | 'cta';
  layout: 'b-photo' | 'b-paper' | 'b-question' | 'b-chart' | 'b-split' | 'b-coffee' | 'b-closing';
  images: DirectionImage[];
  eyebrow?: string;
  headline?: string;
  body?: string;
  sourceNote?: string;
  design?: BusinessDesign;
};
export type BusinessTimeline = {
  fps: number;
  frames: number;
  title: string;
  audio: string;
  shots: BusinessShot[];
  captions: {start: number; end: number; text: string}[];
};
