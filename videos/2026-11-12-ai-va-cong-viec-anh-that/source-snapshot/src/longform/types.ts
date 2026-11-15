export type Beat={phrase:string;title:string;sub:string;at:number};
export type Chapter={id:string;label:string;kind:string;theme:string;source?:string;text:string;start:number;end:number;beats:Beat[]};
export type Timeline={title:string;seconds:number;fps:number;frames:number;chapters:Chapter[];captions:{start:number;end:number;text:string}[]};
