import React from 'react';

export type EmotionV2='neutral'|'happy'|'worried'|'surprised'|'thinking'|'confident';
export type PoseV2='idle'|'talk'|'point'|'shrug'|'give'|'receive'|'celebrate';
export type VariantV2='toon'|'comic'|'line';
export type CharacterV2Props={id:1|2;x?:number;y?:number;scale?:number;emotion?:EmotionV2;pose?:PoseV2;frame?:number;speaking?:boolean;flip?:boolean;variant?:VariantV2;gaze?:'left'|'center'|'right'};
type Point={x:number;y:number};
type Limb={shoulder:Point;elbow:Point;wrist:Point;angle:number;hand:'open'|'point'|'rest'};
type Palette={ink:string;skin:string;shade:string;blush:string;hair:string;hairLight:string;top:string;under:string;pants:string;sole:string;accent:string;stroke:number;arm:number};
const palette=(variant:VariantV2,id:1|2):Palette=>variant==='toon'?{
 ink:'#252A34',skin:id===1?'#F1C9A9':'#EDBEA1',shade:'#DFA88D',blush:'#D88173',hair:id===1?'#31333E':'#59403A',hairLight:id===1?'#505362':'#7D5950',top:id===1?'#438E85':'#D98873',under:'#FFF1D9',pants:id===1?'#384953':'#49516B',sole:'#282F3C',accent:'#DEB85A',stroke:5.8,arm:26,
}:variant==='comic'?{
 ink:'#22202C',skin:id===1?'#EAC29C':'#E5B293',shade:'#CE9577',blush:'#D8756D',hair:id===1?'#282C42':'#3D2B3F',hairLight:'#6C536E',top:id===1?'#725F9F':'#E0AF45',under:id===1?'#F4BE65':'#F6EEE3',pants:id===1?'#2D344E':'#5D4D72',sole:'#22202C',accent:'#D88165',stroke:7,arm:28,
}:{
 ink:'#374340',skin:id===1?'#E9C7AE':'#DDB398',shade:'#CCA187',blush:'#C68070',hair:id===1?'#3B4546':'#65483C',hairLight:'#8A6F58',top:id===1?'#79917D':'#C6AA86',under:'#F8EDDA',pants:id===1?'#485E59':'#6B756D',sole:'#34443F',accent:'#B47C4B',stroke:3.4,arm:24,
};

const limbPose=(side:-1|1,pose:PoseV2,frame:number):Limb=>{
 const f=Math.sin(frame/13)*2.4;
 const s={x:side*63,y:-298};
 let elbow={x:side*85,y:-230},wrist={x:side*77,y:-179},angle=side*178,hand:Limb['hand']='rest';
 if(pose==='talk'&&side===1){elbow={x:113,y:-250};wrist={x:164,y:-280+f};angle=58;hand='open';}
 if(pose==='point'&&side===1){elbow={x:119,y:-274};wrist={x:163,y:-334+f*.4};angle=42;hand='point';}
 if(pose==='give'&&side===1){elbow={x:86,y:-207};wrist={x:174,y:-185+f*.3};angle=72;hand='open';}
 if(pose==='receive'){
  elbow={x:side*81,y:-216};wrist={x:side*154,y:-185+f*.2};angle=side*68;hand='open';
 }
 if(pose==='shrug'){
  elbow={x:side*113,y:-247};wrist={x:side*153,y:-305+f*.4};angle=side*38;hand='open';
 }
 if(pose==='celebrate'){
  elbow={x:side*120,y:-327};wrist={x:side*128,y:-398+f};angle=side*12;hand='open';
 }
 return {shoulder:s,elbow,wrist,angle,hand};
};
const bodyBob=(frame:number)=>Math.sin(frame/23)*1.1;

