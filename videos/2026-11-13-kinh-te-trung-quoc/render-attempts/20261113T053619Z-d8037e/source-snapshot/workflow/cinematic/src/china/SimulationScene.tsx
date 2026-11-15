import {useCurrentFrame} from 'remotion';
import {Frame, Lines, colorFor, cue, font, number, rise} from './Shared';
import type {ChinaShot} from './types';

const person = (x: number, y: number, color: string, scale = 1) => <g transform={`translate(${x} ${y}) scale(${scale})`}><circle cy={-25} r={8} fill={color}/><path d="M-12,-10Q0,-18 12,-10L9,15H-9Z" fill={color}/><path d="M-5,15V37M5,15V37" stroke={color} strokeWidth={6} strokeLinecap="round"/></g>;

export const SimulationScene: React.FC<{shot: ChinaShot; duration: number}> = ({shot, duration}) => {
  const frame = useCurrentFrame(), p = colorFor(shot), sim = shot.design?.simulation;
  if (!sim?.items.length) throw new Error('c-sim needs authored simulation items');
  const items = sim.items.slice(0, 5), maximum = Math.max(1, ...items.map(item => Math.abs(item.value)));
  const note = sim.note ?? 'Mô phỏng cơ chế, không phải dữ liệu theo thời gian thực. Số hiển thị chỉ có ý nghĩa trong phạm vi nguồn ghi kèm.';
  const capacity = Math.max(1, items[0]?.value ?? 1);
  const demandIndex = items.findIndex(item => /đơn hàng|nhu cầu/iu.test(item.label));
  const demand = demandIndex >= 0 ? Math.max(0, items[demandIndex].value) : Math.min(...items.map(item => Math.max(0, item.value)));
  const utilization = Math.min(1, demand / capacity);
  const blocked = demandIndex >= 0 && utilization < 1;
  const scenario = shot.id === 'h08' ? 'gate' : shot.id === 'p04' ? 'utilization' : blocked ? 'capacity' : shot.id === 'd04' ? 'skills' : 'assembly';
  if (sim.kind === 'factory') return <Frame shot={shot} note={note}>
    <svg width={1920} height={1080} style={{position: 'absolute', inset: 0}}>
      <rect x={215} y={635} width={1490} height={57} rx={27} fill={p.rule}/>
      {Array.from({length: 25}, (_, i) => <circle key={i} cx={245 + i * 59} cy={663} r={17} fill={p.paper} stroke={p.quiet} strokeWidth={2}/>)}
      {[420, 960, 1500].map((x, i) => <g key={x} opacity={rise(frame, cue(shot, i, i * 15))}>
        <rect x={x - 112} y={353} width={224} height={208} rx={3} fill={p.soft} stroke={p.ink} strokeWidth={3}/><rect x={x - 72} y={390} width={144} height={95} fill={p.paper}/>
        <path d={`M${x - 68},${521 + Math.sin(frame / (12 - Math.min(6, items[i]?.value ?? 3)) + i) * 9}H${x + 68}`} stroke={p.accent} strokeWidth={15}/>
        <rect x={x - 88} y={561} width={18} height={74} fill={p.ink}/><rect x={x + 70} y={561} width={18} height={74} fill={p.ink}/>
        <text x={x} y={323} textAnchor="middle" fill={p.ink} fontFamily={font} fontSize={34} fontWeight={700}>{items[i]?.label ?? ['Đầu vào', 'Gia công', 'Đầu ra'][i]}</text>
        {items[i] ? <text x={x} y={765} textAnchor="middle" fill={p.accent} fontFamily={font} fontSize={44} fontWeight={700}>{number(items[i].value)}{sim.unit ? ` ${sim.unit}` : ''}</text> : null}
        <rect x={x - 75} y={573} width={150} height={10} fill={p.rule}/><rect x={x - 75} y={573} width={150 * (items[i]?.value ?? 0) / maximum * rise(frame, cue(shot, i, i * 15), 45)} height={10} fill={i === demandIndex ? p.accent : p.ink}/>
      </g>)}
      {Array.from({length: 8}, (_, i) => {
        const x = 230 + ((frame * (2.5 + Math.min(5, demand) * .32) + i * 190) % 1440);
        const completed = x > 1410;
        const retained = !blocked || i < Math.max(1, Math.round(8 * utilization));
        if (!retained && x > 970) return null;
        return <g key={i} transform={`translate(${x} 605)`} opacity={!retained ? .38 : 1}><rect x={-25} y={-25} width={50} height={50} rx={completed ? 23 : 3} fill={completed ? p.accent : p.ink}/><path d={completed ? 'M-12,0L-3,9L14,-11' : 'M-11,-10H11V10H-11Z'} fill="none" stroke={p.paper} strokeWidth={3}/></g>;
      })}
      {scenario === 'gate' ? <g opacity={rise(frame, cue(shot, 1, 20))}><path d="M1085,460V630" stroke={p.accent} strokeWidth={11}/><path d="M1062,476L1108,522M1062,524L1108,570" stroke={p.accent} strokeWidth={4}/><text x={1170} y={405} textAnchor="middle" fill={p.accent} fontFamily="Arial,sans-serif" fontSize={24}>Điểm nghẽn đơn hàng</text></g> : null}
      {scenario === 'capacity' || scenario === 'utilization' ? <g opacity={rise(frame, cue(shot, 1, 20))}>{Array.from({length: 8}, (_, i) => <rect key={i} x={650 + i * 76} y={268} width={52} height={25} fill={i < Math.round(utilization * 8) ? p.accent : 'transparent'} stroke={p.accent} strokeWidth={2} opacity={i < Math.round(utilization * 8) ? 1 : .35}/>)}<text x={960} y={248} textAnchor="middle" fill={p.quiet} fontFamily="Arial,sans-serif" fontSize={22}>{scenario === 'utilization' ? 'Phần được sử dụng / phần công suất còn trống — minh họa' : 'Đơn hàng chỉ lấp một phần công suất — minh họa'}</text></g> : null}
      {scenario === 'skills' ? <g>{[420,960,1500].map((x,i)=><path key={x} d={`M${x-65},${285-i*14}L${x},${260-i*14}L${x+65},${285-i*14}`} fill="none" stroke={p.accent} strokeWidth={4} opacity={rise(frame,cue(shot,i,i*15))}/>)}</g> : null}
      <text x={960} y={825} textAnchor="middle" fill={p.quiet} fontFamily="Arial,sans-serif" fontSize={23}>Dây chuyền minh họa nguyên lý; tốc độ chuyển động không mã hóa năng suất thống kê.</text>
    </svg>
  </Frame>;
  if (sim.kind === 'property') return <Frame shot={shot} note={note}>
    <svg width={1920} height={1080} style={{position: 'absolute', inset: 0}}>
      {items.map((item, i) => {
        const x = 250 + i / Math.max(1, items.length - 1) * 1420;
        const entry = rise(frame, cue(shot, i, i * 20), 30);
        return <g key={item.label} opacity={entry}>
          {i < items.length - 1 ? <><path d={`M${x + 105},520H${x + 1420 / Math.max(1, items.length - 1) - 105}`} stroke={p.accent} strokeWidth={3}/><path d={`M${x + 1420 / Math.max(1, items.length - 1) - 120},510l15,10l-15,10`} fill="none" stroke={p.accent} strokeWidth={3}/><circle cx={x + 110 + ((frame * 2 + i * 45) % Math.max(1, 1420 / Math.max(1, items.length - 1) - 220))} cy={520} r={5} fill={p.accent}/></> : null}
          <path d={`M${x - 80},490L${x},420L${x + 80},490V640H${x - 80}Z`} fill={i % 2 ? p.soft : p.rule} stroke={p.ink} strokeWidth={2}/>
          {[0, 1, 2].map(row => [0, 1].map(col => <rect key={`${row}-${col}`} x={x - 49 + col * 65} y={505 + row * 40} width={27} height={22} fill={p.paper}/>))}
          <Lines text={item.label} x={x} y={710} width={17} size={29} color={p.ink} weight={700}/>
          {sim.unit ? <text x={x} y={790} textAnchor="middle" fill={p.accent} fontFamily={font} fontSize={41} fontWeight={700}>{number(item.value)} {sim.unit}</text> : null}
        </g>;
      })}
    </svg>
  </Frame>;
  if (sim.kind === 'household') {
    const total = items.reduce((sum, item) => sum + Math.max(0, item.value), 0) || 1;
    let cursor = -Math.PI / 2;
    return <Frame shot={shot} note={note}>
      <svg width={1920} height={1080} style={{position: 'absolute', inset: 0}}>
        {items.map((item, i) => {
          const angle = Math.max(0, item.value) / total * Math.PI * 2, start = cursor;
          cursor += angle;
          const entry = rise(frame, cue(shot, i, i * 18), 32), end = start + angle * entry;
          const a = [580 + Math.cos(start) * 205, 553 + Math.sin(start) * 205], b = [580 + Math.cos(end) * 205, 553 + Math.sin(end) * 205];
          const path = `M${a}A205,205 0 ${end - start > Math.PI ? 1 : 0},1 ${b}`;
          const color = item.color ?? [p.accent, p.ink, '#a4b09a', '#caa67a', '#7d9695'][i];
          return <g key={item.label}><path d={path} fill="none" stroke={color} strokeWidth={75}/><g opacity={entry}><rect x={1040} y={320 + i * 95} width={12} height={62} fill={color}/><text x={1080} y={348 + i * 95} fill={p.ink} fontFamily="Arial,sans-serif" fontSize={31}>{item.label}</text><text x={1660} y={348 + i * 95} textAnchor="end" fill={color} fontFamily={font} fontSize={39} fontWeight={700}>{number(item.value)}{sim.unit ? ` ${sim.unit}` : ''}</text></g></g>;
        })}
        {person(560, 555, p.ink, 1.6)}{person(615, 568, p.accent, 1.1)}
        <text x={580} y={806} textAnchor="middle" fill={p.quiet} fontFamily="Arial,sans-serif" fontSize={23}>Tỷ trọng trong tổng các mục được hiển thị</text>
      </svg>
    </Frame>;
  }
  return <Frame shot={shot} note={note}>
    <svg width={1920} height={1080} style={{position: 'absolute', inset: 0}}>
      {items.map((item, i) => {
        const y = 335 + i * Math.min(118, 460 / items.length), entry = rise(frame, cue(shot, i, i * 19), 35), color = item.color ?? (i % 2 ? p.accent : p.ink);
        return <g key={item.label}><Lines text={item.label} x={285} y={y + 25} width={17} size={28} color={p.ink} weight={700}/><rect x={490} y={y} width={1020} height={60} fill={p.rule} opacity={.55}/><rect x={490} y={y} width={1020 * Math.max(0, item.value) / maximum * entry} height={60} fill={color}/><text x={1690} y={y + 42} textAnchor="end" fill={color} fontFamily={font} fontSize={40} fontWeight={700}>{number(item.value)}{sim.unit ? ` ${sim.unit}` : ''}</text></g>;
      })}
      <g opacity={.2}>{Array.from({length: 10}, (_, i) => person(500 + i * 94, 812, i % 2 ? p.accent : p.ink, .64))}</g>
    </svg>
  </Frame>;
};
