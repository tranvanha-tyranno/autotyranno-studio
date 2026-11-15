import React from 'react';
import {AbsoluteFill, Easing, interpolate, useCurrentFrame} from 'remotion';

export type FinanceSegment = {
  id: string;
  from: number;
  duration: number;
  text: string;
  kind: string;
  speaker: string;
  visual: string;
};

export type FinancePlan = {
  durationFrames: number;
  segments: FinanceSegment[];
};

const P = {
  paper: '#F4F1E9',
  ink: '#193133',
  muted: '#62706B',
  line: '#D5DBD0',
  green: '#087D66',
  pale: '#DCEBCF',
  orange: '#B75E3C',
  white: '#FFFEF8',
};
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const ease = Easing.bezier(.16, 1, .3, 1);
const enter = (f: number, at = 0, length = 24) => interpolate(f, [at, at + length], [0, 1], {...clamp, easing: ease});

const Reveal: React.FC<React.PropsWithChildren<{f: number; at?: number; style?: React.CSSProperties}>> = ({f, at = 0, children, style}) => (
  <div style={{opacity: enter(f, at), translate: `0px ${(1 - enter(f, at)) * 26}px`, ...style}}>{children}</div>
);

const Header: React.FC<{step: string; title: string; f: number}> = ({step, title, f}) => <Reveal f={f} style={{position: 'absolute', left: 128, top: 72, width: 1664}}>
  <div style={{fontSize: 22, fontWeight: 700, color: P.green, letterSpacing: 3.2, marginBottom: 24}}>{step}</div>
  <div style={{fontSize: 62, fontWeight: 700, lineHeight: 1.15, letterSpacing: -1.8}}>{title}</div>
</Reveal>;

const Note: React.FC<{text?: string}> = ({text = 'Số liệu giả định để minh họa • Không phải mức chi tiêu khuyến nghị'}) => <div style={{position: 'absolute', left: 128, top: 865, width: 1664, borderTop: `2px solid ${P.line}`, paddingTop: 19, fontSize: 22, color: P.muted}}>{text}</div>;

const Rule: React.FC<{x: number; y: number; width: number; f: number; at?: number}> = ({x, y, width, f, at = 0}) => <div style={{position: 'absolute', left: x, top: y, width: width * enter(f, at), height: 3, background: P.ink}}/>;

const Arrow: React.FC<{color?: string; width?: number}> = ({color = P.green, width = 88}) => <svg width={width} height="54" viewBox="0 0 88 54" fill="none"><path d="M3 27H80M57 5L80 27L57 49" stroke={color} strokeWidth="5" strokeLinecap="round" strokeLinejoin="round"/></svg>;

const Hook: React.FC<{f: number}> = ({f}) => <>
  <Header f={f} step="LƯƠNG TĂNG, TIỀN DƯ CŨNG TĂNG?" title="Chưa chắc."/>
  <Reveal f={f} at={4} style={{position: 'absolute', left: 128, top: 330, width: 520}}>
    <div style={{fontSize: 28, color: P.muted}}>Thu nhập tăng</div>
    <div style={{fontSize: 150, fontWeight: 700, letterSpacing: -9, color: P.green, lineHeight: 1.15}}>+2 triệu</div>
  </Reveal>
  <Reveal f={f} at={17} style={{position: 'absolute', left: 728, top: 330, width: 560}}>
    <div style={{fontSize: 28, color: P.muted}}>Chi tiêu tăng</div>
    <div style={{fontSize: 150, fontWeight: 700, letterSpacing: -9, color: P.orange, lineHeight: 1.15}}>+2 triệu</div>
  </Reveal>
  <Reveal f={f} at={28} style={{position: 'absolute', left: 1330, top: 359, width: 480}}>
    <div style={{fontSize: 32, fontWeight: 700}}>Tiền dư tăng</div>
    <div style={{fontSize: 168, fontWeight: 700, letterSpacing: -10, lineHeight: 1.03}}>0</div>
  </Reveal>
  <Rule x={128} y={600} width={1664} f={f} at={20}/>
  <Reveal f={f} at={34} style={{position: 'absolute', left: 128, top: 652, fontSize: 37, color: P.muted, width: 1500}}>Hai triệu tăng thêm có thể đã có chỗ để đi.</Reveal>
  <Note/>
