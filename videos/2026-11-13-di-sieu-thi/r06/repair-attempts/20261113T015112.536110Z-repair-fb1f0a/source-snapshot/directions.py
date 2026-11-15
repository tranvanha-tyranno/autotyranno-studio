"""Reproduce the retained photo/gallery 3D direction interface and older batches.

For new work read REFERENCE_LEARNING.md and PRODUCTION.md, then use production.py
with the new topic's inspected source catalog. The user restored this gallery
interface; the email/table-heavy semantic rebuild was rejected as the default.
Old image choices remain unaccepted and require clause-by-clause replacement.

Profiles contain original narration, ordered phrase cuts and semantic image choices.
This is a manifest-driven production tool, not automatic understanding of any channel.
It leaves existing approved media/compositions untouched and never time-stretches voice.
"""
from pathlib import Path
import argparse, hashlib, json, math, re, shutil, unicodedata
import requests
from PIL import Image, ImageOps
from documentary import FF, duration, run
from eleven_audio import speech, words

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = Path(__file__).parent
PUB = WORKFLOW/'cinematic/public'
DEFAULT = ROOT/'videos/2026-11-12-hai-huong'
VOICE = '6adFm46eyy74snVn6YrT'
EXTRA_IMAGES = {
    'pens-proof': (7876785, 'people-pointing-their-pens-on-a-printed-paper', 'Kaboompics.com', 'People checking printed paper with pens'),
    'held-docs': (7545311, 'a-person-holding-documents', 'SHVETS production', 'Person holding documents for review'),
    'clipboard-check': (7731400, 'a-person-in-black-blazer-pointing-the-document-on-the-clipboard', 'Mikhail Nilov', 'Person pointing at a document on a clipboard'),
}

def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