/** Global palms, not a guessed prop position. Call with the same props as CharacterV2. */
export const getHandAnchors=(props:CharacterV2Props)=>{
 const {x=0,y=0,scale=1,flip=false,pose='idle',frame=0}=props;
 const sign=flip?-1:1;
 const one=(side:-1|1)=>{
  const p=limbPose(side,pose,frame);
  const a=p.angle*Math.PI/180;
  const palm={x:p.wrist.x+Math.sin(a)*21,y:p.wrist.y-Math.cos(a)*21+bodyBob(frame)};
  return {x:x+sign*scale*palm.x,y:y+scale*palm.y,wristX:x+sign*scale*p.wrist.x,wristY:y+scale*(p.wrist.y+bodyBob(frame)),angle:sign*p.angle,local:palm};
 };
 return {left:one(-1),right:one(1)};
};

const Hand:React.FC<{limb:Limb;p:Palette}>=({limb,p})=><g transform={`translate(${limb.wrist.x},${limb.wrist.y}) rotate(${limb.angle})`}>
 {limb.hand==='rest'?<path d="M-10 4L-12-11Q-16-17-12-22Q-8-25-3-19L1-21Q12-25 17-15L21-5Q19 7 7 10Z" fill={p.skin}/>:limb.hand==='point'?<g>
   <path d="M-11 4L-13-9Q-25-15-20-22Q-16-26-8-17L-6-18-7-49Q-7-58-1-58Q6-58 6-49L7-28Q20-31 24-20L25-9Q22 7 9 10Z" fill={p.skin}/>
   <path d="M8-22L18-18M8-14L18-10" fill="none" strokeWidth={p.stroke*.5}/>
  </g>:<g>
   <path d="M-10 4L-13-10Q-29-16-25-23Q-22-28-17-24L-8-17-10-39Q-11-46-6-47Q0-48 1-40L2-29 1-48Q1-54 7-54Q12-54 12-47L12-29 14-43Q15-50 20-48Q25-47 23-40L21-26 24-35Q27-42 31-38Q35-35 31-28L24-10Q21 6 8 10Z" fill={p.skin}/>
   <path d="M-4-14Q4-20 14-16M3-9Q10-13 17-10" fill="none" stroke={p.shade} strokeWidth="2.2"/>
  </g>}
</g>;

/** Bent elbows use two actual limb segments; wrist and palm positions are exported. */
const Arm:React.FC<{limb:Limb;p:Palette;id:1|2;variant:VariantV2}>=({limb,p,id,variant})=>{
 const {shoulder:s,elbow:e,wrist:w}=limb;
 const skinPath=`M${s.x} ${s.y} Q${e.x} ${e.y-5} ${e.x} ${e.y} L${w.x} ${w.y}`;
 const sleeveEnd=id===1&&variant==='toon'?{x:s.x+(e.x-s.x)*.7,y:s.y+(e.y-s.y)*.7}: {x:e.x+(w.x-e.x)*.55,y:e.y+(w.y-e.y)*.55};
 const sleevePath=`M${s.x} ${s.y} Q${e.x} ${e.y-5} ${e.x} ${e.y} L${sleeveEnd.x} ${sleeveEnd.y}`;
 return <g>
  <path d={skinPath} fill="none" stroke={p.ink} strokeWidth={p.arm+p.stroke*2} strokeLinecap="round" strokeLinejoin="round"/>
  <path d={skinPath} fill="none" stroke={p.skin} strokeWidth={p.arm} strokeLinecap="round" strokeLinejoin="round"/>
  <path d={sleevePath} fill="none" stroke={p.ink} strokeWidth={p.arm+10+p.stroke*2} strokeLinecap="round" strokeLinejoin="round"/>
  <path d={sleevePath} fill="none" stroke={p.top} strokeWidth={p.arm+10} strokeLinecap="round" strokeLinejoin="round"/>
  <Hand limb={limb} p={p}/>
 </g>;
};

