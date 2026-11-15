"""Exact-take cuts for the authorized faster finance rewrite.

The rejected film assigned one fixed composition to each 9--14 second narration
beat. This planner preserves that narration and its semantic beat boundaries,
but gives the new renderers shorter, connected action shots. It prefers complete
sentences and clauses, ordinarily 2.2--4.4 seconds, and will not split a word.
The 4.8 second upper bound is a pacing constraint, not a declaration that a film
has stopped looking like slides: the renderers still need visible cause/effect,
changing subject state, and review of complete moving representative scenes.

No audio is retimed, generated, published, or written by this module. The caller
owns the new batch and can append an exact-take ``subscribe`` segment before
calling ``build_shots``. A subscription outro has stage ``outro`` throughout.

Public API:
    build_shots(plan: dict) -> list[dict]
    audit_shots(plan: dict, shots: list[dict]) -> dict

Every shot has id/from/duration/beatId/part/parts/text/stage. Frame positions are
absolute, ``part`` is zero based, and ``parts`` is the number of shots in its beat.
The stage describes the editorial role, not an automatic visual-quality verdict.
"""
from __future__ import annotations

from collections import Counter
import math
import re
from statistics import median
from typing import Any


TARGET_SECONDS = 3.3
PREFERRED_MIN_SECONDS = 2.2
PREFERRED_MAX_SECONDS = 4.4
MAX_SECONDS = 4.8
MIN_SECONDS = 1.2
STAGES = {'setup', 'action', 'result', 'reaction', 'outro'}

# Avoid a forced cut inside Vietnamese number phrases and common inseparable
# phrases. Punctuation remains authoritative, since it marks the actual clause.
NUMBER_WORDS = {
    'không', 'một', 'hai', 'ba', 'bốn', 'tư', 'năm', 'sáu', 'bảy', 'tám', 'chín',
    'mười', 'mươi', 'trăm', 'nghìn', 'ngàn', 'triệu', 'tỷ', 'phẩy',
}
BAD_TAILS = {
    'và', 'hoặc', 'hay', 'với', 'của', 'cho', 'từ', 'để', 'nếu', 'khi', 'vì',
    'mà', 'nhưng', 'thì', 'là', 'bằng', 'cộng', 'trừ', 'nhân', 'chia', 'có',
    'không', 'đã', 'đang', 'sẽ', 'mỗi', 'những', 'các', 'một', 'phải', 'cạnh',
}
JOINED_PAIRS = {
    ('thu', 'nhập'), ('chi', 'tiêu'), ('thiết', 'yếu'), ('dòng', 'tiền'),
    ('ngân', 'sách'), ('định', 'kỳ'), ('tự', 'động'), ('số', 'dư'),
    ('khoản', 'dư'), ('hóa', 'đơn'), ('thanh', 'toán'), ('đăng', 'ký'),
    ('gia', 'đình'), ('thực', 'tế'), ('kế', 'hoạch'), ('minh', 'họa'),
    ('đứng', 'cạnh'), ('cạnh', 'nhau'), ('có', 'thể'), ('khoản', 'chi'), ('tiết', 'kiệm'),
    ('điều', 'chỉnh'),
}


def _token(text: str) -> str:
    return re.sub(r'[^\w]', '', text.casefold())


