import {CanvasImage, staticFile} from 'remotion';
import {
  Bag, Building, Calendar, Coin, House, InkText, Person, Shield, Shop,
  stage, type PeoplePalette, type PeopleProps,
} from './PeoplePrimitives';

const small = {fontFamily: 'Arial,sans-serif', fontSize: 21};
const label = (text: string, x: number, y: number, p: PeoplePalette, size = 27) => <InkText x={x} y={y} p={p} size={size}>{text}</InkText>;
const glide = (a: number, b: number, v: number) => a + (b - a) * v;

const FamilyDecision = ({t, p}: {t: number; p: PeoplePalette}) => {
  const defer = stage(t, .28, .6), save = stage(t, .52, .88);
  return <g>
    <path d="M210 768 H1710 M230 780 H1690" stroke={p.rule} strokeWidth={3}/>
    <House x={285} y={490} p={p} scale={1.1}/>
    <g transform={`translate(${glide(0, -10, defer)} 0)`} opacity={1 - defer * .45}>
      <path d="M975 357 L1307 341 L1322 585 L990 601 Z" fill={p.soft} stroke={p.ink} strokeWidth={3}/>
      <path d="M1009 468 H1283 M1030 423 l35 -41 h145 l40 41 v56 h-220 Z" fill={p.paper} stroke={p.ink} strokeWidth={3}/>
      <circle cx={1072} cy={481} r={18} fill={p.ink}/><circle cx={1220} cy={481} r={18} fill={p.ink}/>
      {label('Món mua lớn', 1154, 554, p, 30)}
      <g opacity={defer} transform={`rotate(-8 1170 430)`}><rect x={1062} y={399} width={201} height={70} rx={4} fill={p.paper} stroke={p.accent} strokeWidth={4}/>{label('TẠM HOÃN', 1162, 445, p, 29)}</g>
    </g>
    <rect x={637} y={561} width={85} height={137} rx={9} fill={p.rule} stroke={p.ink} strokeWidth={2}/>
    <rect x={808} y={561} width={80} height={133} rx={9} fill={p.rule} stroke={p.ink} strokeWidth={2}/>
    <Person x={680} y={510} scale={1.35} p={p} seated arm={.6}/>
    <Person x={847} y={510} scale={1.23} p={p} coat={p.quiet} seated arm={.2}/>
    <path d="M510 640 L1535 620 L1590 685 L550 710 Z" fill={p.soft} stroke={p.ink} strokeWidth={3}/>
    <path d="M580 706 V825 M1508 690 V815" stroke={p.ink} strokeWidth={14}/>
    <rect x={890} y={608} width={132} height={62} rx={8} fill={p.ink}/>
    <path d="M920 629 H981 M933 646 H968" stroke={p.paper} strokeWidth={3}/>
    <g transform="translate(1420 510)"><path d="M-66 0 H66 L77 126 Q0 150 -77 126 Z" fill={p.paper} stroke={p.accent} strokeWidth={4}/><rect x={-74} y={-18} width={148} height={28} rx={5} fill={p.ink}/>{label('DỰ PHÒNG', 0, 70, p, 25)}</g>
    {Array.from({length: 7}, (_, i) => {
      const v = stage(t, .45 + i * .035, .65 + i * .035);
      return <Coin key={i} x={glide(960, 1391 + i % 3 * 28, v)} y={glide(606, 615 - Math.floor(i / 3) * 29, v) - Math.sin(v * Math.PI) * 140} p={p} size={12} opacity={.25 + .75 * save}/>;
    })}
    {label('Triển vọng thu nhập', 398, 355, p, 28)}
    <path d="M400 378 Q436 433 511 481" fill="none" stroke={p.quiet} strokeWidth={2} strokeDasharray="5 6"/>
    <InkText x={1070} y={835} p={p} size={27} color={p.quiet}>Vẫn có việc ≠ sẵn sàng chi lớn</InkText>
  </g>;
};

