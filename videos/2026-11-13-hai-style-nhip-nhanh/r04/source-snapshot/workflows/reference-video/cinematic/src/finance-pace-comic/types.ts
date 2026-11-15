export type Beat={id:string;from:number;duration:number;text:string;kind:string;headline:string;cueFrame:number;data?:Record<string,unknown>;chapterId?:string;chapterTitle?:string};
export type Shot={id:string;from:number;duration:number;beatId:string;part:number;parts:number;text:string;stage:'setup'|'action'|'result'|'reaction'|'outro';theme?:string};
export type PacedPlan={fps:number;durationFrames:number;segments:Beat[];shots:Shot[];captions:{from:number;end:number;text:string}[];words?:{text:string;start:number;end:number}[]};
export type Ctx={plan:PacedPlan;b:Beat;s:Shot;f:number;d:number;i:number;t:number};
