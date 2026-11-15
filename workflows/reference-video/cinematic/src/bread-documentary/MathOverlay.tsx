import React from 'react';
import {interpolate, useCurrentFrame} from 'remotion';
import {clamp, money, number, palette as P} from './theme';
import type {BreadData, BreadShot} from './types';

const numeric = (data: BreadData | undefined, keys: string[], fallback: number) => {
  for (const key of keys) if (typeof data?.[key] === 'number') return Number(data[key]);
  return fallback;
};
const cue = (shot: BreadShot, index: number, fraction: number) => shot.cueFrames?.[index] ?? Math.round(shot.duration * fraction);
const label: React.CSSProperties = {fontSize: 23, color: P.quiet, lineHeight: 1.35};
const small: React.CSSProperties = {fontSize: 20, color: P.quiet, lineHeight: 1.45};

const GraphicHeading: React.FC<{shot: BreadShot}> = ({shot}) => <>
  <div style={{fontSize: 20, letterSpacing: 2.5, textTransform: 'uppercase', color: P.warm, marginBottom: 19}}>{shot.label ?? 'Mô hình minh họa'}</div>
  {shot.headline && <div style={{fontSize: shot.headline.length > 48 ? 40 : 46, lineHeight: 1.22, fontWeight: 600, marginBottom: 34}}>{shot.headline}</div>}
</>;

/** The same selling price is physically divided. Cost rises first; then selling
 * price changes. This makes "paid more, kept less" a process rather than cards. */
