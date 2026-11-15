"""Offline coverage/cue checks for the substantive simulation upgrade."""
import unittest

from bread_lab import cues


class BreadLabTests(unittest.TestCase):
    def test_mismatched_phrase_order_is_not_relabelled_exact_alignment(self):
        unit = {'id': 'example', 'from': 0, 'duration': 300,
                'wordTimes': [{'text': 'Giá', 'start': 1, 'end': 1.2},
                              {'text': 'lương', 'start': 4, 'end': 4.2}]}
        self.assertEqual(cues(unit, ['giá', 'lương']), [30, 120])
        with self.assertRaisesRegex(ValueError, 'spoken order'):
            cues(unit, ['lương', 'giá'])

    def test_unknown_narration_cue_blocks_visual_mapping(self):
        unit = {'id': 'example', 'from': 0, 'duration': 300,
                'wordTimes': [{'text': 'Giá', 'start': 1, 'end': 1.2}]}
        with self.assertRaisesRegex(ValueError, 'Missing exact phrase'):
            cues(unit, ['lương'])


if __name__ == '__main__':
    unittest.main()