const Clothes:React.FC<{p:Palette;id:1|2;variant:VariantV2}>=({p,id,variant})=>{
 const line=variant==='line';
 return <g>
  <path d={id===1?'M-51-145L50-144 48-20 14-19 5-101-9-99-19-20-56-22Z':'M-56-145L47-145 59-24 23-21-1-102-12-101-23-22-61-22Z'} fill={p.pants}/>
  <path d={id===1?'M-56-23L-20-23-12-8Q-17 0-71-2Q-82-7-56-23ZM15-22L48-22 61-9Q68 0 15-1Z':'M-61-24L-24-24-17-8Q-26 1-76-3Q-84-8-61-24ZM23-24L58-27 76-11Q82 0 25-1Z'} fill={p.sole}/>
  {!line&&<path d="M-66-8H-21M23-8H58" fill="none" stroke={p.under} strokeWidth="3"/>}
  <path d={id===1?'M-32-327Q-62-324-72-302L-64-144Q-6-127 61-141L67-291Q68-316 29-328Z':'M-30-327Q-57-330-69-300L-59-219-67-143Q-9-129 62-143L52-221 65-294Q59-323 28-329Z'} fill={p.top}/>
  {variant==='toon'&&id===1&&<g>
   <path d="M-28-327Q0-308 28-327L31-144Q0-137-22-144Z" fill={p.under}/>
   <path d="M-28-327L-44-304-30-291-39-275-25-219M28-327L43-305 30-293 39-275 31-219" fill="none" strokeWidth="3.3"/>
   <path d="M-59-263H-38V-239H-59Z" fill="none" strokeWidth="3"/>
   <circle cx="42" cy="-252" r="2.4" fill={p.ink} stroke="none"/><circle cx="43" cy="-216" r="2.4" fill={p.ink} stroke="none"/>
  </g>}
  {variant==='toon'&&id===2&&<g>
   <path d="M-30-326Q0-307 28-328L19-278-16-277Z" fill={p.under}/>
   <path d="M-31-328L-46-307-23-273-15-284 0-239 13-278 24-269 43-308 28-328" fill="none" strokeWidth="3.6"/>
   <path d="M-58-172Q-2-159 57-172M-47-211H-27M28-211H49" fill="none" strokeWidth="3"/>
  </g>}
  {variant==='comic'&&id===1&&<g>
   <path d="M-25-329L-16-301 23-305 29-329" fill={p.under}/>
   <path d="M-50-277Q-5-262 45-276M-50-263Q-6-249 46-262" stroke={p.under} strokeWidth="7" fill="none"/>
   <path d="M-61-158Q-5-146 56-156" fill="none" strokeWidth="5"/>
  </g>}
  {variant==='comic'&&id===2&&<g>
   <path d="M-29-328L-15-292H17L29-329" fill={p.under}/>
   <path d="M-30-329L-41-305-17-289 0-265 18-289 42-305 29-329M0-265V-146" fill="none" strokeWidth="4"/>
   <path d="M-52-202L-32-190M29-190L51-203" fill="none" strokeWidth="4"/>
   <circle cx="1" cy="-213" r="3" fill={p.under} stroke="none"/>
  </g>}
  {line&&id===1&&<g>
   <path d="M-25-330Q-2-317 26-330L29-305Q1-290-29-305Z" fill={p.top}/>
   <path d="M-53-163Q1-150 54-162M-46-258Q-36-244-39-218M42-245L47-204" fill="none" stroke="#596F5F" strokeWidth="2.3"/>
  </g>}
  {line&&id===2&&<g>
   <path d="M-28-329L-11-281 18-278 28-330" fill={p.under}/>
   <path d="M-29-330L-46-301-22-282-32-268-10-224 21-268 14-283 39-301 28-331M-12-222L-12-147M-48-192H-25M25-192H48" fill="none" strokeWidth="2.5"/>
  </g>}
  <path d="M-21-350L-20-324Q-1-308 22-326L22-351" fill={p.skin}/>
  <path d="M-19-337Q1-325 21-338" fill="none" stroke={p.shade} strokeWidth="3"/>
 </g>;
};

