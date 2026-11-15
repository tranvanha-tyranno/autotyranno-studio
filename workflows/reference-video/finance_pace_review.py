"""Serve the new paced films and complete temporal-proof clips locally."""
import argparse,html,json,shutil
from functools import partial
from http.server import ThreadingHTTPServer
from finance_pace import BATCH,load,save,sha
from serve_reference_study import StudyHandler
import finance_long_review as viewer

def build(revision='r01'):
    viewer.BATCH=BATCH;viewer.build(revision)
    out=BATCH/revision;clips=[]
    for style in ['comic','flow']:
        receipt=out/style/'proof/receipt.json'
        if receipt.exists():
            for clip in load(receipt)['clips']:clips.append({'style':style,**clip})
        images=sorted((out/style/'preflight').glob('b01-*.jpg'))
        if images:shutil.copy2(images[0],BATCH/('poster-'+style+'.jpg'))
    options=''.join(f'<button data-i="{i}">{html.escape(c["style"])} — {html.escape(c["beat"])}</button>'for i,c in enumerate(clips))
    page='''<!doctype html><html lang="vi"><meta charset="utf-8"><title>Kiểm diễn biến cảnh</title><style>body{background:#191e26;color:#faf3e7;font:16px Arial;margin:25px}video{width:min(1152px,100%);display:block}button{margin:8px;padding:10px}pre{white-space:pre-wrap}</style><h1>Các cảnh kiểm chuyển động</h1><video controls playsinline preload="metadata"></video><div>'''+options+'''</div><pre id="state"></pre><script>
const clips='''+json.dumps(clips,ensure_ascii=False)+''';const v=document.querySelector('video');let current=-1;
function choose(i){current=i;v.src=clips[i].file;v.play();document.querySelector('#state').textContent=JSON.stringify({clip:clips[i].style+' / '+clips[i].beat,sourceFrom:clips[i].from/30,seconds:clips[i].duration/30},null,2)}
document.querySelectorAll('[data-i]').forEach(b=>b.onclick=()=>choose(Number(b.dataset.i)));
v.addEventListener('ended',()=>{if(current+1<clips.length)choose(current+1)});
window.reviewState=()=>({index:current,clip:clips[current],time:v.currentTime,duration:v.duration,paused:v.paused,ended:v.ended,ready:v.readyState});
</script></html>'''
    (BATCH/'motion-review.html').write_text(page,encoding='utf-8');save(out/'proof-index.json',clips)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--revision',default='r01');parser.add_argument('--serve',action='store_true');parser.add_argument('--port',type=int,default=8881);args=parser.parse_args();build(args.revision)
    if args.serve:
        print(f'http://127.0.0.1:{args.port}/',flush=True)
        ThreadingHTTPServer(('127.0.0.1',args.port),partial(StudyHandler,directory=str(BATCH))).serve_forever()
