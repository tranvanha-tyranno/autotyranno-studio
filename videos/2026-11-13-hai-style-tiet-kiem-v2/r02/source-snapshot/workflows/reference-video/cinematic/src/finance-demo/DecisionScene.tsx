import React from 'react';
import {Character} from '../finance-cast/Character';
import {Stage,Label,Jar,Arrow,Money,rise,ink,green,gold} from './Stage';
export const DecisionScene:React.FC<{visual:string;f:number;speaking:boolean}>=({visual,f,speaking})=>{
 if(visual==='choice')return <Stage title="Có thêm thu nhập, có thêm lựa chọn">
 <Character id={1} x={300} y={885} scale={1.05} emotion="thinking" pose="idle" frame={f}/>
 <g opacity={rise(f)}><Label x={790} y={325} size={29} anchor="middle">NẾU GIỮ MỨC CHI CŨ</Label><Label x={790} y={445} size={68} anchor="middle">14 − 10 = 4 triệu</Label><Jar x={1450} y={480} value="4 triệu" level={.8}/></g>
 <g opacity={rise(f,140)}><rect x={600} y={705} width={1100} height={145} rx={22} fill="#e5d8c1"/><Label x={1150} y={765} size={34} anchor="middle">Chi phí thiết yếu tăng? Cần tính lại.</Label><Label x={1150} y={812} size={28} color="#647163" anchor="middle">Mức chi phù hợp tùy hoàn cảnh mỗi người.</Label></g>
 </Stage>;
 if(visual==='transfer')return <Stage title="Dành trước một khoản phù hợp">
 <Character id={2} x={330} y={885} scale={1.15} emotion="confident" pose="point" frame={f} speaking={speaking}/>
 <g><rect x={670} y={300} width={930} height={160} rx={24} fill="#fffaf0" stroke={ink} strokeWidth={4}/><Label x={720} y={365} size={31}>TÍNH TRƯỚC CÁC NGHĨA VỤ</Label><Label x={720} y={417} size={33}>Tiền nhà · Sinh hoạt · Nợ phải trả</Label></g>
 <g opacity={rise(f,85)}><rect x={680} y={550} width={300} height={250} rx={28} fill="#d8e8d8" stroke={ink} strokeWidth={4}/><Label x={830} y={625} size={30} anchor="middle">LƯƠNG VỀ</Label><Label x={830} y={715} size={45} anchor="middle">Đặt lịch</Label><Arrow x1={1020} y1={660} x2={1240} y2={660} color={green}/><Jar x={1430} y={680} value="Vừa sức" label="KHOẢN DÀNH TRƯỚC" fill={gold} level={.45}/>
 <Money x={1020+rise(f,160,55)*190} y={610} scale={.45}/></g>
 </Stage>;
 return <Stage title="Bắt đầu từ một khoản thôi" kicker="TỪ VÍ DỤ ĐẾN VIỆC CỦA BẠN">
 <Character id={1} x={380} y={885} scale={1.25} emotion="happy" pose="celebrate" frame={f} speaking={speaking}/>
 <Character id={2} x={1560} y={885} scale={1.25} emotion="happy" pose="give" flip frame={f}/>
 <g opacity={rise(f)}><rect x={650} y={310} width={610} height={480} rx={30} fill="#fffaf0" stroke={ink} strokeWidth={4}/>
 {['Chọn một khoản tăng gần đây','Cộng đủ cả tháng','Quyết định giữ hay giảm'].map((text,i)=><g key={text} opacity={rise(f,20+i*45)}><circle cx={710} cy={410+i*130} r={23} fill={i===0?green:gold}/><Label x={710} y={420+i*130} size={25} color={i===0?'#fff':ink} anchor="middle">{i+1}</Label><Label x={755} y={420+i*130} size={29}>{text}</Label></g>)}</g>
 </Stage>;
};