</>;

const Disclaimer: React.FC<{f: number}> = ({f}) => <>
  <Reveal f={f} style={{position: 'absolute', left: 128, top: 137, fontSize: 24, letterSpacing: 3.2, fontWeight: 700, color: P.green}}>MIỄN TRỪ TRÁCH NHIỆM</Reveal>
  <Reveal f={f} at={5} style={{position: 'absolute', left: 128, top: 260, width: 1510, fontSize: 82, lineHeight: 1.18, fontWeight: 700, letterSpacing: -2}}>Một tình huống giả định.<br/>Để hiểu cách tiền dịch chuyển.</Reveal>
  <Rule x={128} y={540} width={160} f={f} at={10}/>
  <Reveal f={f} at={14} style={{position: 'absolute', left: 128, top: 600, width: 1500, fontSize: 35, lineHeight: 1.55, color: P.muted}}>Các con số chỉ dùng minh họa.<br/>Nội dung giáo dục, không thay thế tư vấn tài chính cá nhân.</Reveal>
</>;

const Ledger: React.FC<{f: number; after?: boolean}> = ({f, after = false}) => {
  const rows = [
    {label: 'Thu nhập', value: after ? 14 : 12, color: P.ink, mark: '+'},
    {label: 'Chi tiêu', value: after ? 12 : 10, color: P.orange, mark: '−'},
    {label: 'Còn dư', value: 2, color: P.green, mark: '='},
  ];
  return <>
    <Header f={f} step={after ? '02 / SAU KHI TĂNG LƯƠNG' : '01 / MỘT THÁNG BAN ĐẦU'} title={after ? 'Thu nhập mới. Khoản dư cũ.' : 'Mỗi tháng, còn dư 2 triệu.'}/>
    <div style={{position: 'absolute', left: 128, top: 300, width: 1050}}>
      {rows.map((r, i) => <Reveal f={f} at={i * 10} key={r.label} style={{height: 150, borderBottom: i < 2 ? `2px solid ${P.line}` : undefined, display: 'flex', alignItems: 'center', justifyContent: 'space-between'}}>
        <div style={{display: 'flex', alignItems: 'center', gap: 28}}><span style={{fontSize: 42, fontWeight: 400, width: 45, color: P.muted}}>{r.mark}</span><span style={{fontSize: 37, fontWeight: i === 2 ? 700 : 400}}>{r.label}</span></div>
        <div style={{fontSize: i === 2 ? 100 : 90, letterSpacing: -3, color: r.color, fontWeight: 700}}>{r.value}<span style={{fontSize: 28, letterSpacing: 0, fontWeight: 400, marginLeft: 15}}>triệu</span></div>
      </Reveal>)}
    </div>
    <Reveal f={f} at={25} style={{position: 'absolute', left: 1355, top: 378, width: 420, color: after ? P.orange : P.green}}>
      <div style={{fontSize: 23, fontWeight: 700, letterSpacing: 1.5, marginBottom: 25}}>SO VỚI BAN ĐẦU</div>
      {after ? <><div style={{fontSize: 32, lineHeight: 1.65}}>Lương: <b>+2 triệu</b><br/>Chi: <b>+2 triệu</b></div><div style={{height: 2, background: P.line, margin: '25px 0'}}/><div style={{fontSize: 35, fontWeight: 700, lineHeight: 1.4}}>Khoản dư<br/>không tăng.</div></> : <><div style={{fontSize: 29, lineHeight: 1.55, color: P.muted}}>Điểm xuất phát<br/>để so sánh<br/>tháng tiếp theo.</div><div style={{marginTop: 26}}><Arrow/></div></>}
    </Reveal>
    <Note text="Ví dụ giả định • Đơn vị: triệu đồng / tháng"/>
  </>;
};

