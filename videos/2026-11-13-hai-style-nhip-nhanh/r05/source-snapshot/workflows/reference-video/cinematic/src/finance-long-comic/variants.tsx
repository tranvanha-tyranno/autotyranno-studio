import React from 'react';
import type {SceneProps} from './index';
import {Actor, Arrow, Bag, Bubble, C, Cash, House, Jar, Note, Phone, Room, T, Table, clamp, lerp, phase, xy} from './art';
import type {CharacterV2Props} from '../finance-cast-v2/CharacterV2';
const a=(id:1|2,x:number,f:number,extra:Partial<CharacterV2Props>={}):CharacterV2Props=>({id,x,y:925,scale:1.2,frame:f,variant:'comic',pose:id===1?'receive':'give',emotion:id===1?'thinking':'confident',flip:id===2,gaze:'right',...extra});
const Check:React.FC<{x:number;y:number;t:number}>=({x,y,t})=><g opacity={t}><circle cx={x} cy={y} r={31} fill={C.green}/><path d={`M${x-16} ${y}L${x-3} ${y+12}L${x+18} ${y-15}`} stroke={C.white} strokeWidth={6} fill="none"/></g>;
const Bike:React.FC<{x:number;y:number;scale?:number;broken?:boolean}>=({x,y,scale=1,broken=false})=><g transform={`translate(${x} ${y}) scale(${scale})`} stroke={C.ink} strokeWidth={7} fill="none"><circle cx={-113} cy={45} r={68}/><path d={broken?'M52 45Q54-27 123-24Q190-22 190 45Q191 99 146 112L133 96 115 109 101 97Q54 101 52 45Z':'M52 45A69 69 0 1 1 190 45A69 69 0 1 1 52 45Z'}/><path d="M-113 45L-40-72 37 45H-113M-40-72H85L37 45M121 45L85-72 73-104H36M-61-85H-17"/><circle cx={37} cy={45} r={14}/><path d="M37 45L59 69H80"/><path d="M-45-80L-64-112H-7" strokeWidth={11}/>{broken&&<path d="M91 129L104 149M147 123L164 142" stroke={C.red} strokeWidth={8}/>}</g>;
const Wrench:React.FC<{x:number;y:number;rotate?:number;scale?:number}>=({x,y,rotate=0,scale=1})=><g transform={`translate(${x} ${y}) rotate(${rotate}) scale(${scale})`}><path d="M-33-106Q-79-102-72-53L-32-68-9-43-33-18Q6 13 34-18Q55-42 38-75L48-95 77-97Q52-141 14-109L-13-72 82 69Q96 94 74 108Q53 119 39 96L-53-39Z" fill={C.blue} stroke={C.ink} strokeWidth={5}/></g>;

const RepairOrTreat:React.FC<SceneProps>=({f,d})=>{
 const choose=phase(f,d,.22,.82),left=a(1,980,f,{pose:choose>.65?'give':'shrug',emotion:choose>.65?'thinking':'worried'});
 return <><Room/><Actor {...left}/><g transform={`translate(${lerp(450,445,choose)} 591)`}><Bike x={0} y={0} scale={1.1} broken/><T x={0} y={226} size={36}>Xe cần sửa</T><Wrench x={211} y={-34} rotate={lerp(-20,5,choose)} scale={.8}/></g>
 <g transform="translate(1515 598)" stroke={C.ink} strokeWidth={6}><path d="M-94-55H94V85Q0 125-94 85Z" fill={C.white}/><path d="M94-30Q168-24 152 29Q143 57 94 49" fill="none"/><path d="M-34-90Q-62-125-34-148M24-90Q-2-125 24-148" stroke={C.muted}/><T x={0} y={216} size={36}>Niềm vui hôm nay</T></g>
 <g opacity={choose}><Bubble x={405} y={181} width={1100} text="Sống tốt hơn, và dành chỗ cho việc cần." fill={C.yellow}/></g></>;
};

