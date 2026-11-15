import React, {useEffect, useState} from 'react';
import {AbsoluteFill, CanvasImage, cancelRender, continueRender, delayRender, interpolate, staticFile, useCurrentFrame} from 'remotion';
import {CharacterV2} from '../finance-cast-v2';
import './fonts.css';

export const economyFont = '"Economy Be Vietnam Pro", sans-serif';
type Asset = {file: string; backgroundFile?: string; credit?: string; fit?: 'cover' | 'contain'; focus?: [number, number]};
type Datum = string | number | boolean | null | Datum[] | {[key: string]: Datum};
export type EconomySegment = {
  id: string; from: number; duration: number; cueFrame: number; headline: string; text: string;
  chapterTitle: string; chapterIndex: number; visual: 'photo' | 'graphic'; assetTag: string;
  kind?: string; graphic?: string; data?: {[key: string]: Datum}; turnCues?: number[];
};
export type EconomyPlan = {
  fps: number; durationFrames: number; title: string; segments: EconomySegment[];
  captions: {from: number; end: number; text: string}[];
  assets: Record<string, Asset[]>;
};
export type EconomyStoryProps = {plan: EconomyPlan; offset?: number; frames?: number};

const P = {paper: '#f3eddf', ink: '#223d39', green: '#267260', gold: '#d9ac57', rust: '#bf5f40', muted: '#77847b', soft: '#dfe6d7'};
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const smooth = (n: number) => {const t = Math.max(0, Math.min(1, n)); return t * t * (3 - 2 * t);};
const num = (n: number) => n.toLocaleString('vi-VN', {maximumFractionDigits: 2});
const money = (n: number) => `${num(n)} đ`;
const value = (d: EconomySegment['data'], key: string, fallback: number) => typeof d?.[key] === 'number' ? Number(d[key]) : fallback;
const list = (d: EconomySegment['data'], key: string): Datum[] => Array.isArray(d?.[key]) ? d[key] as Datum[] : [];

/** All three weights are shipped with the source bundle. Rendering waits for the
 * actual Vietnamese fonts, so fallback metrics never determine the saved frame. */
const LocalFonts: React.FC = () => {
  const [handle] = useState(() => delayRender('Loading local Be Vietnam Pro fonts'));
  useEffect(() => {
    Promise.all([400, 600, 700].map(w => document.fonts.load(`${w} 32px "Economy Be Vietnam Pro"`, 'Tiếng Việt Ắ ầ ệ Ữ ỹ')))
      .then(() => document.fonts.ready).then(() => continueRender(handle)).catch(cancelRender);
  }, [handle]);
  return null;
};

const Photograph: React.FC<{asset?: Asset; local: number; duration: number; style?: React.CSSProperties}> = ({asset, local, duration, style}) => {
  if (!asset) return <AbsoluteFill style={{background: P.soft, ...style}}/>;
  return <AbsoluteFill style={{overflow: 'hidden', background: '#1c342f', ...style}}>
    {asset.fit === 'contain' && asset.backgroundFile && <CanvasImage src={staticFile(asset.backgroundFile)} style={{position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'cover'}}/>}
    <CanvasImage src={staticFile(asset.file)} style={{position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: asset.fit ?? 'cover', objectPosition: `${asset.focus?.[0] ?? 50}% ${asset.focus?.[1] ?? 50}%`, scale: asset.fit === 'contain' ? 1 : interpolate(local, [0, duration - 1], [1.025, 1.055], clamp)}}/>
  </AbsoluteFill>;
};

type Action = 'bread' | 'receipt' | 'coins' | 'point' | 'count';

/** Choose a physical action from the spoken subject. The action is intentionally
 * small and repeatable: it gives the narration a visible subject/object/state
 * without pretending to be phoneme lip-sync or a new generated performance. */
const actionFor = (s: EconomySegment): Action => {
  const text = `${s.assetTag} ${s.headline} ${s.text}`.toLocaleLowerCase('vi-VN');
  if (s.visual === 'graphic') {
    if (s.graphic === 'cost_stack' || s.graphic === 'cost_compare' || s.graphic === 'real_wage' || s.graphic === 'unit_price' || s.graphic === 'basket') return 'count';
    return 'point';
  }
  if (/bánh|bột|tiệm|lò|bữa sáng|bakery|bread|flour/.test(text)) return 'bread';
  if (/hóa đơn|biên lai|thu nhập|lương|giỏ|receipt|wage|household/.test(text)) return 'receipt';
  if (/tiền|đồng|giá|chi phí|money|cash|coin/.test(text)) return 'coins';
  return 'point';
};

