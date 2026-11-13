"""Build a local reference-study viewer without duplicating the source media.

Reports and captions are embedded, so the HTML also opens from the filesystem.
This private research index does not alter any video composition or application UI.
"""
from __future__ import annotations

import argparse
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import quote, unquote, urlparse

import markdown


REFERENCE_IDS = ['w3z43Hlzq3c', '1OGwWLvasIk', 'gNznfzAUiLw', '3JUxxp2sIDM']


def read_json(path: Path, default=None):
    return json.loads(path.read_text(encoding='utf-8')) if path.exists() else default


def safe_link(value: str) -> bool:
    value = html.unescape(value).strip()
    parsed = urlparse(value)
    return bool(value) and not value.startswith('//') and parsed.scheme.lower() in ('', 'http', 'https')


class CleanHTML(HTMLParser):
    """Allow only document formatting and safe links in generated report HTML."""
    allowed = {'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'ul', 'ol', 'li', 'em',
               'strong', 'code', 'pre', 'table', 'thead', 'tbody', 'tr', 'th', 'td',
               'blockquote', 'br', 'hr', 'a', 'del'}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.output = []

    def handle_starttag(self, tag, attrs):
        if tag not in self.allowed:
            return
        attributes = dict(attrs)
        kept = ''
        if tag == 'a':
            href = attributes.get('href', '')
            if safe_link(href):
                kept = f' href="{html.escape(href, quote=True)}" target="_blank" rel="noopener noreferrer"'
        self.output.append(f'<{tag}{kept}>')

    def handle_endtag(self, tag):
        if tag in self.allowed and tag not in ('br', 'hr'):
            self.output.append(f'</{tag}>')

    def handle_data(self, value):
        self.output.append(html.escape(value))


def rendered_markdown(value: str) -> str:
    # Escape raw HTML before Markdown conversion; sanitize generated link attributes too.
    candidate = markdown.markdown(html.escape(value, quote=False), extensions=['tables', 'fenced_code'])
    parser = CleanHTML()
    parser.feed(candidate)
    return ''.join(parser.output)


def report_file(folder: Path, names: list[str]):
    return next((folder / name for name in names if (folder / name).is_file()), None)


LABELS = {
    'narrated_idea': 'Ý đang kể', 'meaning': 'Ý đang kể',
    'scriptFunction': 'Vai trò trong kịch bản', 'script_function': 'Vai trò trong kịch bản',
    'visibleEvidence': 'Hình đã đối chiếu', 'visible_evidence': 'Hình đã đối chiếu',
    'semantic_match_and_limits': 'Quan hệ lời–hình và giới hạn',
    'attentionInference': 'Cách giữ chú ý — suy luận', 'attention_inference': 'Cách giữ chú ý — suy luận',
    'teaching': 'Bài học', 'lesson': 'Bài học', 'transition': 'Chuyển ý', 'limit': 'Giới hạn',
}


def time_label(seconds) -> str:
    seconds = max(0, int(float(seconds)))
    return f'{seconds // 60:02}:{seconds % 60:02}'


def block_notes(block: dict) -> str:
    if block.get('notes_markdown'):
        return rendered_markdown(block['notes_markdown'])
    sections = []
    title = block.get('title') or block.get('summary')
    if title:
        sections.append(f'### {title}')
    beats = block.get('beats') or block.get('semantic_beats') or []
    for beat in beats:
        sections.append(f"#### {time_label(beat.get('start', block.get('start', 0)))}–{time_label(beat.get('end', block.get('end', 0)))}")
        for key, label in LABELS.items():
            value = beat.get(key)
            if value:
                sections.append(f'**{label}:** {value}')
    for key in ('reusableLesson', 'reusable_lesson', 'lesson', 'teaching'):
        if block.get(key):
            sections.append(f'**Bài học của đoạn:** {block[key]}')
    if not sections:
        return '<p class="muted">Ghi chú phân tích của đoạn đang được hoàn thiện.</p>'
    return rendered_markdown('\n\n'.join(sections))


def relative_url(root: Path, path: Path) -> str:
    return quote(path.relative_to(root).as_posix(), safe='/')


