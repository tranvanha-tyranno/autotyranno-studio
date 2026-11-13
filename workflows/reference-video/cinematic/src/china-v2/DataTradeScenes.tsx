import type {ReactNode} from 'react';

/** Each export branch is an authored mechanism, not a relabelled template.
 * Statistical numbers are the checked NBS values; geometry in trade scenes is
 * explicitly explanatory. The caller owns title, source notes and captions.
 */
type Palette = {paper: string; ink: string; accent: string; quiet: string; rule: string; soft: string};
type Props = {shot: any; frame: number; p: Palette};
const font = 'Bahnschrift,Arial,sans-serif';
const clamp = (v: number) => Math.max(0, Math.min(1, v));
const ease = (v: number) => 1 - (1 - clamp(v)) ** 3;
const stage = (t: number, start: number, end: number) => ease((t - start) / (end - start));
const fmt = (n: number) => new Intl.NumberFormat('vi-VN', {maximumFractionDigits: 1}).format(n);
const Text = ({x, y, children, fill, size = 28, bold = false, anchor = 'start', opacity = 1}: {
  x: number; y: number; children: ReactNode; fill: string; size?: number; bold?: boolean;
  anchor?: 'start' | 'middle' | 'end'; opacity?: number;
}) => <text x={x} y={y} fill={fill} fontFamily={bold ? font : 'Arial,sans-serif'} fontSize={size}
  fontWeight={bold ? 700 : 400} textAnchor={anchor} opacity={opacity}>{children}</text>;

const Sheet = ({x, y, w, h, p, children, turn = 0}: {x: number; y: number; w: number; h: number; p: Palette; children?: ReactNode; turn?: number}) =>
  <g transform={`translate(${x} ${y}) rotate(${turn} ${w / 2} ${h / 2})`}>
    <rect x={12} y={15} width={w} height={h} rx={6} fill={p.ink} opacity={.08}/>
    <path d={`M0,0 H${w - 35} L${w},35 V${h} H0 Z`} fill={p.paper} stroke={p.rule} strokeWidth={2}/>
    <path d={`M${w - 35},0 V35 H${w}`} fill={p.soft} stroke={p.rule} strokeWidth={2}/>{children}
  </g>;
const Crate = ({x, y, w = 125, h = 85, p, color, label, scale = 1}: {x: number; y: number; w?: number; h?: number; p: Palette; color?: string; label?: string; scale?: number}) =>
  <g transform={`translate(${x} ${y}) scale(${scale})`}>
    <path d={`M0,18 L25,0 H${w + 25} L${w},18 Z`} fill={p.soft} stroke={p.rule} strokeWidth={2}/>
    <path d={`M${w},18 L${w + 25},0 V${h - 18} L${w},${h} Z`} fill={p.quiet} opacity={.35}/>
    <rect y={18} width={w} height={h - 18} fill={color ?? p.accent} stroke={p.ink} strokeOpacity={.15} strokeWidth={2}/>
    {Array.from({length: 5}, (_, i) => <line key={i} x1={15 + i * (w - 30) / 4} x2={15 + i * (w - 30) / 4} y1={27} y2={h - 8} stroke={p.paper} opacity={.25} strokeWidth={3}/>)}
    {label ? <Text x={w / 2} y={h / 2 + 24} size={22} fill={p.paper} anchor="middle" bold>{label}</Text> : null}
  </g>;
const Wheel = ({x, y, p}: {x: number; y: number; p: Palette}) => <g><circle cx={x} cy={y} r={22} fill={p.ink}/><circle cx={x} cy={y} r={10} fill={p.rule}/></g>;
const Ship = ({x, y, p, length = 420}: {x: number; y: number; p: Palette; length?: number}) =>
  <g transform={`translate(${x} ${y})`}>
    <ellipse cx={length / 2} cy={164} rx={length * .54} ry={13} fill={p.ink} opacity={.1}/>
    <path d={`M0,108 H${length} L${length - 62},158 H45 Z`} fill={p.ink}/>
    <path d={`M12,123 H${length - 20}`} stroke={p.accent} strokeWidth={5}/>
    <rect x={length - 100} y={28} width={65} height={80} fill={p.soft} stroke={p.quiet} strokeWidth={2}/>
    <rect x={length - 89} y={42} width={39} height={15} fill={p.ink}/>
    <line x1={length - 65} x2={length - 65} y1={-5} y2={28} stroke={p.quiet} strokeWidth={3}/>
    <Crate x={35} y={34} w={95} h={73} p={p}/><Crate x={145} y={34} w={95} h={73} p={p} color={p.quiet}/>
    <Crate x={89} y={-39} w={95} h={73} p={p} color={p.soft}/>
  </g>;