const Cup: React.FC<{x: number; y: number; scale?: number; opacity?: number}> = ({x, y, scale = 1, opacity = 1}) => <g transform={`translate(${x} ${y}) scale(${scale})`} opacity={opacity} stroke={P.ink} strokeWidth="4" strokeLinecap="round" strokeLinejoin="round" fill="none"><path d="M0 0H66L59 72H9L0 0Z" fill={P.white}/><path d="M8 -10H58M-6 1H72M25 24H42M22 38H45"/><path d="M20 -25C12 -34 29 -42 22 -51M43 -25C35 -34 52 -42 45 -51" stroke={P.green}/></g>;

const Daily: React.FC<{f: number}> = ({f}) => <>
  <Header f={f} step="03 / TIỀN ĐI TỪ NHỮNG VIỆC NHỎ" title="Thêm 60.000 đồng mỗi ngày."/>
  <Reveal f={f} at={6} style={{position: 'absolute', left: 128, top: 290, width: 1664, fontSize: 32, color: P.muted}}>Ví dụ: nâng mức ăn uống, cà phê hoặc giao đồ ăn.</Reveal>
  <svg style={{position: 'absolute', left: 128, top: 407, width: 620, height: 290}} viewBox="0 0 620 290">
    {Array.from({length: 30}, (_, i) => <g key={i} opacity={enter(f, 10 + i * 1.4, 10)}><Cup x={17 + (i % 10) * 60} y={30 + Math.floor(i / 10) * 90} scale={.5}/></g>)}
  </svg>
  <Reveal f={f} at={18} style={{position: 'absolute', left: 865, top: 416, width: 920}}>
    <div style={{fontSize: 52, letterSpacing: -1}}>60.000 <span style={{color: P.muted}}>× 30 ngày</span></div>
    <div style={{fontSize: 145, lineHeight: 1.2, letterSpacing: -7, fontWeight: 700, color: P.orange}}>= 1,8 triệu</div>
    <div style={{fontSize: 29, color: P.muted, marginTop: 18}}>Một khoản nhỏ, lặp lại cả tháng.</div>
  </Reveal>
  <Note text="Giả định: tăng thêm 60.000 đồng / ngày trong 30 ngày • Không phải giá thị trường"/>
</>;

const Dinner: React.FC<{f: number}> = ({f}) => <>
  <Header f={f} step="04 / CỘNG THÊM MỘT KHOẢN NỮA" title="Một bữa ăn thêm: 200.000 đồng."/>
  <svg viewBox="0 0 1920 1080" style={{position: 'absolute', inset: 0}}>
    <g opacity={enter(f, 8)} transform="translate(1280 440)" stroke={P.ink} strokeWidth="5" fill="none" strokeLinecap="round">
      <ellipse cx="210" cy="80" rx="157" ry="107" fill={P.white}/><ellipse cx="210" cy="80" rx="108" ry="68" stroke={P.line}/><path d="M0 -23V164M-24 -23V34Q-24 56 0 56Q24 56 24 34V-23M-12 -23V23M12 -23V23M420 -23C365 -15 378 71 418 71V164"/>
      <path d="M145 67Q180 28 216 66T287 66M155 90Q199 120 250 88" stroke={P.green} strokeWidth="12"/>
    </g>
  </svg>
  <Reveal f={f} at={2} style={{position: 'absolute', left: 128, top: 365, width: 1050}}>
    <div style={{fontSize: 51, color: P.muted}}>1.800.000 + 200.000</div>
    <div style={{fontSize: 139, fontWeight: 700, letterSpacing: -6, marginTop: 18, color: P.orange}}>= 2 triệu</div>
  </Reveal>
  <Reveal f={f} at={18} style={{position: 'absolute', left: 128, top: 670, fontSize: 38, width: 1450, lineHeight: 1.4}}>Vừa hết phần thu nhập tăng thêm.</Reveal>
  <Note text="Ví dụ giả định • Chỉ tính phần chi tăng thêm, không phải tổng chi ăn uống"/>
</>;

