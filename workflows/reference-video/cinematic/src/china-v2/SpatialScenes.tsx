import type {ReactNode} from 'react';
import earth from '../china/geography/natural-earth-110m.json';

/** Purpose-built physical scenes. All amounts/objects here are illustrative, not measured data. */
type Palette = {paper:string;ink:string;accent:string;quiet:string;rule:string;soft:string};
type Props = {shot:any;frame:number;p:Palette};
const ease=(v:number)=>{const n=Math.min(1,Math.max(0,v));return n*n*(3-2*n);};
const stage=(t:number,a:number,b:number)=>ease((t-a)/(b-a));
const lerp=(a:number,b:number,t:number)=>a+(b-a)*t;
const face='#c59668';
const china=earth.features.find(f=>f.id==='CHN')!;
const chinaRings:number[][][]=china.geometry.type==='Polygon'?china.geometry.coordinates as number[][][]:(china.geometry.coordinates as number[][][][]).flat();
const outline=chinaRings.map(r=>r.map((pt,i)=>`${i?'L':'M'}${110+(pt[0]-73)/62*215},${414-(pt[1]-18)/36*128}`).join('')+'Z').join('');
const Text=({x,y,children,p,size=27,weight=500,anchor='middle',color}:{x:number;y:number;children:ReactNode;p:Palette;size?:number;weight?:number;anchor?:'middle'|'start'|'end';color?:string})=><text x={x} y={y} fill={color??p.ink} textAnchor={anchor} fontFamily="Bahnschrift,Arial,sans-serif" fontSize={size} fontWeight={weight}>{children}</text>;
const Box=({x,y,w,h,d=28,p,color,opacity=1}:{x:number;y:number;w:number;h:number;d?:number;p:Palette;color?:string;opacity?:number})=><g transform={`translate(${x} ${y})`} opacity={opacity}>
  <path d={`M0,${-h}L${d},${-h-d*.5}H${w+d}L${w},${-h}Z`} fill={p.paper} stroke={p.rule} strokeWidth={2}/>
  <path d={`M${w},${-h}L${w+d},${-h-d*.5}V${-d*.5}L${w},0Z`} fill={p.quiet} stroke={p.rule} strokeWidth={2}/>
  <path d={`M0,${-h}H${w}V0H0Z`} fill={color??p.soft} stroke={p.ink} strokeWidth={2}/>
</g>;
const Person=({x,y,p,scale=1,coat,arm=0}:{x:number;y:number;p:Palette;scale?:number;coat?:string;arm?:number})=><g transform={`translate(${x} ${y}) scale(${scale})`}>
  <circle cy={-62} r={16} fill={face}/><path d="M-14,-67Q0,-88 16,-67L13,-76Q0,-90 -12,-77Z" fill={p.ink}/>
  <path d="M-22,-36Q0,-52 22,-36L19,22H-18Z" fill={coat??p.accent}/>
  <path d="M-13,22L-18,76M13,22L23,76" stroke={p.ink} strokeWidth={13} strokeLinecap="round"/>
  <path d={`M-20,-31L${-37-arm*13},${6-arm*30}M20,-31L${44+arm*22},${-4-arm*26}`} fill="none" stroke={face} strokeWidth={10} strokeLinecap="round"/>
  <path d="M-26,81H-6M15,81H34" stroke={p.ink} strokeWidth={9} strokeLinecap="round"/>
</g>;
const Coin=({x,y,p,r=14,opacity=1}:{x:number;y:number;p:Palette;r?:number;opacity?:number})=><g opacity={opacity}><ellipse cx={x} cy={y+3} rx={r} ry={r*.82} fill={p.quiet}/><circle cx={x} cy={y} r={r} fill={p.accent} stroke={p.ink} strokeWidth={1.5}/><path d={`M${x-r*.35},${y}H${x+r*.35}M${x},${y-r*.35}V${y+r*.35}`} stroke={p.paper} strokeWidth={2}/></g>;
const Arrow=({path,p,opacity=1,color}:{path:string;p:Palette;opacity?:number;color?:string})=><g opacity={opacity}><path d={path} fill="none" stroke={color??p.accent} strokeWidth={3} markerEnd="url(#spatial-arrow)"/></g>;
const Platform=({p,x=250,y=780,w=1400}:{p:Palette;x?:number;y?:number;w?:number})=><g><path d={`M${x},${y}L${x+95},${y-65}H${x+w+95}L${x+w},${y}Z`} fill={p.soft} opacity={.6}/><path d={`M${x},${y}H${x+w}L${x+w},${y+13}H${x}Z`} fill={p.rule}/></g>;
const SmallFactory=({x,y,p,w=210,h=155,progress=1}:{x:number;y:number;p:Palette;w?:number;h?:number;progress?:number})=><g>
  <Box x={x} y={y} w={w} h={h} d={38} p={p}/>
  <path d={`M${x},${y-h}l${w*.25},-35v35l${w*.25},-35v35l${w*.25},-35v35h${w*.25}`} fill={p.soft} stroke={p.ink} strokeWidth={2}/>
  {[0,1,2,3].map(i=><rect key={i} x={x+18+i*(w-32)/4} y={y-h+35} width={(w-50)/5} height={29} fill={p.paper} stroke={p.rule} strokeWidth={1.5}/>)}
  <rect x={x+w*.37} y={y-63} width={w*.31} height={63} fill={p.ink}/><rect x={x+w*.38} y={y-60} width={w*.29} height={60*(1-progress)} fill={p.quiet}/>