const Frequency:React.FC<SceneProps>=({f,d})=>{
 const select=phase(f,d,.15,.85);return <><Room mode="shop"/><Actor {...a(1,310,f,{pose:'give',emotion:'happy'})}/><Actor {...a(2,1630,f,{pose:'give',emotion:'happy'})}/><Table y={770}/>
 <g transform="translate(720 524)">{Array.from({length:5},(_,i)=><g key={i} transform={`translate(${i*153} ${i%2*13})`} opacity={i>1?1-select*.77:1}><path d="M-43-26H43L32 81H-32Z" fill={i<2?C.yellow:C.white} stroke={C.ink} strokeWidth={4}/><path d="M-53-38H53V-22H-53Z" fill={C.purple} stroke={C.ink} strokeWidth={3}/>{i>1&&<path d="M-55-57L57 95" stroke={C.red} strokeWidth={6} opacity={select}/>}</g>)}</g>
 <T x={1000} y={365} size={45}>Giữ khoản đáng tiền.</T><T x={1000} y={711} size={43} fill={C.green}>Đổi tần suất của phần ít giá trị.</T><T x={1000} y={887} size={30}>Hình minh họa cách lựa chọn, không phải định mức.</T></>;
};

const SelectOne:React.FC<SceneProps>=({f,d})=>{
 const select=phase(f,d,.13,.78);return <><Room mode="desk"/><Actor {...a(1,1640,f,{pose:'give',emotion:'confident'})}/>{['GIỮ','THỬ ĐỔI','KIỂM SAU'].map((label,i)=><g key={i} transform={`translate(${425+i*410} ${560-i*25}) rotate(${i===1?lerp(-8,0,select):i===0?-9:8})`} opacity={i===1?1:1-select*.55}><Note x={0} y={0} w={320} h={340} title={label} value={i===1?'Một khoản':'Khoản chi'} fill={i===1?C.yellow:C.white}/>{i===1&&<Check x={94} y={-118} t={select}/>}</g>)}<T x={985} y={884} size={42} fill={C.green}>Một thay đổi cụ thể + ngày kiểm lại.</T></>;
};

const Gap:React.FC<SceneProps>=({f,d})=>{
 const gap=phase(f,d,.15,.68),options=phase(f,d,.67,.93);return <><Room mode="plain"/><Actor {...a(1,300,f,{pose:'shrug',emotion:'worried'})}/><Actor {...a(2,1640,f,{pose:'give',emotion:'thinking'})}/>
 <path d="M650 794H1320" stroke={C.ink} strokeWidth={8}/><rect x={720} y={lerp(650,600,gap)} width={194} height={194} fill={C.green} stroke={C.ink} strokeWidth={5}/><rect x={1065} y={lerp(620,415,gap)} width={194} height={lerp(174,379,gap)} fill={C.red} stroke={C.ink} strokeWidth={5}/><T x={817} y={850} size={32}>Thu nhập</T><T x={1162} y={850} size={32}>Thiết yếu</T>
 <g opacity={options}><House x={794} y={297} scale={.48} label="Nhà ở"/><g transform="translate(1172 286)" stroke={C.ink} strokeWidth={4}><rect x={-77} y={-57} width={154} height={114} rx={12} fill={C.yellow}/><path d="M-33-57V-85H33V-57M-77-12H77" fill="none"/><T x={0} y={107} size={26}>Công việc</T></g><T x={992} y={906} size={32}>Xem lại phương án lớn theo điều kiện thực tế.</T></g></>;
};

const UseBuffer:React.FC<SceneProps>=({f,d})=>{
 const use=phase(f,d,.15,.55),replenish=phase(f,d,.61,.93),pos=xy([607,475],[1325,523],use,145);return <><Room mode="plain"/><Actor {...a(1,321,f,{pose:'give',emotion:'confident'})}/><Actor {...a(2,1620,f,{pose:'give',emotion:'happy'})}/><Jar x={625} y={675} scale={1.1} label="SỬA VIỆC CẦN" value={use>.8?'Đã dùng':'Đã chuẩn bị'} fill={.5-use*.35+replenish*.16}/><Bike x={1260} y={674} broken={use<.8} scale={.95}/><Wrench x={1380} y={455} rotate={use*54} scale={.55}/><Cash x={pos[0]} y={pos[1]} value="Phần để dành" scale={.8}/>
 <Arrow a={[1270,842]} b={[698,846]} t={replenish} color={C.green}/><T x={989} y={912} size={36} fill={C.green}>Dùng đúng việc → bổ sung từng bước khi có thể.</T></>;
};

