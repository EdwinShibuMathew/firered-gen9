#!/usr/bin/env python3
"""Verify one-capture static Legendary recovery contracts."""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
PATCH = ROOT / "patches/pret/0001-repeatable-legendary-encounters.patch"
EXPECTED = ("FLAG_FOUGHT_ZAPDOS", "FLAG_FOUGHT_ARTICUNO", "FLAG_FOUGHT_MOLTRES", "FLAG_FOUGHT_MEWTWO", "FLAG_FOUGHT_LUGIA", "FLAG_FOUGHT_HO_OH", "FLAG_FOUGHT_DEOXYS")
text = PATCH.read_text(encoding="utf-8")
cleared_completion = [flag for flag in EXPECTED if f"clearflag {flag}" in text]
missing_capture_guards = [flag for flag in EXPECTED if flag not in text]
temporary_resets = ("FLAG_LUGIA_FLEW_AWAY", "FLAG_HO_OH_FLEW_AWAY", "FLAG_DEOXYS_FLEW_AWAY")
missing_temporary = [flag for flag in temporary_resets if f"clearflag {flag}" not in text]
errors = bool(cleared_completion or missing_capture_guards or missing_temporary)
print(f"M4 one-capture recovery: {len(EXPECTED) - len(missing_capture_guards)}/{len(EXPECTED)} capture guards; "
      f"{len(temporary_resets) - len(missing_temporary)}/{len(temporary_resets)} temporary locks reset")
if cleared_completion:
    print("Completion flags incorrectly cleared: " + ", ".join(cleared_completion))
if missing_capture_guards:
    print("Missing capture guards: " + ", ".join(missing_capture_guards))
if missing_temporary:
    print("Missing temporary resets: " + ", ".join(missing_temporary))
raise SystemExit(1 if errors else 0)
