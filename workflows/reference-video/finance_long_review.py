"""Build a local paired-film viewer with exact chapter and beat navigation."""
from pathlib import Path
import argparse, html, json
from finance_long import BATCH,load

def build(revision='r01'):
    p=load(BATCH/'plan.json');esc=html.escape
    chapters=''.join(f'<button data-time="{c["from"]/30}"><span>{int(c["from"]/1800):02}:{int(c["from"]/30)%60:02}</span>{esc(c["title"])}</button>' for c in p['chapters'])
    transcript=''.join(f'<article><button data-time="{s["from"]/30}">{esc(s["headline"])}</button><p>{esc(s["text"])}</p></article>' for s in p['segments'])
    title=esc(p['title']);minutes=int(p['durationFrames']/1800);seconds=round(p['durationFrames']/30)%60
    page=f'''<!doctype html><html lang="vi"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title>
<style>*{{box-sizing:border-box}}body{{margin:0;background:#f5f0e5;color:#282632;font:16px/1.6 Arial,sans-serif}}main{{max-width:1360px;margin:auto;padding:30px}}h1{{font-size:32px;line-height:1.2;max-width:850px}}.eyebrow{{color:#417669;font-size:14px;font-weight:bold}}.controls{{display:flex;gap:12px;margin:20px 0}}button,a.download{{cursor:pointer;border:1px solid #d3caba;border-radius:8px;background:#fffaf1;color:#282632;padding:12px 18px;text-align:left;font:inherit}}button.active{{background:#3c7568;color:white;border-color:#3c7568}}video{{width:100%;aspect-ratio:16/9;background:#24232b;border-radius:12px}}.layout{{display:grid;grid-template-columns:minmax(0,1fr) 280px;gap:25px}}nav{{display:flex;flex-direction:column;gap:8px}}nav button{{font-size:14px;line-height:1.4}}nav span{{display:block;font-weight:bold;color:#a46d42}}a{{color:#326d60}}article{{border-top:1px solid #d8d0c3;padding:18px 0}}article button{{padding:0;border:0;background:transparent;color:#326d60;font-weight:bold}}article p{{max-width:950px;margin:8px 0}}summary{{cursor:pointer;margin:24px 0;font-size:20px}}.muted{{color:#77716b}}@media(max-width:900px){{.layout{{grid-template-columns:1fr}}nav{{display:grid;grid-template-columns:1fr 1fr}}}}</style>
<main><div class="eyebrow">HAI PHONG CÁCH · {minutes}:{seconds:02} MỖI BẢN</div><h1>{title}</h1><p>Cùng một lời kể, hai cách minh họa. Chuyển phong cách để xem tiếp tại cùng thời điểm.</p>
<div class="controls"><button class="active" data-style="comic">Comic biểu cảm</button><button data-style="flow">Tối giản chuyển động</button></div>
<div class="layout"><section><video controls playsinline preload="metadata" poster="poster-comic.jpg" src="{revision}/comic/final.mp4"></video><p><a id="download" href="{revision}/comic/final.mp4" download>Tải video đang chọn</a></p></section><nav aria-label="Chương">{chapters}</nav></div>
<p class="muted">Minh, Lan và các số tiền đều là ví dụ giả định. Hãy điều chỉnh theo hoàn cảnh của bạn.</p><details><summary>Kịch bản và mốc xem</summary>{transcript}</details><p class="muted">Tham khảo phương pháp: <a href="https://www.consumerfinance.gov/an-essential-guide-to-building-an-emergency-fund/" target="_blank" rel="noopener">CFPB — quỹ dự phòng và dòng tiền</a> · <a href="https://www.consumerfinance.gov/consumer-tools/educator-tools/your-money-your-goals/toolkit/" target="_blank" rel="noopener">CFPB — công cụ lập kế hoạch</a></p></main>
<script>const v=document.querySelector('video');const rev={json.dumps(revision)};document.querySelectorAll('[data-style]').forEach(b=>b.onclick=()=>{{const t=v.currentTime,playing=!v.paused;v.poster='poster-'+b.dataset.style+'.jpg';v.src=rev+'/'+b.dataset.style+'/final.mp4';document.querySelector('#download').href=v.src;v.addEventListener('loadedmetadata',()=>{{v.currentTime=t;if(playing)v.play()}},{{once:true}});document.querySelectorAll('[data-style]').forEach(x=>x.classList.toggle('active',x===b))}});document.querySelectorAll('[data-time]').forEach(b=>b.onclick=()=>{{v.currentTime=Number(b.dataset.time);v.play();v.scrollIntoView({{behavior:'smooth',block:'center'}})}});</script></html>'''
    (BATCH/'index.html').write_text(page,encoding='utf-8')
    print(BATCH/'index.html')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--revision',default='r01');parser.add_argument('--serve',action='store_true');parser.add_argument('--port',type=int,default=8879)
    args=parser.parse_args();build(args.revision)
    if args.serve:
        from functools import partial
        from http.server import ThreadingHTTPServer
        from serve_reference_study import StudyHandler
        print(f'http://127.0.0.1:{args.port}/',flush=True)
        ThreadingHTTPServer(('127.0.0.1',args.port),partial(StudyHandler,directory=str(BATCH))).serve_forever()
