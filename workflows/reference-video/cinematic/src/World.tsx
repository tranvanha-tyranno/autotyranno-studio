import React,{useMemo} from 'react';
import {useLoader} from '@react-three/fiber';
import {ThreeCanvas} from '@remotion/three';
import {useCurrentFrame,interpolate,spring,staticFile} from 'remotion';
import * as THREE from 'three';
import {FontLoader} from 'three/examples/jsm/loaders/FontLoader.js';
import {TextGeometry} from 'three/examples/jsm/geometries/TextGeometry.js';
import fontData from './font.json';

const face=new FontLoader().parse(fontData);
export const W=1920,H=1080;
export const INK='#080d16',WHITE='#f3f5f0',GREEN='#42ffd2',ORANGE='#ff7358';

export const Stage:React.FC<{children:React.ReactNode;camera?:[number,number,number]}>=({children,camera=[0,0,13]})=><ThreeCanvas width={W} height={H} camera={{fov:34,position:camera}} gl={{antialias:true,alpha:true}} style={{position:'absolute',inset:0}}>
 <ambientLight intensity={1.1}/><directionalLight position={[2,5,6]} intensity={3.2} color="#ffffff"/>
 <pointLight position={[-6,2,4]} intensity={35} color={GREEN}/><pointLight position={[6,-2,3]} intensity={25} color="#638eff"/>
 {children}
</ThreeCanvas>;

export const Digits:React.FC<{text?:string;frame?:number;scale?:number}>=({text='1.000',frame,scale=1.8})=>{
 const now=useCurrentFrame(),f=frame??now;
 const geo=useMemo(()=>{const g=new TextGeometry(text,{font:face,size:1,depth:.22,curveSegments:10,bevelEnabled:true,bevelSize:.018,bevelThickness:.025,bevelSegments:3});g.center();return g;},[text]);
 const intro=spring({frame:f,fps:30,config:{damping:22,stiffness:100}});
 return <group position={[0,.15,(1-intro)*-12]} rotation={[-.13,-.25+Math.sin(f/80)*.1,-.025]} scale={scale*intro}>
  <mesh geometry={geo}><meshPhysicalMaterial color={WHITE} metalness={.48} roughness={.22} clearcoat={1}/></mesh>
 </group>;
};

function useMap(name:string){
 // Suspend before the first GPU draw. Releasing a delayRender immediately
 // after setState can capture the untextured sphere on the first frame.
 const texture=useLoader(THREE.TextureLoader,staticFile(name));
 texture.colorSpace=THREE.SRGBColorSpace;
 return texture;
}

function xyz(lat:number,lon:number,r:number){const a=lat*Math.PI/180,b=lon*Math.PI/180;return new THREE.Vector3(r*Math.cos(a)*Math.cos(b),r*Math.sin(a),-r*Math.cos(a)*Math.sin(b));}
const routes=[[17,108,40,-75],[17,108,51,0],[17,108,-34,151],[17,108,35,139],[17,108,-1,103]];
export const Earth:React.FC<{right?:boolean}>=({right=false})=>{
 const f=useCurrentFrame();const texture=useMap('earth.jpg');const night=useMap('earth-night.jpg');
 const curves=useMemo(()=>routes.map(([a,b,c,d])=>{const p=xyz(a,b,2.6),q=xyz(c,d,2.6),mid=p.clone().add(q).normalize().multiplyScalar(4.6);return new THREE.QuadraticBezierCurve3(p,mid,q);}),[]);
 return <group position={[right?2.3:0,.05,0]} rotation={[.08,-3.8+f*.0012,.08]} scale={.9+ease(f,0,95)*.1}>
  <mesh><sphereGeometry args={[2.6,80,48]}/><meshStandardMaterial map={texture} emissiveMap={night} emissive="#88bfff" emissiveIntensity={.45} roughness={.92} metalness={0}/></mesh>
  <mesh scale={1.018}><sphereGeometry args={[2.6,48,24]}/><meshBasicMaterial color="#3975ff" transparent opacity={.05} side={THREE.BackSide}/></mesh>
  {curves.map((c,i)=>{const progress=((f/100+i*.13)%1);const p=c.getPoint(progress);return <group key={i}>
    <mesh><tubeGeometry args={[c,50,.013,6,false]}/><meshBasicMaterial color={i%2?GREEN:'#8ca7ff'} transparent opacity={.64}/></mesh>
    <mesh position={p}><sphereGeometry args={[.045,8,8]}/><meshBasicMaterial color="#ffffff"/></mesh>
  </group>})}
 </group>;
};

export const Containers:React.FC=()=>{
 const f=useCurrentFrame();
 return <group rotation={[.38,-.55+f*.002,-.1]} position={[.3,-.25,0]}>
  {Array.from({length:12},(_,i)=>{const x=(i%4-1.5)*2.15,y=Math.floor(i/4)*.9-1;const e=spring({frame:f-i*2,fps:30,config:{damping:22}});return <group key={i} position={[x,y-4*(1-e),Math.sin(i*7)*.18]}>
   <mesh><boxGeometry args={[2,.8,.8]}/><meshPhysicalMaterial color={i%4===0?GREEN:i%3===0?ORANGE:'#53617b'} roughness={.45} metalness={.45}/></mesh>
   {Array.from({length:10},(_,j)=><mesh key={j} position={[(j-4.5)*.18,0,.415]}><boxGeometry args={[.025,.7,.035]}/><meshStandardMaterial color={i%4===0?'#237e6a':'#273248'} metalness={.5} roughness={.3}/></mesh>)}
  </group>})}
 </group>;
};

export const Tokens:React.FC=()=>{
 const f=useCurrentFrame();
 return <group rotation={[.24,-.3,.0]} position={[2.5,0,0]}>
  {Array.from({length:14},(_,i)=>{const phase=(f*.005+i*.079)%1;const x=-2+phase*9,y=i%3-1;const outward=i%3!==0;return <group key={i} position={[x,y*(1+phase*1.6),Math.sin(phase*Math.PI)*1.2]} rotation={[Math.PI/2+.2,phase*6+i*.7,.2]}>
   <mesh><cylinderGeometry args={[.36,.36,.10,48]}/><meshPhysicalMaterial color={outward?'#f06a46':'#00a885'} metalness={.5} roughness={.25} clearcoat={1}/></mesh>
   <mesh position={[0,.056,0]} rotation={[-Math.PI/2,0,0]}><torusGeometry args={[.27,.017,8,36]}/><meshStandardMaterial color="#fff0d5" metalness={.45} roughness={.25}/></mesh>
  </group>})}
 </group>;
};

export const bgStyle:React.CSSProperties={background:'radial-gradient(ellipse at 65% 55%,#182b43 0%,#080d16 57%,#05080e 100%)',color:WHITE,fontFamily:'Bahnschrift,Arial,sans-serif'};
export const ease=(f:number,a=0,b=24)=>interpolate(f,[a,b],[0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp',easing:t=>1-Math.pow(1-t,3)});