const TotalCost:React.FC<SceneProps>=({f,d})=>{
 const add=phase(f,d,.1,.85);return <><Room mode="shop"/><Actor {...a(1,326,f,{pose:'receive',emotion:'thinking'})}/><Actor {...a(2,1635,f,{pose:'point',emotion:'confident'})}/><Table y={802}/><g transform="translate(885 613)" stroke={C.ink} strokeWidth={6}><path d="M-139-137H139V137H-139Z" fill={C.yellow}/><path d="M-139-137L0-79 139-137M0-79V137" fill="none"/><T x={-59} y={49} size={25}>MÓN ĐỒ</T></g>
 <Note x={886} y={342} title="GIÁ TRÊN NHÃN" value="Chưa đủ" w={360} h={145}/>{['Phụ kiện cần mua','Phí giao nếu có','Chi phí sử dụng'].map((line,i)=><g key={i} opacity={clamp(add*3-i)}><Note x={1254} y={400+i*169} w={340} h={140} title={`+ PHẦN ${i+1}`} value={line} fill={C.white}/></g>)}<T x={1000} y={915} size={38} fill={C.red}>So tổng tiền phải bỏ ra và điều kiện.</T></>;
};

const Discount:React.FC<SceneProps>=({f,d})=>{
 const putDown=phase(f,d,.23,.73),question=phase(f,d,.65,.9),pos=xy([690,550],[950,715],putDown,50);return <><Room mode="shop"/><Actor {...a(1,455,f,{pose:putDown>.65?'idle':'give',emotion:'thinking'})}/><Actor {...a(2,1615,f,{pose:'give',emotion:'confident'})}/><Table y={804}/><g transform={`translate(${pos.join(' ')}) rotate(${lerp(-9,0,putDown)})`} stroke={C.ink} strokeWidth={5}><rect x={-122} y={-106} width={244} height={208} rx={10} fill={C.blue}/><path d="M-71-65H71V29H-71Z" fill={C.white}/><T x={0} y={76} size={27}>MÓN ĐỒ</T></g>
 <g transform="translate(1200 380) rotate(9)"><path d="M-180-75H136L197 0 136 75H-180Z" fill={C.red} stroke={C.ink} strokeWidth={5}/><circle cx={157} cy={0} r={12} fill={C.paper}/><T x={-10} y={18} size={45} fill={C.white}>GIẢM GIÁ</T></g><T x={1020} y={596} size={42} fill={C.red}>Mua vẫn là trả tiền.</T><g opacity={question}><Bubble x={123} y={167} width={880} text="Không khuyến mại, mình có cần không?" fill={C.yellow}/></g></>;
};

const Pause:React.FC<SceneProps>=({f,d})=>{
 const save=phase(f,d,.1,.53),wait=phase(f,d,.5,.88);return <><Room/><Actor {...a(1,380,f,{pose:'give',emotion:'thinking'})} prop="phone" propLabel="LƯU ĐỂ XEM SAU"/><Phone x={970} y={577} title="DANH SÁCH XEM SAU" lines={['Món chưa cần ngay','Đối chiếu kế hoạch','Có cần và đủ khả năng?']} checked={Math.floor(save*1)}/><g transform="translate(1523 531)" stroke={C.ink} strokeWidth={6}><circle r={155} fill={C.white}/><path d="M0-129V-108M129 0H108M0 129V108M-129 0H-108"/><path d={`M0 0L0-90`} transform={`rotate(${wait*130})`} strokeWidth={9} strokeLinecap="round"/><path d="M0 0L68 24" strokeWidth={10} strokeLinecap="round"/><circle r={9} fill={C.ink}/><T x={0} y={230} size={32}>Cho lựa chọn một nhịp.</T></g><T x={1050} y={910} size={37} fill={C.green}>Vẫn cần và đủ khả năng thì có thể mua.</T></>;
};