def load(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def norm(text):
    return re.sub(r'[^\w]', '', unicodedata.normalize('NFC', text).lower())

def plan(direction, base, profile_path=None):
    profile = load(profile_path or WORKFLOW/f'direction-profiles/{direction}.json')
    if profile['direction'] != direction:
        raise ValueError('Manifest direction differs from requested composition direction')
    if [s['phase'] for s in profile['sections']] != ['hook','disclaimer','content','cta']:
        raise ValueError('Expected exactly hook → disclaimer → content → CTA sections')
    batch = base/direction
    batch.mkdir(parents=True, exist_ok=True)
    save(batch/'profile.json', profile)
    text = '\n\n'.join(section['text'] for section in profile['sections'])
    (batch/'script.txt').write_text(text+'\n', encoding='utf-8')
    save(batch/'batch.json', {
        'direction': direction, 'title': profile['title'], 'scriptWords': len(text.split()),
        'voice': {'name': 'Nhật Phong', 'voice_id': VOICE, 'model_id': 'eleven_v3',
                  'language_code': 'vi', 'speed': 1.0, 'stability': .5, 'similarity_boost': .8},
        'structure': ['hook', 'disclaimer', 'content', 'cta'],
        'durationPolicy': 'Follow exact natural take plus 1s tail; no time stretching or final-sentence truncation',
        'sourceIdentity': 'TYRANNO original demonstration; channel references are structural inspiration',
        'acceptance': 'Pending user visual/audio feedback',
    })
    return profile, batch, text

def voice(direction, base, profile_path=None):
    profile, batch, text = plan(direction, base, profile_path)
    speech(batch/'audio/narration-original.mp3', text, VOICE)

def prepare(direction, base, profile_path=None):
    profile, batch, text = plan(direction, base, profile_path)
    audio = batch/'audio/narration-original.mp3'
    aligned = words(load(audio.with_suffix('.alignment.json')))
    expected = [norm(s) for s in text.split()]
    actual = [norm(s['text']) for s in aligned]
    if actual != expected:
        raise ValueError('Exact speech alignment differs from the final script; reconcile before editing')
    natural = duration(audio)
    seconds = math.ceil(max(natural, aligned[-1]['end'])+1)
    frames = seconds*30
    tokens = [norm(row['text']) for row in aligned]
    def find(phrase, after):
        q = [norm(s) for s in phrase.split()]
        for i in range(after, len(tokens)-len(q)+1):
            if tokens[i:i+len(q)] == q:
                return i
        raise ValueError('Missing/out-of-order actual-take phrase: '+phrase)

    source = ROOT/profile['sourceBatch']
    originals = {r['id']: r for r in load(source/'image-sources.json')}
    derived = {r['file'].split('/')[-1].removesuffix('.jpg'): r for r in load(source/'derived-assets.json')}
    namespace = 'directions/'+direction
    public = PUB/namespace
    public.mkdir(parents=True, exist_ok=True)
    assetdir = batch/'assets'
    assetdir.mkdir(exist_ok=True)
    receipts = {}
    def image(name):
        if name not in receipts:
            if name in EXTRA_IMAGES:
                photo_id, slug, creator, description = EXTRA_IMAGES[name]
                origin = assetdir/f'{name}.jpg'
                download = f'https://images.pexels.com/photos/{photo_id}/pexels-photo-{photo_id}.jpeg?auto=compress&cs=tinysrgb&w=2400'
                if not origin.exists():
                    response = requests.get(download, timeout=45)
                    response.raise_for_status()
                    if not response.headers.get('content-type', '').startswith('image/'):
                        raise ValueError('Source did not return an image: '+name)
                    origin.write_bytes(response.content)
                record = {'id':name, 'providerPhotoId':photo_id,
                          'page':f'https://www.pexels.com/photo/{slug}-{photo_id}/',
                          'download':download, 'creator':creator, 'description':description,
                          'license':'Pexels License', 'licenseURL':'https://www.pexels.com/license/',
                          'role':'Illustrative stock photo, not evidence that the depicted people use AI, lose jobs or endorse this film',
                          'sha256':sha(origin)}
            else:
                record = dict(originals['review-team'] if name=='review-team-detail' else originals[name])
                origin = source/'assets'/f'{name}.jpg'
            expected_hash = derived[name]['sha256'] if name in derived else record['sha256']
            if sha(origin) != expected_hash:
                raise ValueError('Source asset hash changed: '+name)
            if origin.resolve() != (assetdir/origin.name).resolve():
                shutil.copy2(origin, assetdir/origin.name)
            shutil.copy2(origin, public/origin.name)
            with Image.open(origin) as im:
                im.verify()
            with Image.open(origin) as im:
                width, height = im.size
            record.update({'id':name, 'file':'assets/'+origin.name,
                           'width':width, 'height':height, 'sha256':sha(origin),
                           'bytes':origin.stat().st_size,
                           'reusedFrom':None if name in EXTRA_IMAGES else str(source.relative_to(ROOT)).replace('\\','/')})
            if name in derived:
                record['derivation'] = derived[name]
            receipts[name] = record
        r = receipts[name]
        return {'file':namespace+'/'+name+'.jpg',
                'credit':r['creator']+' / Pexels',
                'focus':[50,45], 'aspect':r['width']/r['height']}

    shots, phases, cursor = [], [], 0
    for section in profile['sections']:
        phase = section['phase']
        phase_start = None
        for raw in section['shots']:
            ix = find(raw['phrase'], cursor)
            cursor = ix+1
            start = 0 if not shots else round(aligned[ix]['start']*30)
            row = {**raw, 'start':start, 'phase':phase,
                   'images':[image(name) for name in raw['images']]}
            if phase_start is None:
                phase_start = start
            shots.append(row)
        phases.append({'phase':phase, 'start':phase_start})
    for i, row in enumerate(shots):
        row['end'] = shots[i+1]['start'] if i+1<len(shots) else frames
        if row['end'] <= row['start']:
            raise ValueError('Nonpositive shot duration: '+row['phrase'])
    for i, phase in enumerate(phases):
        phase['end'] = phases[i+1]['start'] if i+1<len(phases) else frames

    caps, part = [], []
    for word in aligned:
        candidate = ' '.join(x['text'] for x in part+[word])
        if part and (len(candidate)>44 or word['end']-part[0]['start']>2.8):
            caps.append({'start':part[0]['start'], 'end':part[-1]['end'],
                         'text':' '.join(x['text'] for x in part)})
            part = []
        part.append(word)
        if re.search(r'[.!?:]$', word['text']):
            caps.append({'start':part[0]['start'], 'end':part[-1]['end'],
                         'text':' '.join(x['text'] for x in part)})
            part = []
    if part:
        caps.append({'start':part[0]['start'], 'end':part[-1]['end'], 'text':' '.join(x['text'] for x in part)})
    data = {'direction':direction, 'fps':30, 'frames':frames, 'title':profile['title'],
            'audio':namespace+'/mix.wav', 'shots':shots, 'captions':caps}
    save(batch/'data.json', data)
    save(batch/'props.json', {'data':data})
    save(public/'data.json', data)
    save(batch/'aligned-words.json', aligned)
    save(batch/'image-sources.json', list(receipts.values()))
    save(batch/'phase-timing.json', phases)
    save(batch/'shotlist.json', shots)
    gallery_frames = sum(s['end']-s['start'] for s in shots if s['layout']=='gallery3d')
    report = {'frames':frames, 'seconds':seconds, 'naturalVoiceSeconds':natural,
              'lastWordEnd':aligned[-1]['end'], 'tempo':1.0, 'scriptWords':len(expected),
              'shots':len(shots), 'uniquePhotos':len(receipts),
              'photoPlacements':sum(len(s['images']) for s in shots),
              'gallery3DSeconds':gallery_frames/30,
              'gallery3DFraction':gallery_frames/frames,
              'captionMaxCharacters':max(len(c['text']) for c in caps),
              'allNarrationWordsAligned':True,
              'visualInspection':'Pending render review; source images reused with verified hashes and recorded crop',
              'userAcceptance':'pending'}
    save(batch/'preflight.json', report)
    save(batch/'research.json', {
        'nature':'Original qualitative hypothetical examples and editorial self-review framework',
        'claimsNotMade':['No employment or job-loss prediction', 'No statistics attributed to the new demo',
                         'No depicted stock subject asserted to use AI, be fired or endorse the film'],
        'channelStructure':'Hook, disclaimer, content, CTA requested by user for both directions; not a universal claim about both reference channels',
        'referenceAudit':'docs/video-references/2026-11-12-two-directions/REFERENCE_AUDIT.md',
    })
    render_assets(direction, base)
    print(json.dumps({'direction':direction, **report}, ensure_ascii=False), flush=True)

def render_assets(direction, base, profile_path=None):
    """Derive bounded JPEG textures, leaving archived originals/audio/timing intact."""
    batch = base/direction
    data = load(batch/'data.json')
    source_rows = {r['id']:r for r in load(batch/'image-sources.json')}
    public = PUB/'directions'/direction
    public.mkdir(parents=True, exist_ok=True)
    used = {Path(image['file']).stem for shot in data['shots'] for image in shot['images']}
    records, aspects = [], {}
    for name in sorted(used):
        receipt = source_rows[name]
        original = batch/receipt['file']
        original_sha = sha(original)
        if original_sha != receipt['sha256']:
            raise ValueError('Original asset differs from retained source receipt: '+name)
        target = public/(name+'.jpg')
        partial = target.with_suffix('.partial')
        with Image.open(original) as stored:
            stored_dimensions = list(stored.size)
            orientation = stored.getexif().get(274, 1)
            oriented = ImageOps.exif_transpose(stored)
            oriented_dimensions = list(oriented.size)
            rgb = oriented.convert('RGB')
            rgb.thumbnail((2048,1280), Image.Resampling.LANCZOS)
            public_dimensions = list(rgb.size)
            rgb.save(partial, format='JPEG', quality=94)
            rgb.close()
            oriented.close()
        partial.replace(target)
        with Image.open(target) as check:
            check.verify()
        aspects[name] = oriented_dimensions[0]/oriented_dimensions[1]
        records.append({
            'id':name, 'originalFile':receipt['file'],
            'publicFile':'directions/'+direction+'/'+target.name,
            'originalSHA256':original_sha, 'publicSHA256':sha(target),
            'originalStoredDimensions':stored_dimensions,
            'exifOrientationBefore':orientation, 'orientedDimensions':oriented_dimensions,
            'publicDimensions':public_dimensions,
            'originalBytes':original.stat().st_size, 'publicBytes':target.stat().st_size,
            'method':{'exifTranspose':True,'thumbnailBounds':[2048,1280],
                      'resampling':'Lanczos','format':'JPEG','quality':94,'crop':None},
            'preservation':'Original bytes retained unchanged in batch/assets',
        })
    aspect_corrections = []
    for shot in data['shots']:
        for image in shot['images']:
            name = Path(image['file']).stem
            if abs(image.get('aspect',aspects[name])-aspects[name])>1e-8:
                aspect_corrections.append({'file':image['file'], 'before':image.get('aspect'), 'after':aspects[name]})
                image['aspect'] = aspects[name]
    # Only EXIF orientation changes can require updating display aspect. All
    # timing, narration, caption and audio fields remain byte-equivalent values.
    if aspect_corrections:
        save(batch/'data.json',data)
        save(batch/'props.json',{'data':data})
        save(public/'data.json',data)
    save(batch/'render-assets.json',{
        'purpose':'Bound decoded texture RAM for Remotion/Three.js; source originals are immutable',
        'direction':direction, 'assets':records, 'aspectCorrections':aspect_corrections,
        'originalDecodedPixels':sum(r['originalStoredDimensions'][0]*r['originalStoredDimensions'][1] for r in records),
        'publicDecodedPixels':sum(r['publicDimensions'][0]*r['publicDimensions'][1] for r in records),
    })
    print('RENDER_ASSETS_READY',direction,len(records),'aspectCorrections',len(aspect_corrections),flush=True)

def mix(direction, base, profile_path=None):
    batch = base/direction
    data = load(batch/'data.json')
    seconds = data['frames']/30
    audio = batch/'audio'
    approved = ROOT/'videos/2026-11-11-cinematic-reset/audio/motion-score.mp3'
    longform = ROOT/'videos/2026-11-11-ai-va-cong-viec-5phut/audio'
    # Reuse approved thematic stem, then move into an actual second composed score.
    # No duplicated narration and no repeated short visual/audio loop to fill time.
    score = audio/'score-assembled.wav'
    second = longform/('analysis-score.mp3' if direction=='long' else 'agency-score.mp3')
    run([FF, '-y', '-v', 'error', '-i', str(approved), '-i', str(second),
         '-filter_complex', '[0:a]atrim=0:30,asetpts=PTS-STARTPTS[a];[1:a]asetpts=PTS-STARTPTS[b];[a][b]acrossfade=d=3:c1=qsin:c2=qsin[out]',
         '-map','[out]', '-t',str(seconds), '-ar','48000','-ac','2', str(score)])
    if duration(score)+.05 < seconds:
        raise ValueError('Composed music too short, do not silently loop')
    cues = []
    def at(phrase):
        matches = [s for s in data['shots'] if s['phrase']==phrase]
        if len(matches)!=1:
            raise ValueError('Ambiguous/missing sound cue '+phrase)
        return matches[0]['start']/30
    for file, phrase in ([('typing.mp3','Bạn giao cho AI'), ('paper.mp3','Sau khi viết'),
                         ('confirm.mp3','Ghi lại thời gian')] if direction=='long' else
                        [('paper.mp3','Nhưng khi một con số'), ('typing.mp3','Hôm nay'),
                         ('confirm.mp3','Chỉ giữ cách làm')]):
        shutil.copy2(longform/file, audio/file)
        receipt = (longform/file).with_suffix('.receipt.json')
        if receipt.exists():
            shutil.copy2(receipt, (audio/file).with_suffix('.receipt.json'))
        cues.append({'file':file,'time':at(phrase)+.15,'phrase':phrase})
    inputs = [FF,'-y','-v','error','-i',str(audio/'narration-original.mp3'),'-i',str(score)]
    # Match the approved speech-first mix recipe. Natural narration speed remains 1.0.
    graph = ['[0:a]highpass=f=70,loudnorm=I=-16:TP=-2:LRA=8,asplit=2[v][key]',
             f'[1:a]loudnorm=I=-27:TP=-7:LRA=8,afade=t=in:d=0.6,afade=t=out:st={seconds-3}:d=3[m]',
             '[m][key]sidechaincompress=threshold=0.025:ratio=3:attack=18:release=260:makeup=1[duck]']
    labels = ['[v]','[duck]']
    for i, cue in enumerate(cues):
        p = audio/cue['file']
        inputs += ['-i',str(p)]
        delay = round(cue['time']*1000)
        graph.append(f'[{i+2}:a]highpass=f=100,loudnorm=I=-31:TP=-9:LRA=5,afade=t=in:d=0.06,afade=t=out:st={max(.1,duration(p)-.25):.3f}:d=0.25,adelay={delay}|{delay}[fx{i}]')
        labels.append(f'[fx{i}]')
    graph.append(''.join(labels)+f'amix=inputs={len(labels)}:duration=longest:normalize=0,alimiter=limit=0.89:level=false,apad=whole_dur={seconds}[out]')
    final = audio/'final-mix.wav'
    run(inputs+['-filter_complex',';'.join(graph),'-map','[out]','-t',str(seconds),'-ar','48000','-ac','2',str(final)])
    shutil.copy2(final, PUB/'directions'/direction/'mix.wav')
    save(batch/'sound-cues.json',cues)
    measured = run([FF,'-hide_banner','-i',str(final),'-af','loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json','-f','null','-'])
    report = json.loads(re.findall(r'\{\s*"input_i".*?\}',measured.stderr.decode('utf-8',errors='replace'),re.S)[-1])
    save(audio/'mix-report.json',report)
    save(batch/'audio-sources.json', {
        'narration':{'file':'audio/narration-original.mp3','sha256':sha(audio/'narration-original.mp3'),
                     'alignment':'audio/narration-original.alignment.json','speed':1.0},
        'music':[{'file':str(p.relative_to(ROOT)).replace('\\','/'),'sha256':sha(p)} for p in [approved,second]],
        'mix':{'file':'audio/final-mix.wav','sha256':sha(final),'seconds':duration(final)},
        'contextualFoley':cues, 'humanListening':'Not claimed; exact take alignment and measurements only',
    })
    print('MIX_READY',direction,seconds,report,flush=True)

if __name__=='__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['plan','voice','prepare','mix','render-assets','all'])
    parser.add_argument('--direction',choices=['long','hidden','both'],default='both')
    parser.add_argument('--batch',type=Path,default=DEFAULT)
    parser.add_argument('--profile',type=Path,help='Original content manifest for another topic; use one matching --direction')
    args = parser.parse_args()
    if args.profile and args.direction=='both':
        parser.error('--profile requires --direction long or hidden')
    for direction in (['long','hidden'] if args.direction=='both' else [args.direction]):
        if args.action=='all':
            voice(direction,args.batch,args.profile)
            prepare(direction,args.batch,args.profile)
            mix(direction,args.batch,args.profile)
        else:
            globals()[args.action.replace('-','_')](direction,args.batch,args.profile)
