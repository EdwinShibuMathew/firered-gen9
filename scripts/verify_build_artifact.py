#!/usr/bin/env python3
"""Verify a pipeline artifact against its lock and boot-critical layout bytes."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "build-lock.json"
LEGENDARY_OPCODE_OFFSETS = (
    0x162558,
    0x16320F,
    0x16381B,
    0x163B96,
    0x1650B4,
    0x1651D9,
    0x16533A,
)
SOUND_INIT_OFFSET = 0x1DD0C8
SOUND_INIT_PRE_CFRU = bytes.fromhex("00 c5 94 00 04 00 00 00")
SOUND_INIT_POST_CFRU = bytes.fromhex("00 cc 94 00 04 00 00 00")


def digest(data: bytes, algorithm: str) -> str:
    return hashlib.new(algorithm, data).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact", choices=("vanilla", "dpe", "cfru"))
    parser.add_argument("rom", type=Path)
    args = parser.parse_args()

    if not args.rom.is_file():
        parser.error(f"ROM not found: {args.rom}")

    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    expected = lock["artifacts"][args.artifact]
    data = args.rom.read_bytes()
    checks = {
        "size": (len(data), expected["size"]),
        "sha1": (digest(data, "sha1"), expected["sha1"]),
        "sha256": (digest(data, "sha256"), expected["sha256"]),
    }
    if "payload_sha256" in expected:
        upstream = "dpe_gen9" if args.artifact == "dpe" else "cfru_expansion"
        offset = int(lock["upstreams"][upstream]["offset"], 16)
        checks["payload_sha256"] = (digest(data[offset:], "sha256"), expected["payload_sha256"])

    layout_expected = SOUND_INIT_POST_CFRU if args.artifact == "cfru" else SOUND_INIT_PRE_CFRU
    layout_actual = data[SOUND_INIT_OFFSET:SOUND_INIT_OFFSET + len(layout_expected)]
    failures = []
    for name, (actual, wanted) in checks.items():
        if actual != wanted:
            failures.append(f"{name}: expected {wanted}, got {actual}")
    if layout_actual != layout_expected:
        failures.append(
            f"sound init bytes at 0x{SOUND_INIT_OFFSET:X}: expected {layout_expected.hex()}, got {layout_actual.hex()}"
        )
    bad_opcodes = [offset for offset in LEGENDARY_OPCODE_OFFSETS if data[offset] != 0x2A]
    if bad_opcodes:
        failures.append("legendary clearflag opcode missing at " + ", ".join(f"0x{x:X}" for x in bad_opcodes))

    if failures:
        for failure in failures:
            print(f"FAIL {args.artifact}: {failure}")
        return 1

    print(f"PASS {args.artifact}: locked digest and boot-critical layout verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