const Duplicate:React.FC<SceneProps>=({f,d})=>{
 const move=phase(f,d,.12,.65),classify=phase(f,d,.62,.92),pos=xy([690,497],[1300,497],move,90);return <><Room mode="plain"/><Actor {...a(2,1635,f,{pose:'point',emotion:'thinking'})}/>
 <Phone x={650} y={587} scale={.82} title="TÀI KHOẢN A" lines={['Chuyển nội bộ']}/><Phone x={1285} y={587} scale={.82} title="TÀI KHOẢN B" lines={['Nhận nội bộ']}/><Arrow a={[820,515]} b={[1115,515]} t={move} color={C.purple}/><Cash x={pos[0]} y={pos[1]} value="Cùng chủ" scale={.65}/>
 <g opacity={classify}><path d="M650 825V860H1285V825" stroke={C.green} strokeWidth={6} fill="none"/><T x={968} y={915} size={38} fill={C.green}>Chuyển chỗ ≠ mua hàng. Tránh đếm hai lần.</T><Note x={330} y={375} w={300} h={140} title="RÚT TIỀN MẶT" value="Cần ghi lúc mua" fill={C.yellow}/></g></>;
};

const Reimburse:React.FC<SceneProps>=({f,d})=>{
 const pair=phase(f,d,.15,.78);return <><Room mode="desk"/><Actor {...a(1,330,f,{pose:'receive',emotion:'thinking'})}/><Actor {...a(2,1630,f,{pose:'give',emotion:'confident'})}/><Note x={lerp(800,855,pair)} y={503} w={360} h={310} title="TRẢ TRƯỚC" value="Bữa ăn chung" rotate={lerp(-13,0,pair)}/><Note x={lerp(1330,1260,pair)} y={503} w={360} h={310} title="ĐƯỢC HOÀN LẠI" value="Phần của bạn" fill={C.yellow} rotate={lerp(12,0,pair)}/><g opacity={pair}><path d="M675 717V751H1440V717" stroke={C.green} strokeWidth={7} fill="none"/><T x={1060} y={816} size={37} fill={C.green}>Ghép hai dòng để xác định phần của mình.</T><T x={1060} y={899} size={31}>Khoản trả lại không tự thành thu nhập mới.</T></g></>;
};

const Questions:React.FC<SceneProps>=({f,d})=>{
 const compare=phase(f,d,.1,.8);return <><Room mode="desk"/><Actor {...a(2,1650,f,{pose:'give',emotion:'confident'})}/><g transform="translate(776 568) rotate(-3)"><rect x={-576} y={-278} width={1152} height={570} rx={13} fill={C.white} stroke={C.ink} strokeWidth={5}/><path d="M0-245V253" stroke={C.line} strokeWidth={4}/><T x={-288} y={-175} size={35}>CẢ THÁNG CÓ ĐỦ?</T><T x={288} y={-175} size={35}>ĐÚNG NGÀY CÓ TIỀN?</T><Jar x={-285} y={35} scale={.63} label="THU − CHI" value="Cân đối" fill={compare*.4}/><g transform="translate(287 20)"><rect x={-120} y={-107} width={240} height={219} fill={C.yellow} stroke={C.ink} strokeWidth={5}/><path d="M-120-59H120" stroke={C.ink} strokeWidth={5}/><T x={0} y={34} size={41}>ĐẾN HẠN</T><path d="M-60 68H60" stroke={C.red} strokeWidth={8}/></g><Check x={-112} y={175} t={compare}/><Check x={466} y={175} t={compare}/></g><T x={946} y={910} size={35} fill={C.green}>Cân đối tháng và lịch dòng tiền là hai phép kiểm.</T></>;
};

const SameTotal:React.FC<SceneProps>=({f,d})=>{
 const move=phase(f,d,.1,.8);return <><Room/><Actor {...a(1,330,f,{pose:'give',emotion:'confident'})}/><Actor {...a(2,1640,f,{pose:'give',emotion:'happy'})}/><Table y={804}/>{['TÚI A','TÚI B'].map((label,i)=><g key={i}><path d={`M${638+i*600} 464H${937+i*600}V745H${638+i*600}Z`} fill={i?C.yellow:C.white} stroke={C.ink} strokeWidth={6}/><path d={`M${638+i*600} 464L${788+i*600} 597L${937+i*600} 464`} fill="none" stroke={C.ink} strokeWidth={4}/><T x={788+i*600} y={704} size={32}>{label}</T></g>)}{[0,1,2,3].map(i=>{const t=clamp(move*2-i*.18),pos=xy([728+i*38,498],[1328+i*38,498],t,155);return <Cash key={i} x={pos[0]} y={pos[1]} value="Tiền" scale={.6}/>;})}<T x={1070} y={336} size={48}>Tổng tiền giữ nguyên.</T><T x={1070} y={906} size={37} fill={C.green}>Chỉ đổi nhiệm vụ, không tự tạo lợi nhuận.</T></>;
};