const Part = ({x, y, p, type = 'gear', opacity = 1, scale = 1}: {x: number; y: number; p: Palette; type?: string; opacity?: number; scale?: number}) =>
  <g transform={`translate(${x} ${y}) scale(${scale})`} opacity={opacity}>
    {type === 'chip' ? <g><rect x={-36} y={-30} width={72} height={60} rx={7} fill={p.accent}/><rect x={-21} y={-17} width={42} height={34} fill={p.paper} opacity={.6}/>{Array.from({length: 4}, (_, i) => <g key={i}><line x1={-50} x2={-36} y1={-22 + i * 15} y2={-22 + i * 15} stroke={p.quiet} strokeWidth={5}/><line x1={36} x2={50} y1={-22 + i * 15} y2={-22 + i * 15} stroke={p.quiet} strokeWidth={5}/></g>)}</g> : type === 'coil' ? <g><ellipse rx={48} ry={37} fill={p.soft} stroke={p.quiet} strokeWidth={4}/><ellipse rx={32} ry={25} fill="none" stroke={p.quiet} strokeWidth={3}/><ellipse rx={16} ry={13} fill={p.paper} stroke={p.quiet} strokeWidth={3}/></g> : <g><path d="M-10,-48 H10 L16,-33 L29,-27 L45,-29 L54,-12 L42,0 L42,15 L50,27 L37,43 L21,38 L7,45 L-1,58 L-21,51 L-25,36 L-39,27 L-54,25 L-57,5 L-42,-2 L-37,-16 L-42,-32 L-25,-44 L-10,-37 Z" fill={p.quiet} opacity={.8}/><circle r={20} fill={p.paper}/></g>}
  </g>;
const Arrow = ({x1, x2, y, p, opacity = 1}: {x1: number; x2: number; y: number; p: Palette; opacity?: number}) =>
  <g opacity={opacity}><line x1={x1} x2={x2 - 13} y1={y} y2={y} stroke={p.quiet} strokeWidth={3}/><path d={`M${x2 - 23},${y - 9} L${x2},${y} L${x2 - 23},${y + 9}`} fill="none" stroke={p.quiet} strokeWidth={3}/></g>;

function ManufacturingReceipt({t, p}: {t: number; p: Palette}) {
  const scan = stage(t, .08, .48), reveal = stage(t, .28, .55);
  return <g>
    <Sheet x={155} y={280} w={640} h={535} p={p} turn={-2}>
      <Text x={42} y={60} fill={p.quiet} size={22}>NBS · Hạch toán sơ bộ</Text>
      <Text x={42} y={116} fill={p.ink} size={35} bold>GIÁ TRỊ TĂNG THÊM</Text>
      <line x1={40} x2={590} y1={145} y2={145} stroke={p.rule} strokeWidth={2}/>
      {['Kỳ đo', 'Phạm vi', 'Cách so sánh', 'Cách tính giá'].map((v, i) => <g key={v}><Text x={42} y={202 + i * 67} fill={p.quiet} size={23}>{v}</Text><Text x={250} y={202 + i * 67} fill={p.ink} size={25} bold>{['1–9 / 2026', 'Ngành chế tạo', 'Cùng kỳ năm trước', 'Giá so sánh'][i]}</Text></g>)}
      <rect x={30} y={218} width={560 * scan} height={46} fill={p.accent} opacity={.11}/>
    </Sheet>
    <g opacity={reveal} transform={`translate(${(1 - reveal) * 70} 0)`}>
      <Text x={1305} y={495} fill={p.accent} size={170} bold anchor="middle">+5,6%</Text>
      <Text x={1305} y={558} fill={p.ink} size={30} anchor="middle">Chế tạo · chín tháng đầu 2026</Text>
      <line x1={995} x2={1615} y1={642} y2={642} stroke={p.quiet} strokeWidth={2}/>
      {Array.from({length: 11}, (_, i) => <g key={i}><line x1={995 + 62 * i} x2={995 + 62 * i} y1={i % 5 === 0 ? 626 : 633} y2={654} stroke={p.quiet} strokeWidth={2}/>{i % 5 === 0 ? <Text x={995 + i * 62} y={689} fill={p.quiet} size={24} anchor="middle">{i}</Text> : null}</g>)}
      <g transform={`translate(${995 + 62 * 5.6 * reveal} 0)`}><path d="M-13,600 L13,600 L0,622 Z" fill={p.accent}/><line y1={600} y2={565} stroke={p.accent} strokeWidth={3}/></g>
      <Text x={1305} y={760} fill={p.quiet} size={25} anchor="middle">Tốc độ tăng, không phải mức lợi nhuận</Text>
    </g>
  </g>;
}