const FinishOrExpand = ({t, p}: {t: number; p: PeoplePalette}) => <g>
  <path d="M200 760 H1720" stroke={p.rule} strokeWidth={4}/>
  <g transform={`translate(${glide(-12, 0, stage(t, 0, .7))} 0)`}>
    <Building x={557} y={702} floors={7} complete={.45 + stage(t, .1, .78) * .55} scale={1.12} p={p}/>
    <path d="M385 708 H756 L803 745 H342 Z" fill={p.rule} stroke={p.ink} strokeWidth={2}/>
    <Person x={375 + stage(t, .56, .85) * 75} y={633} p={p} scale={.78} arm={.65}/>
    <path d="M763 394 V650 M745 405 H900 M792 405 V455" stroke={p.quiet} strokeWidth={5}/>
    <g opacity={stage(t, .68, .9)}><path d="M712 589 l20 24 43 -61" fill="none" stroke={p.accent} strokeWidth={9} strokeLinecap="round"/></g>
    {label('Hoàn thiện dự án cũ', 545, 805, p, 31)}
    {label('Thực hiện nghĩa vụ đã có', 545, 844, p, 23)}
  </g>
  <g transform="translate(1245 0)">
    <path d="M-210 698 L92 663 L256 736 L-53 781 Z" fill={p.soft} stroke={p.ink} strokeWidth={2}/>
    <path d="M-170 696 L95 676 L204 730 L-52 753 Z" fill={p.paper} stroke={p.rule} strokeWidth={4}/>
    {[0, 1, 2].map(i => <path key={i} d={`M${-122 + i * 95} 712 v-101 l38 -3 v110`} fill={p.rule} stroke={p.ink} strokeWidth={2}/>)}
    <path d="M-122 611 V377 L88 358 V642 M-122 377 L40 440 L88 358 M-26 367 L88 423" fill="none" stroke={p.rule} strokeWidth={3} strokeDasharray="9 9"/>
    <path d="M150 404 V645 M135 420 H294 M235 420 V505" stroke={p.quiet} strokeWidth={5}/>
    <path d="M235 505 v25 h-18" fill="none" stroke={p.accent} strokeWidth={4}/>
    {label('Cam kết xây thêm', 0, 805, p, 31)}
    {label('Cần nhu cầu và hiệu quả', 0, 844, p, 23)}
  </g>
  <path d="M960 327 V790" stroke={p.rule} strokeWidth={2} strokeDasharray="7 10"/>
</g>;

const PayrollTown = ({t, p}: {t: number; p: PeoplePalette}) => {
  const wage = stage(t, .08, .4), buy = stage(t, .38, .7), revenue = stage(t, .68, .94);
  return <g>
    <path d="M300 577 C480 725 670 787 950 773 C1230 758 1475 664 1560 532 C1350 275 708 280 350 475" fill="none" stroke={p.rule} strokeWidth={40}/>
    <path d="M300 577 C480 725 670 787 950 773 C1230 758 1475 664 1560 532 C1350 275 708 280 350 475" fill="none" stroke={p.paper} strokeWidth={3} strokeDasharray="20 24"/>
    <g transform="translate(430 420)">
      <path d="M-163 165 V-44 L-58 1 V-45 L41 0 V-44 L150 0 V165 Z" fill={p.soft} stroke={p.ink} strokeWidth={3}/>
      <path d="M115 -5 V-88 H149 V8" fill={p.quiet}/>
      {Array.from({length: 8}, (_, i) => <rect key={i} x={-133 + i % 4 * 66} y={35 + Math.floor(i / 4) * 55} width={40} height={29} fill={p.paper} stroke={p.ink} strokeWidth={2}/>)}
      {label('Doanh nghiệp', 0, 207, p, 29)}
    </g>
    <House x={950} y={661} p={p} scale={.85}/>
    <Shop x={1470} y={420} p={p} scale={1.03}/>
    <Person x={glide(1030, 1370, buy)} y={glide(660, 522, buy)} p={p} scale={.72} walk={Math.sin(buy * Math.PI * 8)}/>
    <Bag x={glide(1058, 1404, buy)} y={glide(707, 569, buy)} p={p} scale={.5} opacity={stage(t, .61, .78)}/>
    <g transform={`translate(${glide(520, 866, wage)} ${glide(492, 674, wage) - Math.sin(wage * Math.PI) * 100}) rotate(${glide(-15, 7, wage)})`} opacity={stage(t, .03, .12) * (1 - stage(t, .43, .54))}>
      <rect x={-55} y={-26} width={110} height={62} fill={p.accent} stroke={p.ink} strokeWidth={2}/><path d="M-55 -26 L0 9 L55 -26" fill="none" stroke={p.paper} strokeWidth={3}/>
    </g>
    {[0, 1, 2, 3].map(i => <Coin key={i} x={glide(1440 - i * 20, 488 - i * 20, revenue)} y={350 - Math.sin(revenue * Math.PI) * (65 + i * 18)} p={p} size={11} opacity={stage(t, .63, .74)}/>) }
    <InkText x={760} y={477} p={p} size={29} color={p.accent}> trả thu nhập </InkText>
    <InkText x={1240} y={695} p={p} size={29} color={p.accent}> chi tiêu </InkText>
    <InkText x={995} y={315} p={p} size={29} color={p.accent}> doanh thu → tiếp tục hoạt động </InkText>
  </g>;
};