const Useful:React.FC<SceneProps>=({f,d})=>{
 const choose=phase(f,d,.12,.84);return <><Room/><Actor {...a(1,550,f,{pose:'receive',emotion:'confident'})}/><Bag x={1035} y={656} label="DÙNG THẬT" scale={1.07}/><g transform="translate(1520 517)" opacity={1-choose*.6}><path d="M-160 158H160" stroke={C.ink} strokeWidth={8}/><rect x={-103} y={-66} width={206} height={217} rx={19} fill={C.blue} stroke={C.ink} strokeWidth={5}/><T x={0} y={27} size={30}>ÍT DÙNG</T><path d="M-93-92l-13-9M32-96l8-20M127-5l20-8" stroke={C.muted} strokeWidth={4}/><T x={0} y={223} size={31}>Mua vì ngẫu hứng</T></g><Check x={1142} y={506} t={choose}/><T x={1040} y={335} size={43}>Chọn công dụng và mức dùng.</T><T x={1040} y={910} size={35} fill={C.green}>Ưu tiên điều cần, thay vì thi chịu thiếu thốn.</T></>;
};

const AnnualCalendar:React.FC<SceneProps>=({f,d})=>{
 const plan=phase(f,d,.12,.9);return <><Room mode="desk"/><Actor {...a(2,1640,f,{pose:'give',emotion:'thinking'})}/><g transform="translate(815 570) rotate(-3)"><rect x={-602} y={-298} width={1204} height={590} rx={12} fill={C.white} stroke={C.ink} strokeWidth={6}/><T x={0} y={-223} size={42}>LỊCH KHOẢN DỰ KIẾN</T>{Array.from({length:12},(_,i)=><g key={i} transform={`translate(${-491+(i%6)*197} ${-109+Math.floor(i/6)*194})`}><rect x={-78} y={-51} width={156} height={149} rx={8} fill={C.paper} stroke={C.ink} strokeWidth={3}/><T x={0} y={-12} size={24}>Tháng {i+1}</T>{i<plan*12&&[2,5,8,11].includes(i)&&<><path d="M-43 34H43M-43 56H27" stroke={C.purple} strokeWidth={8} strokeLinecap="round"/><Check x={46} y={-36} t={1}/></>}</g>)}</g><T x={1000} y={914} size={35} fill={C.green}>Bảo dưỡng · thay đồ dùng · nghĩa vụ định kỳ.</T></>;
};

const ReserveEnvelope:React.FC<SceneProps>=({f,d})=>{
 const reserve=phase(f,d,.12,.84);return <><Room/><Actor {...a(1,350,f,{pose:'give',emotion:'thinking'})}/><Actor {...a(2,1660,f,{pose:'give',emotion:'confident'})}/><Table y={798}/><Jar x={785} y={628} label="TÀI KHOẢN" value="Có nhiệm vụ" scale={.92} fill={.5-reserve*.23}/><path d="M1198 480H1510V737H1198Z" fill={C.yellow} stroke={C.ink} strokeWidth={5}/><path d="M1198 480L1354 611 1510 480" fill="none" stroke={C.ink} strokeWidth={5}/><T x={1354} y={698} size={27}>DỰ TRÙ THÁNG SAU</T>{[0,1,2].map(i=>{const t=clamp(reserve*2-i*.2),pos=xy([770+i*29,474],[1325+i*29,505],t,125);return <Cash key={i} x={pos[0]} y={pos[1]} value="Để riêng" scale={.6}/>;})}<T x={1020} y={337} size={44}>Tiền chưa tiêu, nhưng đã có việc.</T><T x={1040} y={906} size={34} fill={C.green}>Đổi chỗ để tránh tiêu nhầm.</T></>;
};

