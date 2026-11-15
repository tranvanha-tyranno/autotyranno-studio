export type FinanceSegment = {id:string;from:number;duration:number;text:string;kind:string;speaker:string;visual:string;speechStart?:number;speechEnd?:number};
export type FinancePlan = {durationFrames:number;segments:FinanceSegment[];captions?:Array<{from:number;end:number;text:string}>;words?:Array<{start:number;end:number;text:string}>};
