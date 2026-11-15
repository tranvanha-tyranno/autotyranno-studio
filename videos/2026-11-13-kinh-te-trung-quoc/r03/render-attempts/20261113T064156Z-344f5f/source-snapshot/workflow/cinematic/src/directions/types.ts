export type DirectionName = 'long' | 'hidden';

export type DirectionImage = {
  /** Relative to Remotion public/. Keep attribution receipts outside the render. */
  file: string;
  credit: string;
  /** Source width / source height; portraits are preserved rather than stretched. */
  aspect?: number;
  /** Horizontal/vertical focal point, in percent. */
  focus?: [number, number];
  /** Optional inspected moving footage; original speed, no silent looping. */
  mediaType?: 'image' | 'video';
  trimBeforeFrames?: number;
  availableFrames?: number;
  /** Static inspected poster used when a clip appears on a 3D photo plane. */
  posterFile?: string;
  /** Preserve the complete graphic/text when a panel has a different aspect. */
  fit?: 'contain' | 'cover';
};

/** Original explanatory geometry; opt-in so reviewed photo layouts stay intact. */
export type ShoppingMotion = {
  kind: 'basket' | 'price' | 'journey';
  /** The same hypothetical arithmetic, emphasizing unit cost or extra spending. */
  stage?: 'unit' | 'total';
  /** Up to three exact-narration cues, in frames local to this shot. */
  revealFrames?: number[];
};

export type DirectionShot = {
  start: number;
  end: number;
  phase: 'hook' | 'disclaimer' | 'content' | 'cta';
  layout: 'full' | 'diptych' | 'gallery3d' | 'evidence' | 'closing' | 'graphic' | 'object3d';
  images: DirectionImage[];
  motion?: ShoppingMotion;
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
