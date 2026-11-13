import {useCurrentFrame} from 'remotion';
import earth from './geography/natural-earth-110m.json';
import {Frame, colorFor, cue, font, number, rise} from './Shared';
import type {ChinaShot} from './types';

type Coordinate = number[];
const radians = Math.PI / 180;
const albers = (lon: number, lat: number): [number, number] => {
  const p1 = 25 * radians, p2 = 47 * radians, center = 35 * radians;
  const n = (Math.sin(p1) + Math.sin(p2)) / 2;
  const c = Math.cos(p1) ** 2 + 2 * n * Math.sin(p1);
  const rho = Math.sqrt(c - 2 * n * Math.sin(lat * radians)) / n;
  const rho0 = Math.sqrt(c - 2 * n * Math.sin(center)) / n;
  const angle = n * (lon - 105) * radians;
  return [rho * Math.sin(angle), rho0 - rho * Math.cos(angle)];
};
const country = earth.features.find(feature => feature.id === 'CHN')!;
const rings = (feature: typeof country): Coordinate[][] => feature.geometry.type === 'Polygon'
  ? feature.geometry.coordinates as Coordinate[][] : (feature.geometry.coordinates as Coordinate[][][]).flat();
const chinaPoints = rings(country).flat().map(point => albers(point[0], point[1]));
const bounds = [Math.min(...chinaPoints.map(p => p[0])), Math.max(...chinaPoints.map(p => p[0])), Math.min(...chinaPoints.map(p => p[1])), Math.max(...chinaPoints.map(p => p[1]))];

export const MapScene: React.FC<{shot: ChinaShot; duration: number}> = ({shot, duration}) => {
  const frame = useCurrentFrame();
  const p = colorFor(shot);
  const map = shot.design?.map;
  if (!map) throw new Error('c-map needs geographic map data');
  const world = map.mode === 'routes';
  const project = (lon: number, lat: number): [number, number] => {
    if (world) return [185 + (lon + 180) / 360 * 1550, 285 + (76 - lat) / 136 * 465];
    const point = albers(lon, lat), scale = Math.min(1250 / (bounds[1] - bounds[0]), 505 / (bounds[3] - bounds[2]));
    return [960 + (point[0] - (bounds[0] + bounds[1]) / 2) * scale, 530 - (point[1] - (bounds[2] + bounds[3]) / 2) * scale];
  };
  const path = (feature: typeof country) => rings(feature).map(ring => ring.map((point, i) => `${i ? 'L' : 'M'}${project(point[0], point[1]).map(n => n.toFixed(1)).join(',')}`).join('') + 'Z').join('');
  const nodes = new Map(map.nodes.map(node => [node.id, node]));
  return <Frame shot={shot} note={map.note ?? 'Bản đồ khái quát: Natural Earth / public domain. Ranh giới chỉ để định vị, không thể hiện quan điểm về chủ quyền. Tuyến là sơ đồ kết nối.'}>
    <svg width={1920} height={1080} style={{position: 'absolute', inset: 0}}>
      <defs><clipPath id={`map-plate-${shot.id ?? shot.start}`}><rect x={150} y={262} width={1620} height={530}/></clipPath></defs>
      <g clipPath={`url(#map-plate-${shot.id ?? shot.start})`}>{(world ? earth.features : [country]).map(feature => <path key={feature.id} d={path(feature)} fill={feature.id === 'CHN' ? p.soft : p.rule} stroke={p.paper} strokeWidth={world ? 1 : 2} opacity={feature.id === 'CHN' ? 1 : .62}/>)}</g>
      {(map.links ?? []).map((link, i) => {
        const from = nodes.get(link.from), to = nodes.get(link.to);
        if (!from || !to) throw new Error('Map route refers to missing node');
        const a = project(from.lon, from.lat), b = project(to.lon, to.lat);
        const mid: [number, number] = [(a[0] + b[0]) / 2, Math.min(a[1], b[1]) - Math.min(125, Math.abs(a[0] - b[0]) * .16)];
        const line = `M${a}Q${mid} ${b}`;
        const entry = rise(frame, cue(shot, i, 15 + i * 20), 35);
        const cycle = ((Math.max(0, frame - cue(shot, i, 15 + i * 20)) / Math.max(70, duration * .6)) + i * .21) % 1;
        const dot = [(1 - cycle) ** 2 * a[0] + 2 * (1 - cycle) * cycle * mid[0] + cycle ** 2 * b[0], (1 - cycle) ** 2 * a[1] + 2 * (1 - cycle) * cycle * mid[1] + cycle ** 2 * b[1]];
        return <g key={`${link.from}-${link.to}`} opacity={entry}><path d={line} fill="none" stroke={p.accent} strokeWidth={3} pathLength={1} strokeDasharray="1" strokeDashoffset={1 - entry}/><circle cx={dot[0]} cy={dot[1]} r={6} fill={p.accent}/>{link.label ? <text x={mid[0]} y={mid[1] - 12} textAnchor="middle" fontFamily="Arial,sans-serif" fontSize={23} fill={p.ink}>{link.label}</text> : null}</g>;
      })}
      {map.nodes.map((node, i) => {
        const [x, y] = project(node.lon, node.lat), entry = rise(frame, cue(shot, i, i * 13), 25);
        return <g key={node.id} opacity={entry}><circle cx={x} cy={y} r={8 + (1 - entry) * 14} fill={node.color ?? p.accent}/><circle cx={x} cy={y} r={18 + Math.sin(frame / 18 + i) * 3} fill="none" stroke={node.color ?? p.accent} strokeWidth={1.5} opacity={.35}/><text x={x + 20} y={y - 13} fill={p.ink} fontFamily={font} fontSize={27} fontWeight={700} style={{paintOrder: 'stroke', stroke: p.paper, strokeWidth: 7, strokeLinejoin: 'round'}}>{node.label}{node.value === undefined ? '' : ` · ${number(node.value)}`}</text></g>;
      })}
    </svg>
  </Frame>;
};