const HairBack:React.FC<{p:Palette;id:1|2;variant:VariantV2}>=({p,id,variant})=>{
 if(id===1)return null;
 if(variant==='toon')return <path d="M-71-411Q-86-505-3-512Q87-506 77-412L89-327Q53-305 34-329L-40-320-85-338Z" fill={p.hair}/>;
 if(variant==='comic')return <path d="M-75-399Q-93-443-73-462Q-84-492-51-502Q-36-529-5-514Q22-534 47-508Q83-510 82-476Q111-461 88-431L77-388Z" fill={p.hair}/>;
 return <g fill={p.hair}><ellipse cx="48" cy="-489" rx="31" ry="29"/><path d="M-67-401Q-87-465-32-487Q38-508 69-455L72-391-55-382Z"/></g>;
};

const HairFront:React.FC<{p:Palette;id:1|2;variant:VariantV2}>=({p,id,variant})=>{
 if(variant==='toon'&&id===1)return <g>
  <path d="M-71-410Q-90-466-46-492Q-16-516 27-497Q77-502 80-457L70-406 58-421 53-449Q9-425-34-445Q-44-429-57-423L-60-397Z" fill={p.hair}/>
  <path d="M-46-466Q-7-490 40-466" fill="none" stroke={p.hairLight} strokeWidth="5"/>
 </g>;
 if(variant==='toon'&&id===2)return <g>
  <path d="M-73-411Q-81-484-24-505Q34-520 70-477Q88-451 73-414L59-434 51-461Q15-439-8-466Q-23-442-58-444L-60-403Z" fill={p.hair}/>
  <path d="M-47-470Q-24-493 6-488M22-488Q45-485 55-465" stroke={p.hairLight} strokeWidth="4.4" fill="none"/>
 </g>;
 if(variant==='comic'&&id===1)return <g>
  <path d="M-74-408Q-99-440-70-459Q-76-485-48-491Q-43-515-12-503Q17-525 37-501Q73-508 76-475Q102-458 76-406L61-426 52-451Q11-432-24-460Q-42-439-61-439L-59-402Z" fill={p.hair}/>
  <path d="M-47-474Q-34-490-15-480M1-486Q20-499 33-482" stroke={p.hairLight} strokeWidth="5" fill="none"/>
 </g>;
 if(variant==='comic'&&id===2)return <g>
  <path d="M-77-410Q-88-440-66-454Q-77-478-50-484Q-40-507-16-490Q6-509 28-490Q56-500 68-474Q89-465 76-433L65-406 54-427 45-452Q19-439-1-460Q-27-437-56-445L-60-403Z" fill={p.hair}/>
  <path d="M-51-467Q-34-482-18-470M0-478Q17-488 29-472M38-469Q48-477 58-462" fill="none" stroke={p.hairLight} strokeWidth="4"/>
 </g>;
 if(id===1)return <g>
  <path d="M-68-405Q-79-456-44-481Q-11-504 29-486Q69-487 72-447L66-407 53-423 48-451Q5-430-28-450Q-42-433-56-432L-57-402Z" fill={p.hair}/>
  <path d="M-46-462Q-7-485 39-463M-37-452Q-9-468 18-457" fill="none" stroke={p.hairLight} strokeWidth="2.5"/>
 </g>;
 return <g>
  <path d="M-67-408Q-82-460-32-486Q24-504 63-460L69-408 53-425 45-451Q9-441-9-463Q-26-439-56-437L-58-404Z" fill={p.hair}/>
  <path d="M-45-463Q-22-484 4-476M16-477Q36-475 48-458" stroke={p.hairLight} strokeWidth="2.5" fill="none"/>
 </g>;
};

