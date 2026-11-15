import React from 'react';
import {AbsoluteFill, CanvasImage, interpolate, staticFile} from 'remotion';
import {clamp, getAsset, getPosition, type FinancePhotoPlan, type PhotoAsset, type PhotoFocus, type PhotoShot, type PhotoStyle} from './types';

type Cell = {x: number; y: number; w: number; h: number; asset: PhotoAsset; focus?: PhotoFocus};
const focusFor = (shot: PhotoShot, asset: PhotoAsset): PhotoFocus | undefined => {
  const f = shot.focus;
  if (f && !Array.isArray(f) && typeof f === 'object' && !('x' in f)) return f[asset.id];
  return (f as PhotoFocus | undefined) ?? asset.focus;
};
const cellsFor = (shot: PhotoShot, plan: FinancePhotoPlan, style: PhotoStyle): Cell[] => {
  const assets = shot.assets.map(id => getAsset(plan, id));
  if (!assets.length) throw new Error(`Photo shot ${shot.id} requires at least one real photograph.`);
  const cell = (i: number, x: number, y: number, w: number, h: number): Cell => ({x, y, w, h, asset: assets[i], focus: focusFor(shot, assets[i])});
  if (assets.length === 1 || shot.layout === 'full') return [cell(0, 0, 0, 1920, 1080)];
  if (assets.length === 2 || shot.layout === 'split') {
    const edge = style === 'comic' ? 1090 : 960;
    return [cell(0, 0, 0, edge - 2, 1080), cell(1, edge + 2, 0, 1918 - edge, 1080)];
  }
  // Three photographs remain large: one main image and two supporting details.
  const edge = style === 'comic' ? 1200 : 1240;
  return [cell(0, 0, 0, edge - 2, 1080), cell(1, edge + 2, 0, 1918 - edge, 538), cell(2, edge + 2, 542, 1918 - edge, 538)];
};

export const PhotoStage: React.FC<{shot: PhotoShot; plan: FinancePhotoPlan; frame: number; index: number; style: PhotoStyle}> = ({shot, plan, frame, index, style}) => {
  const f = clamp((frame - shot.from) / Math.max(1, shot.duration - 1));
  const cells = cellsFor(shot, plan, style);
  return <AbsoluteFill style={{backgroundColor: '#172224'}}>
    {cells.map((cell, i) => <div key={`${shot.id}-${cell.asset.id}-${i}`} style={{position: 'absolute', left: cell.x, top: cell.y, width: cell.w, height: cell.h, overflow: 'hidden'}}>
      {cell.asset.fit === 'contain' && <CanvasImage src={staticFile(cell.asset.file)} style={{width: '100%', height: '100%', objectFit: 'cover', filter: 'blur(35px) brightness(.55)', scale: '1.12'}}/>}
      <CanvasImage src={staticFile(cell.asset.file)} style={{
        position: 'absolute', inset: 0, width: '100%', height: '100%',
        objectFit: cell.asset.fit ?? 'cover', objectPosition: getPosition(cell.focus),
        scale: cell.asset.fit === 'contain' ? '1' : interpolate(f, [0, 1], index % 2 ? [1.065, 1.025] : [1.025, 1.065]),
        translate: cell.asset.fit === 'contain' ? '0px 0px' : `${interpolate(f, [0, 1], (index + i) % 2 ? [13, -13] : [-13, 13])}px ${interpolate(f, [0, 1], i % 2 ? [-5, 5] : [5, -5])}px`,
        filter: style === 'comic' ? 'saturate(1.065) contrast(1.035)' : 'saturate(.96) contrast(1.025)',
      }}/>
    </div>)}
    <AbsoluteFill style={{background: 'linear-gradient(180deg,rgba(0,0,0,.15),transparent 24%,transparent 62%,rgba(0,0,0,.62) 100%)'}}/>
    <AbsoluteFill style={{boxShadow: 'inset 0 0 160px rgba(0,0,0,.13)', pointerEvents: 'none'}}/>
  </AbsoluteFill>;
};
