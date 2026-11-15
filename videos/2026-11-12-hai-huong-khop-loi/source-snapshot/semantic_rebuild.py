"""Prepare a clause-led rebuild from immutable exact-take audio and reviewed sources.

This validates timing/design coverage. Only inspection of rendered phrase/frame
pairs can establish whether the image actually conveys the narrated operation.
"""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import unicodedata

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = Path(__file__).parent
DEFAULT = ROOT / 'videos/2026-11-12-hai-huong-khop-loi'
PUBLIC = WORKFLOW / 'cinematic/public/semantic'


def load(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prepare(base):
    source_images = load(base / 'source-images.json')
    allowed = {}
    for record in source_images:
        if record.get('reviewDecision') != 'accepted':
            continue
        origin = base / record['file']
        if sha(origin) != record['sha256']:
            raise ValueError('Reviewed photo bytes changed: ' + record['id'])
        target = PUBLIC / 'assets' / origin.name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(origin, target)
        allowed[record['id']] = {'file': 'semantic/assets/' + origin.name,
                                'aspect': record['width'] / record['height'],
                                'credit': record['creator'] + ' / Pexels', 'focus': [50, 50]}
    for direction in ['long', 'hidden']:
        profile = load(WORKFLOW / f'semantic-profiles/{direction}.json')
        source = ROOT / profile['sourceBatch']
        old = load(source / 'data.json')
        words = load(source / 'aligned-words.json')
        shots = profile['shots']
        if [*dict.fromkeys(s['phase'] for s in shots)] != ['hook', 'disclaimer', 'content', 'cta']:
            raise ValueError('Four phases missing or out of order')
        cursor = 0
        runtime = []
        for index, shot in enumerate(shots):
            required = ['id', 'narratedText', 'narratedMeaning', 'requiredVisual', 'visibleFacts', 'forbiddenSubstitute', 'proof', 'semanticContract']
            if any(not shot.get(field) for field in required):
                raise ValueError('Missing semantic contract: ' + str(shot.get('id')))
            if shot['startWordIndex'] != cursor:
                raise ValueError('Narration clause skipped/duplicated: ' + shot['id'])
            end = shot['endWordIndexExclusive']
            exact = ' '.join(word['text'] for word in words[cursor:end])
            if unicodedata.normalize('NFC', exact) != unicodedata.normalize('NFC', shot['narratedText']):
                raise ValueError('Narrated text differs from the measured take: ' + shot['id'])
            if index and shots[index - 1]['end'] != shot['start']:
                raise ValueError('Timeline gap/overlap')
            if shot['end'] <= shot['start']:
                raise ValueError('Empty shot')
            cursor = end
            row = {**shot, 'visible': shot['visibleFacts'], 'proof': shot['requiredVisual']}
            # Media can support the literal operation but never stand in for it.
            asset = 'typing-hands' if shot['scene'] == 'email_prompt' else 'lamp-desk' if shot['scene'] == 'product_facts' else None
            if asset and asset in allowed:
                row['asset'] = allowed[asset]
            runtime.append(row)
        if cursor != len(words) or shots[0]['start'] != 0 or shots[-1]['end'] != old['frames']:
            raise ValueError('Measured narration/runtime is not fully covered')
        facts = profile['caseFacts']
        example = {'productName': facts['product'], 'sourceFeature': facts['sourceFeature'],
                   'unsupportedFeature': facts['unsupportedFeature'], 'sourcePriceVND': facts['sourcePriceVND'],
                   'draftPriceVND': facts['draftPriceVND'], 'baselineMinutes': facts['baselineMinutes'],
                   'writeMinutes': facts['aiWriteMinutes'], 'repairMinutes': facts['aiFixMinutes']}
        data = {'direction': direction, 'fps': old['fps'], 'frames': old['frames'],
                'title': profile['title'], 'audio': f'semantic/{direction}/mix.wav',
                'captions': old['captions'], 'shots': runtime, 'example': example}
        batch = base / direction
        batch.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source / 'audio/final-mix.wav', batch / 'mix.wav')
        destination = PUBLIC / direction
        destination.mkdir(parents=True, exist_ok=True)
        shutil.copy2(batch / 'mix.wav', destination / 'mix.wav')
        for name in ['script.txt', 'aligned-words.json']:
            shutil.copy2(source / name, batch / name)
        save(batch / 'data.json', data)
        save(batch / 'props.json', {'data': data})
        save(batch / 'storyboard.json', profile)
        save(destination / 'data.json', data)
        save(batch / 'preflight.json', {'frames': old['frames'], 'shots': len(shots), 'wordsCovered': cursor,
             'allWordsCoveredExactlyOnce': True, 'audioSHA256': sha(batch / 'mix.wav'),
             'sourceAudioSHA256': sha(source / 'audio/final-mix.wav'), 'voiceRegenerated': False,
             'semanticDesignPresent': True, 'actualVisualReview': 'pending rendered phrase/frame evidence',
             'userAcceptance': 'pending'})
        print('PREPARED', direction, len(shots), 'clauses', cursor, 'words', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--batch', type=Path, default=DEFAULT)
    prepare(parser.parse_args().batch)