function SectorTracks({t, p}: {t: number; p: Palette}) {
  const xmin = 550, xmax = 1650, zero = 1100, scale = (xmax - xmin) / 12;
  return <g>
    <rect x={130} y={275} width={1660} height={550} rx={16} fill={p.soft} opacity={.32}/>
    {[-6, -3, 0, 3, 6].map(v => <g key={v}><line x1={zero + v * scale} x2={zero + v * scale} y1={320} y2={730} stroke={v === 0 ? p.ink : p.rule} strokeWidth={v === 0 ? 3 : 1}/><Text x={zero + v * scale} y={785} fill={p.quiet} anchor="middle" size={24}>{v > 0 ? '+' : ''}{v}%</Text></g>)}
    {[{name: 'Chế tạo', value: 5.6, color: p.accent}, {name: 'Xây dựng', value: -4.1, color: '#af705b'}, {name: 'Dịch vụ', value: 5.2, color: p.ink}].map((s, i) => {
      const a = stage(t, .08 + i * .13, .35 + i * .13), yy = 385 + i * 145, xx = zero + s.value * scale * a;
      return <g key={s.name}><Text x={190} y={yy + 12} fill={p.ink} bold size={36}>{s.name}</Text><line x1={xmin} x2={xmax} y1={yy} y2={yy} stroke={p.rule} strokeWidth={2}/><line x1={zero} x2={xx} y1={yy} y2={yy} stroke={s.color} strokeWidth={8}/><circle cx={xx} cy={yy} r={18} fill={s.color} stroke={p.paper} strokeWidth={5}/><Text x={xx} y={yy - 35} fill={s.color} size={37} bold anchor="middle" opacity={a}>{s.value > 0 ? '+' : '−'}{fmt(Math.abs(s.value))}%</Text></g>;
    })}
  </g>;
}

function InvestmentTiles({t, p}: {t: number; p: Palette}) {
  const removal = stage(t, .22, .66);
  return <g>
    <g transform={`translate(180 315) skewY(-6)`}>
      {Array.from({length: 100}, (_, i) => {
        const removed = i >= 80, partial = i === 79, col = i % 10, row = Math.floor(i / 10);
        const fly = removed ? stage(t, .2 + ((99 - i) / 20) * .18, .59 + ((99 - i) / 20) * .18) : 0;
        return <g key={i} transform={`translate(${col * 57 + fly * 170} ${row * 43 - fly * 100})`} opacity={1 - fly * .85}>
          <path d="M0,0 L13,-9 H61 L48,0 Z" fill={p.soft}/><path d="M48,0 L61,-9 V20 L48,30 Z" fill={p.quiet} opacity={.35}/><rect width={48} height={30} fill={removed ? p.accent : p.ink} opacity={removed ? 1 : .86}/>{partial ? <rect x={48 * (1 - .6 * removal)} width={48 * .6 * removal} height={30} fill={p.paper}/> : null}
        </g>;
      })}
    </g>
    <g transform={`translate(${35 * (1 - removal)} 0)`}>
      <Text x={1305} y={360} fill={p.quiet} anchor="middle" size={26}>Chỉ số so sánh tính từ mức 100</Text>
      <Text x={1100} y={485} fill={p.ink} size={91} bold anchor="middle">100</Text>
      <Arrow x1={1200} x2={1360} y={450} p={p}/>
      <Text x={1510} y={485} fill={p.accent} size={91} bold anchor="middle">79,4</Text>
      <Text x={1305} y={603} fill={p.accent} size={73} bold anchor="middle">−20,6%</Text>
      <Text x={1305} y={675} fill={p.ink} size={30} anchor="middle">Đầu tư phát triển bất động sản</Text>
      <Text x={1305} y={720} fill={p.quiet} size={26} anchor="middle">1–9 / 2026 · so cùng kỳ</Text>
      <path d="M1030,755 H1580" stroke={p.accent} strokeWidth={3}/>
      <Text x={1305} y={800} fill={p.ink} size={27} anchor="middle">Không phải chỉ số giá nhà</Text>
    </g>
  </g>;
}

function PriceLens({t, p}: {t: number; p: Palette}) {
  const through = stage(t, .27, .67), lensX = 730 + through * 390;
  return <g>
    <Sheet x={175} y={280} w={550} h={520} p={p} turn={-3}>
      <Text x={38} y={60} fill={p.quiet} size={23}>CHI TIÊU BÌNH QUÂN ĐẦU NGƯỜI</Text>
      <Text x={38} y={110} fill={p.ink} size={31} bold>Giá hiện hành</Text>
      <Text x={275} y={270} fill={p.accent} size={115} anchor="middle" bold>+3,6%</Text>
      {['Hàng hóa', 'Dịch vụ', 'Mức giá'].map((s, i) => <g key={s}><Text x={40} y={350 + 47 * i} size={24} fill={p.quiet}>{s}</Text><line x1={220} x2={475} y1={343 + i * 47} y2={343 + i * 47} stroke={p.rule} strokeWidth={4}/></g>)}
    </Sheet>
    <path d="M750,520 C920,400 1050,400 1210,520" stroke={p.rule} strokeWidth={4} strokeDasharray="7 12" fill="none"/>
    <g transform={`translate(${lensX} 470)`}>
      <line x1={62} x2={160} y1={85} y2={190} stroke={p.ink} strokeWidth={26} strokeLinecap="round"/>
      <circle r={118} fill={p.paper} fillOpacity={.86} stroke={p.ink} strokeWidth={14}/>
      <circle r={100} fill="none" stroke={p.accent} strokeWidth={3}/>
      <Text x={0} y={-10} fill={p.accent} anchor="middle" size={27} bold>ĐIỀU CHỈNH</Text>
      <Text x={0} y={32} fill={p.ink} anchor="middle" size={39} bold>GIÁ</Text>
    </g>
    <g opacity={stage(t, .48, .73)}>
      <Text x={1485} y={397} fill={p.quiet} size={29} anchor="middle">Sau điều chỉnh giá</Text>
      <Text x={1485} y={548} fill={p.ink} size={115} anchor="middle" bold>+2,7%</Text>
      <Text x={1485} y={617} fill={p.accent} size={31} anchor="middle" bold>Mức tăng thực</Text>
    </g>
    <Text x={1095} y={798} fill={p.quiet} anchor="middle" size={27}>Cùng kỳ đo 1–9 / 2026 · hai cách biểu đạt</Text>
  </g>;
}

