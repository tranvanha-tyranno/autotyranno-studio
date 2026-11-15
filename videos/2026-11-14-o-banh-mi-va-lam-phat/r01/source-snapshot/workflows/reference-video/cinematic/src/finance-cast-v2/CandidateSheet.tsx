import React from 'react';
import {AbsoluteFill} from 'remotion';
import {CharacterV2,type EmotionV2,type PoseV2} from './CharacterV2';

const situations:{title:string;quote1:string;quote2:string;label1:string;label2:string;emotion1:EmotionV2;emotion2:EmotionV2;pose1:PoseV2;pose2:PoseV2;bg:string}[]=[
 {title:'01 / HỎI XOÁY MỘT CHÚT',quote1:'“Có mua gì lớn đâu?”',quote2:'“Thử cộng những món nhỏ nhé.”',label1:'MINH / BĂN KHOĂN',label2:'LAN / TỰ TIN',emotion1:'thinking',emotion2:'confident',pose1:'shrug',pose2:'talk',bg:'#F4E8DA'},
 {title:'02 / NHẬN RA VẤN ĐỀ',quote1:'“Mỗi ngày có từng này...”',quote2:'“Cả tháng là ngần này!”',label1:'MINH / BẤT NGỜ',label2:'LAN / GIẢI THÍCH',emotion1:'surprised',emotion2:'confident',pose1:'receive',pose2:'give',bg:'#EFE6EC'},
 {title:'03 / NHẸ NHÕM, HƠI HÀI',quote1:'“À, tìm ra rồi!”',quote2:'“Giờ mình chọn lại được rồi.”',label1:'MINH / NHẸ NHÕM',label2:'LAN / VUI VẺ',emotion1:'happy',emotion2:'happy',pose1:'celebrate',pose2:'talk',bg:'#E9EDE2'},
];

export const CandidateSheet:React.FC=()=> <AbsoluteFill style={{background:'#FAF6ED'}}>
 <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080" style={{fontFamily:'Arial, sans-serif'}}>
  <text x="62" y="66" fontSize="40" fontWeight="700" fill="#2D3040">COMIC BIỂU CẢM MẠNH, HƠI HÀI HƯỚC</text>
  <text x="62" y="111" fontSize="24" fill="#727178">Tạo hình mới cho Minh &amp; Lan • Hai người trưởng thành, ba nhịp tương tác</text>
  {situations.map((s,i)=>{const x=54+i*624;return <g key={s.title}>
   <rect x={x} y="147" width="600" height="856" rx="25" fill={s.bg} stroke="#D7D0CD" strokeWidth="2"/>
   <rect x={x+24} y="177" width="8" height="38" rx="4" fill="#786397"/>
   <text x={x+47} y="205" fontSize="26" fontWeight="700" fill="#383342">{s.title}</text>
   <path d={`M${x+44} 246H${x+554}Q${x+577} 246 ${x+577} 269V355Q${x+577} 378 ${x+554} 378H${x+402}L${x+386} 395 ${x+371} 378H${x+44}Q${x+22} 378 ${x+22} 355V269Q${x+22} 246 ${x+44} 246Z`} fill="#FFFCF5" stroke="#786397" strokeWidth="2.2"/>
   <text x={x+43} y="295" fontSize={i===1?22:23} fill="#3B3545" fontWeight="700">Minh: {s.quote1}</text>
   <text x={x+43} y="341" fontSize="21" fill="#765C57">Lan: {s.quote2}</text>
   <CharacterV2 id={1} x={x+165} y={934} scale={0.93} emotion={s.emotion1} pose={s.pose1} frame={42} variant="comic" gaze="right"/>
   <CharacterV2 id={2} x={x+435} y={934} scale={0.93} emotion={s.emotion2} pose={s.pose2} frame={42} variant="comic" gaze="right" flip/>
   {i===1&&<g transform={`translate(${x+295},777)`} stroke="#4B4053" strokeWidth="2.5" strokeLinejoin="round">
    <path d="M-56-26H56V43L43 36 31 43 19 36 7 43-5 36-17 43-29 36-41 43-56 36Z" fill="#FFFCF1"/>
    <path d="M-34-7H34M-34 7H18M-34 21H29" fill="none" opacity=".4"/>
   </g>}
   {i===1&&<g stroke="#8E679E" strokeWidth="3" fill="none" strokeLinecap="round"><path d={`M${x+57} 487l-13-13M${x+49} 512l-18-3M${x+80} 472l-2-18`}/></g>}
   <text x={x+165} y="979" fontSize="17" textAnchor="middle" fontWeight="700" fill="#65576E">{s.label1}</text><text x={x+435} y="979" fontSize="17" textAnchor="middle" fontWeight="700" fill="#65576E">{s.label2}</text>
  </g>})}
  <text x="62" y="1047" fontSize="21" fill="#747178">Bản xem trước tạo hình • Thiết kế gốc, nhân vật hư cấu trưởng thành • Chưa nhân rộng lại 30 nhân vật</text>
 </svg>
</AbsoluteFill>;
