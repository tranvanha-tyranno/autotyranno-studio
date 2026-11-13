"""Evidence-backed, append-only editorial learning for local video batches.

This records reviews and exports verified guidance. It neither trains a model nor
changes voice, visual presets, user approval, publishing, or scheduled tasks.
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
import uuid


ROOT = Path(__file__).resolve().parents[2]
EVENT_SCHEMA = 'reference-video-learning-event/1'
GUIDANCE_SCHEMA = 'reference-video-guidance/1'
DECISIONS = {'accepted', 'rejected', 'revision_needed', 'pending'}
DIMENSIONS = {'visual_relevance', 'script', 'voice', 'sound', 'overall', 'workflow'}
METHODS = {'rendered_frame_comparison', 'continuous_av_review', 'audio_listening',
           'script_review', 'human_feedback', 'metadata_only'}
ROLES = {'render', 'frame', 'asset', 'audio', 'feedback', 'report', 'script', 'code', 'source'}
KINDS = {'feedback_recorded', 'technical_check_recorded', 'lesson_proposed',
         'lesson_applied', 'lesson_verified', 'lesson_retired'}


class LearningError(ValueError):
    pass


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(',', ':'), allow_nan=False).encode('utf-8')


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def atomic_json(path, value):
    """Replace a derived export, never an event file."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name('.' + path.name + '.' + uuid.uuid4().hex + '.tmp')
    try:
        with temporary.open('x', encoding='utf-8', newline='\n') as stream:
            stream.write(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n')
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def text(value, name):
    if not isinstance(value, str) or not value.strip():
        raise LearningError(name + ' must be nonempty text')
    return value.strip()


def object_fields(value, allowed, required, name):
    if not isinstance(value, dict):
        raise LearningError(name + ' must be an object')
    missing, extra = set(required) - value.keys(), value.keys() - set(allowed)
    if missing or extra:
        raise LearningError(f'{name}: missing {sorted(missing)}, unknown {sorted(extra)}')


def no_secrets(value):
    """Reject credential fields; free prose must still be reviewed before saving."""
    if isinstance(value, dict):
        for key, child in value.items():
            if re.search(r'(api.?key|access.?token|refresh.?token|authorization|password|credential|secret)', key, re.I):
                raise LearningError('Credential fields do not belong in the learning ledger')
            no_secrets(child)
    elif isinstance(value, list):
        for child in value:
            no_secrets(child)
    elif isinstance(value, str) and re.search(r'\bBearer\s+[A-Za-z0-9._~+/-]{12,}', value, re.I):
        raise LearningError('Authorization text does not belong in the learning ledger')


def feedback_key(payload):
    return (payload['batch'], payload['revision'], payload['dimension'], payload['target']['clause_id'])


def state_from(events):
    feedback, effective, checks, lessons = {}, {}, [], {}
    for event in events:
        eid, payload, kind = event['id'], event['payload'], event['kind']
        if kind == 'feedback_recorded':
            feedback[eid] = event
            effective[feedback_key(payload)] = eid
        elif kind == 'technical_check_recorded':
            checks.append(event)
        elif kind == 'lesson_proposed':
            lessons[eid] = {'proposal': event, 'applications': [], 'verification': None, 'retirement': None}
        elif kind == 'lesson_applied':
            lessons[payload['lesson_id']]['applications'].append(event)
        elif kind == 'lesson_verified':
            lessons[payload['lesson_id']]['verification'] = event
        elif kind == 'lesson_retired':
            lessons[payload['lesson_id']]['retirement'] = event
    return {'feedback': feedback, 'effective': effective, 'checks': checks, 'lessons': lessons}


class LearningStore:
    def __init__(self, store, workspace=ROOT):
        self.workspace = Path(workspace).resolve(strict=True)
        self.store = Path(store).resolve()
        if not self.store.is_relative_to(self.workspace):
            raise LearningError('Learning store must be inside the workspace')
        self.events_dir = self.store / 'events'

    def local_file(self, value):
        relative = Path(text(value, 'evidence path'))
        if relative.is_absolute() or '..' in relative.parts or re.match(r'^[A-Za-z]:', str(relative)):
            raise LearningError('Evidence paths must be workspace-relative and cannot traverse parents')
        path = (self.workspace / relative).resolve(strict=True)
        if not path.is_relative_to(self.workspace) or not path.is_file():
            raise LearningError('Evidence must resolve to a file inside the workspace')
        return path

    def batch(self, value):
        relative = Path(text(value, 'batch'))
        if relative.is_absolute() or '..' in relative.parts or re.match(r'^[A-Za-z]:', str(relative)):
            raise LearningError('Batch must be a workspace-relative directory')
        path = (self.workspace / relative).resolve(strict=True)
        if not path.is_relative_to(self.workspace) or not path.is_dir():
            raise LearningError('Batch must resolve inside the workspace')
        return path.relative_to(self.workspace).as_posix()

    def evidence(self, rows, *, required=True):
        if not isinstance(rows, list) or (required and not rows):
            raise LearningError('Evidence must be a list of retained files with SHA-256')
        output = []
        for row in rows:
            object_fields(row, {'role', 'path', 'sha256', 'description'}, {'role', 'path', 'sha256'}, 'evidence')
            if row['role'] not in ROLES:
                raise LearningError('Unknown evidence role: ' + str(row['role']))
            if not re.fullmatch(r'[a-f0-9]{64}', str(row['sha256'])):
                raise LearningError('Evidence needs a lowercase SHA-256')
            path = self.local_file(row['path'])
            if file_sha(path) != row['sha256']:
                raise LearningError('Evidence hash changed: ' + row['path'])
            saved = {**row, 'path': path.relative_to(self.workspace).as_posix()}
            output.append(saved)
        return output

    def events(self):
        if not self.events_dir.exists():
            return []
        rows, previous, keys = [], None, set()
        for sequence, path in enumerate(sorted(self.events_dir.glob('*.json')), 1):
            event = read_json(path)
            checksum = event.get('event_sha256')
            body = {k: v for k, v in event.items() if k != 'event_sha256'}
            if (event.get('schema') != EVENT_SCHEMA or event.get('sequence') != sequence
                    or event.get('previous_event_sha256') != previous
                    or event.get('kind') not in KINDS or checksum != digest(body)
                    or path.name != event.get('id', '') + '.json'
                    or event.get('request_key') in keys):
                raise LearningError('Event history is incomplete or changed: ' + path.name)
            expected_id = self.event_id(sequence, event['kind'], event['payload'], event['request_key'])
            if event['id'] != expected_id:
                raise LearningError('Event identity differs from its content: ' + path.name)
            keys.add(event['request_key'])
            rows.append(event)
            previous = checksum
        return rows

    @staticmethod
    def event_id(sequence, kind, payload, request_key):
        signature = digest({'kind': kind, 'payload': payload, 'request_key': request_key})
        return f'evt-{sequence:06d}-{signature[:12]}'

    @contextmanager
    def lock(self):
        self.events_dir.mkdir(parents=True, exist_ok=True)
        lock = self.store / '.write.lock'
        try:
            descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError:
            raise LearningError('Another writer or an interrupted write owns .write.lock; reconcile it before retrying') from None
        try:
            with os.fdopen(descriptor, 'w', encoding='utf-8') as stream:
                json.dump({'pid': os.getpid()}, stream)
            yield
        finally:
            lock.unlink(missing_ok=True)

    def validate_feedback(self, payload, state):
        required = {'batch', 'revision', 'dimension', 'decision', 'reviewer', 'target',
                    'method', 'observation', 'action', 'evidence'}
        object_fields(payload, required | {'quote', 'supersedes'}, required, 'feedback')
        payload['batch'] = self.batch(payload['batch'])
        text(payload['revision'], 'revision')
        if payload['dimension'] not in DIMENSIONS or payload['decision'] not in DECISIONS:
            raise LearningError('Unknown editorial feedback dimension or decision')
        object_fields(payload['reviewer'], {'kind', 'name'}, {'kind', 'name'}, 'reviewer')
        if payload['reviewer']['kind'] not in {'human_user', 'agent'}:
            raise LearningError('Machine checks must use record-check, not editorial feedback')
        text(payload['reviewer']['name'], 'reviewer name')
        target = payload['target']
        object_fields(target, {'clause_id', 'narration', 'start', 'end'}, {'clause_id', 'narration', 'start', 'end'}, 'target')
        text(target['clause_id'], 'clause_id')
        text(target['narration'], 'narration')
        if (not isinstance(target['start'], (int, float)) or not isinstance(target['end'], (int, float))
                or not math.isfinite(target['start']) or not math.isfinite(target['end'])
                or target['start'] < 0 or target['end'] < target['start']):
            raise LearningError('Target needs a finite, ordered time interval in seconds')
        if payload['method'] not in METHODS:
            raise LearningError('Unknown review method')
        if payload['method'] == 'human_feedback' and payload['reviewer']['kind'] != 'human_user':
            raise LearningError('An agent review cannot stand in for explicit human feedback')
        text(payload['observation'], 'observation')
        text(payload['action'], 'action')
        payload['evidence'] = self.evidence(payload['evidence'], required=payload['decision'] != 'pending')
        roles = {e['role'] for e in payload['evidence']}
        if payload['decision'] != 'pending':
            if payload['method'] == 'metadata_only':
                raise LearningError('Metadata alone cannot decide editorial acceptance')
            if payload['dimension'] == 'visual_relevance' and not {'render', 'frame', 'asset'} <= roles:
                raise LearningError('Visual feedback needs the rendered file, inspected frame and source asset hashes')
            if payload['dimension'] == 'visual_relevance' and payload['method'] not in {'rendered_frame_comparison', 'continuous_av_review', 'human_feedback'}:
                raise LearningError('Visual feedback requires actual rendered-image comparison or explicit human feedback')
            if payload['dimension'] == 'script' and ('script' not in roles or payload['method'] not in {'script_review', 'continuous_av_review', 'human_feedback'}):
                raise LearningError('Script feedback needs the reviewed script and an editorial review method')
            if payload['dimension'] in {'voice', 'sound'} and 'audio' not in roles:
                raise LearningError('Auditory feedback needs the actual reviewed audio file')
            if payload['dimension'] in {'voice', 'sound'} and payload['method'] not in {'audio_listening', 'continuous_av_review', 'human_feedback'}:
                raise LearningError('Auditory feedback requires listening or explicit human feedback')
            if payload['dimension'] == 'overall' and payload['reviewer']['kind'] == 'agent' and payload['method'] != 'continuous_av_review':
                raise LearningError('An agent overall verdict requires continuous AV review')
            if payload['dimension'] == 'overall' and 'render' not in roles:
                raise LearningError('An overall verdict must identify the actual rendered revision by hash')
        if payload['reviewer']['kind'] == 'human_user' and payload['decision'] != 'pending':
            quote = text(payload.get('quote'), 'exact user quote')
            if payload['method'] != 'human_feedback':
                raise LearningError('Human-user feedback must preserve its explicit feedback method')
            feedback_files = [self.local_file(e['path']) for e in payload['evidence'] if e['role'] == 'feedback']
            if not feedback_files or not any(quote in p.read_text(encoding='utf-8') for p in feedback_files):
                raise LearningError('Exact user quote must occur in the retained feedback evidence')
        elif payload.get('quote'):
            raise LearningError('Do not attribute a user quote to an agent review')
        previous = state['effective'].get(feedback_key(payload))
        if previous and payload.get('supersedes') != previous:
            raise LearningError('A review already exists for this target; explicitly supersede its latest event')
        if payload.get('supersedes') and payload['supersedes'] != previous:
            raise LearningError('Superseded feedback must be the latest review of this exact target')

    def validate(self, kind, payload, state):
        no_secrets(payload)
        if kind == 'feedback_recorded':
            self.validate_feedback(payload, state)
        elif kind == 'technical_check_recorded':
            keys = {'batch', 'revision', 'check_id', 'result', 'observation', 'evidence'}
            object_fields(payload, keys, keys, 'technical check')
            payload['batch'] = self.batch(payload['batch'])
            for key in ['revision', 'check_id', 'observation']:
                text(payload[key], key)
            if payload['result'] not in {'passed', 'failed'}:
                raise LearningError('Technical result must be passed or failed')
            payload['evidence'] = self.evidence(payload['evidence'])
        elif kind == 'lesson_proposed':
            keys = {'title', 'category', 'rule', 'action', 'rationale', 'applies_to', 'source_feedback_ids'}
            object_fields(payload, keys, keys, 'lesson proposal')
            if payload['category'] not in DIMENSIONS:
                raise LearningError('Unknown lesson category')
            for key in ['title', 'rule', 'action', 'rationale']:
                text(payload[key], key)
            if not isinstance(payload['applies_to'], list) or not payload['applies_to']:
                raise LearningError('Lesson needs an explicit application scope')
            for item in payload['applies_to']:
                text(item, 'application scope')
            ids = payload['source_feedback_ids']
            if not isinstance(ids, list) or not ids:
                raise LearningError('Lesson needs traceable editorial feedback')
            for eid in ids:
                source = state['feedback'].get(eid)
                if not source or source['payload']['decision'] == 'pending':
                    raise LearningError('Technical checks and pending reviews cannot be lesson sources')
                if state['effective'].get(feedback_key(source['payload'])) != eid:
                    raise LearningError('A lesson source must be the current review of its target')
                self.evidence(source['payload']['evidence'])
        elif kind in {'lesson_applied', 'lesson_verified', 'lesson_retired'}:
            lesson = state['lessons'].get(payload.get('lesson_id'))
            if not lesson or lesson['retirement']:
                raise LearningError('Lesson does not exist or is retired')
            if kind == 'lesson_applied':
                keys = {'lesson_id', 'batch', 'revision', 'change', 'evidence'}
                object_fields(payload, keys, keys, 'lesson application')
                if lesson['verification']:
                    raise LearningError('Verified lessons are immutable; propose a new lesson to change the rule')
                payload['batch'] = self.batch(payload['batch'])
                text(payload['revision'], 'revision')
                text(payload['change'], 'actual change')
                payload['evidence'] = self.evidence(payload['evidence'])
                if not any(e['role'] in {'render', 'asset', 'script', 'code'} for e in payload['evidence']):
                    raise LearningError('Application needs an actual changed artifact, not only a report')
            elif kind == 'lesson_verified':
                keys = {'lesson_id', 'application_id', 'feedback_id', 'conclusion'}
                object_fields(payload, keys, keys, 'lesson verification')
                if lesson['verification'] or not lesson['applications']:
                    raise LearningError('Lesson must be applied and not already verified')
                application = lesson['applications'][-1]
                if payload['application_id'] != application['id']:
                    raise LearningError('Verify the latest application, not an older attempt')
                feedback = state['feedback'].get(payload['feedback_id'])
                if not feedback or feedback['payload']['decision'] != 'accepted':
                    raise LearningError('Verification needs accepted editorial feedback; decode success is insufficient')
                review = feedback['payload']
                applied = application['payload']
                if (review['batch'], review['revision']) != (applied['batch'], applied['revision']):
                    raise LearningError('Verification must review the batch and revision where the lesson was applied')
                if feedback['sequence'] <= application['sequence']:
                    raise LearningError('Verification review must occur after the actual application')
                if state['effective'][feedback_key(review)] != feedback['id']:
                    raise LearningError('Superseded feedback cannot verify a lesson')
                category = lesson['proposal']['payload']['category']
                if review['dimension'] != category:
                    raise LearningError('Verification feedback must match the lesson category')
                for source_id in lesson['proposal']['payload']['source_feedback_ids']:
                    source = state['feedback'][source_id]
                    if state['effective'].get(feedback_key(source['payload'])) != source_id:
                        raise LearningError('The source review was superseded; reassess the proposed lesson')
                    self.evidence(source['payload']['evidence'])
                self.evidence(review['evidence'])
                self.evidence(applied['evidence'])
                text(payload['conclusion'], 'verification conclusion')
            else:
                object_fields(payload, {'lesson_id', 'reason'}, {'lesson_id', 'reason'}, 'lesson retirement')
                text(payload['reason'], 'retirement reason')
        else:
            raise LearningError('Unknown event kind')

    def append(self, kind, payload, request_key):
        request_key = text(request_key, 'request_key')
        # Copy before normalization so caller dictionaries are never mutated.
        payload = json.loads(canonical(payload))
        with self.lock():
            events = self.events()
            previous_request = next((e for e in events if e['request_key'] == request_key), None)
            if previous_request:
                if previous_request['kind'] != kind or previous_request['payload'] != payload:
                    raise LearningError('Request key was already used with different content')
                return previous_request
            self.validate(kind, payload, state_from(events))
            sequence = len(events) + 1
            eid = self.event_id(sequence, kind, payload, request_key)
            event = {'schema': EVENT_SCHEMA, 'id': eid, 'sequence': sequence,
                'created_at_utc': datetime.now(timezone.utc).isoformat(), 'kind': kind,
                'request_key': request_key, 'previous_event_sha256': events[-1]['event_sha256'] if events else None,
                'payload': payload}
            event['event_sha256'] = digest(event)
            temporary = self.events_dir / ('.' + uuid.uuid4().hex + '.pending')
            final = self.events_dir / (eid + '.json')
            try:
                with temporary.open('x', encoding='utf-8', newline='\n') as stream:
                    stream.write(json.dumps(event, ensure_ascii=False, indent=2) + '\n')
                    stream.flush()
                    os.fsync(stream.fileno())
                # Publish an already complete file atomically. Link fails if it exists;
                # unlike replace(), this can never overwrite a prior event.
                os.link(temporary, final)
            finally:
                temporary.unlink(missing_ok=True)
            return event

    def audit(self, expected_head=None):
        events = self.events()
        failures = []
        current_head = events[-1]['event_sha256'] if events else None
        if expected_head is not None and current_head != expected_head:
            failures.append({'event_id': None, 'path': 'events/',
                'error': 'Ledger head differs from the previously pinned receipt'})
        for event in events:
            for row in event['payload'].get('evidence', []):
                try:
                    self.evidence([row])
                except (LearningError, OSError) as error:
                    failures.append({'event_id': event['id'], 'path': row['path'], 'error': str(error)})
        return {'schema': 'reference-video-learning-audit/1', 'events': len(events),
            'ledger_head_sha256': current_head,
            'file_integrity': 'passed' if not failures else 'changed_or_missing', 'failures': failures,
            'scope': 'Event chain and retained file hashes, not editorial or user acceptance.'}

    def guidance(self):
        events = self.events()
        state = state_from(events)
        lessons, excluded, acceptance = [], [], []
        for eid, lesson in state['lessons'].items():
            proposal = lesson['proposal']['payload']
            verification = lesson['verification']
            if lesson['retirement'] or not verification:
                excluded.append({'id': eid, 'reason': 'retired' if lesson['retirement'] else 'not_verified'})
                continue
            verified = verification['payload']
            feedback = state['feedback'][verified['feedback_id']]
            review = feedback['payload']
            if state['effective'][feedback_key(review)] != feedback['id']:
                excluded.append({'id': eid, 'reason': 'verification_feedback_superseded'})
                continue
            application = lesson['applications'][-1]
            evidence = application['payload']['evidence'] + review['evidence']
            sources = [state['feedback'][source_id] for source_id in proposal['source_feedback_ids']]
            if any(state['effective'].get(feedback_key(source['payload'])) != source['id'] for source in sources):
                excluded.append({'id': eid, 'reason': 'source_feedback_superseded'})
                continue
            try:
                self.evidence(evidence)
                for source in sources:
                    self.evidence(source['payload']['evidence'])
            except (LearningError, OSError) as error:
                excluded.append({'id': eid, 'reason': 'evidence_changed_or_missing', 'detail': str(error)})
                continue
            lessons.append({**proposal, 'id': eid, 'status': 'verified',
                'application_id': application['id'], 'verification_id': verification['id'],
                'verified_by': review['reviewer'], 'acceptance_basis': review['method'],
                'verification_from_user_feedback': review['reviewer']['kind'] == 'human_user',
                'source_reviews': [{'id': source_id, **state['feedback'][source_id]['payload']}
                                   for source_id in proposal['source_feedback_ids']],
                'evidence': evidence})
        for feedback_id in state['effective'].values():
            review = state['feedback'][feedback_id]['payload']
            # User approval is a separate explicit overall decision, never inferred
            # from a technical result or from an agent's clause-level acceptance.
            if review['reviewer']['kind'] == 'human_user' and review['dimension'] == 'overall':
                valid = True
                try:
                    self.evidence(review['evidence'])
                except (LearningError, OSError):
                    valid = False
                acceptance.append({'batch': review['batch'], 'revision': review['revision'],
                    'decision': review['decision'], 'feedback_id': feedback_id,
                    'exact_quote': review.get('quote'), 'evidence_integrity': valid,
                    'user_approved': review['decision'] == 'accepted' and valid})
        return {'schema': GUIDANCE_SCHEMA, 'generated_at_utc': datetime.now(timezone.utc).isoformat(),
            'ledger_head_sha256': events[-1]['event_sha256'] if events else None,
            'source_ledger': self.store.relative_to(self.workspace).as_posix(),
            'scope': 'Editorial guidance only; no runtime visual or voice preset overrides.',
            'lessons': lessons, 'excluded_lessons': excluded, 'user_acceptance_by_batch': acceptance,
            'limitations': ['Local evidence-backed process improvements, not model-weight training.',
                'Technical checks do not establish visual quality, auditory quality or user approval.',
                'Agent verification is labeled separately from explicit human-user approval.',
                'No publishing, messages, paid generation or scheduled tasks are triggered by this export.']}

    def report(self):
        events = self.events()
        state = state_from(events)
        guidance = self.guidance()
        batches = {}
        for eid in state['effective'].values():
            review = state['feedback'][eid]['payload']
            key = (review['batch'], review['revision'])
            summary = batches.setdefault(key, {'batch': key[0], 'revision': key[1],
                'editorial_targets': 0, 'decisions': {decision: 0 for decision in sorted(DECISIONS)}})
            summary['editorial_targets'] += 1
            summary['decisions'][review['decision']] += 1
        return {'schema': 'reference-video-learning-report/1', 'events': len(events),
            'batches': list(batches.values()),
            'feedback': [{'id': eid, **state['feedback'][eid]['payload']} for eid in state['effective'].values()],
            'technical_checks': [{'id': e['id'], **e['payload']} for e in state['checks']],
            'lessons': [{'id': eid, 'title': lesson['proposal']['payload']['title'],
                         'state': 'retired' if lesson['retirement'] else 'verified' if lesson['verification'] else 'applied' if lesson['applications'] else 'proposed'}
                        for eid, lesson in state['lessons'].items()],
            'verified_guidance_count': len(guidance['lessons']),
            'excluded_lessons': guidance['excluded_lessons'],
            'user_acceptance_by_batch': guidance['user_acceptance_by_batch']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--store', type=Path, required=True)
    parser.add_argument('--workspace', type=Path, default=ROOT)
    commands = parser.add_subparsers(dest='command', required=True)
    mutations = {'record-feedback': 'feedback_recorded', 'record-check': 'technical_check_recorded',
        'propose-lesson': 'lesson_proposed', 'apply-lesson': 'lesson_applied',
        'verify-lesson': 'lesson_verified', 'retire-lesson': 'lesson_retired'}
    for name in mutations:
        command = commands.add_parser(name)
        command.add_argument('--input', type=Path, required=True)
        command.add_argument('--request-key', required=True)
    for name in ['export-guidance', 'report', 'audit']:
        command = commands.add_parser(name)
        command.add_argument('--output', type=Path)
        if name == 'audit':
            command.add_argument('--expected-head', help='Previously pinned ledger SHA-256, for detecting unexpected truncation or extension')
    args = parser.parse_args()
    try:
        store = LearningStore(args.store, args.workspace)
        if args.command in mutations:
            event = store.append(mutations[args.command], read_json(args.input), args.request_key)
            result = {'id': event['id'], 'kind': event['kind'], 'sequence': event['sequence'], 'event_sha256': event['event_sha256']}
        else:
            result = store.audit(args.expected_head) if args.command == 'audit' else {'export-guidance': store.guidance, 'report': store.report}[args.command]()
            if args.output:
                output = args.output.resolve()
                if output.is_relative_to(store.events_dir) or output == store.store / '.write.lock':
                    raise LearningError('Derived exports cannot overwrite the event store')
                atomic_json(output, result)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if args.command == 'audit' and result['file_integrity'] != 'passed':
            return 1
        return 0
    except (LearningError, OSError, KeyError, ValueError) as error:
        parser.exit(1, f'Learning error: {error}\n')


if __name__ == '__main__':
    raise SystemExit(main())
