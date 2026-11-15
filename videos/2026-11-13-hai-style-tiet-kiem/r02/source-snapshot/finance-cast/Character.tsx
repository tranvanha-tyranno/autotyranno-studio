import React from 'react';
import {getCharacter, type CastMember} from './roster';

export type Emotion = 'neutral'|'happy'|'worried'|'surprised'|'thinking'|'confident';
export type Pose = 'idle'|'talk'|'point'|'shrug'|'give'|'receive'|'celebrate';
export type CharacterProps = {id:number;x?:number;y?:number;scale?:number;emotion?:Emotion;pose?:Pose;frame?:number;speaking?:boolean;flip?:boolean};
const ink='#252832';

const HairBack:React.FC<{c:CastMember}> = ({c}) => {
  if(c.hair==='long') return <path d="M-65-340Q-91-431-12-429Q75-441 78-343L91-229Q43-207 26-230L-39-221-85-247Z" fill={c.hairColor}/>;
  if(c.hair==='bob') return <path d="M-74-322Q-90-422-6-430Q83-429 78-320L82-287Q61-270 42-289H-49Q-73-281-82-298Z" fill={c.hairColor}/>;
  if(c.hair==='braid') return <g fill={c.hairColor}><path d="M-69-341Q-78-428 0-431Q82-428 72-338Z"/>{[0,1,2,3,4].map(i=><ellipse key={i} cx={65+i*2} cy={-306+i*24} rx={17-i} ry="19"/>)}<path d="M68-191L58-165H84Z"/></g>;
  if(c.hair==='pigtail') return <g fill={c.hairColor}><path d="M-70-340Q-87-422 0-428Q84-424 72-341Z"/><path d="M-62-364Q-127-375-111-307Q-118-278-87-264L-66-321Z"/><path d="M62-364Q127-375 111-307Q118-278 87-264L66-321Z"/><path d="M-97-316l26-6M97-316l-26-6" stroke={c.accent} strokeWidth="9"/></g>;
  return null;
};

const HairFront:React.FC<{c:CastMember}> = ({c})=>{
 const color=c.hairColor;
 switch(c.hair){
 case 'side': return <path d="M-64-342Q-81-407-30-424Q11-443 55-413Q77-398 65-348L49-371Q46-386 35-385Q-7-368-45-383L-51-346Z" fill={color}/>;
 case 'bob': return <path d="M-67-359Q-83-427-1-430Q77-427 69-361L48-384Q12-380-12-398Q-21-378-57-379L-60-353Z" fill={color}/>;
 case 'curly': return <g fill={color}>{[-57,-30,0,30,57].map((v,i)=><circle key={i} cx={v} cy={-399-(i%2)*14} r="26"/>)}<path d="M-75-389Q-86-364-61-344L-51-380H53L61-344Q86-369 72-393Z"/></g>;
 case 'bun': return <g fill={color}><circle cx="6" cy="-449" r="34"/><path d="M-65-355Q-87-422 0-429Q81-423 66-352L52-383Q16-379-19-399Q-30-378-59-378Z"/><path d="M-13-426Q10-415 33-429" fill="none" stroke={c.accent} strokeWidth="8"/></g>;
 case 'crop': return <path d="M-63-363L-66-395Q-43-431 12-425Q62-426 66-386L62-359-49-383Z" fill={color}/>;
 case 'quiff': return <path d="M-65-352Q-81-392-49-414Q-53-440-25-449Q-11-417 23-433Q67-437 70-403Q77-374 64-350L50-383Q2-369-43-389L-51-350Z" fill={color}/>;
 case 'long': return <path d="M-66-355Q-78-425-1-429Q72-430 67-357L55-382Q6-373-12-403Q-28-381-59-378Z" fill={color}/>;
 case 'afro': return <g fill={color}>{[[-68,-392],[-55,-425],[-22,-442],[16,-442],[51,-424],[72,-391],[-72,-356],[73,-357]].map(([cx,cy],i)=><circle key={i} cx={cx} cy={cy} r="29"/>)}<path d="M-66-379H65L53-391Q5-377-47-394Z"/></g>;
 case 'bald': return <g fill={color}><path d="M-67-374Q-77-353-61-332L-53-351-55-383Z"/><path d="M67-374Q77-353 61-332L53-351 55-383Z"/><path d="M-21-415Q-10-422 1-418M3-420Q16-426 25-418" fill="none"/></g>;
 case 'pigtail': return <path d="M-64-362Q-78-426 0-430Q78-426 65-363L49-385Q13-378-4-399Q-25-380-55-379Z" fill={color}/>;
 case 'wave': return <path d="M-62-347Q-90-364-72-389Q-78-413-47-420Q-26-444 1-427Q35-443 51-416Q82-414 74-385Q88-359 63-348L47-383Q16-373-8-395Q-25-378-54-380Z" fill={color}/>;
 case 'braid': return <path d="M-64-353Q-78-422 0-430Q76-421 65-353L52-382Q16-382 0-410Q-19-382-53-381Z" fill={color}/>;
 case 'spiky': return <path d="M-65-349L-78-390-53-384-68-419-37-406-25-443-3-414 22-445 29-413 63-430 57-402 82-396 65-347 49-380Q2-370-48-384L-54-348Z" fill={color}/>;
 case 'cap': return <g><path d="M-70-383Q-70-432-10-433Q57-438 67-386Z" fill={c.accent}/><path d="M-81-389Q-11-403 89-387L90-373Q8-384-76-373Z" fill={c.top}/><path d="M-61-368L-55-342M59-370L58-344" stroke={color} strokeWidth="12"/></g>;
 case 'beanie': return <g><path d="M-68-385Q-72-440 0-445Q70-441 70-386Z" fill={c.accent}/><path d="M-73-395Q-4-407 74-395L74-371Q1-381-73-371Z" fill={c.top}/><path d="M-48-400L-48-423M-23-404L-23-432M3-405L3-434M28-404L28-429M51-401L51-421" fill="none" opacity=".3"/></g>;
 }
};

