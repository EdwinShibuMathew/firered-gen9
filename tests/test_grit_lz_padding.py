"""Padding edits must preserve the complete compressed stream."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from grit_lz_padding import normalize, section_data


def assembly(data, width=1):
    directive = "byte" if width == 1 else "hword"
    values = [int.from_bytes(data[i:i + width], "little") for i in range(0, len(data), width)]
    return '.section .rodata\nSprite:\n\t.' + directive + ' ' + ','.join(hex(v) for v in values) + '\n'


class PaddingTests(unittest.TestCase):
    def test_literal_stream_and_tail_boundaries(self):
        for size in (1, 2, 3):
            payload = b'\x10' + size.to_bytes(3, 'little') + b'\0' + b'A' * size
            padding = b'\xAA' * (4 - len(payload) % 4) if len(payload) % 4 else b''
            if not padding:
                continue
            for width in (1, 2):
                with self.subTest(size=size, width=width), tempfile.TemporaryDirectory() as directory:
                    path, manifest = Path(directory) / 'sprite.s', Path(directory) / 'tails.json'
                    path.write_text(assembly(payload + padding, width))
                    manifest.write_text('{}')
                    normalize(str(path), manifest=manifest)
                    _, values, source, _ = section_data(path.read_text())
                    self.assertEqual(values[:source], payload)
                    self.assertEqual(values[source:], b'\0' * len(padding))
                    before = path.stat().st_mtime_ns
                    normalize(str(path), manifest=manifest)
                    self.assertEqual(path.stat().st_mtime_ns, before)

    def test_backreference_and_preserved_baseline_tail(self):
        # Literal A followed by a distance-one, length-three copy yields AAAA.
        payload = bytes.fromhex('10 04 00 00 40 41 00 00')
        with tempfile.TemporaryDirectory() as directory:
            path, manifest = Path(directory) / 'sprite.s', Path(directory) / 'tails.json'
            path.write_text(assembly(payload + b'\x99'))
            manifest.write_text(json.dumps({'Sprite': '58'}))
            normalize(str(path), manifest=manifest)
            _, values, source, _ = section_data(path.read_text())
            self.assertEqual(values[:source], payload)
            self.assertEqual(values[source:], b'\x58')
            manifest.write_text(json.dumps({'Sprite': '5800'}))
            with self.assertRaisesRegex(ValueError, 'padding length changed'):
                normalize(str(path), manifest=manifest)

    def test_malformed_and_non_lz_sections_are_untouched(self):
        cases = ('00 01 00 00 00 41 99', '10 01 00 00 80',
                 '10 03 00 00 80 00 00 99', '10 01 00 00 00 41',
                 '10 01 00 00 00 41 01 02 03 04')
        for value in cases:
            with self.subTest(value=value):
                self.assertIsNone(section_data(assembly(bytes.fromhex(value))))


if __name__ == '__main__':
    unittest.main()
