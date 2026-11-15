import {Easing, interpolate} from 'remotion';
import type {FinancePlan, FinanceSegment} from '../finance-demo/types';

export const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
export const ease = Easing.bezier(.35, 0, .2, 1);
export const p = (f:number,a:number,b:number) => interpolate(f,[a,Math.max(a+1,b)],[0,1],{...clamp,easing:ease});
export const lerp = (a:number,b:number,t:number) => a+(b-a)*t;
export const arc = (a:[number,number],b:[number,number],t:number,height=100):[number,number] => [lerp(a[0],b[0],t),lerp(a[1],b[1],t)-Math.sin(Math.PI*t)*height];
const clean=(s:string)=>s.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/đ/g,'d').replace(/[^a-z0-9]/g,'');

/** Character alignment is stored in seconds while plan scene positions are frames.
 * Never infer speaking speed from text length when exact-take words are available. */
export const cue=(plan:FinancePlan,s:FinanceSegment,phrase:string,fallback:number,end=false)=>{
  const source=(plan.words??[]).filter(w=>w.start*30>=s.from-2&&w.start*30<s.from+s.duration);
  const wanted=phrase.split(/\s+/).map(clean).filter(Boolean);
  for(let i=0;i<=source.length-wanted.length;i++) {
    if(wanted.every((w,j)=>clean(source[i+j].text)===w)) {
      const word=end?source[i+wanted.length-1]:source[i];
      return Math.max(0,(end?word.end:word.start)*30-s.from);
    }
  }
  return fallback;
};

export const money=(value:number)=>Math.round(value).toLocaleString('vi-VN');
