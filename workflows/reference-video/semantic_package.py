"""Package the rebuilt examples with clause evidence and reproducible sources."""
from pathlib import Path
import argparse
import hashlib
import html
import json
import shutil

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = Path(__file__).parent


def package(batch):
    reports, cards = {}, []
    for direction, label in [('long', 'Hướng Lóng · Tình huống trực diện'), ('hidden', 'Hướng The Hidden Self · Phân tích từng việc')]:
        folder = batch / direction
        data = json.loads((folder / 'data.json').read_text(encoding='utf-8'))
        report = json.loads((folder / 'qa/report.json').read_text(encoding='utf-8'))
        actual_review = folder / 'qa/semantic-review.json'
        if actual_review.exists():
            review = json.loads(actual_review.read_text(encoding='utf-8'))
            reviewed = review['shots']
            expected = {shot['id']: shot for shot in data['shots']}
            if {shot['id'] for shot in reviewed} != set(expected):
                raise ValueError('Final semantic review does not cover all clauses: ' + direction)
            for shot in reviewed:
                evidence_record = shot['evidence']
                filename = evidence_record['file'] if isinstance(evidence_record, dict) else evidence_record
                evidence_hash = evidence_record['sha256'] if isinstance(evidence_record, dict) else shot['evidenceSHA256']
                evidence = folder / 'qa/proofs' / Path(filename).name
                if hashlib.sha256(evidence.read_bytes()).hexdigest() != evidence_hash:
                    raise ValueError('Final reviewed pixels changed: ' + shot['id'])
                shot['fullNarratedText'] = expected[shot['id']]['narratedText']
            actual_review.write_text(json.dumps(review, ensure_ascii=False, indent=2), encoding='utf-8')
            if all(shot['status'] == 'pass' for shot in reviewed):
                report['semanticAcceptance'] = 'All clause samples reviewed on final MP4; core narrated meaning visible. See VISUAL_REVIEW.md for actual scope and limits. User aesthetic acceptance pending.'
                (folder / 'qa/report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
        reports[direction] = report
        cards.append(f'''<article class="{direction}"><p class="label">{html.escape(label)}</p><h2>{html.escape(data['title'])}</h2><video controls preload="metadata" playsinline poster="{direction}/poster.jpg"><source src="{direction}/final.mp4" type="video/mp4"></video><p class="meta">{report['seconds']:.0f} giây · Full HD · {report['clauses']} cụm lời được minh họa</p><nav><a href="{direction}/final.mp4">Mở video</a><a href="{direction}/script.txt">Lời dẫn</a><a href="{direction}/VISUAL_REVIEW.md">Đối chiếu lời và hình</a></nav></article>''')
    page = '''<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>TYRANNO · Làm lại hình theo lời</title><style>*{box-sizing:border-box}body{margin:0;background:#0c1b23;color:#f0eee5;font:16px/1.6 Arial,sans-serif}main{max-width:1640px;margin:auto;padding:50px 34px}.brand{font-size:12px;letter-spacing:4px;color:#81bfb5}h1{font-size:clamp(32px,4vw,57px);line-height:1.1;letter-spacing:-1.5px;margin:24px 0}.intro{max-width:1050px;color:#b7c8cc;font-size:18px}.grid{display:grid;grid-template-columns:1fr 1fr;gap:28px;margin-top:36px}article{background:#132b35;border:1px solid #35505a;padding:26px}.long{border-top:3px solid #d96343}.hidden{border-top:3px solid #8bc9bf}.label{font-size:12px;text-transform:uppercase;letter-spacing:1px;color:#a7c0c4}h2{font-size:25px;line-height:1.3;min-height:65px}video{display:block;width:100%;aspect-ratio:16/9;background:#071117}.meta{font-size:13px;color:#9db3bb}nav{display:flex;gap:22px;flex-wrap:wrap}a{color:#d9e5df;text-decoration:none;border-bottom:1px solid #74998e;font-size:14px}.note{color:#8da8ae;font-size:14px;margin-top:32px;max-width:1100px}@media(max-width:900px){.grid{grid-template-columns:1fr}main{padding:28px 16px}article{padding:18px}h2{min-height:0}}</style></head><body><main><div class="brand">TYRANNO / BẢN DỰNG LẠI</div><h1>Nói đến đâu,<br>hình giải thích đến đó.</h1><p class="intro">Hai bản đã thay phần hình: thấy email đang soạn, lời hứa sai và nguồn gốc đối chiếu, nhu cầu khách, phần câu sửa và tổng thời gian làm việc. Giọng đọc và phối âm giữ nguyên từng bản.</p><div class="grid">'''+''.join(cards)+'''</div><p class="note">Toàn bộ đèn Mẫu A, tính năng, giá và thời gian là ví dụ giả định để giải thích công việc; không phải thông số hay kết quả thử nghiệm của sản phẩm thật. Giao diện và hình 3D được dựng cho tình huống, ảnh nguồn chỉ hỗ trợ nhận diện/thao tác phù hợp. Hai bản mới chờ phản hồi.</p></main></body></html>'''
    (batch / 'index.html').write_text(page, encoding='utf-8')
    snapshot = batch / 'source-snapshot'
    snapshot.mkdir(exist_ok=True)
    files = [*WORKFLOW.glob('semantic_*.py'), WORKFLOW / 'SEMANTIC_REBUILD.md',
             WORKFLOW / 'cinematic.profile.json', WORKFLOW / 'cinematic/src/semantic-entry.tsx', WORKFLOW / 'cinematic/src/Root.tsx',
             WORKFLOW / 'cinematic/scripts/semantic-proof.mjs', WORKFLOW / 'cinematic/package.json',
             WORKFLOW / 'cinematic/package-lock.json']
    files += list((WORKFLOW / 'semantic-profiles').glob('*')) + list((WORKFLOW / 'cinematic/src/semantic').glob('*'))
    hashes = []
    for file in files:
        if not file.is_file():
            continue
        relative = file.relative_to(WORKFLOW)
        target = snapshot / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(file, target)
        hashes.append({'file': relative.as_posix(), 'sha256': hashlib.sha256(file.read_bytes()).hexdigest()})
    for name in ['RELEARN.md', 'evidence.json']:
        shutil.copy2(ROOT / 'docs/video-references/2026-11-12-semantic-relearn' / name, snapshot / name)
    (snapshot / 'hashes.json').write_text(json.dumps(hashes, ensure_ascii=False, indent=2), encoding='utf-8')
    (batch / 'delivery.json').write_text(json.dumps({'directions': reports, 'userAcceptance': 'pending', 'scope': 'rebuild after explicit rejection for semantic mismatch'}, ensure_ascii=False, indent=2), encoding='utf-8')
    print('PACKAGED', batch, flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--batch', type=Path, default=ROOT / 'videos/2026-11-12-hai-huong-khop-loi')
    package(parser.parse_args().batch)
