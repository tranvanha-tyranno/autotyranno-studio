import type {ReactNode} from 'react';

export type PeoplePalette = {paper: string; ink: string; accent: string; quiet: string; rule: string; soft: string};
export type PeopleProps = {shot: any; frame: number; p: PeoplePalette};
export const clamp01 = (x: number) => Math.min(1, Math.max(0, x));
export const stage = (t: number, start = 0, end = 1) => {
  const v = clamp01((t - start) / (end - start));
  return v * v * (3 - 2 * v);
};
export const InkText = ({x, y, children, p, size = 28, anchor = 'middle', color, weight = 600}: {
  x: number; y: number; children: ReactNode; p: PeoplePalette; size?: number;
  anchor?: 'middle' | 'start' | 'end'; color?: string; weight?: number;
}) => <text x={x} y={y} textAnchor={anchor} fill={color ?? p.ink} fontFamily="Arial,sans-serif" fontSize={size} fontWeight={weight}>{children}</text>;

export const Person = ({x, y, scale = 1, p, coat, arm = 0, walk = 0, elderly = false, seated = false}: {
  x: number; y: number; scale?: number; p: PeoplePalette; coat?: string; arm?: number; walk?: number; elderly?: boolean; seated?: boolean;
}) => <g transform={`translate(${x} ${y}) scale(${scale})`}>
  <ellipse cx={0} cy={131} rx={35} ry={7} fill={p.ink} opacity={.09}/>
  <path d="M-11 47 Q-19 83 -13 103" fill="none" stroke={coat ?? p.ink} strokeWidth={15} strokeLinecap="round"/>
  <path d={`M13 48 Q${30 + arm * 14} 69 ${27 + arm * 29} ${93 - arm * 23}`} fill="none" stroke={coat ?? p.ink} strokeWidth={14} strokeLinecap="round"/>
  <path d={seated ? 'M-8 87 L-15 105 L-13 128' : `M-8 87 L${-14 + walk * 10} 126`} fill="none" stroke={p.ink} strokeWidth={12} strokeLinecap="round"/>
  <path d={seated ? 'M9 87 L26 104 L29 127' : `M9 87 L${17 - walk * 10} 126`} fill="none" stroke={p.ink} strokeWidth={12} strokeLinecap="round"/>
  <path d="M-18 46 Q0 34 18 46 L14 89 L-14 89 Z" fill={coat ?? p.accent}/>
  <circle cx={0} cy={18} r={19} fill={p.soft} stroke={p.ink} strokeWidth={2}/>
  <path d="M-18 16 Q-15 -10 9 -1 Q23 2 19 14 Q6 5 -18 16" fill={elderly ? p.quiet : p.ink}/>
  <path d="M3 22 L8 23 M1 31 Q5 33 10 30" stroke={p.ink} strokeWidth={1.7} fill="none"/>
  {elderly ? <><path d="M12 62 Q29 58 30 88 L30 128" fill="none" stroke={p.quiet} strokeWidth={3}/><path d="M-11 18 H-2 M1 18 H10 M-2 18 H1" stroke={p.ink} strokeWidth={2}/></> : null}
</g>;

export const Coin = ({x, y, p, size = 12, opacity = 1}: {x: number; y: number; p: PeoplePalette; size?: number; opacity?: number}) => <g opacity={opacity}>
  <circle cx={x} cy={y} r={size} fill={p.accent} stroke={p.paper} strokeWidth={1.8}/>
  <path d={`M${x - size * .25} ${y - size * .45} H${x + size * .15} M${x - size * .25} ${y} H${x + size * .25} M${x} ${y - size * .6} V${y + size * .55}`} stroke={p.paper} strokeWidth={1.7}/>
</g>;

export const House = ({x, y, p, scale = 1, filled = true}: {x: number; y: number; p: PeoplePalette; scale?: number; filled?: boolean}) => <g transform={`translate(${x} ${y}) scale(${scale})`}>
  <path d="M-91 11 L0 -64 L91 11 V124 H-91 Z" fill={filled ? p.soft : 'none'} stroke={p.ink} strokeWidth={3}/>
  <path d="M-105 15 L0 -76 L105 15" fill="none" stroke={p.accent} strokeWidth={10} strokeLinejoin="round"/>
  <path d="M-20 124 V51 H20 V124" fill={p.paper} stroke={p.ink} strokeWidth={2}/>
  <rect x={-69} y={32} width={32} height={33} fill={p.paper} stroke={p.ink} strokeWidth={2}/>
  <rect x={37} y={32} width={32} height={33} fill={p.paper} stroke={p.ink} strokeWidth={2}/>
  <path d="M-53 32 V65 M-69 48 H-37 M53 32 V65 M37 48 H69" stroke={p.rule} strokeWidth={2}/>
</g>;