const Face:React.FC<{p:Palette;id:1|2;variant:VariantV2;emotion:EmotionV2;frame:number;speaking:boolean;gaze:'left'|'center'|'right'}>=({p,id,variant,emotion,frame,speaking,gaze})=>{
 const blink=((frame+id*53)%157)<4;
 const isHappy=emotion==='happy',surprise=emotion==='surprised',worry=emotion==='worried',thinking=emotion==='thinking';
 const eyeY=-414;
 const pupilOffset=gaze==='left'?-4:gaze==='right'?4:0;
 const activeMouth=speaking&&Math.floor(frame/4)%4!==0;
 const comic=variant==='comic',line=variant==='line';
 const leftBrow=worry?'M-49-439Q-34-451-17-446':thinking?'M-50-437Q-31-443-16-437':surprise?'M-50-456Q-34-469-17-457':emotion==='confident'?'M-50-448Q-32-459-16-447':'M-49-443Q-31-451-15-440';
 const rightBrow=worry?'M17-446Q34-451 49-439':thinking?'M17-455Q33-471 51-456':surprise?'M17-457Q34-471 50-456':emotion==='confident'?'M17-438Q35-444 50-438':'M17-441Q35-449 50-441';
 return <g>
  <path d={leftBrow} fill="none" stroke={p.hair} strokeWidth={line?4.5:comic?7:6}/><path d={rightBrow} fill="none" stroke={p.hair} strokeWidth={line?4.5:comic?7:6}/>
  {[-32,32].map((cx,i)=><g key={i}>
   {blink||isHappy?<path d={`M${cx-15} ${eyeY+2}Q${cx} ${eyeY+(isHappy?-12:2)} ${cx+14} ${eyeY+1}`} fill="none" strokeWidth={line?3:4.3}/>:<g>
    <path d={surprise?`M${cx-17} ${eyeY}Q${cx-14} ${eyeY-25} ${cx+5} ${eyeY-21}Q${cx+20} ${eyeY-16} ${cx+18} ${eyeY+8}Q${cx} ${eyeY+24} ${cx-17} ${eyeY}Z`:thinking&&i===0?`M${cx-17} ${eyeY-1}Q${cx} ${eyeY-5} ${cx+16} ${eyeY-1}Q${cx} ${eyeY+11} ${cx-17} ${eyeY-1}Z`:`M${cx-17} ${eyeY-1}Q${cx-6} ${eyeY-15} ${cx+8} ${eyeY-9}Q${cx+15} ${eyeY-5} ${cx+16} ${eyeY+2}Q${cx} ${eyeY+15} ${cx-17} ${eyeY-1}Z`} fill="#FFF9EF" strokeWidth={line?2.5:3.4}/>
    <ellipse cx={cx+pupilOffset} cy={eyeY+(thinking&&i===0?3:0)} rx={line?6:7.3} ry={surprise?12:thinking&&i===0?5:8.5} fill={p.ink} stroke="none"/>
    <circle cx={cx+pupilOffset-2.2} cy={eyeY+(thinking&&i===0?1:-3.8)} r={line?1.7:2.5} fill="#FFFDF5" stroke="none"/>
    <path d={thinking&&i===0?`M${cx-17} ${eyeY-1}Q${cx} ${eyeY-5} ${cx+16} ${eyeY-1}`:`M${cx-17} ${eyeY-1}Q${cx-6} ${eyeY-15} ${cx+8} ${eyeY-9}`} fill="none" strokeWidth={line?2.8:4}/>
   </g>}
   {line&&<path d={`M${cx-11} ${eyeY+15}Q${cx} ${eyeY+19} ${cx+10} ${eyeY+15}`} fill="none" stroke={p.shade} strokeWidth="2"/>}
  </g>)}
  <path d={line?'M-2-415L-8-390Q-5-385 3-388L7-391':'M-2-414Q-1-403-8-393Q-6-386 5-389L9-392'} fill="none" stroke={line?p.ink:p.shade} strokeWidth={line?2.8:3.8}/>
  <ellipse cx="-50" cy="-389" rx="14" ry="7" fill={p.blush} stroke="none" opacity={line?.1:.22}/><ellipse cx="49" cy="-389" rx="14" ry="7" fill={p.blush} stroke="none" opacity={line?.1:.22}/>
  {activeMouth?<g>
   <path d="M-20-374Q0-380 21-374Q18-347 0-346Q-17-347-20-374Z" fill="#70464B" strokeWidth={line?2.3:3.5}/>
   <path d="M-14-372Q0-375 15-372L12-365H-11Z" fill="#FFF9EC" stroke="none"/>
   <path d="M-8-352Q0-358 9-351" fill="none" stroke="#D58B8C" strokeWidth="4"/>
  </g>:surprise?<g><path d="M-18-375Q1-389 20-373L18-352Q1-337-17-352Z" fill="#70464B" strokeWidth={line?2.5:3.6}/><path d="M-10-371Q0-376 12-371" stroke="#FFF7E7" strokeWidth="5" fill="none"/></g>:worry?<path d="M-18-361Q1-374 20-363" fill="none" strokeWidth={line?2.8:4}/>:thinking?<path d="M-13-364Q0-362 16-369" fill="none" strokeWidth={line?2.8:4}/>:isHappy?<g><path d="M-23-374Q0-346 24-374" fill="#FFF3DF" strokeWidth={line?2.8:4}/><path d="M-11-352Q0-348 10-352" fill="none" stroke={p.shade} strokeWidth="2.3"/></g>:<path d="M-20-368Q-2-356 20-371" fill="none" strokeWidth={line?2.8:4}/>}
  {id===1&&!comic&&<g stroke={p.hair} strokeWidth={line?1.5:2} opacity=".26"><path d="M-34-367L-31-362M-29-357L-26-353M-20-349L-17-345M17-346L20-350M29-354L32-359M36-364L38-368M-5-341L-4-338M6-340L8-338"/></g>}
  {id===2&&<g fill={p.accent} strokeWidth={line?2.3:3}><circle cx="-72" cy="-394" r={line?7:6}/><circle cx="72" cy="-394" r={line?7:6}/></g>}
 </g>;
};