function ImportsWorkshop({t, p}: {t: number; p: Palette}) {
  const incoming = stage(t, .04, .3), outgoing = stage(t, .44, .82), domestic = stage(t, .62, .91);
  return <g>
    <line x1={130} x2={1780} y1={765} y2={765} stroke={p.rule} strokeWidth={3}/>
    <Ship x={110 - incoming * 65} y={585} p={p} length={360}/>
    <Text x={300} y={338} fill={p.ink} size={33} bold anchor="middle">Đầu vào nhập khẩu</Text>
    {[['coil', 0], ['gear', 1], ['chip', 2]].map(([type, i]) => {
      const ix = Number(i), move = stage(t, .12 + ix * .055, .4 + ix * .055);
      return <Part key={type} x={330 + move * 450} y={452 + ix * 65 - move * ix * 38} p={p} type={String(type)} scale={1 - move * .3} opacity={1 - stage(t, .43, .53)}/>
    })}
    <g transform="translate(720 380)">
      <ellipse cx={200} cy={380} rx={280} ry={22} fill={p.ink} opacity={.07}/>
      <path d="M0,95 L75,43 L75,95 L150,43 L150,95 L255,20 V340 H0 Z" fill={p.soft} stroke={p.quiet} strokeWidth={3}/>
      <rect x={256} y={110} width={150} height={230} fill={p.paper} stroke={p.quiet} strokeWidth={3}/>
      <rect x={280} y={145} width={102} height={80} fill={p.ink} opacity={.1}/>
      <rect x={285} y={255} width={92} height={85} fill={p.quiet}/>
      {Array.from({length: 3}, (_, i) => <rect key={i} x={25 + i * 73} y={145} width={48} height={80} fill={p.paper} stroke={p.rule} strokeWidth={2}/>)}
      <Text x={200} y={-30} fill={p.ink} anchor="middle" size={33} bold>Sản xuất trong nước</Text>
    </g>
    <Crate x={1060 + outgoing * 410} y={490 - outgoing * 70} w={145} h={100} p={p} label="HÀNG"/>
    <g opacity={outgoing}><Arrow x1={1250} x2={1390} y={430} p={p}/><Text x={1570} y={338} fill={p.accent} anchor="middle" size={32} bold>Xuất khẩu</Text></g>
    <g opacity={domestic} transform={`translate(1390 ${580 + (1 - domestic) * 30})`}>
      <rect x={0} y={65} width={290} height={120} fill={p.soft} stroke={p.quiet} strokeWidth={2}/>
      <path d="M-10,65 H300 L275,20 H15 Z" fill={p.accent}/>
      {Array.from({length: 6}, (_, i) => <rect key={i} x={i * 50} y={65} width={25} height={20} fill={p.paper} opacity={.7}/>)}
      <rect x={30} y={108} width={135} height={60} fill={p.paper}/><rect x={198} y={100} width={60} height={85} fill={p.quiet}/>
      <Text x={145} y={-8} fill={p.ink} anchor="middle" size={30} bold>Thị trường nội địa</Text>
    </g>
  </g>;
}

function GDPMethod({t, p}: {t: number; p: Palette}) {
  const exclude = stage(t, .36, .78);
  return <g>
    <Text x={960} y={330} fill={p.ink} size={58} bold anchor="middle">C + I + G + (X − M)</Text>
    <g transform="translate(165 410)">
      <rect x={0} y={0} width={620} height={340} rx={15} fill={p.soft} stroke={p.rule} strokeWidth={2}/>
      <Text x={310} y={55} fill={p.ink} anchor="middle" size={32} bold>Giá trị tạo ở nước ngoài</Text>
      <Part x={135 + exclude * 60} y={175 - exclude * 75} p={p} type="chip" opacity={1 - exclude * .65} scale={1.15}/>
      <Part x={305 + exclude * 60} y={175 - exclude * 75} p={p} type="coil" opacity={1 - exclude * .65} scale={1.15}/>
      <Part x={470 + exclude * 60} y={175 - exclude * 75} p={p} opacity={1 - exclude * .65} scale={1.15}/>
      <Text x={310} y={290} fill={p.quiet} anchor="middle" size={26}>Không tính thành sản lượng nội địa</Text>
    </g>
    <Sheet x={1030} y={395} w={700} h={385} p={p} turn={1}>
      <Text x={42} y={68} fill={p.ink} size={34} bold>Sổ tính GDP theo chi tiêu</Text>
      <line x1={40} x2={650} y1={100} y2={100} stroke={p.rule} strokeWidth={3}/>
      <Text x={48} y={160} fill={p.quiet} size={29}>Xuất khẩu</Text><Text x={632} y={160} fill={p.ink} size={37} bold anchor="end">X</Text>
      <Text x={48} y={230} fill={p.quiet} size={29}>Trừ phần nhập khẩu</Text><Text x={632} y={230} fill={p.accent} size={37} bold anchor="end">− M</Text>
      <line x1={40} x2={650} y1={268} y2={268} stroke={p.ink} strokeWidth={2}/>
      <Text x={48} y={325} fill={p.ink} size={29} bold>Xuất khẩu ròng</Text><Text x={632} y={325} fill={p.accent} size={37} bold anchor="end">X − M</Text>
      <rect x={35} y={186} width={620 * exclude} height={60} fill={p.accent} opacity={.12}/>
    </Sheet>
    <g opacity={exclude}><path d="M815,530 L980,530 M950,504 L982,530 L950,556" stroke={p.accent} strokeWidth={5} fill="none"/><Text x={960} y={831} fill={p.ink} size={28} anchor="middle">Phép điều chỉnh thống kê — không phải “nhập khẩu là xấu”</Text></g>
  </g>;
}