const BreadProp: React.FC<{progress: number}> = ({progress}) => <svg width="118" height="68" viewBox="0 0 118 68" style={{position: 'absolute', left: interpolate(progress, [0, .32, .72, 1], [68, 146, 184, 132], clamp), top: interpolate(progress, [0, .32, .72, 1], [206, 165, 150, 178], clamp), opacity: interpolate(progress, [0, .08, .92, 1], [0, 1, 1, .85], clamp), transform: `rotate(${interpolate(progress, [0, 1], [-22, 7], clamp)}deg)`}}>
  <path d="M8 42Q8 22 30 17L91 13Q111 14 112 32L109 48Q103 58 83 56L25 58Q8 56 8 42Z" fill="#d88445" stroke="#462d2a" strokeWidth="4"/>
  <path d="M31 19Q27 32 29 55M48 16Q45 29 47 55M65 15Q61 29 65 55M82 14Q80 26 83 55" fill="none" stroke="#f7cf85" strokeWidth="4" strokeLinecap="round"/>
  <path d="M21 39Q55 28 101 33" fill="none" stroke="#fff3d1" strokeWidth="3" opacity=".72"/>
</svg>;

const ReceiptProp: React.FC<{progress: number}> = ({progress}) => <div style={{position: 'absolute', left: interpolate(progress, [0, .3, .72, 1], [74, 158, 194, 138], clamp), top: interpolate(progress, [0, .3, .72, 1], [213, 158, 142, 176], clamp), width: interpolate(progress, [0, .45, 1], [34, 70, 82], clamp), height: interpolate(progress, [0, .45, 1], [46, 94, 108], clamp), background: '#fffdf3', border: '3px solid #35453f', borderRadius: 5, opacity: interpolate(progress, [0, .07, .94, 1], [0, 1, 1, .8], clamp), transform: `rotate(${interpolate(progress, [0, 1], [18, -8], clamp)}deg)`, boxShadow: '3px 4px 0 rgba(30,48,42,.18)'}}>
  <div style={{margin: '12px 10px', height: 4, background: P.rust, boxShadow: '0 13px #98a39a, 0 26px #98a39a, 0 39px #d9ac57'}}/>
</div>;

const CoinsProp: React.FC<{progress: number}> = ({progress}) => <div style={{position: 'absolute', left: interpolate(progress, [0, .4, .72, 1], [78, 164, 198, 145], clamp), top: interpolate(progress, [0, .4, .72, 1], [244, 208, 188, 216], clamp), width: 88, height: 56, opacity: interpolate(progress, [0, .08, .94, 1], [0, 1, 1, .8], clamp), transform: `translate(${interpolate(progress, [0, .5, 1], [18, 0, 9], clamp)}px,${interpolate(progress, [0, .6, 1], [14, -6, 0], clamp)}px)`}}>
  {[{x: 14, y: 31, r: 16, c: P.gold}, {x: 39, y: 23, r: 17, c: '#e4c97e'}, {x: 64, y: 31, r: 16, c: P.gold}].map((coin, i) => <svg key={i} x={coin.x-coin.r} y={coin.y-coin.r} width={coin.r*2} height={coin.r*2} viewBox="0 0 40 40"><circle cx="20" cy="20" r="17" fill={coin.c} stroke="#6e5530" strokeWidth="3"/><path d="M14 13h12M14 20h12M14 27h12" stroke="#8d7139" strokeWidth="2"/></svg>)}
</div>;

const PointerProp: React.FC<{progress: number}> = ({progress}) => <svg width="210" height="90" viewBox="0 0 210 90" style={{position: 'absolute', left: interpolate(progress, [0, .42, 1], [28, 120, 80], clamp), top: interpolate(progress, [0, .42, 1], [228, 187, 202], clamp), opacity: interpolate(progress, [0, .12, .92, 1], [0, 1, 1, .7], clamp), transform: `rotate(${interpolate(progress, [0, 1], [18, -4], clamp)}deg)`}}>
  <path d="M10 62Q74 15 180 27" fill="none" stroke={P.gold} strokeWidth="10" strokeLinecap="round" opacity=".9"/>
  <path d="M176 12L202 27 178 45" fill="none" stroke={P.rust} strokeWidth="9" strokeLinecap="round" strokeLinejoin="round"/>
</svg>;

