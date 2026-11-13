import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {Header, Source, font, localCue, rise, themeFor} from './Shared';
import type {BusinessShot} from './types';

const numeral = (value: number) => new Intl.NumberFormat('vi-VN', {maximumFractionDigits: 1}).format(value);
const x0 = 240, x1 = 1690, y0 = 766, y1 = 314;

/** Data is authored in the manifest; this scene never manufactures figures. */
export const ChartScene: React.FC<{shot: BusinessShot; duration: number}> = ({shot, duration}) => {
  const frame = useCurrentFrame();
  const p = themeFor(shot);
  const chart = shot.design?.chart;
  if (!chart?.items.length) throw new Error(`Business chart ${shot.id ?? ''} needs data.`);
  const line = chart.kind === 'line' || chart.kind === 'breakeven';
  const values = chart.items.map(item => item.value);
  const positiveMax = Math.max(1, ...values.map(Math.abs), chart.fixed ?? 0, chart.target ?? 0);
  const maximum = chart.max ?? positiveMax * 1.13;
  let partial = 0;
  const balances = chart.kind === 'waterfall' ? chart.items.map((item, index) => index === chart.items.length - 1 ? item.value : (partial += item.value)) : values;
  const minimum = Math.min(0, ...balances, ...values) < 0 && balances.some(value => value < 0)
    ? Math.floor(Math.min(0, ...balances) / 10) * 10 : 0;
  const y = (value: number) => y0 - (value - minimum) / (maximum - minimum) * (y0 - y1);
  const maxX = Math.max(1, ...chart.items.map((item, i) => item.x ?? i + 1));
  const x = (value: number) => x0 + value / maxX * (x1 - x0);
  const progress = rise(frame, localCue(shot, 0, 8), Math.min(90, Math.max(25, duration * .42)));
  const linePoints = chart.items.map((item, i) => [x(item.x ?? i + 1), y(item.value)]);
  const points = linePoints.map(point => point.join(',')).join(' ');
  let running = 0;
  return <AbsoluteFill style={{background: p.paper, color: p.ink}}>
    <Header shot={shot}/>
    <svg width={1920} height={1080} style={{position: 'absolute', inset: 0}}>
      <defs><clipPath id={`chart-reveal-${shot.id ?? shot.start}`}><rect x={x0 - 10} y={y1 - 60} width={(x1 - x0 + 40) * progress} height={y0 - y1 + 120}/></clipPath></defs>
      {[0, .25, .5, .75, 1].map(fraction => <g key={fraction}>
        <line x1={x0} y1={y(minimum+(maximum-minimum) * fraction)} x2={x1} y2={y(minimum+(maximum-minimum) * fraction)} stroke={p.rule} strokeWidth={fraction === 0 ? 2 : 1}/>
        <text x={x0 - 24} y={y(minimum+(maximum-minimum) * fraction) + 7} textAnchor="end" fill={p.quiet} fontFamily="Arial,sans-serif" fontSize={23}>{numeral(minimum+(maximum-minimum) * fraction)}</text>
      </g>)}
      {minimum < 0 ? <line x1={x0} x2={x1} y1={y(0)} y2={y(0)} stroke={p.quiet} strokeWidth={2}/> : null}
      <text x={x0} y={y1 - 28} fill={p.quiet} fontFamily="Arial,sans-serif" fontSize={23}>{chart.unit ?? ''}</text>
      {!line && chart.target !== undefined ? <g>
        <line x1={x0} x2={x1} y1={y(chart.target)} y2={y(chart.target)} stroke={p.accent} strokeWidth={3} strokeDasharray="10 9"/>
        <text x={x1} y={y(chart.target)-14} textAnchor="end" fill={p.accent} fontFamily="Arial,sans-serif" fontSize={25}>Mốc: {numeral(chart.target)}</text>
      </g> : null}
      {line ? <>
        {(chart.fixed ?? chart.target) !== undefined ? <>
          <line x1={x0} x2={x1} y1={y(chart.fixed ?? chart.target ?? 0)} y2={y(chart.fixed ?? chart.target ?? 0)} stroke={p.accent} strokeWidth={3} strokeDasharray="10 9"/>
          <text x={x1} y={y(chart.fixed ?? chart.target ?? 0) - 14} textAnchor="end" fill={p.accent} fontFamily={font} fontWeight={700} fontSize={28}>{chart.kind === 'breakeven' ? 'Chi phí cố định: ' : 'Mốc: '}{numeral(chart.fixed ?? chart.target ?? 0)}</text>
        </> : null}
        <g clipPath={`url(#chart-reveal-${shot.id ?? shot.start})`}>
          <polyline points={points} fill="none" stroke={p.ink} strokeWidth={6} strokeLinejoin="round" strokeLinecap="round"/>
          {chart.items.map((item, i) => <g key={item.label}>
            <circle cx={linePoints[i][0]} cy={linePoints[i][1]} r={i === chart.highlight ? 10 : 7} fill={i === chart.highlight ? p.accent : p.ink}/>
            <text x={linePoints[i][0]} y={linePoints[i][1] - 23} textAnchor="middle" fill={i === chart.highlight ? p.accent : p.ink} fontFamily={font} fontWeight={700} fontSize={30}>{numeral(item.value)}</text>
          </g>)}
        </g>
        {chart.items.map((item, i) => <text key={`${item.label}-x`} x={linePoints[i][0]} y={y0 + 39} textAnchor="middle" fill={p.quiet} fontFamily="Arial,sans-serif" fontSize={24}>{item.label}</text>)}
        {chart.xLabel ? <text x={(x0 + x1) / 2} y={y0 + 86} textAnchor="middle" fill={p.quiet} fontFamily="Arial,sans-serif" fontSize={25}>{chart.xLabel}</text> : null}
      </> : chart.items.map((item, i) => {
        const gap = (x1 - x0) / chart.items.length;
        const width = Math.min(238, gap * .60);
        const center = x0 + gap * (i + .5);
        const waterfall = chart.kind === 'waterfall';
        const final = waterfall && i === chart.items.length - 1;
        const before = final ? 0 : running;
        const after = waterfall && !final ? before + item.value : item.value;
        if (waterfall && !final) running = after;
        const upper = waterfall ? Math.max(before, after) : Math.max(0, item.value);
        const lower = waterfall ? Math.min(before, after) : Math.min(0, item.value);
        const reveal = rise(frame, localCue(shot, i, 10 + i * Math.min(18, duration / 8)), 25);
        const height = Math.max(2, Math.abs(y(lower) - y(upper)) * reveal);
        const color = item.color ?? (i === chart.highlight || final ? p.accent : item.value < 0 ? '#b28c6c' : p.ink);
        return <g key={`${item.label}-${i}`} opacity={reveal}>
          {waterfall && i > 0 && !final ? <line x1={center - gap + width / 2} x2={center - width / 2} y1={y(before)} y2={y(before)} stroke={p.quiet} strokeDasharray="5 5" opacity={.6}/> : null}
          <rect x={center - width / 2} y={y(lower) - height} width={width} height={height} fill={color}/>
          <text x={center} y={y(upper) - 20} textAnchor="middle" fill={color} fontFamily={font} fontSize={44} fontWeight={700}>{item.value < 0 ? '−' : ''}{numeral(Math.abs(item.value))}</text>
          <text x={center} y={y0 + 43} textAnchor="middle" fill={p.ink} fontFamily="Arial,sans-serif" fontSize={28}>{item.label}</text>
        </g>;
      })}
    </svg>
    {shot.body ? <div style={{position: 'absolute', left: 200, right: 200, top: 868, font: '29px Arial,sans-serif', textAlign: 'center', lineHeight: 1.3, opacity: rise(frame, localCue(shot, 2, 55)), color: p.quiet}}>{shot.body}</div> : null}
    <Source shot={shot} style={{bottom: 143}}/>
  </AbsoluteFill>;
};
