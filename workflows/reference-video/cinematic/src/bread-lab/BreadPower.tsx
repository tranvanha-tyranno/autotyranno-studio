import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Arrow,cue,Footer,LabHeading,money,number,P,progress,Tag} from './common';
import type {BreadLabShot} from './types';

export const BreadPower:React.FC<{shot:BreadLabShot}>=({shot})=>{
 const f=useCurrentFrame();const stage=shot.data?.stage;
 const salary=cue(shot,0,.13);const price=cue(shot,1,.35);const units=stage==='quantity'?cue(shot,1,.45):stage==='result'?0:cue(shot,2,.59);const answer=stage==='quantity'?cue(shot,2,.78):stage==='result'?cue(shot,0,.2):cue(shot,3,.85);
 const p=progress(f,salary,25);const q=progress(f,price,25);const r=progress(f,units,35);
 const afterIncome=f>=salary?10500000:10000000;const afterPrice=f>=price?22000:20000;
 if(stage==='income'){
  const priceCue=cue(shot,0,.1);const incomeCue=cue(shot,1,.35);const incomeAfter=cue(shot,2,.6);const endCue=cue(shot,3,.85);
  return <><LabHeading shot={shot} title="Hai tốc độ tăng trong cùng một kỳ" subtitle="Mới so thu nhập và giá chiếc bánh; chưa chuyển sang số ổ tương đương"/>
   <svg width={1920} height={1080} style={{position:'absolute',inset:0}}>
    <g opacity={progress(f,priceCue,15)}><Tag x={130} y={345} color={P.quiet} size={33}>GIÁ CÙNG CHIẾC BÁNH</Tag><text x={130} y={455} fontSize={67} fontWeight={700} fill={P.ink}>20.000 đ</text><Arrow x1={570} y1={426} x2={750} y2={426}/><text x={809} y={455} fontSize={67} fontWeight={700} fill={P.rust}>22.000 đ</text><text x={1420} y={455} fontSize={75} fontWeight={700} fill={P.rust}>+10%</text></g>
    <line x1={130} x2={1780} y1={532} y2={532} stroke={P.rule} strokeWidth={2}/>
    <g opacity={progress(f,incomeCue,15)}><Tag x={130} y={625} color={P.quiet} size={33}>THU NHẬP TRONG CÙNG KỲ</Tag><text x={130} y={738} fontSize={67} fontWeight={700} fill={P.ink}>10 triệu</text><Arrow x1={570} y1={710} x2={750} y2={710}/><g opacity={progress(f,incomeAfter,15)}><text x={809} y={738} fontSize={67} fontWeight={700} fill={P.green}>10,5 triệu</text><text x={1420} y={738} fontSize={75} fontWeight={700} fill={P.green}>+5%</text></g></g>
    <g opacity={progress(f,endCue,12)}><text x={130} y={903} fontSize={37} fill={P.ink} fontWeight={600}>Cùng nhìn số tiền tăng, nhưng chưa biết nó mua được bao nhiêu.</text></g>
   </svg><Footer>Ví dụ minh họa, không phải mức lương thị trường. Chỉ số chung và sức mua toàn giỏ chưa được tính từ một chiếc bánh.</Footer></>;
 }
 const quantityOnly=stage==='quantity'||stage==='result';const known=stage==='result';
 return <><LabHeading shot={shot} title={quantityOnly?'Cùng chiếc bánh, hai mức lương đổi được bao nhiêu?':'Lương nhiều hơn, đổi được ít bánh hơn'} subtitle="Cùng kỳ so sánh · Một chiếc bánh làm thước đo nhỏ, không phải toàn bộ chi tiêu"/>
 <svg width={1920} height={1080} style={{position:'absolute',inset:0}}>
  {quantityOnly?<><Tag x={117} y={299} color={P.quiet} size={27}>PHÉP SO ĐÃ CÓ ĐỦ ĐẦU VÀO</Tag><text x={117} y={367} fontSize={39} fontWeight={600} fill={P.ink}>10.000.000 ÷ 20.000 = 500 ổ</text><text x={955} y={367} fontSize={39} fontWeight={600} fill={P.green} opacity={known?1:progress(f,cue(shot,1,.45),15)}>10.500.000 ÷ 22.000 ≈ 477 ổ</text></>:<>
   <Tag x={117} y={299} color={P.quiet} size={27}>THU NHẬP</Tag><Tag x={955} y={299} color={P.quiet} size={27}>GIÁ CÙNG CHIẾC BÁNH</Tag>
   <text x={117} y={369} fontSize={45} fontWeight={700} fill={P.ink}>10 triệu</text><Arrow x1={426} y1={350} x2={548} y2={350}/><text x={589} y={369} fontSize={45} fontWeight={700} fill={P.green} opacity={p}>10,5 triệu</text>
   <text x={955} y={369} fontSize={45} fontWeight={700} fill={P.ink}>20.000 đ</text><Arrow x1={1244} y1={350} x2={1350} y2={350}/><text x={1392} y={369} fontSize={45} fontWeight={700} fill={P.rust} opacity={q}>22.000 đ</text>
   <Tag x={596} y={414} color={P.green} size={29}>+5%</Tag><g opacity={q}><Tag x={1410} y={414} color={P.rust} size={29}>+10%</Tag></g>
  </>}
  <Tag x={117} y={493} size={29}>Một ô = một ổ tương đương</Tag>
  {Array.from({length:500},(_,i)=>{
   const x=124+(i%50)*24;const y=535+Math.floor(i/50)*31;const missing=i>=477;
   const t=missing?(known?1:progress(f,units+(i-477)*1.2,Math.min(30,shot.duration*.1))):0;
   return <g key={i} transform={`translate(${x},${y+t*155})`} opacity={missing?1-t:1}>
    <rect width={17} height={22} rx={8} fill={missing&&t>.1?P.rust:P.gold}/><path d="M4 7L9 3M7 13L13 8" stroke={P.paper} strokeWidth={1.6}/>
   </g>;
  })}
  <text x={1454} y={568} fontSize={80} fontWeight={700} fill={P.ink}>{!known&&f<units?'500':'477'}</text><Tag x={1454} y={612} color={P.quiet} size={27}>ổ tương đương</Tag>
  <g opacity={known?1:r}><Tag x={1454} y={687} color={P.rust} size={35}>Ít hơn ≈23 ổ</Tag><text x={1454} y={773} fontSize={69} fontWeight={700} fill={P.rust}>−4,5%</text></g>
  <g opacity={progress(f,answer,10)}><text x={118} y={934} fontSize={34} fontWeight={600} fill={P.ink}>{quantityOnly?'Lương +5% · Giá bánh +10% → sức mua bánh giảm':`${money(afterIncome)} ÷ ${money(afterPrice)} ≈ ${f<price?number(afterIncome/afterPrice):'477'} ổ`}</text></g>
 </svg><Footer>477,27 được làm tròn thành 477 để vẽ ô; chênh lệch xấp xỉ 23. Không giả định dùng toàn bộ lương mua bánh; sức mua bánh giảm chính xác khoảng 4,55%.</Footer></>;
};
