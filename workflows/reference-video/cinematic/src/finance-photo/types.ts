import type {PacedPlan} from '../finance-pace-flow';

export type PhotoStyle = 'comic' | 'clean';
export type PhotoFocus = string | [number, number] | {x: number; y: number};
export type PhotoAsset = {
  id: string;
  file: string;
  observed?: string | string[];
  focus?: PhotoFocus;
  fit?: 'cover' | 'contain';
  width?: number;
  height?: number;
  [key: string]: unknown;
};
export type PhotoShot = {
  id: string;
  from: number;
  duration: number;
  beatId: string;
  mode: 'photo' | 'simulation';
  assets: string[];
  layout: 'full' | 'split' | 'gallery';
  focus?: PhotoFocus | Record<string, PhotoFocus>;
  caption?: string;
  simulationKind?: string;
};
export type FinancePhotoPlan = PacedPlan & {
  assets: Record<string, PhotoAsset> | PhotoAsset[];
  photoShots: PhotoShot[];
};
export type FinancePhotoProps = {
  plan: FinancePhotoPlan;
  fromFrame?: number;
  frames?: number;
};

export const clamp = (v: number) => Math.min(1, Math.max(0, v));
export const smooth = (v: number) => {const t = clamp(v); return t * t * (3 - 2 * t);};
export const getAsset = (plan: FinancePhotoPlan, id: string): PhotoAsset => {
  const asset = Array.isArray(plan.assets) ? plan.assets.find(v => v.id === id) : plan.assets[id];
  if (!asset?.file) throw new Error(`Photo asset ${id} has no local file in the finance photo catalog.`);
  return asset;
};
export const getPosition = (focus?: PhotoFocus): string => {
  if (typeof focus === 'string') return focus;
  if (!focus) return '50% 50%';
  const xy = Array.isArray(focus) ? focus : [focus.x, focus.y];
  return xy.map(v => `${Math.max(0, Math.min(100, Math.abs(v) <= 1 ? v * 100 : v))}%`).join(' ');
};
