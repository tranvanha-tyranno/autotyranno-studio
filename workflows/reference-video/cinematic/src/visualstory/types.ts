import type {Chapter,Timeline} from '../longform/types';
export type Shot={asset:string;type:string;file:string;start:number;end:number;phrase:string;purpose:string;pan:number;focus:number[];aspect:number};
export type VisualChapter=Chapter&{shots:Shot[]};
export type VisualTimeline=Omit<Timeline,'chapters'>&{chapters:VisualChapter[]};
