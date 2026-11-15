"""Local photo-finance viewer with source receipts and temporal proofs."""
import argparse,html,json,shutil
from functools import partial
from http.server import ThreadingHTTPServer
from finance_photo_render import BATCH,load,save
from serve_reference_study import StudyHandler
import finance_long_review as viewer


def build(revision='r01'):
    plan=load(BATCH/'photo-plan.json');save(BATCH/'plan.json',plan)
    viewer.BATCH=BATCH;viewer.build(revision)
    file=BATCH/'index.html';page=file.read_text(encoding='utf-8')
    page=page.replace('data-style="flow"','data-style="clean"').replace('Comic biểu cảm','Ảnh thật · mô phỏng comic').replace('Tối giản chuyển động','Ảnh thật · mô phỏng gọn')
    page=page.replace('Cùng một lời kể, hai cách minh họa.','Ảnh đời sống minh họa theo lời kể; mô phỏng ở đoạn tính toán và giải thích dòng tiền.')
    page=page.replace('</main>','<p><a href="asset-catalog.json">Nguồn ảnh và giấy phép</a> · <a href="photo-coverage.json">Phủ hình theo lời</a></p></main>');file.write_text(page,encoding='utf-8')
    clips=[];out=BATCH/revision
    for style in ['comic','clean']:
        receipt=out/style/'proof/receipt.json'
        if receipt.exists():clips.extend({'style':style,**c} for c in load(receipt)['clips'])
        photos=sorted((out/style/'preflight').glob('shot-*.jpg'))
        if photos:shutil.copy2(photos[0],BATCH/f'poster-{style}.jpg')
    options=''.join(f'<button data-i="{i}">{html.escape(c["style"])} — {html.escape(c["beat"])}</button>' for i,c in enumerate(clips))
    page='''<!doctype html><html lang="vi"><meta charset="utf-8"><title>Kiểm cảnh ảnh thật</title><style>body{background:#191e26;color:#faf3e7;font:16px Arial;margin:25px}video{width:min(1152px,100%);display:block}button{margin:8px;padding:10px}pre{white-space:pre-wrap}</style><h1>Cảnh ảnh thật và mô phỏng</h1><video controls playsinline preload="metadata"></video><div>'''+options+'''</div><pre id="state"></pre><script>
const clips='''+json.dumps(clips,ensure_ascii=False)+''';const v=document.querySelector('video');let current=-1;
function choose(i){current=i;v.src=clips[i].file;v.play();document.querySelector('#state').textContent=JSON.stringify({clip:clips[i].style+' / '+clips[i].beat,sourceFrom:clips[i].from/30,seconds:clips[i].frames/30},null,2)}
document.querySelectorAll('[data-i]').forEach(b=>b.onclick=()=>choose(Number(b.dataset.i)));
window.reviewState=()=>({index:current,clip:clips[current],time:v.currentTime,duration:v.duration,paused:v.paused,ended:v.ended,ready:v.readyState});
</script></html>'''
    (BATCH/'motion-review.html').write_text(page,encoding='utf-8');save(out/'proof-index.json',clips)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--revision',default='r01');p.add_argument('--serve',action='store_true');p.add_argument('--port',type=int,default=8882);a=p.parse_args();build(a.revision)
    if a.serve:
        print(f'http://127.0.0.1:{a.port}/',flush=True)
        ThreadingHTTPServer(('127.0.0.1',a.port),partial(StudyHandler,directory=str(BATCH))).serve_forever()