function ArithmeticBlocks({t, p}: {t: number; p: Palette}) {
  const minus = stage(t, .22, .6), remain = stage(t, .55, .82);
  return <g>
    <Text x={430} y={350} fill={p.ink} size={44} bold anchor="middle">+10 đơn vị</Text>
    <Text x={1120} y={350} fill={p.quiet} size={44} bold anchor="middle">−7 đơn vị</Text>
    <Text x={1640} y={350} fill={p.accent} size={44} bold anchor="middle">= +3</Text>
    <path d="M140,720 H1750 L1680,770 H200 Z" fill={p.soft} stroke={p.rule} strokeWidth={2}/>
    {Array.from({length: 10}, (_, i) => {
      const col = i % 5, row = Math.floor(i / 5), selected = i < 7;
      const a = selected ? stage(t, .2 + i * .02, .52 + i * .02) : 0;
      const keep = selected ? 0 : remain;
      const initialX = 180 + col * 105, initialY = 495 + row * 120;
      const targetX = selected ? 950 + (i % 4) * 110 : 1430 + (i - 7) * 105;
      const targetY = selected ? 470 + Math.floor(i / 4) * 110 : 570;
      const travel = selected ? a : keep;
      const x = initialX + (targetX - initialX) * travel;
      const y = initialY + (targetY - initialY) * travel - Math.sin(travel * Math.PI) * 140;
      return <g key={i}><Crate x={x} y={y} w={75} h={84} p={p} color={selected ? p.quiet : p.accent}/></g>;
    })}
    <g opacity={minus}><path d="M1035,418 V660 H1485 V418" fill="none" stroke={p.quiet} strokeDasharray="8 8" strokeWidth={3}/><Text x={1260} y={704} fill={p.quiet} size={26} anchor="middle">Phần nhập khẩu tăng</Text></g>
    <Text x={435} y={804} fill={p.quiet} size={26} anchor="middle">Xuất khẩu tăng</Text>
    <Text x={1610} y={804} fill={p.accent} size={26} anchor="middle">Chênh lệch tăng</Text>
    <rect x={685} y={385} width={120} height={70} rx={35} fill={p.paper} stroke={p.rule} strokeWidth={2}/><Text x={745} y={436} fill={p.ink} size={62} anchor="middle">−</Text>
    <Text x={960} y={846} fill={p.quiet} size={24} anchor="middle">Ví dụ số học giả định · không phải đóng góp GDP thực tế</Text>
  </g>;
}

function ExportObstacles({t, p}: {t: number; p: Palette}) {
  const shipmove = stage(t, .03, .8), stamps = ['Thị hiếu', 'Cạnh tranh', 'Vận chuyển', 'Chính sách'];
  return <g>
    <path d="M140,720 Q500,675 850,720 T1770,720" fill="none" stroke={p.rule} strokeWidth={4}/>
    <g transform={`translate(${160 + 1020 * shipmove} 0)`}><Ship x={0} y={560} p={p} length={350}/></g>
    {stamps.map((name, i) => {
      const a = stage(t, .08 + i * .14, .2 + i * .14), x = 220 + i * 405;
      return <g key={name} opacity={a} transform={`translate(${x} ${302 - (1 - a) * 55}) rotate(${i % 2 ? 3 : -3} 150 100)`}>
        <rect x={0} y={0} width={300} height={180} rx={8} fill={p.paper} stroke={p.quiet} strokeWidth={3}/>
        <path d="M18,18 H282 V162 H18 Z" fill="none" stroke={p.rule} strokeWidth={2}/>
        <Text x={150} y={78} fill={p.ink} anchor="middle" size={31} bold>{name}</Text>
        {i === 0 ? <path d="M95,120 C95,95 120,95 130,112 C145,88 175,93 175,115 C175,139 135,153 135,153 Z" fill={p.accent}/> : i === 1 ? <g><path d="M80,140 L125,95 L160,127 L220,76" stroke={p.accent} strokeWidth={6} fill="none"/><path d="M190,76 H220 V106" stroke={p.accent} strokeWidth={6} fill="none"/></g> : i === 2 ? <g><rect x={82} y={100} width={90} height={40} fill={p.accent}/><path d="M172,108 H200 L216,128 V140 H172 Z" fill={p.quiet}/><Wheel x={105} y={142} p={p}/><Wheel x={191} y={142} p={p}/></g> : <g><rect x={110} y={95} width={75} height={18} fill={p.accent}/><path d="M145,110 L165,145 H130 Z" fill={p.quiet}/><path d="M92,147 H203" stroke={p.quiet} strokeWidth={5}/></g>}
        <line x1={150} x2={150} y1={185} y2={290} stroke={p.rule} strokeWidth={2} strokeDasharray="5 7"/>
      </g>;
    })}
    <Text x={960} y={820} fill={p.ink} anchor="middle" size={28}>Đơn hàng bên ngoài còn chịu nhiều điều kiện</Text>
  </g>;
}

