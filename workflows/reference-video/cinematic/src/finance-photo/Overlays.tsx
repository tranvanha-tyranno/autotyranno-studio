import React from 'react';
import {clamp, smooth, type FinancePhotoPlan, type PhotoShot, type PhotoStyle} from './types';

const font = 'Arial, sans-serif';
const Check: React.FC<{color?: string}> = ({color = '#fff'}) => <svg width={34} height={34} viewBox="0 0 40 40"><path d="M7 20l9 9L34 10" fill="none" stroke={color} strokeWidth={4} strokeLinecap="round" strokeLinejoin="round"/></svg>;
const Bell: React.FC = () => <svg width={40} height={40} viewBox="0 0 48 48"><path d="M13 21c0-15 22-15 22 0v10l5 5H8l5-5Z" fill="none" stroke="currentColor" strokeWidth={3}/><path d="M19 41h10M24 4V1" stroke="currentColor" strokeWidth={3} strokeLinecap="round"/></svg>;

export const CaptionTrack: React.FC<{plan: FinancePhotoPlan; frame: number}> = ({plan, frame}) => {
  const c = plan.captions.find(v => frame >= v.from && frame < v.end);
  return c ? <div style={{position: 'absolute', left: 130, right: 130, bottom: 30, color: '#fff', textAlign: 'center', font: `500 38px/1.3 ${font}`, textShadow: '0 2px 5px #000', pointerEvents: 'none'}}><span style={{display: 'inline-block', maxWidth: 1650, padding: '9px 22px', borderRadius: 7, background: 'rgba(12,18,22,.85)'}}>{c.text}</span></div> : null;
};

export const ContextOverlay: React.FC<{shot: PhotoShot; frame: number; style: PhotoStyle; disclaimer?: boolean}> = ({shot, frame, style, disclaimer}) => {
  const local = frame - shot.from;
  return <>
    <div style={{position: 'absolute', left: 43, bottom: 150, font: `500 20px ${font}`, letterSpacing: .3, color: 'rgba(255,255,255,.8)', textShadow: '0 2px 4px #000'}}>Ảnh minh họa</div>
    {disclaimer ? <div style={{position: 'absolute', left: 80, right: 600, top: 155, color: '#fff', textShadow: '0 2px 14px rgba(0,0,0,.75)', fontFamily: font}}>
      <div style={{fontSize: 31, fontWeight: 700, letterSpacing: 2, marginBottom: 20}}>MIỄN TRỪ TRÁCH NHIỆM</div>
      <div style={{fontSize: 49, fontWeight: 700, lineHeight: 1.3}}>Minh, Lan và các số tiền là ví dụ giả định.</div>
      <div style={{fontSize: 34, lineHeight: 1.4, marginTop: 20}}>Không phải tư vấn tài chính cá nhân.<br/>Điều chỉnh theo hoàn cảnh của bạn.</div>
    </div> : shot.caption ? <div style={{position: 'absolute', left: 80, top: 95, maxWidth: 950, color: '#fff', fontFamily: font, fontSize: shot.caption.length > 60 ? 43 : 53, fontWeight: style === 'comic' ? 800 : 650, lineHeight: 1.16, textShadow: '0 2px 18px rgba(0,0,0,.8)', opacity: smooth(local / 7), translate: `0px ${14 * (1 - smooth(local / 7))}px`}}>{shot.caption}</div> : null}
  </>;
};

export const SubscribeOverlay: React.FC<{plan: FinancePhotoPlan; frame: number; style: PhotoStyle}> = ({plan, frame, style}) => {
  const s = plan.shots.find(v => frame >= v.from && frame < v.from + v.duration);
  const segment = plan.segments.find(v => v.id === s?.beatId);
  if (segment?.kind !== 'subscribe' || !s) return null;
  const p = Math.min(3, s.part), u = clamp((frame - s.from) / Math.max(1, s.duration - 1)), active = u > .48;
  const accent = style === 'comic' ? '#f0c54d' : '#1c967c';
  const color = p === 0 && !active ? accent : '#1d8f77';
  const text = p === 0 ? active ? 'ĐÃ ĐĂNG KÝ' : 'ĐĂNG KÝ KÊNH' : p === 1 ? 'BẬT THÔNG BÁO' : p === 2 ? 'Bạn muốn xem lại khoản chi nào?' : active ? 'ĐÃ GỬI BÌNH LUẬN' : 'ĐỂ LẠI BÌNH LUẬN';
  return <div style={{position: 'absolute', left: 80, bottom: 235, fontFamily: font, color: '#fff', textShadow: '0 2px 12px #000'}}>
    <div style={{fontSize: 56, fontWeight: 750, marginBottom: 25, maxWidth: 900}}>{p < 2 ? 'Thấy video hữu ích?' : p === 2 ? 'Chọn một khoản chi trong tháng này.' : 'Hẹn gặp ở video tiếp theo.'}</div>
    <div style={{position: 'relative', display: 'inline-flex', gap: 20, alignItems: 'center', minHeight: 86, padding: '17px 28px', borderRadius: style === 'comic' ? 12 : 7, background: color, color: p === 0 && !active && style === 'comic' ? '#152b2d' : '#fff', boxShadow: '0 8px 30px rgba(0,0,0,.18)', textShadow: 'none', fontSize: p === 2 ? 35 : 36, fontWeight: 750}}>
      {p === 1 ? <Bell/> : active && p !== 2 ? <Check/> : null}{text}
      {p !== 2 && u > .2 && u < .75 && <div style={{position: 'absolute', right: 22, bottom: 8, width: 25, height: 25, borderRadius: '50%', background: '#fff', opacity: (1 - Math.abs(u - .48) / .28) * .8, scale: .6 + smooth((u - .2) / .55) * 1.8, border: '2px solid rgba(0,0,0,.15)'}}/>}
    </div>
  </div>;
};
