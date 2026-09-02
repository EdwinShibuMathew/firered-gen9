#!/usr/bin/env python3
"""Verify the locked M6 Contrary Charizard starter source overlays."""
from __future__ import annotations
import hashlib, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def main() -> int:
    lock = json.loads((ROOT / "build-lock.json").read_text())
    required = {"dpe_contrary_charizard_starter_data", "cfru_contrary_charizard_starter_gift"}
    ok = True
    for key in required:
        entry = lock["compatibility_overlays"][key]
        path = ROOT / entry["path"]
        digest = hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else ""
        passed = path.exists() and digest == entry["sha256"]
        print(f"{'PASS' if passed else 'FAIL'} {key}: {path}")
        ok &= passed
    print("PASS source markers: Contrary + starter gift overlays are locked" if ok else "FAIL source markers")
    return 0 if ok else 1
if __name__ == "__main__":
    raise SystemExit(main())