function SupplyPivot({t, p}: {t: number; p: Palette}) {
  const reroute = stage(t, .25, .7);
  return <g>
    <rect x={135} y={277} width={460} height={520} rx={18} fill={p.soft} fillOpacity={.35} stroke={p.rule} strokeWidth={2}/>
    <rect x={730} y={277} width={440} height={520} rx={18} fill={p.soft} fillOpacity={.35} stroke={p.rule} strokeWidth={2}/>
    <rect x={1330} y={277} width={460} height={520} rx={18} fill={p.soft} fillOpacity={.35} stroke={p.rule} strokeWidth={2}/>
    <Text x={365} y={330} fill={p.ink} anchor="middle" size={33} bold>Nhà cung cấp</Text>
    <Text x={950} y={330} fill={p.ink} anchor="middle" size={33} bold>Hoàn thiện</Text>
    <Text x={1560} y={330} fill={p.ink} anchor="middle" size={33} bold>Người mua</Text>
    <Part x={290} y={450} p={p} type="chip" scale={1.2}/><Part x={430} y={450} p={p} type="coil" scale={1.2}/>
    <Part x={290} y={620} p={p} scale={1.2}/><Part x={430} y={620} p={p} type="chip" scale={1.2}/>
    <Crate x={865} y={410 - reroute * 15} w={135} h={100} p={p} label="A"/>
    <Crate x={865} y={620} w={135} h={100} p={p} label="B" color={p.quiet}/>
    <path d="M565,456 H825 M1035,456 H1390" fill="none" stroke={p.quiet} strokeWidth={3} strokeDasharray="6 8"/>
    <path d="M565,620 C660,620 685,675 825,675 M1035,675 C1190,675 1210,535 1390,535" fill="none" stroke={p.accent} strokeWidth={5} strokeDasharray={900} strokeDashoffset={900 * (1 - reroute)}/>
    <g transform={`translate(${570 + 210 * reroute} ${620 + 55 * reroute})`} opacity={stage(t, .27, .45)}><circle r={15} fill={p.accent}/><circle r={25} stroke={p.accent} fill="none" strokeWidth={2} opacity={.35}/></g>
    <g transform="translate(1430 420)"><path d="M0,90 H270 L245,220 H25 Z" fill="none" stroke={p.ink} strokeWidth={5}/><path d="M55,90 L95,0 M215,90 L175,0" fill="none" stroke={p.ink} strokeWidth={5}/><Crate x={80} y={125} w={100} h={70} p={p}/></g>
    <Text x={960} y={840} fill={p.ink} anchor="middle" size={27}>Một khâu điều chỉnh ≠ toàn bộ chuỗi giá trị chuyển đi</Text>
  </g>;
}

function ReceiptLayers({t, p}: {t: number; p: Palette}) {
  const stages = [.03, .22, .43, .65];
  return <g>
    {[
      {x: 145, y: 280, w: 445, h: 510, name: 'Kim ngạch gộp', key: 'HÀNG XUẤT KHẨU', lines: ['Giá trị giao dịch', 'Không phải thu nhập hộ']},
      {x: 570, y: 340, w: 430, h: 450, name: 'Chi phí', key: 'HÓA ĐƠN ĐẦU VÀO', lines: ['Nguyên liệu · vận hành', 'Vốn · vận chuyển']},
      {x: 985, y: 400, w: 365, h: 390, name: 'Lợi nhuận', key: 'KẾT QUẢ DOANH NGHIỆP', lines: ['Phần còn lại sau chi phí', 'Còn phụ thuộc nhiều yếu tố']},
      {x: 1355, y: 300, w: 410, h: 490, name: 'Thu nhập hộ', key: 'BẢNG THU NHẬP', lines: ['Lương · các nguồn thu', 'Phân bổ giữa các hộ khác nhau']},
    ].map((s, i) => {
      const a = stage(t, stages[i], stages[i] + .19);
      return <g key={s.name} opacity={a} transform={`translate(0 ${55 * (1 - a)})`}>
        <Sheet x={s.x} y={s.y} w={s.w} h={s.h} p={p} turn={i % 2 ? 1.8 : -1.6}>
          <Text x={28} y={46} fill={p.quiet} size={19}>{s.key}</Text><line x1={28} x2={s.w - 28} y1={68} y2={68} stroke={p.rule} strokeWidth={2}/>
          <Text x={s.w / 2} y={143} fill={i === 3 ? p.accent : p.ink} size={36} anchor="middle" bold>{s.name}</Text>
          {Array.from({length: 4}, (_, j) => <line key={j} x1={32} x2={s.w - 32 - j % 2 * 75} y1={186 + j * 35} y2={186 + j * 35} stroke={p.rule} strokeWidth={5}/>)}
          {s.lines.map((line, j) => <Text key={line} x={s.w / 2} y={s.h - 75 + j * 38} fill={p.quiet} size={i === 2 ? 19 : 22} anchor="middle">{line}</Text>)}
        </Sheet>
      </g>;
    })}
    <Text x={960} y={840} fill={p.ink} size={28} anchor="middle">Đọc từng đại lượng — không suy thẳng từ kim ngạch tới mức sống</Text>
  </g>;
}

