import React from 'react';
import {AbsoluteFill, Sequence, staticFile, interpolate} from 'remotion';
import {Media, font} from '../business/Shared';
import earth from '../china/geography/natural-earth-110m.json';

const clamp={extrapolateLeft:'clamp',extrapolateRight:'clamp'} as const;
const enter=(f:number,a=0,n=24)=>interpolate(f,[a,a+n],[0,1],{...clamp,easing:t=>1-(1-t)**3});
const Text=({x,y,children,p,size=30,anchor='start',weight=500}:any)=><text x={x} y={y} fill={p.ink} fontFamily={font} fontSize={size} textAnchor={anchor} fontWeight={weight}>{children}</text>;
const Caption=({x,y,children,p,size=24}:any)=><text x={x} y={y} fill={p.quiet} fontFamily="Arial,sans-serif" fontSize={size}>{children}</text>;
const Coin=({x,y,p,scale=1}:any)=><g transform={`translate(${x} ${y}) scale(${scale})`}><ellipse cy={6} rx={19} ry={8} fill={p.ink} opacity={.18}/><circle r={18} fill={p.accent}/><circle r={12} fill="none" stroke={p.paper} strokeWidth={1.7}/></g>;
const House=({x,y,p,w=180,h=190,lit=false}:any)=><g transform={`translate(${x} ${y})`}><path d={`M0 0 L${w*.5} -55 L${w} 0V${h}H0Z`} fill={p.soft} stroke={p.ink} strokeWidth={2}/><path d={`M${w} 0l35 -22v${h}l-35 22Z`} fill={p.rule}/><path d={`M${w*.5} -55l35 -22 ${w*.5} 55 -35 22Z`} fill={p.accent}/>{[0,1,2].map(i=><g key={i}>{[0,1].map(j=><rect key={j} x={25+j*(w-70)} y={25+i*43} width={24} height={25} fill={lit?p.accent:p.paper}/>)}</g>)}<rect x={w*.43} y={h-44} width={30} height={44} fill={p.ink}/></g>;
const Gear=({x,y,p,r=75,angle=0}:any)=><g transform={`translate(${x} ${y}) rotate(${angle})`}>{Array.from({length:12},(_,i)=><rect key={i} x={-14} y={-r-12} width={28} height={40} fill={p.accent} transform={`rotate(${i*30})`}/>)}<circle r={r} fill={p.soft} stroke={p.accent} strokeWidth={13}/><circle r={r*.35} fill={p.paper} stroke={p.ink} strokeWidth={4}/></g>;
const Person=({x,y,p,scale=1}:any)=><g transform={`translate(${x} ${y}) scale(${scale})`}><circle cy={-39} r={16} fill={p.ink}/><path d="M-22 -16Q0 -30 22 -16L18 38H9L7 80H-7L-9 38H-18Z" fill={p.accent}/></g>;

const Page=({x,y,p,title,sub,rotate=0,opacity=1}:any)=><g opacity={opacity} transform={`translate(${x} ${y}) rotate(${rotate})`}><rect x={9} y={12} width={370} height={375} rx={5} fill={p.ink} opacity={.12}/><rect width={370} height={375} rx={5} fill={p.paper} stroke={p.rule} strokeWidth={2}/><rect x={28} y={35} width={65} height={8} fill={p.accent}/><Text x={28} y={92} p={p} size={29} weight={700}>{title}</Text><Caption x={28} y={127} p={p} size={20}>{sub}</Caption>{[0,1,2,3,4,5].map(i=><rect key={i} x={28} y={173+i*25} width={i%2?246:295} height={5} fill={p.rule}/>)}<rect x={25} y={235} width={305} height={22} fill={p.accent} opacity={.16}/></g>;

