import type {BreadShot} from '../bread-documentary/types';

export type BreadSimulation = 'money_split' | 'price_level' | 'inventory' | 'cost_ledger' | 'competition' | 'bread_power' | 'basket_scope' | 'synthesis';
export type BreadLabShot = Omit<BreadShot, 'file' | 'media'> & {
  media: 'video' | 'graphic' | 'simulation';
  /** Required for video interludes; optional real footage inset in lab scenes. */
  file?: string;
  simulation?: BreadSimulation;
  narrationId?: string;
  narrationUnit?: string;
  overlay?: {title: string; kicker?: string; items?: string[]};
};
export type BreadLabPlan = {fps: number; durationFrames: number; title: string; shots: BreadLabShot[]; audio: string};
export type BreadLabProps = {plan: BreadLabPlan; startFrame?: number; frames?: number};