const HouseholdConditions = ({t, p}: {t: number; p: PeoplePalette}) => <g>
  <path d="M215 800 H1705" stroke={p.rule} strokeWidth={5}/>
  <path d="M1100 760 V370 H1665 V760" fill={p.soft} stroke={p.ink} strokeWidth={3}/>
  <rect x={1175} y={422} width={134} height={117} fill={p.paper} stroke={p.ink} strokeWidth={2}/>
  <path d="M1242 422 V539 M1175 481 H1309" stroke={p.rule} strokeWidth={4}/>
  <rect x={1397} y={602} width={66} height={109} rx={7} fill={p.rule} stroke={p.ink} strokeWidth={2}/>
  <rect x={1532} y={603} width={57} height={104} rx={7} fill={p.rule} stroke={p.ink} strokeWidth={2}/>
  <Person x={1430} y={561} p={p} scale={.96} seated arm={.6}/><Person x={1560} y={566} p={p} scale={.86} seated coat={p.quiet} arm={.4}/>
  <path d="M1350 657 H1632 V685 H1350 M1380 685 V760 M1607 685 V760" stroke={p.ink} strokeWidth={7} fill={p.paper}/>
  <g opacity={stage(t, .06, .2)} transform={`translate(358 ${glide(420, 390, stage(t, .03, .28))})`}>
    <rect x={-123} y={-88} width={246} height={207} fill={p.paper} stroke={p.ink} strokeWidth={3}/>
    <path d="M-82 -43 H80 M-82 -10 H80 M-82 23 H19" stroke={p.rule} strokeWidth={8}/>
    <path d="M37 46 l21 20 40 -44" fill="none" stroke={p.accent} strokeWidth={8}/>
    {label('Công việc', 0, 174, p, 28)}
  </g>
  <Calendar x={755} y={437} p={p} scale={1.12} mark={stage(t, .25, .49)}/>
  {label('Thu nhập kỳ vọng', 755, 582, p, 28)}
  <g transform="translate(367 693)" opacity={stage(t, .39, .56)}><path d="M-100 -65 H100 V64 H-100 Z" fill={p.soft} stroke={p.ink} strokeWidth={2}/><path d="M-70 -26 H67 M-70 5 H40" stroke={p.quiet} strokeWidth={5}/>{label('Nghĩa vụ nợ', 0, 39, p, 26)}</g>
  <Shield x={757} y={702} p={p} scale={.76} opacity={stage(t, .5, .7)}/>
  <g opacity={stage(t, .5, .7)}>{label('Dự phòng', 757, 821, p, 27)}</g>
  <g opacity={stage(t, .68, .88)}><path d="M1004 660 h68" stroke={p.accent} strokeWidth={4}/><path d="M1052 645 l20 15 -20 15" fill="none" stroke={p.accent} strokeWidth={4}/><Bag x={1214} y={673} p={p} scale={.75}/>{label('Quyết định chi', 1331, 820, p, 28)}</g>
</g>;

const AllocationJars = ({t, p, id}: {t: number; p: PeoplePalette; id: string}) => {
  const xs = [465, 960, 1455], vals = [50, 25, 25], names = ['TIÊU DÙNG', 'TRẢ NGHĨA VỤ', 'DỰ PHÒNG'];
  return <g>
    <path d="M200 746 L1685 716 L1758 766 L270 801 Z" fill={p.soft} stroke={p.ink} strokeWidth={3}/>
    <path d="M300 797 V839 M1668 777 V837" stroke={p.ink} strokeWidth={10}/>
    {xs.map((x, j) => <g key={x}>
      <defs><clipPath id={`${id}-jar-${j}`}><path d={`M${x - 136} 425 H${x + 136} L${x + 157} 693 Q${x} 730 ${x - 157} 693 Z`}/></clipPath></defs>
      <path d={`M${x - 136} 425 H${x + 136} L${x + 157} 693 Q${x} 730 ${x - 157} 693 Z`} fill={p.paper} stroke={p.ink} strokeWidth={3}/>
      <g clipPath={`url(#${id}-jar-${j})`}>
        {Array.from({length: vals[j]}, (_, i) => {
          const columns = j === 0 ? 10 : 5, v = stage(t, .06 + j * .12 + i * .002, .32 + j * .12 + i * .002);
          const targetX = x - (columns - 1) * 12 + i % columns * 24, targetY = 676 - Math.floor(i / columns) * 30;
          return <Coin key={i} x={targetX} y={glide(343 - i * 2, targetY, v)} p={p} size={10.3} opacity={v}/>;
        })}
      </g>
      <path d={`M${x - 145} 406 H${x + 145} V430 H${x - 145} Z`} fill={p.ink}/>
      <InkText x={x} y={374} p={p} size={56} color={p.accent}>{vals[j]}</InkText>
      <rect x={x - 130} y={447} width={260} height={47} rx={3} fill={p.paper} stroke={p.rule} strokeWidth={1.5}/>
      {label(names[j], x, 480, p, 27)}
    </g>)}
    <InkText x={960} y={314} p={p} size={24} color={p.quiet}>100 phần thu nhập giả định · mỗi đồng xu = 1 phần</InkText>
    <InkText x={960} y={837} p={p} size={24} color={p.accent}>MINH HỌA CƠ CHẾ — không phải cơ cấu thực của Trung Quốc</InkText>
  </g>;
};

