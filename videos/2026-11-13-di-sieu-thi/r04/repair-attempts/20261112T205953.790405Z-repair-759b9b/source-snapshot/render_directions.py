"""Sequential persistent-bundle renderer for prepared photo/3D direction films.

This never calls the voice provider. It uses bounded public image derivatives,
retains every render attempt, validates each MP4, then packages both directions.
"""
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
import argparse
import ctypes
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
import uuid

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = Path(__file__).resolve().parent
PROJECT = WORKFLOW/'cinematic'
ENTRY = PROJECT/'src/directions-entry.tsx'
CLI = PROJECT/'node_modules/@remotion/cli/remotion-cli.js'
DEFAULT = ROOT/'videos/2026-11-12-hai-huong'


def memory_snapshot():
    """Read physical memory at attempt start without changing OS/process settings."""
    if os.name == 'nt':
        class MemoryStatus(ctypes.Structure):
            _fields_ = [('length', ctypes.c_ulong), ('load', ctypes.c_ulong),
                ('totalPhysical', ctypes.c_ulonglong), ('availablePhysical', ctypes.c_ulonglong),
                ('totalPageFile', ctypes.c_ulonglong), ('availablePageFile', ctypes.c_ulonglong),
                ('totalVirtual', ctypes.c_ulonglong), ('availableVirtual', ctypes.c_ulonglong),
                ('availableExtendedVirtual', ctypes.c_ulonglong)]
        value = MemoryStatus()
        value.length = ctypes.sizeof(value)
        if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(value)):
            return {'totalPhysicalBytes': value.totalPhysical, 'availablePhysicalBytes': value.availablePhysical,
                    'method': 'Windows GlobalMemoryStatusEx'}
    elif hasattr(os, 'sysconf'):
        try:
            page = os.sysconf('SC_PAGE_SIZE')
            return {'totalPhysicalBytes': os.sysconf('SC_PHYS_PAGES') * page,
                    'availablePhysicalBytes': os.sysconf('SC_AVPHYS_PAGES') * page, 'method': 'sysconf physical pages'}
        except (ValueError, OSError):
            pass
    return {'totalPhysicalBytes': None, 'availablePhysicalBytes': None, 'method': 'unavailable'}


def resolved_render_options(concurrency, crf, memory_profile='default'):
    if memory_profile not in ['default', 'bounded']:
        raise ValueError('Unknown memory profile')
    if concurrency < 1 or not 0 <= crf <= 51:
        raise ValueError('concurrency must be positive and CRF between 0 and 51')
    return {'memoryProfile': memory_profile, 'concurrency': 1 if memory_profile == 'bounded' else concurrency,
            'crf': crf, 'mediaCacheSizeInBytes': 256 * 1024 * 1024 if memory_profile == 'bounded' else None,
            'scope': 'Decoded @remotion/media cache budget only; not a total RAM cap or verified performance improvement.'}


def render_arguments(props, options):
    arguments = [f'--props={props}', f'--concurrency={options["concurrency"]}',
                 '--codec=h264', f'--crf={options["crf"]}', '--log=info']
    if options['mediaCacheSizeInBytes'] is not None:
        arguments.append(f'--media-cache-size-in-bytes={options["mediaCacheSizeInBytes"]}')
    return arguments


