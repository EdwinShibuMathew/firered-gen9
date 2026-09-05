"""Exercise ledger checks without modifying repository data."""
from collections import Counter
import contextlib
import csv
import io
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from audit_availability import render_rows
import audit_release


class LedgerChecks(unittest.TestCase):
    @unittest.skipUnless((ROOT / '.upstream/cfru/src/party_menu.c').exists(), 'requires provisioned upstreams')
    def test_ledger_check_modes(self):
        for script in ('audit_availability.py', 'audit_forms.py'):
            with self.subTest(script=script), tempfile.TemporaryDirectory() as temp:
                target = Path(temp) / 'ledger.csv'
                command = [sys.executable, str(ROOT/'scripts'/script), '--require-complete', '--csv', str(target)]
                def run(*extra):
                    return subprocess.run(command + list(extra), capture_output=True, text=True)
                self.assertEqual(run('--check').returncode, 1)
                self.assertFalse(target.exists())
                self.assertEqual(run().returncode, 0)
                data, modified = target.read_bytes(), target.stat().st_mtime_ns
                self.assertEqual(run('--check').returncode, 0)
                self.assertEqual(target.stat().st_mtime_ns, modified)
                self.assertEqual(run().returncode, 0)
                self.assertEqual(target.read_bytes(), data)
                for broken in (data.splitlines(keepends=True)[0], data.replace(b'SPECIES_', b'INVALID_', 1)):
                    target.write_bytes(broken)
                    modified = target.stat().st_mtime_ns
                    self.assertEqual(run('--check').returncode, 1)
                    self.assertEqual(target.read_bytes(), broken)
                    self.assertEqual(target.stat().st_mtime_ns, modified)

    def test_availability_order_is_stable_and_duplicates_survive(self):
        with (ROOT/'data/availability.csv').open(newline='') as handle:
            rows = list(csv.DictReader(handle))
        rows.append(rows[0].copy())
        rendered = render_rows(rows)
        self.assertEqual(rendered, render_rows(list(reversed(rows))))
        decoded = list(csv.DictReader(io.StringIO(rendered.decode())))
        self.assertEqual(Counter(tuple(r.items()) for r in rows), Counter(tuple(r.items()) for r in decoded))

    def test_release_hygiene_rejects_tracked_rom(self):
        with patch.object(audit_release.subprocess, 'check_output', return_value='leaked.gba\n'), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(audit_release.main(), 1)

    def test_documentation_rejects_stale_current_hash(self):
        read = Path.read_text
        def stale(path, *args, **kwargs):
            text = read(path, *args, **kwargs)
            if path == ROOT/'docs/STATUS.md':
                import re
                text = re.sub(r'(Candidate ROM SHA-256: `)[0-9a-f]{64}', lambda m: m[1] + '0'*64, text)
            return text
        with patch.object(Path, 'read_text', stale), contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(SystemExit) as result:
                runpy.run_path(str(ROOT/'scripts/audit_documentation.py'), run_name='__main__')
            self.assertEqual(result.exception.code, 1)


if __name__ == '__main__':
    unittest.main()