function GDPBook({t, p}: {t: number; p: Palette}) {
  const open = stage(t, .08, .58), big = stage(t, .27, .64);
  return <g>
    <g transform={`translate(${185 - open * 20} ${320 + open * 5})`}>
      <path d="M0,45 L430,5 L730,120 V435 L430,315 L0,355 Z" fill={p.ink} opacity={.12}/>
      <path d="M0,0 L430,-40 L430,290 L0,330 Z" fill={p.soft} stroke={p.rule} strokeWidth={3}/>
      <path d={`M430,-40 L${430 + 280 * open},${-40 + 130 * open} V${290 + 130 * open} L430,290 Z`} fill={p.paper} stroke={p.quiet} strokeWidth={3}/>
      <path d="M430,-40 V290" stroke={p.quiet} strokeWidth={7}/>
      <Text x={200} y={100} fill={p.ink} size={76} bold anchor="middle">GDP</Text>
      <Text x={200} y={160} fill={p.quiet} size={29} anchor="middle">Hạch toán sơ bộ</Text>
      {Array.from({length: 4}, (_, i) => <line key={i} x1={55} x2={350} y1={210 + i * 25} y2={185 + i * 25} stroke={p.rule} strokeWidth={4}/>)}
      <Text x={575} y={195} fill={p.ink} size={52} bold anchor="middle" opacity={open}>1–9</Text>
      <Text x={575} y={250} fill={p.quiet} size={30} anchor="middle" opacity={open}>2026</Text>
    </g>
    <g opacity={big}>
      <Text x={1360} y={482} fill={p.accent} size={170} bold anchor="middle">+4,6%</Text>
      <Text x={1360} y={555} fill={p.ink} size={34} anchor="middle">So cùng kỳ · giá so sánh</Text>
      <path d="M1060,610 H1660" stroke={p.rule} strokeWidth={3}/>
      {Array.from({length: 9}, (_, i) => <g key={i} transform={`translate(${1070 + i * 65} 655)`} opacity={stage(t, .28 + i * .025, .48 + i * .025)}><rect width={49} height={57} rx={5} fill={p.soft}/><rect width={49} height={13} rx={3} fill={p.accent}/><Text x={24.5} y={43} fill={p.ink} anchor="middle" size={24} bold>{i + 1}</Text></g>)}
      <Text x={1360} y={790} fill={p.quiet} size={27} anchor="middle">Chưa phải kết quả cả năm 2026</Text>
    </g>
  </g>;
}

function QuarterCalendars({t, p}: {t: number; p: Palette}) {
  const yy = (v: number) => 732 - v * 55;
  return <g>
    {[0, 2, 4, 6].map(v => <g key={v}><line x1={315} x2={1740} y1={yy(v)} y2={yy(v)} stroke={p.rule} strokeWidth={1.5}/><Text x={270} y={yy(v) + 8} fill={p.quiet} size={25} anchor="end">{v}%</Text></g>)}
    {[{q: 'Q1', v: 5, months: 'Tháng 1–3'}, {q: 'Q2', v: 4.3, months: 'Tháng 4–6'}, {q: 'Q3', v: 4.5, months: 'Tháng 7–9'}].map((s, i) => {
      const a = stage(t, .06 + .16 * i, .33 + .16 * i), x = 585 + 450 * i, y = yy(s.v * a);
      return <g key={s.q}>
        <rect x={x - 155} y={275} width={310} height={520} rx={15} fill={p.paper} stroke={p.rule} strokeWidth={2}/>
        <rect x={x - 155} y={275} width={310} height={90} rx={15} fill={p.soft}/>
        <rect x={x - 155} y={330} width={310} height={35} fill={p.soft}/>
        {[-80, 80].map(d => <line key={d} x1={x + d} x2={x + d} y1={260} y2={295} stroke={p.quiet} strokeWidth={9} strokeLinecap="round"/>)}
        <Text x={x} y={337} fill={p.ink} size={40} bold anchor="middle">{s.q}</Text>
        <line x1={x} x2={x} y1={732} y2={y} stroke={p.rule} strokeWidth={3}/>
        <circle cx={x} cy={y} r={16} fill={p.accent}/><circle cx={x} cy={y} r={26} fill="none" stroke={p.accent} strokeWidth={2} opacity={.4}/>
        <Text x={x} y={y - 40} fill={p.ink} size={48} bold anchor="middle" opacity={a}>{s.v === 5 ? '5,0' : fmt(s.v)}%</Text>
        <Text x={x} y={777} fill={p.quiet} size={22} anchor="middle">{s.months}</Text>
      </g>;
    })}
    <Text x={960} y={840} fill={p.ink} size={28} anchor="middle">Từng quý so với cùng kỳ năm trước · không phải so quý liền trước</Text>
  </g>;
}

