"""Regression tests: stale script reviews and missing chapters cannot spend TTS."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import editorial_gate as gate
import eleven_audio as audio


def reviewed_map():
    value = {'schema': gate.SCHEMA, 'title': 'The receipt', 'centralQuestion': 'Where did the money go?',
             'thesis': 'Revenue and retained money differ.', 'viewerStake': 'Read a shop bill.',
             'hookPromise': 'Follow one receipt.', 'exclusions': ['Monetary policy'],
             'units': [{'id': 'h', 'phase': 'hook', 'text': 'The price rose. Who gained?'},
                       {'id': 'd', 'phase': 'disclaimer', 'text': 'This is an illustrative shop.'},
                       {'id': 'a', 'phase': 'content', 'text': 'The input bill rose faster than revenue.'},
                       {'id': 'b', 'phase': 'content', 'text': 'More revenue can leave less money.'},
                       {'id': 'c', 'phase': 'cta', 'text': 'Compare both sides of your receipt.'}],
             'chapters': [], 'payoff': {'answer': 'The input bill absorbed the increase.', 'unitIds': ['b']}}
    for uid in ['a', 'b']:
        value['chapters'].append({'id': uid, 'title': 'A bill' if uid == 'a' else 'The answer',
                                 'unitIds': [uid], 'question': 'Which change matters?',
                                 'answer': 'Compare the retained amount.', 'mechanism': 'Inputs absorb revenue.',
                                 'whyItMatters': 'The price alone hides the cost.', 'takeaway': 'Read both numbers.',
                                 'evidenceExamples': [{'kind': 'illustrative', 'detail': 'A hypothetical bill.'}],
                                 'emphasis': {'spokenQuote': value['units'][2 if uid == 'a' else 3]['text'],
                                              'visualFocus': 'The two amounts', 'purpose': 'Explain the gap.'},
                                 'bridge': {'reason': 'The bill sets the retained amount.',
                                            'nextQuestion': 'Who gained?'}})
    accept(value)
    return value


def accept(value):
    value['review'] = {'status': 'accepted', 'method': 'full_script_read',
                       'reviewer': {'kind': 'agent', 'name': 'Fixture reviewer'},
                       'contentSHA256': gate.content_hash(value), 'unresolvedIssues': [],
                       'checks': {d: {'decision': 'accepted', 'observation': 'Read the complete test fixture.'}
                                  for d in gate.DIMENSIONS}}


class EditorialGateTests(unittest.TestCase):
    def test_chapter_aligned_take_and_full_script_are_eligible_without_user_approval(self):
        value = reviewed_map()
        for text in [value['units'][2]['text'], '\n\n'.join(u['text'] for u in value['units'])]:
            report = gate.validate(value, text)
            self.assertTrue(report['readyForNewNarration'], report['errors'])
            self.assertEqual(report['userApproval'], 'not_established')

    def test_removed_reordered_or_duplicated_content_is_blocked(self):
        for ids in [[], ['b', 'a'], ['a', 'a'], ['missing']]:
            value = reviewed_map()
            value['chapters'] = [value['chapters'][0]]
            value['chapters'][0]['unitIds'] = ids
            accept(value)
            self.assertFalse(gate.validate(value)['readyForNewNarration'])

    def test_changing_script_or_chapter_reasoning_invalidates_old_review(self):
        for field in ['text', 'mechanism']:
            value = reviewed_map()
            if field == 'text':
                value['units'][2][field] += ' An extra claim.'
            else:
                value['chapters'][0][field] = 'A different causal account.'
            self.assertIn('Review is stale', ' '.join(gate.validate(value)['errors']))

    def test_headings_alone_and_unresolved_issues_are_insufficient(self):
        value = reviewed_map()
        value['chapters'][0]['mechanism'] = ''
        accept(value)
        value['review']['unresolvedIssues'] = ['The transition is missing.']
        self.assertFalse(gate.validate(value)['readyForNewNarration'])

    def test_new_take_must_match_whole_units_and_emphasis_must_be_spoken(self):
        value = reviewed_map()
        self.assertFalse(gate.validate(value, 'The input bill rose.')['readyForNewNarration'])
        value['chapters'][0]['emphasis']['spokenQuote'] = 'Revenue guarantees profits.'
        accept(value)
        self.assertFalse(gate.validate(value)['readyForNewNarration'])

    def test_main_answer_must_precede_cta_in_last_chapter(self):
        value = reviewed_map()
        value['payoff']['unitIds'] = ['c']
        accept(value)
        self.assertFalse(gate.validate(value)['readyForNewNarration'])

    def test_take_must_preserve_punctuation_including_numeric_signs(self):
        value = reviewed_map()
        value['units'][2]['text'] = 'The change is -2.8 percent.'
        value['chapters'][0]['emphasis']['spokenQuote'] = value['units'][2]['text']
        accept(value)
        self.assertTrue(gate.validate(value, 'The change is -2.8 percent.')['readyForNewNarration'])
        for altered in ['The change is 2.8 percent.', 'The change is -2,8 percent.']:
            self.assertFalse(gate.validate(value, altered)['readyForNewNarration'])

    def test_emphasis_preserves_numeric_signs_separators_and_punctuation(self):
        value = reviewed_map()
        value['units'][2]['text'] = 'The change is -2.8 percent; the old price was 2,000.'
        value['chapters'][0]['emphasis']['spokenQuote'] = 'The change is -2.8 percent;'
        accept(value)
        self.assertTrue(gate.validate(value)['readyForNewNarration'])
        for altered in ['The change is 2.8 percent;', 'The change is -2,8 percent;',
                        'The change is -2.8 percent.']:
            value['chapters'][0]['emphasis']['spokenQuote'] = altered
            accept(value)
            self.assertFalse(gate.validate(value)['readyForNewNarration'])

    def test_short_emphasis_cannot_extract_an_unsigned_or_partial_number(self):
        source = 'The change is -2.8 percent; the price is 2,000.'
        for quote in ['2.8', '8', '2,00', '000', 'change is 2.8']:
            self.assertFalse(gate.exact_quote_in_text(quote, source), quote)
        for quote in ['-2.8', '2,000', 'The change is -2.8 percent;', 'price is 2,000.']:
            self.assertTrue(gate.exact_quote_in_text(quote, source), quote)

    def test_default_still_requires_disclaimer_but_explicit_user_override_allows_omission(self):
        value = reviewed_map()
        value['units'] = [u for u in value['units'] if u['phase'] != 'disclaimer']
        accept(value)
        self.assertFalse(gate.validate(value)['readyForNewNarration'])
        value['structurePolicy'] = 'no-spoken-disclaimer-user-requested'
        accept(value)
        self.assertTrue(gate.validate(value)['readyForNewNarration'])

    def test_unknown_policy_and_disclaimer_under_omission_policy_are_blocked(self):
        value = reviewed_map()
        for policy in ['omit-disclaimer', 'no-spoken-disclaimer-user-requested']:
            value['structurePolicy'] = policy
            accept(value)
            self.assertFalse(gate.validate(value)['readyForNewNarration'])

    def test_changing_structure_policy_invalidates_old_review(self):
        value = reviewed_map()
        value['structurePolicy'] = 'no-spoken-disclaimer-user-requested'
        self.assertIn('Review is stale', ' '.join(gate.validate(value)['errors']))

    def test_missing_map_stops_before_credentials_or_network(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            target = root / 'batch/audio/chapter.mp3'
            with patch.object(audio, 'PROJECT', root), patch.object(audio, 'CACHE', root / 'cache'), \
                 patch.object(audio, 'key') as key, patch.object(audio.requests, 'post') as post:
                with self.assertRaisesRegex(ValueError, 'editorial-map'):
                    audio.generate(target, '/v1/text-to-speech/example/with-timestamps', {'text': 'Unreviewed'}, True)
                key.assert_not_called()
                post.assert_not_called()
                self.assertFalse(target.with_suffix('.intent.json').exists())

    def test_existing_exact_take_remains_reusable_without_rewriting_old_batch(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            target = root / 'old.mp3'
            target.write_bytes(b'existing audio')
            endpoint, payload = '/v1/text-to-speech/example/with-timestamps', {'text': 'Old script'}
            digest = audio.hashlib.sha256(json.dumps({'endpoint': endpoint, 'body': payload},
                sort_keys=True, ensure_ascii=False).encode()).hexdigest()
            target.with_suffix('.receipt.json').write_text(json.dumps({'request_hash': digest}))
            target.with_suffix('.alignment.json').write_text('{}')
            with patch.object(audio, 'CACHE', root / 'cache'), patch.object(audio, 'key') as key, \
                 patch.object(audio.requests, 'post') as post:
                self.assertEqual(audio.generate(target, endpoint, payload, True), target)
                key.assert_not_called()
                post.assert_not_called()

    def test_batch_map_discovery_and_mutation_detection(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            folder = root / 'batch'
            folder.mkdir()
            value = reviewed_map()
            path = folder / 'editorial-map.json'
            path.write_text(json.dumps(value), encoding='utf-8')
            receipt = gate.require_for_take(folder / 'audio/new.mp3', value['units'][2]['text'], root)
            self.assertEqual(receipt['map'], 'batch/editorial-map.json')
            value['units'][2]['text'] = 'A silently changed script.'
            path.write_text(json.dumps(value), encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'stale'):
                gate.require_for_take(folder / 'audio/new.mp3', value['units'][2]['text'], root)


if __name__ == '__main__':
    unittest.main()
