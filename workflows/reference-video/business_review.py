"""Build and locally serve a restrained, unbranded business-video review page."""
from __future__ import annotations

import argparse
from functools import partial
import html
from html.parser import HTMLParser
from http.server import ThreadingHTTPServer
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

from serve_reference_study import StudyHandler
from business_qa import revision_folder


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def esc(value):
    return html.escape(str(value or ''), quote=True)


def stamp(seconds):
    total = int(seconds)
    return f'{total // 60:02}:{total % 60:02}'


def web_link(url, label):
    if urlsplit(str(url or '')).scheme not in ['https', 'http']:
        return esc(label)
    return f'<a href="{esc(url)}" target="_blank" rel="noopener noreferrer">{esc(label)}</a>'


def plain(value):
    return html.unescape(re.sub(r'<[^>]*>', '', str(value or ''))).strip()


class VisibleText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ignored = 0
        self.text = []

    def handle_starttag(self, tag, attrs):
        if tag in ['script', 'style']:
            self.ignored += 1

    def handle_endtag(self, tag):
        if tag in ['script', 'style']:
            self.ignored = max(0, self.ignored - 1)

    def handle_data(self, data):
        if not self.ignored:
            self.text.append(data)


def build(batch, revision=None):
    batch = Path(batch).resolve()
    film = revision_folder(batch, revision)
    prefix = film.relative_to(batch).as_posix() + '/' if film != batch else ''
    data, content = load(film / 'data.json'), load(batch / 'content.json')
    chapters = load(batch / 'chapter-timing.json')
    shots = {shot['id']: shot for shot in data['shots']}
    buttons = ''.join(f'<button class="chapter" data-time="{row["startSeconds"]:.6f}"><span>{stamp(row["startSeconds"])}</span>{esc(row["title"])}</button>' for row in chapters)
    transcript = []
    for chapter in content['chapters']:
        entries = []
        for beat in chapter['beats']:
            shot = shots[beat['id']]
            at = shot['start'] / data['fps']
            entries.append(f'<li><button class="clause" data-time="{at:.6f}"><span>{stamp(at)}</span>{esc(shot.get("headline") or beat["id"])}</button><p>{esc(beat["text"])}</p></li>')
        transcript.append(f'<section><h3>{esc(chapter["title"])}</h3><ol>{"".join(entries)}</ol></section>')

    rows, seen = [], set()
    for record in load(batch / 'source-receipts.json'):
        source = record['source']
        identity = source.get('sha256') or record.get('sourceSHA256') or source.get('id')
        if identity in seen:
            continue
        seen.add(identity)
        creator = plain(source.get('creator', 'Tác giả chưa ghi rõ'))
        page = source.get('page') or source.get('url') or source.get('source', {}).get('url')
        title = source.get('title') or source.get('id', 'Ảnh / clip minh họa')
        license_name = source.get('license') or source.get('source', {}).get('license', 'Xem biên nhận nguồn')
        license_url = source.get('licenseURL') or source.get('source', {}).get('licenseURL')
        location = source.get('location', {})
        if not isinstance(location, dict):
            location = {'place': str(location)}
        place = location.get('place') or 'Chưa xác nhận nơi chụp / quay'
        date = source.get('capturedDate')
        published = source.get('sourcePublishedDate')
        dating = f'Chụp / quay: {esc(date)}' if date else f'Đăng nguồn: {esc(published)}; ngày quay chưa xác nhận' if published else 'Ngày chụp / quay chưa xác nhận'
        inspection = source.get('inspection', {})
        limits = inspection.get('doesNotEstablish') or source.get('role') or 'Tư liệu minh họa bối cảnh; không chứng minh kết quả kinh doanh của cơ sở được chụp.'
        observed = inspection.get('observedSubjectAction')
        modification = source.get('modifications')
        rows.append(f'<li class="source"><h4>{web_link(page, plain(title))}</h4><p>{web_link(page, creator)} · {web_link(license_url, license_name)}</p><p class="muted">{dating} · {esc(place)}</p>{f"<p>{esc(observed)}</p>" if observed else ""}<p class="muted">{esc(limits)}</p>{f"<p class=muted>{esc(modification)}</p>" if modification else ""}</li>')
    title = esc(data['title'])
    duration = stamp(data['frames'] / data['fps'])
    qa_link = f'<a href="{esc(prefix)}qa/report.json">Kiểm tra bản xuất</a>' if (film / 'qa/report.json').is_file() else ''
    script_link = prefix + 'script.txt' if (film / 'script.txt').is_file() else 'script.txt'
    poster_link = prefix + 'poster.jpg' if (film / 'poster.jpg').is_file() else 'poster.jpg'
    page = '''<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>'''+title+'''</title><style>
*{box-sizing:border-box}body{margin:0;background:#f1ecdf;color:#24332a;font:17px/1.6 Arial,sans-serif}main{max-width:1220px;margin:auto;padding:42px 28px 70px}h1{font-size:clamp(28px,4vw,48px);line-height:1.14;letter-spacing:-1.4px;max-width:1040px;margin:0 0 16px}.intro{color:#6a7167;max-width:960px;margin:0 0 25px}.player{position:relative;background:#14251b;box-shadow:0 15px 40px #17311a19}video{display:block;width:100%;aspect-ratio:16/9;background:#14251b}.chapters{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:24px 0 30px}button{font:inherit;cursor:pointer}.chapter{text-align:left;background:transparent;border:1px solid #d6cebd;padding:12px 15px;color:#334238;line-height:1.32;font-size:14px;min-height:77px}.chapter span,.clause span{display:block;color:#af4f33;font-size:12px;font-variant-numeric:tabular-nums;margin-bottom:5px}.chapter.active{background:#e0d7c5;border-color:#9caa99}.links{display:flex;gap:22px;flex-wrap:wrap;font-size:14px;margin:0 0 35px}a{color:#38634c;text-decoration-thickness:1px;text-underline-offset:4px}details{border-top:1px solid #d4cbb9;padding:20px 0}summary{font-size:18px;font-weight:700;cursor:pointer}details>p{color:#6a7167;max-width:950px}h3{font-size:23px;margin:32px 0 14px}ol{list-style:none;padding:0;margin:0}li{margin:0 0 20px}.clause{background:transparent;border:0;padding:0;text-align:left;font-weight:700;color:#243b2c}.clause span{display:inline-block;width:57px;margin:0 12px 0 0}li p{margin:7px 0 0;color:#59685c;max-width:1050px}.sources{list-style:none;padding:0}.source{padding:20px 0;border-bottom:1px solid #ded7c7;font-size:14px}.source h4{margin:0 0 6px;font-size:16px}.source p{margin:5px 0}.muted{color:#718071!important}.sound{font-size:14px;color:#6c796e;margin-top:20px}.footlinks{font-size:13px;margin-top:25px;display:flex;gap:20px}@media(max-width:800px){main{padding:26px 17px 45px}.chapters{grid-template-columns:repeat(2,1fr)}.chapter{min-height:70px}h1{letter-spacing:-.8px}.clause span{width:auto;margin-right:10px}}@media(prefers-reduced-motion:reduce){*{scroll-behavior:auto}}
</style></head><body><main><h1>'''+title+'''</h1><p class="intro">'''+duration+''' · Một mô hình cà phê giả định để nhìn rõ phần đóng góp, hòa vốn và lịch tiền mặt. Ảnh và clip minh họa bối cảnh; không mô tả kết quả kinh doanh của các quán trong hình.</p><div class="player"><video id="film" controls playsinline preload="metadata" poster="'''+esc(poster_link)+'''"><source src="'''+esc(prefix)+'''final.mp4" type="video/mp4"></video></div><nav class="chapters" aria-label="Chọn chương">'''+buttons+'''</nav><div class="links"><a href="'''+esc(prefix)+'''final.mp4">Mở video</a><a href="'''+esc(script_link)+'''">Lời dẫn</a>'''+qa_link+'''</div><details><summary>Lời dẫn theo từng đoạn</summary>'''+''.join(transcript)+'''</details><details><summary>Nguồn hình và giấy phép</summary><p>Các con số trong mô hình được tạo cho ví dụ giáo dục. Ảnh / clip bên dưới dùng để minh họa hành động và bối cảnh; địa điểm chưa được nguồn xác nhận được giữ nguyên giới hạn ấy.</p><ul class="sources">'''+''.join(rows)+'''</ul></details><details><summary>Âm thanh</summary><p class="sound">Giọng Nhật Phong, nhạc không lời thay đổi theo mạch kể và hiệu ứng theo hành động. Nhạc hạ dưới lời dẫn; một số nhịp dừng giữ khoảng yên để làm rõ ý.</p><div class="footlinks"><a href="audio-sources.json">Nguồn âm và bản phối</a><a href="sound-cues.json">Các điểm âm thanh</a></div></details></main><script>
const film=document.getElementById('film');const chapterButtons=[...document.querySelectorAll('.chapter')];document.querySelectorAll('[data-time]').forEach(button=>button.addEventListener('click',()=>{film.currentTime=Number(button.dataset.time);film.play().catch(()=>{});}));film.addEventListener('timeupdate',()=>{let active=-1;chapterButtons.forEach((button,i)=>{if(Number(button.dataset.time)<=film.currentTime)active=i;});chapterButtons.forEach((button,i)=>button.classList.toggle('active',i===active));});film.addEventListener('loadedmetadata',()=>{const match=location.hash.match(/^#t=(\d+(?:\.\d+)?)$/);if(match)film.currentTime=Math.min(Number(match[1]),Math.max(0,film.duration-.1));});
</script></body></html>'''
    visible = VisibleText()
    visible.feed(page)
    if 'tyranno' in '\n'.join(visible.text).casefold():
        raise ValueError('Review page includes forbidden visible channel branding')
    (batch / 'index.html').write_text(page, encoding='utf-8')
    return {'page': str(batch / 'index.html'), 'chapters': len(chapters), 'clauses': len(shots),
            'uniqueSources': len(rows), 'visibleBrandingPass': True, 'revision': revision,
            'video': prefix + 'final.mp4', 'qa': prefix + 'qa/report.json'}


class ReviewHandler(StudyHandler):
    def list_directory(self, path):
        self.send_error(403, 'Directory listing disabled')
        return None


def serve(batch, port=8882):
    root = Path(batch).resolve(strict=True)
    if not (root / 'index.html').is_file():
        raise ValueError('Build the review page before serving')
    server = ThreadingHTTPServer(('127.0.0.1', port), partial(ReviewHandler, directory=root))
    print(f'Review: http://127.0.0.1:{port}/index.html', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--batch', type=Path, required=True)
    parser.add_argument('--port', type=int, default=8882)
    parser.add_argument('--revision', help='Optional prepared batch subfolder such as r02')
    parser.add_argument('--build-only', action='store_true')
    args = parser.parse_args()
    print(json.dumps(build(args.batch, revision=args.revision), ensure_ascii=False))
    if not args.build_only:
        serve(args.batch, args.port)
