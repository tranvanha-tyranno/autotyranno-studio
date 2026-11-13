import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {Character, type Emotion, type Pose} from './Character';
import {roster} from './roster';
const font='Arial, sans-serif';

export const CastSheet:React.FC=()=> <AbsoluteFill style={{background:'#F5F0E7'}}>
 <svg viewBox="0 0 1920 1080" width="1920" height="1080" style={{fontFamily:font}}>
  <text x="72" y="54" fill="#263D42" fontWeight="700" fontSize="31">30 NHÂN VẬT • THƯ VIỆN HOẠT HÌNH TÀI CHÍNH</text>
  <text x="1848" y="52" textAnchor="end" fill="#6B7678" fontSize="19">THIẾT KẾ GỐC / BẢN XEM THỬ</text>
  {roster.map((c,i)=>{const x=60+(i%6)*302;const y=83+Math.floor(i/6)*187;return <g key={c.id}>
    <rect x={x} y={y} width="288" height="177" rx="18" fill={i%2?'#ECE8E2':'#FFFDF8'} stroke="#DCD8D0"/>
    <text x={x+14} y={y+25} fill="#83908C" fontSize="18" fontWeight="700">{String(c.id).padStart(2,'0')}</text>
    <Character id={c.id} x={x+145} y={y+132} scale={0.25} frame={42} emotion={(['happy','neutral','confident','thinking'] as Emotion[])[i%4]}/>
    <text x={x+145} y={y+150} textAnchor="middle" fill="#253D43" fontSize="20" fontWeight="700">{c.name}</text>
    <text x={x+145} y={y+170} textAnchor="middle" fill="#667673" fontSize="15">{c.role}</text>
  </g>})}
  <text x="72" y="1050" fill="#667673" fontSize="20">6 biểu cảm · 8 tư thế · Chớp mắt, đầu, tay và miệng điều khiển bằng frame · Nhân vật hư cấu trưởng thành</text>
 </svg>
</AbsoluteFill>;

const poses:Pose[]=['talk','point','shrug','give','receive','celebrate'];
const emotions:Emotion[]=['neutral','thinking','worried','surprised','confident','happy'];
const labels=['GIẢI THÍCH','CHỈ VÀO Ý CHÍNH','BĂN KHOĂN','TRAO / ĐƯA','NHẬN / CÂN NHẮC','VUI MỪNG'];
export const CastMotion:React.FC=()=>{
 const f=useCurrentFrame();
 const step=Math.floor(f/60)%6;
 const actors=[1,3,2,5,10,14];
 return <AbsoluteFill style={{background:'#F5F0E7'}}>
  <svg viewBox="0 0 1920 1080" width="1920" height="1080" style={{fontFamily:font}}>
   <text x="72" y="74" fill="#263D42" fontWeight="700" fontSize="40">MỘT BỘ NHÂN VẬT. NHIỀU TÌNH HUỐNG.</text>
   <text x="73" y="114" fill="#667673" fontSize="23">Thử chuyển động và biểu cảm • Tái sử dụng trực tiếp trong cảnh kể chuyện</text>
   {actors.map((id,i)=>{const x=68+(i%3)*600;const y=153+Math.floor(i/3)*423;const p=(step+i)%6;const c=roster[id-1];return <g key={id}>
    <rect x={x} y={y} width="584" height="401" rx="25" fill={i%2?'#E4ECE5':'#FFFCF6'} stroke="#D9DFD8" strokeWidth="2"/>
    <Character id={id} x={x+294} y={y+322} scale={0.62} frame={f} pose={poses[p]} emotion={emotions[p]} speaking={p===0}/>
    <text x={x+26} y={y+39} fill="#557B73" fontWeight="700" fontSize="21">{String(id).padStart(2,'0')} / {c.name}</text>
    <text x={x+292} y={y+369} fill="#263D42" textAnchor="middle" fontSize="23" fontWeight="700">{labels[p]}</text>
   </g>})}
   <text x="72" y="1050" fill="#667673" fontSize="21">Chuyển động miệng là hoạt họa theo nhịp frame, không phải đồng bộ âm vị.</text>
  </svg>
 </AbsoluteFill>;
};