</g>;
const Apartment=({x,y,p,floors=5,fill=1,w=145}:{x:number;y:number;p:Palette;floors?:number;fill?:number;w?:number})=><g>
  <Box x={x} y={y} w={w} h={floors*43+22} d={30} p={p}/>
  {Array.from({length:floors},(_,row)=><g key={row}>{[0,1,2].map(col=><rect key={col} x={x+15+col*(w-25)/3} y={y-38-row*43} width={(w-50)/3} height={25} fill={row<Math.ceil(floors*fill)?p.paper:p.quiet} opacity={row<Math.ceil(floors*fill)?1:.45}/>)}</g>)}
</g>;
const Road=({p,y=720}:{p:Palette;y?:number})=><g><path d={`M150,${y}H1770L1707,${y+72}H87Z`} fill={p.rule}/><path d={`M140,${y+35}H1710`} stroke={p.paper} strokeWidth={4} strokeDasharray="29 26"/></g>;
const Truck=({x,y,p,loaded=true}:{x:number;y:number;p:Palette;loaded?:boolean})=><g transform={`translate(${x} ${y})`}>
  <rect x={-51} y={-47} width={100} height={44} fill={loaded?p.accent:p.soft} stroke={p.ink} strokeWidth={2}/><path d="M49,-35H82L103,-13V0H49Z" fill={p.paper} stroke={p.ink} strokeWidth={2}/><path d="M61,-29H78L92,-15H61Z" fill={p.quiet}/><path d="M-55,0H106" stroke={p.ink} strokeWidth={5}/><circle cx={-28} cy={5} r={13} fill={p.ink}/><circle cx={78} cy={5} r={13} fill={p.ink}/><circle cx={-28} cy={5} r={5} fill={p.paper}/><circle cx={78} cy={5} r={5} fill={p.paper}/>
</g>;