const CountProp: React.FC<{progress: number}> = ({progress}) => <div style={{position: 'absolute', left: interpolate(progress, [0, .35, .72, 1], [72, 154, 190, 136], clamp), top: interpolate(progress, [0, .35, .72, 1], [240, 205, 180, 212], clamp), width: 110, height: 80, opacity: interpolate(progress, [0, .1, .9, 1], [0, 1, 1, .75], clamp)}}>
  {[0, 1, 2, 3].map((i) => <div key={i} style={{position: 'absolute', left: i * 22, bottom: i * 7, width: 35, height: 17 + i * 4, borderRadius: 5, background: i < Math.ceil(progress * 4) ? [P.green, P.gold, P.rust, '#82978b'][i] : '#c7d1c1', border: '2px solid #38524b'}}/>)}</div>;

const ActionProp: React.FC<{action: Action; progress: number}> = ({action, progress}) => action === 'bread' ? <BreadProp progress={progress}/> : action === 'receipt' ? <ReceiptProp progress={progress}/> : action === 'coins' ? <CoinsProp progress={progress}/> : action === 'count' ? <CountProp progress={progress}/> : action === 'point' ? <PointerProp progress={progress}/> : null;

/** The former QuietActor froze a frame-0 idle pose. This actor remains anchored
 * but unfolds one content-specific action: the prop enters, the hand reaches or
 * points, and the action settles before the next clause. */
const QuietActor: React.FC<{s: EconomySegment; local: number; side?: 'left' | 'right'; dark?: boolean}> = ({s, local, side = 'right', dark = false}) => {
  const cues = s.turnCues?.length ? s.turnCues : [s.cueFrame ?? 0];
  const action = actionFor(s);
  const duration = Math.max(1, s.duration);
  const progress = smooth(Math.min(1, local / Math.max(18, duration * .68)));
  const cueIndex = cues.reduce((n, cue) => n + (local >= cue ? 1 : 0), 0);
  const cueSwing = cueIndex % 2 === 0 ? 0 : 1;
  const yaw = interpolate(smooth(Math.min(1, local / 20)), [0, 1], [-7, 7], clamp) + (cueSwing ? -3 : 0);
  const gestureProgress = smooth(Math.max(0, Math.min(1, (local - Math.min(42, duration * .12)) / Math.max(30, duration * .42))));
  const pose = action === 'bread' ? (gestureProgress < .18 ? 'idle' : gestureProgress < .62 ? 'receive' : 'give')
    : action === 'receipt' ? (gestureProgress < .20 ? 'idle' : gestureProgress < .68 ? 'receive' : 'point')
      : action === 'coins' ? (gestureProgress < .16 ? 'idle' : gestureProgress < .62 ? 'give' : 'receive')
        : action === 'count' ? (gestureProgress < .22 ? 'idle' : gestureProgress < .70 ? 'point' : 'talk') : (gestureProgress < .25 ? 'idle' : 'point');
  const emotion = action === 'coins' || action === 'count' ? 'thinking' : action === 'bread' ? 'happy' : 'neutral';
  const gaze = pose === 'point' ? 'right' : pose === 'receive' || pose === 'give' ? 'left' : 'center';
  return <div style={{position: 'absolute', width: 290, height: 375, bottom: 174, ...(side === 'right' ? {right: 56} : {left: 73}), perspective: 1200}}>
    <div style={{position: 'absolute', left: 30, top: 24, width: 235, height: 302, borderRadius: '48% 48% 35% 35%', background: dark ? 'rgba(243,237,223,.94)' : '#e4dfcf'}}/>
    <div style={{position: 'absolute', inset: 0, transformOrigin: '50% 95%', transform: `rotateY(${yaw}deg) translateY(${interpolate(gestureProgress, [0, .2, .55, 1], [0, 0, -5, 0], clamp)}px)`}}>
      <ActionProp action={action} progress={progress}/>
      <svg width={290} height={350} viewBox="0 0 290 350" style={{position: 'absolute', inset: 0}}>
        <CharacterV2 id={2} x={145} y={336} scale={.60} frame={Math.round(local * .7)} pose={pose} emotion={emotion} speaking={false} variant="comic" gaze={gaze}/>
      </svg>
    </div>
    <div style={{position: 'absolute', top: 352, width: '100%', textAlign: 'center', fontSize: 16, color: dark ? '#eee7d9' : P.muted}}>Nhân vật hư cấu</div>
  </div>;
};

const Chapter: React.FC<{s: EconomySegment; dark?: boolean}> = ({s, dark}) => <div style={{position: 'absolute', left: 82, top: 49, display: 'flex', alignItems: 'center', gap: 20, color: dark ? '#efe9db' : P.ink}}>
  <div style={{width: 42, height: 3, background: dark ? P.gold : P.green}}/>
  <div style={{fontSize: 22, fontWeight: 600, letterSpacing: .25}}>{s.chapterTitle}</div>
