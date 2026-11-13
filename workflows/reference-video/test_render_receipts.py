"""Render receipt integrity under a simulated storage failure."""
import errno
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import render_directions


class ReceiptIntegrityTests(unittest.TestCase):
    def test_failed_flush_preserves_last_complete_receipt(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'attempt.json'
            render_directions.save(path, {'status': 'running', 'completedPatches': [0, 1]})
            before = path.read_bytes()
            with patch.object(render_directions.os, 'fsync', side_effect=OSError(errno.ENOSPC, 'disk full')):
                with self.assertRaises(OSError):
                    render_directions.save(path, {'status': 'completed'})
            self.assertEqual(path.read_bytes(), before)
            self.assertEqual(json.loads(path.read_text())['completedPatches'], [0, 1])
            render_directions.save(path, {'status': 'completed'})
            self.assertEqual(json.loads(path.read_text())['status'], 'completed')


if __name__ == '__main__':
    unittest.main()