const Face:React.FC<{emotion:Emotion;frame:number;speaking:boolean;c:CastMember}>=({emotion,frame,speaking,c})=>{
 const blink=((frame+c.id*19)%149)<5;
 const mouthOpen = speaking && (Math.floor(frame/3)%5!==0);
 const eyeY=emotion==='surprised'?-353:-350;
 const happy=emotion==='happy';
 return <g>
   <path d={emotion==='worried'?'M-43-367L-17-374M17-374L43-367':emotion==='confident'?'M-43-373L-17-367M17-367L43-373':emotion==='surprised'?'M-43-381Q-29-392-16-380M16-380Q29-392 43-381':emotion==='thinking'?'M-43-369L-17-372M17-378L43-373':'M-43-374Q-29-379-16-373M16-373Q29-379 43-374'} fill="none" stroke={c.hairColor} strokeWidth="5"/>
   {[-28,28].map((x,i)=><g key={i}>{blink||happy?<path d={`M${x-9} ${eyeY+1}Q${x} ${happy?eyeY-8:eyeY+2} ${x+9} ${eyeY+1}`} fill="none"/>:<><ellipse cx={x} cy={eyeY} rx={emotion==='surprised'?10:7} ry={emotion==='surprised'?14:10} fill={ink} stroke="none"/><circle cx={x-2} cy={eyeY-3} r="2.3" fill="#fff" stroke="none"/></>}</g>)}
   <path d="M-2-347L-6-333 2-331" stroke="#AD775E" strokeWidth="3" fill="none"/>
   <ellipse cx="-45" cy="-326" rx="11" ry="5" fill="#EA8F81" stroke="none" opacity=".28"/><ellipse cx="45" cy="-326" rx="11" ry="5" fill="#EA8F81" stroke="none" opacity=".28"/>
   {mouthOpen ? <g><path d={`M-15-316Q0-322 15-316Q13 ${-300+(frame%3)*2} 0 ${-297+(frame%3)*2}Q-13 ${-300+(frame%3)*2}-15-316Z`} fill="#663D42" strokeWidth="3"/><path d="M-9-315H9" stroke="#FFF6E5" strokeWidth="4"/></g> : emotion==='surprised'?<ellipse cx="0" cy="-311" rx="11" ry="15" fill="#663D42" strokeWidth="3"/>: <path d={emotion==='worried'?'M-15-307Q0-319 15-307':emotion==='thinking'?'M-8-310L13-312':emotion==='neutral'?'M-12-311Q0-308 12-311':'M-19-316Q0-295 19-316'} fill="none" strokeWidth="4"/>}
   {(c.accessory==='round-glasses'||c.accessory==='square-glasses') && <g fill="none" strokeWidth="4">{[-28,28].map((x,i)=>c.accessory==='round-glasses'?<circle key={i} cx={x} cy="-350" r="21"/>:<rect key={i} x={x-23} y="-369" width="45" height="36" rx="7"/>)}<path d="M-7-353Q0-359 7-353M-50-355L-64-360M50-355L64-360"/></g>}
   {c.accessory==='moustache'&&<path d="M0-323Q-12-334-28-318Q-14-308 0-319Q14-308 28-318Q12-334 0-323Z" fill={c.hairColor} strokeWidth="2"/>}
   {c.accessory==='beard'&&<path d="M-49-319Q-43-281 0-281Q43-281 49-319L36-307Q16-294 0-300Q-16-294-36-307Z" fill={c.hairColor} strokeWidth="2"/>}
   {c.accessory==='earrings'&&<g fill={c.accent}><circle cx="-69" cy="-328" r="7"/><circle cx="69" cy="-328" r="7"/></g>}
 </g>;
};