def _finite(value: Any, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(label + ' must be finite numeric data')
    return float(value)


def _plan_data(plan: dict) -> tuple[float, int, list[dict], list[dict]]:
    fps = _finite(plan.get('fps'), 'fps')
    if fps <= 0:
        raise ValueError('fps must be positive')
    frames = plan.get('durationFrames')
    if isinstance(frames, bool) or not isinstance(frames, int) or frames < 1:
        raise ValueError('durationFrames must be a positive integer')
    segments, words = plan.get('segments'), plan.get('words')
    if not isinstance(segments, list) or not segments:
        raise ValueError('Exact-take segments are required')
    if not isinstance(words, list) or not words:
        raise ValueError('Exact-take words are required; cuts must not use text length estimates')
    previous = 0
    ids = set()
    for segment in segments:
        if segment.get('id') in ids or not isinstance(segment.get('id'), str):
            raise ValueError('Segments need unique string IDs')
        ids.add(segment['id'])
        start, duration = segment.get('from'), segment.get('duration')
        if not isinstance(start, int) or not isinstance(duration, int) or duration <= 0 or start != previous:
            raise ValueError('Segments must cover the timeline contiguously in integer frames')
        previous = start + duration
    if previous != frames:
        raise ValueError('Segments do not cover durationFrames')
    previous_start = -1.
    for word in words:
        start = _finite(word.get('start'), 'word.start')
        end = _finite(word.get('end'), 'word.end')
        if start < previous_start or start < 0 or end < start or end * fps > frames + 1:
            raise ValueError('Word alignment is unordered or outside the timeline')
        if not isinstance(word.get('text'), str) or not word['text'].strip():
            raise ValueError('Every aligned word needs nonempty text')
        previous_start = start
    return fps, frames, segments, words


def _words_in(words: list[dict], start: int, end: int, fps: float) -> list[dict]:
    # The source planner rounds segment starts in exactly this way. Using rounded
    # onsets gives each token one owner, including near-half-frame boundaries.
    return [word for word in words if start <= round(word['start'] * fps) < end]


def _boundary_cost(previous: dict, following: dict) -> tuple[float, str]:
    text = previous['text'].rstrip('”’"\'»)]}')
    if re.search(r'[.!?]$', text):
        return -1.0, 'sentence'
    if re.search(r'[;:]$', text):
        return -.5, 'clause'
    if text.endswith(','):
        return -.2, 'clause'
    left, right = _token(previous['text']), _token(following['text'])
    penalty = .7
    if left in NUMBER_WORDS and right in NUMBER_WORDS:
        penalty += 8
    if (left, right) in JOINED_PAIRS:
        penalty += 7
    if left in BAD_TAILS:
        penalty += 3
    # Favour a natural second-clause conjunction, with the conjunction retained
    # at the start of the new shot, rather than orphaned at the preceding end.
    if right in {'nhưng', 'nếu', 'khi', 'rồi', 'vì', 'đừng', 'hãy'}:
        penalty -= .6
    return penalty, 'word'


def _segment_cuts(segment: dict, words: list[dict], fps: float) -> list[int]:
    start, end = segment['from'], segment['from'] + segment['duration']
    local = _words_in(words, start, end, fps)
    if not local:
        if end - start > round(MAX_SECONDS * fps):
            raise ValueError(f'{segment["id"]}: long segment has no aligned words')
        return [start, end]
    boundaries = {start: (0., 'beat'), end: (0., 'beat')}
    for i in range(1, len(local)):
        frame = round(local[i]['start'] * fps)
        if start < frame < end:
            value = _boundary_cost(local[i-1], local[i])
            if frame not in boundaries or value[0] < boundaries[frame][0]:
                boundaries[frame] = value
    candidates = sorted(boundaries)
    max_frames, min_frames = round(MAX_SECONDS * fps), round(MIN_SECONDS * fps)
    # The hook's first complete sentence can be slightly shorter than 1.2s; the
    # measured opening 'Lương tăng hai triệu.' is a purposeful complete reveal.
    hook_min = round(1.0 * fps) if segment.get('kind') == 'hook' else min_frames
    scores = {start: 0.}
    predecessors: dict[int, int] = {}
    for j in range(1, len(candidates)):
        stop = candidates[j]
        for i in range(j-1, -1, -1):
            beginning = candidates[i]
            length = stop - beginning
            if length > max_frames:
                break
            minimum = hook_min if beginning == start else min_frames
            # A whole short beat is valid; it should not be stretched or looped.
            if length < minimum and not (beginning == start and stop == end):
                continue
            if beginning not in scores:
                continue
            seconds = length / fps
            cost = ((seconds - TARGET_SECONDS) / 1.45) ** 2 + .65
            if seconds < PREFERRED_MIN_SECONDS:
                cost += (PREFERRED_MIN_SECONDS - seconds) * 1.1
            if seconds > PREFERRED_MAX_SECONDS:
                cost += (seconds - PREFERRED_MAX_SECONDS) * 2
            cost += boundaries[stop][0]
            # Softly prefer at least one sentence/clause per shot. Word cuts are
            # still possible where a spoken sentence genuinely exceeds 4.8s.
            if beginning != start and boundaries[beginning][1] == 'word':
                cost += .15
            total = scores[beginning] + cost
            if total < scores.get(stop, math.inf):
                scores[stop] = total
                predecessors[stop] = beginning
    if end not in scores:
        raise ValueError(f'{segment["id"]}: cannot cut within 4.8s at actual word onsets; inspect alignment/gaps')
    cuts = [end]
    while cuts[-1] != start:
        cuts.append(predecessors[cuts[-1]])
    return list(reversed(cuts))


def _stage(segment: dict, text: str, part: int, parts: int) -> str:
    if segment.get('kind') in {'subscribe', 'outro'}:
        return 'outro'
    if parts == 1:
        return 'result' if segment.get('kind') not in {'hook', 'disclaimer'} else 'setup'
    if part == 0:
        return 'setup'
    normalized = ' '.join(_token(word) for word in text.split())
    # A stated arithmetic consequence should be visible during that statement,
    # not withheld until a generic final 'result' shot after the narration.
    if any(phrase in normalized for phrase in ['bằng ', 'cộng ', 'trừ ', 'còn hai triệu', 'vẫn còn', 'tổng chi', 'tổng tiền', 'dư hai triệu']):
        return 'result'
    if part == parts-1:
        if any(phrase in normalized for phrase in ['không phải', 'điều chỉnh', 'nếu ', 'có thể', 'giữ nguyên', 'quyết định', 'theo hoàn cảnh']):
            return 'reaction'
        return 'result'
    return 'action'


def build_shots(plan: dict) -> list[dict]:
    """Return connected 1.2--4.8s shots without changing any audio timing.

    Most shots fall in 2.2--4.4s. Each boundary lies either on its original beat
    edge or on an exact rounded word onset from ``plan['words']``. Input is read
    only: no plan dictionary or list is mutated and no file is written.
    """
    fps, _, segments, words = _plan_data(plan)
    shots = []
    for segment in segments:
        cuts = _segment_cuts(segment, words, fps)
        parts = len(cuts) - 1
        for part, (start, end) in enumerate(zip(cuts, cuts[1:])):
            text = ' '.join(word['text'] for word in _words_in(words, start, end, fps))
            shots.append({'id':f'{segment["id"]}-p{part+1:02}', 'from':start,
                'duration':end-start, 'beatId':segment['id'], 'part':part, 'parts':parts,
                'text':text, 'stage':_stage(segment, text, part, parts)})
    audit_shots(plan, shots)
    return shots


def audit_shots(plan: dict, shots: list[dict]) -> dict:
    """Assert frame/word continuity and return a diagnostic pacing summary.

    This does not judge visual quality or prove that actions remain meaningful.
    The caller must inspect complete rendered moving scenes separately.
    """
    fps, frames, segments, words = _plan_data(plan)
    if not isinstance(shots, list) or not shots:
        raise ValueError('At least one paced shot is required')
    by_id = {segment['id']:segment for segment in segments}
    beat_edges = {s['from'] for s in segments} | {frames}
    word_onsets = {round(w['start'] * fps) for w in words}
    previous, ids, ownership = 0, set(), Counter()
    output_tokens = []
    for shot in shots:
        if shot.get('id') in ids or not isinstance(shot.get('id'), str):
            raise ValueError('Shot IDs must be unique strings')
        ids.add(shot['id'])
        start, duration = shot.get('from'), shot.get('duration')
        if not isinstance(start, int) or not isinstance(duration, int) or duration < 1 or start != previous:
            raise ValueError('Shots must provide positive contiguous integer-frame coverage')
        if duration > round(MAX_SECONDS * fps):
            raise ValueError('Shot exceeds the 4.8 second maximum')
        end = start + duration
        segment = by_id.get(shot.get('beatId'))
        if not segment or not (segment['from'] <= start < end <= segment['from'] + segment['duration']):
            raise ValueError('A shot crosses its original narration beat boundary')
        if start not in beat_edges and start not in word_onsets:
            raise ValueError('A cut is not aligned to an exact word onset or original beat edge')
        if shot.get('stage') not in STAGES:
            raise ValueError('Unknown editorial shot stage')
        if shot.get('part') != ownership[segment['id']]:
            raise ValueError('Shot parts must be consecutive and zero based within each beat')
        ownership[segment['id']] += 1
        expected_words = _words_in(words, start, end, fps)
        expected_text = ' '.join(w['text'] for w in expected_words)
        if shot.get('text') != expected_text:
            raise ValueError('Shot text does not match its actual aligned word ownership')
        output_tokens.extend(w['text'] for w in expected_words)
        previous = end
    if previous != frames or ownership.keys() != by_id.keys():
        raise ValueError('Shot coverage does not match the complete narration timeline')
    if output_tokens != [w['text'] for w in words]:
        raise ValueError('Shot text omitted, duplicated, or reordered aligned words')
    if any(shot['parts'] != ownership[shot['beatId']] for shot in shots):
        raise ValueError('Shot parts total differs from the actual number in its beat')
    durations = [s['duration'] / fps for s in shots]
    punctuation = sum(
        1 for shot in shots
        if shot['from'] in beat_edges or any(
            round(words[i]['start'] * fps) == shot['from']
            and re.search(r'[.!?;:,][”’"\'»)]*$', words[i-1]['text'])
            for i in range(1, len(words))
        )
    )
    return {'shots':len(shots), 'beats':len(segments), 'durationFrames':frames,
        'seconds':frames/fps, 'minShotSeconds':min(durations),
        'maxShotSeconds':max(durations), 'meanShotSeconds':sum(durations)/len(durations),
        'medianShotSeconds':median(durations),
        'shotsInPreferredRange':sum(PREFERRED_MIN_SECONDS <= d <= PREFERRED_MAX_SECONDS for d in durations),
        'punctuationOrBeatAlignedShotStarts':punctuation,
        'wordCoverage':'exactly-once', 'frameCoverage':'continuous',
        'stageCounts':dict(Counter(s['stage'] for s in shots)),
        'shotsByBeat':dict(ownership),
        'scope':'Pacing/timestamp continuity only; requires separate complete moving-scene review.'}
