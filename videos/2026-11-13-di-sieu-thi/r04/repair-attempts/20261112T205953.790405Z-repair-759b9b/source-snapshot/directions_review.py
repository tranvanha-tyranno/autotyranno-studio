"""Package locally rendered direction samples with sources and source snapshot."""
from pathlib import Path
import argparse
import hashlib
import html
import json
import shutil

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = Path(__file__).parent


def package(batch):
    snapshot = batch / 'source-snapshot'
    snapshot.mkdir(exist_ok=True)
    files = [WORKFLOW / name for name in [
        'directions.py', 'render_directions.py', 'direction_qa.py', 'directions_review.py', 'TWO_DIRECTIONS.md',
        'cinematic.profile.json', 'eleven_audio.py', 'documentary.py',
        'cinematic/src/Root.tsx', 'cinematic/src/directions-entry.tsx', 'cinematic/package.json', 'cinematic/package-lock.json',
        'cinematic/remotion.config.ts', 'cinematic/tsconfig.json',
    ]]
    files += list((WORKFLOW / 'direction-profiles').glob('*'))
    files += list((WORKFLOW / 'cinematic/src/directions').glob('*'))
    receipts = []
    for file in files:
        if not file.is_file():
            continue
        relative = file.relative_to(WORKFLOW)
        destination = snapshot / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(file, destination)
        receipts.append({'file':relative.as_posix(), 'sha256':hashlib.sha256(file.read_bytes()).hexdigest()})
    audit = ROOT / 'docs/video-references/2026-11-12-two-directions/REFERENCE_AUDIT.md'
    shutil.copy2(audit, snapshot / 'REFERENCE_AUDIT.md')
    (snapshot / 'hashes.json').write_text(json.dumps(receipts, indent=2), encoding='utf-8')
    cards = []
    metrics = {}
    for direction, label, character in [
        ('long', 'Hướng 1 · Tham chiếu Lóng', 'Trực diện, gần gũi; đặt vấn đề bằng một tình huống cụ thể.'),
        ('hidden', 'Hướng 2 · Tham chiếu The Hidden Self', 'Chậm hơn, phân tích nhiều lớp; từ nghịch lý tới cách tự kiểm tra.'),
    ]:
        folder = batch / direction
        data = json.loads((folder / 'data.json').read_text(encoding='utf-8'))
        report = json.loads((folder / 'qa/report.json').read_text(encoding='utf-8'))
        sources = json.loads((folder / 'image-sources.json').read_text(encoding='utf-8'))
        source_links = ''.join(f'<li><a href="{html.escape(row["page"], quote=True)}" target="_blank" rel="noreferrer">{html.escape(row["creator"])} — {html.escape(row["id"])}</a> · {html.escape(row["license"])}</li>' for row in sources)
        (folder / 'credits.html').write_text('<!doctype html><meta charset="utf-8"><title>Nguồn ảnh</title><style>body{max-width:960px;margin:40px auto;font:16px/1.7 Arial}a{color:#176357}</style><h1>Nguồn ảnh minh họa</h1><p>Ảnh stock minh họa thao tác và bối cảnh; không mô tả người trong ảnh đang dùng AI hoặc bảo chứng cho nội dung.</p><ul>'+source_links+'</ul>', encoding='utf-8')
        cards.append(f'''<article class="{direction}"><p class="label">{html.escape(label)}</p><h2>{html.escape(data['title'])}</h2><p class="character">{html.escape(character)}</p>
<video controls playsinline preload="metadata" poster="{direction}/poster.jpg"><source src="{direction}/final.mp4" type="video/mp4"></video>
<div class="meta"><span>{report['seconds']:.0f} giây · Full HD</span><span>{report['uniqueImages']} ảnh riêng · {report['shots']} cảnh</span></div>
<div class="links"><a href="{direction}/final.mp4">Mở video</a><a href="{direction}/script.txt">Lời dẫn</a><a href="{direction}/credits.html">Nguồn ảnh</a></div></article>''')
        metrics[direction] = report
    page = '''<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>TYRANNO · Hai hướng kể chuyện</title><style>
*{box-sizing:border-box}body{margin:0;background:#10181c;color:#f1efe7;font-family:Arial,sans-serif}main{max-width:1600px;margin:auto;padding:58px 36px}.brand{font-size:13px;letter-spacing:4px;color:#8abbb1}h1{font-size:clamp(30px,4vw,56px);letter-spacing:-1.5px;margin:22px 0 20px;max-width:1050px}.intro{color:#b8c7c9;line-height:1.65;max-width:1000px;font-size:18px}.flow{margin:30px 0 38px;color:#ddd8c9;font-size:15px;letter-spacing:.5px}.grid{display:grid;grid-template-columns:1fr 1fr;gap:30px}article{border:1px solid #314047;padding:26px;background:#152127}article.long{border-top:3px solid #f17854}article.hidden{border-top:3px solid #8abbb1}.label{font-size:12px;letter-spacing:1px;text-transform:uppercase;color:#9ab6b8}h2{font-size:26px;line-height:1.22;min-height:64px;max-width:650px}.character{color:#adbec3;line-height:1.55;min-height:50px;font-size:15px}video{width:100%;display:block;background:#080d10;margin-top:24px;aspect-ratio:16/9}.meta,.links{display:flex;justify-content:space-between;gap:15px;flex-wrap:wrap;font-size:13px}.meta{margin:19px 0;color:#a8b9be}.links{justify-content:flex-start;margin-top:23px}.links a{color:#e3e8df;text-decoration:none;border-bottom:1px solid #6a8b8d;padding-bottom:5px}.note{margin-top:38px;color:#8da4aa;font-size:14px;line-height:1.6}@media(max-width:900px){.grid{grid-template-columns:1fr}main{padding:30px 18px}article{padding:18px}h2,.character{min-height:0}}
</style></head><body><main><div class="brand">TYRANNO / HAI HƯỚNG KỂ CHUYỆN</div><h1>Ảnh thật kể chuyện.<br>Chiều sâu làm rõ ý.</h1><p class="intro">Hai bản mẫu về AI và công việc, giữ giọng Nhật Phong và cách phối âm đã chốt. Mỗi hướng có kịch bản riêng, nhiều ảnh minh họa theo lời kể và những đoạn giao diện ảnh 3D ngắn.</p><p class="flow">Hook → Miễn trừ trách nhiệm → Nội dung chính → Kêu gọi hành động</p><section class="grid">'''+''.join(cards)+'''</section><p class="note">Bản mẫu mới đang chờ phản hồi. Tham khảo cấu trúc kể chuyện của hai kênh; hình, lời và nhận diện thuộc bản dựng riêng của dự án. Ảnh chuyển khung và các tấm ảnh trong không gian 3D là ảnh tĩnh có chuyển động máy quay.</p></main></body></html>'''
    (batch / 'index.html').write_text(page, encoding='utf-8')
    (batch / 'delivery.json').write_text(json.dumps({'acceptance':'pending user feedback', 'directions':metrics}, ensure_ascii=False, indent=2), encoding='utf-8')
    print('PACKAGED', str(batch), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--batch', type=Path, default=ROOT / 'videos/2026-11-12-hai-huong')
    package(parser.parse_args().batch)