const PortHome=({t,p}:{t:number;p:Palette})=>{
 const train=stage(t,.12,.65),home=stage(t,.18,.42),load=stage(t,.08,.38);
 return <g>
   <path d="M120 635H1150V805H120Z" fill={p.soft}/><path d="M120 647H1150M140 689H1118M174 735H1088M145 778H1118" stroke={p.quiet} strokeWidth={2} opacity={.55}/>
   <path d="M165 560H883L827 638H260Z" fill={p.ink}/><path d="M208 576H850" stroke={p.accent} strokeWidth={8}/><path d="M257 548V462H354V548" fill={p.paper} stroke={p.ink} strokeWidth={3}/><rect x={277} y={479} width={50} height={25} fill={p.quiet}/><path d="M280 458V415H308V458" fill={p.ink}/>
   {[0,1,2,3,4].map(i=><g key={i}><rect x={377+i*86} y={507} width={79} height={49} fill={i%2?p.soft:p.accent} stroke={p.paper} strokeWidth={2}/>{[1,2,3,4].map(j=><path key={j} d={`M${377+i*86+j*15},514V548`} stroke={p.ink} strokeWidth={1} opacity={.45}/>)}</g>)}
   <g transform={`translate(0 ${lerp(-40,0,load)})`}><rect x={480} y={452} width={79} height={49} fill={p.accent} stroke={p.paper} strokeWidth={2}/><path d="M480 452L519 430L559 452M519 430V373" fill="none" stroke={p.quiet} strokeWidth={3}/></g>
   <path d="M780 603V305H855V603M789 323H1068L1049 345H792M819 307L1049 323M885 345V447" fill="none" stroke={p.accent} strokeWidth={10}/><path d="M820 348V584M799 404H844M799 470H844M799 536H844" fill="none" stroke={p.paper} strokeWidth={2}/><path d="M875 447Q885 471 897 447" fill="none" stroke={p.ink} strokeWidth={4}/>
   <path d="M118 807H1098M138 824H1118" stroke={p.quiet} strokeWidth={5}/>
   <g transform={`translate(${lerp(-130,60,train)} 0)`}>{[0,1,2].map(i=><g key={i}><rect x={190+i*227} y={746} width={211} height={54} fill={i===0?p.accent:p.rule} stroke={p.ink} strokeWidth={2}/><path d={`M${190+i*227},772H${401+i*227}`} stroke={p.paper} strokeWidth={2}/><circle cx={222+i*227} cy={804} r={10} fill={p.ink}/><circle cx={369+i*227} cy={804} r={10} fill={p.ink}/></g>)}</g>
   <path d="M1185 283V834" stroke={p.rule} strokeWidth={2}/>
   <g opacity={home} transform={`translate(${(1-home)*60} 0)`}>
    <path d="M1273 450L1460 320L1694 450V768H1273Z" fill={p.soft} stroke={p.quiet} strokeWidth={3}/><path d="M1258 454L1460 311L1710 454" fill="none" stroke={p.accent} strokeWidth={7}/><rect x={1320} y={458} width={130} height={99} fill={p.paper} stroke={p.ink} strokeWidth={3}/><path d="M1385 458V557M1320 507H1450" stroke={p.rule} strokeWidth={3}/>
    <path d="M1360 672H1650M1386 672V756M1617 672V756" stroke={p.ink} strokeWidth={10}/><path d="M1432 639L1595 628L1621 668H1420Z" fill={p.paper} stroke={p.ink} strokeWidth={2}/><path d="M1480 638H1559M1477 651H1522" stroke={p.quiet} strokeWidth={3}/>
    <Person x={1356} y={625} scale={.9} p={p} arm={.5}/><Person x={1639} y={625} scale={.86} p={p} coat={p.quiet} arm={.1}/><Coin x={1514} y={626} p={p} r={15}/>
   </g>
   <Text x={590} y={311} p={p} size={24} color={p.quiet}>Hàng hóa tiếp tục di chuyển</Text><Text x={1481} y={818} p={p} size={27} color={p.accent}>Gia đình cân nhắc từng khoản chi</Text>
 </g>;
};

const RegionalCity=({t,p}:{t:number;p:Palette})=>{
 const expand=stage(t,.05,.45),ship=stage(t,.40,.88);
 return <g transform={`translate(${lerp(12,-9,t)} 0)`}>
  <path d={outline} fill={p.soft} stroke={p.quiet} strokeWidth={1.5}/><Text x={222} y={449} p={p} size={19} color={p.quiet}>Trung Quốc · Natural Earth</Text>
  <Platform p={p} x={210} y={738} w={1430}/><Road p={p} y={695}/>
  <Apartment x={265} y={669} p={p} floors={4} w={110}/><Apartment x={400} y={662} p={p} floors={6} w={120}/>
  <g opacity={expand}><SmallFactory x={645} y={650} w={290} h={172} p={p}/><path d="M950 650V374H999V627" fill={p.soft} stroke={p.ink} strokeWidth={3}/><path d="M957 416H992M957 459H992M957 502H992" stroke={p.rule} strokeWidth={3}/></g>
  <g opacity={stage(t,.2,.55)}><Box x={1110} y={651} w={245} h={93} d={75} p={p}/><path d="M1110 558L1230 506L1355 558" fill={p.paper} stroke={p.ink} strokeWidth={3}/><path d="M1155 651V595H1220V651M1245 651V595H1310V651" fill={p.ink}/></g>
  <g opacity={stage(t,.35,.62)}><path d="M1455 652V427H1516V652M1480 427H1705M1630 427V579" fill="none" stroke={p.accent} strokeWidth={9}/><path d="M1461 464H1508M1461 512H1508M1461 560H1508" stroke={p.ink} strokeWidth={2}/><rect x={1571} y={595} width={149} height={56} fill={p.ink}/><path d="M1571 613H1720M1604 595V651M1640 595V651M1677 595V651" stroke={p.paper} strokeWidth={2}/></g>
  <Truck x={lerp(500,1390,ship)} y={734} p={p}/>
  <Text x={404} y={369} p={p} size={27}>Thành phố</Text><Text x={800} y={397} p={p} size={27}>Cụm sản xuất</Text><Text x={1222} y={466} p={p} size={27}>Kho &amp; logistics</Text><Text x={1570} y={368} p={p} size={27}>Cảng</Text>
  <path d="M350 806H1640" stroke={p.rule} strokeWidth={2}/><Text x={960} y={839} p={p} size={23} color={p.quiet}>Đô thị minh họa kết nối hạ tầng — không phải bản đồ tỷ lệ</Text>
 </g>;
};

