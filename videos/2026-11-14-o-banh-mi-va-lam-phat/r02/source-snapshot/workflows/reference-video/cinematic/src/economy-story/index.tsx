import React, {useEffect, useState} from 'react';
import {AbsoluteFill, CanvasImage, cancelRender, continueRender, delayRender, interpolate, staticFile, useCurrentFrame} from 'remotion';
import {CharacterV2} from '../finance-cast-v2';
import './fonts.css';

export const economyFont = '"Economy Be Vietnam Pro", sans-serif';
type Asset = {file: string; credit?: string; fit?: 'cover' | 'contain'; focus?: [number, number]};
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
    {asset.fit === 'contain' && <CanvasImage src={staticFile(asset.file)} style={{position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'cover', filter: 'blur(35px) brightness(.5)'}}/>}
    <CanvasImage src={staticFile(asset.file)} style={{position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: asset.fit ?? 'cover', objectPosition: `${asset.focus?.[0] ?? 50}% ${asset.focus?.[1] ?? 50}%`, scale: asset.fit === 'contain' ? 1 : interpolate(local, [0, duration - 1], [1.025, 1.055], clamp)}}/>
  </AbsoluteFill>;
};

/** This actor is deliberately frozen at frame zero: no breathing, bobbing,
 * blinking, lips, arms, walking, or procedural gestures. Only the outside yaw
 * changes, once per supplied narration cue, while the feet stay anchored. */