export const Shop = ({x, y, p, scale = 1, sign = 'CỬA HÀNG'}: {x: number; y: number; p: PeoplePalette; scale?: number; sign?: string}) => <g transform={`translate(${x} ${y}) scale(${scale})`}>
  <path d="M-144 -75 H144 V122 H-144 Z" fill={p.soft} stroke={p.ink} strokeWidth={3}/>
  <rect x={-158} y={-82} width={316} height={53} fill={p.ink}/>
  <InkText x={0} y={-47} p={p} color={p.paper} size={25}>{sign}</InkText>
  {Array.from({length: 8}, (_, i) => <path key={i} d={`M${-156 + i * 39} -29 h39 l9 40 h-48 Z`} fill={i % 2 ? p.paper : p.accent} stroke={p.ink} strokeWidth={1.5}/>)}
  <rect x={-125} y={25} width={167} height={72} fill={p.paper} stroke={p.ink} strokeWidth={2}/>
  <path d="M-121 68 H38" stroke={p.quiet} strokeWidth={3}/>
  {[0, 1, 2, 3, 4].map(i => <rect key={i} x={-115 + i * 28} y={42 + i % 2 * 6} width={21} height={23 - i % 2 * 6} fill={i % 2 ? p.soft : p.accent} stroke={p.ink} strokeWidth={1.3}/>)}
  <rect x={62} y={22} width={61} height={100} fill={p.paper} stroke={p.ink} strokeWidth={2}/>
  <circle cx={109} cy={77} r={3} fill={p.accent}/>
</g>;

export const Bag = ({x, y, p, scale = 1, opacity = 1}: {x: number; y: number; p: PeoplePalette; scale?: number; opacity?: number}) => <g transform={`translate(${x} ${y}) scale(${scale})`} opacity={opacity}>
  <path d="M-27 0 H27 L35 63 H-35 Z" fill={p.accent} stroke={p.ink} strokeWidth={2}/>
  <path d="M-14 7 V-8 C-14 -25 14 -25 14 -8 V7" fill="none" stroke={p.ink} strokeWidth={4}/>
</g>;

export const Calendar = ({x, y, p, scale = 1, mark = 0}: {x: number; y: number; p: PeoplePalette; scale?: number; mark?: number}) => <g transform={`translate(${x} ${y}) scale(${scale})`}>
  <rect x={-84} y={-70} width={168} height={154} rx={6} fill={p.paper} stroke={p.ink} strokeWidth={3}/>
  <path d="M-84 -32 H84" stroke={p.ink} strokeWidth={3}/>
  <rect x={-84} y={-70} width={168} height={36} fill={p.accent}/>
  {[-48, 0, 48].map(x1 => <path key={x1} d={`M${x1} -82 v26`} stroke={p.ink} strokeWidth={7} strokeLinecap="round"/>)}
  {Array.from({length: 12}, (_, i) => <rect key={i} x={-65 + i % 4 * 36} y={-14 + Math.floor(i / 4) * 29} width={23} height={19} fill={p.soft} stroke={p.rule} strokeWidth={1}/>)}
  <path d="M16 51 l10 11 23 -29" fill="none" stroke={p.accent} strokeWidth={7} strokeLinecap="round" strokeDasharray="55" strokeDashoffset={55 * (1 - mark)}/>
</g>;

export const Shield = ({x, y, p, scale = 1, opacity = 1}: {x: number; y: number; p: PeoplePalette; scale?: number; opacity?: number}) => <g transform={`translate(${x} ${y}) scale(${scale})`} opacity={opacity}>
  <path d="M0 -71 L62 -48 V6 Q59 58 0 85 Q-59 58 -62 6 V-48 Z" fill={p.soft} stroke={p.accent} strokeWidth={5}/>
  <path d="M-28 2 L-6 26 L34 -20" fill="none" stroke={p.ink} strokeWidth={8} strokeLinecap="round" strokeLinejoin="round"/>
</g>;

export const Building = ({x, y, p, floors = 5, complete = 1, scale = 1}: {x: number; y: number; p: PeoplePalette; floors?: number; complete?: number; scale?: number}) => <g transform={`translate(${x} ${y}) scale(${scale})`}>
  <path d={`M-85 0 L-85 ${-floors * 42} L65 ${-floors * 42} L105 ${-floors * 42 + 25} V25 H-45 Z`} fill={p.soft} stroke={p.ink} strokeWidth={3}/>
  <path d={`M65 ${-floors * 42} V0 L105 25 V${-floors * 42 + 25}`} fill={p.rule} stroke={p.ink} strokeWidth={2}/>
  {Array.from({length: floors}, (_, i) => <g key={i} opacity={i < floors * complete ? 1 : .22}>
    <path d={`M-85 ${-i * 42} H65 L105 ${-i * 42 + 25}`} fill="none" stroke={p.ink} strokeWidth={2}/>
    {[-60, -13, 34].map(wx => <rect key={wx} x={wx} y={-i * 42 - 31} width={24} height={20} fill={i < floors * complete ? p.paper : 'none'} stroke={p.ink} strokeWidth={1.6}/>)}
  </g>)}
  <path d="M-13 0 V-34 H13 V0" fill={p.ink}/>
</g>;

export const Arrow = ({d, p, color, dashed = false, opacity = 1}: {d: string; p: PeoplePalette; color?: string; dashed?: boolean; opacity?: number}) => <path d={d} fill="none" stroke={color ?? p.accent} strokeWidth={4} strokeLinecap="round" strokeDasharray={dashed ? '8 10' : undefined} opacity={opacity}/>;