const CostStack: React.FC<{shot: BreadShot}> = ({shot}) => {
  const frame = useCurrentFrame();
  const beforePrice = numeric(shot.data, ['beforePrice', 'priceBefore'], 20000);
  const stage = shot.data?.stage;
  const afterPrice = numeric(shot.data, ['afterPrice', 'priceAfter', 'price'], 22000);
  const beforeVariable = numeric(shot.data, ['beforeVariable', 'variableBefore'], 12000);
  const afterVariable = numeric(shot.data, ['afterVariable', 'variableAfter', 'variable'], 14500);
  const fixed = numeric(shot.data, ['fixedPerUnit', 'fixed'], 5000);
  const beforeRemainder = beforePrice - beforeVariable - fixed;
  const afterRemainder = afterPrice - afterVariable - fixed;
  const costCue = stage === 'after' ? cue(shot, 0, .12) : cue(shot, 1, .34);
  const priceCue = cue(shot, 2, .62);
  const deltaCue = cue(shot, 3, .82);
  const barMax = Math.max(beforePrice, afterPrice, beforeVariable + fixed, afterVariable + fixed) * 1.04;
  const amount = stage === 'before' ? numeric(shot.data, ['price'], beforePrice) : frame < priceCue ? beforePrice : afterPrice;
  const variable = stage === 'before' ? numeric(shot.data, ['variable'], beforeVariable) : frame < costCue ? beforeVariable : afterVariable;
  const remainder = amount - variable - fixed;
  const currentState = stage === 'before' ? 'Giá bán trước đổi bảng' : frame < costCue ? 'Trước' : frame < priceCue ? 'Đầu vào tăng · giữ giá cũ' : 'Sau đổi giá';
  if (stage === 'compare') return <>
    <GraphicHeading shot={shot}/>
    <div style={label}>Phần còn lại trên mỗi ổ*</div>
    <div style={{fontSize: 75, fontWeight: 700, letterSpacing: -2, marginTop: 20, display: 'flex', alignItems: 'baseline', gap: 22}}>
      <span>{number(beforeRemainder)}</span><span style={{fontSize: 45, color: P.quiet}}>→</span>
      <span style={{color: P.rust, opacity: interpolate(frame, [cue(shot, 0, .14), cue(shot, 0, .14) + 8], [0, 1], clamp)}}>{number(afterRemainder)}<span style={{fontSize: 28, color: P.quiet}}> đ</span></span>
    </div>
    <div style={{marginTop: 42, height: 4, width: 690, background: 'rgba(255,250,240,.12)'}}><div style={{height: 4, background: P.rust,
      width: interpolate(frame, [cue(shot, 0, .14), cue(shot, 0, .14) + 22], [690, Math.max(0, afterRemainder / Math.max(1, beforeRemainder) * 690)], clamp)}}/></div>
    <div style={{marginTop: 44, opacity: interpolate(frame, [cue(shot, 1, .42), cue(shot, 1, .42) + 8], [0, 1], clamp)}}>
      <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'baseline'}}><span style={label}>Khách trả thêm</span><span style={{fontSize: 44, color: P.white, fontWeight: 600}}>+{money(afterPrice - beforePrice)}</span></div>
      <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginTop: 22}}><span style={label}>Đầu vào tăng</span><span style={{fontSize: 44, color: P.rust, fontWeight: 600}}>+{money(afterVariable - beforeVariable)}</span></div>
    </div>
    <div style={{marginTop: 42, fontSize: 31, color: P.warm, lineHeight: 1.35,
      opacity: interpolate(frame, [cue(shot, 2, .72), cue(shot, 2, .72) + 8], [0, 1], clamp)}}>{shot.emphasis ?? 'Trả thêm ≠ giữ lại thêm'}</div>
    <div style={{...small, marginTop: 23}}>*Khoảng dư trong mô hình, chưa phải lợi nhuận ròng.</div>
  </>;
  return <>
    <GraphicHeading shot={shot}/>
    <div style={{...label, marginBottom: 4}}>{currentState}</div>
    <div style={{fontSize: 89, lineHeight: 1.15, fontWeight: 700, letterSpacing: -2}}>{money(amount)}</div>
    <div style={{height: 62, position: 'relative', marginTop: 32, width: 704}}>
      <div style={{position: 'absolute', top: 0, left: 0, bottom: 0, width: 704, borderBottom: `1px solid ${P.rule}`}}/>
      <div style={{position: 'absolute', left: 0, top: 4, bottom: 4, background: P.rust,
        opacity: stage === 'before' ? interpolate(frame, [cue(shot, 1, .3), cue(shot, 1, .3) + 8], [0, 1], clamp) : 1,
        width: stage === 'before' ? variable / barMax * 704 : interpolate(frame, [costCue, costCue + 22], [beforeVariable / barMax * 704, afterVariable / barMax * 704], clamp)}}/>
      <div style={{position: 'absolute', top: 4, bottom: 4, background: '#b9b5ac',
        opacity: stage === 'before' ? interpolate(frame, [cue(shot, 2, .53), cue(shot, 2, .53) + 8], [0, 1], clamp) : 1,
        left: stage === 'before' ? variable / barMax * 704 : interpolate(frame, [costCue, costCue + 22], [beforeVariable / barMax * 704, afterVariable / barMax * 704], clamp), width: fixed / barMax * 704}}/>
      <div style={{position: 'absolute', top: 4, bottom: 4, background: P.warm,
        opacity: stage === 'before' ? interpolate(frame, [cue(shot, 3, .77), cue(shot, 3, .77) + 8], [0, 1], clamp) : 1,
        left: stage === 'before' ? (variable + fixed) / barMax * 704 : interpolate(frame, [costCue, costCue + 22], [(beforeVariable + fixed) / barMax * 704, (afterVariable + fixed) / barMax * 704], clamp),
        width: stage === 'before' ? remainder / barMax * 704 : Math.max(0, interpolate(frame, [costCue, costCue + 22, Math.max(costCue + 23, priceCue), Math.max(costCue + 24, priceCue + 22)],
          [beforeRemainder / barMax * 704, (beforePrice - afterVariable - fixed) / barMax * 704, (beforePrice - afterVariable - fixed) / barMax * 704, afterRemainder / barMax * 704], clamp))}}/>
    </div>
    <div style={{display: 'flex', gap: 34, marginTop: 24, alignItems: 'flex-start'}}>
      <div style={{width: 218, opacity: stage === 'before' ? interpolate(frame, [cue(shot, 1, .3), cue(shot, 1, .3) + 8], [0, 1], clamp) : 1}}><div style={{...label, color: P.rust}}>Đầu vào</div><div style={{fontSize: 36, fontWeight: 600, marginTop: 7}}>{money(variable)}</div></div>
      <div style={{width: 200, opacity: stage === 'before' ? interpolate(frame, [cue(shot, 2, .53), cue(shot, 2, .53) + 8], [0, 1], clamp) : 1}}><div style={label}>Cố định / ổ</div><div style={{fontSize: 36, fontWeight: 600, marginTop: 7}}>{money(fixed)}</div></div>
      <div style={{width: 220, opacity: stage === 'before' ? interpolate(frame, [cue(shot, 3, .77), cue(shot, 3, .77) + 8], [0, 1], clamp) : 1}}><div style={{...label, color: P.warm}}>Còn lại*</div><div style={{fontSize: 42, color: remainder < 0 ? P.rust : P.warm, fontWeight: 700, marginTop: 4}}>{money(remainder)}</div></div>
    </div>
    {stage !== 'before' && <div style={{marginTop: 32, borderTop: `1px solid ${P.rule}`, paddingTop: 21,
      opacity: interpolate(frame, [deltaCue, deltaCue + 8], [0, 1], clamp)}}>
      <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'baseline'}}>
        <div style={{fontSize: 23, color: P.quiet}}>Thay đổi phần còn lại</div>
        <div style={{fontSize: 57, color: afterRemainder < beforeRemainder ? P.rust : P.green, fontWeight: 700}}>{afterRemainder < beforeRemainder ? '−' : '+'}{money(Math.abs(afterRemainder - beforeRemainder))}</div>
      </div>
    </div>}
    <div style={{...small, marginTop: 19}}>*Chưa phải lợi nhuận ròng. Lượng bán giả định không đổi.</div>
  </>;
};

