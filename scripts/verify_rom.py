#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path


def digest(path: Path, algorithm: str) -> str:
    value = hashlib.new(algorithm)
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("rom", type=Path)
    parser.add_argument("--sha1")
    args = parser.parse_args()
    if not args.rom.is_file():
        parser.error(f"ROM not found: {args.rom}")
    sha1 = digest(args.rom, "sha1")
    print(f"path={args.rom}")
    print(f"size={args.rom.stat().st_size}")
    print(f"sha1={sha1}")
    print(f"sha256={digest(args.rom, 'sha256')}")
    if args.sha1 and sha1.lower() != args.sha1.lower():
        print(f"expected_sha1={args.sha1.lower()}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