const ExplodedAssembly=({t,p}:{t:number;p:Palette})=>{
 const assemble=stage(t,.16,.58),check=stage(t,.64,.9), lift=Math.sin(assemble*Math.PI)*35;
 return <g>
  <path d="M355 715L476 640H1430L1560 715L1440 767H480Z" fill={p.rule}/><path d="M480 767V813M1439 767V813" stroke={p.ink} strokeWidth={9}/>
  <ellipse cx={960} cy={671} rx={335} ry={65} fill={p.quiet} opacity={.15}/>
  <g transform={`translate(${lerp(280,0,assemble)} ${lerp(28,0,assemble)-lift})`}><path d="M513 542L700 491H1114L1316 544L1124 600H703Z" fill={p.soft} stroke={p.ink} strokeWidth={3}/><path d="M513 542V591L703 648H1124L1316 591V544L1124 600H703Z" fill={p.paper} stroke={p.ink} strokeWidth={3}/><path d="M704 600V648M1124 600V648" stroke={p.rule} strokeWidth={3}/></g>
  <g transform={`translate(${lerp(-260,0,assemble)} ${lerp(-115,-10,assemble)-lift})`}><path d="M682 526L809 491H1051L1176 526L1051 565H809Z" fill={p.accent} stroke={p.ink} strokeWidth={3}/><path d="M682 526V549L809 590H1051L1176 549V526L1051 565H809Z" fill={p.quiet} stroke={p.ink} strokeWidth={2}/>{Array.from({length:7},(_,i)=><path key={i} d={`M${792+i*36} 506V548`} stroke={p.paper} strokeWidth={4}/>)}</g>
  <g transform={`translate(0 ${lerp(-214,-27,assemble)-lift})`}><path d="M551 542L716 492H1110L1287 544L1110 599H716Z" fill={p.ink} stroke={p.accent} strokeWidth={3}/><path d="M585 541L727 506H1098L1248 544L1098 581H727Z" fill={p.paper}/><path d="M759 530H1120M726 552H1085" stroke={p.rule} strokeWidth={3}/></g>
  <g opacity={1-assemble*.45}><Text x={403} y={388} p={p} size={27}>Vỏ</Text><Text x={1280} y={355} p={p} size={27}>Linh kiện</Text><Text x={961} y={292} p={p} size={27}>Lắp ráp</Text><path d="M430 400L575 475M1260 366L1160 425M960 304V340" stroke={p.quiet} strokeWidth={2}/></g>
  <g opacity={check}><circle cx={1455} cy={413} r={78} fill={p.paper} stroke={p.accent} strokeWidth={5}/><path d="M1420 413L1446 440L1495 385" fill="none" stroke={p.accent} strokeWidth={9} strokeLinecap="round"/><Text x={1455} y={538} p={p} size={28}>Kiểm tra</Text></g>
  <rect x={1500} y={619} width={116} height={87} rx={6} fill={p.ink}/><path d="M1523 644H1591M1523 659H1567M1523 676H1582" stroke={p.paper} strokeWidth={3}/>
  <Person x={338} y={598} p={p} scale={1.1} arm={assemble*.7}/><Text x={960} y={816} p={p} size={26} color={p.quiet}>Linh kiện → phối hợp → sản phẩm đạt kiểm tra</Text>
 </g>;
};

