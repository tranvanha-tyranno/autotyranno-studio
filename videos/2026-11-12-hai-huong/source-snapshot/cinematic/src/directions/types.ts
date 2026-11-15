export type DirectionName = 'long' | 'hidden';

export type DirectionImage = {
  /** Relative to Remotion public/. Keep attribution receipts outside the render. */
  file: string;
  credit: string;
  /** Source width / source height; portraits are preserved rather than stretched. */
  aspect?: number;
  /** Horizontal/vertical focal point, in percent. */
  focus?: [number, number];
};

export type DirectionShot = {
  start: number;
  end: number;
  phase: 'hook' | 'disclaimer' | 'content' | 'cta';
  layout: 'full' | 'diptych' | 'gallery3d' | 'evidence' | 'closing';
  images: DirectionImage[];
  eyebrow?: string;
  headline?: string;
  body?: string;
  sourceNote?: string;
};

export type DirectionTimeline = {
  direction: DirectionName;
  fps: number;
  frames: number;
  title: string;
  audio: string;
  shots: DirectionShot[];
  /** Exact narration take timing, in seconds. */
  captions: {start: number; end: number; text: string}[];
};