const Outfit:React.FC<{c:CastMember;w:number}>=({c,w})=><g>
 <path d={`M${-w+10}-117H${w-10}L${w-13}-27H18L8-91H-8L-18-27H${-w+13}Z`} fill={c.pants}/>
 <path d={`M${-w+14}-30H-17L-14-9H${-w+5}Q${-w-11}-17 ${-w+14}-30ZM17-30H${w-14}Q${w+11}-17 ${w-5}-9H14Z`} fill={ink}/>
 <path d={`M-37-275Q${-w-14}-267 ${-w}-219L${-w+2}-106Q0-94 ${w-2}-106L${w}-219Q${w+14}-267 37-275Z`} fill={c.top}/>
 {c.outfit==='tee'&&<path d="M-31-273Q0-240 31-273" fill="none" strokeWidth="6"/>}
 {c.outfit==='shirt'&&<g><path d="M-32-274L0-253 32-274 21-238 0-253-21-238Z" fill={c.accent}/><path d="M0-248V-109" fill="none" strokeWidth="3"/>{[-225,-195,-165,-135].map(y=><circle key={y} cx="5" cy={y} r="2" fill={ink} stroke="none"/>)}<path d="M22-219H48V-193H22Z" fill="none" strokeWidth="3"/></g>}
 {c.outfit==='blazer'&&<g><path d="M-28-274L0-111 28-274 0-262Z" fill={c.accent}/><path d="M-34-273L-48-237-27-228-39-210 0-139 39-210 27-228 48-237 34-273" fill="none" strokeWidth="4"/><path d="M-8-259L-12-244 0-202 12-244 8-259Z" fill={c.pants} strokeWidth="2"/><path d="M25-174H49M-48-174H-24" strokeWidth="4"/></g>}
 {c.outfit==='apron'&&<g><path d="M-32-268L-30-227H30L32-268M-38-222H38L52-110H-52Z" fill={c.accent}/><path d="M-24-174H24V-145Q0-136-24-145Z" fill={c.top} strokeWidth="3"/></g>}
 {c.outfit==='cardigan'&&<g><path d="M-29-272L-18-107H18L29-272Q0-248-29-272Z" fill={c.accent}/><path d="M-32-270L-18-108M32-270L18-108" fill="none" strokeWidth="4"/><path d="M-51-163H-29M29-163H51" fill="none" strokeWidth="3"/></g>}
 {c.outfit==='hoodie'&&<g><path d="M-37-271Q-53-294-36-300Q0-310 36-300Q53-294 37-271L0-244Z" fill={c.accent}/><path d="M-17-259L-20-220M17-259L20-220" fill="none" strokeWidth="3"/><path d="M-28-161H28L39-130H-39Z" fill="none" strokeWidth="3"/></g>}
 {c.outfit==='vest'&&<g><path d="M-31-273Q0-250 31-273L40-238 34-112H-34L-40-238Z" fill={c.accent}/><path d="M-30-273L0-229 30-273M0-230V-109" fill="none" strokeWidth="4"/><path d="M-23-165H-9M10-165H24" strokeWidth="3"/></g>}
 {c.outfit==='overall'&&<g><path d="M-38-269H-23L-20-219H20L23-269H38L37-214H48V-107H-48V-214H-37Z" fill={c.pants}/><path d="M-25-191H25V-163Q0-151-25-163Z" fill="none" stroke={c.accent} strokeWidth="3"/><circle cx="-30" cy="-222" r="4" fill={c.accent}/><circle cx="30" cy="-222" r="4" fill={c.accent}/></g>}
 {c.outfit==='tunic'&&<g><path d="M-29-273Q0-256 29-273M-47-142Q0-135 47-142" fill="none" stroke={c.accent} strokeWidth="5"/><path d="M-49-109L-54-88H54L49-109" fill={c.top}/></g>}
 {c.outfit==='sweater'&&<g><path d="M-30-276Q0-263 30-276L28-256Q0-242-28-256Z" fill={c.accent}/><path d={`M${-w+6}-121Q0-113 ${w-6}-121`} fill="none" stroke={c.accent} strokeWidth="9"/></g>}
 {c.accessory==='necklace'&&<g fill="none" stroke={c.accent} strokeWidth="4"><path d="M-27-273Q0-210 27-273"/><circle cx="0" cy="-236" r="6" fill={c.accent}/></g>}
 {c.accessory==='scarf'&&<g fill={c.accent}><path d="M-32-280Q0-265 32-280L36-258Q0-245-36-258Z"/><path d="M8-254L31-249 40-197 14-201Z"/></g>}