const IndustrialCluster=({t,p}:{t:number;p:Palette})=>{
 const connect=stage(t,.16,.63),repair=stage(t,.62,.9);
 return <g>
  <Platform p={p} x={250} y={751} w={1360}/><path d="M353 685L1052 421L1662 660M1039 760L522 425" fill="none" stroke={p.rule} strokeWidth={39}/><path d="M353 685L1052 421L1662 660M1039 760L522 425" fill="none" stroke={p.paper} strokeWidth={3} strokeDasharray="20 16"/>
  <SmallFactory x={716} y={626} p={p} w={331} h={178}/><Text x={900} y={373} p={p} size={30} weight={700}>Xưởng lắp ráp</Text>
  <g opacity={stage(t,.03,.24)}><Box x={280} y={603} w={203} h={110} d={45} p={p}/><path d="M280 493L381 453L483 493" fill={p.paper} stroke={p.ink} strokeWidth={2}/><Text x={379} y={662} p={p} size={27}>Nhà cung cấp</Text><path d="M318 548H451M318 569H425" stroke={p.accent} strokeWidth={6}/></g>
  <g opacity={stage(t,.12,.36)}><Box x={1234} y={521} w={242} h={113} d={35} p={p}/><path d="M1261 435H1449M1261 456H1449M1261 477H1408" stroke={p.accent} strokeWidth={6}/><Text x={1374} y={359} p={p} size={27}>Đào tạo kỹ năng</Text></g>
  <g opacity={stage(t,.25,.49)}><Box x={1262} y={762} w={253} h={107} d={42} p={p}/><path d="M1341 684L1372 714L1428 673M1322 730H1456" fill="none" stroke={p.accent} strokeWidth={7}/><Text x={1401} y={821} p={p} size={27}>Dịch vụ sửa chữa</Text></g>
  <g opacity={connect}><Truck x={lerp(530,663,connect)} y={674-20*connect} p={p}/><Person x={1160} y={461} p={p} scale={.63} coat={p.quiet}/><Person x={1138} y={488} p={p} scale={.63}/></g>
  <g opacity={repair}><path d="M1075 588L1200 699" stroke={p.accent} strokeWidth={4} strokeDasharray="9 8"/><path d="M1187 660L1224 696L1207 717L1172 680Z" fill={p.ink}/><circle cx={1184} cy={673} r={17} fill={p.paper} stroke={p.ink} strokeWidth={6}/></g>
  <Text x={386} y={793} p={p} size={23} color={p.quiet}>Đầu vào gần hơn</Text><Text x={914} y={829} p={p} size={24} color={p.quiet}>Khoảng cách, kỹ năng và dịch vụ cùng tạo lợi thế</Text>
 </g>;
};

const WarehouseOrders=({t,p}:{t:number;p:Palette})=>{
 const orders=stage(t,.12,.42),pickup=stage(t,.48,.85);
 return <g>
  <path d="M197 762H1725" stroke={p.rule} strokeWidth={4}/>
  <path d="M260 339V755M895 339V755M250 486H905M250 663H905" fill="none" stroke={p.ink} strokeWidth={12}/>
  {Array.from({length:8},(_,i)=>{const row=Math.floor(i/4),col=i%4;const taken=i<5?stage(t,.44+i*.035,.66+i*.035):0;return <g key={i} transform={`translate(${taken*210} ${taken*30})`} opacity={1-taken*.85}>
    <Box x={285+col*151} y={row?651:474} w={112} h={91} d={15} p={p} color={i<5?p.accent:p.soft}/><path d={`M${340+col*151} ${row?560:383}V${row?651:474}`} stroke={p.paper} strokeWidth={3}/>
   </g>;})}
  <Text x={579} y={300} p={p} size={31} weight={700}>8 vị trí công suất</Text>
  <g opacity={orders}><path d="M1125 335H1453V618H1125Z" fill={p.paper} stroke={p.ink} strokeWidth={3}/><rect x={1225} y={321} width={127} height={31} rx={8} fill={p.ink}/><Text x={1290} y={402} p={p} size={29} weight={700}>5 đơn hàng</Text>{Array.from({length:5},(_,i)=><g key={i}><rect x={1156} y={430+i*32} width={17} height={17} fill={i/5<pickup?p.accent:p.rule}/><path d={`M1191 ${438+i*32}H${1360+i%2*46}`} stroke={p.quiet} strokeWidth={3}/></g>)}</g>
  <Truck x={lerp(1002,1460,pickup)} y={731} p={p}/>
  <g opacity={stage(t,.75,.92)}><path d="M336 370H803" stroke={p.quiet} strokeWidth={3} strokeDasharray="9 9"/><Text x={590} y={818} p={p} size={27} color={p.accent}>Công suất trống không tự tạo doanh thu</Text></g>
  <Text x={1541} y={352} p={p} size={22} color={p.quiet}>Số giả định</Text>
 </g>;
};