def load(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')


def sha(path):
    result = hashlib.sha256()
    with path.open('rb') as source:
        for block in iter(lambda: source.read(1024*1024), b''):
            result.update(block)
    return result.hexdigest()


def within(parent, path):
    resolved = path.resolve()
    if not resolved.is_relative_to(parent.resolve()):
        raise ValueError('Path leaves its intended directory: '+str(path))
    return resolved


@contextmanager
def project_lock(attempt_id):
    # An exclusive project lock serializes this orchestrator across batches that
    # otherwise share the Rspack cache. Never silently discard another job's lock.
    path = PROJECT/'.render-directions.lock'
    try:
        descriptor = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        raise RuntimeError('Another render orchestrator owns '+str(path)+'. Reconcile its process before retrying.') from None
    with os.fdopen(descriptor, 'w', encoding='utf-8') as handle:
        json.dump({'pid':os.getpid(), 'attempt':attempt_id}, handle)
    try:
        yield
    finally:
        if path.exists() and load(path).get('attempt') == attempt_id:
            path.unlink()


def preflight(batch, selected, public_source=None):
    if not ENTRY.is_file() or not CLI.is_file():
        raise ValueError('Missing production entry or local Remotion CLI; install the cinematic dependencies first')
    public_source = Path(public_source or PROJECT/'public').resolve()
    films = {}
    for direction in selected:
        folder = within(batch, batch/direction)
        data = load(folder/'data.json')
        if data['direction'] != direction or load(folder/'props.json').get('data') != data:
            raise ValueError('Timeline/props do not match for '+direction)
        if data['fps'] != 30 or data['frames'] <= 0:
            raise ValueError('Invalid exact-take runtime for '+direction)
        derivatives = {row['publicFile']:row for row in load(folder/'render-assets.json')['assets']}
        assets = {}
        for shot in data['shots']:
            for image in shot['images']:
                for key in [image['file']] + ([image['posterFile']] if image.get('posterFile') else []):
                    if not key.startswith('directions/'+direction+'/'):
                        raise ValueError('Only this direction namespace may be staged: '+key)
                    source = within(public_source/'directions', public_source/key)
                    receipt = derivatives.get(key)
                    if not receipt or not source.is_file() or sha(source) != receipt['publicSHA256']:
                        raise ValueError('Render derivative missing/changed: '+key+'. Prepare the correct batch assets.')
                    if max(receipt['publicDimensions']) > 2048 or receipt['publicDimensions'][1] > 1280:
                        raise ValueError('Oversized image/video derivative: '+key)
                    assets[key] = source
        mix = folder/'audio/final-mix.wav'
        if sha(mix) != load(folder/'audio-sources.json')['mix']['sha256']:
            raise ValueError('Final mix differs from retained receipt for '+direction)
        if data['audio'] != 'directions/'+direction+'/mix.wav':
            raise ValueError('Unexpected audio namespace for '+direction)
        films[direction] = {'folder':folder, 'data':data, 'assets':assets, 'mix':mix,
                            'props':(folder/'props.json').resolve(), 'final':folder/'final.mp4'}
    return films


def snapshot_sources(destination, films):
    destination.mkdir(parents=True)
    files = [WORKFLOW/name for name in [
        'directions.py', 'render_directions.py', 'direction_qa.py', 'directions_review.py',
        'production.py', 'PRODUCTION.md', 'reference-learning.profile.json',
        'TWO_DIRECTIONS.md', 'cinematic.profile.json', 'eleven_audio.py', 'documentary.py',
        'cinematic/src/directions-entry.tsx', 'cinematic/package.json',
        'cinematic/package-lock.json', 'cinematic/remotion.config.ts', 'cinematic/tsconfig.json',
    ]]
    files += list((WORKFLOW/'direction-profiles').rglob('*'))
    files += list((PROJECT/'src/directions').rglob('*'))
    records = []
    for source in files:
        if not source.is_file():
            continue
        relative = source.relative_to(WORKFLOW)
        target = destination/relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        records.append({'file':relative.as_posix(), 'sha256':sha(source)})
    for direction, film in films.items():
        for name in ['data.json', 'props.json', 'profile.json', 'script.txt',
                     'render-assets.json', 'image-sources.json', 'audio-sources.json',
                     'production-manifest.json', 'learning-guidance.json']:
            source = film['folder']/name
            if not source.is_file():
                continue
            target = destination/'batch'/direction/name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source,target)
            records.append({'file':target.relative_to(destination).as_posix(), 'sha256':sha(source)})
    save(destination/'hashes.json',records)


def stage_public(batch, public, attempt, films):
    # Retain an existing persistent tree instead of deleting another attempt's
    # evidence. Both move targets are checked against the named batch first.
    if public.exists():
        public.rename(within(batch, attempt/'previous-render-public'))
    public.mkdir(parents=True)
    for direction, film in films.items():
        for key, source in film['assets'].items():
            target = within(public, public/key)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source,target)
        namespace = public/'directions'/direction
        shutil.copy2(film['folder']/'data.json',namespace/'data.json')
        shutil.copy2(film['mix'],namespace/'mix.wav')


