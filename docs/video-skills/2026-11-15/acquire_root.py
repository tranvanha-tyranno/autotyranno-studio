"""Archive public video-skill sources; never execute downloaded code."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path, PurePosixPath
import hashlib
import json
import os
import subprocess
import urllib.request
import zipfile

BASE = Path(__file__).resolve().parent
REPOS = [
    'Barty-Bart/motion-graphics', 'Clipwing/skills',
    'ishuagrawal/skills', 'win4r/video-director',
    'smixs/visual-skills', 'Aaryan-Kapoor/video-production-skill',
    'liangdabiao/math-concept-film', 'Yusuke710/manim-skill',
    'TashanGKD/tashan-research-skills',
]


def acquire(repo):
    dest = BASE / 'sources' / repo.replace('/', '__')
    dest.mkdir(parents=True, exist_ok=True)
    receipt = dest / 'receipt.json'
    if receipt.exists():
        return json.loads(receipt.read_text(encoding='utf-8'))
    record = {'repo': repo, 'canonicalURL': f'https://github.com/{repo}',
              'externalCodeExecuted': False, 'reviewStatus': 'downloaded_not_yet_read'}
    try:
        env = dict(os.environ, GIT_TERMINAL_PROMPT='0', GCM_INTERACTIVE='Never')
        result = subprocess.run(['git', 'ls-remote', f'https://github.com/{repo}.git', 'HEAD'],
                                capture_output=True, text=True, timeout=55, env=env, check=True)
        commit = result.stdout.split()[0]
        if len(commit) != 40 or any(c not in '0123456789abcdef' for c in commit):
            raise ValueError('Invalid commit')
        record['commit'] = commit
        archive = dest / 'source.zip'
        request = urllib.request.Request(f'https://codeload.github.com/{repo}/zip/{commit}',
                                         headers={'User-Agent': 'Codex-video-skill-archive'})
        with urllib.request.urlopen(request, timeout=60) as response, archive.open('wb') as output:
            count = 0
            while chunk := response.read(1024 * 1024):
                count += len(chunk)
                if count > 200 * 1024 * 1024:
                    raise ValueError('Archive exceeds 200 MiB bound')
                output.write(chunk)
        snapshot = dest / 'snapshot'
        snapshot.mkdir(exist_ok=True)
        with zipfile.ZipFile(archive) as zf:
            if sum(i.file_size for i in zf.infolist()) > 600 * 1024 * 1024:
                raise ValueError('Expanded archive exceeds 600 MiB bound')
            for member in zf.infolist():
                parts = PurePosixPath(member.filename).parts[1:]
                if not parts:
                    continue
                if any(p in ('.', '..') or ':' in p or '\\' in p for p in parts):
                    raise ValueError('Unsafe archive entry')
                if (member.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('Archive contains symbolic link')
                target = snapshot.joinpath(*parts)
                if not target.resolve().is_relative_to(snapshot.resolve()):
                    raise ValueError('Archive escapes snapshot')
                if member.is_dir():
                    target.mkdir(parents=True, exist_ok=True)
                else:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(zf.read(member))
        record.update(archive=str(archive.relative_to(BASE)), archiveBytes=archive.stat().st_size,
                      archiveSHA256=hashlib.sha256(archive.read_bytes()).hexdigest(),
                      snapshot=str(snapshot),
                      skillPaths=[p.relative_to(snapshot).as_posix() for p in snapshot.rglob('SKILL.md')],
                      licenses=[p.relative_to(snapshot).as_posix() for p in snapshot.rglob('*')
                                if p.is_file() and p.name.lower() in ('license', 'license.md', 'license.txt', 'copying')],
                      fileCount=sum(1 for p in snapshot.rglob('*') if p.is_file()))
    except Exception as exc:
        record['error'] = f'{type(exc).__name__}: {str(exc)[:500]}'
    receipt.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding='utf-8')
    return record


if __name__ == '__main__':
    results = []
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = [pool.submit(acquire, repo) for repo in REPOS]
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            print(result['repo'], result.get('error', f"{len(result['skillPaths'])} skill entries"), flush=True)
    (BASE / 'group-root-downloads.json').write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')