const Choice: React.FC<{f: number}> = ({f}) => <>
  <Header f={f} step="05 / CÙNG MỘT MỨC LƯƠNG" title="Khoản chi quyết định phần còn lại."/>
  <Reveal f={f} at={4} style={{position: 'absolute', left: 128, top: 302, width: 1664, fontSize: 29, color: P.muted}}>Nếu vẫn giữ mức chi ban đầu, phép tính sẽ đổi:</Reveal>
  <div style={{position: 'absolute', top: 403, left: 128, display: 'flex', gap: 90, width: 1664}}>
    <Reveal f={f} at={8} style={{width: 720}}>
      <div style={{fontSize: 25, color: P.orange, fontWeight: 700, letterSpacing: 1.6}}>CHI TĂNG THEO LƯƠNG</div>
      <div style={{fontSize: 75, letterSpacing: -3, marginTop: 37}}>14 − 12 = <b>2</b></div>
      <div style={{fontSize: 29, color: P.muted, marginTop: 25}}>Còn dư 2 triệu / tháng</div>
    </Reveal>
    <div style={{width: 2, background: P.line, height: 288}}/>
    <Reveal f={f} at={20} style={{width: 780}}>
      <div style={{fontSize: 25, color: P.green, fontWeight: 700, letterSpacing: 1.6}}>GIỮ MỨC CHI BAN ĐẦU</div>
      <div style={{fontSize: 75, letterSpacing: -3, marginTop: 37}}>14 − 10 = <b style={{color: P.green}}>4</b></div>
      <div style={{fontSize: 29, color: P.green, marginTop: 25}}>Còn dư 4 triệu / tháng</div>
    </Reveal>
  </div>
  <Reveal f={f} at={115} style={{position: 'absolute', left: 128, top: 750, width: 1664, fontSize: 30, color: P.orange, lineHeight: 1.4}}>Chi phí thiết yếu tăng? Hãy tính lại, đừng ép mình theo con số này.</Reveal>
  <Note text="Mô hình giả định • Giữ nguyên các khoản khác để so sánh tác động của chi tiêu"/>
</>;

