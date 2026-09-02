#!/usr/bin/env python3
"""Audit the verifiable M5 content contracts without claiming gameplay QA."""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORMS = ROOT / "data/forms.csv"
AVAIL = ROOT / "data/availability.csv"
PARTY = ROOT / ".upstream/cfru/src/party_menu.c"
ITEMS = ROOT / ".upstream/cfru/src/Tables/item_tables.c"
ROUTES = ROOT / "data/form_routes.csv"
LEGENDARIES = ROOT / "data/legendary_encounters.csv"
DEX_GUIDE = ROOT / "patches/cfru/0011-pokedex-evolution-guide.patch"
FORM_LAB = ROOT / "patches/cfru/0009-cinnabar-form-research-lab.patch"
LEGENDARY_HUB = ROOT / "patches/cfru/0010-legendary-research-hub.patch"

HANDLER_TOKENS = ("FieldUseFunc_FormChangeItem", "DoItemFormChange")
ITEM_TOKENS = ("ITEM_GRACIDEA", "ITEM_DNA_SPLICERS", "ITEM_REVEAL_GLASS", "ITEM_PRISON_BOTTLE", "ITEM_N_SOLARIZER", "ITEM_REINS_OF_UNITY", "ITEM_RED_NECTAR", "ITEM_YELLOW_NECTAR", "ITEM_PINK_NECTAR", "ITEM_PURPLE_NECTAR")

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--require-audited", action="store_true")
    args = ap.parse_args()
    form_rows = list(csv.DictReader(FORMS.open(encoding="utf-8")))
    availability_rows = list(csv.DictReader(AVAIL.open(encoding="utf-8")))
    party = PARTY.read_text(encoding="utf-8")
    items = ITEMS.read_text(encoding="utf-8")
    checks = {
        "form_registry": bool(form_rows) and all(not row["missing"] for row in form_rows),
        "permanent_form_api": all(token in party for token in HANDLER_TOKENS),
        "permanent_form_items": all(token in items for token in ITEM_TOKENS),
        "availability_quest_schema": all("quest" in row for row in availability_rows),
        "form_route_contract": ROUTES.exists() and all(row.get("route_category") for row in csv.DictReader(ROUTES.open(encoding="utf-8"))),
        "legendary_contract": LEGENDARIES.exists() and all(row.get("implementation_status") for row in csv.DictReader(LEGENDARIES.open(encoding="utf-8"))),
        "evolution_guide_runtime": DEX_GUIDE.exists() and all(token in DEX_GUIDE.read_text(encoding="utf-8") for token in ("M5DexGuideInputHook", "gEvolutionTable", "M5DexGuideHandleInput")),
        "form_lab_runtime": FORM_LAB.exists() and all(token in FORM_LAB.read_text(encoding="utf-8") for token in ("EventScript_M5FormResearcher", "TryChangeMonForm", "npc 12 3 1")),
        "legendary_hub_runtime": LEGENDARY_HUB.exists() and all(token in LEGENDARY_HUB.read_text(encoding="utf-8") for token in ("EventScript_M5LegendaryCoordinator", "npc 31 3 2", "FLAG_M5_FOUGHT_DEOXYS")),
    }
    print("M5 CONTENT AUDIT")
    for name, ok in checks.items():
        print(f"  {'PASS' if ok else 'PENDING'} {name}")
    print(f"  form families: {len(form_rows)}")
    print(f"  quest-tagged acquisition records: {sum(bool(row.get('quest')) for row in availability_rows)}")
    encyclopedia = ROOT / "data/evolution_encyclopedia.csv"
    print(f"  evolution encyclopedia ledger: {'PASS' if encyclopedia.exists() else 'PENDING'}")
    print(f"  evolution encyclopedia UI: {'PASS' if checks['evolution_guide_runtime'] else 'PENDING'}")
    return 0 if (not args.require_audited or all(checks.values())) else 1

if __name__ == "__main__":
    raise SystemExit(main())
