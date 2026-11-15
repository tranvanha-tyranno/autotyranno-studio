import {useEffect, useMemo} from 'react';
import {ThreeCanvas} from '@remotion/three';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import * as THREE from 'three';
import {Header, Media, Source, clamp, font, localCue, rise, themeFor} from './Shared';
import type {BusinessShot} from './types';

const Cup: React.FC<{fill: number; accent: string}> = ({fill, accent}) => {
  const geometry = useMemo(() => new THREE.LatheGeometry([
    new THREE.Vector2(.20, -.73), new THREE.Vector2(.61, -.73), new THREE.Vector2(.72, -.61),
    new THREE.Vector2(.86, .64), new THREE.Vector2(.84, .72), new THREE.Vector2(.77, .72),
    new THREE.Vector2(.69, -.56), new THREE.Vector2(.20, -.61),
  ], 64), []);
  useEffect(() => () => geometry.dispose(), [geometry]);
  return <group>
    <mesh geometry={geometry}><meshStandardMaterial color="#f4ead4" roughness={.34} metalness={.04} side={THREE.DoubleSide}/></mesh>
    <mesh position={[.94, .02, 0]} rotation={[0, 0, -.1]} scale={[.75, 1, 1]}><torusGeometry args={[.47, .095, 12, 40]}/><meshStandardMaterial color="#f4ead4" roughness={.34}/></mesh>
    <mesh position={[0, .50, 0]} rotation={[-Math.PI / 2, 0, 0]} scale={Math.max(.001, fill)}><circleGeometry args={[.76, 64]}/><meshStandardMaterial color="#513220" roughness={.24}/></mesh>
    <mesh position={[0, -.81, 0]}><cylinderGeometry args={[1.26, 1.20, .10, 64]}/><meshStandardMaterial color="#e3d3b9" roughness={.42}/></mesh>
    <mesh position={[0, -.89, 0]} rotation={[-Math.PI / 2, 0, 0]} scale={[1, .7, 1]}><circleGeometry args={[1.52, 64]}/><meshBasicMaterial color="#645842" transparent opacity={.13} depthWrite={false}/></mesh>
    <mesh position={[0, -.05, .81]}><circleGeometry args={[.22, 40]}/><meshStandardMaterial color={accent} roughness={.7}/></mesh>
  </group>;
};

const Coins: React.FC<{frame: number; starts: number[]; accent: string}> = ({frame, starts, accent}) => <group>
  {starts.map((start, i) => {
    const progress = rise(frame, start, 26);
    if (frame < start) return null;
    return <mesh key={start} position={[1.7 + i * .18, -1.2 + i * .11 + (1 - progress) * 3, .3 + i * .15]} rotation={[0, 0, (1 - progress) * .35]}><cylinderGeometry args={[.34, .34, .085, 36]}/><meshStandardMaterial color={accent} metalness={.55} roughness={.35}/></mesh>;
  })}
</group>;

/** The coffee object clarifies a single unit; photos carry the business context. */
export const CoffeeScene: React.FC<{shot: BusinessShot; duration: number}> = ({shot, duration}) => {
  const frame = useCurrentFrame();
  const p = themeFor(shot);
  const kind = shot.design?.coffee?.kind ?? 'cup';
  const notes = shot.design?.paper;
  const cues = [0, 1, 2].map(i => localCue(shot, i, 8 + i * duration * .23));
  const fill = rise(frame, cues[0], 38);
  return <AbsoluteFill style={{background: p.paper, color: p.ink}}>
    <Header shot={shot}/>
    <div style={{position: 'absolute', left: 100, top: 285, width: 620, height: 505, overflow: 'hidden', rotate: '-1.5deg', boxShadow: '0 18px 40px rgba(25,23,15,.12)'}}>{shot.images[0] ? <Media image={shot.images[0]} duration={duration}/> : null}</div>
    <div style={{position: 'absolute', left: 750, top: 245, width: 1070, height: 540}}>
      <ThreeCanvas width={1070} height={540} camera={{fov: 34, position: [0, 1.8, 6.5]}} gl={{alpha: true, antialias: true}} style={{position: 'absolute', inset: 0}}>
        <ambientLight intensity={1.6}/><directionalLight position={[-3, 5, 6]} intensity={2.1}/><directionalLight position={[4, 3, -2]} intensity={.7}/>
        <group rotation={[0, interpolate(frame, [0, Math.max(1, duration - 1)], [-.22, .06], clamp), 0]} position={[kind === 'cup' ? 0 : -.42, -.10, 0]}>
          <Cup fill={fill} accent={p.accent}/>
          {kind !== 'cup' ? <Coins frame={frame} starts={cues} accent={p.accent}/> : null}
          {kind === 'flow' ? [0, 1].map(i => <group key={i} position={[-1.8 - i * .8, -.49, -.65]} scale={.40}><Cup fill={fill} accent={p.accent}/></group>) : null}
        </group>
      </ThreeCanvas>
    </div>
    {notes?.rows?.length ? <div style={{position: 'absolute', left: 790, right: 100, top: 733, display: 'flex', justifyContent: 'center', gap: 45}}>{notes.rows.slice(0, 3).map((row, i) => <div key={row.label} style={{textAlign: 'center', opacity: rise(frame, cues[i])}}><div style={{fontFamily: font, fontSize: 48, fontWeight: 700, color: i === 2 ? p.accent : p.ink}}>{row.value}</div><div style={{font: '23px Arial,sans-serif', maxWidth: 250, marginTop: 7, color: p.quiet}}>{row.label}</div></div>)}</div> : shot.body ? <div style={{position: 'absolute', left: 790, right: 100, top: 791, textAlign: 'center', font: '32px Arial,sans-serif', lineHeight: 1.35}}>{shot.body}</div> : null}
    <Source shot={shot}/>
  </AbsoluteFill>;
};
