"""Preserve reviewed, unused LZ77 tail bytes in DPE sprite assembly."""
from __future__ import annotations

import json
from pathlib import Path
import re

SECTIONS = re.compile(r"(?ms)(^\s*\.section[^\n]*\n.*?)(?=^\s*\.section|\Z)")
DIRECTIVES = re.compile(r"(?m)^\s*\.(byte|hword)\s+([^\n]+)")
NUMBERS = re.compile(r"0x[0-9A-Fa-f]+|\d+")


def section_data(section):
    values = bytearray()
    tokens = []
    for directive in DIRECTIVES.finditer(section):
        width = 1 if directive.group(1) == "byte" else 2
        for number in NUMBERS.finditer(directive.group(2)):
            offset = len(values)
            values.extend(int(number.group(), 0).to_bytes(width, "little"))
            tokens.append((directive.start(2) + number.start(), directive.start(2) + number.end(), offset, width))
    if len(values) < 5 or values[0] != 0x10:
        return None
    size = int.from_bytes(values[1:4], "little")
    source, produced = 4, 0
    while produced < size and source < len(values):
        flags = values[source]
        source += 1
        for bit in range(8):
            if produced >= size:
                break
            width = 2 if flags & (0x80 >> bit) else 1
            if source + width > len(values):
                return None
            if width == 2:
                distance = ((values[source] & 0x0F) << 8 | values[source + 1]) + 1
                if distance > produced:
                    return None
            produced += (values[source] >> 4) + 3 if width == 2 else 1
            source += width
    if produced != size or not 1 <= len(values) - source <= 3:
        return None
    symbol = re.search(r"(?m)^([A-Za-z_]\w*):", section)
    if symbol is None:
        return None
    return symbol.group(1), values, source, tokens


def normalize(assembly_file: str, *, manifest: Path):
    tails = json.loads(manifest.read_text(encoding="utf-8"))

    def replace(match):
        section = match.group()
        parsed = section_data(section)
        if parsed is None:
            return section
        symbol, values, source, tokens = parsed
        padding = bytes.fromhex(tails.get(symbol, "00" * (len(values) - source)))
        if len(padding) != len(values) - source:
            raise ValueError(f"LZ77 padding length changed for {symbol}; review {manifest}")
        values[source:] = padding
        for start, end, offset, width in reversed(tokens):
            if offset + width > source:
                value = int.from_bytes(values[offset:offset + width], "little")
                section = section[:start] + f"0x{value:0{width * 2}X}" + section[end:]
        return section

    path = Path(assembly_file)
    original = path.read_text(encoding="utf-8")
    result = SECTIONS.sub(replace, original)
    if result != original:
        path.write_text(result, encoding="utf-8")