/** Each price appears only when narration reaches it. The upward line continues
 * even as its slope eases, making lower inflation visibly different from a fall. */
const PricePath: React.FC<{shot: BreadShot}> = ({shot}) => {
  const frame = useCurrentFrame();
  const raw = shot.data?.prices ?? shot.data?.values;
  const prices = Array.isArray(raw) && raw.every(v => typeof v === 'number') ? raw as number[] : [20000, 22000, 22440];
  const names = Array.isArray(shot.data?.labels) ? shot.data?.labels as string[] : ['Ban đầu', 'Kỳ 1', 'Kỳ 2'];
  const values = prices.slice(0, 4);
  const minimum = Math.min(...values) * .95;
  const maximum = Math.max(...values) * 1.035;
  const gap = 610 / Math.max(1, values.length - 1);
  const x = (i: number) => 40 + i * gap;
  const y = (n: number) => 300 - (n - minimum) / Math.max(1, maximum - minimum) * 236;
  const cueFor = (i: number) => cue(shot, i, .1 + i * .28);
  const latest = values.reduce((current, _, i) => frame >= cueFor(i) ? i : current, 0);
  return <>
    <GraphicHeading shot={shot}/>
    <svg width={704} height={400} viewBox="0 0 704 400" style={{overflow: 'visible'}}>
      <line x1={24} y1={321} x2={680} y2={321} stroke={P.rule}/>
      {values.map((value, i) => <g key={i} opacity={interpolate(frame, [cueFor(i), cueFor(i) + 7], [0, 1], clamp)}>
        {i > 0 && <line x1={x(i - 1)} y1={y(values[i - 1])}
          x2={interpolate(frame, [cueFor(i), cueFor(i) + 22], [x(i - 1), x(i)], clamp)}
          y2={interpolate(frame, [cueFor(i), cueFor(i) + 22], [y(values[i - 1]), y(value)], clamp)} stroke={P.warm} strokeWidth={5} strokeLinecap="round"/>}
        <circle cx={x(i)} cy={y(value)} r={7} fill={P.warm}/>
        <text x={x(i)} y={y(value) - 27} textAnchor={i === 0 ? 'start' : i === values.length - 1 ? 'end' : 'middle'} fill={P.white} fontSize={i === latest ? 43 : 34} fontWeight={700}>{number(value)}</text>
        <text x={x(i)} y={363} textAnchor={i === 0 ? 'start' : i === values.length - 1 ? 'end' : 'middle'} fill={P.quiet} fontSize={24}>{names[i] ?? `Kỳ ${i}`}</text>
        {i > 0 && <text x={(x(i - 1) + x(i)) / 2} y={(y(values[i - 1]) + y(value)) / 2 + 57} fill={i === values.length - 1 ? P.green : P.warm} textAnchor="middle" fontSize={31} fontWeight={600}>+{number((value / values[i - 1] - 1) * 100, 1)}%</text>}
      </g>)}
    </svg>
    <div style={{fontSize: 29, color: P.warm, lineHeight: 1.35, marginTop: 8,
      opacity: interpolate(frame, [cue(shot, values.length, .86), cue(shot, values.length, .86) + 7], [0, 1], clamp)}}>{shot.emphasis ?? 'Tăng chậm hơn. Giá vẫn cao hơn.'}</div>
    <div style={{...small, marginTop: 22}}>Cùng lượng, cùng chất lượng · Đơn vị: đồng</div>
  </>;
};

/** Equal baseline lengths become unequal purchasing power. The result is the
 * income multiplier divided by the SAME basket's price multiplier. */
