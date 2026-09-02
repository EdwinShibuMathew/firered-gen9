#!/usr/bin/env python3
"""Audit optional M7 prerequisites and report implementation gaps."""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def main() -> int:
    config = (ROOT / ".upstream/cfru/src/config.h").read_text()
    source = (ROOT / ".upstream/cfru/src/start_menu.c").read_text()
    groups = ROOT / "data/habitat_migration_groups.csv"
    checks = {"dexnav_config": "FLAG_SYS_DEXNAV" in config, "dexnav_start_menu": "STARTMENU_DEXNAV" in source, "deterministic_m4_prerequisite": (ROOT / "data/availability.csv").exists(), "migration_group_contract": groups.exists() and sum(1 for _ in groups.open()) == 10}
    for name, ok in checks.items(): print(f"{'PASS' if ok else 'PENDING'} {name}")
    print("PENDING national habitat migration groups and advanced-mechanics regression QA")
    return 0
if __name__ == "__main__": raise SystemExit(main())
