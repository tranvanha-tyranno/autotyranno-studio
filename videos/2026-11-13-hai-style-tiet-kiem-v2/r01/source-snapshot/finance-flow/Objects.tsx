import React from 'react';

/** Original, code-native desk props. Coordinates are object centres unless noted.
 * Every export returns <g>; the owning scene supplies the SVG camera and timing.
 */
export const P = {
  paper: '#F4F0E5',
  ink: '#1C2526',
  yellow: '#EFE34B',
  green: '#197863',
  red: '#D05B46',
  muted: '#78817B',
  line: '#CDD1C5',
};

type Positioned = {x: number; y: number; scale?: number};
type Angled = Positioned & {rotate?: number; opacity?: number};
const typeStyle: React.CSSProperties = {fontFamily: 'Arial, sans-serif', fontVariantNumeric: 'tabular-nums'};
const at = ({x, y, scale = 1, rotate = 0}: Angled) => `translate(${x} ${y}) rotate(${rotate}) scale(${scale})`;
const outline = {stroke: P.ink, strokeWidth: 5, strokeLinecap: 'round', strokeLinejoin: 'round'} as const;

export const Label: React.FC<{x?: number; y?: number; children: React.ReactNode; size?: number; color?: string; anchor?: 'start'|'middle'|'end'; weight?: number}> = ({x = 0, y = 0, children, size = 26, color = P.ink, anchor = 'middle', weight = 700}) => <text x={x} y={y} textAnchor={anchor} fill={color} fontSize={size} fontWeight={weight} style={typeStyle}>{children}</text>;

/** 160 × 86; enough detail to read as a money token without imitating currency. */
export const Bill: React.FC<Angled & {value?: string; fill?: string}> = (props) => {
  const {value = '1 tr', fill = P.yellow, opacity = 1} = props;
  return <g transform={at(props)} opacity={opacity} {...outline}>
    <rect x="-77" y="-39" width="160" height="86" rx="9" fill={P.ink} stroke="none" opacity=".13"/>
    <rect x="-80" y="-43" width="160" height="86" rx="9" fill={fill}/>
    <path d="M-63-27H-49M-63-27V-14M63-27H49M63-27V-14M-63 27H-49M-63 27V14M63 27H49M63 27V14" fill="none" strokeWidth="3"/>
    <ellipse cx="0" cy="0" rx="42" ry="31" fill={P.paper} strokeWidth="2.5"/>
    <text x="0" y="10" textAnchor="middle" stroke="none" fill={P.ink} fontSize="29" fontWeight="700" style={typeStyle}>{value}</text>
  </g>;
};

/** 360 × 200 body; open raises its back lip by up to 66 units. */
export const Wallet: React.FC<Positioned & {open?: number; label?: string; amount?: string}> = (props) => {
  const {open = 0, label = 'CÒN LẠI', amount = ''} = props;
  const o = Math.min(1, Math.max(0, open));
  return <g transform={at(props)} {...outline}>
    <ellipse cx="10" cy="116" rx="181" ry="17" fill={P.ink} opacity=".12" stroke="none"/>
    <path d={`M-180-56Q-180-91-143-91H146Q177-91 177-56V-66L151 ${-105 - o * 66}H-147Q-180 ${-100 - o * 58}-180-56Z`} fill={P.ink}/>
    <rect x="-180" y="-88" width="360" height="194" rx="29" fill={P.green}/>
    <path d="M-154-63H151M-154 79H151" fill="none" stroke={P.paper} strokeWidth="2" strokeDasharray="6 8" opacity=".65"/>
    <path d="M164-21H207Q221-21 221-6V31Q221 46 207 46H164Q145 46 145 28V-3Q145-21 164-21Z" fill={P.yellow}/>
    <circle cx="184" cy="12" r="9" fill={P.ink} stroke="none"/>
    <text x="-12" y="-25" textAnchor="middle" stroke="none" fill={P.paper} fontSize="22" fontWeight="700" letterSpacing="2" style={typeStyle}>{label}</text>
    <text x="-12" y="41" textAnchor="middle" stroke="none" fill={P.paper} fontSize="57" fontWeight="700" letterSpacing="-2" style={typeStyle}>{amount}</text>
  </g>;
};