</g>;

const Arm:React.FC<{side:-1|1;angle:number;c:CastMember;extended?:boolean}>=({side,angle,c,extended=false})=><g transform={`translate(${side*61},-246) rotate(${-side*angle}) scale(${side},1)`}>
 <path d="M0-10Q22-11 23 13L33 57-3 64-16 22Q-23 2 0-10Z" fill={c.top}/>
 <path d="M-3 53L32 48 42 89 15 100Z" fill={c.skin}/>
 {extended?<path d="M18 88Q8 77 10 71Q18 69 24 83L30 92Q49 84 54 97L57 108Q53 117 42 113L41 139Q39 148 33 144L27 118Q15 113 16 100Z" fill={c.skin}/>:<path d="M16 88Q5 77 9 71Q16 69 24 82Q42 72 48 83L55 99Q53 115 34 115Q18 112 16 100Z" fill={c.skin}/>}
 <path d="M33 89L40 103M42 87L48 99" fill="none" strokeWidth="2.5"/>
 {c.accessory==='watch'&&side===-1&&<g><path d="M11 83L36 75" stroke={c.pants} strokeWidth="10"/><circle cx="23" cy="79" r="10" fill={c.accent} strokeWidth="3"/></g>}
</g>;

/** Feet pivot. Idle x ±105; extended gesture x ±210, y -485..0. No CSS timeline. */
export const Character:React.FC<CharacterProps>=({id,x=0,y=0,scale=1,emotion='neutral',pose='idle',frame=0,speaking=false,flip=false})=>{
 const c=getCharacter(id);
 const w=c.build==='broad'?76:c.build==='slim'?58:66;
 const pulse=Math.sin(frame/8+c.id)*3;
 const bob=pose==='celebrate'?Math.abs(Math.sin(frame/7))*-12:Math.sin(frame/17+c.id)*1.5;
 let left=0,right=0;
 if(pose==='talk'){left=8+pulse;right=43+pulse*3;}
 if(pose==='point'){left=5;right=105+pulse;}
 if(pose==='shrug'){left=105+pulse;right=105-pulse;}
 if(pose==='give'){left=5;right=72+pulse;}
 if(pose==='receive'){left=65+pulse;right=65-pulse;}
 if(pose==='celebrate'){left=152+pulse;right=152-pulse;}
 const tilt=emotion==='thinking'?-6:emotion==='worried'?4:pose==='talk'?Math.sin(frame/19)*1.5:0;
 return <g transform={`translate(${x},${y}) scale(${flip?-scale:scale},${scale})`} stroke={ink} strokeWidth="5.5" strokeLinecap="round" strokeLinejoin="round">
  <ellipse cx="0" cy="-4" rx={w+24} ry="11" fill="#253B42" stroke="none" opacity=".12"/>
  <g transform={`translate(0,${bob})`}>
   <HairBack c={c}/><Outfit c={c} w={w}/>
   <path d="M-22-291V-270Q0-253 22-270V-291" fill={c.skin}/>
   <Arm side={-1} angle={left} c={c}/><Arm side={1} angle={right} c={c} extended={pose==='point'}/>
   <g transform={`rotate(${tilt},0,-327)`}>
    <ellipse cx="-66" cy="-342" rx="11" ry="19" fill={c.skin}/><ellipse cx="66" cy="-342" rx="11" ry="19" fill={c.skin}/>
    <path d="M-65-368Q-66-412 0-414Q66-412 65-368L62-332Q56-284 0-282Q-56-284-62-332Z" fill={c.skin}/>
    <HairFront c={c}/><Face emotion={emotion} frame={frame} speaking={speaking} c={c}/>
    {c.accessory==='headphones'&&<g><path d="M-76-350V-384Q-70-445 0-445Q70-445 76-384V-350" fill="none" stroke={c.accent} strokeWidth="12"/><rect x="-85" y="-366" width="20" height="43" rx="8" fill={c.accent}/><rect x="65" y="-366" width="20" height="43" rx="8" fill={c.accent}/></g>}
   </g>
  </g>
 </g>;
};
