"""Prepare original, inspected photo/gallery films and run resumable serial batches.

Machine checks establish integrity and timing, never semantic or aesthetic approval.
No content is copied from a reference and no call retrains model weights.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import unicodedata

from PIL import Image, ImageOps

WORKFLOW = Path(__file__).resolve().parent
ROOT = WORKFLOW.parents[1]
VOICE = '6adFm46eyy74snVn6YrT'
PHASES = ['hook', 'disclaimer', 'content', 'cta']
LAYOUTS = {'full', 'diptych', 'gallery3d', 'evidence', 'closing', 'graphic'}
ROLES = {'evidence', 'context', 'mechanism', 'metaphor'}
STEPS = ['plan', 'check', 'voice', 'prepare', 'mix', 'render']


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def save(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.partial')
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')
    temporary.replace(path)


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def normalized_words(text):
    return [re.sub(r'[^\w]', '', unicodedata.normalize('NFC', word).lower())
            for word in text.split() if re.sub(r'[^\w]', '', word)]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def within(root, path):
    root, path = Path(root).resolve(), Path(path).resolve()
    require(path.is_relative_to(root), 'Path leaves its declared root: ' + str(path))
    return path


def local_file(root, value):
    require(nonempty(value) and not Path(value).is_absolute(), 'Use a relative local file path')
    return within(root, Path(root) / value)


def writing_text(manifest):
    return '\n\n'.join(section['text'] for section in manifest['sections'])


def validate_structure(manifest):
    require(manifest.get('schema') == 'reference-video-production/1', 'Unsupported production manifest schema')
    require(re.fullmatch(r'[a-z0-9][a-z0-9-]{1,79}', manifest.get('id', '')), 'Use a stable lowercase production id')
    require(manifest.get('direction') in ['long', 'hidden'], 'Direction must be long or hidden')
    require(manifest.get('renderOptions', {}).get('memoryProfile', 'default') in ['default', 'bounded'],
            'renderOptions.memoryProfile must be default or bounded')
    for field in ['title', 'editorialAngle', 'audience', 'hookPromise', 'payoff']:
        require(nonempty(manifest.get(field)), 'Missing writing brief field: ' + field)
    require([s.get('phase') for s in manifest.get('sections', [])] == PHASES,
            'Exactly hook → disclaimer → content → CTA sections are required')
    assets = manifest.get('assets', [])
    require(isinstance(assets, list) and assets, 'The new topic requires its own asset catalog')
    by_id = {}
    for asset in assets:
        key = asset.get('id', '')
        require(bool(re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9_-]*', key)), 'Invalid asset id')
        require(key not in by_id, 'Duplicate asset id: ' + key)
        by_id[key] = asset
    shot_ids, used = set(), set()
    for section in manifest['sections']:
        require(nonempty(section.get('text')), 'Empty section narration: ' + section['phase'])
        require(section.get('shots'), 'Every section needs a storyboard')
        clauses = []
        for shot in section['shots']:
            key = shot.get('id', '')
            require(nonempty(key) and key not in shot_ids, 'Missing or repeated shot id: ' + key)
            shot_ids.add(key)
            require(shot.get('layout') in LAYOUTS, 'Unsupported retained-interface layout: ' + key)
            require(shot.get('mediaRole') in ROLES, 'Missing explicit media role: ' + key)
            for field in ['phrase', 'narrationClause', 'needToSee', 'supports', 'limits']:
                require(nonempty(shot.get(field)), 'Missing shot ' + field + ': ' + key)
            clause = normalized_words(shot['narrationClause'])
            phrase = normalized_words(shot['phrase'])
            require(phrase and clause[:len(phrase)] == phrase,
                    'Shot phrase must open its actual narration clause: ' + key)
            clauses += clause
            images = shot.get('images')
            require(isinstance(images, list) and images and len(set(images)) == len(images), 'Missing/repeated images: ' + key)
            require(all(image in by_id for image in images), 'Unknown asset in shot: ' + key)
            require(shot['layout'] != 'diptych' or len(images) >= 2, 'Diptych needs two images: ' + key)
            require(shot['layout'] != 'gallery3d' or len(images) >= 2, 'Gallery needs at least two distinct images: ' + key)
            if shot['mediaRole'] == 'evidence':
                require(any(by_id[image].get('source', {}).get('kind') == 'evidence' for image in images),
                        'Evidence narration cannot be proven by illustrative stock: ' + key)
                require(shot.get('sourceIds'), 'Evidence shot must cite research source ids: ' + key)
            used.update(images)
        require(clauses == normalized_words(section['text']),
                'Storyboard clauses must account for every narration word, once and in order: ' + section['phase'])
    sources = manifest.get('researchSources', [])
    source_ids = {source.get('id') for source in sources}
    require(len(source_ids) == len(sources), 'Duplicate research source id')
    for source in sources:
        require(nonempty(source.get('id')) and str(source.get('url', '')).startswith('https://'), 'Research source needs id and HTTPS URL')
    for section in manifest['sections']:
        for shot in section['shots']:
            require(all(key in source_ids for key in shot.get('sourceIds', [])), 'Unknown research source id in ' + shot['id'])
    for claim in manifest.get('claims', []):
        require(nonempty(claim.get('id')) and nonempty(claim.get('text')), 'Claim requires id and text')
        require(claim.get('sourceIds') and all(key in source_ids for key in claim['sourceIds']), 'Claim requires known research source ids')
        require(nonempty(claim.get('scope')) and nonempty(claim.get('limitations')), 'Claim requires scope and limitations')
    return by_id, used


def inspected_record(record, expected_hash, label):
    require(record.get('status') == 'inspected', 'Actual inspection remains pending: ' + label)
    require(nonempty(record.get('reviewer')) and nonempty(record.get('observations')), 'Inspection needs reviewer and actual observations: ' + label)
    require(record.get('sha256') == expected_hash, 'Inspection does not cover current file bytes: ' + label)


def validate_guidance(value):
    require(value.get('schema') == 'reference-video-guidance/1' and isinstance(value.get('lessons'), list),
            'Use a verified guidance export from learning.py')
    for lesson in value['lessons']:
        reviewer = lesson.get('verified_by', {})
        require(lesson.get('status') == 'verified' and nonempty(lesson.get('verification_id'))
                and isinstance(reviewer, dict) and reviewer.get('kind') in ['agent', 'human_user'] and nonempty(reviewer.get('name')),
                'Guidance cannot promote proposed or unverified lessons')
    return value


def pinned_guidance(folder, supplied=None):
    target = Path(folder) / 'learning-guidance.json'
    if target.exists():
        saved = load(target)
        validate_guidance(saved['content'])
        require(hashlib.sha256(saved['sourceText'].encode('utf-8')).hexdigest() == saved['sha256'], 'Pinned guidance bytes changed')
        require(json.loads(saved['sourceText'].lstrip('\ufeff')) == saved['content'], 'Pinned guidance text/content differs')
        if supplied:
            require(sha(supplied) == saved['sha256'], 'Batch guidance is already pinned; use a new revision for different lessons')
        return saved
    return None


def video_info(file):
    import cv2
    cap = cv2.VideoCapture(str(file))
    try:
        require(cap.isOpened(), 'Could not open selected video')
        fps = cap.get(cv2.CAP_PROP_FPS)
        size = [int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))]
        require(fps > 0 and min(size) > 0 and size[0] <= 2048 and size[1] <= 1280,
                'Use bounded landscape video derivatives (at most2048×1280) with positive FPS')
        count = 0
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            count += 1
        require(count > 0, 'Selected video contains no decoded frames')
        return {'fps': fps, 'dimensions': size, 'decodedFrames': count,
                'timelineFrames': math.floor(count / fps * 30 + 1e-6)}
    finally:
        cap.release()


def check(manifest_path, batch, guidance=None):
    path = Path(manifest_path).resolve()
    manifest = load(path)
    assets, used = validate_structure(manifest)
    files = {}
    for key in sorted(used):
        asset = assets[key]
        file = local_file(path.parent, asset.get('file'))
        require(file.is_file(), 'Missing source asset: ' + key)
        current_hash = sha(file)
        require(asset.get('sha256') == current_hash, 'Source asset differs from catalog: ' + key)
        source = asset.get('source', {})
        require(source.get('kind') in ['stock', 'evidence', 'original'], 'Unknown source role: ' + key)
        for field in ['url', 'creator', 'license', 'licenseURL']:
            require(nonempty(source.get(field)), 'Source requires ' + field + ': ' + key)
        if source['kind'] != 'original':
            require(source['url'].startswith('https://') and source['licenseURL'].startswith('https://'), 'External source and license must have HTTPS receipts: ' + key)
        observed = asset.get('observed', {})
        for field in ['subject', 'action', 'objects', 'limits']:
            require(nonempty(observed.get(field)), 'Record what actual pixels show (' + field + '): ' + key)
        inspected_record(asset.get('inspection', {}), current_hash, key)
        crop = asset.get('crop', [0, 0, 1, 1])
        require(isinstance(crop, list) and len(crop) == 4 and all(isinstance(v, (int, float)) for v in crop), 'Invalid normalized crop: ' + key)
        require(0 <= crop[0] < crop[2] <= 1 and 0 <= crop[1] < crop[3] <= 1, 'Crop outside source: ' + key)
        focus = asset.get('focus', [50, 50])
        require(len(focus) == 2 and all(0 <= v <= 100 for v in focus), 'Focus outside frame: ' + key)
        require(asset.get('fit') in [None, 'contain', 'cover'], 'Asset fit must be contain or cover: ' + key)
        kind = asset.get('mediaType', 'image')
        require(kind in ['image', 'video'], 'Unsupported media type: ' + key)
        info = None
        if kind == 'video':
            require(crop == [0, 0, 1, 1], 'Prepare a separate bounded video crop before cataloging it')
            require(file.suffix.lower() == '.mp4', 'Video assets must be MP4 derivatives')
            info = video_info(file)
            available = asset.get('availableFrames', info['timelineFrames'])
            trim = asset.get('trimBeforeFrames', 0)
            require(isinstance(available, int) and isinstance(trim, int) and 0 <= trim < available <= info['timelineFrames'],
                    'Video available/trim frames exceed actual decoded duration: ' + key)
        else:
            with Image.open(file) as image:
                image.verify()
        files[key] = {'path': file, 'sha256': current_hash, 'catalog': asset, 'videoInfo': info}
    for section in manifest['sections']:
        for shot in section['shots']:
            review = shot.get('review', {})
            require(review.get('status') == 'inspected' and nonempty(review.get('reviewer')) and nonempty(review.get('observations')),
                    'Record an actual clause-to-image storyboard review: ' + shot['id'])
            expected = {key: files[key]['sha256'] for key in shot['images']}
            require(review.get('assetHashes') == expected, 'Storyboard review does not cover the exact selected assets: ' + shot['id'])
            for key in shot['images']:
                asset = files[key]['catalog']
                if asset.get('mediaType') == 'video' and shot['layout'] == 'gallery3d':
                    require(asset.get('posterFile') and asset.get('posterSHA256'), 'Video gallery needs an inspected poster derivative: ' + key)
                    poster = local_file(path.parent, asset['posterFile'])
                    require(sha(poster) == asset['posterSHA256'], 'Video poster differs from catalog: ' + key)
    folder = film_folder(manifest, batch)
    pinned = pinned_guidance(folder, guidance)
    if guidance:
        validate_guidance(load(guidance))  # Editorial rules are archived, not executable overrides.
        require(pinned or not (folder / 'production-manifest.json').exists(),
                'Cannot add guidance after planning this batch; use a new revision')
    return manifest, files


def film_folder(manifest, batch):
    return within(batch, Path(batch) / manifest['direction'])


def plan(manifest_path, batch, guidance=None):
    path, batch = Path(manifest_path).resolve(), Path(batch).resolve()
    manifest = load(path)
    validate_structure(manifest)
    folder = film_folder(manifest, batch)
    folder.mkdir(parents=True, exist_ok=True)
    snapshot = folder / 'production-manifest.json'
    require(not (folder / 'final.mp4').exists() or snapshot.exists(),
            'An older output already occupies this folder; use a new batch')
    existing_plan = snapshot.exists()
    require(not existing_plan or load(snapshot) == manifest,
            'This batch already retains a different manifest; use a new revision/batch')
    pinned = pinned_guidance(folder, guidance)
    if guidance:
        validate_guidance(load(guidance))
        require(pinned or not existing_plan, 'Cannot add guidance after planning this batch; use a new revision')
        if not pinned:
            # Preserve exact source newline bytes on Windows for the pinned hash.
            text = Path(guidance).read_bytes().decode('utf-8')
            pinned = {'file': str(Path(guidance).resolve()), 'sha256': sha(guidance), 'sourceText': text,
                'content': load(guidance), 'application': 'Editorial guidance only; no automatic style, voice or acceptance override.'}
            save(folder / 'learning-guidance.json', pinned)
    save(snapshot, manifest)
    (folder / 'script.txt').write_text(writing_text(manifest) + '\n', encoding='utf-8')
    save(folder / 'profile.json', manifest)
    save(folder / 'batch.json', {'id': manifest['id'], 'direction': manifest['direction'], 'title': manifest['title'],
        'structure': PHASES, 'voice': {'name': 'Nhật Phong', 'voice_id': VOICE, 'model_id': 'eleven_v3', 'language_code': 'vi',
            'speed': 1.0, 'stability': .5, 'similarity_boost': .8},
        'durationPolicy': 'Natural exact take plus at least one second tail; never truncate the final sentence or stretch voice.',
        'userAcceptance': 'pending', 'manifestSHA256': sha(path),
        'guidanceSHA256': pinned['sha256'] if pinned else None})
    return manifest, folder


def voice(manifest_path, batch, guidance=None):
    from eleven_audio import speech
    manifest, _ = check(manifest_path, batch, guidance)
    _, folder = plan(manifest_path, batch, guidance)
    speech(folder / 'audio/narration-original.mp3', writing_text(manifest), VOICE)
    return folder


def captions(aligned):
    result, part = [], []
    for word in aligned:
        candidate = ' '.join(row['text'] for row in part + [word])
        if part and (len(candidate) > 44 or word['end'] - part[0]['start'] > 2.8):
            result.append({'start': part[0]['start'], 'end': part[-1]['end'], 'text': ' '.join(row['text'] for row in part)})
            part = []
        part.append(word)
        if re.search(r'[.!?:]$', word['text']):
            result.append({'start': part[0]['start'], 'end': part[-1]['end'], 'text': ' '.join(row['text'] for row in part)})
            part = []
    if part:
        result.append({'start': part[0]['start'], 'end': part[-1]['end'], 'text': ' '.join(row['text'] for row in part)})
    return result


def prepare(manifest_path, batch, guidance=None):
    from documentary import duration
    from eleven_audio import words
    manifest, files = check(manifest_path, batch, guidance)
    _, folder = plan(manifest_path, batch, guidance)
    audio = folder / 'audio/narration-original.mp3'
    receipt = load(audio.with_suffix('.receipt.json'))
    require(sha(audio) == receipt['sha256'], 'Narration audio differs from provider receipt')
    payload = {'text': writing_text(manifest), 'model_id': 'eleven_v3', 'language_code': 'vi',
               'voice_settings': {'stability': .5, 'similarity_boost': .8, 'speed': 1.0}}
    endpoint = f'/v1/text-to-speech/{VOICE}/with-timestamps'
    request_hash = hashlib.sha256(json.dumps({'endpoint': endpoint, 'body': payload}, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    require(receipt.get('request_hash') == request_hash, 'Narration receipt must match this script and the pinned Vietnamese voice/settings')
    aligned = [word for word in words(load(audio.with_suffix('.alignment.json'))) if normalized_words(word['text'])]
    require(aligned and normalized_words(' '.join(row['text'] for row in aligned)) == normalized_words(writing_text(manifest)),
            'Exact narration alignment differs from complete final script')
    require(all(0 <= row['start'] < row['end'] for row in aligned), 'Invalid word timing')
    require(all(a['start'] <= b['start'] for a, b in zip(aligned, aligned[1:])), 'Word timings move backward')
    natural = duration(audio)
    require(aligned[-1]['end'] <= natural + .25, 'Alignment extends beyond actual audio')
    seconds, fps = math.ceil(max(natural, aligned[-1]['end']) + 1), 30
    frames = seconds * fps
    namespace = 'directions/' + manifest['direction']
    public = within(batch, Path(batch) / 'production-public' / namespace)
    public.mkdir(parents=True, exist_ok=True)
    sources, derivatives, rendered = [], [], {}
    for key, entry in files.items():
        asset, source = entry['catalog'], entry['path']
        # Preserve the selected derivative's name; the asset id is only the
        # public namespace. Raw clip-aisle.mp4 and clip-aisle-720p.mp4 may coexist.
        original = folder / 'assets' / source.name
        original.parent.mkdir(parents=True, exist_ok=True)
        if source.resolve() != original.resolve():
            require(not original.exists() or sha(original) == entry['sha256'], 'Retained original differs: ' + key)
            shutil.copy2(source, original)
        box = asset.get('crop', [0, 0, 1, 1])
        if asset.get('mediaType') == 'video':
            stored_size = before = size = entry['videoInfo']['dimensions']
            target = public / (key + '.mp4')
            shutil.copy2(source, target)
        else:
            with Image.open(source) as stored:
                stored_size = list(stored.size)
                oriented = ImageOps.exif_transpose(stored).convert('RGB')
                before = list(oriented.size)
                cropped = oriented.crop(tuple(round(v * before[i % 2]) for i, v in enumerate(box)))
                require(cropped.width > 0 and cropped.height > 0, 'Crop became empty: ' + key)
                cropped.thumbnail((2048, 1280), Image.Resampling.LANCZOS)
                target = public / (key + '.jpg')
                cropped.save(target, format='JPEG', quality=94)
                size = list(cropped.size)
        record = {'id': key, 'file': 'assets/' + original.name, 'sha256': entry['sha256'], 'bytes': original.stat().st_size,
            'width': before[0], 'height': before[1], 'creator': asset['source']['creator'], 'page': asset['source']['url'],
            'license': asset['source']['license'], 'licenseURL': asset['source']['licenseURL'],
            'role': asset['source']['kind'], 'observed': asset['observed'], 'inspection': asset['inspection']}
        sources.append(record)
        derivatives.append({'id': key, 'originalFile': record['file'], 'publicFile': namespace + '/' + target.name,
            'originalSHA256': entry['sha256'], 'publicSHA256': sha(target), 'originalStoredDimensions': stored_size,
            'orientedDimensions': before, 'publicDimensions': size, 'mediaType': asset.get('mediaType', 'image'),
            'method': {'exifTranspose': asset.get('mediaType') != 'video', 'crop': box,
                'thumbnailBounds': [2048, 1280], 'format': 'MP4 source copy' if asset.get('mediaType') == 'video' else 'JPEG', 'quality': 94}})
        rendered[key] = {'file': namespace + '/' + target.name, 'aspect': size[0] / size[1],
                         'focus': asset.get('focus', [50, 50]), 'credit': asset.get('credit', asset['source']['creator'])}
        if asset.get('fit'):
            rendered[key]['fit'] = asset['fit']
        if asset.get('mediaType') == 'video':
            rendered[key].update({'mediaType': 'video', 'trimBeforeFrames': asset.get('trimBeforeFrames', 0),
                'availableFrames': asset.get('availableFrames', entry['videoInfo']['timelineFrames']),
                'sourceFPS': entry['videoInfo']['fps']})
            if asset.get('posterFile'):
                poster = local_file(Path(manifest_path).parent, asset['posterFile'])
                require(sha(poster) == asset.get('posterSHA256'), 'Video poster hash changed')
                poster_target = public / (key + '-poster.jpg')
                with Image.open(poster) as image:
                    image = ImageOps.exif_transpose(image).convert('RGB')
                    image.thumbnail((2048, 1280), Image.Resampling.LANCZOS)
                    image.save(poster_target, quality=94)
                rendered[key]['posterFile'] = namespace + '/' + poster_target.name
                derivatives.append({'id': key + '-poster', 'publicFile': rendered[key]['posterFile'],
                    'publicSHA256': sha(poster_target), 'publicDimensions': list(image.size)})
    shots, phases, cursor = [], [], 0
    for section in manifest['sections']:
        for raw in section['shots']:
            clause_length = len(normalized_words(raw['narrationClause']))
            row = {key: value for key, value in raw.items() if key != 'images'}
            row.update({'start': 0 if not shots else round(aligned[cursor]['start'] * fps), 'phase': section['phase'],
                        'images': [rendered[key] for key in raw['images']]})
            if not phases or phases[-1]['phase'] != section['phase']:
                phases.append({'phase': section['phase'], 'start': row['start']})
            shots.append(row)
            cursor += clause_length
    require(cursor == len(aligned), 'Shot coverage differs from actual aligned words')
    for i, shot in enumerate(shots):
        shot['end'] = shots[i + 1]['start'] if i + 1 < len(shots) else frames
        require(shot['end'] > shot['start'], 'Word-aligned cuts produce a nonpositive shot: ' + shot['id'])
        if shot['layout'] != 'gallery3d':
            for asset in shot['images']:
                if asset.get('mediaType') == 'video':
                    # The retained Film overlaps neighbouring shots by seven frames.
                    require(shot['end'] - shot['start'] + (7 if i + 1 < len(shots) else 0) <= asset['availableFrames'] - asset['trimBeforeFrames'],
                            'Video cannot fill its narrated interval without looping/freezing: ' + shot['id'])
    for i, phase in enumerate(phases):
        phase['end'] = phases[i + 1]['start'] if i + 1 < len(phases) else frames
    data = {'direction': manifest['direction'], 'fps': fps, 'frames': frames, 'title': manifest['title'],
            'audio': namespace + '/mix.wav', 'shots': shots, 'captions': captions(aligned)}
    for name, value in [('data.json', data), ('props.json', {'data': data}), ('aligned-words.json', aligned),
                        ('shotlist.json', shots), ('phase-timing.json', phases), ('image-sources.json', sources),
                        ('render-assets.json', {'direction': manifest['direction'], 'assets': derivatives})]:
        save(folder / name, value)
    save(public / 'data.json', data)
    save(folder / 'preflight.json', {'technicalIntegrity': 'passed', 'frames': frames, 'seconds': seconds,
        'naturalVoiceSeconds': natural, 'lastWordEnd': aligned[-1]['end'], 'tempo': 1.0, 'shots': len(shots),
        'uniquePhotos': len(files), 'allNarrationWordsAligned': True, 'publicSource': str(public.parent.parent),
        'sourceInspections': 'Recorded actual inspections with matching hashes; machine checks do not establish their semantic truth.',
        'visualInspection': 'Rendered crop, text, timing and motion still require inspection.', 'userAcceptance': 'pending',
        'audioListening': 'Not established by preparation', 'manifestSHA256': sha(manifest_path)})
    if (folder / 'learning-guidance.json').exists():
        preflight = load(folder / 'preflight.json')
        preflight['guidanceSnapshotSHA256'] = sha(folder / 'learning-guidance.json')
        preflight['guidanceSourceSHA256'] = load(folder / 'learning-guidance.json')['sha256']
        save(folder / 'preflight.json', preflight)
    return folder


def audio_path(value, manifest_path):
    path = Path(value)
    if path.is_absolute():
        return within(ROOT, path)
    nearby = within(Path(manifest_path).parent, Path(manifest_path).parent / path)
    return nearby if nearby.is_file() else within(ROOT, ROOT / path)


def mix(manifest_path, batch, guidance=None):
    from documentary import FF, duration, run
    manifest, folder = plan(manifest_path, batch, guidance)
    data = load(folder / 'data.json')
    seconds = data['frames'] / data['fps']
    config = manifest.get('audio', {})
    music = config.get('music', [])
    require(music, 'Choose and inspect music stems in manifest.audio.music; no automatic unrelated topic music')
    inputs = [FF, '-y', '-v', 'error', '-i', str(folder / 'audio/narration-original.mp3')]
    stems = []
    for entry in music:
        path = audio_path(entry['file'], manifest_path)
        require(sha(path) == entry.get('sha256'), 'Music differs from selected stem receipt')
        inputs += ['-i', str(path)]
        stems.append({'file': str(path.relative_to(ROOT)).replace('\\', '/'), 'sha256': sha(path)})
    # Assemble selected full stems once. Never loop a short clip to fill the film.
    graph = ['[0:a]highpass=f=70,loudnorm=I=-16:TP=-2:LRA=8,asplit=2[v][key]']
    for i in range(len(music)):
        graph.append(f'[{i+1}:a]aresample=48000,aformat=channel_layouts=stereo,asetpts=PTS-STARTPTS[m{i}]')
    require(sum(duration(audio_path(entry['file'], manifest_path)) for entry in music) >= seconds,
            'Selected music is shorter than the film; provide a complete score instead of looping')
    label = '[m0]'
    for i in range(1, len(music)):
        graph.append(f'{label}[m{i}]acrossfade=d=3:c1=qsin:c2=qsin[cross{i}]')
        label = f'[cross{i}]'
    require(sum(duration(audio_path(entry['file'], manifest_path)) for entry in music) - 3 * (len(music) - 1) >= seconds,
            'Music after crossfades is shorter than the exact take')
    graph.append(f'{label}loudnorm=I=-27:TP=-7:LRA=8,afade=t=in:d=0.6,afade=t=out:st={max(0, seconds-3)}:d=3[m]')
    graph.append('[m][key]sidechaincompress=threshold=0.025:ratio=3:attack=18:release=260:makeup=1[duck]')
    labels, cues = ['[v]', '[duck]'], []
    for i, entry in enumerate(config.get('cues', [])):
        cue = audio_path(entry['file'], manifest_path)
        require(sha(cue) == entry.get('sha256'), 'Foley differs from selected stem receipt')
        require(nonempty(entry.get('role')), 'Foley must describe a relevant action/meaning')
        matches = [shot for shot in data['shots'] if shot['phrase'] == entry['phrase']]
        require(len(matches) == 1, 'Foley cue phrase is missing or ambiguous')
        at = matches[0]['start'] / 30 + entry.get('offsetSeconds', 0)
        require(0 <= at < seconds, 'Foley cue is outside the film')
        inputs += ['-i', str(cue)]
        graph.append(f'[{len(music)+i+1}:a]aresample=48000,aformat=channel_layouts=stereo,highpass=f=100,loudnorm=I=-31:TP=-9:LRA=5,adelay={round(at*1000)}|{round(at*1000)}[fx{i}]')
        labels.append(f'[fx{i}]')
        cues.append({**entry, 'time': at})
    graph.append(''.join(labels) + f'amix=inputs={len(labels)}:duration=longest:normalize=0,alimiter=limit=0.89:level=false,apad=whole_dur={seconds}[out]')
    final = folder / 'audio/final-mix.wav'
    run(inputs + ['-filter_complex', ';'.join(graph), '-map', '[out]', '-t', str(seconds), '-ar', '48000', '-ac', '2', str(final)])
    namespace = Path(batch) / 'production-public/directions' / manifest['direction']
    shutil.copy2(final, namespace / 'mix.wav')
    save(folder / 'sound-cues.json', cues)
    save(folder / 'audio-sources.json', {'narration': {'file': 'audio/narration-original.mp3',
        'sha256': sha(folder / 'audio/narration-original.mp3'), 'alignment': 'audio/narration-original.alignment.json', 'speed': 1.0},
        'music': stems, 'mix': {'file': 'audio/final-mix.wav', 'sha256': sha(final), 'seconds': duration(final)},
        'contextualFoley': cues, 'humanListening': 'Not claimed by the mixer; record actual listening separately.'})
    return folder


def render(manifest_path, batch, guidance=None):
    manifest, _ = check(manifest_path, batch, guidance)
    command = [sys.executable, str(WORKFLOW / 'render_directions.py'), '--batch', str(Path(batch).resolve()),
        '--direction', manifest['direction'], '--public-source', str(Path(batch).resolve() / 'production-public'),
        '--skip-existing']
    if manifest.get('renderOptions', {}).get('memoryProfile') == 'bounded':
        command += ['--memory-profile', 'bounded']
    subprocess.run(command, check=True)
    return film_folder(manifest, batch)


@contextmanager
def exclusive_lock(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        raise RuntimeError('Another job owns the queue lock; reconcile its process before resuming') from None
    with os.fdopen(fd, 'w') as stream:
        stream.write(str(os.getpid()))
    try:
        yield
    finally:
        path.unlink()


def output_files(step, folder):
    mapping = {'plan': ['production-manifest.json', 'script.txt', 'profile.json', 'batch.json'],
        'check': [], 'voice': ['audio/narration-original.mp3', 'audio/narration-original.receipt.json', 'audio/narration-original.alignment.json'],
        'prepare': ['data.json', 'props.json', 'shotlist.json', 'render-assets.json', 'preflight.json'],
        'mix': ['audio/final-mix.wav', 'audio-sources.json'], 'render': ['final.mp4', 'qa/report.json']}
    names = mapping[step] + (['learning-guidance.json'] if step == 'plan' and (folder / 'learning-guidance.json').exists() else [])
    return {str(Path(name)): sha(folder / name) for name in names}


def queue(queue_path, retry_failed=False, guidance=None):
    path = Path(queue_path).resolve()
    config = load(path)
    require(config.get('schema') == 'reference-video-queue/1', 'Unsupported queue schema')
    require(config.get('jobs'), 'Queue contains no jobs')
    state_path = path.with_suffix('.state.json')
    state = load(state_path) if state_path.exists() else {'schema': 'reference-video-queue-state/1', 'jobs': {}}
    jobs = config['jobs']
    require(len({job.get('id') for job in jobs}) == len(jobs), 'Duplicate queue job id')
    with exclusive_lock(path.with_suffix('.lock')):
        for job in jobs:
            require(nonempty(job.get('id')), 'Queue job needs id')
            manifest_path = local_file(path.parent, job['manifest'])
            batch = local_file(path.parent, job['batch'])
            manifest = load(manifest_path)
            validate_structure(manifest)
            steps = job.get('steps', ['plan', 'check', 'prepare'])
            require(steps and all(step in STEPS for step in steps) and len(set(steps)) == len(steps), 'Invalid queue steps')
            require(steps == sorted(steps, key=STEPS.index), 'Queue steps must follow production order')
            fingerprint = hashlib.sha256(json.dumps({'manifest': sha(manifest_path), 'batch': str(batch), 'steps': steps,
                'guidance': sha(guidance) if guidance else None}, sort_keys=True).encode()).hexdigest()
            entry = state['jobs'].setdefault(job['id'], {'fingerprint': fingerprint, 'steps': {}, 'status': 'pending'})
            require(entry['fingerprint'] == fingerprint, 'Queued content changed; use a new job id/revision')
            folder = film_folder(manifest, batch)
            for step in steps:
                old = entry['steps'].get(step)
                if old and old['status'] == 'completed':
                    require(all((folder / name).is_file() and sha(folder / name) == digest for name, digest in old['outputs'].items()),
                            'Completed queue output changed; inspect before a new revision: ' + step)
                    # Even a resumed check must detect source corruption and stale inspection hashes.
                    if step == 'check':
                        check(manifest_path, batch, guidance)
                    continue
                require(not old or old['status'] == 'pending' or retry_failed,
                        'Failed/interrupted step needs explicit --retry-failed after inspection: ' + step)
                entry['status'] = 'running'
                entry['steps'][step] = {'status': 'running', 'attempt': (old or {}).get('attempt', 0) + 1,
                    'startedUTC': datetime.now(timezone.utc).isoformat()}
                save(state_path, state)
                try:
                    globals()[step](manifest_path, batch, guidance)
                    entry['steps'][step].update({'status': 'completed', 'outputs': output_files(step, folder)})
                    save(state_path, state)
                except Exception as error:
                    entry['status'] = 'failed'
                    entry['steps'][step].update({'status': 'failed', 'errorType': type(error).__name__, 'error': str(error)})
                    save(state_path, state)
                    raise
            entry['status'] = 'completed'
            entry['userAcceptance'] = 'pending'
            save(state_path, state)
    return state


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=STEPS + ['queue'])
    parser.add_argument('--manifest', type=Path)
    parser.add_argument('--batch', type=Path)
    parser.add_argument('--guidance', type=Path)
    parser.add_argument('--queue', type=Path, dest='queue_file')
    parser.add_argument('--retry-failed', action='store_true')
    args = parser.parse_args()
    if args.action == 'queue':
        if not args.queue_file:
            parser.error('queue requires --queue')
        result = queue(args.queue_file, args.retry_failed, args.guidance)
    else:
        if not args.manifest or not args.batch:
            parser.error('Every production action requires --manifest and --batch')
        result = globals()[args.action](args.manifest, args.batch, args.guidance)
    print(json.dumps({'action': args.action, 'status': 'completed', 'userAcceptance': 'pending'}, ensure_ascii=False))
