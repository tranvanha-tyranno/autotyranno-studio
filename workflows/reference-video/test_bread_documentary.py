"""Offline checks for the new film's arithmetic, source intervals and exact cuts."""
import unittest

from bread_documentary_content import CONTENT
from bread_documentary_edit import allocate, cuts


class BreadDocumentaryTests(unittest.TestCase):
    def test_same_bread_amounts_link_margin_and_purchasing_power(self):
        units = {u['id']: u for c in CONTENT['chapters'] for u in c['units']}
        before, after = units['b03']['data'], units['b05']['data']
        self.assertEqual(before['price'] - before['variable'] - before['fixed'], 3000)
        self.assertEqual(after['price'] - after['variable'] - after['fixed'], 2500)
        wage = units['b17']['data']
        self.assertEqual(wage['priceBefore'], before['price'])
        self.assertEqual(wage['priceAfter'], after['price'])
        quantity = units['b18']['data']
        self.assertAlmostEqual(wage['incomeAfter'] / wage['priceAfter'], quantity['after'], places=3)
        self.assertAlmostEqual((quantity['after'] / quantity['before'] - 1) * 100, -4.54545, places=3)

    def test_reusing_a_source_advances_to_non_overlapping_intervals(self):
        assets = [{'id': 'a', 'durationSeconds': 20, 'tags': ['bread']}]
        usage = {}
        a, first = allocate(assets, usage, ['bread'], 5, None)
        _, second = allocate(assets, usage, ['bread'], 5, a['id'])
        self.assertGreater(second, first + 5)
        allocate(assets, usage, ['bread'], 5, 'a')
        with self.assertRaisesRegex(ValueError, 'No inspected non-overlapping'):
            allocate(assets, usage, ['bread'], 5, 'a')

    def test_unrelated_footage_cannot_fill_a_missing_subject(self):
        with self.assertRaises(ValueError):
            allocate([{'id': 'a', 'durationSeconds': 20, 'tags': ['market']}], {}, ['flour'], 4, None)

    def test_sentence_cuts_keep_whole_interval_without_gaps_or_tiny_tail(self):
        for frames in [20, 150, 211, 1000]:
            unit = {'id': 'b99', 'from': 17, 'duration': frames, 'wordTimes': []}
            parts = cuts(unit)
            self.assertEqual(parts[0][0], 17)
            self.assertEqual(parts[-1][1], 17 + frames)
            self.assertEqual(sum(b - a for a, b, _ in parts), frames)
            self.assertTrue(all(parts[i][1] == parts[i+1][0] for i in range(len(parts)-1)))

    def test_short_quantity_explanation_clears_before_rest_of_long_unit(self):
        parts = cuts({'id': 'b18', 'from': 100, 'duration': 600, 'wordTimes': []})
        self.assertEqual(sum(1 for _, _, graphic in parts if graphic), 1)
        self.assertFalse(parts[-1][2])


if __name__ == '__main__':
    unittest.main()
