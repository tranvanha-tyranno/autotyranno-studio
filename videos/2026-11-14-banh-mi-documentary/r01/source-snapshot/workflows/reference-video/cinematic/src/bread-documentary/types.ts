export type BreadGraphicKind = 'cost_stack' | 'price_path' | 'purchasing_power';

export type BreadData = Record<string, number | string | number[] | string[] | boolean | undefined>;

export type BreadShot = {
  id: string;
  /** Absolute frame on the final narration timeline. */
  from: number;
  /** Frames on the final narration timeline; source footage must cover them. */
  duration: number;
  chapterId: string;
  chapterTitle: string;
  /** A graphic is an explanation over its own real moving footage, not a card. */
  media: 'video' | 'graphic';
  /** Local MP4 path relative to Remotion public/, including graphic backplates. */
  file: string;
  /** Seconds into the source MP4. All other timing fields in this interface use frames. */
  sourceStartSeconds: number;
  /** A short editorial point, never a transcription/subtitle. */
  headline?: string;
  /** Optional short large number or relation. Show only when it adds information. */
  emphasis?: string;
  kind?: BreadGraphicKind;
  data?: BreadData;
  /** Frame offsets within THIS shot, taken from the final narration alignment. */
  cueFrames?: number[];
  /** Override graphic placement to protect a face, action or object in the crop. */
  graphicSide?: 'left' | 'right';
  /** Subtle exposure/contrast changes should be source-specific and inspected. */
  exposure?: number;
  /** Small context label such as "Mô hình minh họa"; never automatic captions. */
  label?: string;
};

export type BreadPlan = {
  fps: number;
  durationFrames: number;
  title: string;
  shots: BreadShot[];
  /** A finalized speech-first mix, relative to public/. Empty only for silent proofs. */
  audio: string;
};

export type BreadDocumentaryProps = {
  plan: BreadPlan;
  /** Proof render: absolute source timeline frame where the review starts. */
  startFrame?: number;
  /** Proof render length; omitted for the full plan. */
  frames?: number;
};
