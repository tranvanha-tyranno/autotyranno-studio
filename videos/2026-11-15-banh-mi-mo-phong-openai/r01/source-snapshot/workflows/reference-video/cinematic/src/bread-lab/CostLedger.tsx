import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Arrow,cue,Footer,LabHeading,P,progress,Tag} from './common';
import type {BreadLabShot} from './types';

export const CostLedger:React.FC<{shot:BreadLabShot}> = ({shot})=>{
 const f=useCurrentFrame();const down=cue(shot,0,.15);const others=cue(shot,1,.39);const total=cue(shot,2,.66);const counter=cue(shot,3,.85);
 const rows=['Bột','Tiền thuê','Lương đã thỏa thuận','Điện · nhân · bao bì'];
 const counterMode=shot.data?.stage==='counterexample';
 const stage=shot.data?.stage;
 if(stage==='not_net_profit')return <><LabHeading shot={shot} title="3.000 đồng chưa phải tiền bỏ túi" subtitle="Giữ nguyên khoảng dư mô hình, mở những khoản chưa tính thay vì gọi nó là lợi nhuận ròng"/>
 <svg width={1920} height={1080} style={{position:'absolute',inset:0}}>
  <text x={185} y={500} fontSize={140} fontWeight={700} fill={P.green}>3.000 đ</text><Tag x={190} y={569} size={35}>Khoảng còn lại trong phép tính</Tag>
  <Arrow x1={784} y1={513} x2={1050} y2={513}/>
  {['Thuế','Khấu hao','Công của chủ tiệm'].map((name,i)=>{const p=progress(f,cue(shot,i,.15+i*.22),25);return <g key={name} opacity={p}><path d={`M${1100} ${380+i*155}H${1690}`} stroke={P.rule} strokeWidth={2}/><Tag x={1130} y={437+i*155} size={37}>{name}</Tag><text x={1630} y={437+i*155} fill={P.rust} fontSize={38}>?</text><path d={`M${1055} ${512}Q${1080} ${437+i*155} ${1110} ${437+i*155}`} fill="none" stroke={P.rust} strokeWidth={3}/></g>;})}
  <g opacity={progress(f,cue(shot,3,.85),10)}><text x={188} y={799} fontSize={52} fill={P.rust} fontWeight={700}>Chưa tính đủ → chưa kết luận lãi ròng</text></g>
 </svg><Footer>Khoản 3.000 đồng là phần dư sau những chi phí đã đưa vào mô hình, không phải khoản thu nhập thực tế của chủ tiệm.</Footer></>;
 if(stage==='question')return <><LabHeading shot={shot} title="Tin lạm phát hạ chưa trả lời hóa đơn của tiệm" subtitle="Phân biệt một tỷ lệ chung với các khoản chi cụ thể trước khi đưa ra giả thuyết giá bột giảm"/>
 <svg width={1920} height={1080} style={{position:'absolute',inset:0}}><Tag x={145} y={351} size={36}>Bản tin</Tag><text x={145} y={447} fontSize={64} fontWeight={700} fill={P.green}>Tỷ lệ thấp hơn</text>
 <Arrow x1={765} y1={494} x2={1025} y2={494} dashed/><text x={850} y={450} fontSize={39} fill={P.rust}>≠</text>
 {['Bao bột','Tiền thuê','Tiền điện'].map((name,i)=><g key={name} opacity={progress(f,cue(shot,i,.1+i*.15),20)}><Tag x={1110} y={365+i*122} size={34}>{name}</Tag><text x={1670} y={365+i*122} fontSize={44} fill={P.quiet}>?</text></g>)}
 <g opacity={progress(f,cue(shot,3,.75),12)}><text x={144} y={757} fontSize={48} fontWeight={700} fill={P.ink}>Nếu có một hóa đơn giảm thật?</text><Tag x={145} y={837} size={29} color={P.quiet}>Đó là tình huống cần kiểm tiếp, chưa phải điều bản tin tự chứng minh.</Tag></g>
 </svg><Footer>Không suy ra từng chi phí đã về giá cũ chỉ từ tỷ lệ lạm phát thấp hơn.</Footer></>;
 return <><LabHeading shot={shot} title={counterMode?'Nếu tổng chi phí thật sự giảm thì sao?':'Một dòng giảm chưa phải tổng chi phí giảm'} subtitle={counterMode?'Phản biện có điều kiện: giữ nguyên giá bán và lượng bán; xét tổng chi phí đã giảm thật':'Không giả định thêm mức giá thực tế; mô phỏng hướng thay đổi của từng khoản'}/>
 <svg width={1920} height={1080} style={{position:'absolute',inset:0}}>
  <rect x={108} y={273} width={1175} height={623} rx={12} fill={P.white} stroke={P.rule} strokeWidth={2}/>
  <Tag x={151} y={322} size={25} color={P.quiet}>Khoản chi</Tag><Tag x={652} y={322} size={25} color={P.quiet}>Trước</Tag><Tag x={957} y={322} size={25} color={P.quiet}>Hiện tại</Tag>
  {rows.map((name,i)=>{
    const y=397+i*128;const show=i===0?1:progress(f,others+(i-1)*9,15);const drop=i===0?progress(f,down,34):0;
    return <g key={name} opacity={show}>
      <line x1={150} x2={1240} y1={y+74} y2={y+74} stroke={P.rule}/><Tag x={151} y={y+23} size={29}>{name}</Tag>
      <line x1={662} x2={822} y1={y+12} y2={y+12} stroke={P.gray} strokeWidth={10} strokeLinecap="round"/>
      <line x1={957} x2={1117-drop*80} y1={y+12} y2={y+12} stroke={i===0?P.green:P.gray} strokeWidth={10} strokeLinecap="round"/>
      <text x={1174} y={y+23} fill={i===0?P.green:P.quiet} fontSize={i===0?41:28} fontWeight={700}>{i===0?(drop>.5?'↓':'—'):i===3&&!counterMode?'?':'='}</text>
    </g>;
  })}
  <path d="M1312 363H1340V845H1312" fill="none" stroke={P.ink} strokeWidth={3}/>
  <g opacity={progress(f,total,12)}><Arrow x1={1361} y1={606} x2={1450} y2={606}/><Tag x={1467} y={528} color={P.quiet} size={29}>Tổng chi phí</Tag><text x={1464} y={619} fontSize={counterMode?56:78} fontWeight={700} fill={counterMode?P.green:P.ink}>{counterMode?'Đã giảm ↓':'Chưa biết'}</text><text x={1467} y={689} fontSize={29} fill={P.quiet}>{counterMode?'Trong giả định này':'Phải cộng đủ các khoản'}</text></g>
  <g opacity={progress(f,counter,8)}><rect x={1410} y={753} width={370} height={136} fill="#dce5d4" rx={8}/><text x={1441} y={797} fontSize={25} fontWeight={600} fill={P.green}>{counterMode?'Cùng lượng bán':'Một khoản giảm'}</text><text x={1441} y={846} fontSize={29} fontWeight={700} fill={P.ink}>{counterMode?'Khoảng dư có thể tăng':'≠ mọi khoản đều giảm'}</text></g>
 </svg><Footer>Độ dài nét chỉ minh họa hướng, không thể hiện quyền số hay tỷ lệ chi phí. Cần sổ thực tế trước khi kết luận tiệm lời hơn.</Footer></>;
};
