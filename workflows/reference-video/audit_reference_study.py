"""Audit the saved reference library's files, hashes and contiguous report coverage."""
import argparse
import hashlib
import json
from pathlib import Path


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def digest(path):
    value = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            value.update(chunk)
    return value.hexdigest()


def audit(root):
    records, failures = [], []
    folders = [p for p in root.iterdir() if p.is_dir() and (p / 'metadata.json').exists()]
    for folder in folders:
        record = {'id': folder.name, 'errors': []}
        try:
            meta = read(folder / 'metadata.json')
            media = read(folder / 'media-receipt.json')
            caption = read(folder / 'caption-receipt.json')
            sampling = read(folder / 'sampling-receipt.json')
            source = read(folder / 'study-blocks.json')
            analysis = read(folder / 'analysis.json')
            blocks = analysis['blocks']
            assert (folder / 'analysis.md').stat().st_size > 1000, 'Missing authored report'
            assert any((folder / name).is_file() for name in ['script-pattern.md', 'scriptpattern.md']), 'Missing script pattern'
            assert len(blocks) == len(source), 'Incomplete analysis blocks'
            assert blocks[0]['start'] == 0 and blocks[-1]['end'] == meta['duration'], 'Missing report start/end'
            for item, expected in zip(blocks, source):
                assert item['start'] == expected['start'] and item['end'] == expected['end'], 'Analysis block differs from evidence interval'
            for first, second in zip(blocks, blocks[1:]):
                assert first['end'] == second['start'], 'Gap or overlap in analysis blocks'
            sheets = [name for block in source for name in block['sheets']]
            assert all((folder / name).is_file() for name in sheets), 'Missing contact sheet'
            frames = sum(len(block['frames']) for block in source)
            assert frames == sampling['selected_frames'], 'Sampling count mismatch'
            assert digest(folder / 'reference.mp4') == media['sha256'], 'MP4 bytes changed'
            assert digest(folder / 'captions.json3') == caption['sha256'], 'Raw caption bytes changed'
            assert media['full_av_decode'] == 'passed', 'No successful AV decode receipt'
            assert any('Audio:' in s for s in media['streams']), 'No audio stream receipt'
            assert len(read(folder / 'transcript.json')) == caption['rows'], 'Caption row count mismatch'
            beats = analysis.get('semantic_beats') or [beat for block in blocks for beat in block.get('beats', [])]
            record.update({'title': meta['title'], 'channel': meta['channel'],
                'url': meta.get('url', f'https://www.youtube.com/watch?v={folder.name}'),
                'duration_seconds': meta['duration'], 'media': f'{folder.name}/reference.mp4',
                'media_bytes': media['bytes'], 'media_sha256': media['sha256'],
                'full_av_decode': media['full_av_decode'], 'analysis_blocks': len(blocks),
                'caption_rows': caption['rows'], 'sheets': len(sheets), 'sampled_frames': frames,
                'authored_semantic_beats': len(beats), 'analysis': f'{folder.name}/analysis.md',
                'script_pattern': next(f'{folder.name}/{name}' for name in ['script-pattern.md', 'scriptpattern.md'] if (folder / name).exists()),
                'review_method': 'Complete captions and all indexed contact sheets; selected native frames as documented per report.',
                'continuous_av_playback': False, 'auditory_approval': False})
        except (AssertionError, KeyError, OSError, ValueError) as error:
            record['errors'].append(str(error))
            failures.append({'id': folder.name, 'error': str(error)})
        records.append(record)
    totals = {key: sum(x.get(key, 0) for x in records) for key in
              ['duration_seconds', 'analysis_blocks', 'caption_rows', 'sheets', 'sampled_frames', 'authored_semantic_beats']}
    result = {'study_date': '2026-11-13', 'status': 'passed' if not failures and len(records) == 4 else 'incomplete',
        'scope': 'File integrity and saved analysis/evidence coverage, not aesthetic, auditory or fact-verification approval.',
        'records': records, 'totals': totals, 'failures': failures,
        'limits': ['Sampled-image review is not continuous watching/listening.',
                   'Semantic beat boundaries use captions and sampled frames, not a frame-accurate EDL.',
                   'Audience and attention interpretations have no private analytics backing.',
                   'Reference claims are not independently verified by this coverage audit.']}
    (root / 'REVIEW_COVERAGE.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    (root / 'catalog.json').write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'status': result['status'], 'totals': totals, 'failures': failures}, ensure_ascii=False))
    return result['status'] == 'passed'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    args = parser.parse_args()
    raise SystemExit(0 if audit(args.root) else 1)
