import type {DirectionImage} from '../directions/types';
import type {BusinessChart, BusinessTheme} from '../business/types';

export type ChinaNode = {id: string; label: string; lon: number; lat: number; value?: number; color?: string};
export type ChinaDesign = {
  theme?: BusinessTheme;
  cues?: number[];
  emphasis?: string[];
  chart?: BusinessChart & {min?: number; series?: {label: string; color?: string; items: {label: string; value: number; x?: number}[]}[]};
  map?: {mode: 'regions' | 'routes'; nodes: ChinaNode[]; links?: {from: string; to: string; value?: number; label?: string}[]; note?: string};
  /** Link values set explanatory ribbon widths only when explicitly stated. */
  flow?: {nodes: {id: string; label: string; value?: number; column?: number}[];
    links: {from: string; to: string; value: number; label?: string}[]; unit?: string; note?: string};
  simulation?: {kind: 'factory' | 'household' | 'property' | 'cohorts';
    items: {label: string; value: number; color?: string}[]; unit?: string; note?: string};
  comparison?: {columns: {label: string; title: string; body?: string; value?: string}[];
    rows?: {label: string; values: string[]}[]; note?: string};
};
export type ChinaShot = {
  id?: string; start: number; end: number;
  phase: 'hook' | 'disclaimer' | 'content' | 'cta';
  layout: 'c-map' | 'c-flow' | 'c-chart' | 'c-sim' | 'c-compare' | 'c-photo' | 'c-question' | 'c-closing';
  images: DirectionImage[];
  eyebrow?: string; headline?: string; body?: string; sourceNote?: string;
  design?: ChinaDesign;
};
export type ChinaTimeline = {fps: number; frames: number; title: string; audio: string;
  shots: ChinaShot[]; captions: {start: number; end: number; text: string}[]};
