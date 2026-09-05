"""Regression cases for filesystem-independent build ordering."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from ordered_build_inputs import ordered_glob


class BuildOrderTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.manifest = Path(self.temp.name) / "order.json"
        self.write_order(["src/b.c", "src/a.c"])

    def write_order(self, paths):
        self.manifest.write_text(json.dumps({"schema_version": 1, "groups": {"src/*.c": paths}}))

    def ordered(self, discovered):
        with patch("ordered_build_inputs.discover", return_value=discovered):
            return ordered_glob("./src/*.c", manifest=self.manifest)

    def test_reversed_creation_order_keeps_reviewed_order_and_path_spelling(self):
        expected = ["./src/b.c", "./src/a.c"]
        self.assertEqual(self.ordered(expected), expected)
        self.assertEqual(self.ordered(list(reversed(expected))), expected)

    def test_missing_input(self):
        with self.assertRaisesRegex(ValueError, "missing=.*src/b.c"):
            self.ordered(["src/a.c"])

    def test_unlisted_input(self):
        with self.assertRaisesRegex(ValueError, "unexpected=.*src/c.c"):
            self.ordered(["src/a.c", "src/b.c", "src/c.c"])

    def test_duplicate_manifest_entry(self):
        self.write_order(["src/a.c", "src/a.c"])
        with self.assertRaisesRegex(ValueError, "Duplicate build inputs"):
            self.ordered(["src/a.c"])

    def test_duplicate_discovery(self):
        with self.assertRaisesRegex(ValueError, "Duplicate discovered"):
            self.ordered(["src/a.c", "./src/a.c", "src/b.c"])

    def test_unlisted_pattern(self):
        with self.assertRaisesRegex(ValueError, "Unlisted build-input pattern"):
            ordered_glob("other/*.c", manifest=self.manifest)

    def test_paths_cannot_escape_checkout(self):
        for paths in (["../other.c"], ["/tmp/other.c"], ["src/../other.c"]):
            with self.subTest(paths=paths):
                self.write_order(paths)
                with self.assertRaisesRegex(ValueError, "Invalid relative paths"):
                    self.ordered([])


if __name__ == "__main__":
    unittest.main()