const DifferentBaskets = ({t, p}: {t: number; p: PeoplePalette}) => <g>
  <path d="M240 751 H1690" stroke={p.rule} strokeWidth={4}/>
  <path d="M254 485 H1690" stroke={p.quiet} strokeWidth={2} strokeDasharray="9 8" opacity={stage(t, .42, .65)}/>
  <g opacity={stage(t, .5, .7)}><rect x={803} y={446} width={325} height={49} fill={p.paper}/>{label('Một số bình quân', 965, 480, p, 26)}</g>
  {[425, 960, 1495].map((x, j) => {
    const v = stage(t, j * .1, .35 + j * .1), heights = [115, 205, 65], n = [6, 10, 3];
    return <g key={x}>
      <Person x={x - 80} y={glide(580, 555, v)} p={p} scale={.77} arm={.35}/><Person x={x + 10} y={572} p={p} scale={.64} coat={p.quiet}/>
      <path d={`M${x - 151} 662 H${x + 151} L${x + 130} 745 H${x - 130} Z`} fill={p.soft} stroke={p.ink} strokeWidth={3}/>
      <path d={`M${x - 150} 662 Q${x} ${662 - heights[j] * v} ${x + 150} 662`} fill="none" stroke={p.accent} strokeWidth={5}/>
      {Array.from({length: n[j]}, (_, i) => <g key={i} opacity={stage(t, .1 + i * .02, .42 + i * .02)}><rect x={x - 105 + i % 5 * 46} y={647 - Math.floor(i / 5) * 47} width={34} height={32} rx={3} fill={i % 2 ? p.accent : p.quiet} stroke={p.paper} strokeWidth={2}/></g>)}
      {label(`Hộ ${String.fromCharCode(65 + j)}`, x, 802, p, 30)}
    </g>;
  })}
  <InkText x={960} y={837} p={p} size={23} color={p.quiet}>Các giỏ hàng chỉ minh họa sự khác nhau; không phải số liệu khảo sát</InkText>
</g>;

const ScopeBaskets = ({t, p}: {t: number; p: PeoplePalette}) => {
  const open = stage(t, .18, .7);
  return <g>
    <path d="M300 330 L1657 292 L1707 783 L349 820 Z" fill={p.soft} stroke={p.rule} strokeWidth={3}/>
    <path d="M349 820 L360 835 L1718 798 L1707 783" fill={p.rule}/>
    <InkText x={1000} y={363} p={p} size={36}>Tiêu dùng hộ gia đình trong GDP</InkText>
    <g transform={`translate(${glide(-25, 0, open)} 0)`}>
      <path d="M414 442 L881 431 L894 722 L427 737 Z" fill={p.paper} stroke={p.ink} strokeWidth={3}/>
      <path d="M427 737 L438 750 L906 735 L894 722" fill={p.rule}/>
      <Bag x={520} y={532} p={p} scale={1.08}/>
      <path d="M620 526 h107 l12 86 h-131 Z" fill={p.soft} stroke={p.ink} strokeWidth={3}/><path d="M630 524 q40 -65 77 0" fill="none" stroke={p.accent} strokeWidth={4}/>
      <path d="M758 534 h67 v82 h-67 Z M770 552 h43" fill={p.quiet} stroke={p.ink} strokeWidth={2}/>
      {label('Hàng hóa', 650, 679, p, 31)}
    </g>
    <g opacity={open} transform={`translate(${glide(60, 0, open)} 0)`}>
      <path d="M997 440 L1554 424 L1567 714 L1010 730 Z" fill={p.paper} stroke={p.ink} strokeWidth={3}/>
      <path d="M1010 730 L1021 744 L1579 729 L1567 714" fill={p.rule}/>
      <path d="M1066 543 h90 v75 h-90 Z M1111 523 v115 M1082 580 h58" fill={p.soft} stroke={p.accent} strokeWidth={5}/>
      <path d="M1205 530 q36 -16 74 0 v92 q-38 -16 -74 0 Z M1279 530 q37 -16 74 0 v92 q-37 -16 -74 0 Z" fill={p.soft} stroke={p.ink} strokeWidth={3}/>
      <path d="M1407 532 v75 M1392 533 v28 q15 17 30 0 v-28 M1453 533 v75" fill="none" stroke={p.ink} strokeWidth={7} strokeLinecap="round"/>
      {label('Dịch vụ và phạm vi khác', 1279, 676, p, 30)}
    </g>
    <path d="M728 399 L748 370" stroke={p.accent} strokeWidth={3}/><InkText x={585} y={408} p={p} size={24}>Bán lẻ hàng hóa có phạm vi riêng</InkText>
    <InkText x={1000} y={804} p={p} size={23} color={p.quiet}>Sơ đồ phạm vi khái niệm, không biểu thị tỷ trọng hay đồng nhất hai chỉ tiêu</InkText>
  </g>;
};