</div>;

const Heading: React.FC<{text: string; dark?: boolean; width?: number; size?: number; style?: React.CSSProperties}> = ({text, dark, width = 1110, size, style}) => <div style={{fontSize: size ?? (text.length > 73 ? 58 : text.length > 46 ? 67 : 76), fontWeight: 700, lineHeight: 1.27, letterSpacing: -1.1, maxWidth: width, color: dark ? '#fff6e6' : P.ink, ...style}}>{text}</div>;

const DisclaimerScene: React.FC<{s: EconomySegment; asset?: Asset; local: number}> = ({s, asset, local}) => <AbsoluteFill style={{background: P.paper}}>
  <div style={{position: 'absolute', left: 990, right: 70, top: 134, bottom: 170, borderRadius: 22, overflow: 'hidden'}}><Photograph asset={asset} local={local} duration={s.duration}/></div>
  <Chapter s={s}/><Heading text="MIỄN TRỪ TRÁCH NHIỆM" width={790} size={49} style={{position: 'absolute', top: 252, left: 83}}/>
  <div style={{position: 'absolute', left: 85, top: 416, width: 770, color: P.ink, fontSize: 36, lineHeight: 1.55}}>Câu chuyện và các phép tính là ví dụ minh họa.<br/><br/>Không phải tư vấn tài chính cá nhân.</div>
</AbsoluteFill>;

const PhotoScene: React.FC<{s: EconomySegment; assets: Asset[]; local: number; index: number}> = ({s, assets, local, index}) => {
  const layout = index % 4;
  const chosen = assets[index % Math.max(1, assets.length)];
  const second = assets.length > 1 ? assets[(index + 1) % assets.length] : chosen;
  if (layout === 0) return <AbsoluteFill>
    <Photograph asset={chosen} local={local} duration={s.duration}/>
    <AbsoluteFill style={{background: 'linear-gradient(90deg,rgba(11,30,24,.86),rgba(11,30,24,.4) 55%,rgba(11,30,24,.12)),linear-gradient(0deg,rgba(11,30,24,.6),transparent 45%)'}}/>
    <Chapter s={s} dark/><Heading text={s.headline} dark width={1130} style={{position: 'absolute', left: 82, top: 243}}/>
    <QuietActor s={s} local={local} dark/>
    <div style={{position: 'absolute', left: 85, bottom: 174, color: '#e6e4d5', fontSize: 17}}>Ảnh minh họa{chosen?.credit ? ` · ${chosen.credit}` : ''}</div>
  </AbsoluteFill>;
  if (layout === 1) return <AbsoluteFill style={{background: P.paper}}>
    <div style={{position: 'absolute', left: 745, top: 0, right: 0, bottom: 0}}><Photograph asset={chosen} local={local} duration={s.duration}/></div>
    <div style={{position: 'absolute', left: 745, top: 0, right: 0, bottom: 0, background: 'linear-gradient(0deg,rgba(14,31,24,.65),transparent 45%)'}}/>
    <Chapter s={s}/><Heading text={s.headline} width={580} size={s.headline.length > 52 ? 53 : 64} style={{position: 'absolute', left: 82, top: 221}}/>
    <QuietActor s={s} local={local} side="left"/>
    <div style={{position: 'absolute', left: 791, bottom: 176, color: '#eee5d7', fontSize: 17}}>Ảnh minh họa{chosen?.credit ? ` · ${chosen.credit}` : ''}</div>
  </AbsoluteFill>;
  if (layout === 2) return <AbsoluteFill style={{background: P.paper}}>
    <Chapter s={s}/><Heading text={s.headline} width={1670} size={57} style={{position: 'absolute', left: 82, top: 116}}/>
    <div style={{position: 'absolute', left: 82, width: 1110, top: 294, bottom: 164, overflow: 'hidden', borderRadius: 15}}><Photograph asset={chosen} local={local} duration={s.duration}/></div>
    <div style={{position: 'absolute', right: 80, width: 620, top: 294, bottom: 164, overflow: 'hidden', borderRadius: 15}}><Photograph asset={second} local={local} duration={s.duration}/></div>
    <QuietActor s={s} local={local} side="right"/>
    <div style={{position: 'absolute', left: 99, bottom: 186, color: 'white', background: 'rgba(15,34,25,.7)', borderRadius: 4, padding: '8px 13px', fontSize: 16}}>Ảnh minh họa</div>
  </AbsoluteFill>;
  return <AbsoluteFill style={{background: '#183d32'}}>
    <div style={{position: 'absolute', left: 71, top: 130, width: 1055, bottom: 170, borderRadius: 14, overflow: 'hidden'}}><Photograph asset={chosen} local={local} duration={s.duration}/></div>
    <Chapter s={s} dark/><Heading text={s.headline} dark width={620} size={s.headline.length > 57 ? 54 : 62} style={{position: 'absolute', left: 1190, top: 204}}/>
    <QuietActor s={s} local={local} dark/>
    <div style={{position: 'absolute', left: 90, bottom: 191, color: 'white', fontSize: 17, background: 'rgba(15,34,25,.65)', padding: '6px 11px', borderRadius: 4}}>Ảnh minh họa</div>
  </AbsoluteFill>;
};

