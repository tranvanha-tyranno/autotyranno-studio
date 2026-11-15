"""Fetch pinned GitHub source archives for read-only research; execute none.

The extraction is bounded and rejects traversal, links and Windows device paths.
"""
from pathlib import Path, PurePosixPath
import hashlib
import json
import os
import re
import stat
import subprocess
import time
import zipfile

import requests

OUT=Path(__file__).resolve().parent/'sources'
REPOS=['MichaelAchugwo/agentic-video-edits-gen','sub-level/marketing-videos',
       'pifferologo/ai-agent-video-editor','Mng-dev-ai/explainer-video',
       'precious112/demo-director','openai/skills']
MAX_ARCHIVE=64*1024*1024
MAX_EXTRACTED=384*1024*1024
RESERVED=re.compile(r'^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\.|$)',re.I)


def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()


def save(path,obj):
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


def fetch(repo):
    folder=OUT/repo.replace('/','__');folder.mkdir(parents=True,exist_ok=True)
    receipt=folder/'source-receipt.json'
    if receipt.exists():
        previous=json.loads(receipt.read_text(encoding='utf-8'))
        if previous.get('status')=='downloaded_and_extracted':
            archive=folder/previous['archiveFile']
            if archive.exists() and sha(archive)==previous['archiveSHA256']:
                print(json.dumps({'repo':repo,'cached':True,'commit':previous['commit']}),flush=True)
                return previous
            raise ValueError('Existing research receipt does not match archive')
    started=time.perf_counter();canonical='https://github.com/'+repo
    state={'repo':repo,'canonicalURL':canonical,'purpose':'Read-only source/skill study; no external source execution or global install',
           'maxArchiveBytes':MAX_ARCHIVE,'maxExtractedBytes':MAX_EXTRACTED,'status':'pending'}
    try:
        env={**os.environ,'GIT_TERMINAL_PROMPT':'0'}
        result=subprocess.run(['git','ls-remote','--symref',canonical+'.git','HEAD'],capture_output=True,
                              text=True,encoding='utf-8',errors='replace',timeout=35,env=env)
        if result.returncode:raise RuntimeError('git ls-remote failed: '+result.stderr[-600:])
        head=re.search(r'^([a-f0-9]{40})\s+HEAD$',result.stdout,re.M)
        if not head:raise RuntimeError('No HEAD commit returned')
        commit=head.group(1);branch=re.search(r'^ref: refs/heads/(\S+)\s+HEAD$',result.stdout,re.M)
        state.update(commit=commit,defaultBranch=branch.group(1) if branch else None,remoteEvidence=result.stdout.strip())
        archive=folder/'archive.zip';partial=folder/'archive.partial.zip'
        url=f'https://codeload.github.com/{repo}/zip/{commit}';total=0
        with requests.get(url,stream=True,timeout=(15,35)) as response:
            response.raise_for_status()
            if int(response.headers.get('Content-Length','0'))>MAX_ARCHIVE:raise RuntimeError('Archive exceeds configured byte limit')
            with partial.open('wb') as f:
                for chunk in response.iter_content(1024*1024):
                    if not chunk:continue
                    total+=len(chunk)
                    if total>MAX_ARCHIVE:raise RuntimeError('Archive exceeds configured byte limit')
                    f.write(chunk)
        partial.replace(archive)
        destination=(folder/'extracted').resolve();destination.mkdir(exist_ok=True)
        with zipfile.ZipFile(archive) as z:
            entries=z.infolist()
            if len(entries)>30000:raise RuntimeError('Too many archive entries')
            if sum(x.file_size for x in entries)>MAX_EXTRACTED:raise RuntimeError('Expanded archive exceeds byte limit')
            validated=[]
            for info in entries:
                posix=PurePosixPath(info.filename)
                if posix.is_absolute() or any(p in ('..','') or ':' in p or '\\' in p or RESERVED.match(p) for p in posix.parts):
                    raise RuntimeError('Rejected unsafe archive path: '+info.filename)
                mode=info.external_attr>>16
                if stat.S_ISLNK(mode):raise RuntimeError('Rejected symbolic link: '+info.filename)
                target=destination.joinpath(*posix.parts).resolve()
                if not target.is_relative_to(destination):raise RuntimeError('Archive path escaped extraction root')
                validated.append((info,target))
            for info,target in validated:
                if info.is_dir():target.mkdir(parents=True,exist_ok=True);continue
                target.parent.mkdir(parents=True,exist_ok=True)
                if target.exists():raise RuntimeError('Refuse overwriting existing extracted file: '+str(target))
                with z.open(info) as src,target.open('xb') as dst:
                    for chunk in iter(lambda:src.read(1024*1024),b''):dst.write(chunk)
        roots=[p for p in destination.iterdir() if p.is_dir()]
        state.update(status='downloaded_and_extracted',archiveFile=archive.name,archiveURL=url,
                     archiveSHA256=sha(archive),archiveBytes=archive.stat().st_size,
                     extractedRoot=str(roots[0].relative_to(folder)).replace('\\','/') if len(roots)==1 else 'extracted',
                     fileCount=sum(1 for p in destination.rglob('*') if p.is_file()),
                     downloadedAt='2026-11-15 Asia/Saigon',wallSeconds=round(time.perf_counter()-started,3))
    except Exception as error:
        state.update(status='failed',errorType=type(error).__name__,error=str(error),wallSeconds=round(time.perf_counter()-started,3))
    save(receipt,state);print(json.dumps({k:state.get(k) for k in ['repo','status','commit','archiveBytes','fileCount','error']},ensure_ascii=False),flush=True)
    return state


if __name__=='__main__':
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(fetch,REPOS))
    save(OUT.parent/'group-c-downloads.json',results)
