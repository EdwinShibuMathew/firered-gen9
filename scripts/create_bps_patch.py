#!/usr/bin/env python3
"""Create a deterministic BPS patch using SourceRead/TargetRead runs."""
from __future__ import annotations
import argparse
import binascii
from pathlib import Path

def number(value: int) -> bytes:
    out = bytearray()
    while True:
        byte = value & 0x7F
        value >>= 7
        if value == 0:
            out.append(byte | 0x80)
            return bytes(out)
        out.append(byte)
        value -= 1

def create(source: bytes, target: bytes) -> bytes:
    patch = bytearray(b"BPS1")
    patch += number(len(source)) + number(len(target)) + number(0)
    pos = 0
    while pos < len(target):
        equal = pos < len(source) and source[pos] == target[pos]
        end = pos + 1
        if equal:
            while end < len(target) and end < len(source) and source[end] == target[end]:
                end += 1
            patch += number(((end - pos - 1) << 2) | 0)
        else:
            while end < len(target) and not (end < len(source) and source[end] == target[end]):
                end += 1
            patch += number(((end - pos - 1) << 2) | 1)
            patch += target[pos:end]
        pos = end
    patch += binascii.crc32(source).to_bytes(4, "little")
    patch += binascii.crc32(target).to_bytes(4, "little")
    patch += binascii.crc32(patch).to_bytes(4, "little")
    return bytes(patch)

def read_number(data: bytes, offset: int) -> tuple[int, int]:
    value = 0
    shift = 1
    while True:
        byte = data[offset]
        offset += 1
        value += (byte & 0x7F) * shift
        if byte & 0x80:
            return value, offset
        shift <<= 7
        value += shift

def verify(source: bytes, target: bytes, patch: bytes) -> bool:
    if patch[:4] != b"BPS1" or binascii.crc32(patch[:-4]) != int.from_bytes(patch[-4:], "little"):
        return False
    offset = 4
    source_size, offset = read_number(patch, offset)
    target_size, offset = read_number(patch, offset)
    metadata_size, offset = read_number(patch, offset)
    offset += metadata_size
    output = bytearray()
    while len(output) < target_size:
        action, offset = read_number(patch, offset)
        length, mode = (action >> 2) + 1, action & 3
        if mode == 0:
            output += source[len(output):len(output) + length]
        elif mode == 1:
            output += patch[offset:offset + length]
            offset += length
        else:
            return False
    return (source_size == len(source) and bytes(output) == target
            and binascii.crc32(source) == int.from_bytes(patch[-12:-8], "little")
            and binascii.crc32(target) == int.from_bytes(patch[-8:-4], "little"))

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("target", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--source-sha1", required=True)
    args = parser.parse_args()
    import hashlib
    source = args.source.read_bytes()
    actual = hashlib.sha1(source).hexdigest()
    if actual != args.source_sha1.lower():
        raise SystemExit(f"source SHA-1 mismatch: expected {args.source_sha1.lower()}, got {actual}")
    target = args.target.read_bytes()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    patch = create(source, target)
    if not verify(source, target, patch):
        raise SystemExit("generated BPS failed round-trip verification")
    args.output.write_bytes(patch)
    print(f"source_sha1={actual}")
    print(f"target_sha256={hashlib.sha256(target).hexdigest()}")
    print(f"patch_sha256={hashlib.sha256(args.output.read_bytes()).hexdigest()}")
    print(f"patch={args.output.resolve()}")
    print("round_trip=PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
