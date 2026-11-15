import {useMemo} from 'react';
import {useCurrentFrame,spring} from 'remotion';
import * as THREE from 'three';
import {RoundedBoxGeometry} from 'three/examples/jsm/geometries/RoundedBoxGeometry.js';
import {Stage,Digits,ease,GREEN,ORANGE} from '../World';

const rounded=new RoundedBoxGeometry(1,1,1,3,.09);
const Material:React.FC<{color?:string;light?:boolean}>=({color='#dce4e7',light=false})=><meshPhysicalMaterial color={color} metalness={light?.12:.35} roughness={.3} clearcoat={.8}/>;
const Block:React.FC<{size:[number,number,number];position?:[number,number,number];color?:string}>=({size,position=[0,0,0],color})=><mesh geometry={rounded} position={position} scale={size}><Material color={color}/></mesh>;

const Chip:React.FC=()=>{
 const f=useCurrentFrame();return <group rotation={[.25,-.35+Math.sin(f/110)*.15,.05]} scale={.85+ease(f,0,30)*.15}>
 <Block size={[3.1,2.7,.35]} color="#152b3b"/>
 <Block size={[2.65,2.25,.12]} position={[0,0,.23]} color="#31516a"/>
 <group position={[0,-.08,.44]}><Digits text="AI" scale={1.6}/></group>
 {Array.from({length:8},(_,i)=><group key={i}>{[-1,1].map(s=><group key={s}>
 <Block size={[.48,.065,.12]} position={[s*1.75,(i-3.5)*.29,0]} color={GREEN}/>
 <Block size={[.065,.4,.12]} position={[(i-3.5)*.32,s*1.55,0]} color={i%2?GREEN:'#658cb0'}/>
 </group>)}</group>)}
 </group>;
};

const Tasks:React.FC<{splitAt:number}>=({splitAt})=>{
 const f=useCurrentFrame();return <group rotation={[.22,-.25+Math.sin(f/140)*.18,-.06]}>
 {Array.from({length:12},(_,i)=>{const p=spring({frame:f-i*3,fps:30,config:{damping:22}});const col=i%3;const spread=.3*ease(f,splitAt,splitAt+30);return <group key={i} position={[(col-1)*(1.27+spread),1.45-Math.floor(i/3)*.96-(1-p)*3,Math.sin(i)*.1]} scale={p}>
 <Block size={[1.12,.79,.18]} color={col===0?GREEN:col===1?'#648eab':ORANGE}/>
 {[0,1,2].map(j=><Block key={j} size={[.68-j*.12,.034,.02]} position={[-j*.06,.19-j*.14,.105]} color={col===0?'#17564a':'#192b3c'}/>)}
 </group>})}
 </group>;
};

const Documents:React.FC<{phase:number}>=({phase})=>{
 const f=useCurrentFrame();return <group rotation={[.18,-.4+Math.sin(f/140)*.13,-.06]}>
 {Array.from({length:4},(_,i)=>{const intro=ease(f,i*8,i*8+30);return <group key={i} position={[(i-1.5)*.25,(i-1.5)*.16-(1-intro)*3,-i*.3]} rotation={[0,0,i*.025]}>
 <Block size={[2.5,3.25,.08]} color={i===0?'#eeeede':'#6b8298'}/>
 {Array.from({length:8},(_,j)=><Block key={j} size={[j%3===0?1.3:1.8,.07,.02]} position={[-.2+(j%3===0?-.25:0),1.1-j*.28,.061]} color={phase>=1&&j===3?ORANGE:j===0?'#00a483':'#486276'}/>)}
 </group>})}
 </group>;
};

const People:React.FC<{phase:number}>=({phase})=>{
 const f=useCurrentFrame();return <group rotation={[.07,-.15+Math.sin(f/160)*.12,0]}>
 {Array.from({length:4},(_,i)=>{const p=spring({frame:f-i*7,fps:30,config:{damping:20}});const color=i===0?GREEN:'#72859b';return <group key={i} position={[(i-1.5)*1.14,-.35-(1-p)*3,0]} scale={i===0&&phase>=0?1.06:1}>
 <mesh position={[0,1.2,0]}><sphereGeometry args={[.28,24,16]}/><Material color={color}/></mesh>
 <mesh position={[0,.28,0]}><capsuleGeometry args={[.24,.85,6,16]}/><Material color={color}/></mesh>
 {[-1,1].map(s=><mesh key={s} position={[s*.14,-.58,0]}><capsuleGeometry args={[.10,.65,5,12]}/><Material color={color}/></mesh>)}
 </group>})}
 <mesh position={[0,-1.3,0]} rotation={[-Math.PI/2,0,0]}><circleGeometry args={[2.8,64]}/><meshBasicMaterial color="#172938" transparent opacity={.6}/></mesh>
 </group>;
};

