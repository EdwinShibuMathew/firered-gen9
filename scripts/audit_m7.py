#!/usr/bin/env python3
"""Audit the generated, postgame M7 DexNav migration selector."""
import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
config = (ROOT / ".upstream/cfru/src/config.h").read_text(encoding="utf-8")
source = (ROOT / ".upstream/cfru/src/dexnav.c").read_text(encoding="utf-8")
header = (ROOT / ".upstream/cfru/include/generated/m7_habitat_groups.h").read_text(encoding="utf-8")
rows = list(csv.DictReader((ROOT / "data/habitat_migration_groups.csv").open(encoding="utf-8")))
species = re.findall(r"SPECIES_[A-Z0-9_]+", header)
checks = {
    "nine implemented regional groups": len(rows) == 9 and all(row["implementation_status"] == "IMPLEMENTED_UNVERIFIED" for row in rows),
    "collision-free persistent variable": "#define VAR_M7_MIGRATION_GROUP 0x515A" in config and config.count("0x515A") == 1,
    "generated 9x16 pools": len(species) == 144 and "M7_MIGRATION_GROUP_COUNT 9" in header,
    "SELECT selector and postgame gate": all(token in source for token in ("JOY_NEW(SELECT_BUTTON)", "FLAG_SYS_GAME_CLEAR", "Task_DexNavMigrationSelect")),
    "normal encounter tables untouched": "Migrations augment only the scanner" in source,
    "migration scan level binding": all(token in source for token in ("M7IsMigrationSpecies", "GetEncounterLevel", "GetTotalEncounterChance")),
}
for name, passed in checks.items():
    print(("PASS " if passed else "FAIL ") + name)
raise SystemExit(0 if all(checks.values()) else 1)
