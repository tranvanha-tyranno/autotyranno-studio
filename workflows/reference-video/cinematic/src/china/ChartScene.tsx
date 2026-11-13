import {useCurrentFrame} from 'remotion';
import {Frame, colorFor, cue, font, number, rise} from './Shared';
import type {ChinaShot} from './types';

/** Negative domains, true numeric x coordinates, and separately colored series. */
export const ChinaChart: React.FC<{shot: ChinaShot; duration: number}> = ({shot, duration}) => {
  const frame = useCurrentFrame(), p = colorFor(shot), chart = shot.design?.chart;
  if (!chart?.items.length) throw new Error('c-chart needs verified authored data');
  const line = ['line', 'breakeven'].includes(chart.kind);
  const series = chart.series?.length ? chart.series : [{label: '', color: p.ink, items: chart.items}];
  let running = 0;
  const balances = chart.items.map((item, i) => chart.kind === 'waterfall' ? i === chart.items.length - 1 ? item.value : running += item.value : item.value);
  const values = line ? series.flatMap(s => s.items.map(item => item.value)) : balances;
  const min = chart.min ?? (Math.min(0, ...values) < 0 ? Math.min(...values) * 1.2 : 0);
  const max = chart.max ?? Math.max(1, ...values, chart.fixed ?? 0, chart.target ?? 0) * 1.16;
  const y = (value: number) => 758 - (value - min) / Math.max(.0001, max - min) * 442;
  const allX = series.flatMap(s => s.items.map((item, i) => item.x ?? i));
  const minX = Math.min(...allX), maxX = Math.max(minX + 1, ...allX);
  const x = (value: number) => 245 + (value - minX) / (maxX - minX) * 1435;
  running = 0;
  return <Frame shot={shot}>
    <svg width={1920} height={1080} style={{position: 'absolute', inset: 0}}>
      <defs><clipPath id={`china-chart-${shot.id ?? shot.start}`}><rect x={225} y={260} width={1480 * rise(frame, cue(shot, 0, 5), Math.min(95, duration * .48))} height={530}/></clipPath></defs>
      {[0, .25, .5, .75, 1].map(fraction => {
        const value = min + fraction * (max - min);
        return <g key={fraction}><line x1={245} x2={1680} y1={y(value)} y2={y(value)} stroke={p.rule} strokeWidth={1}/><text x={216} y={y(value) + 7} textAnchor="end" fill={p.quiet} fontFamily="Arial,sans-serif" fontSize={23}>{number(value)}</text></g>;
      })}
      <line x1={245} x2={1680} y1={y(0)} y2={y(0)} stroke={p.quiet} strokeWidth={2}/>
      <text x={245} y={284} fill={p.quiet} fontFamily="Arial,sans-serif" fontSize={23}>{chart.unit}</text>
      {(chart.fixed ?? chart.target) !== undefined ? <g><line x1={245} x2={1680} y1={y(chart.fixed ?? chart.target ?? 0)} y2={y(chart.fixed ?? chart.target ?? 0)} stroke={p.accent} strokeWidth={2.5} strokeDasharray="9 8"/><text x={1680} y={y(chart.fixed ?? chart.target ?? 0) - 13} textAnchor="end" fill={p.accent} fontFamily="Arial,sans-serif" fontSize={24}>Mốc: {number(chart.fixed ?? chart.target ?? 0)}</text></g> : null}
      {line ? series.map((s, si) => <g key={`${s.label}-${si}`}>
        <g clipPath={`url(#china-chart-${shot.id ?? shot.start})`}><polyline points={s.items.map((item, i) => `${x(item.x ?? i)},${y(item.value)}`).join(' ')} fill="none" stroke={s.color ?? p.accent} strokeWidth={5} strokeLinejoin="round" strokeLinecap="round"/>{s.items.map((item, i) => <g key={i}><circle cx={x(item.x ?? i)} cy={y(item.value)} r={5} fill={s.color ?? p.accent}/>{s.items.length <= 9 ? <text x={x(item.x ?? i)} y={y(item.value) - 19 - si * 8} textAnchor="middle" fill={s.color ?? p.accent} fontFamily={font} fontSize={28} fontWeight={700}>{number(item.value)}</text> : null}</g>)}</g>
        {si === 0 ? s.items.map((item, i) => <text key={i} x={x(item.x ?? i)} y={801} textAnchor="middle" fill={p.quiet} fontFamily="Arial,sans-serif" fontSize={23}>{item.label}</text>) : null}
        {s.label ? <g><line x1={245 + si * 410} x2={283 + si * 410} y1={235} y2={235} stroke={s.color ?? p.accent} strokeWidth={5}/><text x={295 + si * 410} y={242} fill={p.ink} fontFamily="Arial,sans-serif" fontSize={23}>{s.label}</text></g> : null}
      </g>) : chart.items.map((item, i) => {
        const gap = 1435 / chart.items.length, center = 245 + gap * (i + .5), width = Math.min(220, gap * .60);
        const waterfall = chart.kind === 'waterfall', final = waterfall && i === chart.items.length - 1;
        const before = final || !waterfall ? 0 : running, after = waterfall && !final ? before + item.value : item.value;
        if (waterfall && !final) running = after;
        const upper = Math.max(before, after), lower = Math.min(before, after), entry = rise(frame, cue(shot, i, i * 19), 30);
        const color = item.color ?? (item.value < 0 ? '#ad8b72' : i === chart.highlight || final ? p.accent : p.ink);
        const height = Math.abs(y(lower) - y(upper)) * entry;
        return <g key={item.label} opacity={entry}>{waterfall && i > 0 && !final ? <line x1={center - gap + width / 2} x2={center - width / 2} y1={y(before)} y2={y(before)} stroke={p.quiet} strokeDasharray="5 5"/> : null}<rect x={center - width / 2} y={y(lower) - height} width={width} height={Math.max(1, height)} fill={color}/><text x={center} y={y(upper) - 18} textAnchor="middle" fill={color} fontFamily={font} fontSize={40} fontWeight={700}>{number(item.value)}</text><text x={center} y={802} textAnchor="middle" fill={p.ink} fontFamily="Arial,sans-serif" fontSize={26}>{item.label}</text></g>;
      })}
      {chart.xLabel ? <text x={960} y={836} textAnchor="middle" fill={p.quiet} fontFamily="Arial,sans-serif" fontSize={24}>{chart.xLabel}</text> : null}
    </svg>
  </Frame>;
};