const HousingRoles=({t,p}:{t:number;p:Palette})=>{
 const reveal=stage(t,.10,.47),money=stage(t,.47,.81);
 return <g>
  <Platform p={p} x={620} y={760} w={640}/><Apartment x={778} y={734} w={258} floors={7} fill={.6} p={p}/>
  <path d="M778 434H1036M864 412V735M950 412V735" stroke={p.paper} strokeWidth={6}/>
  <g><path d="M182 603L323 506L465 603V741H182Z" fill={p.soft} stroke={p.ink} strokeWidth={3}/><Person x={270} y={658} p={p} scale={.76}/><Person x={364} y={662} p={p} scale={.72} coat={p.quiet}/><Text x={323} y={796} p={p} size={28}>Người mua</Text></g>
  <g opacity={reveal}><path d="M1392 407H1687L1539 329Z" fill={p.accent} stroke={p.ink} strokeWidth={2}/><path d="M1390 416H1689V436H1390ZM1380 598H1700V625H1380Z" fill={p.ink}/>{[0,1,2,3].map(i=><rect key={i} x={1410+i*73} y={436} width={31} height={162} fill={p.paper} stroke={p.ink} strokeWidth={2}/>)}<Text x={1540} y={676} p={p} size={27}>Ngân hàng</Text></g>
  <g opacity={stage(t,.20,.55)}><Truck x={1420} y={790} p={p}/><Person x={1650} y={718} p={p} scale={.71}/><path d="M1627 659Q1650 637 1673 659H1627Z" fill={p.accent} stroke={p.ink} strokeWidth={2}/><Text x={1517} y={843} p={p} size={27}>Nhà thầu &amp; vật liệu</Text></g>
  <g opacity={stage(t,.27,.58)}><Box x={337} y={437} w={146} h={102} d={24} p={p}/><path d="M334 333L409 296L484 333" fill={p.paper} stroke={p.ink} strokeWidth={2}/><Text x={410} y={283} p={p} size={25}>Địa phương</Text></g>
  <g opacity={money}><Arrow path="M487 643Q648 624 758 600" p={p}/><Arrow path="M1359 501Q1204 481 1067 510" p={p}/><Arrow path="M1082 646Q1220 709 1334 740" p={p}/><Arrow path="M756 476Q595 366 504 387" p={p}/></g>
  {Array.from({length:4},(_,i)=>{const m=stage(t,.47+i*.04,.65+i*.04);return <Coin key={i} x={lerp(521,727,m)} y={lerp(634,601,m)} r={12} p={p} opacity={money}/>;})}
  <Text x={927} y={801} p={p} size={28} weight={700}>Dự án &amp; chủ đầu tư</Text>
 </g>;
};

const EscrowTimeline=({t,p}:{t:number;p:Palette})=>{
 const sent=stage(t,.08,.32),held=stage(t,.32,.55),wait=stage(t,.55,.85);
 return <g>
  <path d="M200 782H1730" stroke={p.rule} strokeWidth={4}/>
  <Person x={291} y={588} p={p} scale={1.25} arm={.8*sent}/><Text x={291} y={745} p={p} size={28}>Người mua</Text>
  <g transform="translate(640 522)"><path d="M-145-106H145V150H-145Z" fill={p.soft} stroke={p.ink} strokeWidth={3}/><rect x={-116} y={-58} width={232} height={169} rx={4} fill={p.paper} stroke={p.ink} strokeWidth={2}/><circle r={53} cy={28} fill={p.rule} stroke={p.ink} strokeWidth={3}/><path d="M-28 28H28M0 0V56" stroke={p.ink} strokeWidth={4}/><Text x={0} y={-77} p={p} size={27}>Tài khoản dự án</Text></g>
  {Array.from({length:6},(_,i)=>{const m=stage(t,.09+i*.018,.27+i*.018);return <Coin key={i} x={lerp(363,567+i%3*44,m)} y={lerp(551,490+Math.floor(i/3)*39,m)-Math.sin(m*Math.PI)*75} p={p} r={14}/>;})}
  <g opacity={held}><rect x={515} y={344} width={250} height={50} rx={4} fill={p.ink}/><Text x={640} y={378} p={p} color={p.paper} size={25}>Tiền thu chậm lại</Text></g>
  <g transform="translate(1110 653)"><path d="M-131 0H122M-100 0V-244M0 0V-244M100 0V-244M-100-184H100M-100-119H100M-100-54H100" stroke={p.ink} strokeWidth={8} fill="none"/><path d="M-100-184H0V-119H-100Z" fill={p.soft}/><path d="M0-184H100V-119H0Z" fill={p.accent} opacity={1-held*.6}/><Text x={0} y={85} p={p} size={28}>Lịch xây dựng</Text></g>
  <g opacity={wait}><path d="M1359 434H1666V650H1359Z" fill={p.paper} stroke={p.ink} strokeWidth={3}/><path d="M1359 481H1666" stroke={p.accent} strokeWidth={9}/>{[0,1,2].map(i=><path key={i} d={`M1390 ${522+i*39}H1630`} stroke={p.rule} strokeWidth={3}/>)}<circle cx={1592} cy={631} r={47} fill={p.soft} stroke={p.ink} strokeWidth={3}/><path d="M1592 600V631L1615 645" stroke={p.ink} strokeWidth={4} fill="none"/><Text x={1513} y={738} p={p} size={28}>Nhà thầu chờ tiền</Text></g>
  <path d="M816 533H949M1265 533H1332" stroke={p.quiet} strokeWidth={3} strokeDasharray="8 9"/>
  <g opacity={wait}><path d="M873 495V565M899 495V565" stroke={p.accent} strokeWidth={9}/><Text x={960} y={829} p={p} size={25} color={p.quiet}>Dòng tiền chậm → xem lại lịch thanh toán và tiến độ</Text></g>
 </g>;
};