/** 300 × 180; open expands the flap above the body, keeping the label clear. */
export const Envelope: React.FC<Positioned & {label: string; fill?: string; open?: number; amount?: string}> = (props) => {
  const {label, fill = P.yellow, open = 0, amount = ''} = props;
  const o = Math.min(1, Math.max(0, open));
  return <g transform={at(props)} {...outline}>
    <rect x="-143" y="-82" width="300" height="180" rx="11" fill={P.ink} stroke="none" opacity=".12"/>
    <path d={`M-150-90L0 ${-12 - o * 166}L150-90Z`} fill={fill}/>
    <rect x="-150" y="-90" width="300" height="180" rx="11" fill={fill}/>
    <path d="M-145 85L-47 7M145 85L47 7" strokeWidth="3" opacity=".3"/>
    {o < .98 && <path d={`M-150-90L0 ${-12 - o * 166}L150-90`} fill="none" strokeWidth="4" opacity={1 - o}/>} 
    <text x="0" y="28" textAnchor="middle" fill={P.ink} stroke="none" fontSize="23" fontWeight="700" letterSpacing=".5" style={typeStyle}>{label}</text>
    <text x="0" y="65" textAnchor="middle" fill={P.ink} stroke="none" fontSize="31" fontWeight="700" style={typeStyle}>{amount}</text>
  </g>;
};

/** 180 × 230; centre at (x,y). Amount is the illustrated expense, no pricing claim. */
export const Receipt: React.FC<Angled & {amount?: string; day?: number; label?: string}> = (props) => {
  const {amount = '60.000', day, label = 'CHI THÊM', opacity = 1} = props;
  return <g transform={at(props)} opacity={opacity} {...outline}>
    <path d="M-84-109H96V109L81 121 66 109 51 121 36 109 21 121 6 109-9 121-24 109-39 121-54 109-69 121-84 109Z" fill={P.ink} stroke="none" opacity=".12"/>
    <path d="M-90-115L-75-106-60-115-45-106-30-115-15-106 0-115 15-106 30-115 45-106 60-115 75-106 90-115V103L75 115 60 103 45 115 30 103 15 115 0 103-15 115-30 103-45 115-60 103-75 115-90 103Z" fill="#FFFEF6" strokeWidth="3"/>
    <path d="M-64-38H64M-64 33H64" stroke={P.line} strokeWidth="2"/>
    <text x="0" y="-66" textAnchor="middle" fill={P.ink} stroke="none" fontSize={label.length>16?13:18} fontWeight="700" style={typeStyle}>{label}</text>
    <text x="0" y="8" textAnchor="middle" fill={P.ink} stroke="none" fontSize="33" fontWeight="700" letterSpacing="-1" style={typeStyle}>{amount}</text>
    <text x="0" y="62" textAnchor="middle" fill={P.muted} stroke="none" fontSize="16" fontWeight="700" style={typeStyle}>{day === undefined ? 'VÍ DỤ GIẢ ĐỊNH' : `NGÀY ${String(day).padStart(2, '0')}`}</text>
    <g stroke={P.ink} strokeWidth="2.3" opacity=".55">{[0, 5, 9, 17, 22, 27, 35, 43, 48, 55, 63, 67, 73, 81, 88, 94].map((v, i) => <path key={v} d={`M${v - 48} 76V${i % 3 === 0 ? 91 : 87}`}/>)}</g>
  </g>;
};

/** Body 560 × 480. Intake/rollers centre (0,0), output slot centre (0,162).
 * Rotating roller markings are driven only by the supplied active/frame pair.
 */
