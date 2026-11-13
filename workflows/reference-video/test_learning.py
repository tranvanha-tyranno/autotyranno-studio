"""Offline invariants for evidence, feedback revisions and lesson promotion."""
import json
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).parent))
from learning import LearningError, LearningStore, file_sha


@pytest.fixture
def setup(tmp_path):
    batch = tmp_path / 'videos/pilot'
    batch.mkdir(parents=True)
    for revision in ['r1', 'r2']:
        folder = batch / revision
        folder.mkdir()
        for name in ['final.mp4', 'frame.png', 'asset.jpg', 'script.txt', 'mix.wav', 'qa.json', 'code-snapshot.py']:
            (folder / name).write_text(revision + '/' + name, encoding='utf-8')
        (folder / 'user-feedback.txt').write_text('User: Giữ hình này, đã khớp lời.\n', encoding='utf-8')
    return LearningStore(tmp_path / 'learning', tmp_path), tmp_path


def evidence(root, revision='r1', roles=('render', 'frame', 'asset')):
    files = {'render': 'final.mp4', 'frame': 'frame.png', 'asset': 'asset.jpg',
             'script': 'script.txt', 'audio': 'mix.wav', 'report': 'qa.json',
             'code': 'code-snapshot.py', 'feedback': 'user-feedback.txt'}
    return [{'role': role, 'path': f'videos/pilot/{revision}/{files[role]}',
             'sha256': file_sha(root / f'videos/pilot/{revision}/{files[role]}')}
            for role in roles]


def feedback(root, revision='r1', decision='rejected', **overrides):
    return {'batch': 'videos/pilot', 'revision': revision, 'dimension': 'visual_relevance',
        'decision': decision, 'reviewer': {'kind': 'agent', 'name': 'frame reviewer'},
        'target': {'clause_id': 'c01', 'narration': 'Cánh cửa hẹp khiến xe không đi qua.', 'start': 2.1, 'end': 5.4},
        'method': 'rendered_frame_comparison',
        'observation': 'Frame shows an open road; it does not show the narrated narrow passage.',
        'action': 'Use the inspected narrow-passage asset and retain the doorway in the crop.',
        'evidence': evidence(root, revision), **overrides}


def propose(store, root):
    source = store.append('feedback_recorded', feedback(root), 'source-r1')
    proposal = store.append('lesson_proposed', {
        'title': 'Keep the narrated obstruction visible', 'category': 'visual_relevance',
        'rule': 'Match the visible action and obstruction to the narrated clause.',
        'action': 'Inspect the final crop beside the exact clause.',
        'rationale': 'A related location alone did not show the obstruction.',
        'applies_to': ['photo_explainer'], 'source_feedback_ids': [source['id']]}, 'propose')
    return source, proposal


def apply(store, root, proposal):
    return store.append('lesson_applied', {'lesson_id': proposal['id'], 'batch': 'videos/pilot',
        'revision': 'r2', 'change': 'Replaced the unrelated source image and changed the crop.',
        'evidence': evidence(root, 'r2', ('render', 'frame', 'asset', 'code'))}, 'apply-r2')


def verify(store, root):
    source, proposal = propose(store, root)
    application = apply(store, root, proposal)
    accepted = store.append('feedback_recorded', feedback(root, 'r2', 'accepted',
        observation='The cropped render now visibly shows the narrated narrow passage.',
        action='Retain this crop and use the same inspection rule for later clauses.'), 'review-r2')
    verified = store.append('lesson_verified', {'lesson_id': proposal['id'],
        'application_id': application['id'], 'feedback_id': accepted['id'],
        'conclusion': 'The changed rendered crop fixes the documented mismatch.'}, 'verify-r2')
    return source, proposal, application, accepted, verified


def test_guidance_is_empty_until_actual_application_and_later_editorial_verification(setup):
    store, root = setup
    _, proposed = propose(store, root)
    assert store.guidance()['lessons'] == []
    applied = apply(store, root, proposed)
    assert store.guidance()['lessons'] == []
    accepted = store.append('feedback_recorded', feedback(root, 'r2', 'accepted'), 'accepted')
    store.append('lesson_verified', {'lesson_id': proposed['id'], 'application_id': applied['id'],
        'feedback_id': accepted['id'], 'conclusion': 'The rendered relation is now visible.'}, 'verify')
    guidance = store.guidance()
    assert len(guidance['lessons']) == 1
    assert guidance['lessons'][0]['status'] == 'verified'
    assert guidance['lessons'][0]['verification_from_user_feedback'] is False
    assert guidance['user_acceptance_by_batch'] == []


