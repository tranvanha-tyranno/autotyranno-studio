export type SemanticDirection = "long" | "hidden";
export type SemanticScene =
  | "email_prompt"
  | "email_draft"
  | "wrong_claim"
  | "customer_reply"
  | "product_facts"
  | "source_check"
  | "tone_edit"
  | "feedback"
  | "task_map"
  | "send_gate"
  | "time_log"
  | "quality_compare"
  | "work_role"
  | "decision"
  | "trial"
  | "comment_cta"
  | "subscribe"
  | "disclaimer"
  | "intro"
  | "goal"
  | "review_work"
  | "context"
  | "quality_gate";
export type SemanticAsset = {
  file: string;
  aspect?: number;
  focus?: [number, number];
  credit?: string;
};
export type SemanticShot = {
  start: number;
  end: number;
  phase: "hook" | "disclaimer" | "content" | "cta";
  scene: SemanticScene;
  mode?: string;
  headline?: string;
  detail?: string;
  asset?: SemanticAsset;
  visible: string[];
  proof: string;
  phrase: string;
  continuityGroup?: string;
  continuityStart?: number;
  /** Optional paired media, only if both show the stated operation. */
  assets?: SemanticAsset[];
};
export type SemanticExample = {
  productName: string;
  sourceFeature: string;
  unsupportedFeature: string;
  sourcePriceVND: number;
  draftPriceVND: number;
  baselineMinutes: number;
  writeMinutes: number;
  repairMinutes: number;
};
export type SemanticTimeline = {
  direction: SemanticDirection;
  fps: number;
  frames: number;
  audio: string;
  title: string;
  captions: { start: number; end: number; text: string }[];
  shots: SemanticShot[];
  example?: Partial<SemanticExample>;
};