const SupportBridge = ({t, p}: {t: number; p: PeoplePalette}) => {
  const build = stage(t, .12, .55), move = stage(t, .5, .92);
  const walkerX = glide(492, 1340, move), u = (walkerX - 472) / 974;
  const bridgeHeight = (1 - u) * (1 - u) * 747 + 2 * (1 - u) * u * 632 + u * u * 741;
  const walkerY = bridgeHeight - .74 * 131;
  return <g>
    <path d="M210 766 L554 766 L602 840 H210 Z M1350 765 H1710 V840 H1300 Z" fill={p.rule}/>
    <path d="M554 766 Q958 925 1350 765" fill="none" stroke={p.quiet} strokeWidth={3} strokeDasharray="8 9"/>
    <path d="M472 747 Q956 632 1446 741" fill="none" stroke={p.accent} strokeWidth={16} strokeDasharray="1020" strokeDashoffset={1020 * (1 - build)}/>
    <path d="M472 709 Q956 596 1446 703" fill="none" stroke={p.ink} strokeWidth={3} opacity={build}/>
    {Array.from({length: 19}, (_, i) => {
      const x = 490 + i * 52, y = 747 - Math.sin(i / 18 * Math.PI) * 55;
      return <path key={i} d={`M${x} ${y} v-34`} stroke={p.ink} strokeWidth={3} opacity={stage(t, .12 + i * .013, .27 + i * .013)}/>;
    })}
    <path d="M670 755 Q960 830 1250 753" fill="none" stroke={p.accent} strokeWidth={3} opacity={build}/>
    {[0, 1, 2, 3, 4, 5, 6].map(i => <path key={i} d={`M${670 + i * 97} ${755 + Math.sin(i / 6 * Math.PI) * 70} l54 -47 M${670 + i * 97} ${755 + Math.sin(i / 6 * Math.PI) * 70} l-39 -52`} fill="none" stroke={p.accent} strokeWidth={2} opacity={build * .75}/>)}
    <House x={310} y={595} p={p} scale={.63}/><Shop x={1550} y={560} p={p} scale={.75}/>
    <Person x={walkerX} y={walkerY} p={p} scale={.74} walk={Math.sin(move * Math.PI * 14)}/>
    <Bag x={walkerX + 28} y={walkerY + 67} p={p} scale={.4} opacity={stage(t, .81, .97)}/>
    <Shield x={960} y={430} p={p} scale={.82} opacity={stage(t, .1, .4)}/>
    <InkText x={960} y={310} p={p} size={25} color={p.quiet}>Điều kiện thay đổi trước khi quyết định chi thay đổi</InkText>
    {label('Thu nhập', 635, 543, p, 28)}{label('An sinh', 960, 570, p, 28)}{label('Niềm tin', 1255, 540, p, 28)}
  </g>;
};

const WarehouseBottleneck = ({t, p}: {t: number; p: PeoplePalette}) => {
  const gate = stage(t, .35, .7);
  return <g>
    <path d="M205 760 H1720" stroke={p.rule} strokeWidth={4}/>
    <path d="M235 728 V388 L586 288 L905 388 V728" fill={p.soft} stroke={p.ink} strokeWidth={3}/>
    <path d="M200 391 L586 270 L939 391" fill="none" stroke={p.ink} strokeWidth={7}/>
    <rect x={309} y={420} width={514} height={308} fill={p.paper} stroke={p.ink} strokeWidth={3}/>
    {[0, 1, 2].map(row => <g key={row}>
      <path d={`M326 ${500 + row * 86} H807`} stroke={p.ink} strokeWidth={6}/>
      {Array.from({length: 7}, (_, i) => <g key={i} opacity={stage(t, (row * 7 + i) * .009, .24 + (row * 7 + i) * .009)}><rect x={337 + i * 66} y={447 + row * 86} width={53} height={50} fill={i % 3 ? p.soft : p.accent} stroke={p.ink} strokeWidth={2}/><path d={`M${363 + i * 66} ${447 + row * 86} v18`} stroke={p.ink} strokeWidth={2}/></g>)}
    </g>)}
    <Shop x={1480} y={576} p={p} scale={.83} sign="NGƯỜI MUA"/>
    <path d="M947 645 H1303" stroke={p.rule} strokeWidth={45}/><path d="M947 645 H1303" stroke={p.paper} strokeWidth={3} strokeDasharray="16 16"/>
    <path d={`M1109 729 V${450 - gate * 8} M1109 ${476 - gate * 4} L${1206 - gate * 55} ${476 - gate * 4}`} fill="none" stroke={p.accent} strokeWidth={7}/>
    <path d="M1135 480 v128 M1163 480 v128 M1191 480 v128" stroke={p.accent} strokeWidth={6} opacity={1 - gate * .75}/>
    <Person x={1269} y={638} p={p} scale={.74}/>
    <rect x={1002 + gate * 40} y={610} width={61} height={58} fill={p.accent} stroke={p.ink} strokeWidth={3}/>
    <InkText x={584} y={806} p={p} size={30}>Thêm hàng trong kho</InkText>
    <InkText x={1399} y={806} p={p} size={30}>Cần đơn hàng và sức mua</InkText>
    <InkText x={1137} y={391} p={p} size={24} color={p.accent}>Điểm nghẽn chưa tự biến mất</InkText>
  </g>;
};