def test_decode_success_cannot_be_an_editorial_verification_or_lesson_source(setup):
    store, root = setup
    technical = store.append('technical_check_recorded', {'batch': 'videos/pilot', 'revision': 'r1',
        'check_id': 'full_decode', 'result': 'passed', 'observation': 'All packets decoded.',
        'evidence': evidence(root, roles=('render', 'report'))}, 'decode')
    with pytest.raises(LearningError, match='Technical checks'):
        store.append('lesson_proposed', {'title': 'Visuals are good', 'category': 'visual_relevance',
            'rule': 'Trust decoding.', 'action': 'Skip inspection.', 'rationale': 'Decode passed.',
            'applies_to': ['explainer'], 'source_feedback_ids': [technical['id']]}, 'wrong-source')
    _, proposed = propose(store, root)
    applied = apply(store, root, proposed)
    with pytest.raises(LearningError, match='accepted editorial feedback'):
        store.append('lesson_verified', {'lesson_id': proposed['id'], 'application_id': applied['id'],
            'feedback_id': technical['id'], 'conclusion': 'Decode passed.'}, 'wrong-verification')
    assert store.guidance()['lessons'] == []


def test_retries_are_idempotent_but_request_keys_cannot_change_meaning(setup):
    store, root = setup
    payload = feedback(root)
    first = store.append('feedback_recorded', payload, 'review-r1')
    event_path = store.events_dir / (first['id'] + '.json')
    original_bytes = event_path.read_bytes()
    assert store.append('feedback_recorded', payload, 'review-r1') == first
    assert event_path.read_bytes() == original_bytes
    assert len(store.events()) == 1
    with pytest.raises(LearningError, match='different content'):
        store.append('feedback_recorded', {**payload, 'decision': 'accepted'}, 'review-r1')
    assert event_path.read_bytes() == original_bytes


def test_feedback_revisions_must_explicitly_supersede_current_target(setup):
    store, root = setup
    first = store.append('feedback_recorded', feedback(root), 'reject')
    original_bytes = (store.events_dir / (first['id'] + '.json')).read_bytes()
    with pytest.raises(LearningError, match='explicitly supersede'):
        store.append('feedback_recorded', feedback(root, decision='accepted'), 'accept-without-history')
    next_review = store.append('feedback_recorded', feedback(root, decision='accepted', supersedes=first['id']), 'accept')
    assert len(store.events()) == 2
    assert store.report()['feedback'][0]['id'] == next_review['id']
    assert (store.events_dir / (first['id'] + '.json')).read_bytes() == original_bytes
    with pytest.raises(LearningError, match='latest event'):
        store.append('feedback_recorded', feedback(root, supersedes=first['id']), 'stale-rejection')


def test_verification_requires_same_revision_category_and_review_after_application(setup):
    store, root = setup
    _, proposal = propose(store, root)
    early = store.append('feedback_recorded', feedback(root, 'r2', 'accepted'), 'early-review')
    application = apply(store, root, proposal)
    payload = {'lesson_id': proposal['id'], 'application_id': application['id'],
        'feedback_id': early['id'], 'conclusion': 'Earlier review is not a review of this change.'}
    with pytest.raises(LearningError, match='after the actual application'):
        store.append('lesson_verified', payload, 'verify-too-early')
    mismatched = store.append('feedback_recorded', feedback(root, 'r1', 'accepted',
        target={'clause_id': 'another', 'narration': 'Another clause.', 'start': 7, 'end': 8}), 'different-revision')
    with pytest.raises(LearningError, match='batch and revision'):
        store.append('lesson_verified', {**payload, 'feedback_id': mismatched['id']}, 'verify-wrong-revision')
    script_review = store.append('feedback_recorded', feedback(root, 'r2', 'accepted',
        dimension='script', method='script_review', evidence=evidence(root, 'r2', ('script',))), 'script-review')
    with pytest.raises(LearningError, match='match the lesson category'):
        store.append('lesson_verified', {**payload, 'feedback_id': script_review['id']}, 'verify-wrong-category')


