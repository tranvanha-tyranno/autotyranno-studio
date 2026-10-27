"use client";
import "../globals.css";

import type { ReactNode } from "react";

const navItems = [
  { label: "Tổng quan", icon: "grid", active: true },
  { label: "Video của tôi", icon: "play" },
  { label: "Lịch đăng", icon: "calendar" },
  { label: "Kho sản phẩm", icon: "box" },
];

const videos = [
  { title: "Máy xay Toshiba · phiên bản 01", type: "Product showcase", status: "Đã đăng", date: "Hôm nay, 09:42", views: "12.8K", color: "sunset", platform: "TikTok" },
  { title: "Serum phục hồi da ban đêm", type: "UGC review", status: "Đang xử lý", date: "Hôm nay, 10:15", views: "—", color: "lavender", platform: "Reels" },
  { title: "Tai nghe không dây Pro X", type: "Flash sale", status: "Đã lên lịch", date: "28/10, 19:30", views: "—", color: "ocean", platform: "TikTok" },
  { title: "Kem chống nắng Daily Shield", type: "Product showcase", status: "Đã đăng", date: "Hôm qua, 20:05", views: "8.4K", color: "mint", platform: "YouTube" },
];

const schedule = [
  { time: "10:30", title: "Serum phục hồi da ban đêm", channel: "Instagram Reels", color: "lavender" },
  { time: "14:00", title: "Tai nghe không dây Pro X", channel: "TikTok", color: "ocean" },
  { time: "19:30", title: "Kem chống nắng Daily Shield", channel: "YouTube Shorts", color: "mint" },
];

function Icon({ name, size = 18 }: { name: string; size?: number }) {
  const common = { width: size, height: size, viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: 1.8, strokeLinecap: "round" as const, strokeLinejoin: "round" as const };
  if (name === "grid") return <svg {...common}><rect x="3" y="3" width="7" height="7" rx="1" /><rect x="14" y="3" width="7" height="7" rx="1" /><rect x="3" y="14" width="7" height="7" rx="1" /><rect x="14" y="14" width="7" height="7" rx="1" /></svg>;
  if (name === "play") return <svg {...common}><rect x="3" y="4" width="18" height="16" rx="3" /><path d="m10 8 5 4-5 4V8Z" /></svg>;
  if (name === "calendar") return <svg {...common}><rect x="3" y="5" width="18" height="16" rx="2" /><path d="M16 3v4M8 3v4M3 10h18" /></svg>;
  if (name === "box") return <svg {...common}><path d="m12 3 8 4.5v9L12 21l-8-4.5v-9L12 3Z" /><path d="m4.3 7.7 7.7 4.5 7.7-4.5M12 12.2V21" /></svg>;
  if (name === "chart") return <svg {...common}><path d="M4 19V5M4 19h17" /><path d="m7 15 3-3 3 2 5-6" /></svg>;
  if (name === "settings") return <svg {...common}><path d="M12 15.2a3.2 3.2 0 1 0 0-6.4 3.2 3.2 0 0 0 0 6.4Z" /><path d="m19.4 15 .1.1a1.8 1.8 0 0 1-2.5 2.5l-.1-.1a1.8 1.8 0 0 0-3.1 1.3v.2a1.8 1.8 0 0 1-3.6 0v-.2a1.8 1.8 0 0 0-3.1-1.3l-.1.1a1.8 1.8 0 1 1-2.5-2.5l.1-.1A1.8 1.8 0 0 0 3.3 12a1.8 1.8 0 0 1 0-3.6h.2a1.8 1.8 0 0 0 1.3-3.1l-.1-.1a1.8 1.8 0 1 1 2.5-2.5l.1.1a1.8 1.8 0 0 0 3.1-1.3v-.2a1.8 1.8 0 0 1 3.6 0v.2a1.8 1.8 0 0 0 3.1 1.3l.1-.1a1.8 1.8 0 1 1 2.5 2.5l-.1.1A1.8 1.8 0 0 0 20.7 8h.2a1.8 1.8 0 0 1 0 3.6h-.2a1.8 1.8 0 0 0-1.3 3.4Z" /></svg>;
  if (name === "bell") return <svg {...common}><path d="M18 9a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9ZM10 21h4" /></svg>;
  if (name === "search") return <svg {...common}><circle cx="10.8" cy="10.8" r="6.8" /><path d="m16 16 4.5 4.5" /></svg>;
  if (name === "plus") return <svg {...common}><path d="M12 5v14M5 12h14" /></svg>;
  if (name === "arrow") return <svg {...common}><path d="M5 12h14M13 6l6 6-6 6" /></svg>;
  if (name === "spark") return <svg {...common}><path d="m12 3 1.5 5.5L19 10l-5.5 1.5L12 17l-1.5-5.5L5 10l5.5-1.5L12 3ZM19 16l.6 2.4L22 19l-2.4.6L19 22l-.6-2.4L16 19l2.4-.6L19 16Z" /></svg>;
  return <svg {...common}><circle cx="12" cy="12" r="8" /></svg>;
}