def build(root: Path, allow_incomplete: bool = False):
    references = []
    for video_id in REFERENCE_IDS:
        folder = root / video_id
        meta = read_json(folder / 'metadata.json')
        if not meta:
            raise FileNotFoundError(folder / 'metadata.json')
        study = read_json(folder / 'study-blocks.json', [])
        analysis = read_json(folder / 'analysis.json', {})
        analysis_blocks = analysis.get('blocks', []) if isinstance(analysis, dict) else analysis
        by_index = {b.get('index', i): b for i, b in enumerate(analysis_blocks)}
        analysis_path = report_file(folder, ['analysis.md'])
        pattern_path = report_file(folder, ['script-pattern.md', 'scriptpattern.md'])
        analysis_text = analysis_path.read_text(encoding='utf-8') if analysis_path else '# Phân tích\n\nBản phân tích chi tiết đang được hoàn thiện.'
        pattern_text = pattern_path.read_text(encoding='utf-8') if pattern_path else '# Cách viết kịch bản\n\nBản ghi cách viết đang được hoàn thiện.'
        blocks = []
        for i, block in enumerate(study):
            reviewed = by_index.get(block.get('index', i), {})
            blocks.append({
                'index': block.get('index', i), 'start': block['start'], 'end': block['end'],
                'title': reviewed.get('title', ''), 'notes': block_notes(reviewed),
                'transcript': block.get('transcript', []),
                'sheets': [relative_url(root, folder / name) for name in block.get('sheets', [])],
                'frames': block.get('frames', []),
            })
        references.append({
            'id': video_id, 'title': meta.get('title', video_id), 'channel': meta.get('channel', ''),
            'duration': meta['duration'], 'source': f'https://www.youtube.com/watch?v={video_id}',
            'media': relative_url(root, folder / 'reference.mp4'),
            'analysis': rendered_markdown(analysis_text), 'pattern': rendered_markdown(pattern_text),
            'analysisFile': relative_url(root, analysis_path) if analysis_path else None,
            'patternFile': relative_url(root, pattern_path) if pattern_path else None,
            'transcriptFile': relative_url(root, folder / 'transcript.txt'),
            'metadataFile': relative_url(root, folder / 'metadata.json'),
            'receiptFile': relative_url(root, folder / 'media-receipt.json'),
            'captionsFile': relative_url(root, folder / 'captions.json3'),
            'chapters': meta.get('chapters') or [], 'blocks': blocks,
            'analysisReady': bool(analysis_path), 'patternReady': bool(pattern_path),
            'sampledFrames': sum(len(b['frames']) for b in blocks),
            'analysisBlocks': analysis_blocks,
        })
    playbook_path = root / 'PLAYBOOK.md'
    playbook_text = playbook_path.read_text(encoding='utf-8') if playbook_path.exists() else '# Bài học chung\n\nBản tổng hợp đang được hoàn thiện.'
    public_references = [{k: v for k, v in ref.items() if k != 'analysisBlocks'} for ref in references]
    payload = json.dumps({'references': public_references, 'playbook': rendered_markdown(playbook_text),
        'playbookFile': relative_url(root, playbook_path) if playbook_path.exists() else None,
        'readmeFile': 'README.md' if (root / 'README.md').exists() else None}, ensure_ascii=False, separators=(',', ':'))
    payload = payload.replace('&', '\\u0026').replace('<', '\\u003c').replace('>', '\\u003e').replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
    output = PAGE.replace('__DATA__', payload)
    target = root / 'index.html'
    checks = validate(root, references, output)
    checks['require_complete_reports'] = not allow_incomplete
    (root / 'library-checks.json').write_text(json.dumps(checks, ensure_ascii=False, indent=2), encoding='utf-8')
    if checks['missing_local_files'] or checks['coverage_errors'] or (not allow_incomplete and checks['incomplete_report_errors']):
        raise RuntimeError('Viewer has missing files, timeline gaps or incomplete reports; see library-checks.json. Use --allow-incomplete only for a working preview.')
    target.write_text(output, encoding='utf-8')
    print(json.dumps({'html': str(target.resolve()), **checks}, ensure_ascii=False))


