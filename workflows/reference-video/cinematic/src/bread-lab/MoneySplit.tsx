import React from 'react';
import {interpolate, useCurrentFrame} from 'remotion';
import {Arrow, clamp, cue, Footer, LabHeading, money, MoneyToken, P, progress, Tag} from './common';
import type {BreadLabShot} from './types';

const target = (group: number, i: number) => ({x: 1015 + (i % 8) * 53, y: [310, 560, 780][group] + Math.floor(i / 8) * 23});
export const MoneySplit: React.FC<{shot: BreadLabShot}> = ({shot}) => {
  const f = useCurrentFrame(); const stage = shot.data?.stage;
  const splitAt = cue(shot, 0, .08);
  const costAt = stage === 'after' || stage === 'compare' ? cue(shot, 0, .16) : cue(shot, 1, .39);
  const priceAt = stage === 'after' || stage === 'compare' ? cue(shot, 1, .54) : cue(shot, 2, .65);
  const closeAt = stage === 'after' || stage === 'compare' ? cue(shot, 2, .8) : cue(shot, 3, .86);
  const comparison = stage === 'compare';
  const changed = comparison || stage !== 'before' && f >= costAt;
  const raised = comparison || stage !== 'before' && f >= priceAt;
  const total = raised ? 22000 : 20000; const input = changed ? 14500 : 12000; const rem = total - input - 5000;
  return <>
    <LabHeading shot={shot} title="Tiền khách trả được chia đi đâu?" subtitle="Một ổ bánh · Mỗi ô tiền là 500 đồng trong phép tính"/>
    <svg width={1920} height={1080} style={{position:'absolute',inset:0}}>
      <rect x={117} y={308} width={510} height={517} rx={16} fill={P.white} stroke={P.rule} strokeWidth={2}/>
      <Tag x={153} y={359}>Tiền bán một ổ</Tag>
      <text x={153} y={437} fontSize={65} fontWeight={700} fill={P.ink}>{money(total)}</text>
      <Tag x={153} y={782} color={P.quiet} size={24}>{raised ? 'Thêm 2.000 đ vào quầy' : 'Giữ cùng lượng bán giả định'}</Tag>
      <Arrow x1={664} y1={531} x2={920} y2={531}/>
      {[0,1,2].map((g)=><g key={g}><line x1={976} x2={1730} y1={[448,661,882][g]} y2={[448,661,882][g]} stroke={P.rule} strokeWidth={2}/><Tag x={978} y={[279,527,750][g]} color={[P.rust,P.quiet,P.green][g]} size={29}>{['Đầu vào biến đổi','Cố định phân bổ / ổ','Khoảng còn lại*'][g]}</Tag><text x={1480} y={[377,614,840][g]} fontSize={50} fontWeight={700} fill={[P.rust,P.quiet,P.green][g]}>{money([input,5000,rem][g])}</text></g>)}
      {Array.from({length:44},(_,i)=>{
        const newMoney = i >= 40;
        const source = {x:157+(i%7)*57,y:510+Math.floor((i%40)/7)*33};
        const beforeGroup = i<24?0:i<34?1:2;
        const beforeIndex = i<24?i:i<34?i-24:i-34;
        const before = target(beforeGroup,beforeIndex);
        const afterGroup = i<24||i>=34&&i<39?0:i<34?1:2;
        const afterIndex = i<24?i:i<34?i-24:i<39?i-10:i===39?0:i-39;
        const after = target(afterGroup,afterIndex);
        const splitDuration = Math.max(12,Math.min(50,shot.duration*.17));
        const p = stage==='after'||comparison?1:progress(f,splitAt+(i%40)*.65,splitDuration);
        const q = comparison?1:stage==='before'?0:progress(f,costAt+(i-34)*1.3,Math.max(12,Math.min(30,shot.duration*.1)));
        const add = comparison?1:progress(f,priceAt+(i-40)*4,Math.max(12,Math.min(30,shot.duration*.1)));
        const firstX=source.x+(before.x-source.x)*p;
        const firstY=source.y+(before.y-source.y)*p-Math.sin(p*Math.PI)*95;
        const x=newMoney?source.x+(after.x-source.x)*add:firstX+(after.x-before.x)*q;
        const y=newMoney?source.y+(after.y-source.y)*add-Math.sin(add*Math.PI)*115:firstY+(after.y-before.y)*q-Math.sin(q*Math.PI)*65;
        return <MoneyToken key={i} x={x} y={y} color={beforeGroup===1?P.gray:newMoney?P.gold:afterGroup===0&&q>.5?P.rust:beforeGroup===0&&p>.5?P.rust:P.green} opacity={newMoney?(stage==='before'?0:comparison?1:interpolate(f,[priceAt-3,priceAt],[0,1],clamp)):1}/>;
      })}
      {comparison&&<g opacity={progress(f,cue(shot,0,.1),12)}><text x={151} y={607} fontSize={32} fill={P.quiet}>Trước: còn 3.000 đ</text><text x={151} y={664} fontSize={38} fill={P.green} fontWeight={700}>Nay: còn 2.500 đ</text><path d="M155 696H501" stroke={P.rust} strokeWidth={5} strokeDasharray="9 7"/></g>}
      <g opacity={stage==='before'?0:progress(f,comparison?cue(shot,1,.45):closeAt,8)}><text x={122} y={921} fill={P.rust} fontSize={39} fontWeight={700}>Giá bán +2.000 đ</text><text x={708} y={921} fill={P.rust} fontSize={39} fontWeight={700}>Đầu vào +2.500 đ</text><text x={1310} y={921} fill={P.green} fontSize={39} fontWeight={700}>Còn lại −500 đ</text></g>
    </svg>
    <Footer>*Khoảng dư mô hình, chưa phải lợi nhuận ròng; chưa tính đủ thuế, khấu hao và công chủ tiệm.</Footer>
  </>;
};