const Protect:React.FC<SceneProps>=({f,d,s})=>{
 const block=phase(f,d,.1,.78),cut=s.data?.action==='stop_cutting_essentials';return <><Room mode="plain"/><Actor {...a(1,370,f,{pose:'receive',emotion:'worried'})}/><Actor {...a(2,1615,f,{pose:'give',emotion:'confident'})}/><g transform="translate(1010 593)"><path d="M0-246Q173-201 287-202V9Q268 187 0 304Q-268 187-287 9V-202Q-173-201 0-246Z" fill="#D5E5D9" stroke={C.green} strokeWidth={8}/><House x={-135} y={20} scale={.65} label="NƠI Ở"/><Bag x={120} y={9} scale={.66} label="ĂN UỐNG"/><path d="M-30-159H30V-120H71V-62H30V-23H-30V-62H-71V-120H-30Z" fill={C.red} stroke={C.ink} strokeWidth={4}/></g>
 {cut&&<g transform={`translate(${lerp(1240,1454,block)} ${lerp(341,449,block)}) rotate(${lerp(-30,9,block)})`} stroke={C.ink} strokeWidth={7} fill={C.blue}><circle cx={-40} cy={38} r={32}/><circle cx={40} cy={38} r={32}/><path d="M-21 14L62-147-3-26-62-147 21 14"/><path d="M-94-114L91 79" stroke={C.red} strokeWidth={12}/></g>}
 <T x={1010} y={913} size={37} fill={C.green}>{cut?'Sức khỏe và nghĩa vụ quan trọng cần được giữ.':'Nhu cầu thiết yếu không phải khoản thừa.'}</T></>;
};

const Assumptions:React.FC<SceneProps>=({f,d})=>{
 const change=phase(f,d,.14,.86);return <><Room mode="desk"/><Actor {...a(1,330,f,{pose:'point',emotion:'thinking'})}/><Actor {...a(2,1640,f,{pose:'give',emotion:'confident'})}/><g transform="translate(1005 566) rotate(-3)"><rect x={-485} y={-271} width={970} height={570} rx={16} fill={C.white} stroke={C.ink} strokeWidth={6}/><T x={0} y={-177} size={39}>ĐIỀU KIỆN: CHI KHÁC KHÔNG ĐỔI</T><T x={0} y={-81} size={53}>14 − 11,4 = 2,6 triệu</T><g opacity={change}><path d="M-392-108L387-55" stroke={C.red} strokeWidth={7}/><Note x={0} y={73} w={600} h={144} title="NẾU TIỀN NHÀ TĂNG" value="Cần tính lại kết quả" fill={C.yellow}/><T x={0} y={230} size={35} fill={C.green}>Cập nhật giả định theo thực tế.</T></g></g></>;
};

const Reminder:React.FC<SceneProps>=({f,d})=>{
 const set=phase(f,d,.12,.78);return <><Room/><Actor {...a(1,410,f,{pose:'give',emotion:'confident'})} prop="phone" propLabel="NHẮC TRƯỚC HẠN"/><Phone x={1030} y={577} title="ĐẶT NHẮC VIỆC" lines={['Hạn thanh toán','Nhắc trước hạn','Kiểm số dư','Kiểm điều kiện']} checked={Math.floor(set*4)}/><g transform={`translate(1540 464) rotate(${lerp(-15,0,set)})`} opacity={set}><path d="M-91 66Q-67 35-67-39Q-63-119 0-119Q63-119 67-39Q67 35 91 66Z" fill={C.yellow} stroke={C.ink} strokeWidth={6}/><path d="M-30 79Q0 126 30 79" fill={C.purple} stroke={C.ink} strokeWidth={5}/><path d="M-120-39Q-135-6-121 24M120-39Q135-6 121 24" fill="none" stroke={C.ink} strokeWidth={6}/><T x={0} y={211} size={32}>Có thời gian kiểm.</T></g><T x={1100} y={914} size={36} fill={C.green}>Thông báo giúp nhớ, không tự tạo ra tiền.</T></>;
};