type Item = {label: string; value: string; hint?: string; accent?: string};
const Items: React.FC<{items: Item[]; top?: number; size?: number; reveal?: number}> = ({items, top = 380, size = 64, reveal = 1}) => <div style={{position: 'absolute', left: 110, right: 390, top, display: 'flex', gap: 36}}>{items.map((item, i) => {
  const shown = smooth((reveal - i * .22) / .56);
  return <div key={`${item.label}-${i}`} style={{flex: 1, minWidth: 0, paddingTop: 25, borderTop: `4px solid ${item.accent ?? P.green}`, opacity: shown, translate: `0 ${interpolate(shown, [0, 1], ['26px', '0px'], clamp)}`}}>
  <div style={{fontSize: 27, color: P.muted, marginBottom: 26, fontWeight: 600, lineHeight: 1.4}}>{item.label}</div>
  <div style={{fontSize: size, fontWeight: 700, letterSpacing: -1.5, lineHeight: 1.27, color: item.accent ?? P.ink, whiteSpace: 'nowrap'}}>{item.value}</div>
  {item.hint && <div style={{fontSize: 25, lineHeight: 1.5, color: P.muted, marginTop: 22}}>{item.hint}</div>}
</div>;
})}</div>;

const GraphicMotion: React.FC<{s: EconomySegment; local: number}> = ({s, local}) => {
  const kind = s.graphic ?? 'flow';
  const t = smooth((local - Math.min(22, s.duration * .10)) / Math.max(32, s.duration * .58));
  const stroke = '#365e55';
  if (kind === 'price_path' || kind === 'price' || kind === 'index') {
    const vals = list(s.data, 'values').map(Number); const labels = list(s.data, 'labels').map(String);
    const count = s.data?.stage === 1 ? 2 : 3; const safe = (vals.length ? vals : [20000, 22000, 22440]).slice(0, count);
    const x = (i: number) => 170 + i * (760 / Math.max(1, safe.length - 1));
    return <svg width="920" height="92" viewBox="0 0 920 92" style={{position: 'absolute', left: 108, top: 268, overflow: 'visible'}}>
      <path d={`M${x(0)} 46H${x(Math.max(0, safe.length - 1))}`} stroke="#c7d1c1" strokeWidth="7" strokeLinecap="round"/>
      {safe.map((amount, i) => {const appear = smooth((t - i * .20) / .46); const px = x(i); return <g key={amount} opacity={appear} transform={`translate(${px} ${46 + Math.sin(Math.min(1, appear) * Math.PI) * -17})`}>
        <circle r="27" fill={i === safe.length - 1 ? P.rust : P.green} stroke="#f3eddf" strokeWidth="5"/>
        <text y="6" textAnchor="middle" fontSize="15" fontWeight="700" fill="#fff9eb">{labels[i] ?? `${i + 1}`}</text>
      </g>;})}
      {safe.slice(0, -1).map((_, i) => <path key={i} d={`M${x(i)+35} 46L${x(i+1)-36} 46`} stroke={stroke} strokeWidth="4" strokeDasharray="10 8" strokeDashoffset={interpolate(t, [0, 1], [40, 0], clamp)}/>) }
    </svg>;
  }
  if (kind === 'cost_stack' || kind === 'cost' || kind === 'cost_compare' || kind === 'comparison') {
    const widths = kind === 'cost_stack' || kind === 'cost' ? [60, 25, 15] : [50, 50];
    const colors = [P.green, P.gold, P.rust];
    return <div style={{position: 'absolute', left: 111, right: 408, top: 280, height: 22, display: 'flex', overflow: 'hidden', borderRadius: 6, background: '#dfe6d7'}}>
      {widths.map((w, i) => <div key={i} style={{width: `${w * smooth((t - i * .22) / .5)}%`, background: colors[i], height: '100%'}}/>)}
    </div>;
  }
  if (kind === 'basket') {
    const weights = list(s.data, 'weights').map(Number); const colors = [P.rust, P.green, P.gold, '#82978b'];
    return <div style={{position: 'absolute', left: 111, right: 430, top: 280, height: 22, display: 'flex', overflow: 'hidden', borderRadius: 6, background: '#dfe6d7'}}>
      {weights.map((w, i) => <div key={i} style={{width: `${w * smooth((t - i * .14) / .5)}%`, background: colors[i % colors.length], height: '100%'}}/>)}
    </div>;
  }
  if (kind === 'unit_price') return <svg width="900" height="100" viewBox="0 0 900 100" style={{position: 'absolute', left: 108, top: 260, overflow: 'visible'}}>
    <rect x="20" y="28" width={interpolate(t, [0, 1], [0, 270], clamp)} height="34" rx="8" fill={P.green}/><rect x="330" y="28" width={interpolate(t, [0, 1], [0, 390], clamp)} height="34" rx="8" fill={P.rust}/>
    <text x="20" y="18" fontSize="20" fill={P.muted}>100 g</text><text x="330" y="18" fontSize="20" fill={P.muted}>90 g cùng giá</text>
  </svg>;
  const labels = list(s.data, 'labels').length ? list(s.data, 'labels').map(String) : list(s.data, 'items').map(String);
  const nodes = (labels.length ? labels : ['Chi phí', 'Giá bán', 'Sức mua']).slice(0, 4);
  return <svg width="930" height="100" viewBox="0 0 930 100" style={{position: 'absolute', left: 108, top: 260, overflow: 'visible'}}>
    {nodes.map((label, i) => {const q = smooth((t - i * .18) / .45); const px = 70 + i * (760 / Math.max(1, nodes.length - 1)); return <g key={label} opacity={q}><circle cx={px} cy="48" r="27" fill={i === nodes.length - 1 ? P.rust : P.green}/><text x={px} y="54" textAnchor="middle" fontSize="16" fontWeight="700" fill="#fff9eb">{i + 1}</text>{i < nodes.length - 1 && <path d={`M${px+34} 48H${px+760 / Math.max(1, nodes.length - 1)-42}`} stroke={P.gold} strokeWidth="5" strokeDasharray="12 8" strokeDashoffset={interpolate(q, [0, 1], [50, 0], clamp)}/>}</g>;})}
  </svg>;
};