export const CharacterV2:React.FC<CharacterV2Props>=({id,x=0,y=0,scale=1,emotion='neutral',pose='idle',frame=0,speaking=false,flip=false,variant='comic',gaze=id===1?'right':'left'})=>{
 const p=palette(variant,id);
 const headTilt=emotion==='thinking'?(id===1?-6:6):emotion==='surprised'?(id===1?-4:4):emotion==='worried'?(id===1?3:-3):pose==='talk'?Math.sin(frame/25)*1.2:0;
 const headScale=variant==='comic'?1.06:variant==='line'?.9:1;
 const jaw=id===1?'M-70-435Q-69-484 0-487Q70-482 70-431L64-388Q57-345 9-331Q-36-331-59-372Z':'M-70-432Q-66-482 0-486Q68-483 71-429L63-386Q51-343 0-332Q-49-340-63-383Z';
 return <g transform={`translate(${x},${y}) scale(${flip?-scale:scale},${scale})`} stroke={p.ink} strokeWidth={p.stroke} strokeLinecap="round" strokeLinejoin="round">
  <ellipse cx="0" cy="0" rx="92" ry="11" fill={p.ink} stroke="none" opacity=".11"/>
  <g transform={`translate(0,${bodyBob(frame)})`}>
   <HairBack p={p} id={id} variant={variant}/>
   <Clothes p={p} id={id} variant={variant}/>
   <Arm limb={limbPose(-1,pose,frame)} p={p} id={id} variant={variant}/>
   <Arm limb={limbPose(1,pose,frame)} p={p} id={id} variant={variant}/>
   <g transform={`translate(0,-334) scale(${headScale}) translate(0,334) rotate(${headTilt},0,-398)`}>
    <path d="M-68-424Q-86-434-84-410Q-82-391-67-393M68-424Q85-432 84-411Q82-391 68-394" fill={p.skin}/>
    <path d={jaw} fill={p.skin}/>
    <path d={id===1?'M53-448Q65-421 58-393Q45-356 8-341':'M56-445Q65-416 57-390Q44-356 6-341'} fill="none" stroke={p.shade} strokeWidth={variant==='line'?5:9} opacity=".36"/>
    <HairFront p={p} id={id} variant={variant}/>
    <Face p={p} id={id} variant={variant} emotion={emotion} frame={frame} speaking={speaking} gaze={gaze}/>
   </g>
  </g>
 </g>;
};