def validate(root: Path, references: list[dict], output: str):
    missing, coverage_errors, incomplete = [], [], []
    analysis_counts = {}
    for ref in references:
        links = [ref[key] for key in ('media', 'analysisFile', 'patternFile', 'transcriptFile', 'metadataFile', 'receiptFile', 'captionsFile') if ref.get(key)]
        links += [x for block in ref['blocks'] for x in block['sheets']]
        missing += [link for link in links if not (root / unquote(link)).is_file()]
        cursor = 0
        for block in ref['blocks']:
            if block['start'] != cursor or block['end'] <= block['start']:
                coverage_errors.append({'id': ref['id'], 'at': block['start'], 'expected': cursor})
            cursor = block['end']
        if cursor != ref['duration']:
            coverage_errors.append({'id': ref['id'], 'end': cursor, 'expected': ref['duration']})
        analysis_counts[ref['id']] = {'expected': len(ref['blocks']), 'actual': len(ref['analysisBlocks'])}
        if not ref['analysisReady'] or not ref['patternReady']:
            incomplete.append({'id': ref['id'], 'analysis_md': ref['analysisReady'], 'script_pattern': ref['patternReady']})
        if len(ref['analysisBlocks']) != len(ref['blocks']):
            incomplete.append({'id': ref['id'], 'analysis_block_count': len(ref['analysisBlocks']), 'expected': len(ref['blocks'])})
        cursor = 0
        for i, block in enumerate(ref['analysisBlocks']):
            if block.get('start') != cursor or block.get('end', 0) <= block.get('start', 0):
                incomplete.append({'id': ref['id'], 'analysis_block': i, 'start': block.get('start'), 'expected': cursor})
            cursor = block.get('end')
        if cursor != ref['duration']:
            incomplete.append({'id': ref['id'], 'analysis_end': cursor, 'expected': ref['duration']})
    return {
        'reference_count': len(references), 'total_duration_seconds': sum(x['duration'] for x in references),
        'contiguous_blocks': sum(len(x['blocks']) for x in references),
        'contact_sheets': sum(len(b['sheets']) for x in references for b in x['blocks']),
        'sampled_frames': sum(x['sampledFrames'] for x in references),
        'completed_analysis_reports': sum(x['analysisReady'] for x in references),
        'completed_script_patterns': sum(x['patternReady'] for x in references),
        'analysis_block_counts': analysis_counts, 'incomplete_report_errors': incomplete,
        'missing_local_files': missing, 'coverage_errors': coverage_errors,
        'report_html_allowlist': True, 'embedded_payload_has_no_raw_close_script': '</script' not in output.split('<script id="study-data" type="application/json">', 1)[1].split('</script>', 1)[0].lower(),
        'scope': 'File references, continuous interval coverage and safe HTML structure only; not audiovisual or aesthetic acceptance.',
    }