const QuietActor: React.FC<{s: EconomySegment; local: number; side?: 'left' | 'right'; dark?: boolean}> = ({s, local, side = 'right', dark = false}) => {
  const cues = s.turnCues?.length ? s.turnCues : [s.cueFrame ?? 0];
  let yaw = -6;
  cues.forEach((cue, i) => {
    const target = i % 2 === 0 ? 7 : -6;
    yaw += (target - (i % 2 === 0 ? -6 : 7)) * smooth((local - cue) / 18);
  });
  return <div style={{position: 'absolute', width: 290, height: 375, bottom: 174, ...(side === 'right' ? {right: 56} : {left: 73}), perspective: 1200}}>
    <div style={{position: 'absolute', left: 30, top: 24, width: 235, height: 302, borderRadius: '48% 48% 35% 35%', background: dark ? 'rgba(243,237,223,.94)' : '#e4dfcf'}}/>
    <svg width={290} height={350} viewBox="0 0 290 350" style={{position: 'absolute', inset: 0, transformOrigin: '50% 95%', transform: `rotateY(${yaw}deg)`}}>
      <CharacterV2 id={2} x={145} y={336} scale={.60} frame={0} pose="idle" emotion="neutral" speaking={false} variant="comic" gaze="center"/>
    </svg>
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
const Items: React.FC<{items: Item[]; top?: number; size?: number}> = ({items, top = 380, size = 64}) => <div style={{position: 'absolute', left: 110, right: 390, top, display: 'flex', gap: 36}}>{items.map((item, i) => <div key={`${item.label}-${i}`} style={{flex: 1, minWidth: 0, paddingTop: 25, borderTop: `4px solid ${item.accent ?? P.green}`}}>
  <div style={{fontSize: 27, color: P.muted, marginBottom: 26, fontWeight: 600, lineHeight: 1.4}}>{item.label}</div>
  <div style={{fontSize: size, fontWeight: 700, letterSpacing: -1.5, lineHeight: 1.27, color: item.accent ?? P.ink, whiteSpace: 'nowrap'}}>{item.value}</div>
  {item.hint && <div style={{fontSize: 25, lineHeight: 1.5, color: P.muted, marginTop: 22}}>{item.hint}</div>}
</div>)}</div>;

const CostStack: React.FC<{s: EconomySegment}> = ({s}) => {
  const d = s.data, price = value(d, 'price', 20000), variable = value(d, 'variable', 12000), fixed = value(d, 'fixed', 5000), remaining = value(d, 'remaining', 3000);
  const parts = [{label: 'Nguyên liệu & chi phí biến đổi', n: variable, color: P.green}, {label: 'Chi phí cố định phân bổ', n: fixed, color: P.gold}, {label: 'Phần còn lại', n: remaining, color: P.rust}];
  return <><div style={{position: 'absolute', left: 111, top: 316, fontSize: 30, color: P.muted}}>Một chiếc bánh bán {money(price)}</div>
    <div style={{position: 'absolute', left: 111, right: 408, top: 414, height: 90, display: 'flex', overflow: 'hidden', borderRadius: 7}}>{parts.map(v => <div key={v.label} style={{width: `${v.n / price * 100}%`, background: v.color}}/>)}</div>
    <div style={{position: 'absolute', left: 111, right: 410, top: 562, display: 'flex', gap: 42}}>{parts.map(v => <div key={v.label} style={{flex: 1, borderLeft: `5px solid ${v.color}`, paddingLeft: 22}}><div style={{fontSize: 39, fontWeight: 700}}>{money(v.n)}</div><div style={{fontSize: 25, lineHeight: 1.45, color: P.muted, marginTop: 17}}>{v.label}</div></div>)}</div>
  </>;
};

const GraphicBody: React.FC<{s: EconomySegment; local: number}> = ({s, local}) => {
  const d = s.data, kind = s.graphic ?? 'flow';
  if (kind === 'price_path' || kind === 'price' || kind === 'index') {
    const vals = list(d, 'values').map(Number); const amounts = vals.length ? vals : [20000, 22000, 22440];
    const labels = list(d, 'labels').map(String); const rates = list(d, 'rates').map(Number);
    const count = d?.stage === 1 ? 2 : 3;
    return <Items items={amounts.slice(0, count).map((v, i) => ({label: labels[i] ?? ['Ban đầu', 'Năm thứ nhất', 'Năm thứ hai'][i], value: money(v), hint: i > 0 ? `${(rates[i - 1] ?? 0) < 0 ? 'Giảm' : 'Tăng'} ${num(Math.abs(rates[i - 1] ?? 0))}%` : 'Mốc so sánh', accent: i === 2 ? P.rust : P.green}))} size={57}/>;
  }
  if (kind === 'cost_stack' || kind === 'cost') return <CostStack s={s}/>;
  if (kind === 'cost_compare' || kind === 'comparison') {
    const before = d?.before as {[key: string]: Datum} | undefined, after = d?.after as {[key: string]: Datum} | undefined;
    return <Items items={[
      {label: 'Trước khi tăng giá', value: money(value(before, 'price', 20000)), hint: `Còn lại ${money(value(before, 'remaining', 3000))}`, accent: P.green},
      {label: 'Sau khi tăng giá', value: money(value(after, 'price', 22000)), hint: `Còn lại ${money(value(after, 'remaining', 2500))}`, accent: P.rust},
    ]} size={70}/>;
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
    return <Items items={d?.stage === 'income-prices' ? wageItems.slice(0, 2) : wageItems} size={65}/>;
  }
  if (kind === 'unit_price') return <Items items={[
    {label: 'Trước đây', value: `${value(d, 'weightBefore', 100)} g`, hint: `Giá ${money(value(d, 'priceBefore', 20000))}`},
    {label: 'Bây giờ', value: `${value(d, 'weightAfter', 90)} g`, hint: `Giá ${money(value(d, 'priceAfter', 20000))}`},
    {label: 'Giá trên mỗi gram', value: `+${num(value(d, 'increasePercent', 11.1111))}%`, hint: 'Cùng số tiền, ít hàng hơn', accent: P.rust},
  ]} size={65}/>;
  const labels = list(d, 'labels').length ? list(d, 'labels').map(String) : list(d, 'items').map(String);
  const words = (labels.length ? labels : ['Chi phí đầu vào', 'Giá bán', 'Sức mua']).slice(0, 4);
  const active = Math.max(0, Math.min(words.length - 1, Math.floor(smooth((local - (s.cueFrame ?? 0)) / Math.max(30, s.duration * .65)) * words.length)));
  return <div style={{position: 'absolute', left: 111, right: 420, top: 355, display: 'flex', alignItems: 'center', gap: 25}}>{words.map((t, i) => <React.Fragment key={t}><div style={{flex: 1, borderTop: `5px solid ${i <= active ? P.green : '#c7d1c1'}`, padding: '35px 0', fontSize: words.length > 3 ? 31 : 38, lineHeight: 1.4, fontWeight: 600, color: i <= active ? P.ink : P.muted}}>{t}</div>{i < words.length - 1 && <div style={{fontSize: 36, color: P.gold}}>→</div>}</React.Fragment>)}</div>;
};

const GraphicScene: React.FC<{s: EconomySegment; local: number}> = ({s, local}) => <AbsoluteFill style={{background: P.paper}}>
  <div style={{position: 'absolute', width: 540, height: 540, borderRadius: '50%', right: -230, top: 290, background: '#e5ddc8'}}/>
  <Chapter s={s}/><Heading text={s.headline} width={1580} size={s.headline.length > 62 ? 56 : 65} style={{position: 'absolute', left: 111, top: 139}}/>
  <GraphicBody s={s} local={local}/><QuietActor s={s} local={local}/>
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
