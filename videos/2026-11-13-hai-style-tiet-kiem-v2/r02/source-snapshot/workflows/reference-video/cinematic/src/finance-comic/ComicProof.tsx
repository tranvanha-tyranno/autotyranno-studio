import React from 'react';
import {useCurrentFrame,interpolate} from 'remotion';
import {CharacterV2,getHandAnchors} from '../finance-cast-v2/CharacterV2';
import type {FinancePlan} from '../finance-demo/types';
const ink='#272631',cream='#f7edce',yellow='#f7ca45',red='#d65643',green='#228469';
const clamp={extrapolateLeft:'clamp',extrapolateRight:'clamp'} as const;
const p=(f:number,s:number,n=18)=>interpolate(f,[s,s+n],[0,1],{...clamp,easing:t=>1-(1-t)**3});
const Text:React.FC<{x:number;y:number;children:React.ReactNode;size?:number;color?:string;anchor?:'start'|'middle'|'end'}>=({x,y,children,size=36,color=ink,anchor='middle'})=><text x={x} y={y} fontSize={size} fill={color} fontWeight={800} textAnchor={anchor}>{children}</text>;
const Bubble:React.FC<{x:number;y:number;width:number;text:string;tail?:'left'|'right';color?:string}>=({x,y,width,text,tail='left',color='#fffdf3'})=><g transform={`translate(${x} ${y})`}><path d={`M26 0 H${width-26} Q${width} 0 ${width} 26 V88 Q${width} 110 ${width-26} 110 H${tail==='left'?100:width-70} L${tail==='left'?57:width-25} 151 L${tail==='left'?65:width-126} 110 H26 Q0 110 0 84 V26 Q0 0 26 0Z`} fill={color} stroke={ink} strokeWidth={5}/><Text x={width/2} y={69} size={39}>{text}</Text></g>;
/** Comic proof uses the original daily→dinner take, with the paper held at rig palm anchors. */
export const ComicProof:React.FC<{plan:FinancePlan}>=({plan})=>{
 const global=useCurrentFrame(),f=global-890;
 const inward=p(f,104,48);const x1=430+inward*180,x2=1490-inward*180;
 const close=p(f,100,40);const scale=1.38-close*.13;
 const reveal=p(f,142,45);const unroll=p(f,170,67);
 const sum=p(f,388,16);const bill=p(f,327,30);
 const speaking=Boolean(plan.words?.some(w=>global/30>=w.start&&global/30<w.end));
 const minhProps={id:1 as const,x:x1,y:935,scale,variant:'comic' as const,pose:(f<102?'shrug':'receive') as 'shrug'|'receive',emotion:(f<102?'thinking':f<388?'thinking':'surprised') as 'thinking'|'surprised',frame:f,speaking:speaking&&f<102,flip:false,gaze:(f<102?'right':'right') as 'right'};
 const lanProps={id:2 as const,x:x2,y:935,scale,variant:'comic' as const,pose:'give' as const,emotion:(f<388?'confident':'happy') as 'confident'|'happy',frame:f,speaking:speaking&&f>=102,flip:true,gaze:'right' as const};
 const a=getHandAnchors(minhProps).right,b=getHandAnchors(lanProps).right;
 const left=Math.min(a.x,b.x)-3,right=Math.max(a.x,b.x)+3,top=(a.y+b.y)/2;
 const middle=(left+right)/2;const width=right-left;
 const height=45+unroll*215;
 const camera=1+p(f,0,40)*.02-p(f,90,30)*.02+p(f,388,18)*.035;
 return <svg viewBox="0 0 1920 1080" width={1920} height={1080} style={{background:cream,fontFamily:'Arial,sans-serif'}}>
 <defs><pattern id="comic-halftone" width={22} height={22} patternUnits="userSpaceOnUse"><circle cx={3} cy={3} r={1.4} fill="#b9ac8a"/></pattern></defs>
 <rect width={1920} height={1080} fill={cream}/><rect width={1920} height={970} fill="url(#comic-halftone)" opacity={.32}/>
 <path d="M0 970Q960 860 1920 970V1080H0Z" fill="#dfd4b8"/>
 <g transform={`translate(960 590) scale(${camera}) translate(-960 -590)`}>
 {f<128&&<g opacity={1-p(f,100,28)}><Bubble x={100} y={50} width={630} text="Mình có mua gì lớn đâu?"/><g transform={`translate(945 ${500-p(f,35,25)*40}) rotate(${-8+p(f,35,25)*8})`}><path d="M-100-60H100V85H-100Q-125 70-125 10Q-125-45-100-60Z" fill={green} stroke={ink} strokeWidth={7}/><path d="M0-12H105V48H0Q-20 18 0-12Z" fill="#1d6a54" stroke={ink} strokeWidth={5}/><circle cx={72} cy={18} r={6} fill={yellow}/><Text x={-8} y={135} size={25}>KHÔNG MUA MÓN LỚN…</Text></g></g>}
 <CharacterV2 {...minhProps}/><CharacterV2 {...lanProps}/>
 {reveal>0&&<g opacity={reveal}>
   <path d={`M${left} ${top-15} L${right} ${top-15} L${right} ${top+height} L${right-14} ${top+height-8} L${right-28} ${top+height} L${right-42} ${top+height-8} L${left} ${top+height}Z`} fill="#fffdf5" stroke={ink} strokeWidth={4}/>
   <path d={`M${left+12} ${top+49}H${right-12}`} stroke="#d8ceaf" strokeWidth={2} strokeDasharray="7 5"/>
   <Text x={middle} y={top+30} size={Math.min(31,width/9)}>CHI THÊM</Text>
   <g opacity={p(f,198,10)}><Text x={middle} y={top+102} size={f>=327?31:Math.min(44,width/7)}>{f>=327?'1.800.000':'60.000₫'}</Text></g>
   <g opacity={p(f,232,14)}><Text x={middle} y={top+148} size={32}>{f>=327?'+ 200.000':'× 30 ngày'}</Text></g>
   <g opacity={p(f,266,12)*(1-sum)}><Text x={middle} y={top+222} size={Math.min(45,width/7)} color={red}>= 1,8 triệu</Text></g>
   {sum>0&&<g opacity={sum}><Text x={middle} y={top+206} size={Math.min(52,width/6)} color={red}>= 2 triệu!</Text><Text x={middle} y={top+245} size={18}>ĐỦ PHẦN TĂNG</Text></g>}
 </g>}
 {bill>0&&<g transform={`translate(${1070+(1-bill)*350} ${270+(1-bill)*-220}) rotate(${(1-bill)*28-4})`} opacity={bill}>
  <path d="M-145-66H145V70L130 59 115 70 100 59H-145Z" fill={yellow} stroke={ink} strokeWidth={5}/><Text x={0} y={-13} size={27}>THÊM MỘT BỮA ĂN</Text><Text x={0} y={38} size={46}>+200.000₫</Text>
  <path d={`M-20 93Q-30 145 ${middle-1070} ${top-270-45}`} fill="none" stroke={ink} strokeWidth={5} strokeDasharray="8 8"/>
 </g>}
 {f>=388&&<g opacity={p(f,388,10)}><path d="M294 356l-26-34M327 340l-3-46M358 352l24-34M1470 355l31-30M1505 388l45-5" stroke={red} strokeWidth={8} strokeLinecap="round"/>
 <Bubble x={92} y={124} width={650} text="Nhỏ từng lần. Hết cả khoản!" color={yellow}/></g>}
 </g>
 <Text x={96} y={1064} size={18} anchor="start" color="#706a57">TRÍCH ĐOẠN THỬ · TÌNH HUỐNG VÀ SỐ TIỀN MINH HỌA</Text>
 </svg>;
};
