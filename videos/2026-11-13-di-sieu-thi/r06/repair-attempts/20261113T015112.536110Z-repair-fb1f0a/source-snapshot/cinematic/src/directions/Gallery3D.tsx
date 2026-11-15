import {useEffect, useMemo} from 'react';
import {useLoader} from '@react-three/fiber';
import {ThreeCanvas} from '@remotion/three';
import {interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import * as THREE from 'three';
import type {DirectionImage, DirectionName} from './types';

const clamped = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;

const PhotoPlane: React.FC<{
  image: DirectionImage;
  size: [number, number];
  accent: string;
  ink: string;
}> = ({image, size, accent, ink}) => {
  // ThreeCanvas' SuspenseLoader holds the render until useLoader has resolved.
  // Clone per panel so repeat/offset never mutate another use of this image.
  const loaded = useLoader(THREE.TextureLoader, staticFile(image.mediaType === 'video' ? image.posterFile! : image.file));
  const [panelWidth, panelHeight] = size;
  const texture = useMemo(() => {
    const copy = loaded.clone();
    const source = loaded.image as {width: number; height: number};
    const sourceAspect = source.width / source.height;
    const targetAspect = panelWidth / panelHeight;
    const [x, y] = image.focus ?? [50, 50];
    copy.colorSpace = THREE.SRGBColorSpace;
    copy.wrapS = THREE.ClampToEdgeWrapping;
    copy.wrapT = THREE.ClampToEdgeWrapping;
    if (sourceAspect > targetAspect) {
      const visible = targetAspect / sourceAspect;
      copy.repeat.set(visible, 1);
      copy.offset.set((1 - visible) * Math.max(0, Math.min(1, x / 100)), 0);
    } else {
      const visible = sourceAspect / targetAspect;
      copy.repeat.set(1, visible);
      copy.offset.set(0, (1 - visible) * Math.max(0, Math.min(1, 1 - y / 100)));
    }
    copy.needsUpdate = true;
    return copy;
  }, [loaded, image.focus, panelWidth, panelHeight]);
  useEffect(() => () => texture.dispose(), [texture]);

  return (
    <group>
      <mesh position={[0, 0, -.065]}>
        <boxGeometry args={[size[0] + .10, size[1] + .10, .10]}/>
        <meshStandardMaterial color={ink} metalness={.25} roughness={.55}/>
      </mesh>
      <mesh>
        <planeGeometry args={size}/>
        <meshBasicMaterial map={texture} toneMapped={false}/>
      </mesh>
      <mesh position={[-size[0] / 2 + .018, 0, .015]}>
        <planeGeometry args={[.036, size[1]]}/>
        <meshBasicMaterial color={accent} toneMapped={false}/>
      </mesh>
    </group>
  );
};

const EvidencePlanes: React.FC<{
  images: DirectionImage[];
  direction: DirectionName;
  duration: number;
}> = ({images, direction, duration}) => {
  const frame = useCurrentFrame();
  const long = direction === 'long';
  const progress = interpolate(frame, [0, Math.max(1, duration - 1)], [0, 1], clamped);
  const entrance = interpolate(frame, [0, long ? 18 : 30], [0, 1], {
    ...clamped,
    easing: t => 1 - Math.pow(1 - t, 3),
  });
  const accent = long ? '#f15f40' : '#7dc4bd';
  const ink = long ? '#292521' : '#182c38';
  const deck = useMemo(() => images.slice(0, 3), [images]);

  return (
    <group position={[long ? -.14 + progress * .28 : .16 - progress * .32, -.10, 0]} rotation={[0, (progress - .5) * (long ? .07 : .045), 0]}>
      {deck.map((image, i) => {
        const middle = i === 1 || deck.length === 1;
        const side = deck.length === 1 ? 0 : i - 1;
        const y = middle ? .12 : long ? -.08 : -.20;
        const maxWidth = middle ? 5.7 : 4.7;
        const maxHeight = middle ? 4.5 : 4.0;
        const aspect = image.aspect ?? 1.5;
        // The frame follows each source ratio, so portrait subjects keep their
        // hands and faces in the 3D interface just as they do in the flat shots.
        const size: [number, number] = [Math.min(maxWidth, maxHeight * aspect), Math.min(maxHeight, maxWidth / aspect)];
        return (
          <group key={`${image.file}-${i}`} position={[side * 4.15, y - (1 - entrance) * (middle ? .3 : .55), middle ? .15 : -.95]} rotation={[0, side * -.13, long ? side * -.035 : 0]}>
            <PhotoPlane image={image} size={size} accent={accent} ink={ink}/>
          </group>
        );
      })}
      {deck.length > 1 ? <>
        <mesh position={[0, -2.70, -1]}>
          <boxGeometry args={[11.5, .014, .025]}/>
          <meshBasicMaterial color={accent} transparent opacity={.5}/>
        </mesh>
        {[-4.15, 0, 4.15].slice(0, deck.length).map((x, i) => <mesh key={x} position={[x, -2.70, -.97]}>
          <sphereGeometry args={[i === 1 ? .055 : .035, 14, 10]}/>
          <meshBasicMaterial color={accent}/>
        </mesh>)}
      </> : null}
    </group>
  );
};

/** Real photographs placed on actual Three.js geometry, with a small camera dolly. */
export const Gallery3D: React.FC<{
  images: DirectionImage[];
  direction: DirectionName;
  duration: number;
}> = ({images, direction, duration}) => {
  const {width, height} = useVideoConfig();
  return (
    <ThreeCanvas width={width} height={height} camera={{fov: 34, position: [0, .1, 12.5]}} gl={{antialias: true, alpha: true}} style={{position: 'absolute', inset: 0}}>
      <ambientLight intensity={1.4}/>
      <directionalLight position={[0, 5, 7]} intensity={2}/>
      <EvidencePlanes images={images} direction={direction} duration={duration}/>
    </ThreeCanvas>
  );
};
