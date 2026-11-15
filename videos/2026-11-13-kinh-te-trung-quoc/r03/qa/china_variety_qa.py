"""Reuse complete China technical QA while sampling every authored variety shot.

Coverage and authoring labels are mechanical evidence only. A unique mechanic
string, decoded movie or populated contact sheet cannot establish visual variety.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
from unittest.mock import patch

import china_qa as base

_legacy_capture_plan = base.capture_plan
FRACTIONS = (.08, .29, .50, .71, .92)


def capture_plan(data):
    plan = _legacy_capture_plan(data)
    motion = []
    for index, shot in enumerate(data['shots']):
        name = base.safe_name(shot.get('id', f'shot-{index + 1:02}'))
        motion.append({'shot': shot.get('id', name), 'layout': shot['layout'],
            'module': shot.get('variety', {}).get('module'),
            'mechanic': shot.get('variety', {}).get('mechanic'),
            'samples': [{'frame': shot['start'] + round((shot['end'] - shot['start'] - 1) * fraction),
                         'fraction': fraction, 'file': f'temporal/{name}-{j + 1}.jpg'}
                        for j, fraction in enumerate(FRACTIONS)],
            'strip': f'temporal/{name}-strip.jpg'})
    plan['temporal'] = motion
    plan['scope'] = 'Every authored shot, including media, disclaimer and closing; five samples per shot.'
    return plan


def mechanic_plan(data):
    shots = []
    for shot in data['shots']:
        v = shot.get('variety', {})
        base.require(isinstance(v.get('module'), str) and v['module'].strip()
                     and isinstance(v.get('mechanic'), str) and v['mechanic'].strip(),
                     'Every variety shot needs authored module/mechanic metadata: ' + str(shot.get('id')))
        shots.append({'id': shot.get('id'), 'start': shot['start'], 'end': shot['end'],
                      'layout': shot['layout'], 'module': v['module'], 'mechanic': v['mechanic'],
                      'narration': shot.get('text', ''), 'actualRenderedReview': 'pending'})
    return {'schema': 'china-variety-mechanic-plan/1',
        'createdUTC': datetime.now(timezone.utc).isoformat(),
        'shots': shots, 'moduleCounts': dict(Counter(s['module'] for s in shots)),
        'authoredMechanicLabels': len(set(s['mechanic'] for s in shots)),
        'scope': 'Authoring inventory only; label uniqueness is not proof of aesthetic diversity, motion or clause relevance.',
        'actualRenderedReview': 'pending', 'userAcceptance': 'pending'}


def inspect(batch, *, revision=None, video=None):
    root = Path(batch).resolve()
    folder = base.revision_folder(root, revision)
    data = base.load(folder / 'data.json')
    out = folder / 'qa'
    base.save(out / 'mechanic-plan.json', mechanic_plan(data))
    # Revisions carry their own receipts and isolated production-public folder.
    # Base source/font/caption/branding/decode/audio gates remain enabled.
    with patch.object(base, 'capture_plan', capture_plan):
        report = base.inspect(folder, video=video)
    base.require(report['evidence']['temporalShots'] == len(data['shots']),
                 'Temporal evidence did not cover every authored variety shot')
    report.update({'schema': 'china-variety-video-qa/1', 'revision': revision,
        'rootSourceBatch': str(root), 'qaWrapperSHA256': base.sha(Path(__file__)),
        'qaBaseSHA256': base.sha(Path(base.__file__)),
        'varietyScope': 'All-shot evidence capture plus mechanical authoring inventory; actual motion/diversity/semantic review is pending.',
        'actualRenderedDiversityReview': 'pending', 'aestheticAcceptance': 'pending user feedback'})
    report['evidence'].update({'temporalLayoutScope': 'all authored shots regardless of layout',
        'temporalSamplesPerShot': len(FRACTIONS), 'mechanicPlan': 'mechanic-plan.json'})
    base.save(out / 'report.json', report)
    (out / 'china_variety_qa.py').write_bytes(Path(__file__).read_bytes())
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--batch', type=Path, required=True)
    parser.add_argument('--revision')
    args = parser.parse_args()
    print(json.dumps(inspect(args.batch, revision=args.revision), ensure_ascii=False, indent=2))