const Atlas:React.FC<any>=({shot,frame,p})=>{
 const t=enter(frame,10,120),dy=interpolate(frame,[0,shot.end-shot.start],[12,-10],clamp);
 const rings=(f:any):number[][][]=>f.geometry.type==='Polygon'?f.geometry.coordinates:f.geometry.coordinates.flat();
 const project=(lo:number,la:number)=>[170+(lo+180)/360*1120,340+(80-la)/150*420];
 const path=(f:any)=>rings(f).map(r=>r.map((pt,i)=>(i?'L':'M')+project(pt[0],pt[1]).join(',')).join('')+'Z').join('');
 const nodes=[{x:121.47,y:31.23,name:'Trung Quốc'},{x:10,y:50,name:'Châu Âu'},{x:-98,y:39,name:'Bắc Mỹ'},{x:108,y:8,name:'Đông Nam Á'}];
 const a=project(nodes[0].x,nodes[0].y);
 return <><svg width={1920} height={1080}><g transform={`translate(0 ${dy})`}>{earth.features.map(f=><path key={f.id} d={path(f)} fill={f.id==='CHN'?p.accent:p.rule} stroke={p.paper} strokeWidth={.8} opacity={f.id==='CHN'?.95:.55}/>)}{nodes.slice(1).map((n,i)=>{const b=project(n.x,n.y);return <g key={n.name} opacity={enter(frame,25+i*25)}><path d={`M${a}Q${(a[0]+b[0])/2} ${Math.min(a[1],b[1])-80} ${b}`} fill="none" stroke={p.accent} strokeWidth={3} pathLength={1} strokeDasharray="1" strokeDashoffset={1-enter(frame,25+i*25,100)}/></g>;})}{nodes.map(n=>{const q=project(n.x,n.y);return <g key={n.name}><circle cx={q[0]} cy={q[1]} r={7} fill={p.accent}/><Text x={q[0]+13} y={q[1]-15} p={p} size={25}>{n.name}</Text></g>;})}</g><Caption x={180} y={821} p={p}>Kết nối minh họa · Không biểu thị tuyến tàu hay khối lượng</Caption></svg>{shot.images[0]?<div style={{position:'absolute',left:1370,top:330,width:440,height:400,overflow:'hidden',border:`8px solid ${p.paper}`,rotate:`${-3+t*3}deg`,boxShadow:'0 16px 40px #0003'}}><Media image={shot.images[0]} duration={shot.end-shot.start}/><div style={{position:'absolute',bottom:0,left:0,right:0,background:'#14221de8',padding:20,color:'#fff4df',font:'26px Arial'}}>Cảng Dương Sơn · Thượng Hải</div></div>:null}</>;
};

