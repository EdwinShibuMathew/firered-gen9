#!/usr/bin/env python3
"""M8 release hygiene gate; manual gameplay rows remain explicitly pending."""
from __future__ import annotations
import json
import subprocess
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def main() -> int:
    lock = json.loads((ROOT / "build-lock.json").read_text())
    required = ["README.md", "CREDITS.md", "docs/GEN9_ARCHITECTURE.md", "docs/TEST_MATRIX.md", "docs/GEN9_COMPLETION_ROADMAP.md", "docs/EVOLUTION_GUIDE_UI.md", "data/availability.csv", "data/forms.csv", "data/form_routes.csv", "data/legendary_encounters.csv", "data/asset_provenance.csv", "data/evolution_encyclopedia.csv"]
    tracked = subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True).splitlines()
    forbidden = {".gba", ".sav", ".bios", ".ss0", ".state", ".bps", ".ups"}
    checks = {"build_lock_json": bool(lock.get("upstreams")) and bool(lock.get("artifacts")), "required_docs_and_ledgers": all((ROOT / p).exists() for p in required), "release_rom_policy": not any(Path(p).suffix.lower() in forbidden for p in tracked), "ignored_bps_test_candidate": (ROOT / "build/private/firered-gen9-m8-test-candidate.bps").is_file()}
    for name, ok in checks.items(): print(f"{'PASS' if ok else 'FAIL'} {name}")
    print("PENDING owner-led manual test matrix and public asset review")
    return 0 if all(checks.values()) else 1
if __name__ == "__main__": raise SystemExit(main())
