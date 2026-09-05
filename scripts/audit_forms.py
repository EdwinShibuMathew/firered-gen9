#!/usr/bin/env python3
"""Audit meaningful Gen 9 form families and permanent item-change handlers."""

from __future__ import annotations

import argparse
import csv
import io
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPECIES = ROOT / ".upstream/cfru/include/constants/species.h"
PARTY_MENU = ROOT / ".upstream/cfru/src/party_menu.c"
DEFAULT_CSV = ROOT / "data/forms.csv"

FAMILIES = {
    "Paldean Tauros": ("SPECIES_TAUROS_P", "SPECIES_TAUROS_BLAZE_P", "SPECIES_TAUROS_AQUA_P"),
    "Basculin": ("SPECIES_BASCULIN_RED", "SPECIES_BASCULIN_BLUE", "SPECIES_BASCULIN_H"),
    "Oricorio": ("SPECIES_ORICORIO", "SPECIES_ORICORIO_Y", "SPECIES_ORICORIO_P", "SPECIES_ORICORIO_S"),
    "Deerling/Sawsbuck": ("SPECIES_DEERLING", "SPECIES_DEERLING_AUTUMN", "SPECIES_DEERLING_SUMMER", "SPECIES_DEERLING_WINTER"),
    "Shellos/Gastrodon": ("SPECIES_SHELLOS", "SPECIES_SHELLOS_EAST", "SPECIES_GASTRODON", "SPECIES_GASTRODON_EAST"),
    "Flabebe": ("SPECIES_FLABEBE", "SPECIES_FLABEBE_BLUE", "SPECIES_FLABEBE_ORANGE", "SPECIES_FLABEBE_WHITE", "SPECIES_FLABEBE_YELLOW"),
    "Pumpkaboo/Gourgeist": ("SPECIES_PUMPKABOO", "SPECIES_GOURGEIST", "SPECIES_GOURGEIST_L", "SPECIES_GOURGEIST_M", "SPECIES_GOURGEIST_XL"),
    "Tatsugiri": ("SPECIES_TATSUGIRI", "SPECIES_TATSUGIRI_RED", "SPECIES_TATSUGIRI_YELLOW"),
    "Maushold": ("SPECIES_MAUSHOLD", "SPECIES_MAUSHOLD_FOUR"),
    "Dudunsparce": ("SPECIES_DUDUNSPARCE", "SPECIES_DUDUNSPARCE_THREE"),
    "Rotom": ("SPECIES_ROTOM", "SPECIES_ROTOM_HEAT", "SPECIES_ROTOM_WASH", "SPECIES_ROTOM_FROST", "SPECIES_ROTOM_FAN", "SPECIES_ROTOM_MOW"),
    "Deoxys": ("SPECIES_DEOXYS", "SPECIES_DEOXYS_ATTACK", "SPECIES_DEOXYS_DEFENSE", "SPECIES_DEOXYS_SPEED"),
    "Shaymin": ("SPECIES_SHAYMIN", "SPECIES_SHAYMIN_SKY"),
    "Hoopa": ("SPECIES_HOOPA", "SPECIES_HOOPA_UNBOUND"),
    "Furfrou": ("SPECIES_FURFROU", "SPECIES_FURFROU_HEART", "SPECIES_FURFROU_DIAMOND", "SPECIES_FURFROU_STAR"),
    "Arceus": ("SPECIES_ARCEUS", "SPECIES_ARCEUS_FIRE", "SPECIES_ARCEUS_WATER", "SPECIES_ARCEUS_GRASS"),
    "Silvally": ("SPECIES_SILVALLY", "SPECIES_SILVALLY_FIRE", "SPECIES_SILVALLY_WATER", "SPECIES_SILVALLY_FAIRY"),
    "Genesect": ("SPECIES_GENESECT", "SPECIES_GENESECT_BURN", "SPECIES_GENESECT_CHILL", "SPECIES_GENESECT_DOUSE", "SPECIES_GENESECT_SHOCK"),
    "Ogerpon": ("SPECIES_OGERPON", "SPECIES_OGERPON_WELLSPRING_MASK", "SPECIES_OGERPON_HEARTHFLAME_MASK", "SPECIES_OGERPON_CORNERSTONE_MASK"),
    "Terapagos": ("SPECIES_TERAPAGOS", "SPECIES_TERAPAGOS_STELLAR"),
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV)
    parser.add_argument("--require-complete", action="store_true")
    parser.add_argument("--check", action="store_true", help="compare the ledger without writing it")
    args = parser.parse_args()
    species_text = SPECIES.read_text(encoding="utf-8")
    known = set(re.findall(r"^#define\s+(SPECIES_[A-Z0-9_]+)\s+0x[0-9A-Fa-f]+", species_text, re.M))
    handler_text = PARTY_MENU.read_text(encoding="utf-8")
    rows = []
    missing = []
    for family, members in FAMILIES.items():
        present = [member for member in members if member in known]
        absent = [member for member in members if member not in known]
        handler = "item/form handler present" if any(member in handler_text for member in present) else "requires handler review"
        rows.append({"family": family, "members": ";".join(members), "present": ";".join(present), "missing": ";".join(absent), "handler": handler})
        missing.extend((family, member) for member in absent)
    handle = io.StringIO(newline="")
    writer = csv.DictWriter(handle, fieldnames=("family", "members", "present", "missing", "handler"))
    writer.writeheader()
    writer.writerows(rows)
    rendered = handle.getvalue().encode("utf-8")
    ledger_ok = True
    if args.check:
        ledger_ok = args.csv.is_file() and args.csv.read_bytes() == rendered
        print(f"{'PASS' if ledger_ok else 'STALE'} forms ledger: {args.csv}")
    else:
        args.csv.parent.mkdir(parents=True, exist_ok=True)
        args.csv.write_bytes(rendered)
        print(f"Wrote ledger: {args.csv}")
    print(f"M5 FORM AUDIT: {len(FAMILIES) - len({f for f, _ in missing})}/{len(FAMILIES)} families have all requested constants")
    print(f"Form families audited: {len(FAMILIES)}; missing constants: {len(missing)}")
    if missing:
        print("Missing: " + ", ".join(f"{family}:{member}" for family, member in missing))
    return 1 if not ledger_ok or (args.require_complete and missing) else 0


if __name__ == "__main__":
    raise SystemExit(main())