PAGE = r'''<!doctype html>
<html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Hồ sơ học mẫu · 4 video Lóng</title><link rel="icon" href="data:,">
<style>
:root{color-scheme:light;--ink:#17202c;--muted:#626e7b;--line:#dce2e7;--accent:#265f58;--paper:#fff;--canvas:#f4f6f5}
*{box-sizing:border-box}body{margin:0;background:var(--canvas);color:var(--ink);font:16px/1.65 system-ui,-apple-system,"Segoe UI",sans-serif}button,select{font:inherit}button,a,select{touch-action:manipulation}a{color:var(--accent);text-underline-offset:3px}button{cursor:pointer}button:focus-visible,a:focus-visible,select:focus-visible{outline:3px solid #e1a458;outline-offset:3px}header{background:#182a2a;color:#f3f7f4;padding:30px 24px}header>div,main{max-width:1180px;margin:auto}h1{font-size:clamp(24px,3vw,34px);line-height:1.2;margin:0 0 10px;letter-spacing:-.025em}header p{margin:0;color:#c6d4d0}.eyebrow{font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:#a6c9bc;margin-bottom:10px}main{padding:24px}.selector{background:var(--paper);border:1px solid var(--line);border-radius:12px;padding:18px;margin-bottom:20px}.selector label{display:block;font-size:13px;color:var(--muted);margin-bottom:6px}select{width:100%;padding:12px;background:white;color:var(--ink);border:1px solid #aab7b4;border-radius:7px}h2{font-size:24px;line-height:1.35;margin:0 0 8px}.muted{color:var(--muted);font-size:14px}.player-card{background:var(--paper);border:1px solid var(--line);border-radius:12px;padding:20px}video{display:block;width:100%;max-height:58vh;background:#111;margin:16px auto 12px;border-radius:6px}.links{display:flex;gap:12px 20px;flex-wrap:wrap;font-size:14px}.tabs{display:flex;gap:5px;flex-wrap:wrap;margin:22px 0 0;border-bottom:1px solid var(--line)}.tabs button{background:none;border:0;border-bottom:3px solid transparent;padding:12px 16px;color:var(--muted)}.tabs button[aria-selected="true"]{color:var(--accent);border-bottom-color:var(--accent);font-weight:650}.pane{background:var(--paper);border:1px solid var(--line);border-top:0;padding:26px;border-radius:0 0 12px 12px;min-height:200px}.report{max-width:900px;margin:auto;overflow-wrap:anywhere}.report h1{font-size:28px;margin:10px 0 16px}.report h2{font-size:22px;margin:32px 0 14px}.report h3{font-size:19px;margin:26px 0 10px}.report h4{font-size:16px;margin:24px 0 8px}.report p{margin:12px 0}.report li{margin:8px 0}.report table{width:100%;border-collapse:collapse;display:block;overflow:auto;font-size:14px;margin:20px 0}.report th,.report td{border:1px solid var(--line);padding:10px;text-align:left;vertical-align:top}.report blockquote{border-left:3px solid #afc6bc;margin:18px 0;padding-left:18px;color:var(--muted)}.report code{font-size:.86em;background:#edf2ee;padding:2px 4px;border-radius:3px}.report pre{overflow:auto;background:#edf2ee;padding:14px}.report pre code{padding:0}.scope{padding:14px 0;color:var(--muted);font-size:13px}.blocknav,.chapters{display:flex;flex-wrap:wrap;gap:7px;margin:14px 0 22px}.blocknav button,.chapters button,.seek{border:1px solid #c8d3cf;border-radius:7px;background:white;color:var(--accent);padding:7px 10px;font-size:13px}.blocknav button[aria-pressed="true"]{background:var(--accent);color:white;border-color:var(--accent)}.segment-heading{display:flex;gap:14px;align-items:baseline;justify-content:space-between;flex-wrap:wrap;border-top:1px solid var(--line);padding-top:22px}.segment-heading h3{margin:0}.caption{border-top:1px solid var(--line);padding-top:18px;margin-top:24px}.caption summary{cursor:pointer;font-weight:600}.caption-list{max-height:380px;overflow:auto;padding:10px 8px 10px 0}.caption-row{display:grid;grid-template-columns:64px 1fr;gap:12px;padding:6px;border-radius:5px;font-size:14px}.caption-row button{align-self:start;border:0;background:#eef3f0;color:var(--accent);border-radius:4px;padding:2px 4px;font:12px/1.8 ui-monospace,monospace}.sheets{display:grid;gap:18px;margin-top:18px}.sheets img{display:block;width:100%;height:auto;background:#17191e;border:1px solid var(--line)}.sheets figure{margin:0}.sheets figcaption{font-size:13px;color:var(--muted);margin:5px 0}footer{padding:20px 0 0;font-size:13px;color:var(--muted)}[hidden]{display:none!important}.source-grid{display:grid;gap:14px}.source-grid p{margin:0}.small-title{font-size:14px;font-weight:650;margin-top:18px}.count{font-variant-numeric:tabular-nums}body.no-js .selector,body.no-js .player-card,body.no-js .tabs,body.no-js .pane{display:none}
@media(max-width:640px){main{padding:14px}.player-card,.selector,.pane{padding:16px}header{padding:25px 18px}h2{font-size:20px}.tabs button{padding:10px}.caption-row{grid-template-columns:58px 1fr;gap:8px}.report h1{font-size:23px}video{max-height:45vh}.links{gap:8px 15px}}
</style></head><body class="no-js">
<header><div><div class="eyebrow">Hồ sơ nghiên cứu · 13/11/2026</div><h1>Học cách kể, đối chiếu từng đoạn</h1><p>4 video Lóng · 77 phút 10 giây · Bản tải, lời thoại, hình đối chiếu và ghi chú kịch bản.</p></div></header>
<main><noscript><p>Trang tra cứu cần JavaScript để chuyển video và mốc thời gian. Các bản MP4, transcript và báo cáo Markdown vẫn có trong từng thư mục video.</p></noscript>
<div class="selector"><label for="reference">Chọn video tham khảo</label><select id="reference" aria-label="Chọn video tham khảo"></select></div>
<section class="player-card" aria-labelledby="video-title"><h2 id="video-title"></h2><div id="video-info" class="muted count"></div><video id="player" controls preload="metadata" playsinline></video><div id="media-links" class="links"></div><div id="chapter-wrap" hidden><div class="small-title">Chương do nguồn cung cấp</div><div id="chapter-links" class="chapters"></div></div></section>
<div class="tabs" role="tablist" aria-label="Nội dung nghiên cứu"><button type="button" role="tab" aria-selected="true" data-tab="analysis">Phân tích</button><button type="button" role="tab" aria-selected="false" data-tab="pattern">Cách viết</button><button type="button" role="tab" aria-selected="false" data-tab="timeline">Từng đoạn</button><button type="button" role="tab" aria-selected="false" data-tab="playbook">Bài học chung</button><button type="button" role="tab" aria-selected="false" data-tab="sources">Tệp nguồn</button></div>
<section id="pane" class="pane" aria-live="polite"></section>
<div class="scope">Phạm vi: đọc toàn caption và đối chiếu các khung hình chọn mẫu trên toàn timeline. Caption tự động có thể sai; việc này không đồng nghĩa đã xem/nghe liên tục hoặc xác nhận mọi dữ kiện của nguồn. Bấm mốc để tự phát lại đoạn gốc.</div>
<footer>Thư viện nghiên cứu riêng. Tệp media được giữ để phân tích tham khảo; quyền tái sử dụng hình/âm thanh trong sản phẩm mới chưa được xác lập.</footer>
</main>
<script id="study-data" type="application/json">__DATA__</script>
<script>
'use strict';
document.body.classList.remove('no-js');
const library=JSON.parse(document.getElementById('study-data').textContent),refs=library.references;
const selector=document.getElementById('reference'),player=document.getElementById('player'),pane=document.getElementById('pane');
let current=0,activeTab='analysis',currentBlock=0,pendingSeek=null;
const tlabel=t=>`${String(Math.floor(t/60)).padStart(2,'0')}:${String(Math.floor(t%60)).padStart(2,'0')}`;
function el(tag,text,className){const node=document.createElement(tag);if(text!==undefined)node.textContent=text;if(className)node.className=className;return node;}
function link(text,url,download=false){const a=el('a',text);a.href=url;if(download)a.download='';else{a.target='_blank';a.rel='noopener noreferrer';}return a;}
function seek(t){t=Number(t);if(!Number.isFinite(t))return;const ref=refs[current];t=Math.min(Math.max(0,t),ref.duration);if(pendingSeek)player.removeEventListener('loadedmetadata',pendingSeek);const apply=()=>{player.currentTime=t;pendingSeek=null;};if(player.readyState>=1)apply();else{pendingSeek=apply;player.addEventListener('loadedmetadata',apply,{once:true});}history.replaceState(null,'',`#${ref.id}&t=${t}`);player.scrollIntoView({behavior:'smooth',block:'center'});}
function button(text,onClick,className){const b=el('button',text,className);b.type='button';b.addEventListener('click',onClick);return b;}
function showVideo(index,fromHash=false){player.pause();if(pendingSeek){player.removeEventListener('loadedmetadata',pendingSeek);pendingSeek=null;}current=index;currentBlock=0;selector.value=String(index);const ref=refs[index];document.getElementById('video-title').textContent=ref.title;document.getElementById('video-info').textContent=`${ref.channel} · ${tlabel(ref.duration)} · ${ref.blocks.length} khoảng liên tiếp · ${ref.sampledFrames} khung hình chọn mẫu`;player.src=ref.media;player.load();const links=document.getElementById('media-links');links.replaceChildren(link('Tải / mở MP4',ref.media,true),link('Video gốc trên YouTube',ref.source));const chapters=document.getElementById('chapter-links');chapters.replaceChildren();ref.chapters.forEach(ch=>chapters.append(button(`${tlabel(ch.start_time)} · ${ch.title}`,()=>seek(ch.start_time))));document.getElementById('chapter-wrap').hidden=!ref.chapters.length;if(!fromHash)history.replaceState(null,'',`#${ref.id}`);render();}
function render(){const ref=refs[current];document.querySelectorAll('[data-tab]').forEach(b=>b.setAttribute('aria-selected',String(b.dataset.tab===activeTab)));pane.replaceChildren();
 if(activeTab==='playbook'){const article=el('article',undefined,'report');article.innerHTML=library.playbook;pane.append(article);const links=el('p',undefined,'links');if(library.playbookFile)links.append(link('Mở bài học chung dạng Markdown',library.playbookFile));if(library.readmeFile)links.append(link('Hướng dẫn và phạm vi nghiên cứu',library.readmeFile));pane.append(links);return;}
 if(activeTab==='analysis'||activeTab==='pattern'){const article=el('article',undefined,'report');article.innerHTML=ref[activeTab];pane.append(article);const path=activeTab==='analysis'?ref.analysisFile:ref.patternFile;if(path){const p=el('p',undefined,'muted');p.append(link('Mở bản Markdown',path));pane.append(p);}return;}
 if(activeTab==='sources'){const box=el('div',undefined,'source-grid');box.append(el('h3','Các tệp đã lưu'));[['MP4 có hình và tiếng','media'],['Lời thoại có mốc thời gian','transcriptFile'],['Caption JSON3 gốc','captionsFile'],['Metadata YouTube','metadataFile'],['Biên nhận tải, SHA-256 và decode','receiptFile']].forEach(([title,key])=>{const p=el('p');p.append(link(title,ref[key],key==='media'));box.append(p);});box.append(el('p','Nguồn dữ kiện của video chưa được kiểm chứng độc lập. Ảnh chụp màn hình và thông tin quảng cáo được dùng để phân tích cách kể, không phải xác nhận chất lượng sản phẩm hoặc tính đúng của mọi lời nói.','muted'));pane.append(box);return;}
 const nav=el('div',undefined,'blocknav');nav.setAttribute('aria-label','Các khoảng liên tiếp');ref.blocks.forEach((b,i)=>{const btn=button(`${tlabel(b.start)}–${tlabel(b.end)}`,()=>{currentBlock=i;render();});btn.setAttribute('aria-pressed',String(i===currentBlock));nav.append(btn);});pane.append(el('p','Chọn một khoảng để xem ghi chú, lời thoại và toàn bộ trang ảnh đối chiếu của khoảng đó.','muted'),nav);
 const block=ref.blocks[currentBlock];if(!block){pane.append(el('p','Chưa có timeline.'));return;}
 const heading=el('div',undefined,'segment-heading');heading.append(el('h3',`${tlabel(block.start)}–${tlabel(block.end)}`),button('Đến mốc này trong video',()=>seek(block.start),'seek'));pane.append(heading);
 const notes=el('article',undefined,'report');notes.innerHTML=block.notes;pane.append(notes);
 const transcript=el('details',undefined,'caption');transcript.open=true;transcript.append(el('summary',`Lời thoại · ${block.transcript.length} dòng caption`));const rows=el('div',undefined,'caption-list');block.transcript.forEach(row=>{const p=el('div',undefined,'caption-row');p.append(button(tlabel(row.start),()=>seek(row.start)),el('span',row.text));rows.append(p);});transcript.append(rows);pane.append(transcript);
 const sheets=el('div',undefined,'sheets');block.sheets.forEach((src,i)=>{const fig=el('figure'),a=link('',src),img=el('img');img.src=src;img.alt=`Ảnh đối chiếu ${ref.title}, khoảng ${tlabel(block.start)}–${tlabel(block.end)}, trang ${i+1}`;img.loading='lazy';a.append(img);fig.append(a,el('figcaption',`Trang ${i+1}/${block.sheets.length} · Bấm ảnh để mở kích thước đầy đủ.`));sheets.append(fig);});pane.append(sheets);
 const footer=el('div',undefined,'links');if(currentBlock>0)footer.append(button('← Đoạn trước',()=>{currentBlock--;render();},'seek'));if(currentBlock<ref.blocks.length-1)footer.append(button('Đoạn sau →',()=>{currentBlock++;render();},'seek'));pane.append(footer);
}
refs.forEach((ref,i)=>{const option=el('option',`${i+1}. ${ref.title} (${tlabel(ref.duration)})`);option.value=String(i);selector.append(option);});
selector.addEventListener('change',()=>showVideo(Number(selector.value)));
document.querySelectorAll('[data-tab]').forEach(b=>b.addEventListener('click',()=>{activeTab=b.dataset.tab;render();}));
function readHash(){const [id,param]=location.hash.slice(1).split('&t=');const i=refs.findIndex(r=>r.id===id);showVideo(i<0?0:i,true);if(param!==undefined)seek(Number(param));}
readHash();window.addEventListener('hashchange',readHash);
</script></body></html>'''


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--allow-incomplete', action='store_true', help='Build a working preview while reports are still being authored; final builds require all four reports and full analysis-block coverage.')
    args = parser.parse_args()
    build(args.root.resolve(), allow_incomplete=args.allow_incomplete)
