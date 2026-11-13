"""Build a private review page for one existing production revision.

The page reads saved media, exact-take timing, source/crop receipts and QA evidence.
It never renders a video, changes a composition, executes a queue or assigns user
approval. --allow-pending builds a clearly labeled preview while assets are pending.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from urllib.parse import quote, urlparse


def read(path, default=None):
    return json.loads(Path(path).read_text(encoding='utf-8-sig')) if Path(path).is_file() else default


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def within(root, path):
    resolved = Path(path).resolve()
    if not resolved.is_relative_to(root):
        raise ValueError('Review files must remain inside the declared review root: ' + str(path))
    return resolved


def local_link(root, path):
    file = within(root, path)
    return quote(file.relative_to(root).as_posix(), safe='/') if file.is_file() else None


def external_url(value):
    return value if isinstance(value, str) and urlparse(value).scheme == 'https' else None


def file_link(root, path, label):
    path = within(root, path)
    if not path.is_file():
        return None
    return {'label': label, 'file': local_link(root, path), 'sha256': sha(path)}


def build(root, batch, manifest=None, direction='long', allow_pending=False):
    root = Path(root).resolve(strict=True)
    revision = within(root, root / batch)
    folder = within(root, revision / direction)
    manifest_path = within(root, root / manifest) if manifest else folder / 'production-manifest.json'
    content = read(manifest_path)
    retained = read(folder / 'production-manifest.json')
    if content is None:
        if not allow_pending:
            raise ValueError('Production manifest is not ready: ' + str(manifest_path))
        content = {'title': 'Video thử quy trình mới', 'sections': [], 'assets': []}
    if retained is not None and content != retained:
        raise ValueError('Review manifest differs from the retained production manifest')
    data = read(folder / 'data.json', {})
    qa = read(folder / 'qa/report.json', {})
    media = folder / 'final.mp4'
    pending = []
    for file in [media, folder / 'data.json', folder / 'qa/report.json']:
        if not file.is_file():
            pending.append(file.relative_to(root).as_posix())
    fps = data.get('fps', 30)
    if not isinstance(fps, (int, float)) or fps <= 0:
        raise ValueError('Timeline must have a positive FPS')
    shots = data.get('shots', [])
    if data:
        if (not shots or shots[0]['start'] != 0 or shots[-1]['end'] != data['frames']
                or any(s['end'] <= s['start'] for s in shots)
                or any(a['end'] != b['start'] for a, b in zip(shots, shots[1:]))):
            raise ValueError('Saved exact-take timeline is not continuous')
    if qa and (qa.get('expectedFrames') != data.get('frames')
               or qa.get('decodedFrames') != data.get('frames') or not qa.get('frameCountPass')):
        raise ValueError('Saved QA does not account for the complete timeline')
    media_sha = sha(media) if media.is_file() else None
    if qa and media_sha and qa.get('videoSHA256') != media_sha:
        raise ValueError('QA receipt belongs to a different MP4')
    if pending and not allow_pending:
        raise ValueError('Final review is missing files: ' + ', '.join(pending))

    manifest_shots = {s['id']: s for section in content.get('sections', []) for s in section.get('shots', [])}
    assets = {asset['id']: asset for asset in content.get('assets', [])}
    originals = {row['id']: row for row in read(folder / 'image-sources.json', [])}
    derivatives = {row['id']: row for row in read(folder / 'render-assets.json', {}).get('assets', [])}
    records = []
    frames_found = 0
    for index, shot in enumerate(shots):
        source = manifest_shots.get(shot.get('id'), shot)
        midpoint = min(shot['end'] - 1, shot['start'] + max(1, (shot['end'] - shot['start']) // 2))
        frame = folder / f'qa/frame-{midpoint:05d}.jpg'
        frame_info = file_link(root, frame, 'Frame giữa cảnh')
        if frame_info:
            frames_found += 1
        images = []
        for asset_id in source.get('images', []):
            if not isinstance(asset_id, str):
                continue
            asset, original, derivative = assets.get(asset_id, {}), originals.get(asset_id, {}), derivatives.get(asset_id, {})
            source_file = (folder / original['file']) if original.get('file') else (manifest_path.parent / asset.get('file', ''))
            source_file = within(root, source_file)
            derivative_file = within(root, revision / 'production-public' / derivative.get('publicFile', ''))
            saved_hash = original.get('sha256') or asset.get('sha256')
            if source_file.is_file() and saved_hash and sha(source_file) != saved_hash:
                raise ValueError('Source receipt no longer matches: ' + asset_id)
            if derivative_file.is_file() and derivative.get('publicSHA256') and sha(derivative_file) != derivative['publicSHA256']:
                raise ValueError('Crop derivative no longer matches: ' + asset_id)
            source_meta = asset.get('source', {})
            images.append({'id': asset_id, 'sourceFile': local_link(root, source_file),
                'sha256': saved_hash, 'renderFile': local_link(root, derivative_file),
                'renderSHA256': derivative.get('publicSHA256'),
                'crop': derivative.get('method', {}).get('crop', asset.get('crop', [0, 0, 1, 1])),
                'focus': asset.get('focus', [50, 50]),
                'kind': asset.get('mediaType', 'image'), 'sourceRole': source_meta.get('kind'),
                'sourceURL': external_url(source_meta.get('url') or original.get('page')),
                'creator': source_meta.get('creator') or original.get('creator'),
                'license': source_meta.get('license') or original.get('license'),
                'licenseURL': external_url(source_meta.get('licenseURL') or original.get('licenseURL')),
                'observed': asset.get('observed', original.get('observed', {})),
                'inspection': asset.get('inspection', original.get('inspection', {}))})
        records.append({'id': shot.get('id', f'shot-{index+1}'), 'index': index,
            'phase': shot.get('phase'), 'startFrame': shot['start'], 'endFrame': shot['end'],
            'start': shot['start'] / fps, 'end': shot['end'] / fps,
            'clause': shot.get('narrationClause') or source.get('narrationClause', ''),
            'phrase': shot.get('phrase'), 'layout': shot.get('layout'),
            'headline': shot.get('headline'), 'body': shot.get('body'), 'sourceNote': shot.get('sourceNote'),
            'mediaRole': shot.get('mediaRole'), 'needToSee': shot.get('needToSee'),
            'supports': shot.get('supports'), 'limits': shot.get('limits'),
            'sourceIds': shot.get('sourceIds', []), 'review': shot.get('review', {}),
            'frame': {**frame_info, 'index': midpoint, 'time': midpoint / fps} if frame_info else None,
            'images': images})
    if qa and not allow_pending and frames_found != len(records):
        raise ValueError('Final review requires the retained QA midpoint frame for every shot')

    candidates = [
        (root / 'README.md', 'Hướng dẫn bản thử'), (root / 'PRODUCTION_NOTES.md', 'Ghi chú sản xuất và giới hạn'),
        (root / 'UPGRADES.md', 'Nâng cấp theo phản hồi mới'),
        (revision / 'CREDITS.md', 'Nguồn và giấy phép ảnh'),
        (root / 'source-vietnam.json', 'Nguồn ảnh tại Việt Nam'),
        (revision / 'SEMANTIC_CORRECTION.md', 'Kiểm cảnh nhãn khuyến mại'),
        (manifest_path, 'Manifest sản xuất'), (folder / 'script.txt', 'Lời dẫn đã chốt'),
        (folder / 'qa/report.json', 'QA kỹ thuật'), (folder / 'preflight.json', 'Timing và preflight'),
        (folder / 'qa/INDEPENDENT_VISUAL_REVIEW.md', 'Kiểm hình độc lập của revision'),
        (folder / 'qa/independent-visual-review.json', 'Ghi chú hình theo từng cảnh'),
        (root / 'r03/long/qa/INDEPENDENT_VISUAL_REVIEW.md', 'Kiểm hình độc lập r03 trước sửa'),
        (root / 'r03/long/qa/independent-visual-review.json', 'Ghi chú r03 và hai cảnh cần sửa'),
        (folder / 'image-sources.json', 'Biên nhận nguồn ảnh'), (folder / 'render-assets.json', 'Crop và bản render'),
        (folder / 'audio-sources.json', 'Giọng, nhạc và mix'), (folder / 'aligned-words.json', 'Mốc từ của take thật'),
        (folder / 'learning-guidance.json', 'Guidance đã pin trong batch'),
        (folder / 'research.json', 'Hồ sơ nghiên cứu'), (folder / 'RESEARCH.md', 'Ghi chú nghiên cứu'),
        (root / 'long/research.json', 'Hồ sơ nghiên cứu chủ đề'), (root / 'long/RESEARCH.md', 'Nguồn nghiên cứu chủ đề'),
        (folder / 'review.json', 'Nhận xét revision'), (folder / 'REVIEW.md', 'Ghi chú kiểm revision'),
        (root / 'learning/report.json', 'Lịch sử cải tiến của pilot'), (root / 'learning/guidance.json', 'Bài học đã kiểm chứng'),
        (root / 'learning-guidance.json', 'Guidance mới cho batch tiếp theo'),
        (root / 'learning-report.json', 'Các sự kiện cải tiến đã ghi'),
        (root / 'learning-audit.json', 'Kiểm tính toàn vẹn hồ sơ cải tiến'),
        (root / 'learning/evidence/script-label-review.md', 'Kiểm cách gọi tổng tiền và chênh lệch'),
        (root / 'learning/evidence/render-graphic-loss-r03-review.md', 'Lỗi crop và chữ đè ở r03'),
        (root / 'learning/evidence/render-graphic-visibility-r04-review.md', 'Kiểm lại hai frame đã sửa ở r04'),
        (folder / 'repair-receipt.json', 'Biên nhận sửa chọn lọc, giữ take và timing'),
    ]
    # Include retained review/evidence records without inventing a review verdict.
    for base in [folder / 'review', root / 'review', root / 'learning']:
        if base.is_dir():
            candidates += [(path, path.name) for path in sorted(base.glob('*')) if path.suffix.lower() in {'.json', '.md', '.txt'}]
    candidates += [(path, path.name) for path in sorted((folder / 'qa').glob('*'))
                   if path.suffix.lower() in {'.json', '.md', '.txt'}]
    candidates += [(path, path.name) for path in sorted(folder.glob('*review*'))
                   if path.suffix.lower() in {'.json', '.md', '.txt'}]
    seen, links = set(), []
    for path, label in candidates:
        link = file_link(root, path, label)
        if link and link['file'] not in seen:
            seen.add(link['file'])
            links.append(link)
    sheets = [file_link(root, path, path.name) for path in sorted((folder / 'qa').glob('*.jpg'))
              if path.name.startswith(('full-duration-', 'keyframes-', 'spatial-'))]
    research = [{**source, 'url': external_url(source.get('url'))} for source in content.get('researchSources', [])]
    script_file = folder / 'script.txt'
    script = script_file.read_text(encoding='utf-8-sig') if script_file.is_file() else '\n\n'.join(s.get('text', '') for s in content.get('sections', []))
    payload = {'schema': 'reference-video-production-review/1', 'title': content.get('title', data.get('title', 'Video thử quy trình mới')),
        'revision': revision.relative_to(root).as_posix(), 'direction': direction,
        'userAcceptance': 'pending user feedback', 'pendingFiles': pending,
        'video': local_link(root, media), 'videoSHA256': media_sha,
        'poster': local_link(root, folder / 'poster.jpg'), 'fps': fps,
        'frames': data.get('frames'), 'seconds': data['frames'] / fps if data else None,
        'editorialAngle': content.get('editorialAngle'), 'audience': content.get('audience'),
        'hookPromise': content.get('hookPromise'), 'payoff': content.get('payoff'),
        'shots': records, 'script': script, 'researchSources': research,
        'claims': content.get('claims', []), 'qa': qa, 'links': links,
        'qaSheets': sheets, 'framesLinked': frames_found,
        'scope': 'Private review of existing artifacts; timing from saved exact-take frames. Source/storyboard notes are recorded observations, not machine-certified semantic or aesthetic approval.'}
    serialized = json.dumps(payload, ensure_ascii=False).replace('<', '\\u003c').replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
    output = PAGE.replace('__PAYLOAD__', serialized)
    (root / 'index.html').write_text(output, encoding='utf-8')
    (root / 'review.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    checks = {'schema': 'reference-video-production-review-check/1', 'revision': payload['revision'],
        'userAcceptance': payload['userAcceptance'], 'videoReady': bool(payload['video']),
        'shots': len(records), 'exactTimelineFrames': data.get('frames'), 'framesLinked': frames_found,
        'qaFrameCountPass': qa.get('frameCountPass'), 'videoSHA256': media_sha,
        'pendingFiles': pending, 'filesLinked': len(links), 'qaSheets': len(sheets),
        'noRawCloseScriptInPayload': '</script' not in serialized.lower(),
        'scope': 'Saved file consistency and review-page structure only.'}
    (root / 'review-checks.json').write_text(json.dumps(checks, ensure_ascii=False, indent=2), encoding='utf-8')
    return checks


PAGE = r'''<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="icon" href="data:,"><title>TYRANNO · Xem bản dựng</title>
<style>
:root{--ink:#17211e;--muted:#65716d;--line:#dbe2dc;--green:#235f4d;--cream:#f6f7f2}*{box-sizing:border-box}body{margin:0;background:var(--cream);color:var(--ink);font:16px/1.65 system-ui,"Segoe UI",sans-serif}main{max-width:1180px;margin:auto;padding:34px 22px}header{margin-bottom:24px}.brand{letter-spacing:.14em;font-size:12px;color:var(--green)}h1{font-size:clamp(26px,4vw,42px);line-height:1.2;letter-spacing:-.035em;margin:15px 0}h2{font-size:23px;line-height:1.35}h3{font-size:18px;margin:0 0 10px}p{margin:10px 0}.muted{color:var(--muted);font-size:14px}a{color:var(--green);text-underline-offset:3px}button,select{font:inherit}button{cursor:pointer}a:focus-visible,button:focus-visible,select:focus-visible{outline:3px solid #d5a04e;outline-offset:3px}.card{background:white;border:1px solid var(--line);border-radius:12px;padding:22px;margin-bottom:20px}video{display:block;width:100%;max-height:67vh;background:#111;border-radius:6px;margin:14px 0}.meta,.links{display:flex;flex-wrap:wrap;gap:9px 20px}.meta{font-size:13px;color:var(--muted)}.pending{display:inline-block;font-size:13px;background:#fbefcf;border:1px solid #e9d7a7;border-radius:100px;padding:4px 12px;color:#77581d}.links{margin-top:16px;font-size:14px}.tabs{display:flex;flex-wrap:wrap;gap:7px;border-bottom:1px solid var(--line)}.tabs button{background:transparent;border:0;border-bottom:3px solid transparent;padding:11px 14px;color:var(--muted)}.tabs button[aria-selected=true]{color:var(--green);border-bottom-color:var(--green);font-weight:650}.pane{background:white;border:1px solid var(--line);border-top:0;border-radius:0 0 12px 12px;padding:24px}.blocknav{display:flex;flex-wrap:wrap;gap:7px;margin:12px 0 22px}.blocknav button,.seek{background:white;color:var(--green);border:1px solid #c2d0c8;border-radius:6px;padding:6px 9px;font-size:13px}.blocknav button[aria-pressed=true]{background:var(--green);color:white}.heading{display:flex;flex-wrap:wrap;gap:12px;align-items:baseline;justify-content:space-between}.visual{display:grid;grid-template-columns:minmax(0,1fr) minmax(250px,.7fr);gap:20px;margin:18px 0}.visual img{display:block;width:100%;border:1px solid var(--line)}.clause{font-size:19px;line-height:1.65;border-left:3px solid var(--green);padding-left:16px;margin:16px 0}.detail{font-size:14px}.detail strong{display:block;color:var(--muted);font-size:12px;margin-top:12px}.asset{border-top:1px solid var(--line);padding-top:16px;margin-top:18px}.asset p{font-size:14px}code{font:12px/1.5 ui-monospace,monospace;overflow-wrap:anywhere;background:#edf1eb;padding:2px 4px}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f4f6f1;border:1px solid var(--line);padding:16px;font:14px/1.8 ui-monospace,monospace}details{margin:14px 0}summary{cursor:pointer;color:var(--green)}table{width:100%;border-collapse:collapse;font-size:14px}th,td{text-align:left;vertical-align:top;padding:10px;border:1px solid var(--line)}.sheets{display:grid;gap:16px}.sheets img{display:block;width:100%;height:auto;border:1px solid var(--line)}footer{margin-top:24px;font-size:13px;color:var(--muted)}[hidden]{display:none!important}@media(max-width:700px){main{padding:22px 14px}.card,.pane{padding:16px}.visual{grid-template-columns:1fr}.tabs button{padding:9px 10px}video{max-height:45vh}.clause{font-size:17px}}
</style></head><body><main><header><div class="brand">TYRANNO / BẢN XEM THỬ</div><h1 id="title">Đang mở bản dựng</h1><p class="muted" id="brief"></p><span class="pending">Chờ phản hồi người dùng</span></header>
<section class="card"><div class="meta" id="meta"></div><video id="player" controls playsinline preload="metadata"></video><p id="waiting" class="muted" hidden>MP4 revision này đang được chuẩn bị. Trang chưa dùng video revision cũ thay thế.</p><div class="links" id="main-links"></div></section>
<nav class="tabs" aria-label="Nội dung xem bản dựng"><button data-tab="timeline" aria-selected="true">Lời và hình</button><button data-tab="script" aria-selected="false">Kịch bản</button><button data-tab="sources" aria-selected="false">Nguồn và crop</button><button data-tab="qa" aria-selected="false">Kiểm tra</button><button data-tab="files" aria-selected="false">Tệp và cải tiến</button></nav><section id="pane" class="pane" aria-live="polite"></section>
<footer>Đây là trang xem artifact riêng. Ghi chú nguồn và storyboard là hồ sơ đối chiếu; kiểm giải mã, số frame và hash không tự xác nhận hình đẹp, khớp nghĩa, đã nghe âm thanh hoặc người dùng đã duyệt. Giọng Nhật Phong và giao diện ảnh/gallery 3D được giữ theo chỉ đạo.</footer></main>
<script type="application/json" id="review-data">__PAYLOAD__</script><script>
'use strict';const data=JSON.parse(document.getElementById('review-data').textContent),player=document.getElementById('player'),pane=document.getElementById('pane');let active='timeline',selected=0,pendingSeek=null;
const el=(tag,text,cls)=>{const n=document.createElement(tag);if(text!==undefined)n.textContent=text;if(cls)n.className=cls;return n;};
const time=t=>{if(t===null||t===undefined)return '—';const m=Math.floor(t/60),s=t-m*60;return `${String(m).padStart(2,'0')}:${s.toFixed(2).padStart(5,'0')}`;};
function link(label,url){const a=el('a',label);a.href=url;a.target='_blank';a.rel='noopener noreferrer';return a;}
function button(label,fn,cls){const b=el('button',label,cls);b.type='button';b.addEventListener('click',fn);return b;}
function seek(t){if(!data.video)return;const apply=()=>{player.currentTime=t;pendingSeek=null;};if(player.readyState>=1)apply();else{if(pendingSeek)player.removeEventListener('loadedmetadata',pendingSeek);pendingSeek=apply;player.addEventListener('loadedmetadata',apply,{once:true});}history.replaceState(null,'',`#shot=${encodeURIComponent(data.shots[selected]?.id||'')}&t=${t}`);player.scrollIntoView({behavior:'smooth',block:'center'});}
function detail(label,text,parent){if(text===undefined||text===null||text==='')return;const p=el('p',undefined,'detail');p.append(el('strong',label),el('span',typeof text==='object'?JSON.stringify(text):text));parent.append(p);}
function sourceCard(asset){const box=el('section',undefined,'asset');box.append(el('h3',asset.id));detail('Vai trò nguồn',asset.sourceRole,box);detail('Nguồn / quyền sử dụng',`${asset.creator||'Chưa ghi'} · ${asset.license||'Chưa ghi'}`,box);detail('Crop chuẩn hóa [trái, trên, phải, dưới]',asset.crop,box);detail('Focus sau crop [%]',asset.focus,box);detail('Hash ảnh/clip nguồn',asset.sha256,box);detail('Hash bản render/crop',asset.renderSHA256,box);const p=el('p',undefined,'links');if(asset.sourceFile)p.append(link('Tệp nguồn giữ lại',asset.sourceFile));if(asset.renderFile)p.append(link('Bản crop / render',asset.renderFile));if(asset.sourceURL)p.append(link('Trang nguồn',asset.sourceURL));if(asset.licenseURL)p.append(link('Giấy phép',asset.licenseURL));box.append(p);const d=el('details');d.append(el('summary','Quan sát đã lưu về nguồn'),el('pre',JSON.stringify({observed:asset.observed,inspection:asset.inspection},null,2)));box.append(d);return box;}
function render(){document.querySelectorAll('[data-tab]').forEach(b=>b.setAttribute('aria-selected',String(b.dataset.tab===active)));pane.replaceChildren();
 if(active==='script'){pane.append(el('h2','Lời dẫn và hướng khai thác'));detail('Góc khai thác',data.editorialAngle,pane);detail('Người xem hướng tới — giả thuyết biên tập',data.audience,pane);detail('Lời hứa đầu bài',data.hookPromise,pane);detail('Điều chốt lại',data.payoff,pane);pane.append(el('pre',data.script));return;}
 if(active==='sources'){pane.append(el('h2','Nguồn theo từng mạch ý'));const seen=new Set;data.shots.forEach(s=>s.images.forEach(a=>{if(!seen.has(a.id)){seen.add(a.id);pane.append(sourceCard(a));}}));pane.append(el('h2','Nguồn nghiên cứu nội dung'));data.researchSources.forEach(s=>{const box=el('section',undefined,'asset');box.append(el('h3',s.title||s.id));if(s.url)box.append(link(s.url,s.url));const rest={...s};delete rest.url;box.append(el('pre',JSON.stringify(rest,null,2)));pane.append(box);});if(data.claims.length){pane.append(el('h2','Phạm vi các phát biểu'),el('pre',JSON.stringify(data.claims,null,2)));}return;}
 if(active==='qa'){pane.append(el('h2','Bằng chứng kiểm bản xuất'));pane.append(el('p',data.qa.frameCountPass?'Đã có báo cáo kiểm số frame của MP4. Kết quả này chỉ xác nhận tính toàn vẹn kỹ thuật.':'Báo cáo kiểm MP4 của revision này chưa hoàn tất.','muted'));pane.append(el('pre',JSON.stringify(data.qa,null,2)));const sheets=el('div',undefined,'sheets');data.qaSheets.forEach(s=>{const a=link(s.label,s.file),img=el('img');img.src=s.file;img.alt=s.label;img.loading='lazy';a.append(img);sheets.append(a);});pane.append(sheets);return;}
 if(active==='files'){pane.append(el('h2','Tệp, biên nhận và vòng cải tiến'));pane.append(el('p','Phản hồi, lần sửa và kết quả kiểm lại được ghi riêng. Guidance được pin vào batch không tự thay preset hoặc đánh dấu video đã được duyệt.','muted'));data.links.forEach(row=>{const p=el('p');p.append(link(row.label,row.file));pane.append(p);});detail('Hash MP4 revision này',data.videoSHA256,pane);if(data.pendingFiles.length)pane.append(el('pre',JSON.stringify({pending:data.pendingFiles},null,2)));return;}
 pane.append(el('h2','Đối chiếu từng mệnh đề'));if(!data.shots.length){pane.append(el('p','Timeline của take mới đang được chuẩn bị; chưa ước lượng thời gian từ số từ.','muted'));return;}
 const nav=el('div',undefined,'blocknav');data.shots.forEach((s,i)=>{const b=button(`${i+1} · ${time(s.start)}`,()=>{selected=i;render();});b.setAttribute('aria-pressed',String(i===selected));nav.append(b);});pane.append(nav);const shot=data.shots[selected],head=el('div',undefined,'heading');head.append(el('h3',`${selected+1}. ${shot.id} · ${time(shot.start)}–${time(shot.end)}`),button('Đến đoạn này',()=>seek(shot.start),'seek'));pane.append(head,el('p',shot.clause,'clause'));const visual=el('div',undefined,'visual'),frame=el('div');if(shot.frame){const a=link('Mở frame gốc',shot.frame.file),img=el('img');img.src=shot.frame.file;img.alt=`Frame ${shot.frame.index}, ${time(shot.frame.time)}, cảnh ${shot.id}`;img.loading='lazy';a.append(img);frame.append(a,el('p',`Frame ${shot.frame.index} · ${time(shot.frame.time)} · ảnh chọn mẫu giữa cảnh, không thay lượt xem chuyển động.`, 'muted'));}else frame.append(el('p','Frame QA của cảnh này đang chờ bản xuất.','muted'));const notes=el('div');detail('Bố cục / vai trò hình',`${shot.layout} · ${shot.mediaRole}`,notes);detail('Chữ nhấn / nội dung trên hình',shot.headline||shot.body,notes);detail('Nhãn nguồn trên hình',shot.sourceNote,notes);detail('Điều cần nhìn thấy',shot.needToSee,notes);detail('Hình hỗ trợ điều gì',shot.supports,notes);detail('Giới hạn',shot.limits,notes);detail('Mốc frame theo take thật',`${shot.startFrame} → ${shot.endFrame} @ ${data.fps} fps`,notes);if(shot.sourceIds.length)detail('Nguồn nghiên cứu',shot.sourceIds.join(', '),notes);visual.append(frame,notes);pane.append(visual);shot.images.forEach(a=>pane.append(sourceCard(a)));const review=el('details');review.append(el('summary','Ghi chú storyboard đã lưu'),el('pre',JSON.stringify(shot.review,null,2)));pane.append(review);const next=el('p',undefined,'links');if(selected>0)next.append(button('← Đoạn trước',()=>{selected--;render();},'seek'));if(selected<data.shots.length-1)next.append(button('Đoạn sau →',()=>{selected++;render();},'seek'));pane.append(next);
}
document.title=`TYRANNO · ${data.title}`;document.getElementById('title').textContent=data.title;document.getElementById('brief').textContent=data.editorialAngle||'Bản thử của quy trình sản xuất đã nâng cấp.';const meta=document.getElementById('meta');meta.append(el('span',`Revision ${data.revision} / ${data.direction}`),el('span',data.seconds===null?'Timing đang chuẩn bị':`${data.seconds.toFixed(2)} giây · ${data.fps} fps`),el('span',`${data.shots.length} mệnh đề / cảnh`));if(data.video){player.src=data.video;if(data.poster)player.poster=data.poster;document.getElementById('main-links').append(link('Mở / tải MP4',data.video));}else{player.hidden=true;document.getElementById('waiting').hidden=false;}data.links.filter(x=>/Lời dẫn|QA kỹ thuật|Nguồn nghiên cứu chủ đề|Lịch sử cải tiến/.test(x.label)).forEach(x=>document.getElementById('main-links').append(link(x.label,x.file)));document.querySelectorAll('[data-tab]').forEach(b=>b.addEventListener('click',()=>{active=b.dataset.tab;render();}));render();
</script></body></html>'''


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--batch', type=Path, required=True, help='Revision directory relative to --root, e.g. r03')
    parser.add_argument('--manifest', type=Path, help='Manifest relative to --root; default is the retained revision manifest')
    parser.add_argument('--direction', choices=['long', 'hidden'], default='long')
    parser.add_argument('--allow-pending', action='store_true')
    args = parser.parse_args()
    print(json.dumps(build(args.root, args.batch, args.manifest, args.direction, args.allow_pending), ensure_ascii=False))