def test_superseding_verification_feedback_removes_effective_guidance(setup):
    store, root = setup
    _, _, _, accepted, _ = verify(store, root)
    assert len(store.guidance()['lessons']) == 1
    store.append('feedback_recorded', feedback(root, 'r2', 'revision_needed', supersedes=accepted['id']), 'later-correction')
    guidance = store.guidance()
    assert guidance['lessons'] == []
    assert guidance['excluded_lessons'][0]['reason'] == 'verification_feedback_superseded'
    assert store.report()['lessons'][0]['state'] == 'verified'  # Historical event stays intact.


def test_correcting_the_original_review_also_removes_unsupported_guidance(setup):
    store, root = setup
    source, _, _, _, _ = verify(store, root)
    store.append('feedback_recorded', feedback(root, decision='accepted', supersedes=source['id'],
        observation='The original review was mistaken; this artifact did show the passage.',
        action='Correct the old review and reassess the derived rule.'), 'correct-original-review')
    guidance = store.guidance()
    assert guidance['lessons'] == []
    assert guidance['excluded_lessons'][0]['reason'] == 'source_feedback_superseded'
    original_proposal = store.events()[1]['payload']
    with pytest.raises(LearningError, match='current review'):
        store.append('lesson_proposed', original_proposal, 'reuse-superseded-review')


def test_source_review_must_still_support_the_rule_at_verification_time(setup):
    store, root = setup
    source, proposal = propose(store, root)
    application = apply(store, root, proposal)
    store.append('feedback_recorded', feedback(root, decision='accepted', supersedes=source['id']), 'correct-source')
    accepted = store.append('feedback_recorded', feedback(root, 'r2', 'accepted'), 'accepted-r2')
    with pytest.raises(LearningError, match='source review was superseded'):
        store.append('lesson_verified', {'lesson_id': proposal['id'], 'application_id': application['id'],
            'feedback_id': accepted['id'], 'conclusion': 'Cannot rely on a corrected original review.'}, 'verify')
    assert store.report()['lessons'][0]['state'] == 'applied'


def test_changed_evidence_blocks_verification_and_stale_guidance(setup):
    store, root = setup
    _, _, _, _, _ = verify(store, root)
    (root / 'videos/pilot/r2/frame.png').write_bytes(b'changed frame')
    assert store.guidance()['lessons'] == []
    assert store.guidance()['excluded_lessons'][0]['reason'] == 'evidence_changed_or_missing'
    assert store.audit()['file_integrity'] == 'changed_or_missing'


def test_paths_and_hashes_cannot_point_outside_or_to_a_different_asset(setup):
    store, root = setup
    payload = feedback(root)
    payload['evidence'][0]['path'] = '../outside.mp4'
    with pytest.raises(LearningError, match='workspace-relative'):
        store.append('feedback_recorded', payload, 'outside')
    payload = feedback(root)
    payload['evidence'][1]['sha256'] = '0' * 64
    with pytest.raises(LearningError, match='hash changed'):
        store.append('feedback_recorded', payload, 'wrong-hash')
    assert store.events() == []


def test_user_acceptance_requires_exact_retained_feedback_for_the_render(setup):
    store, root = setup
    human = feedback(root, decision='accepted', dimension='overall', method='human_feedback',
        reviewer={'kind': 'human_user', 'name': 'User'}, quote='Looks good.',
        evidence=evidence(root, roles=('render', 'feedback')))
    with pytest.raises(LearningError, match='Exact user quote'):
        store.append('feedback_recorded', human, 'invented-quote')
    human['quote'] = 'Giữ hình này, đã khớp lời.'
    store.append('feedback_recorded', human, 'exact-quote')
    acceptance = store.guidance()['user_acceptance_by_batch']
    assert acceptance[0]['user_approved'] is True
    assert acceptance[0]['exact_quote'] == human['quote']
    assert store.guidance()['lessons'] == []  # Human feedback does not silently make a lesson.


def test_non_listening_or_machine_reviews_cannot_pass_audio_and_overall(setup):
    store, root = setup
    for update in [
        {'reviewer': {'kind': 'machine', 'name': 'decoder'}},
        {'method': 'metadata_only'},
        {'dimension': 'voice', 'evidence': evidence(root, roles=('audio',)), 'method': 'rendered_frame_comparison'},
        {'dimension': 'overall', 'method': 'rendered_frame_comparison'},
        {'method': 'human_feedback'},
    ]:
        with pytest.raises(LearningError):
            store.append('feedback_recorded', feedback(root, decision='accepted', **update), 'bad-review')
    assert store.events() == []