function MockAction({ children, primary = false, className = "" }: { children: ReactNode; primary?: boolean; className?: string }) {
  return <button className={`mock-action ${primary ? "primary" : ""} ${className}`} disabled aria-disabled="true">{children}</button>;
}

export default function Home() {
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand"><div className="brand-mark">A<span>·</span></div><div><strong>auto<span>tyranno</span></strong><small>CONTENT STUDIO</small></div></div>
        <div className="workspace-switch"><div className="workspace-avatar">T</div><div><strong>Tyranno Store</strong><small>Workspace cá nhân</small></div><span className="chevron">⌄</span></div>
        <div className="sidebar-label">WORKSPACE</div>
        <nav className="nav-list">{navItems.map((item) => <button key={item.label} className={`nav-item ${item.active ? "active" : ""}`} disabled={!item.active} aria-disabled={!item.active}><Icon name={item.icon} /><span>{item.label}</span>{item.label === "Video của tôi" && <em>12</em>}</button>)}</nav>
        <div className="sidebar-label sidebar-label-spaced">PHÂN TÍCH</div>
        <nav className="nav-list"><button className="nav-item" disabled aria-disabled="true"><Icon name="chart" /><span>Hiệu suất</span></button><button className="nav-item" disabled aria-disabled="true"><Icon name="settings" /><span>Cài đặt</span></button></nav>
        <div className="sidebar-bottom"><div className="muse-mini"><div className="muse-orb"><Icon name="spark" size={15} /></div><div><strong>Muse2API</strong><small>Chưa kết nối</small></div><span className="status-dot offline" /></div><div className="user-card"><div className="user-avatar">TN</div><div><strong>Trần Ngọc</strong><small>Chủ workspace</small></div><span className="more">•••</span></div></div>
      </aside>

      <main className="main-content">
        <header className="topbar"><div className="breadcrumb"><span>Workspace</span><b>/</b><strong>Tổng quan</strong></div><div className="topbar-actions"><div className="search-box"><Icon name="search" size={16} /><span>Tìm kiếm...</span><kbd>⌘ K</kbd></div><button className="icon-button" disabled aria-label="Thông báo"><Icon name="bell" size={19} /><i /></button><div className="top-avatar">TN</div></div></header>
        <div className="page-wrap">
          <section className="welcome-row"><div><p className="eyebrow">THỨ BA, 27 THÁNG 10, 2026</p><h1>Chào buổi sáng, Trần Ngọc <span>✦</span></h1><p className="page-intro">Theo dõi nội dung và lịch đăng của bạn trong một nơi.</p></div><MockAction primary><Icon name="plus" size={17} /> Tạo video mới</MockAction></section>

          <section className="stat-grid"><div className="stat-card"><div className="stat-head"><span className="stat-icon purple"><Icon name="play" size={17} /></span><span className="stat-trend up">↗ 18.4%</span></div><p>Video đã đăng</p><strong>128</strong><small>so với tháng trước</small></div><div className="stat-card"><div className="stat-head"><span className="stat-icon orange"><Icon name="spark" size={17} /></span><span className="stat-trend neutral">Đang xử lý</span></div><p>Đang xử lý</p><strong>12</strong><small>ước tính ~ 8 phút</small></div><div className="stat-card"><div className="stat-head"><span className="stat-icon blue"><Icon name="calendar" size={17} /></span><span className="stat-trend blue-text">Hôm nay</span></div><p>Lịch đăng hôm nay</p><strong>08</strong><small>3 nền tảng</small></div><div className="stat-card"><div className="stat-head"><span className="stat-icon green"><Icon name="chart" size={17} /></span><span className="stat-trend up">↗ 4.2%</span></div><p>Tỷ lệ thành công</p><strong>94.8%</strong><small>trong 30 ngày qua</small></div></section>

          <section className="content-grid"><div className="panel campaign-panel"><div className="panel-heading"><div><p className="eyebrow">HIỆU SUẤT</p><h2>Chiến dịch tuần này</h2></div><button className="select-button" disabled>7 ngày qua <span>⌄</span></button></div><div className="campaign-kpi"><strong>32.6K</strong><span>lượt xem tổng <b>↗ 12.8%</b></span></div><div className="chart-wrap"><div className="chart-y"><span>12K</span><span>8K</span><span>4K</span><span>0</span></div><div className="chart"><div className="grid-lines"><i /><i /><i /><i /></div><svg viewBox="0 0 620 180" preserveAspectRatio="none" className="chart-line"><defs><linearGradient id="area" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stopColor="#8f7cff" stopOpacity=".24" /><stop offset="1" stopColor="#8f7cff" stopOpacity="0" /></linearGradient></defs><path className="area" d="M0 143 C30 126 44 139 72 126 S108 107 132 119 S170 83 198 101 S238 115 264 91 S301 47 328 68 S360 91 388 80 S423 105 450 71 S493 59 520 35 S568 55 620 19 L620 180 L0 180Z" /><path className="line" d="M0 143 C30 126 44 139 72 126 S108 107 132 119 S170 83 198 101 S238 115 264 91 S301 47 328 68 S360 91 388 80 S423 105 450 71 S493 59 520 35 S568 55 620 19" /></svg><div className="chart-x"><span>T2</span><span>T3</span><span>T4</span><span>T5</span><span>T6</span><span>T7</span><span>CN</span></div></div></div></div><div className="panel api-panel"><div className="panel-heading"><div><p className="eyebrow">KẾT NỐI</p><h2>Muse2API</h2></div><span className="pill muted-pill"><i className="status-dot offline" /> Chưa kết nối</span></div><div className="api-illustration"><div className="api-ring ring-one" /><div className="api-ring ring-two" /><div className="api-core"><Icon name="spark" size={24} /></div></div><p className="api-title">Sẵn sàng tạo video AI?</p><p className="api-copy">Kết nối Muse2API để bắt đầu tạo video sản phẩm tự động.</p><MockAction className="full-button">Kết nối Muse2API <Icon name="arrow" size={16} /></MockAction><span className="preview-note"><span className="tiny-dot" /> Đây là bản xem trước frontend</span></div></section>

          <section className="lower-grid"><div className="panel schedule-panel"><div className="panel-heading"><div><p className="eyebrow">HÔM NAY</p><h2>Lịch đăng tiếp theo</h2></div><button className="text-button" disabled>Xem lịch đầy đủ <Icon name="arrow" size={15} /></button></div><div className="schedule-list">{schedule.map((item) => <div className="schedule-item" key={item.time}><time>{item.time}</time><div className={`schedule-thumb ${item.color}`}><Icon name="play" size={16} /></div><div className="schedule-info"><strong>{item.title}</strong><span>{item.channel}</span></div><span className="schedule-status">Đã lên lịch</span></div>)}</div></div><div className="panel quick-panel"><div className="panel-heading"><div><p className="eyebrow">GỢI Ý</p><h2>Bắt đầu nhanh</h2></div><Icon name="spark" size={18} /></div><div className="quick-card"><span className="quick-icon"><Icon name="box" size={18} /></span><div><strong>Thêm sản phẩm đầu tiên</strong><small>Tạo thư viện nội dung cho store</small></div><Icon name="arrow" size={16} /></div><div className="quick-card"><span className="quick-icon"><Icon name="calendar" size={18} /></span><div><strong>Lên lịch hàng loạt</strong><small>Chuẩn bị nội dung cho cả tuần</small></div><Icon name="arrow" size={16} /></div></div></section>

          <section className="panel recent-panel"><div className="panel-heading"><div><p className="eyebrow">CONTENT LIBRARY</p><h2>Video gần đây</h2></div><button className="text-button" disabled>Xem tất cả <Icon name="arrow" size={15} /></button></div><div className="table-wrap"><table><thead><tr><th>TÊN VIDEO</th><th>NỀN TẢNG</th><th>TRẠNG THÁI</th><th>NGÀY ĐĂNG</th><th>LƯỢT XEM</th></tr></thead><tbody>{videos.map((video) => <tr key={video.title}><td><div className="video-cell"><div className={`video-thumb ${video.color}`}><Icon name="play" size={15} /></div><div><strong>{video.title}</strong><span>{video.type}</span></div></div></td><td><span className="platform"><span className={`platform-dot ${video.platform.toLowerCase().replaceAll(' ', '-')}`} />{video.platform}</span></td><td><span className={`status-badge ${video.status === "Đang xử lý" ? "processing" : video.status === "Đã lên lịch" ? "scheduled" : "published"}`}><i />{video.status}</span></td><td className="date-cell">{video.date}</td><td className="views-cell">{video.views}</td></tr>)}</tbody></table></div></section>
          <footer><span>AutoTyranno v0.1 · Frontend preview</span><span><i className="status-dot offline" /> Muse2API chưa kết nối</span></footer>
        </div>
      </main>
    </div>
  );
}
