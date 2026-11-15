export type PaceShot={id:string;from:number;duration:number;beatId:string;part:number;parts:number;text:string;stage:'setup'|'action'|'result'|'reaction'|'outro'};
export type PaceSegment={id:string;from:number;duration:number;text:string;kind:string;headline:string;cueFrame:number;data?:Record<string,unknown>;chapterId?:string;chapterTitle?:string};
export type PacedPlan={fps:number;durationFrames:number;segments:PaceSegment[];shots:PaceShot[];captions:{from:number;end:number;text:string}[];words?:{start:number;end:number;text:string}[]};
export type Context={plan:PacedPlan;s:PaceSegment;shot:PaceShot;f:number;beatFrame:number;u:number};
export const C={paper:'#F4F0E5',ink:'#172F32',green:'#1F806B',mint:'#CCE2D6',gold:'#EFCE4E',red:'#D05B46',blue:'#BDD2DE',muted:'#71807A',line:'#C5CDC0',white:'#FFFDF5'};
export const clamp=(n:number)=>Math.max(0,Math.min(1,n));
export const lerp=(a:number,b:number,t:number)=>a+(b-a)*t;
export const q=(f:number,a:number,b:number)=>{const t=clamp((f-a)/Math.max(1,b-a));return t*t*(3-2*t)};
export const arc=(a:[number,number],b:[number,number],t:number,h=70):[number,number]=>[lerp(a[0],b[0],t),lerp(a[1],b[1],t)-Math.sin(t*Math.PI)*h];
export const num=(c:Context,key:string,fallback=0)=>typeof c.s.data?.[key]==='number'?Number(c.s.data[key]):fallback;
export const action=(c:Context)=>String(c.s.data?.action??'');
export const money=(n:number)=>Math.round(n).toLocaleString('vi-VN');
export const million=(n:number)=>(n/1000000).toLocaleString('vi-VN',{maximumFractionDigits:2});
const clean=(s:string)=>s.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/đ/g,'d').replace(/[^a-z0-9]/g,'');
export const phraseAt=(c:Context,phrases:string|string[],fallback=c.s.cueFrame)=>{
 const ws=(c.plan.words??[]).filter(w=>w.start*c.plan.fps>=c.s.from-1&&w.start*c.plan.fps<c.s.from+c.s.duration);
 for(const phrase of typeof phrases==='string'?[phrases]:phrases){const parts=phrase.split(/\s+/).map(clean);for(let i=0;i<=ws.length-parts.length;i++)if(parts.every((p,j)=>p===clean(ws[i+j].text)))return ws[i].start*c.plan.fps-c.s.from;}
 return fallback;
};
