import {spring,useCurrentFrame,interpolate} from 'remotion';

/** Word planes rotate into the camera, paced from exact narration cues. */
export const Type:React.FC<{text:string;at?:number;step?:number;style?:React.CSSProperties}>=({text,at=0,step=3,style})=>{
 const f=useCurrentFrame();
 return <div style={{perspective:900,...style}}>{text.split(' ').map((word,i)=>{
  const p=spring({frame:f-at-i*step,fps:30,config:{damping:19,stiffness:145,mass:.7}});
  return <span key={i} style={{display:'inline-block',whiteSpace:'pre',opacity:interpolate(p,[0,.35],[0,1],{extrapolateRight:'clamp'}),transform:`translate3d(0,${(1-p)*90}px,${(1-p)*-130}px) rotateX(${(1-p)*75}deg)`,transformOrigin:'center bottom'}}>{word}{i<text.split(' ').length-1?' ':''}</span>;
 })}</div>;
};