const Clock:React.FC=()=>{
 const f=useCurrentFrame();return <group rotation={[.2,-.28+Math.sin(f/170)*.1,.03]}>
 <mesh><torusGeometry args={[1.85,.11,16,80]}/><Material color="#356f80"/></mesh>
 {Array.from({length:12},(_,i)=>{const a=i*Math.PI/6;return <group key={i} rotation={[0,0,-a]}><Block size={[.045,.15,.06]} position={[0,1.58,0]} color={i%3===0?ORANGE:'#6b8c97'}/></group>})}
 <group rotation={[0,0,-f*.012]}><Block size={[.07,1.45,.075]} position={[0,.53,.05]} color="#00a483"/></group>
 <group rotation={[0,0,-.8-f*.001]}><Block size={[.12,.9,.10]} position={[0,.3,.12]} color={ORANGE}/></group>
 <mesh position={[0,0,.2]}><sphereGeometry args={[.15,20,16]}/><Material color="#152b3b"/></mesh>
 </group>;
};

const Bars:React.FC=()=>{
 const f=useCurrentFrame();const p=ease(f,10,70);return <group rotation={[.08,-.24,.0]}>
 {[{v:170,x:-1.05,c:GREEN},{v:92,x:1.05,c:ORANGE}].map(({v,x,c},i)=>{const h=(v/170)*3.65*p;return <group key={v} position={[x,-1.8,0]}>
 <Block size={[1.1,Math.max(.01,h),1.0]} position={[0,h/2,0]} color={c}/>
 <group position={[0,h+.35,.35]} scale={.5}><Digits text={String(v)} scale={1}/></group>
 <Block size={[1.4,.07,1.3]} position={[0,-.08,0]} color={i===0?'#1c6659':'#6c3a32'}/>
 </group>})}
 </group>;
};

const Network:React.FC<{bridge?:boolean}>=({bridge=false})=>{
 const f=useCurrentFrame();const points=useMemo(()=>Array.from({length:9},(_,i)=>new THREE.Vector3((i%3-1)*1.7,(Math.floor(i/3)-1)*1.3,Math.sin(i*2)*.6)),[]);
 const curves=useMemo(()=>points.slice(0,-1).map((p,i)=>new THREE.LineCurve3(p,points[i+1])),[points]);
 return <group rotation={[.15,-.25+Math.sin(f/130)*.16,.04]}>
 {points.map((p,i)=><group key={i} position={p} scale={.8+ease(f,i*3,i*3+30)*.2}><Block size={[.72,.72,.22]} color={i===4?GREEN:i%2?ORANGE:'#54798f'}/></group>)}
 {curves.map((c,i)=>{const pos=c.getPoint((f/100+i*.19)%1);return <group key={i}><mesh><tubeGeometry args={[c,1,.025,6,false]}/><meshBasicMaterial color={bridge?'#d2a389':'#587c91'}/></mesh><mesh position={pos}><sphereGeometry args={[.075,12,8]}/><meshBasicMaterial color={GREEN}/></mesh></group>})}
 </group>;
};

const Gate:React.FC=()=>{
 const f=useCurrentFrame();const t=(f/160)%1;return <group rotation={[.16,-.4,.02]}>
 <mesh position={[0,0,.2]}><torusGeometry args={[1.65,.09,12,70]}/><Material color="#00a483"/></mesh>
 <mesh position={[.05,0,-.35]}><torusGeometry args={[1.65,.04,10,70]}/><Material color="#506e88"/></mesh>
 <group position={[-3.8+t*7.6,Math.sin(t*Math.PI)*.15,.45]} rotation={[0,0,.1]}><Block size={[1,.7,.15]} color={t<.5?ORANGE:GREEN}/></group>
 <group position={[.15,-1.95,.5]}><Block size={[1.1,.12,.15]} color="#54798f"/></group>
 </group>;
};

const Steps:React.FC=()=>{
 const f=useCurrentFrame();return <group rotation={[.25,-.45,.0]}>
 {Array.from({length:4},(_,i)=>{const p=ease(f,10+i*12,45+i*12);return <group key={i} position={[(i-1.5)*1.1,-1.7,0]}>
 <Block size={[.9,Math.max(.01,(i+1)*.75*p),1.3]} position={[0,(i+1)*.375*p,0]} color={i===3?ORANGE:i%2?GREEN:'#507891'}/>
 </group>})}
 </group>;
};

export const Objects:React.FC<{kind:string;phase:number;splitAt:number}>=({kind,phase,splitAt})=><Stage><group position={[2.85,.05,0]}>
 {kind==='chip'?<Chip/>:kind==='tasks'?<Tasks splitAt={splitAt}/>:kind==='documents'?<Documents phase={phase}/>:kind==='people'?<People phase={phase}/>:kind==='clock'?<Clock/>:kind==='bars'?<Bars/>:kind==='network'||kind==='bridge'?<Network bridge={kind==='bridge'}/>:kind==='steps'?<Steps/>:<Gate/>}
 </group></Stage>;