export const StoryScene:React.FC<{shot:any;frame:number;p:any}>=({shot,frame,p})=>{
 const duration=shot.end-shot.start;
 const prog=Math.min(1,frame/Math.max(1,duration-1));
 if(['f07','d05','e04'].includes(shot.id)){
  const cuts=shot.id==='e04'?[0,Math.min(194,Math.floor(duration/2)),duration]:[0,Math.floor(duration*.48),duration];
  return <>{shot.images.map((im:any,i:number)=><Sequence key={im.file} from={cuts[i]} durationInFrames={cuts[i+1]-cuts[i]}><AbsoluteFill style={{overflow:'hidden',clipPath:shot.id==='d05'?'polygon(0 0,100% 0,100% 100%,0 100%)':undefined}}><Media image={im} duration={cuts[i+1]-cuts[i]}/><AbsoluteFill style={{background:'linear-gradient(180deg,rgba(7,19,26,.65),transparent 44%,rgba(7,19,26,.8))'}}/></AbsoluteFill></Sequence>)}{shot.id==='f07'?<div style={{position:'absolute',left:112,top:660,color:'#fff4df',fontFamily:font}}><div style={{fontSize:56,fontWeight:700}}>Một ngành ≠ Toàn bộ nền kinh tế</div><div style={{font:'29px Arial',marginTop:20}}>Các ngành, doanh nghiệp và gia đình có thể khác nhịp.</div></div>:shot.id==='d05'?<svg width={1920} height={1080} style={{position:'absolute',inset:0}}><g transform={`translate(${120+prog*80} 670)`}><rect width={770} height={135} fill="#12232deb"/><Text x={28} y={52} p={{ink:'#fff4df'}} size={42}>Cơ hội công nghệ</Text><Caption x={28} y={100} p={{quiet:'#e3c8a0'}} size={29}>Vốn · Kỹ năng · Chuyển đổi việc làm</Caption></g></svg>:<div style={{position:'absolute',left:115,top:600,color:'#fff4df',fontFamily:font}}><div style={{fontSize:68,fontWeight:700}}>Bạn muốn đào sâu phần nào?</div><div style={{display:'flex',gap:44,marginTop:35,font:'34px Arial'}}>{['Bất động sản','Xe điện','Thương mại'].map((t,i)=><div key={t} style={{opacity:enter(frame,45+i*35),borderBottom:'3px solid #e5af6c',paddingBottom:16}}>{t}</div>)}</div><div style={{marginTop:35,font:'30px Arial'}}>Bình luận chủ đề bạn muốn tìm hiểu tiếp.</div></div>}</>;
 }
 if(shot.id==='t01')return <Atlas shot={shot} frame={frame} p={p}/>;
 return <svg width={1920} height={1080} style={{position:'absolute',inset:0}}>
  {shot.id==='o02'?<g>
    <path d="M300 745H1620M920 675L1000 675 1040 745 880 745Z" fill={p.soft} stroke={p.ink} strokeWidth={3}/><path d="M960 500V675" stroke={p.ink} strokeWidth={10}/>
    <g transform={`translate(960 500) rotate(${interpolate(frame,[0,duration*.5,duration],[-6,5,0],clamp)})`}><path d="M-560 0H560" stroke={p.ink} strokeWidth={12}/><path d="M-470 0V100M470 0V100" stroke={p.quiet} strokeWidth={3}/><path d="M-590 100H-350L-400 145H-540Z M350 100H590L540 145H400Z" fill={p.accent}/><Gear x={-470} y={-95} r={70} p={p} angle={frame*.28}/><g transform="translate(470 -130)"><Person x={-28} y={0} p={p}/><Person x={50} y={10} p={p} scale={.75}/></g></g>
    <Text x={490} y={345} p={p} size={42} anchor="middle">Sản xuất</Text><Text x={1430} y={345} p={p} size={42} anchor="middle">Sức mua</Text>
    <Caption x={705} y={809} p={p} size={30}>Năng lực tạo hàng cần gặp nhu cầu.</Caption>
  </g>:null}
  {shot.id==='o03'?<g transform={`translate(${90-prog*20} 0)`}>
    <path d="M180 350Q500 300 820 360V790Q500 730 180 760Z" fill={p.soft} stroke={p.ink} strokeWidth={2}/><path d="M820 360Q1150 305 1490 355V765Q1150 725 820 790Z" fill={p.paper} stroke={p.ink} strokeWidth={2}/><path d="M820 360V790" stroke={p.accent} strokeWidth={5}/>
    {['Động cơ sản xuất','Nhà ở và sức mua','Cấu trúc dài hạn'].map((s,i)=><g key={s} opacity={enter(frame,10+i*28)} transform={`translate(${i===0?240:915} ${i===0?470:450+(i-1)*180})`}><Text x={0} y={0} p={p} size={26}>0{i+1}</Text><Text x={0} y={55} p={p} size={37} weight={700}>{s}</Text><path d="M0 80H440" stroke={p.accent} strokeWidth={2}/></g>)}
    <path d="M1530 390l110 40v350l-110 -40Z" fill={p.accent} opacity={.65}/>
  </g>:null}
  {shot.id==='o04'?<g>
    <path d="M300 345L375 320 450 345V410Q450 470 375 505Q300 470 300 410Z" fill={p.soft} stroke={p.accent} strokeWidth={3}/><path d="M340 405l25 25 45 -55" fill="none" stroke={p.accent} strokeWidth={7}/>
    <Text x={535} y={390} p={p} size={49} weight={700}>Phân tích giáo dục</Text><Text x={535} y={452} p={p} size={35}>Không phải khuyến nghị đầu tư.</Text>
    {['Số liệu: giữ kỳ đo và nguồn','Mô phỏng: chỉ giải thích cơ chế','Không phải dự báo doanh nghiệp cụ thể'].map((s,i)=><g key={s} opacity={enter(frame,15+i*30)}><circle cx={335} cy={585+i*68} r={6} fill={p.accent}/><Text x={365} y={595+i*68} p={p} size={32}>{s}</Text></g>)}
  </g>:null}
  {shot.id==='f08'?<g>
    <path d="M200 730H1720" stroke={p.rule} strokeWidth={8}/><g transform={`translate(${300+prog*140} 0)`}><rect x={0} y={450} width={260} height={220} rx={20} fill={p.soft} stroke={p.ink} strokeWidth={3}/><Gear x={130} y={550} r={52} p={p} angle={frame*.36}/><circle cx={45} cy={697} r={35} fill={p.ink}/><circle cx={215} cy={697} r={35} fill={p.ink}/><path d="M260 610H410" stroke={p.accent} strokeWidth={7}/><rect x={410} y={540} width={390} height={150} fill={p.rule}/><Text x={605} y={610} p={p} anchor="middle" size={37}>Thu nhập</Text><circle cx={460} cy={705} r={25} fill={p.ink}/><circle cx={750} cy={705} r={25} fill={p.ink}/><path d="M800 610H925" stroke={p.accent} strokeWidth={7}/><rect x={925} y={575} width={230} height={115} fill={p.accent}/><Text x={1040} y={640} p={{ink:p.paper}} anchor="middle" size={33}>Nhu cầu</Text><circle cx={960} cy={705} r={25} fill={p.ink}/><circle cx={1120} cy={705} r={25} fill={p.ink}/></g>
    <Text x={410} y={340} p={p} size={38}>Sức kéo</Text><g opacity={enter(frame,duration*.47)}><path d="M1605 727l55 -77 55 77Z" fill={p.accent}/><Text x={1660} y={600} p={p} anchor="middle" size={32}>Điểm ghìm</Text></g>
  </g>:null}
  {shot.id==='r06'?<g>
    <Page x={160} y={320} p={p} title="WORLD BANK" sub="Rebalancing Growth · 07/2026" rotate={-4}/>
    <Page x={560} y={360} p={p} title="IMF" sub="Tham vấn 2025 · Xuất bản 2026" rotate={3} opacity={enter(frame,25)}/>
    <path d="M1005 675H1255" stroke={p.accent} strokeWidth={5} strokeDasharray="9 10"/>
    {shot.images[0]?<image href={staticFile(shot.images[0].file)} x={1210} y={345} width={500} height={350} preserveAspectRatio="xMidYMid slice"/>:<House x={1320} y={435} p={p} h={265} w={215}/>}
    <Text x={1220} y={744} p={p} size={30}>Nhà ở · Tư liệu bối cảnh Thâm Quyến</Text>
    <Text x={1120} y={800} p={p} size={28}>Bàn giao · Tổn thất · Thanh toán</Text>
  </g>:null}
  {shot.id==='p03'?<g>
    <path d="M300 390H1615V455H300Z" fill={p.rule}/><path d="M370 390H1520" stroke={p.accent} strokeWidth={10} pathLength={1} strokeDasharray="1" strokeDashoffset={1-enter(frame,15,100)}/>
    <Text x={300} y={340} p={p} size={39}>Nguồn hỗ trợ</Text>
    {['Đầu tư','Hộ gia đình','Nghĩa vụ cũ'].map((s,i)=><g key={s} opacity={enter(frame,25+i*30)} transform={`translate(${470+i*480} 0)`}><path d="M0 440V590" stroke={p.ink} strokeWidth={14}/><circle cx={0} cy={495} r={28} fill={p.paper} stroke={p.accent} strokeWidth={5}/><path d={`M-20 495H20M0 475V515`} stroke={p.accent} strokeWidth={3}/>{Array.from({length:4},(_,j)=><Coin key={j} x={0} y={555+((frame*1.1+j*35)%90)} p={p} scale={.7}/>)}<path d="M-115 655L-80 735H80L115 655" fill={p.soft} stroke={p.ink} strokeWidth={3}/><Text x={0} y={795} anchor="middle" p={p} size={32}>{s}</Text></g>)}
  </g>:null}
  {shot.id==='p07'?<g>
    {shot.images[0]?<image href={staticFile(shot.images[0].file)} x={850} y={320} width={740} height={430} preserveAspectRatio="xMidYMid slice" opacity={.26}/>:null}
    <Page x={230} y={355} p={p} title="MỘT THÔNG TIN MỚI" sub="Phải đọc cùng điều kiện và phạm vi." rotate={-3}/>
    <g transform={`translate(${970+prog*150} ${520-Math.sin(prog*Math.PI)*45})`}><circle r={145} fill={p.soft} fillOpacity={.35} stroke={p.ink} strokeWidth={15}/><path d="M105 105L210 225" stroke={p.accent} strokeWidth={35} strokeLinecap="round"/><Text x={0} y={-35} p={p} size={34} anchor="middle">Kỳ đo</Text><Text x={0} y={20} p={p} size={34} anchor="middle">Điều kiện</Text><Text x={0} y={75} p={p} size={34} anchor="middle">Phạm vi</Text></g>
    <Caption x={230} y={824} p={p} size={28}>Một con số cần bối cảnh trước khi thành kết luận.</Caption>
  </g>:null}
  {shot.id==='e01'?<g transform={`translate(${-prog*30} 0)`}>
    <path d="M130 740L400 610 700 760 1050 575 1410 710 1750 590V815H130Z" fill={p.rule}/>
    <g transform="translate(240 430)"><rect width={340} height={240} fill={p.soft}/><path d="M0 0l85 -55v55l85 -55v55l85 -55v55Z" fill={p.accent}/>{[0,1,2].map(i=><rect key={i} x={30+i*100} y={50} width={65} height={100} fill={p.paper}/>)}<Text x={170} y={300} p={p} size={32} anchor="middle">Sản xuất</Text></g>
    <House x={820} y={430} p={p} w={180} h={245}/><House x={1030} y={485} p={p} w={140} h={190}/><Text x={990} y={780} p={p} size={32} anchor="middle">Nhà ở</Text>
    <Person x={1460} y={550} p={p} scale={1.2}/><Person x={1550} y={560} p={p}/><Person x={1630} y={575} p={p} scale={.8}/><Text x={1540} y={780} p={p} size={32} anchor="middle">Hộ gia đình</Text>
    <path d="M580 550Q700 400 820 530M1170 550Q1320 410 1450 550" fill="none" stroke={p.accent} strokeWidth={5} strokeDasharray="10 10"/>
  </g>:null}
  {shot.id==='e02'?<g>
    <ellipse cx={960} cy={570} rx={625} ry={220} fill="none" stroke={p.rule} strokeWidth={42}/><path d="M380 510Q960 140 1540 510" fill="none" stroke={p.accent} strokeWidth={4} pathLength={1} strokeDasharray="1" strokeDashoffset={1-enter(frame,15,140)}/>
    <g transform="translate(295 400)"><rect width={280} height={205} fill={p.soft} stroke={p.ink} strokeWidth={2}/><path d="M0 0l70 -45v45l70 -45v45l70 -45v45Z" fill={p.accent}/><Text x={140} y={260} p={p} anchor="middle" size={34}>Doanh nghiệp</Text></g>
    <House x={1310} y={415} p={p} w={200} h={200} lit={prog>.5}/><Person x={1230} y={555} p={p}/><Text x={1420} y={680} p={p} anchor="middle" size={34}>Gia đình</Text>
    {Array.from({length:5},(_,i)=>{const a=(prog*.72+i/5)*Math.PI*2;return <Coin key={i} x={960+620*Math.cos(a)} y={570+215*Math.sin(a)} p={p}/>;})}
    <Text x={960} y={540} p={p} anchor="middle" size={38}>Thu nhập → Chi tiêu</Text><Text x={960} y={600} p={p} anchor="middle" size={38}>Đơn hàng → Việc làm</Text>
  </g>:null}
  {shot.id==='e03'?<g>
    <rect x={310} y={290} width={1200} height={535} fill={p.soft}/><path d="M345 325H1475M345 335H1475" stroke={p.rule}/>
    {['Kỳ nào?','Theo giá nào?','Mức hay tốc độ tăng?','Đại diện cho điều gì?'].map((s,i)=><g key={s} opacity={enter(frame,15+i*40)}><rect x={380} y={380+i*98} width={40} height={40} fill={p.paper} stroke={p.accent} strokeWidth={3}/><path d={`M390 ${401+i*98}l8 9 17 -22`} fill="none" stroke={p.accent} strokeWidth={4}/><Text x={455} y={414+i*98} p={p} size={38}>{s}</Text><Text x={1380} y={414+i*98} p={p} size={26} anchor="end">0{i+1}</Text></g>)}
  </g>:null}
 </svg>;
};
