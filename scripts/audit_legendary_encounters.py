#!/usr/bin/env python3
"""Validate real bindings and collision-free completion flags for M5 encounters."""
from __future__ import annotations
import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROWS = list(csv.DictReader((ROOT / "data/legendary_encounters.csv").open(encoding="utf-8")))
FLAGS = (ROOT / ".upstream/pret/include/constants/flags.h").read_text(encoding="utf-8")
HUB = (ROOT / ".upstream/cfru/assembly/overworld_scripts/system_scripts.s").read_text(encoding="utf-8")
RESET = (ROOT / "patches/pret/0001-repeatable-legendary-encounters.patch").read_text(encoding="utf-8")
RESET_ADDITIONS = {
    line[1:].strip()
    for line in RESET.splitlines()
    if line.startswith("+") and not line.startswith("+++")
}
DEFEAT_CLEAR_FLAGS = {
    "FLAG_FOUGHT_ARTICUNO",
    "FLAG_FOUGHT_ZAPDOS",
    "FLAG_FOUGHT_MOLTRES",
    "FLAG_FOUGHT_MEWTWO",
}

implemented = [row for row in ROWS if row["implementation_status"] != "NOT_IMPLEMENTED"]
errors: list[str] = []
seen_flags: dict[str, str] = {}
for row in implemented:
    species = row["species"].removeprefix("SPECIES_").replace("_", "").lower()
    flag = row["capture_flag"]
    if flag in seen_flags:
        errors.append(f"duplicate capture flag {flag}: {seen_flags[flag]} and {row['species']}")
    seen_flags[flag] = row["species"]
    if not (re.search(rf"#define\s+{re.escape(flag)}\s+", FLAGS)
            or re.search(rf"\.equ\s+{re.escape(flag)},\s*0x[0-9A-Fa-f]+", HUB)):
        errors.append(f"undefined capture flag {flag}")
    if row["portal_or_map"] != "SeviiResearchHub" and not (ROOT / ".upstream/pret/data/maps" / row["portal_or_map"]).is_dir():
        errors.append(f"missing map {row['portal_or_map']}")
    if row["species"] not in HUB and row["species"] not in {"SPECIES_ARTICUNO", "SPECIES_ZAPDOS", "SPECIES_MOLTRES", "SPECIES_MEWTWO", "SPECIES_LUGIA", "SPECIES_HO_OH", "SPECIES_DEOXYS"}:
        errors.append(f"missing hub binding {row['species']}")
    if f"clearflag {flag}" in RESET_ADDITIONS and flag not in DEFEAT_CLEAR_FLAGS:
        errors.append(f"capture completion is reset for {row['species']}")

if len(implemented) != len(ROWS):
    errors.append(f"{len(ROWS) - len(implemented)} contract rows remain unimplemented")

required = ("EventScript_M5LegendaryCoordinator", "EventScript_M5LegendaryDirectBattle", "special2 LASTRESULT 0xB4", "compare LASTRESULT 0x7", "warp 1, 87", "warp 2, 56")
for token in required:
    if token not in HUB:
        errors.append(f"hub runtime token missing: {token}")

print(f"M5 legendary bindings: {len(implemented)} implemented rows, {len(seen_flags)} unique completion flags")
print("Legendary flag collision report: " + ("PASS" if not errors else "FAILED"))
for error in errors:
    print("  " + error)
raise SystemExit(bool(errors))
