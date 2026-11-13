import {useCurrentFrame} from 'remotion';
import {Frame, Lines, colorFor, cue, number, rise} from './Shared';
import type {ChinaShot} from './types';

/** Schematic transmission links; widths only encode the supplied illustrative values. */
export const FlowScene: React.FC<{shot: ChinaShot; duration: number}> = ({shot, duration}) => {
  const frame = useCurrentFrame(), p = colorFor(shot), flow = shot.design?.flow;
  if (!flow?.nodes.length) throw new Error('c-flow needs nodes and links');
  const columns = Math.max(1, ...flow.nodes.map(node => node.column ?? 0));
  const byColumn = new Map<number, typeof flow.nodes>();
  flow.nodes.forEach(node => byColumn.set(node.column ?? 0, [...(byColumn.get(node.column ?? 0) ?? []), node]));
  const positions = new Map(flow.nodes.map(node => {
    const col = node.column ?? 0, deck = byColumn.get(col)!, i = deck.indexOf(node);
    return [node.id, [230 + col / columns * 1460, 330 + (i + .5) / deck.length * 420] as [number, number]];
  }));
  const maxLink = Math.max(1, ...flow.links.map(link => link.value));
  return <Frame shot={shot} note={flow.note ?? 'Sơ đồ cơ chế. Liên kết không tự chứng minh quy mô hoặc quan hệ nhân quả của số liệu.'}>
    <svg width={1920} height={1080} style={{position: 'absolute', inset: 0}}>
      {flow.links.map((link, i) => {
        const a = positions.get(link.from), b = positions.get(link.to);
        if (!a || !b) throw new Error('Flow link refers to missing node');
        const entry = rise(frame, cue(shot, i, 12 + i * 13), 35);
        const sx = a[0] + 115, ex = b[0] - 115, mid = (sx + ex) / 2;
        const path = `M${sx},${a[1]}C${mid},${a[1]} ${mid},${b[1]} ${ex},${b[1]}`;
        return <g key={`${link.from}-${link.to}-${i}`} opacity={entry}><path d={path} fill="none" stroke={p.accent} opacity={.18} strokeWidth={8 + link.value / maxLink * 36}/><path d={path} fill="none" stroke={p.accent} strokeWidth={2} pathLength={1} strokeDasharray=".035 .14" strokeDashoffset={-frame / Math.max(120, duration)} opacity={.85}/>{link.label ? <text x={mid} y={(a[1] + b[1]) / 2 - 25} textAnchor="middle" fill={p.quiet} fontFamily="Arial,sans-serif" fontSize={22}>{link.label}</text> : null}</g>;
      })}
      {flow.nodes.map((node, i) => {
        const [x, y] = positions.get(node.id)!, entry = rise(frame, cue(shot, i, i * 10), 22);
        return <g key={node.id} opacity={entry}><rect x={x - 115} y={y - 56} width={230} height={112} rx={3} fill={p.paper} stroke={p.rule} strokeWidth={2}/><rect x={x - 115} y={y - 56} width={5} height={112} fill={p.accent}/><Lines text={node.label} x={x} y={y - (node.value === undefined ? 0 : 13)} width={17} size={26} color={p.ink} weight={700}/>{node.value !== undefined ? <text x={x} y={y + 34} textAnchor="middle" fill={p.accent} fontFamily="Arial,sans-serif" fontSize={24}>{number(node.value)}{flow.unit ? ` ${flow.unit}` : ''}</text> : null}</g>;
      })}
    </svg>
  </Frame>;
};
