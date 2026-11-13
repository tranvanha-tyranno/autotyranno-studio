"""Bundle and render the literal visual workflow without replacing earlier batches."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from documentary import FF

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = Path(__file__).parent
PROJECT = WORKFLOW / 'cinematic'
DEFAULT = ROOT / 'videos/2026-11-12-hai-huong-khop-loi'


def cli(args, log):
    node = shutil.which('node')
    script = PROJECT / 'node_modules/@remotion/cli/remotion-cli.js'
    log.parent.mkdir(parents=True, exist_ok=True)
    if log.exists():
        raise FileExistsError('Preserve previous attempt; use a new revision: ' + str(log))
    with log.open('w', encoding='utf-8') as stream:
        process = subprocess.run([node, str(script), *args], cwd=PROJECT, stdout=stream, stderr=subprocess.STDOUT)
    if process.returncode:
        raise RuntimeError('Render tool failed; inspect ' + str(log))


def run(action, batch, revision, direction, attempt=None, chunk_seconds=5):
    bundle = batch / ('bundle-' + revision)
    public = batch / 'render-public'
    directions = ['long', 'hidden'] if direction == 'both' else [direction]
    if action == 'bundle':
        if bundle.exists():
            raise FileExistsError('Use a new revision to retain bundle evidence')
        (public / 'semantic').mkdir(parents=True, exist_ok=True)
        shutil.copytree(PROJECT / 'public/semantic', public / 'semantic', dirs_exist_ok=True)
        cli(['bundle', 'src/semantic-entry.tsx', '--out-dir=' + str(bundle), '--public-dir=' + str(public), '--log=info'], batch / f'bundle-{revision}.log')
        return
    for name in directions:
        folder = batch / name
        if action == 'proofs':
            if (folder / 'proofs').exists():
                raise FileExistsError('Archive earlier proof directory before regenerating: ' + str(folder))
            subprocess.run([shutil.which('node'), str(PROJECT / 'scripts/semantic-proof.mjs'), '--bundle', str(bundle), '--batch', str(folder)], cwd=PROJECT, check=True)
            subprocess.run([sys.executable, str(WORKFLOW / 'semantic_pairs.py'), '--batch', str(folder)], check=True)
        elif action in ['render', 'chunks']:
            final = folder / 'final.mp4'
            if final.exists():
                raise FileExistsError('Keep existing final intact; choose a new batch')
            review = json.loads((folder / 'proofs/semantic-review.json').read_text(encoding='utf-8'))
            shots = review['shots']
            expected = json.loads((folder / 'data.json').read_text(encoding='utf-8'))['shots']
            if {s['id'] for s in shots} != {s['id'] for s in expected} or any(s['status'] != 'pass' for s in shots):
                raise ValueError('Every clause needs actual proof inspection and unresolved mismatches must be fixed')
            for shot in shots:
                if shot.get('evidenceSHA256'):
                    evidence = folder / 'proofs' / shot['evidence']
                    if hashlib.sha256(evidence.read_bytes()).hexdigest() != shot['evidenceSHA256']:
                        raise ValueError('Reviewed proof changed after inspection: ' + shot['id'])
            common = ['render', str(bundle), 'SemanticReview']
            flags = ['--props=' + str(folder / 'props.json'), '--codec=h264', '--crf=19', '--concurrency=1', '--disable-shared-memory-capture', '--log=info']
            if action == 'render':
                cli(common + [str(final)] + flags, folder / f'render-{attempt or revision}.log')
            else:
                chunks = folder / ('chunks-' + (attempt or revision))
                chunks.mkdir(exist_ok=True)
                data = json.loads((folder / 'data.json').read_text(encoding='utf-8'))
                span = round(data['fps'] * chunk_seconds)
                parts = []
                for start in range(0, data['frames'], span):
                    end = min(data['frames'], start + span) - 1
                    part = chunks / f'{start:05}-{end:05}.mp4'
                    if not part.exists():
                        cli(common + [str(part)] + flags + [f'--frames={start}-{end}', '--muted'], chunks / f'{start:05}-{end:05}.log')
                    parts.append(part)
                    print('CHUNK', direction, start, end, flush=True)
                listfile = chunks / 'concat.txt'
                listfile.write_text(''.join("file '" + p.as_posix().replace("'", "'\\''") + "'\n" for p in parts), encoding='utf-8')
                subprocess.run([FF, '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', str(listfile),
                                '-i', str(folder / 'mix.wav'), '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'copy',
                                '-c:a', 'aac', '-b:a', '192k', '-t', str(data['frames'] / data['fps']),
                                '-movflags', '+faststart', str(final)], check=True)
        elif action == 'qa':
            subprocess.run([sys.executable, str(WORKFLOW / 'semantic_qa.py'), '--batch', str(folder)], check=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['bundle', 'proofs', 'render', 'chunks', 'qa'])
    parser.add_argument('--batch', type=Path, default=DEFAULT)
    parser.add_argument('--revision', required=True)
    parser.add_argument('--direction', choices=['long', 'hidden', 'both'], default='both')
    parser.add_argument('--attempt', help='Keep a new log when retrying the same reviewed bundle')
    parser.add_argument('--chunk-seconds', type=float, default=5)
    args = parser.parse_args()
    run(args.action, args.batch.resolve(), args.revision, args.direction, args.attempt, args.chunk_seconds)