def test_pending_is_visible_but_cannot_seed_a_lesson(setup):
    store, root = setup
    pending = store.append('feedback_recorded', feedback(root, decision='pending', evidence=[]), 'pending')
    assert store.report()['feedback'][0]['decision'] == 'pending'
    with pytest.raises(LearningError, match='pending reviews'):
        store.append('lesson_proposed', {'title': 'Premature rule', 'category': 'visual_relevance',
            'rule': 'Unreviewed rule.', 'action': 'Change the style.', 'rationale': 'No evidence yet.',
            'applies_to': ['explainer'], 'source_feedback_ids': [pending['id']]}, 'premature')


def test_retirement_keeps_history_and_removes_guidance(setup):
    store, root = setup
    _, proposal, _, _, _ = verify(store, root)
    count = len(store.events())
    store.append('lesson_retired', {'lesson_id': proposal['id'], 'reason': 'A later style decision supersedes this rule.'}, 'retire')
    assert len(store.events()) == count + 1
    assert store.guidance()['lessons'] == []
    assert store.report()['lessons'][0]['state'] == 'retired'
    with pytest.raises(LearningError, match='retired'):
        store.append('lesson_applied', {'lesson_id': proposal['id'], 'batch': 'videos/pilot',
            'revision': 'r2', 'change': 'A new attempt after retirement.',
            'evidence': evidence(root, 'r2', ('render',))}, 'new-apply-after-retirement')


def test_event_tampering_is_detected_and_interrupted_staging_is_ignored(setup):
    store, root = setup
    event = store.append('feedback_recorded', feedback(root), 'review')
    (store.events_dir / '.interrupted.pending').write_text('unfinished', encoding='utf-8')
    assert len(store.events()) == 1
    store.append('technical_check_recorded', {'batch': 'videos/pilot', 'revision': 'r1',
        'check_id': 'decode', 'result': 'passed', 'observation': 'Decodes.',
        'evidence': evidence(root, roles=('render',))}, 'decode')
    path = store.events_dir / (event['id'] + '.json')
    tampered = json.loads(path.read_text(encoding='utf-8'))
    tampered['payload']['decision'] = 'accepted'
    path.write_text(json.dumps(tampered), encoding='utf-8')
    with pytest.raises(LearningError, match='history is incomplete or changed'):
        store.events()


def test_busy_lock_is_not_silently_removed(setup):
    store, root = setup
    store.store.mkdir()
    lock = store.store / '.write.lock'
    lock.write_text('{"pid":12345}', encoding='utf-8')
    with pytest.raises(LearningError, match='reconcile'):
        store.append('feedback_recorded', feedback(root), 'review')
    assert lock.read_text(encoding='utf-8') == '{"pid":12345}'


def test_pinned_head_detects_a_missing_tail_even_if_remaining_prefix_is_valid(setup):
    store, root = setup
    first = store.append('feedback_recorded', feedback(root), 'first')
    second = store.append('technical_check_recorded', {'batch': 'videos/pilot', 'revision': 'r1',
        'check_id': 'decode', 'result': 'passed', 'observation': 'Decoded.',
        'evidence': evidence(root, roles=('render',))}, 'second')
    assert store.audit(expected_head=second['event_sha256'])['file_integrity'] == 'passed'
    (store.events_dir / (second['id'] + '.json')).unlink()  # Simulate external deletion, not a supported operation.
    assert store.events() == [first]
    assert store.audit(expected_head=second['event_sha256'])['file_integrity'] == 'changed_or_missing'


def test_no_credential_fields_are_written(setup):
    store, root = setup
    payload = feedback(root)
    payload['reviewer']['api_key'] = 'do-not-write'
    with pytest.raises(LearningError, match='Credential fields'):
        store.append('feedback_recorded', payload, 'secret')
    assert store.events() == []


def test_real_verified_export_matches_the_production_guidance_contract(setup):
    import production

    store, root = setup
    verify(store, root)
    guidance = store.guidance()
    assert guidance['lessons'][0]['verified_by'] == {'kind': 'agent', 'name': 'frame reviewer'}
    assert production.validate_guidance(guidance) is guidance