const PopulationGrid = ({t, p}: {t: number; p: PeoplePalette}) => <g>
  <g transform="translate(280 308)">
    {Array.from({length: 100}, (_, i) => {
      const highlight = i < 23, reveal = stage(t, i * .0015, .26 + i * .0015);
      return <g key={i} opacity={.1 + .9 * reveal}>
        <Person x={i % 20 * 49} y={Math.floor(i / 20) * 91} p={p} scale={.5} coat={highlight ? p.accent : p.quiet} elderly={highlight}/>
        {highlight ? <circle cx={i % 20 * 49} cy={Math.floor(i / 20) * 91 + 9} r={16} fill="none" stroke={p.accent} strokeWidth={2} opacity={stage(t, .25 + i * .004, .5 + i * .004)}/> : null}
      </g>;
    })}
  </g>
  <g transform={`translate(1430 ${glide(25, 0, stage(t, .18, .56))})`} opacity={stage(t, .18, .56)}>
    <InkText x={0} y={428} p={p} size={112} color={p.accent}>23%</InkText>
    {label('Từ 60 tuổi trở lên', 0, 486, p, 30)}
    <path d="M-164 535 H164" stroke={p.rule} strokeWidth={3}/>
    <InkText x={0} y={592} p={p} size={57}>77%</InkText>
    {label('Dưới 60 tuổi', 0, 638, p, 27)}
  </g>
  <InkText x={960} y={819} p={p} size={24} color={p.quiet}>100 hình người = 100 phần dân số · cơ cấu cuối năm 2025 theo NBS</InkText>
</g>;

const AgeThreshold = ({t, p}: {t: number; p: PeoplePalette}) => {
  const reveal = stage(t, .12, .4), shift = stage(t, .25, .46);
  return <g>
    <path d="M300 606 H1680 V662 H300 Z" fill={p.soft} stroke={p.ink} strokeWidth={3}/>
    {Array.from({length: 41}, (_, i) => {
      const x = 330 + i * 32.7;
      return <g key={i}><path d={`M${x} 606 v${i % 5 ? 17 : 34}`} stroke={p.ink} strokeWidth={i % 5 ? 1.5 : 3}/>{i % 5 === 0 ? <InkText x={x} y={700} p={p} size={24}>{40 + i}</InkText> : null}</g>;
    })}
    <path d="M984 600 V357" stroke={p.accent} strokeWidth={5}/><path d="M970 366 l14 -16 14 16" fill="none" stroke={p.accent} strokeWidth={5}/>
    <rect x={987} y={531} width={652 * reveal} height={69} fill={p.accent} opacity={.18}/>
    <g opacity={reveal}>
      <InkText x={1015} y={334} p={p} size={40} color={p.accent}>60+</InkText>
      <InkText x={1325} y={449} p={p} size={83} color={p.accent}>23%</InkText>
      <InkText x={1325} y={493} p={p} size={26}>cuối 2025 · NBS</InkText>
    </g>
    <g opacity={shift}><path d="M1147 606 V730" stroke={p.quiet} strokeWidth={3} strokeDasharray="7 7"/><InkText x={1168} y={778} p={p} size={38}>65+</InkText><path d="M1230 766 H1644" stroke={p.rule} strokeWidth={2}/><InkText x={1438} y={802} p={p} size={23} color={p.quiet}>Một nhóm tuổi khác</InkText></g>
    <Person x={504} y={438} scale={1.0} p={p}/><Person x={664} y={434} scale={1.03} p={p} elderly coat={p.quiet}/>
    <InkText x={595} y={347} p={p} size={29}>Giữ nguyên mốc tuổi</InkText>
    <InkText x={674} y={825} p={p} size={27} color={p.accent}>Đổi mốc tuổi → không được giữ lại 23%</InkText>
  </g>;
};

