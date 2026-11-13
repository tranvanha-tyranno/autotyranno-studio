import {useEffect, useMemo} from 'react';
import {ThreeCanvas} from '@remotion/three';
import {AbsoluteFill, CanvasImage, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import * as THREE from 'three';
import type {DirectionName, DirectionShot, ShoppingMotion} from './types';

const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const colors = {
  long: {paper: '#f1ebdf', ink: '#27251f', accent: '#ee5f3f', quiet: '#68645c', mint: '#8cafa0'},
  hidden: {paper: '#e8e7dd', ink: '#0c1c28', accent: '#86c7c0', quiet: '#647678', mint: '#b6a883'},
};

const cue = (motion: ShoppingMotion, index: number, duration: number, fraction: number) =>
  motion.revealFrames?.[index] ?? Math.round(Math.max(1, duration - 1) * fraction);

const appear = (frame: number, start: number) => interpolate(frame, [start, start + 9], [0, 1], clamp);

/** A gable-top carton, not a branded or price-verified product. */
const Carton: React.FC<{color?: string; scale?: number}> = ({color = '#8cafa0', scale = 1}) => {
  const roof = useMemo(() => {
    const triangle = new THREE.Shape();
    triangle.moveTo(-.34, 0);
    triangle.lineTo(.34, 0);
    triangle.lineTo(0, .29);
    triangle.closePath();
    return new THREE.ExtrudeGeometry(triangle, {depth: .46, bevelEnabled: false});
  }, []);
  useEffect(() => () => roof.dispose(), [roof]);
  return <group scale={scale}>
    <mesh><boxGeometry args={[.68, 1.08, .46]}/><meshStandardMaterial color={color} roughness={.8}/></mesh>
    <mesh position={[0, .54, -.23]} geometry={roof}><meshStandardMaterial color="#faf5e9" roughness={.85}/></mesh>
    <mesh position={[0, .838, 0]}><boxGeometry args={[.042, .047, .47]}/><meshStandardMaterial color={color}/></mesh>
    <mesh position={[0, .02, .236]}><planeGeometry args={[.39, .34]}/><meshBasicMaterial color="#faf5e9"/></mesh>
    <mesh position={[0, -.03, .242]}><circleGeometry args={[.10, 24]}/><meshBasicMaterial color="#ee5f3f"/></mesh>
  </group>;
};

/** Open rails keep the added items visible rather than hiding them in a box. */
const Basket: React.FC<{accent: string}> = ({accent}) => <group>
  <mesh position={[0, -.52, 0]}><boxGeometry args={[2.65, .14, 1.48]}/><meshStandardMaterial color={accent} roughness={.62}/></mesh>
  {[-.71, .71].map(z => <group key={z}>
    {[-.18, .17, .52].map(y => <mesh key={y} position={[0, y, z]}><boxGeometry args={[2.75, .075, .075]}/><meshStandardMaterial color={accent}/></mesh>)}
    {[-1.28, -.85, -.42, 0, .42, .85, 1.28].map(x => <mesh key={x} position={[x, 0, z]}><boxGeometry args={[.065, 1.04, .075]}/><meshStandardMaterial color={accent}/></mesh>)}
  </group>)}
  {[-1.33, 1.33].map(x => <group key={x}>
    {[-.18, .17, .52].map(y => <mesh key={y} position={[x, y, 0]}><boxGeometry args={[.075, .075, 1.48]}/><meshStandardMaterial color={accent}/></mesh>)}
    <mesh position={[x, 0, 0]}><boxGeometry args={[.075, 1.04, .065]}/><meshStandardMaterial color={accent}/></mesh>
  </group>)}
  {/* The handle sits behind the goods so the action has an unobstructed face. */}
  {[-1.05, 1.05].map(x => <mesh key={x} position={[x, 1.04, -.50]}><boxGeometry args={[.09, 1.12, .09]}/><meshStandardMaterial color="#494b43"/></mesh>)}
  <mesh position={[0, 1.61, -.50]}><boxGeometry args={[2.18, .11, .11]}/><meshStandardMaterial color="#494b43"/></mesh>
</group>;

const ContactShadow: React.FC<{x?: number; scale?: number}> = ({x = 0, scale = 1}) => <mesh position={[x, -1.23, 0]} rotation={[-Math.PI / 2, 0, 0]} scale={[scale, .65 * scale, 1]}>
  <circleGeometry args={[1.75, 48]}/><meshBasicMaterial color="#8b8171" transparent opacity={.12} depthWrite={false}/>
</mesh>;

const DroppingCarton: React.FC<{frame: number; fps: number; start: number; index: number; color: string}> = ({frame, fps, start, index, color}) => {
  if (frame < start) return null;
  const settle = spring({frame: frame - start, fps, config: {damping: 18, stiffness: 145, mass: .8}});
  const positions: [number, number, number][] = [[-.78, .06, .08], [0, .15, -.12], [.78, .08, .13]];
  const [x, y, z] = positions[index];
  return <group position={[x + (1 - settle) * .35, y + (1 - settle) * 3.6, z]} rotation={[0, -.06 + index * .08, (1 - settle) * (index % 2 ? -.24 : .20)]}>
    <Carton color={color} scale={.88}/>
  </group>;
};

const BasketScene: React.FC<{motion: ShoppingMotion; direction: DirectionName; duration: number}> = ({motion, direction, duration}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = colors[direction];
  const angle = interpolate(frame, [0, Math.max(1, duration - 1)], [-.30, -.18], clamp);
  return <group position={[0, -.17, 0]} rotation={[0, angle, 0]}>
    <ContactShadow scale={1.2}/>
    <group position={[0, -.42, 0]}>
      <Basket accent={p.accent}/>
      {[p.mint, '#e8c77e', '#a5b9c5'].map((color, index) => <DroppingCarton key={color} frame={frame} fps={fps} start={cue(motion, index, duration, .08 + index * .22)} index={index} color={color}/>)}
    </group>
  </group>;
};

const PriceScene: React.FC<{motion: ShoppingMotion; direction: DirectionName; duration: number}> = ({motion, direction, duration}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = colors[direction];
  const first = cue(motion, 0, duration, .04);
  const second = cue(motion, 1, duration, .31);
  return <group position={[0, -.08, 0]}>
    {[-3.5, 3.5].map((x, i) => {
      const start = i === 0 ? first : second;
      const rise = spring({frame: Math.max(0, frame - start), fps, config: {damping: 22, stiffness: 130}});
      return <group key={x} position={[x, 0, 0]}>
        <ContactShadow scale={1.12}/>
        <mesh position={[0, -1.03, 0]}><cylinderGeometry args={[1.65, 1.65, .25, 48]}/><meshStandardMaterial color={i === 0 ? '#e4dac6' : '#e8c3ac'} roughness={.9}/></mesh>
        {frame >= start ? <group position={[0, (1 - rise) * 2.8 - .25, 0]} rotation={[0, -.16, (1 - rise) * .08]}>
          {i === 0 ? <Carton color={p.mint} scale={1.18}/> : <>
            <group position={[-.53, 0, -.06]}><Carton color={p.mint} scale={1.18}/></group>
            <group position={[.53, 0, .06]}><Carton color={p.mint} scale={1.18}/></group>
          </>}
        </group> : null}
      </group>;
    })}
  </group>;
};

const Home: React.FC<{accent: string}> = ({accent}) => <group>
  <mesh position={[0, -.22, 0]}><boxGeometry args={[1.48, 1.45, 1.05]}/><meshStandardMaterial color="#e2d5bc" roughness={.85}/></mesh>
  <mesh position={[0, .71, 0]} rotation={[0, Math.PI / 4, 0]}><coneGeometry args={[1.20, .83, 4]}/><meshStandardMaterial color={accent} roughness={.8}/></mesh>
  <mesh position={[.12, -.44, .536]}><planeGeometry args={[.41, .90]}/><meshBasicMaterial color="#737c6c"/></mesh>
  <mesh position={[-.45, .02, .54]}><planeGeometry args={[.27, .32]}/><meshBasicMaterial color="#f8f1dc"/></mesh>
</group>;

const Shelf: React.FC<{accent: string; itemVisible: boolean}> = ({accent, itemVisible}) => <group>
  {[-.95, .95].map(x => <mesh key={x} position={[x, -.12, -.25]}><boxGeometry args={[.08, 2.48, .08]}/><meshStandardMaterial color="#7c8175"/></mesh>)}
  {[-1.19, -.28, .64].map(y => <mesh key={y} position={[0, y, 0]}><boxGeometry args={[2.05, .09, .80]}/><meshStandardMaterial color="#c6c2af"/></mesh>)}
  {[-.60, 0, .60].map((x, i) => <group key={x} position={[x, .96, 0]}><Carton color={i === 1 ? accent : '#a9b8a0'} scale={.47}/></group>)}
  {[-.58, .58].map(x => <group key={x} position={[x, .01, 0]}><Carton color="#e2c27c" scale={.47}/></group>)}
  {itemVisible ? <group position={[0, -.88, .03]}><Carton color="#8cafa0" scale={.47}/></group> : null}
</group>;

const JourneyScene: React.FC<{motion: ShoppingMotion; direction: DirectionName; duration: number}> = ({motion, direction, duration}) => {
  const frame = useCurrentFrame();
  const p = colors[direction];
  const depart = cue(motion, 1, duration, .30);
  const arrive = cue(motion, 2, duration, .68);
  const travelEnd = Math.max(depart + 1, arrive);
  const travel = interpolate(frame, [depart, travelEnd], [0, 1], {...clamp, easing: t => t * t * (3 - 2 * t)});
  const entry = appear(frame, cue(motion, 0, duration, .02));
  return <group position={[0, -.03, 0]} rotation={[0, -.08, 0]}>
    <ContactShadow x={-3.8} scale={.73}/><ContactShadow scale={.83}/><ContactShadow x={3.8} scale={.8}/>
    <group position={[-3.8, -.1 - (1 - entry) * .8, 0]} scale={entry}><Home accent={p.accent}/></group>
    <group position={[0, -.04, 0]} scale={.86}><Shelf accent={p.accent} itemVisible={frame < depart}/></group>
    <group position={[3.8, -.53, 0]} scale={.68}><Basket accent={p.accent}/></group>
    {frame >= depart ? <group position={[travel * 3.8, -.7968 + Math.sin(travel * Math.PI) * 1.0 + travel * .6368, .0258 + travel * .0742]} rotation={[0, -.10, Math.sin(travel * Math.PI) * -.25]}><Carton color={p.mint} scale={.4042 + travel * .0658}/></group> : null}
    <mesh position={[0, -1.25, -.30]}><boxGeometry args={[9.8, .025, .025]}/><meshBasicMaterial color={p.quiet} transparent opacity={.22}/></mesh>
    {[-3.8, 0, 3.8].map((x, i) => <mesh key={x} position={[x, -1.25, -.25]}><sphereGeometry args={[.07, 16, 8]}/><meshBasicMaterial color={frame >= cue(motion, i, duration, [.02, .30, .68][i]) ? p.accent : '#b4ad9e'}/></mesh>)}
  </group>;
};

/** Original geometry + an inspected photo. Price numbers are illustrative only. */
export const Shopping3D: React.FC<{shot: DirectionShot; direction: DirectionName; duration: number}> = ({shot, direction, duration}) => {
  const frame = useCurrentFrame();
  const p = colors[direction];
  const motion = shot.motion;
  if (!motion) throw new Error('object3d needs an explicit motion kind.');
  const price = motion.kind === 'price';
  const journey = motion.kind === 'journey';
  const photo = shot.images[0];
  const first = cue(motion, 0, duration, .04);
  const second = cue(motion, 1, duration, .31);
  const third = cue(motion, 2, duration, .58);
  const credit = shot.sourceNote ?? [...new Set(shot.images.map(image => image.credit).filter(Boolean))].join(' / ');
  const font = direction === 'long' ? 'Bahnschrift,Arial,sans-serif' : 'Times New Roman,serif';
  return <AbsoluteFill style={{background: 'radial-gradient(ellipse at 55% 43%,#fffaf0,#e8dfcd)', color: p.ink, overflow: 'hidden'}}>
    <div style={{position: 'absolute', left: 88, right: 88, top: 63, font: '700 20px Arial,sans-serif', letterSpacing: 3, color: price ? p.accent : p.quiet}}>{price ? 'VÍ DỤ GIẢ ĐỊNH — KHÔNG PHẢI GIÁ BÁN' : shot.eyebrow}</div>
    <div style={{position: 'absolute', left: 88, right: 88, top: 112, fontFamily: font, fontSize: 59, fontWeight: direction === 'long' ? 700 : 400, lineHeight: 1.12, letterSpacing: -1.4, opacity: appear(frame, 0), translate: `0 ${interpolate(frame, [0, 15], [18, 0], clamp)}px`}}>{shot.headline ?? (price ? motion.stage === 'total' ? 'Giá mỗi hộp giảm. Tổng tiền tăng.' : 'Một hộp và hai hộp khác nhau ở đâu?' : journey ? 'Ba điểm dừng cho một quyết định.' : 'Từ một món cần mua…')}</div>
    {!price && !journey && photo ? <div style={{position: 'absolute', left: 88, top: 255, width: 490, height: 510, overflow: 'hidden', boxShadow: '0 22px 40px rgba(55,45,28,.16)', border: '5px solid #fff9ed', rotate: '-2deg', opacity: appear(frame, 2)}}>
      <CanvasImage src={staticFile(photo.mediaType === 'video' ? photo.posterFile! : photo.file)} style={{width: '100%', height: '100%', objectFit: photo.fit === 'contain' ? 'contain' : 'cover', objectPosition: `${photo.focus?.[0] ?? 50}% ${photo.focus?.[1] ?? 50}%`, scale: photo.fit === 'contain' ? 1 : interpolate(frame, [0, Math.max(1, duration - 1)], [1.015, 1.065], clamp)}}/>
    </div> : null}
    {journey ? shot.images.slice(0, 3).map((image, i) => <div key={`${image.file}-${i}`} style={{position: 'absolute', left: [260, 795, 1330][i], top: 251, width: 330, height: 200, overflow: 'hidden', border: '4px solid #fff9ed', boxShadow: '0 12px 23px rgba(55,45,28,.12)', rotate: `${i === 0 ? -1.5 : i === 2 ? 1.5 : 0}deg`, opacity: appear(frame, cue(motion, i, duration, [.02, .30, .68][i]))}}>
      <CanvasImage src={staticFile(image.mediaType === 'video' ? image.posterFile! : image.file)} style={{width: '100%', height: '100%', objectFit: image.fit === 'contain' ? 'contain' : 'cover', objectPosition: `${image.focus?.[0] ?? 50}% ${image.focus?.[1] ?? 50}%`, scale: image.fit === 'contain' ? 1 : interpolate(frame, [0, Math.max(1, duration - 1)], [1.012, 1.05], clamp)}}/>
    </div>) : null}
    <div style={{position: 'absolute', left: price || journey ? 120 : 605, top: price ? 265 : journey ? 422 : 245, width: price || journey ? 1680 : 1227, height: price ? 460 : journey ? 400 : 565}}>
      <ThreeCanvas width={price || journey ? 1680 : 1227} height={price ? 460 : journey ? 400 : 565} camera={{fov: price ? 31 : journey ? 22 : 34, position: [0, price ? 1.3 : 1.6, price ? 7.0 : journey ? 7.1 : 7.2]}} gl={{antialias: true, alpha: true}} style={{position: 'absolute', inset: 0}}>
        <ambientLight intensity={1.7}/><directionalLight position={[-3, 6, 8]} intensity={2.2}/><directionalLight position={[5, 2, -3]} intensity={.6}/>
        {price ? <PriceScene motion={motion} direction={direction} duration={duration}/> : journey ? <JourneyScene motion={motion} direction={direction} duration={duration}/> : <BasketScene motion={motion} direction={direction} duration={duration}/>}
      </ThreeCanvas>
    </div>
    {price ? <>
      {[{x: 220, n: '1 HỘP', total: '30.000đ', unit: '30.000đ / hộp', start: first}, {x: 1050, n: '2 HỘP', total: '50.000đ', unit: '25.000đ / hộp', start: second}].map(item => <div key={item.n} style={{position: 'absolute', left: item.x, width: 650, top: 231, textAlign: 'center', opacity: appear(frame, item.start)}}>
        <div style={{font: '700 23px Arial,sans-serif', letterSpacing: 2, color: p.quiet}}>{item.n}</div>
        <div style={{fontFamily: font, fontSize: 68, fontWeight: 700, marginTop: 5, fontVariantNumeric: 'tabular-nums'}}>{item.total}</div>
        <div style={{marginTop: 346, font: `${motion.stage === 'unit' ? '700' : '400'} 34px Arial,sans-serif`, color: motion.stage === 'unit' ? p.accent : p.quiet, opacity: appear(frame, third)}}>{item.unit}</div>
      </div>)}
      <div style={{position: 'absolute', left: 200, right: 200, top: 797, textAlign: 'center', font: '700 39px Arial,sans-serif', color: p.accent, opacity: appear(frame, third)}}>{motion.stage === 'total' ? 'Mua hai thay vì một: chi thêm 20.000đ' : 'Giá mỗi hộp thấp hơn khi mua hai hộp'}</div>
      <div style={{position: 'absolute', left: 150, right: 150, bottom: 146, textAlign: 'center', font: '18px Arial,sans-serif', color: p.quiet}}>Minh họa bằng hình khối gốc; số tiền giả định, không đại diện giá niêm yết.</div>
    </> : journey ? <>
      {['TRƯỚC KHI ĐI', 'GIỮA KỆ HÀNG', 'TRƯỚC THANH TOÁN'].map((label, i) => <div key={label} style={{position: 'absolute', left: [178, 713, 1248][i], width: 494, top: 822, textAlign: 'center', font: '700 25px Arial,sans-serif', letterSpacing: 1.4, color: frame >= cue(motion, i, duration, [.02, .30, .68][i]) ? p.accent : p.quiet}}>{label}</div>)}
      <div style={{position: 'absolute', left: 88, right: 88, bottom: 146, font: '18px Arial,sans-serif', color: p.quiet, lineHeight: 1.3}}>Ảnh bối cảnh: {credit} · Nhà, kệ, giỏ và tuyến chuyển động: minh họa 3D gốc.</div>
    </> : <>
      {shot.body ? <div style={{position: 'absolute', left: 650, width: 1100, top: 811, font: '31px Arial,sans-serif', lineHeight: 1.35, textAlign: 'center'}}>{shot.body}</div> : null}
      {credit ? <div style={{position: 'absolute', left: 88, right: 88, bottom: 146, font: '18px Arial,sans-serif', color: p.quiet, lineHeight: 1.3}}>Ảnh bối cảnh: {credit} · Giỏ và hộp: minh họa 3D gốc.</div> : null}
    </>}
  </AbsoluteFill>;
};