export const Printer: React.FC<Positioned & {frame: number; sum: string; count: number; active?: boolean; meal?: boolean}> = (props) => {
  const {frame, sum, count, active = false, meal = false} = props;
  const angle = active ? frame * 16 : 0;
  return <g transform={at(props)} {...outline}>
    <ellipse cx="8" cy="256" rx="281" ry="22" fill={P.ink} stroke="none" opacity=".13"/>
    <path d="M-280-139L-237-226Q-228-242-207-242H206Q228-242 237-226L280-139V202Q280 238 245 238H-245Q-280 238-280 202Z" fill={P.ink}/>
    <path d="M-280-139H280V187Q280 215 250 215H-250Q-280 215-280 187Z" fill={P.yellow}/>
    <rect x="-216" y="-208" width="432" height="128" rx="14" fill={P.paper}/>
    <text x="-187" y="-176" fill={P.muted} stroke="none" fontSize="17" fontWeight="700" letterSpacing="1.1" style={typeStyle}>{meal ? 'CỘNG THÊM BỮA ĂN' : `${String(count).padStart(2, '0')} / 30 NGÀY`}</text>
    <text x="187" y="-112" textAnchor="end" fill={P.ink} stroke="none" fontSize="49" fontWeight="700" letterSpacing="-1.5" style={typeStyle}>{sum}</text>
    <rect x="-241" y="-43" width="482" height="85" rx="27" fill={P.ink}/>
    <rect x="-204" y="-12" width="408" height="21" rx="10" fill="#0E1516" stroke="none"/>
    {[-220, 220].map((x) => <g key={x} transform={`translate(${x} 0) rotate(${angle})`}><circle cx="0" cy="0" r="21" fill={P.paper} strokeWidth="3"/><path d="M-13 0H13M0-13V13" fill="none" strokeWidth="3"/></g>)}
    <path d="M-229 70H-101M-229 86H-101M-229 102H-101" strokeWidth="4" opacity=".45"/>
    {[0, 1, 2].map((i) => <g key={i}><rect x={-55 + i * 85} y="67" width="61" height="48" rx="10" fill={i === 2 ? P.red : P.paper} strokeWidth="3"/><path d={i === 0 ? 'M-37 91H-12' : i === 1 ? 'M53 80V102M42 91H64' : 'M128 84L141 96M141 84L128 96'} fill="none" stroke={i === 2 ? P.paper : P.ink} strokeWidth="3"/></g>)}
    <rect x="-179" y="151" width="358" height="22" rx="11" fill={P.ink}/>
    <path d="M-176 187H176" stroke={P.paper} strokeWidth="2" strokeDasharray="5 9"/>
    <circle cx="240" cy="166" r="8" fill={active ? P.green : P.paper} strokeWidth="2.5"/>
  </g>;
};

export const Plate: React.FC<Positioned> = (props) => <g transform={at(props)} {...outline}>
  <ellipse cx="5" cy="14" rx="141" ry="89" fill={P.ink} opacity=".12" stroke="none"/>
  <ellipse cx="0" cy="0" rx="136" ry="89" fill={P.paper}/>
  <ellipse cx="0" cy="0" rx="105" ry="65" fill="#FFFEF6" strokeWidth="2.5"/>
  <path d="M-59 7Q-47-33-12-35Q22-42 36-9Q51 10 28 28Q-12 55-51 28Z" fill={P.yellow} strokeWidth="3"/>
  <path d="M-36-5L-30 7M-10-12L-2 0M-12 22L-3 25M15 7L24 1" stroke={P.paper} strokeWidth="6"/>
  <path d="M45-32Q67-41 72-19Q83-10 62 2Q54 20 40 7Q22 3 33-13Z" fill={P.green} strokeWidth="3"/>
  <path d="M41-8L62-20" stroke={P.paper} strokeWidth="2"/>
  <circle cx="-60" cy="-29" r="15" fill={P.red} strokeWidth="3"/>
  <path d="M-174-73V75M-192-73V-35Q-192-15-174-15Q-156-15-156-35V-73M-174-73V-36M171-71Q144-60 149-26Q152-7 171-7V75" fill="none" strokeWidth="6"/>
</g>;

/** Palm at (x,y), forearm extends 430 units right; rotate to place a receipt. */
export const Hand: React.FC<Angled> = (props) => <g transform={at(props)} opacity={props.opacity ?? 1} {...outline}>
  <path d="M430-65H180Q151-65 120-95L37-139Q8-153-7-127Q-18-105 8-89L61-53H-37Q-69-53-64-22Q-61-1-31-1L36 1-44 12Q-75 16-65 45Q-60 64-30 60L48 46-11 68Q-41 81-24 105Q-13 125 16 115L100 87Q139 72 168 48H430Z" fill="#E6AD7F"/>
  <path d="M61-53L97-30M36 1L75-5M48 46L88 24M127-28Q108 8 124 40" fill="none" stroke="#B67A53" strokeWidth="3"/>
  <path d="M317-65H430V48H317Z" fill={P.green}/>
  <path d="M321-51V34" stroke={P.paper} strokeWidth="2" strokeDasharray="5 7"/>
</g>;