const LifeCourseRoom = ({t, p}: {t: number; p: PeoplePalette}) => {
  const active = stage(t, .12, .7);
  return <g>
    <path d="M205 765 H1715 M220 778 H1690" stroke={p.rule} strokeWidth={3}/>
    <path d="M230 739 V363 H808 V739 M808 363 H1661 V739" fill={p.soft} stroke={p.rule} strokeWidth={3}/>
    <path d="M808 363 V739" stroke={p.ink} strokeWidth={5}/>
    <path d="M278 535 H738 V651 H278 Z M289 650 V726 M715 651 V726" fill={p.paper} stroke={p.ink} strokeWidth={4}/>
    <path d="M313 515 Q468 450 650 521 L707 568 H327 Z" fill={p.rule} stroke={p.ink} strokeWidth={2}/>
    <Person x={440} y={458} scale={.7} p={p} elderly seated/>
    <Person x={693} y={542} scale={1.1} p={p} coat={p.quiet} arm={.9}/>
    <path d="M639 613 h-39 v43 h53 v-43" fill={p.paper} stroke={p.ink} strokeWidth={2}/>
    <path d="M624 627 v17 M616 635 h17" stroke={p.accent} strokeWidth={4}/>
    <Calendar x={1017} y={453} p={p} scale={.77} mark={active}/>
    <rect x={1355} y={545} width={73} height={111} rx={7} fill={p.rule} stroke={p.ink} strokeWidth={2}/>
    <Person x={1391} y={496} p={p} scale={1.03} seated arm={.55}/>
    <path d="M1280 592 H1610 V615 H1280 M1315 615 V738 M1574 615 V738" stroke={p.ink} strokeWidth={8} fill={p.paper}/>
    <path d="M1483 536 h88 l-10 56 h-102 Z" fill={p.quiet} stroke={p.ink} strokeWidth={2}/>
    <g opacity={stage(t, .46, .72)}><Person x={1125} y={619} p={p} scale={.78}/><Person x={1210} y={647} p={p} scale={.58} coat={p.quiet}/></g>
    {label(t < .52 ? 'Đời sống người cao tuổi' : 'Nhu cầu chăm sóc', 497, 811, p, 30)}{label('Lao động · chi tiêu · kế hoạch gia đình', 1283, 811, p, 27)}
    <path d="M987 653 h73 M1024 621 v64" stroke={p.accent} strokeWidth={8} strokeLinecap="round" opacity={active}/>
  </g>;
};

const TrainingStaircase = ({t, p}: {t: number; p: PeoplePalette}) => {
  const travel = stage(t, .08, .86), x = glide(383, 1410, travel);
  const stairIndex = Math.min(5, Math.max(0, Math.floor((x - 490) / 210) + 1));
  const stepY = 776 - stairIndex * 69;
  return <g>
    <path d="M250 807 H1674" stroke={p.rule} strokeWidth={3}/>
    <path d="M310 776 H490 V707 H700 V638 H910 V569 H1120 V500 H1330 V431 H1540 V776 Z" fill={p.soft} stroke={p.ink} strokeWidth={4}/>
    {[0, 1, 2, 3, 4].map(i => <g key={i} opacity={stage(t, i * .1, .2 + i * .1)}>
      <path d={`M${532 + i * 210} ${662 - i * 69} l30 -18 30 18 -30 18 Z`} fill={p.accent}/>
      <path d={`M${532 + i * 210} ${662 - i * 69} v27 l30 18 30 -18 v-27`} fill={p.rule} stroke={p.ink} strokeWidth={1.5}/>
    </g>)}
    <Person x={x} y={stepY - .87 * 131} p={p} scale={.87} walk={Math.sin(travel * Math.PI * 14)} arm={.3}/>
    <path d="M1288 333 L1348 295 L1410 332 L1348 372 Z M1310 349 V383 Q1348 408 1388 383 V349" fill={p.ink} stroke={p.paper} strokeWidth={2}/>
    <path d="M1410 332 v57" stroke={p.accent} strokeWidth={4}/>
    {label('Nền tảng', 407, 827, p, 26)}{label('Kỹ năng', 722, 827, p, 26)}{label('Ứng dụng', 1025, 827, p, 26)}{label('Thích nghi', 1375, 827, p, 26)}
    <InkText x={715} y={343} p={p} size={31}>Năng suất cần cả đào tạo và hỗ trợ</InkText>
    <InkText x={808} y={389} p={p} size={25} color={p.quiet}>Một quá trình nhiều năm, không phải doanh số một tháng</InkText>
    <path d="M356 756 Q913 465 1466 407" fill="none" stroke={p.accent} strokeWidth={2} strokeDasharray="8 10" opacity={.45}/>
  </g>;
};

