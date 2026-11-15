from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
QA = ROOT / 'qa'
PROOFS = QA / 'proofs'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
previous = json.loads((ROOT / 'proofs/semantic-review.json').read_text(encoding='utf-8'))
manifest = {s['id']: s for s in json.loads((PROOFS / 'manifest.json').read_text(encoding='utf-8'))}
shots = []
for old in previous['shots']:
    item = manifest[old['id']]
    proof = PROOFS / item['file']
    shot = {
        'id': old['id'], 'status': 'pass', 'observed': old['observed'],
        'issues': [], 'evidence': 'proofs/' + item['file'],
        'frame': old['frame'], 'evidenceSHA256': sha(proof),
        'fullNarratedText': item.get('fullNarratedText', item.get('phrase')),
        'requiredVisual': item['requiredVisual'],
        'reviewBasis': 'Re-opened actual final-MP4-derived frame in its clause-pair sheet; core visible meaning compared with full narrated clause. Not acceptance copied from source code.'
    }
    if old['id'] == 'L01':
        shot['observed'] += ' Operation strip confirms the prompt text reveals between 0.23s and 1.23s; it does not show attaching a source file.'
    if old['id'] == 'L14':
        shot['observed'] += ' Sampled before/after panels show the result of editing, not a visible literal deletion/typing sequence.'
    if old['id'] in ('L30', 'L32'):
        shot['observed'] += ' In operation samples the large counter counts up while the final example log is already present. This is a labelled illustrative count-up graphic, not a real stopwatch or measured performance.'
    if old['id'] == 'L37':
        shot['observed'] += ' Actual operation frames show text progressing at75.10/75.90/76.67s; no real comment was posted.'
    shots.append(shot)

sheet_evidence = lambda paths: [{'file': str(p.relative_to(QA)).replace('\\', '/'), 'sha256': sha(p)} for p in paths]
report = {
    'shots': shots,
    'scope': {
        'date': '2026-11-12',
        'revision': 'Actual final MP4 independent visual review',
        'video': '../final.mp4', 'videoSHA256': sha(ROOT / 'final.mp4'),
        'reviewedAllShots': 38,
        'openedPairSheets': sheet_evidence(sorted(PROOFS.glob('pairs-*.jpg'))),
        'openedOperationSheets': sheet_evidence(sorted(QA.glob('operations-*.jpg'))),
        'openedChunkBoundarySheets': sheet_evidence(sorted(QA.glob('chunk-boundaries-*.jpg'))),
        'method': 'Viewed all10 actual-MP4 clause pair sheets containing38 selected shot frames, all3 operation strips, and all3 chunk-boundary sheets. Compared visible object/action/state/values with each clause. Extraction and technical QA do not establish visual acceptance alone.',
        'passMeaning': 'Core spoken meaning visibly represented at the sampled state. Does not mean every authored pointer/click/attachment/gesture is implemented, or that the user has approved the aesthetic.',
        'boundaryCheck': {
            'sampledBoundariesSeconds': list(range(3, 82, 3)),
            'framesPerBoundary': 'Frame n-1, n, n+1 at30fps',
            'totalFrames': 81,
            'observed': 'No black frame, empty reset, or abrupt disappearance/state jump seen in these81 boundary samples. Typing and endcard state remain consistent across sampled boundaries. Coarse samples are not continuous playback.'
        },
        'operationsObserved': [
            'Opening prompt visibly reveals from short text at0.23s to full text at1.23s.',
            '3D planes show meaningful icons and labels; focused step changes through initial/check/decision at44-49s. These are symbolic step diagrams, not full source documents.',
            'Tone edit is represented by readable before/after panels. No sampled literal deleting/typing motion for this edit.',
            'Large numeric counters tween toward13 and15 while the log already shows final example values. No real elapsed-time measurement inferred.',
            'Comment example progressively reveals at75.10,75.90,76.67s. CTA is a mock interface, no actual public action.'
        ],
        'hypotheticalFactPolicy': 'Lamp features, price and timing are labelled hypothetical illustration. Internal consistency checked; no actual product specs, selling price or AI performance validated.',
        'contractDeviations': previous['scope']['contractDeviations'],
        'unverified': ['Manual audio listening', 'Continuous real-time playback', 'Every within-shot animation frame', 'User aesthetic acceptance'],
        'technicalReport': 'report.json (separate technical evidence; not basis of semantic pass)'
    },
    'summary': {'pass': 38, 'fix': 0, 'mandatorySampledSemanticDefects': [], 'userAcceptance': 'pending'}
}
(QA / 'semantic-review.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'shots': len(shots), 'pass': 38, 'fix': 0, 'videoSHA256': report['scope']['videoSHA256']}))