const CostStack: React.FC<{s: EconomySegment; local: number}> = ({s, local}) => {
  const d = s.data, price = value(d, 'price', 20000), variable = value(d, 'variable', 12000), fixed = value(d, 'fixed', 5000), remaining = value(d, 'remaining', 3000);
  const fill = smooth((local - Math.min(24, s.duration * .08)) / Math.max(36, s.duration * .55));
  const parts = [{label: 'Nguyên liệu & chi phí biến đổi', n: variable, color: P.green}, {label: 'Chi phí cố định phân bổ', n: fixed, color: P.gold}, {label: 'Phần còn lại', n: remaining, color: P.rust}];
  return <><div style={{position: 'absolute', left: 111, top: 316, fontSize: 30, color: P.muted}}>Một chiếc bánh bán {money(price)}</div>
    <div style={{position: 'absolute', left: 111, right: 408, top: 414, height: 90, display: 'flex', overflow: 'hidden', borderRadius: 7, background: '#dfe6d7'}}>{parts.map((v, i) => <div key={v.label} style={{width: `${v.n / price * 100 * smooth((fill - i * .16) / .48)}%`, background: v.color}}/>)}</div>
    <div style={{position: 'absolute', left: 111, right: 410, top: 562, display: 'flex', gap: 42}}>{parts.map((v, i) => <div key={v.label} style={{flex: 1, borderLeft: `5px solid ${v.color}`, paddingLeft: 22, opacity: smooth((fill - i * .12) / .45), translate: `0 ${interpolate(smooth((fill - i * .12) / .45), [0, 1], ['20px', '0px'], clamp)}`}}><div style={{fontSize: 39, fontWeight: 700}}>{money(v.n)}</div><div style={{fontSize: 25, lineHeight: 1.45, color: P.muted, marginTop: 17}}>{v.label}</div></div>)}</div>
  </>;
};