const IncomeSecurityShop = ({t, p}: {t: number; p: PeoplePalette}) => {
  const paid = stage(t, .04, .3), confident = stage(t, .25, .5), spend = stage(t, .48, .85);
  return <g>
    <path d="M210 772 H1710" stroke={p.rule} strokeWidth={5}/>
    <House x={426} y={520} p={p} scale={1.25}/>
    <Shield x={743} y={438} p={p} scale={.95} opacity={confident}/>
    <Shop x={1475} y={584} p={p} scale={1.01} sign="HÀNG HÓA · DỊCH VỤ"/>
    <g transform={`translate(${glide(370, 580, paid)} ${glide(376, 548, paid) - Math.sin(paid * Math.PI) * 95})`} opacity={stage(t, 0, .12) * (1 - stage(t, .32, .45))}>
      <rect x={-53} y={-25} width={106} height={61} fill={p.accent} stroke={p.ink} strokeWidth={2}/><path d="M-53 -25 l53 36 53 -36" fill="none" stroke={p.paper} strokeWidth={3}/>
    </g>
    <path d="M545 744 Q941 732 1345 739" fill="none" stroke={p.rule} strokeWidth={39}/>
    <Person x={glide(562, 1314, spend)} y={623} p={p} scale={.91} walk={Math.sin(spend * Math.PI * 12)} arm={.25}/>
    <Bag x={glide(591, 1343, spend)} y={694} p={p} scale={.5} opacity={stage(t, .76, .94)}/>
    <g opacity={stage(t, .72, .96)}>
      {[0, 1, 2].map(i => <g key={i} transform={`translate(${1338 + i * 61} ${370 + i % 2 * 22}) rotate(${i % 2 ? 5 : -4})`}><path d="M0 0 h55 v78 l-7 -6 -7 6 -7 -6 -7 6 -7 -6 -7 6 -6 -6 Z" fill={p.paper} stroke={p.ink} strokeWidth={2}/><path d="M10 18 h32 M10 32 h24 M10 46 h32" stroke={p.quiet} strokeWidth={3}/></g>)}
    </g>
    <InkText x={414} y={330} p={p} size={29}>Thu nhập</InkText>
    <InkText x={897} y={585} p={p} size={28}>An tâm để quyết định chi</InkText>
    <InkText x={1480} y={332} p={p} size={29}>Đơn hàng thực tế</InkText>
    <InkText x={950} y={821} p={p} size={24} color={p.quiet}>Minh họa đường truyền; không khẳng định hiệu quả của một chính sách cụ thể</InkText>
  </g>;
};

/** Each ID owns a different object/action grammar; no donut/conveyor/ribbon fallback. */
export const PeopleScene = ({shot, frame, p}: PeopleProps) => {
  const t = Math.min(1, Math.max(0, frame / Math.max(1, shot.end - shot.start - 1)));
  const id = String(shot.id ?? 'people');
  const content = id === 'r05' ? <FamilyDecision t={t} p={p}/>
    : id === 'r07' ? <FinishOrExpand t={t} p={p}/>
    : id === 'h01' ? <PayrollTown t={t} p={p}/>
    : id === 'h02' ? <HouseholdConditions t={t} p={p}/>
    : id === 'h03' ? <AllocationJars t={t} p={p} id={id}/>
    : id === 'h05' ? <DifferentBaskets t={t} p={p}/>
    : id === 'h06' ? <ScopeBaskets t={t} p={p}/>
    : id === 'h07' ? <SupportBridge t={t} p={p}/>
    : id === 'h08' ? <WarehouseBottleneck t={t} p={p}/>
    : id === 'd01' ? <PopulationGrid t={t} p={p}/>
    : id === 'd02' ? <AgeThreshold t={t} p={p}/>
    : id === 'd03' ? <LifeCourseRoom t={t} p={p}/>
    : id === 'd06' ? <TrainingStaircase t={t} p={p}/>
    : id === 'p05' ? <IncomeSecurityShop t={t} p={p}/>
    : null;
  const contextPhoto = id === 'd03' ? shot.images?.[0] : null;
  const photoOpacity = stage(t, 0, .06) * (1 - stage(t, .3, .52));
  return <>
    <svg viewBox="0 0 1920 1080" width="100%" height="100%" style={{position: 'absolute', inset: 0, ...small}} aria-label={`${id} original illustrated scene`}>
      {content}
    </svg>
    {contextPhoto ? <div style={{position: 'absolute', left: 234, top: 368, width: 570, height: 372, overflow: 'hidden', opacity: photoOpacity, background: p.paper}}>
      <CanvasImage src={staticFile(contextPhoto.file)} style={{width: '100%', height: '100%', objectFit: 'cover', scale: 1.02 + t * .06}}/>
      <div style={{position: 'absolute', bottom: 0, left: 0, right: 0, padding: '12px 16px', background: 'rgba(15,28,22,.86)', color: '#fff3df', font: '24px Arial,sans-serif'}}>Người cao tuổi · Jingshan, Bắc Kinh</div>
    </div> : null}
  </>;
};

export const peopleSceneIds = ['r05', 'r07', 'h01', 'h02', 'h03', 'h05', 'h06', 'h07', 'h08', 'd01', 'd02', 'd03', 'd06', 'p05'];