const PurchasingPower: React.FC<{shot: BreadShot}> = ({shot}) => {
  const frame = useCurrentFrame();
  const stage = shot.data?.stage;
  const incomeBefore = numeric(shot.data, ['incomeBefore'], 10000000);
  const incomeAfter = numeric(shot.data, ['incomeAfter'], 10500000);
  const priceBefore = numeric(shot.data, ['priceBefore'], 20000);
  const priceAfter = numeric(shot.data, ['priceAfter'], 22000);
  const wageGrowth = numeric(shot.data, ['wageGrowth', 'incomeGrowth'], (incomeAfter / incomeBefore - 1) * 100);
  const basketGrowth = numeric(shot.data, ['basketGrowth', 'priceGrowth'], (priceAfter / priceBefore - 1) * 100);
  const ratio = (1 + wageGrowth / 100) / (1 + basketGrowth / 100);
  const wageCue = cue(shot, 0, .12);
  const basketCue = cue(shot, 1, .38);
  const resultCue = cue(shot, 2, .69);
  const max = Math.max(1 + wageGrowth / 100, 1 + basketGrowth / 100) * 1.02;
  const width = 690;
  if (stage === 'quantity' || stage === 'result') {
    const before = numeric(shot.data, ['before'], incomeBefore / priceBefore);
    const after = numeric(shot.data, ['after'], incomeAfter / priceAfter);
    const exactChange = (after / before - 1) * 100;
    return <>
      <GraphicHeading shot={shot}/>
      <div style={label}>Hai mức lương, cùng chiếc bánh ấy</div>
      <div style={{display: 'flex', alignItems: 'baseline', gap: 24, marginTop: 22}}>
        <span style={{fontSize: 89, lineHeight: 1.1, fontWeight: 700}}>{number(before)}</span><span style={{fontSize: 42, color: P.quiet}}>→</span>
        <span style={{fontSize: 89, lineHeight: 1.1, fontWeight: 700, color: P.rust,
          opacity: interpolate(frame, [cue(shot, 0, .12), cue(shot, 0, .12) + 8], [0, 1], clamp)}}>{number(after)}</span>
        <span style={{fontSize: 26, color: P.quiet}}>ổ</span>
      </div>
      <div style={{width: 690, height: 38, marginTop: 32, position: 'relative', background: 'rgba(255,250,240,.14)'}}>
        <div style={{position: 'absolute', height: '100%', background: P.warm,
          width: interpolate(frame, [cue(shot, 0, .12), cue(shot, 0, .12) + 28], [690, Math.max(0, after / before * 690)], clamp)}}/>
        <div style={{position: 'absolute', left: Math.max(0, after / before * 690), top: -8, height: 54, width: 2, background: P.rust,
          opacity: interpolate(frame, [cue(shot, 0, .12) + 20, cue(shot, 0, .12) + 28], [0, 1], clamp)}}/>
      </div>
      <div style={{marginTop: 41, opacity: interpolate(frame, [cue(shot, 1, .45), cue(shot, 1, .45) + 8], [0, 1], clamp)}}>
        <div style={label}>Sức mua tính riêng bằng bánh</div>
        <div style={{display: 'flex', alignItems: 'baseline', gap: 18, marginTop: 4}}><span style={{fontSize: 91, fontWeight: 700, color: exactChange < 0 ? P.rust : P.green, letterSpacing: -2}}>{exactChange < 0 ? '−' : '+'}{number(Math.abs(exactChange), 1)}%</span><span style={{fontSize: 26, color: P.quiet}}>xấp xỉ</span></div>
      </div>
      {stage === 'result' && shot.emphasis && <div style={{fontSize: 30, color: P.warm, marginTop: 25, lineHeight: 1.35,
        opacity: interpolate(frame, [cue(shot, 2, .72), cue(shot, 2, .72) + 8], [0, 1], clamp)}}>{shot.emphasis}</div>}
      <div style={{...small, marginTop: 25}}>Phép so minh họa; không giả định dùng cả lương mua bánh.<br/>Một mặt hàng không đại diện sức mua toàn giỏ hoặc CPI.</div>
    </>;
  }
  if (stage === 'income') return <>
    <GraphicHeading shot={shot}/>
    <div style={label}>Thu nhập trong cùng kỳ</div>
    <div style={{fontSize: 51, fontWeight: 600, marginTop: 17, display: 'flex', alignItems: 'baseline', gap: 18}}>
      <span>{number(incomeBefore / 1000000, 1)}</span><span style={{color: P.quiet, fontSize: 36}}>→</span><span>{number(incomeAfter / 1000000, 1)}</span><span style={{fontSize: 24, color: P.quiet}}>triệu đồng</span>
    </div>
    <div style={{fontSize: 83, fontWeight: 700, color: P.warm, marginTop: 13,
      opacity: interpolate(frame, [wageCue, wageCue + 8], [0, 1], clamp)}}>+{number(wageGrowth, 1)}%</div>
    <div style={{marginTop: 36, paddingTop: 28, borderTop: `1px solid ${P.rule}`,
      opacity: interpolate(frame, [basketCue, basketCue + 8], [0, 1], clamp)}}>
      <div style={label}>Giá cùng chiếc bánh</div>
      <div style={{fontSize: 38, fontWeight: 600, marginTop: 13}}>{number(priceBefore)} → {money(priceAfter)}</div>
      <div style={{fontSize: 75, fontWeight: 700, color: P.rust, marginTop: 9}}>+{number(basketGrowth, 1)}%</div>
    </div>
    <div style={{...small, marginTop: 26}}>Ví dụ cùng kỳ · Cùng lượng và chất lượng chiếc bánh</div>
  </>;
  return <>
    <GraphicHeading shot={shot}/>
    <div style={{marginTop: 12}}>
      <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: 18}}><span style={label}>Thu nhập</span><span style={{fontSize: 46, fontWeight: 700}}>+{number(wageGrowth, 1)}%</span></div>
      <div style={{height: 30, background: 'rgba(255,250,240,.1)', width}}><div style={{height: '100%', background: P.warm,
        width: interpolate(frame, [wageCue, wageCue + 24], [1 / max * width, (1 + wageGrowth / 100) / max * width], clamp)}}/></div>
      <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginTop: 37, marginBottom: 18,
        opacity: interpolate(frame, [basketCue, basketCue + 6], [0, 1], clamp)}}><span style={label}>Chi phí cùng giỏ hàng</span><span style={{fontSize: 46, fontWeight: 700, color: P.rust}}>+{number(basketGrowth, 1)}%</span></div>
      <div style={{height: 30, background: 'rgba(255,250,240,.1)', width,
        opacity: interpolate(frame, [basketCue, basketCue + 6], [0, 1], clamp)}}><div style={{height: '100%', background: P.rust,
        width: interpolate(frame, [basketCue, basketCue + 24], [1 / max * width, (1 + basketGrowth / 100) / max * width], clamp)}}/></div>
    </div>
    <div style={{marginTop: 48, borderTop: `1px solid ${P.rule}`, paddingTop: 29,
      opacity: interpolate(frame, [resultCue, resultCue + 8], [0, 1], clamp)}}>
      <div style={{fontSize: 24, color: P.quiet}}>Sức mua cùng một giỏ hàng</div>
      <div style={{display: 'flex', alignItems: 'baseline', gap: 23, marginTop: 9}}>
        <span style={{fontSize: 90, fontWeight: 700, color: ratio < 1 ? P.rust : P.green, letterSpacing: -2}}>{ratio < 1 ? '−' : '+'}{number(Math.abs(ratio - 1) * 100, 1)}%</span>
        <span style={{fontSize: 29, color: P.quiet}}>xấp xỉ</span>
      </div>
      <div style={{...small, marginTop: 10}}>100 phần sức mua trước → {number(100 * ratio, 1)} phần sau</div>
    </div>
    <div style={{...small, marginTop: 26}}>Cùng kỳ so sánh · Giỏ minh họa không đại diện CPI</div>
  </>;
};

export const MathOverlay: React.FC<{shot: BreadShot}> = ({shot}) => {
  const frame = useCurrentFrame();
  const end = Math.max(16, shot.duration - 1);
  const left = shot.graphicSide === 'left';
  return <div style={{position: 'absolute', top: 218, width: 724, [left ? 'left' : 'right']: 105, color: P.white,
    opacity: interpolate(frame, [0, 6, end - 6, end], [0, 1, 1, 0], clamp),
    textShadow: '0 2px 15px rgba(0,0,0,.2)'}}>
    {shot.kind === 'cost_stack' ? <CostStack shot={shot}/> : shot.kind === 'price_path' ? <PricePath shot={shot}/> : shot.kind === 'purchasing_power' ? <PurchasingPower shot={shot}/> : null}
  </div>;
};