def run_logged(command, log, state, attempt):
    record = {'command':command, 'cwd':str(PROJECT), 'log':str(log),
              'startedUTC':datetime.now(timezone.utc).isoformat(), 'status':'running'}
    state['steps'].append(record)
    save(attempt/'attempt.json',state)
    print('RUNNING',log.name,'log:',str(log),flush=True)
    started = time.monotonic()
    with log.open('xb') as output:
        output.write((json.dumps({'argv':command,'cwd':str(PROJECT)},ensure_ascii=False)+'\n').encode('utf-8'))
        output.flush()
        result = subprocess.run(command,cwd=PROJECT,stdout=output,stderr=subprocess.STDOUT,shell=False)
    record.update({'returncode':result.returncode,'elapsedSeconds':round(time.monotonic()-started,3),
                   'status':'completed' if result.returncode==0 else 'failed'})
    save(attempt/'attempt.json',state)
    if result.returncode:
        raise RuntimeError('Command failed; retained full log at '+str(log))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--batch',type=Path,default=DEFAULT)
    parser.add_argument('--direction',choices=['long','hidden','both'],default='both')
    parser.add_argument('--concurrency',type=int,default=1)
    parser.add_argument('--memory-profile',choices=['default','bounded'],default='default',
                        help='Opt in to one render page and a 256 MiB @remotion/media cache; does not cap total RAM')
    parser.add_argument('--public-source',type=Path,help='Batch-local prepared public assets; default retains cinematic/public')
    parser.add_argument('--crf',type=int,default=19)
    existing = parser.add_mutually_exclusive_group()
    existing.add_argument('--overwrite',action='store_true',help='Retain previous final in this attempt before installing the new one')
    existing.add_argument('--skip-existing',action='store_true',help='Keep existing finals and run their QA; render missing finals only')
    parser.add_argument('--dry-run',action='store_true',help='Read/validate inputs and print argv; do not bundle, render or modify files')
    args = parser.parse_args()
    if args.concurrency < 1 or not 0 <= args.crf <= 51:
        parser.error('concurrency must be positive and CRF between 0 and 51')
    options = resolved_render_options(args.concurrency,args.crf,args.memory_profile)
    batch = args.batch.resolve()
    selected = ['long','hidden'] if args.direction=='both' else [args.direction]
    public_source = (args.public_source or PROJECT/'public').resolve()
    films = preflight(batch,selected,public_source)
    present = [name for name,film in films.items() if film['final'].exists()]
    if present and not (args.overwrite or args.skip_existing):
        parser.error('Existing final.mp4 for '+', '.join(present)+'. Use --skip-existing to validate, or --overwrite to retain and replace explicitly.')
    node = shutil.which('node')
    if not node:
        parser.error('Node.js is unavailable')
    cli = [str(Path(node).resolve()),str(CLI.resolve())]
    attempt_id = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')+'-'+uuid.uuid4().hex[:6]
    attempt = within(batch,batch/'render-attempts'/attempt_id)
    bundle = within(batch,batch/'render-bundle')
    public = within(batch,batch/'render-public')
    rendering = [d for d in selected if args.overwrite or not films[d]['final'].exists()]
    bundle_command = cli+['bundle',str(ENTRY.resolve()),f'--out-dir={bundle}',f'--public-dir={public}','--log=info']
    commands = []
    if rendering:
        commands.append(bundle_command)
    for direction in selected:
        film = films[direction]
        if direction in rendering:
            commands.append(cli+['render',str(bundle),'DirectionPreview',str(attempt/(direction+'-render.mp4')),
                                  *render_arguments(film['props'],options)])
        commands.append([sys.executable,str(WORKFLOW/'direction_qa.py'),'--batch',str(film['folder']),'--public-source',str(public_source)])
    if selected==['long','hidden']:
        commands.append([sys.executable,str(WORKFLOW/'directions_review.py'),'--batch',str(batch)])
    if args.dry_run:
        print(json.dumps({'dryRun':True,'cwd':str(PROJECT),'attempt':str(attempt),
                          'sequential':True,'concurrency':options['concurrency'],'renderOptions':options,
                          'memoryAtStart':memory_snapshot(),'commands':commands},ensure_ascii=False,indent=2))
        return
    with project_lock(attempt_id):
        attempt.mkdir(parents=True,exist_ok=False)
        state = {'attempt':attempt_id,'batch':str(batch),'directions':selected,'status':'running','steps':[],
                 'renderOptions':options,'memoryAtStart':memory_snapshot(),
                 'aestheticAcceptance':'pending user feedback; technical QA is not visual approval'}
        save(attempt/'attempt.json',state)
        try:
            snapshot_sources(attempt/'source-snapshot',films)
            if rendering:
                stage_public(batch,public,attempt,films)
                if bundle.exists():
                    bundle.rename(within(batch,attempt/'previous-render-bundle'))
                run_logged(bundle_command,attempt/'bundle.log',state,attempt)
                if not (bundle/'index.html').is_file():
                    raise RuntimeError('Explicit persistent bundle directory was not created; do not render a temporary fallback')
            for direction in selected:
                film = films[direction]
                if direction in rendering:
                    output = attempt/(direction+'-render.mp4')
                    command = cli+['render',str(bundle),'DirectionPreview',str(output),
                                   *render_arguments(film['props'],options)]
                    run_logged(command,attempt/(direction+'-render.log'),state,attempt)
                    if not output.is_file() or output.stat().st_size==0:
                        raise RuntimeError('Renderer returned without a nonempty video for '+direction)
                    if film['final'].exists():
                        if not args.overwrite:
                            raise RuntimeError('A final appeared during render; retained the new output in this attempt without replacing '+str(film['final']))
                        film['final'].rename(attempt/(direction+'-previous-final.mp4'))
                    output.replace(film['final'])
                if (film['folder']/'qa').exists():
                    shutil.copytree(film['folder']/'qa',attempt/(direction+'-previous-qa'))
                run_logged([sys.executable,str(WORKFLOW/'direction_qa.py'),'--batch',str(film['folder']),'--public-source',str(public_source)],
                           attempt/(direction+'-qa.log'),state,attempt)
            if selected==['long','hidden']:
                run_logged([sys.executable,str(WORKFLOW/'directions_review.py'),'--batch',str(batch)],
                           attempt/'package.log',state,attempt)
            state['status'] = 'completed'
            save(attempt/'attempt.json',state)
            print('COMPLETED',str(attempt),'visual/audio acceptance pending user review',flush=True)
        except BaseException as error:
            state.update({'status':'failed','errorType':type(error).__name__,'error':str(error)})
            save(attempt/'attempt.json',state)
            raise


if __name__=='__main__':
    main()