const ConstructionProgress=({t,p}:{t:number;p:Palette})=>{
 const pause=stage(t,.24,.48),concern=stage(t,.48,.75);
 const floors=2+Math.min(3,Math.floor(stage(t,.02,.32)*3));
 return <g>
  <Platform p={p} x={265} y={783} w={1340}/>
  <path d="M735 732V322M885 732V322M1035 732V322M1185 732V322" fill="none" stroke={p.ink} strokeWidth={12}/>
  {[0,1,2,3,4].map(i=><g key={i}><path d={`M728 ${732-i*79}H1211L1264 ${706-i*79}`} fill="none" stroke={p.ink} strokeWidth={8}/><path d={`M736 ${727-i*79}H1184V${665-i*79}H736Z`} fill={i<floors?p.soft:'transparent'} stroke={p.rule} strokeWidth={2}/>{[0,1,2].map(j=><rect key={j} x={764+j*144} y={682-i*79} width={86} height={31} fill={i<floors?p.paper:'transparent'} stroke={p.rule} strokeWidth={2}/>)}</g>)}
  <path d="M1310 758V275H1360V758M1333 273H1628L1607 296H1333M1569 296V451" fill="none" stroke={p.accent} strokeWidth={9}/><g transform={`translate(0 ${lerp(-55,0,pause)})`}><path d="M1534 451H1606V488H1534Z" fill={p.rule} stroke={p.ink} strokeWidth={3}/><path d="M1569 419V451" stroke={p.ink} strokeWidth={3}/></g>
  <g opacity={pause}><path d="M1429 543V619M1460 543V619" stroke={p.ink} strokeWidth={13}/><Text x={1443} y={666} p={p} size={26}>Tiến độ chậm</Text></g>
  <Person x={405} y={633} p={p} scale={1.35}/><Person x={548} y={663} p={p} scale={1.02} coat={p.quiet}/>
  <g opacity={concern}><path d="M308 387Q308 344 355 344H576Q614 344 614 387V472Q614 510 575 510H424L385 547V510H349Q308 510 308 472Z" fill={p.paper} stroke={p.accent} strokeWidth={3}/><path d="M435 380Q458 354 484 379Q508 409 469 429V448" fill="none" stroke={p.accent} strokeWidth={7} strokeLinecap="round"/><circle cx={469} cy={475} r={5} fill={p.accent}/></g>
  <Text x={467} y={811} p={p} size={27}>Lo về ngày nhận nhà</Text><Text x={1052} y={835} p={p} size={23} color={p.quiet}>Tiến độ minh họa — không mô tả một dự án thực</Text>
 </g>;
};