const Transfer: React.FC<{f: number}> = ({f}) => {
  const p = enter(f, 30, 54);
  return <>
    <Header f={f} step="06 / BIẾN Ý ĐỊNH THÀNH LỊCH" title="Tiền vừa về. Phân bổ trước."/>
    <Reveal f={f} at={5} style={{position: 'absolute', top: 312, left: 128, width: 700}}>
      <div style={{fontSize: 47, fontWeight: 700, lineHeight: 1.3}}>Chọn khoản tiết kiệm<br/>phù hợp với mình.</div>
      <div style={{fontSize: 31, color: P.muted, lineHeight: 1.65, marginTop: 42}}>Có thể hẹn chuyển khi nhận lương,<br/>sau khi tính đủ nhu cầu thiết yếu<br/>và nghĩa vụ cần thanh toán.</div>
    </Reveal>
    <div style={{position: 'absolute', left: 957, top: 300, width: 820, height: 440, border: `2px solid ${P.line}`, borderRadius: 24, padding: 40, boxSizing: 'border-box', background: P.white}}>
      <div style={{fontSize: 22, color: P.muted, letterSpacing: 1.5, fontWeight: 700}}>MÔ PHỎNG PHÂN BỔ TIỀN</div>
      <div style={{position: 'absolute', left: 40, right: 40, top: 108, display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: 29, fontWeight: 700}}><span>Tài khoản lương</span><span style={{color: P.green}}>Tiết kiệm</span></div>
      <svg style={{position: 'absolute', left: 0, top: 180, width: 820, height: 85}} viewBox="0 0 820 85" fill="none">
        <path d="M115 42H630M612 26L630 42L612 58" stroke={P.line} strokeWidth="4" strokeLinecap="round" strokeLinejoin="round"/>
        <circle cx="72" cy="42" r="32" stroke={P.line} strokeWidth="3"/>
        <circle cx="700" cy="42" r="32" stroke={P.green} strokeWidth="3" fill={P.pale}/>
      </svg>
      <div style={{position: 'absolute', left: 43, top: 193, width: 58, height: 58, borderRadius: 30, background: P.green, color: P.white, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 30, translate: `${p * 628}px 0px`}}>₫</div>
      <div style={{position: 'absolute', left: 40, right: 40, top: 302, height: 2, background: P.line}}/>
      <div style={{position: 'absolute', left: 40, right: 40, top: 327, display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
        <span style={{fontSize: 27, color: P.muted}}>Ngày nhận lương</span>
        <span style={{fontSize: 25, color: P.green, fontWeight: 700, opacity: enter(f, 88)}}>✓ Chuyển theo lịch</span>
      </div>
    </div>
    <Note text="Cách phân bổ phụ thuộc hoàn cảnh cá nhân • Giao diện minh họa, không phải ứng dụng ngân hàng"/>
  </>;
};

const CTA: React.FC<{f: number}> = ({f}) => <>
  <Reveal f={f} style={{position: 'absolute', left: 128, top: 118, fontSize: 24, fontWeight: 700, letterSpacing: 3, color: P.green}}>THỬ NGAY HÔM NAY</Reveal>
  <Reveal f={f} at={5} style={{position: 'absolute', left: 117, top: 216, fontSize: 250, fontWeight: 700, lineHeight: 1, letterSpacing: -20, color: P.green}}>1</Reveal>
  <Reveal f={f} at={8} style={{position: 'absolute', left: 330, top: 255, width: 1400, fontSize: 75, lineHeight: 1.24, fontWeight: 700, letterSpacing: -2}}>Chọn một khoản chi<br/>đang tự động lớn lên.</Reveal>
  <Rule x={128} y={580} width={1664} f={f} at={16}/>
  <Reveal f={f} at={20} style={{position: 'absolute', left: 128, top: 631, fontSize: 41, color: P.muted, lineHeight: 1.5, width: 1550}}>Khoản đó có còn đáng với bạn?<br/><span style={{color: P.ink, fontWeight: 700}}>Xem lại một khoản trước khi thêm một khoản mới.</span></Reveal>
</>;

/** Low-cost alternative: authored typography and arithmetic, no paid visual generation.
 * Frame positions come from the exact narration plan; no independent timing clock.
 * Root owns the shared audio and subtitles so A/B visuals can share one exact take.
 */
export const Minimal: React.FC<{plan: FinancePlan}> = ({plan}) => {
  const frame = useCurrentFrame();
  const segment = plan.segments.find((s) => frame >= s.from && frame < s.from + s.duration) ?? plan.segments[plan.segments.length - 1];
  if (!segment) return <AbsoluteFill style={{background: P.paper}}/>;
  const f = frame - segment.from;
  const opacity = interpolate(f, [0, 7, Math.max(8, segment.duration - 7), segment.duration], [0, 1, 1, 0], clamp);
  let content: React.ReactNode;
  switch (segment.visual) {
    case 'hook': content = <Hook f={f}/>; break;
    case 'disclaimer': content = <Disclaimer f={f}/>; break;
    case 'before': content = <Ledger f={f}/>; break;
    case 'after': content = <Ledger f={f} after/>; break;
    case 'daily': content = <Daily f={f}/>; break;
    case 'dinner': content = <Dinner f={f}/>; break;
    case 'choice': content = <Choice f={f}/>; break;
    case 'transfer': content = <Transfer f={f}/>; break;
    case 'cta': content = <CTA f={f}/>; break;
    default: content = <Header f={f} step="TIỀN & THÓI QUEN" title={segment.text}/>;
  }
  return <AbsoluteFill style={{background: P.paper, color: P.ink, fontFamily: 'Arial, sans-serif', fontVariantNumeric: 'tabular-nums', overflow: 'hidden'}}>
    <div style={{position: 'absolute', width: '100%', height: 9, background: P.line}}><div style={{height: '100%', width: `${100 * (frame + 1) / Math.max(1, plan.durationFrames)}%`, background: P.green}}/></div>
    <AbsoluteFill style={{opacity}}>{content}</AbsoluteFill>
  </AbsoluteFill>;
};
