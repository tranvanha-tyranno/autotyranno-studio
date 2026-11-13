import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {Header, Media, Source, font, localCue, rise, themeFor} from './Shared';
import type {BusinessShot} from './types';

export const PaperScene: React.FC<{shot: BusinessShot; duration: number}> = ({shot, duration}) => {
  const frame = useCurrentFrame();
  const p = themeFor(shot);
  const receipt = shot.design?.paper;
  const intro = rise(frame, 1, 22);
  return <AbsoluteFill style={{background: p.paper, color: p.ink}}>
    <div style={{position: 'absolute', left: 100, top: 268, width: 710, height: 540, overflow: 'hidden', rotate: '-2deg'}}>
      {shot.images[0] ? <Media image={shot.images[0]} duration={duration}/> : null}
      <AbsoluteFill style={{background: 'linear-gradient(0deg,rgba(16,30,21,.6),transparent 60%)'}}/>
      {shot.body ? <div style={{position: 'absolute', left: 35, right: 35, bottom: 36, font: '31px Arial,sans-serif', lineHeight: 1.35, color: '#fff5e3'}}>{shot.body}</div> : null}
    </div>
    <Header shot={shot}/>
    <div style={{position: 'absolute', left: 890, top: 271, width: 862, height: 550, background: p.soft, rotate: '2deg', translate: `${(1 - intro) * 90}px ${(1 - intro) * 50}px`, opacity: intro}}/>
    <div style={{position: 'absolute', left: 875, top: 255, width: 862, minHeight: 570, boxSizing: 'border-box', padding: '35px 45px 38px', background: '#fffaf0', color: '#29352b', boxShadow: '0 18px 44px rgba(32,29,19,.13)', rotate: `${(1 - intro) * 5 - .6}deg`, opacity: intro, translate: `0 ${(1 - intro) * 100}px`, clipPath: 'polygon(0 0,100% 0,100% 98%,98% 100%,96% 98%,94% 100%,92% 98%,90% 100%,88% 98%,86% 100%,84% 98%,82% 100%,80% 98%,78% 100%,76% 98%,74% 100%,72% 98%,70% 100%,68% 98%,66% 100%,64% 98%,62% 100%,60% 98%,58% 100%,56% 98%,54% 100%,52% 98%,50% 100%,48% 98%,46% 100%,44% 98%,42% 100%,40% 98%,38% 100%,36% 98%,34% 100%,32% 98%,30% 100%,28% 98%,26% 100%,24% 98%,22% 100%,20% 98%,18% 100%,16% 98%,14% 100%,12% 98%,10% 100%,8% 98%,6% 100%,4% 98%,2% 100%,0 98%)'}}>
      <div style={{fontFamily: font, fontSize: 35, fontWeight: 700, paddingBottom: 25, borderBottom: '2px dashed #c9c4b4', marginBottom: 9}}>{receipt?.title ?? 'Ví dụ minh họa'}</div>
      {receipt?.rows.slice(0, 5).map((row, i) => <div key={`${row.label}-${i}`} style={{display: 'flex', justifyContent: 'space-between', gap: 25, padding: '19px 0', borderBottom: '1px solid #e9e2d2', font: '30px Arial,sans-serif', opacity: rise(frame, localCue(shot, i, 12 + i * 14)), translate: `0 ${(1 - rise(frame, localCue(shot, i, 12 + i * 14))) * 15}px`}}><span style={{maxWidth: 510}}>{row.label}</span><strong style={{whiteSpace: 'nowrap', fontVariantNumeric: 'tabular-nums'}}>{row.value}</strong></div>)}
      {receipt?.total ? <div style={{display: 'flex', justifyContent: 'space-between', gap: 25, marginTop: 26, font: '700 34px Arial,sans-serif', color: '#b64e32', opacity: rise(frame, localCue(shot, 2, 55))}}><span style={{maxWidth: 475}}>{receipt.total.label}</span><span style={{whiteSpace: 'nowrap', fontVariantNumeric: 'tabular-nums'}}>{receipt.total.value}</span></div> : null}
    </div>
    <Source shot={shot}/>
  </AbsoluteFill>;
};