const Workbench=({t,p}:{t:number;p:Palette})=>{
 const learn=stage(t,.1,.38),tool=stage(t,.35,.63),process=stage(t,.61,.88);
 return <g>
  <path d="M224 680L361 604H1539L1660 680L1518 756H347Z" fill={p.soft} stroke={p.ink} strokeWidth={3}/><path d="M349 754V829M1516 754V829" stroke={p.ink} strokeWidth={13}/>
  <Person x={419} y={537} p={p} scale={1.6} arm={.8*learn}/>
  <g opacity={learn} transform={`translate(0 ${30*(1-learn)})`}><path d="M590 406L734 383L881 406V538L734 516L590 538Z" fill={p.paper} stroke={p.ink} strokeWidth={3}/><path d="M734 389V511M614 430L704 417M614 455L704 442M759 418L851 432M759 446L851 460" stroke={p.quiet} strokeWidth={3}/><Text x={734} y={343} p={p} size={29} weight={700}>Kỹ năng</Text></g>
  <g opacity={tool} transform={`translate(${lerp(85,0,tool)} 0)`}><path d="M1042 605V441H1167V605" fill={p.ink} stroke={p.rule} strokeWidth={2}/><path d="M1104 440L1209 388L1264 490L1155 535" fill="none" stroke={p.accent} strokeWidth={24} strokeLinejoin="round"/><circle cx={1208} cy={391} r={17} fill={p.paper} stroke={p.ink} strokeWidth={3}/><path d="M1264 489L1300 516L1291 549M1264 489L1231 532L1255 555" fill="none" stroke={p.ink} strokeWidth={7}/><Text x={1150} y={323} p={p} size={29} weight={700}>Công cụ</Text></g>
  <g opacity={process}><path d="M1437 359H1684V554H1437Z" fill={p.paper} stroke={p.ink} strokeWidth={3}/>{[0,1,2].map(i=><g key={i}><circle cx={1470} cy={404+i*55} r={12} fill={p.accent}/><path d={`M1500 ${404+i*55}H1646`} stroke={p.quiet} strokeWidth={3}/></g>)}<Text x={1558} y={305} p={p} size={29} weight={700}>Quy trình</Text></g>
  {[0,1,2,3,4].map(i=><g key={i} opacity={i<2?1:stage(t,.64+(i-2)*.065,.78+(i-2)*.065)} transform={`translate(${710+i*145} ${649+(i%2)*17})`}><path d="M-34-34L10-52L57-32L12-12Z" fill={p.paper} stroke={p.ink} strokeWidth={2}/><path d="M-34-34V12L12 33V-12Z" fill={p.accent} stroke={p.ink} strokeWidth={2}/><path d="M12-12L57-32V12L12 33Z" fill={p.rule} stroke={p.ink} strokeWidth={2}/></g>)}
  <Text x={960} y={822} p={p} size={25} color={p.quiet}>Cùng con người, thêm kỹ năng — công cụ — phối hợp</Text>
 </g>;
};

const ProjectAlternatives=({t,p}:{t:number;p:Palette})=>{
 const demand=stage(t,.16,.47),choice=stage(t,.5,.85);
 return <g>
  <path d="M960 289V824" stroke={p.rule} strokeWidth={3} strokeDasharray="6 11"/>
  <Platform p={p} x={215} y={745} w={607}/><Platform p={p} x={1100} y={745} w={607}/>
  <SmallFactory x={320} y={697} w={334} h={190} p={p} progress={.5}/>
  <g opacity={.7-choice*.3}><SmallFactory x={1200} y={697} w={334} h={190} p={p}/><path d="M1242 566L1492 669M1242 669L1492 566" stroke={p.quiet} strokeWidth={4} opacity={.4}/></g>
  <g opacity={demand}><Truck x={lerp(780,620,demand)} y={735} p={p}/><Person x={288} y={705} p={p} scale={.75}/><Person x={785} y={705} p={p} scale={.75} coat={p.quiet}/></g>
  <Text x={555} y={324} p={p} size={30} weight={700}>Công suất có người mua</Text><Text x={1405} y={324} p={p} size={30} weight={700}>Xây thêm, cầu chưa tới</Text>
  <g opacity={choice}><path d="M468 414L520 460L609 368" fill="none" stroke={p.accent} strokeWidth={10} strokeLinecap="round"/><path d="M1376 377V432M1408 377V432" stroke={p.quiet} strokeWidth={12}/></g>
  <Text x={548} y={814} p={p} size={25} color={p.accent}>Hiệu quả &amp; thu nhập lâu dài?</Text><Text x={1402} y={814} p={p} size={25} color={p.quiet}>Nghĩa vụ xử lý về sau?</Text>
 </g>;
};

/** Content only: the composition owns headers, notes, sound and captions. */
export const SpatialScene=({shot,frame,p}:Props)=>{
 const t=Math.min(1,Math.max(0,frame/Math.max(1,shot.end-shot.start-1)));
 const scenes:Record<string,ReactNode>={
  o01:<PortHome t={t} p={p}/>,f01:<RegionalCity t={t} p={p}/>,f02:<ExplodedAssembly t={t} p={p}/>,f03:<IndustrialCluster t={t} p={p}/>,f04:<WarehouseOrders t={t} p={p}/>,
  r01:<HousingRoles t={t} p={p}/>,r02:<EscrowTimeline t={t} p={p}/>,r03:<ConstructionProgress t={t} p={p}/>,d04:<Workbench t={t} p={p}/>,p04:<ProjectAlternatives t={t} p={p}/>,
 };
 if(!scenes[shot.id])throw new Error(`Unauthored spatial shot: ${shot.id}`);
 return <svg viewBox="0 0 1920 1080" width={1920} height={1080} style={{position:'absolute',inset:0}}>
  <defs><marker id="spatial-arrow" viewBox="0 0 10 10" refX={9} refY={5} markerWidth={7} markerHeight={7} orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill={p.accent}/></marker></defs>
  {scenes[shot.id]}
 </svg>;
};