const Installments:React.FC<SceneProps>=({f,d})=>{
 const spread=phase(f,d,.12,.83);return <><Room mode="desk"/><Actor {...a(1,355,f,{pose:'give',emotion:'thinking'})}/><Actor {...a(2,1720,f,{pose:'point',emotion:'confident'})}/><g transform="translate(1050 568)"><path d="M-520 173H520" stroke={C.ink} strokeWidth={7}/>{Array.from({length:4},(_,i)=><g key={i} transform={`translate(${lerp(0,-420+i*280,spread)} ${lerp(-105,0,spread)})`}><rect x={-109} y={-185} width={218} height={289} rx={13} fill={C.white} stroke={C.ink} strokeWidth={5}/><rect x={-109} y={-185} width={218} height={64} rx={12} fill={C.yellow} stroke={C.ink} strokeWidth={5}/><T x={0} y={-143} size={28}>LẦN {i+1}</T><T x={0} y={-21} size={28}>Khoản trả</T><T x={0} y={40} size={25}>+ phí nếu có</T><path d="M0 108V173" stroke={C.ink} strokeWidth={5}/></g>)}<path d="M-528 223V255H528V223" stroke={C.red} strokeWidth={5} fill="none"/></g><T x={1050} y={895} size={38} fill={C.red}>Chia lần trả ≠ tổng tiền nhỏ đi.</T></>;
};

const Fields:React.FC<SceneProps>=({f,d})=>{
 const fill=phase(f,d,.1,.9);return <><Room mode="desk"/><Actor {...a(1,1635,f,{pose:'give',emotion:'thinking'})}/><g transform="translate(830 585) rotate(-3)"><rect x={-603} y={-270} width={1206} height={558} fill={C.white} stroke={C.ink} strokeWidth={6}/>{['NGÀY','KHOẢN CHI','SỐ TIỀN','GHI CHÚ'].map((label,i)=><g key={i}><path d={`M${-593+i*300}-260V276`} stroke={C.line} strokeWidth={3}/><T x={-447+i*300} y={-203} size={29}>{label}</T>{[0,1,2,3].map(row=><g key={row} opacity={clamp(fill*4-row)}><path d={`M${-561+i*300} ${-113+row*94}H${-339+i*300}`} stroke={i===2?C.green:C.purple} strokeWidth={11} strokeLinecap="round"/><path d={`M${-593+i*300} ${-76+row*94}H${-293+i*300}`} stroke={C.line} strokeWidth={2}/></g>)}</g>)}</g><T x={990} y={914} size={35}>Thêm tiền mặt, bắt đầu từ dữ liệu đang có.</T></>;
};

const OwnProgress:React.FC<SceneProps>=({f,d})=>{
 const inspect=phase(f,d,.12,.86);return <><Room mode="desk"/><Actor {...a(1,1640,f,{pose:'point',emotion:'confident'})}/><g transform="translate(825 565)"><Note x={-315} y={0} w={500} h={530} title="MÌNH THÁNG TRƯỚC" value="Ghi thiếu / quên hạn" rotate={-5}/><Note x={300} y={0} w={500} h={530} title="MÌNH THÁNG NÀY" value="Rõ khoản / rõ lịch" fill={C.yellow} rotate={3}/><path d="M-440-70H-190M-440-13H-250M175-70H425M175-13H425" stroke={C.purple} strokeWidth={12} strokeLinecap="round"/><Check x={445} y={-150} t={inspect}/></g><T x={1000} y={913} size={35} fill={C.green}>So với dữ liệu của mình, không chấm bằng người khác.</T></>;
};

export const actionScenes:Record<string,React.FC<SceneProps>>={repair_vs_treat:RepairOrTreat,keep_or_reduce:Frequency,select_one_receipt:SelectOne,income_expense_gap:Gap,use_and_replenish_buffer:UseBuffer,total_purchase_cost:TotalCost,discount_vs_need:Discount,pause_purchase:Pause,remove_duplicate_transfer:Duplicate,match_reimbursement:Reimburse,monthly_vs_timing:Questions,same_total_different_jobs:SameTotal,useful_vs_unused:Useful,annual_calendar:AnnualCalendar,reserve_envelope:ReserveEnvelope,protect_essentials:Protect,stop_cutting_essentials:Protect,schedule_reminder:Reminder,installments_on_calendar:Installments,own_progress:OwnProgress,assign_and_schedule:Reminder};
export const fieldsScene=Fields;
export const assumptionsScene=Assumptions;