function ObligationFolders({t, p}: {t: number; p: Palette}) {
  const move = stage(t, .18, .46), actual = stage(t, .58, .88);
  return <g>
    <g transform="translate(165 360)">
      <path d="M0,35 H130 L155,0 H420 L440,35 V360 H0 Z" fill={p.soft} stroke={p.quiet} strokeWidth={3}/>
      <Text x={220} y={100} fill={p.ink} size={32} bold anchor="middle">Bảng cân đối A</Text>
      {[0, 1, 2].map(i => <line key={i} x1={40} x2={390} y1={155 + i * 55} y2={155 + i * 55} stroke={p.rule} strokeWidth={5}/>)}
    </g>
    <g transform="translate(765 360)">
      <path d="M0,35 H130 L155,0 H420 L440,35 V360 H0 Z" fill={p.paper} stroke={p.quiet} strokeWidth={3}/>
      <Text x={220} y={100} fill={p.ink} size={32} bold anchor="middle">Bảng cân đối B</Text>
      {[0, 1, 2].map(i => <line key={i} x1={40} x2={390} y1={155 + i * 55} y2={155 + i * 55} stroke={p.rule} strokeWidth={5}/>)}
    </g>
    {[0, 1, 2].map(i => {
      const x = 235 + 600 * move, y = 505 + i * 64;
      return <g key={i} transform={`translate(${x} ${y})`} opacity={1 - actual}><rect width={290} height={49} rx={4} fill={p.accent}/><Text x={145} y={33} fill={p.paper} size={24} bold anchor="middle">Nghĩa vụ {i + 1}</Text></g>;
    })}
    <Text x={685} y={320} fill={p.quiet} anchor="middle" size={29} opacity={1 - actual}>Đổi nơi ghi nhận ≠ tự xóa rủi ro</Text>
    <g opacity={actual} transform={`translate(1370 ${370 + (1 - actual) * 55})`}>
      <path d="M0,0 H340 V330 H0 Z" fill={p.paper} stroke={p.quiet} strokeWidth={2}/>
      <Text x={170} y={65} fill={p.ink} size={32} anchor="middle" bold>XỬ LÝ THỰC</Text>
      <Text x={170} y={135} fill={p.quiet} size={24} anchor="middle">Nhận diện tổn thất</Text>
      <Text x={170} y={185} fill={p.quiet} size={24} anchor="middle">Tái cơ cấu nghĩa vụ</Text>
      <Text x={170} y={235} fill={p.quiet} size={24} anchor="middle">Hoàn thiện dự án</Text>
      <path d="M140,275 L160,294 L205,252" fill="none" stroke={p.accent} strokeWidth={7}/>
    </g>
    <g opacity={actual}><path d="M860,535 L890,565 L950,495" fill="none" stroke={p.accent} strokeWidth={8}/><Text x={985} y={657} fill={p.quiet} size={26} anchor="middle">Không chỉ chuyển chỗ</Text></g>
    <Text x={960} y={820} fill={p.ink} size={28} anchor="middle">Cơ chế minh họa · không phải bảng cân đối của tổ chức cụ thể</Text>
  </g>;
}

export const DATA_TRADE_IDS = ['f05', 'f06', 'r04', 'h04', 't02', 't03', 't04', 't05', 't06', 't07', 'p01', 'p02', 'p06'] as const;

export const DataTradeScene: React.FC<Props> = ({shot, frame, p}) => {
  const t = clamp(frame / Math.max(1, shot.end - shot.start - 1));
  const contents: Record<string, ReactNode> = {
    f05: <ManufacturingReceipt t={t} p={p}/>, f06: <SectorTracks t={t} p={p}/>,
    r04: <InvestmentTiles t={t} p={p}/>, h04: <PriceLens t={t} p={p}/>,
    t02: <ImportsWorkshop t={t} p={p}/>, t03: <GDPMethod t={t} p={p}/>,
    t04: <ArithmeticBlocks t={t} p={p}/>, t05: <ExportObstacles t={t} p={p}/>,
    t06: <SupplyPivot t={t} p={p}/>, t07: <ReceiptLayers t={t} p={p}/>,
    p01: <GDPBook t={t} p={p}/>, p02: <QuarterCalendars t={t} p={p}/>,
    p06: <ObligationFolders t={t} p={p}/>,
  };
  if (!contents[shot.id]) throw new Error(`No authored data/trade scene for ${shot.id}`);
  return <svg width={1920} height={1080} viewBox="0 0 1920 1080" style={{position: 'absolute', inset: 0}}>{contents[shot.id]}</svg>;
};
