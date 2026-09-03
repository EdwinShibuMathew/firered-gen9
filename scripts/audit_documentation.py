#!/usr/bin/env python3
"""Validate the canonical documentation set and reject stale milestone claims."""
from pathlib import Path
import hashlib
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
required = {
    "README.md": ("442 canonical alternate-form IDs", "nine optional DexNav migration groups"),
    "docs/STATUS.md": ("development-complete", "e2d4da0696ac9b0c"),
    "docs/FEATURES.md": ("439 resolve", "nine-region selector"),
    "docs/ARCHITECTURE.md": ("0x1600000", "0x1000000"),
    "docs/TESTING.md": ("Boundary matrix", "manual"),
    "docs/HISTORY.md": ("Retired document map", "M2 species audit"),
}
stale = {
    "README.md": ("dedicated field routes", "migration groups remain optional work"),
}
retired = {
    "docs/DEVELOPMENT_COMPLETION_PLAN.md", "docs/EVOLUTION_GUIDE_UI.md",
    "docs/GEN9_ARCHITECTURE.md", "docs/GEN9_COMPLETION_ROADMAP.md",
    "docs/M1_COMPLETION_REPORT.md", "docs/M1_COMPLETION_STATUS.md",
    "docs/M1_TEST_RESULTS.md", "docs/M2_SPECIES_AUDIT_PLAN.md",
    "docs/M2_SPECIES_AUDIT_PROGRESS.md", "docs/M2_SPECIES_AUDIT_REPORT.md",
    "docs/M3_EVOLUTION_PLAN.md", "docs/M3_EVOLUTION_PROGRESS.md",
    "docs/M4_AVAILABILITY_PROGRESS.md", "docs/M5_DESIGN_SPEC.md",
    "docs/M5_FORMS_PROGRESS.md", "docs/M5_MANUAL_TEST_CHECKLIST.md",
    "docs/M6_STARTER_PROGRESS.md", "docs/M7_HABITAT_PROGRESS.md",
    "docs/M8_RELEASE_PROGRESS.md", "docs/TEST_MATRIX.md", "docs/UPSTREAM_PINS.md",
    "M1_COMPLETION_SUMMARY.md",
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
for name in retired:
    if (ROOT / name).exists():
        print(f"FAIL retired document still present: {name}")
        failed = True
history = (ROOT / "docs/HISTORY.md").read_text(encoding="utf-8")
for name in retired:
    commits = subprocess.check_output(["git", "rev-list", "--all", "--", name], cwd=ROOT, text=True).splitlines()
    original = None
    for commit in commits:
        candidate = subprocess.run(
            ["git", "show", f"{commit}:{name}"], cwd=ROOT,
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
        )
        if candidate.returncode == 0:
            original = candidate.stdout
            break
    if original is None:
        print(f"FAIL retired document missing from pre-cleanup revision: {name}")
        failed = True
        continue
    expected = hashlib.sha256(original).hexdigest()
    row = re.search(rf"\| `{re.escape(name)}` \| `?([0-9a-f]{{64}})`? \|", history)
    if not row or row.group(1) != expected:
        print(f"FAIL archive manifest hash mismatch: {name}")
        failed = True
print("PASS milestone documentation reconciled" if not failed else "FAIL milestone documentation")
raise SystemExit(1 if failed else 0)