const GraphicBody: React.FC<{s: EconomySegment; local: number}> = ({s, local}) => {
  const d = s.data, kind = s.graphic ?? 'flow';
  const reveal = smooth((local - Math.min(18, s.duration * .08)) / Math.max(36, s.duration * .58));
  if (kind === 'price_path' || kind === 'price' || kind === 'index') {
    const vals = list(d, 'values').map(Number); const amounts = vals.length ? vals : [20000, 22000, 22440];
    const labels = list(d, 'labels').map(String); const rates = list(d, 'rates').map(Number);
    const count = d?.stage === 1 ? 2 : 3;
    return <Items items={amounts.slice(0, count).map((v, i) => ({label: labels[i] ?? ['Ban đầu', 'Năm thứ nhất', 'Năm thứ hai'][i], value: money(v), hint: i > 0 ? `${(rates[i - 1] ?? 0) < 0 ? 'Giảm' : 'Tăng'} ${num(Math.abs(rates[i - 1] ?? 0))}%` : 'Mốc so sánh', accent: i === 2 ? P.rust : P.green}))} size={57} reveal={reveal}/>;
  }
  if (kind === 'cost_stack' || kind === 'cost') return <CostStack s={s} local={local}/>;
  if (kind === 'cost_compare' || kind === 'comparison') {
    const before = d?.before as {[key: string]: Datum} | undefined, after = d?.after as {[key: string]: Datum} | undefined;
    return <Items items={[
      {label: 'Trước khi tăng giá', value: money(value(before, 'price', 20000)), hint: `Còn lại ${money(value(before, 'remaining', 3000))}`, accent: P.green},
      {label: 'Sau khi tăng giá', value: money(value(after, 'price', 22000)), hint: `Còn lại ${money(value(after, 'remaining', 2500))}`, accent: P.rust},
    ]} size={70} reveal={reveal}/>;
  }
  if (kind === 'basket') {
    const labels = list(d, 'items').map(String); const weights = list(d, 'weights').map(Number); const rates = list(d, 'rates').map(Number); const colors = [P.rust, P.green, P.gold, '#82978b'];
    const showRates = d?.stage !== 'weights';
    return <><div style={{position: 'absolute', left: 111, right: 430, top: 348, display: 'flex', height: 76, borderRadius: 7, overflow: 'hidden'}}>{weights.map((w, i) => <div key={i} style={{width: `${w}%`, background: colors[i % 4]}}/>)}</div>
      <div style={{position: 'absolute', left: 111, top: 474, right: 430, display: 'flex', gap: 34}}>{labels.map((t, i) => <div key={t} style={{flex: 1, color: P.muted, fontSize: 24, lineHeight: 1.6}}><div style={{color: colors[i % 4], fontWeight: 700, fontSize: 29}}>{t}</div><div>Tỷ trọng {weights[i]}%</div>{showRates && <div>Giá {rates[i] > 0 ? '+' : ''}{rates[i]}%</div>}</div>)}</div>
      {showRates && <div style={{position: 'absolute', left: 111, top: 716, fontSize: 42, fontWeight: 700}}>Cả rổ chi tiêu: <span style={{color: P.rust}}>+{value(d, 'total', 4)}%</span></div>}
    </>;
  }
  if (kind === 'real_wage' || kind === 'wages') {
    const incomeRatio = value(d, 'incomeAfter', 10500000) / value(d, 'incomeBefore', 10000000);
    const priceRatio = value(d, 'priceIndexAfter', 108) / value(d, 'priceIndexBefore', 100);
    const signed = (n: number) => `${n > 0 ? '+' : ''}${num(n)}%`;
    const wageItems: Item[] = [
      {label: 'Thu nhập danh nghĩa', value: signed((incomeRatio - 1) * 100), hint: `${num(value(d, 'incomeBefore', 10000000) / 1000000)} → ${num(value(d, 'incomeAfter', 10500000) / 1000000)} triệu đồng`},
      {label: 'Giá của rổ hàng', value: signed((priceRatio - 1) * 100), hint: `Chỉ số ${value(d, 'priceIndexBefore', 100)} → ${value(d, 'priceIndexAfter', 108)}`},
      {label: 'Sức mua thực tế', value: signed((incomeRatio / priceRatio - 1) * 100), hint: `${num(incomeRatio * 100)} ÷ ${num(priceRatio * 100)} − 1`, accent: P.rust},
    ];
    return <Items items={d?.stage === 'income-prices' ? wageItems.slice(0, 2) : wageItems} size={65} reveal={reveal}/>;
  }
  if (kind === 'unit_price') return <Items items={[
    {label: 'Trước đây', value: `${value(d, 'weightBefore', 100)} g`, hint: `Giá ${money(value(d, 'priceBefore', 20000))}`},
    {label: 'Bây giờ', value: `${value(d, 'weightAfter', 90)} g`, hint: `Giá ${money(value(d, 'priceAfter', 20000))}`},
    {label: 'Giá trên mỗi gram', value: `+${num(value(d, 'increasePercent', 11.1111))}%`, hint: 'Cùng số tiền, ít hàng hơn', accent: P.rust},
  ]} size={65} reveal={reveal}/>;
  const labels = list(d, 'labels').length ? list(d, 'labels').map(String) : list(d, 'items').map(String);
  const words = (labels.length ? labels : ['Chi phí đầu vào', 'Giá bán', 'Sức mua']).slice(0, 4);
  const active = Math.max(0, Math.min(words.length - 1, Math.floor(smooth((local - (s.cueFrame ?? 0)) / Math.max(30, s.duration * .65)) * words.length)));
  return <div style={{position: 'absolute', left: 111, right: 420, top: 355, display: 'flex', alignItems: 'center', gap: 25}}>{words.map((t, i) => <React.Fragment key={t}><div style={{flex: 1, borderTop: `5px solid ${i <= active ? P.green : '#c7d1c1'}`, padding: '35px 0', fontSize: words.length > 3 ? 31 : 38, lineHeight: 1.4, fontWeight: 600, color: i <= active ? P.ink : P.muted}}>{t}</div>{i < words.length - 1 && <div style={{fontSize: 36, color: P.gold}}>→</div>}</React.Fragment>)}</div>;
};

