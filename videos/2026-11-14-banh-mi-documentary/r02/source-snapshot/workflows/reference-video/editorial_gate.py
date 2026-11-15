"""Check a chapter argument map before NEW explainer narration is purchased.

This checks coverage, exact text and a declared editorial review. It cannot judge
whether an argument is compelling or substitute for reading/listening feedback.
Existing exact audio and cache hits remain reusable without changing old batches.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import unicodedata

SCHEMA = 'reference-video-editorial/1'
DIMENSIONS = {'structure', 'focus', 'evidence', 'progression', 'payoff', 'spokenNaturalness'}
PHASES = ['hook', 'disclaimer', 'content', 'cta']
STRUCTURE_POLICIES = {
    'hook-disclaimer-content-cta': PHASES,
    'no-spoken-disclaimer-user-requested': ['hook', 'content', 'cta'],
}


def words(value):
    return re.findall(r'\w+', unicodedata.normalize('NFC', value).casefold())


def exact_text(value):
    """Allow spacing changes only; punctuation can change numbers and delivery."""
    return ' '.join(unicodedata.normalize('NFC', value).split())


def exact_quote_in_text(quote, source):
    """Match actual prose without turning a signed/larger number into another one."""
    quote, source = exact_text(quote), exact_text(source)
    if not quote:
        return False
    for match in re.finditer(re.escape(quote), source):
        start, end = match.span()
        before, after = source[start - 1:start] if start else '', source[end:end + 1]
        if (quote[0].isalnum() and before and (before.isalnum() or before == '_')):
            continue
        if quote[0].isdigit() and before and before in '+-−.,':
            continue
        if quote[-1].isalnum() and after and (after.isalnum() or after == '_'):
            continue
        if (quote[-1].isdigit() and after in ('.', ',')
                and source[end + 1:end + 2].isdigit()):
            continue
        return True
    return False


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                    separators=(',', ':')).encode('utf-8')).hexdigest()


def content_hash(document):
    """Bind review to both the spoken units AND the reasoning/emphasis map."""
    return digest({k: v for k, v in document.items() if k != 'review'})


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def validate(document, request_text=None):
    errors, warnings = [], []

    def need(condition, message):
        if not condition:
            errors.append(message)

    def text(value):
        return isinstance(value, str) and bool(value.strip()) and value.strip().casefold() not in {
            'todo', 'tbd', 'pending', 'placeholder', 'chưa điền'}

    need(document.get('schema') == SCHEMA, 'Unsupported editorial map schema')
    structure_policy = document.get('structurePolicy', 'hook-disclaimer-content-cta')
    need(structure_policy in STRUCTURE_POLICIES, 'Unknown structurePolicy')
    expected_phases = STRUCTURE_POLICIES.get(structure_policy, PHASES)
    for field in ['title', 'centralQuestion', 'thesis', 'viewerStake', 'hookPromise']:
        need(text(document.get(field)), 'Missing editorial brief: ' + field)
    need(isinstance(document.get('exclusions'), list) and bool(document['exclusions'])
         and all(text(x) for x in document['exclusions']), 'State the tangents excluded from this film')
    units = document.get('units', [])
    need(isinstance(units, list) and bool(units), 'Spoken units must be a nonempty ordered list')
    if not isinstance(units, list):
        units = []
    by_id, phases = {}, []
    for unit in units:
        if not isinstance(unit, dict):
            errors.append('Each spoken unit must be an object')
            continue
        uid = unit.get('id')
        if not text(uid) or uid in by_id:
            errors.append('Missing or duplicate spoken unit id')
            continue
        by_id[uid] = unit
        need(text(unit.get('text')), 'Missing spoken text: ' + uid)
        phase = unit.get('phase')
        need(phase in PHASES, 'Unknown unit phase: ' + uid)
        if not phases or phases[-1] != phase:
            phases.append(phase)
    need(phases == expected_phases, 'Spoken order must be ' + ' -> '.join(expected_phases)
         + ' under the selected structurePolicy')
    chapters = document.get('chapters', [])
    need(isinstance(chapters, list) and bool(chapters), 'Write explicit main-content chapters')
    if not isinstance(chapters, list):
        chapters = []
    assigned, chapter_ids = [], set()
    for index, chapter in enumerate(chapters):
        if not isinstance(chapter, dict):
            errors.append('Each chapter must be an object')
            continue
        cid = chapter.get('id', '')
        need(text(cid) and cid not in chapter_ids, 'Missing or duplicate chapter id')
        chapter_ids.add(cid)
        for field in ['title', 'question', 'answer', 'mechanism', 'whyItMatters', 'takeaway']:
            need(text(chapter.get(field)), 'Missing chapter ' + field + ': ' + str(cid))
        ids = chapter.get('unitIds', [])
        need(isinstance(ids, list) and bool(ids), 'Chapter needs spoken unitIds: ' + str(cid))
        if not isinstance(ids, list):
            ids = []
        assigned.extend(ids)
        need(all(isinstance(uid, str) and uid in by_id and by_id[uid].get('phase') == 'content'
                 for uid in ids), 'Chapter contains unknown/non-content units: ' + str(cid))
        chapter_text = '\n\n'.join(by_id[uid].get('text', '') for uid in ids
                                   if isinstance(uid, str) and uid in by_id)
        examples = chapter.get('evidenceExamples', [])
        need(isinstance(examples, list) and bool(examples), 'Chapter needs a concrete example/evidence: ' + str(cid))
        for example in examples if isinstance(examples, list) else []:
            if not isinstance(example, dict):
                errors.append('Example must identify its kind and detail: ' + str(cid))
                continue
            kind = example.get('kind')
            need(kind in ['illustrative', 'primary', 'reference_rhetoric'], 'Unknown evidence kind: ' + str(cid))
            need(text(example.get('detail')), 'Empty evidence/example: ' + str(cid))
            if kind != 'illustrative':
                need(text(example.get('source')), 'Evidence needs a source: ' + str(cid))
        emphasis = chapter.get('emphasis', {})
        if not isinstance(emphasis, dict):
            emphasis = {}
        quote = emphasis.get('spokenQuote', '')
        need(text(quote) and bool(words(quote)) and exact_quote_in_text(quote, chapter_text),
             'Emphasis must quote the actual chapter narration: ' + str(cid))
        need(text(emphasis.get('visualFocus')) and text(emphasis.get('purpose')),
             'Say what is emphasized and why: ' + str(cid))
        if index < len(chapters) - 1:
            bridge = chapter.get('bridge', {})
            if not isinstance(bridge, dict):
                bridge = {}
            need(text(bridge.get('reason')) and text(bridge.get('nextQuestion')),
                 'Chapter bridge must explain why the next question follows: ' + str(cid))
    expected = [uid for uid, unit in by_id.items() if unit.get('phase') == 'content']
    need(assigned == expected, 'Every content unit must belong to exactly one chapter, once and in spoken order')
    payoff = document.get('payoff', {})
    if not isinstance(payoff, dict):
        payoff = {}
    need(text(payoff.get('answer')), 'State the final answer to the hook')
    payoff_ids = payoff.get('unitIds', [])
    need(isinstance(payoff_ids, list) and bool(payoff_ids)
         and all(isinstance(uid, str) and uid in expected for uid in payoff_ids), 'Payoff needs actual main-content units before CTA')
    if chapters and isinstance(chapters[-1], dict) and isinstance(payoff_ids, list):
        need(all(uid in chapters[-1].get('unitIds', []) for uid in payoff_ids), 'Resolve the hook in the final main-content chapter')
    if request_text is not None:
        # A provider take must consist of complete consecutive units, not a
        # different rewrite or an arbitrary sentence scraped from an approved map.
        target = exact_text(request_text)
        found = False
        tokens = [exact_text(u.get('text', '')) for u in units if isinstance(u, dict) and isinstance(u.get('text'), str)]
        for start in range(len(tokens)):
            parts = []
            for part in tokens[start:]:
                parts.append(part)
                candidate = ' '.join(parts)
                if candidate == target and target:
                    found = True
                    break
                if len(candidate) >= len(target):
                    break
            if found:
                break
        need(found, 'Requested take is not complete consecutive spoken units in this reviewed map')
    review = document.get('review', {})
    if not isinstance(review, dict):
        review = {}
    need(review.get('status') == 'accepted', 'Editorial review still needs revision/reading')
    reviewer = review.get('reviewer', {})
    if not isinstance(reviewer, dict):
        reviewer = {}
    need(reviewer.get('kind') in ['agent', 'human_user'] and text(reviewer.get('name')),
         'Name the actual script reviewer')
    need(review.get('method') == 'full_script_read', 'Review requires reading the complete script')
    need(review.get('contentSHA256') == content_hash(document), 'Review is stale: script or argument map changed')
    checks = review.get('checks', {})
    if not isinstance(checks, dict):
        checks = {}
    for dimension in sorted(DIMENSIONS):
        check = checks.get(dimension, {})
        need(isinstance(check, dict) and check.get('decision') == 'accepted' and text(check.get('observation')),
             'Missing reasoned script review: ' + dimension)
    need(review.get('unresolvedIssues') == [], 'Resolve open editorial issues before new narration')
    warnings.append('Formal coverage and declared review do not establish engaging content, factual truth, audiovisual quality or user approval.')
    return {'schema': 'reference-video-editorial-check/1', 'contentSHA256': content_hash(document),
            'readyForNewNarration': not errors, 'errors': errors, 'warnings': warnings,
            'chapterCount': len(chapters), 'spokenUnitCount': len(units), 'userApproval': 'not_established'}


def require_for_take(target, request_text, workspace):
    workspace = Path(workspace).resolve()
    target = Path(target).resolve()
    if not target.is_relative_to(workspace):
        raise ValueError('New narration target must be inside its project workspace')
    for folder in target.parents:
        candidate = folder / 'editorial-map.json'
        if candidate.is_file():
            report = validate(read(candidate), request_text)
            if not report['readyForNewNarration']:
                raise ValueError('Editorial gate blocked new narration: ' + '; '.join(report['errors']))
            return {'map': candidate.relative_to(workspace).as_posix(),
                    'mapSHA256': hashlib.sha256(candidate.read_bytes()).hexdigest(),
                    'contentSHA256': report['contentSHA256'], 'userApproval': 'not_established'}
        if folder == workspace:
            break
    raise ValueError('New narration needs a reviewed editorial-map.json in its batch; read CONTENT_FIRST.md')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('map', type=Path)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    result = validate(read(args.map))
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(rendered + '\n', encoding='utf-8')
    print(rendered)
    raise SystemExit(0 if result['readyForNewNarration'] else 1)
