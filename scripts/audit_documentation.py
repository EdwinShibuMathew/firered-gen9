#!/usr/bin/env python3
"""Reject known stale milestone claims and require the current handoff documents."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
required = {
    "README.md": ("442 canonical alternate-form IDs", "nine optional DexNav migration groups"),
    "docs/DEVELOPMENT_COMPLETION_PLAN.md": ("development-complete", "e2d4da0696ac9b0c"),
    "docs/M5_FORMS_PROGRESS.md": ("439 runtime-bound", "no known remaining M5 code task"),
    "docs/M7_HABITAT_PROGRESS.md": ("0x515A", "nine-region selector"),
    "docs/M8_RELEASE_PROGRESS.md": ("ab4cc33cc061f8e5", "round-trip verified"),
}
stale = {
    "README.md": ("dedicated field routes", "migration groups remain optional work"),
    "docs/M5_FORMS_PROGRESS.md": ("479 internal form IDs", "264 explicitly unimplemented"),
    "docs/M7_HABITAT_PROGRESS.md": ("PENDING_UI_INTEGRATION",),
}
failed = False
for name, tokens in required.items():
    text = (ROOT / name).read_text(encoding="utf-8")
    for token in tokens:
        if token not in text:
            print(f"FAIL {name}: missing {token!r}")
            failed = True
for name, tokens in stale.items():
    text = (ROOT / name).read_text(encoding="utf-8")
    for token in tokens:
        if token in text:
            print(f"FAIL {name}: stale claim {token!r}")
            failed = True
print("PASS milestone documentation reconciled" if not failed else "FAIL milestone documentation")
raise SystemExit(1 if failed else 0)