const GraphicScene: React.FC<{s: EconomySegment; local: number}> = ({s, local}) => <AbsoluteFill style={{background: P.paper}}>
  <div style={{position: 'absolute', width: 540, height: 540, borderRadius: '50%', right: -230, top: 290, background: '#e5ddc8'}}/>
  <Chapter s={s}/><Heading text={s.headline} width={1580} size={s.headline.length > 62 ? 56 : 65} style={{position: 'absolute', left: 111, top: 139}}/>
  <GraphicMotion s={s} local={local}/><GraphicBody s={s} local={local}/><QuietActor s={s} local={local}/>
  <div style={{position: 'absolute', left: 111, right: 420, bottom: 166, color: P.muted, fontSize: 20, lineHeight: 1.4}}>SỐ LIỆU MINH HỌA · {typeof s.data?.note === 'string' ? s.data.note : 'Ví dụ giả định để giải thích cơ chế; không phải số liệu thị trường hiện tại.'}</div>
</AbsoluteFill>;

export const EconomyStory: React.FC<EconomyStoryProps> = ({plan, offset = 0}) => {
  const frame = useCurrentFrame() + offset;
  const i = plan.segments.findIndex(s => frame >= s.from && frame < s.from + s.duration);
  const s = plan.segments[Math.max(0, i)];
  const c = plan.captions.find(v => frame >= v.from && frame < v.end);
  if (!s) return <AbsoluteFill style={{background: P.paper}}><LocalFonts/></AbsoluteFill>;
  const local = frame - s.from;
  const disclaimer = s.kind === 'disclaimer' || s.graphic === 'disclaimer' || /disclaimer|miễn trừ/i.test(s.id + s.chapterTitle);
  return <AbsoluteFill style={{fontFamily: economyFont, background: P.paper, color: P.ink, overflow: 'hidden', fontVariantNumeric: 'tabular-nums'}}>
    <LocalFonts/>
    {disclaimer ? <DisclaimerScene s={s} local={local} asset={plan.assets[s.assetTag]?.[0]}/> : s.visual === 'graphic' ? <GraphicScene s={s} local={local}/> : <PhotoScene s={s} local={local} index={Math.max(0, i)} assets={plan.assets[s.assetTag] ?? []}/>}
    {i > 0 && local < 6 && <AbsoluteFill style={{background: P.paper, opacity: 1 - smooth(local / 6)}}/>}
    {c && <div style={{position: 'absolute', left: 100, right: 100, bottom: 32, textAlign: 'center', pointerEvents: 'none'}}><span style={{display: 'inline-block', maxWidth: 1690, background: 'rgba(12,31,26,.93)', color: '#fff9eb', padding: '10px 27px 13px', borderRadius: 8, fontSize: 34, lineHeight: 1.5, fontWeight: 400, textWrap: 'balance'}}>{c.text}</span></div>}
  </AbsoluteFill>;
};
