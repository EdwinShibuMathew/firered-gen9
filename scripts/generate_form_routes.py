#!/usr/bin/env python3
"""Generate the canonical form-route contract and Form Lab runtime table.

An alternate form is defined by DPE's species-to-National-Dex mapping, not by
underscores in a C identifier. This avoids treating NIDORAN_F or HO_OH as forms.
"""
from __future__ import annotations

import argparse
import csv
import io
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPECIES_H = ROOT / ".upstream/cfru/include/constants/species.h"
INSERT_SPECIES_H = ROOT / ".upstream/dpe/include/species.h"
DEX_MAP = ROOT / ".upstream/dpe/src/Species_To_Pokdex_Table.c"
CSV_PATH = ROOT / "data/form_routes.csv"
HEADER_PATH = ROOT / ".upstream/cfru/include/generated/m5_form_routes.h"

FIELDS = (
    "internal_id", "base_species", "target_form", "route_category",
    "trigger_item", "trigger_location", "item_consumed", "reversible",
    "battle_only", "acquisition_method", "implementation_status",
    "handler_type", "handler_symbol", "script_symbol", "binding_source", "notes",
)
SAFE_FUSIONS = {
    "SPECIES_KYUREM_BLACK", "SPECIES_KYUREM_WHITE",
    "SPECIES_NECROZMA_DUSK_MANE", "SPECIES_NECROZMA_DAWN_WINGS",
    "SPECIES_CALYREX_ICE_RIDER", "SPECIES_CALYREX_SHADOW_RIDER",
}
UNSUPPORTED = {"SPECIES_SHADOW_WARRIOR", "SPECIES_ZYGARDE_CELL", "SPECIES_ZYGARDE_CORE"}
HELD_PREFIXES = ("SPECIES_ARCEUS_", "SPECIES_SILVALLY_", "SPECIES_GENESECT_")
HELD_EXACT = {
    "SPECIES_GIRATINA_ORIGIN", "SPECIES_ZACIAN_CROWNED", "SPECIES_ZAMAZENTA_CROWNED",
    "SPECIES_OGERPON_WELLSPRING_MASK", "SPECIES_OGERPON_HEARTHFLAME_MASK",
    "SPECIES_OGERPON_CORNERSTONE_MASK",
}
KEY_EXACT = {
    "SPECIES_SHAYMIN_SKY", "SPECIES_HOOPA_UNBOUND", "SPECIES_ZYGARDE_10",
    "SPECIES_KELDEO_RESOLUTE", "SPECIES_DIALGA_ORIGIN", "SPECIES_PALKIA_ORIGIN",
}
KEY_PREFIXES = (
    "SPECIES_TORNADUS_", "SPECIES_THUNDURUS_", "SPECIES_LANDORUS_", "SPECIES_ENAMORUS_",
)
LAB_FAMILIES = {"ROTOM", "DEOXYS", "FURFROU", "MAGEARNA", "ZARUDE"}
BATTLE_EXACT = {
    "SPECIES_DARMANITANZEN", "SPECIES_DARMANITAN_G_ZEN", "SPECIES_MELOETTA_PIROUETTE",
    "SPECIES_CHERRIM_SUN", "SPECIES_AEGISLASH_BLADE", "SPECIES_ASHGRENINJA",
    "SPECIES_MINIOR_SHIELD", "SPECIES_WISHIWASHI_S", "SPECIES_MIMIKYU_BUSTED",
    "SPECIES_NECROZMA_ULTRA", "SPECIES_XERNEAS_NATURAL", "SPECIES_CRAMORANT_GULPING",
    "SPECIES_CRAMORANT_GORGING", "SPECIES_EISCUE_NOICE", "SPECIES_MORPEKO_HANGRY",
    "SPECIES_ETERNATUS_ETERNAMAX", "SPECIES_PALAFIN_HERO", "SPECIES_OGERPON_TERASTAL",
    "SPECIES_OGERPON_WELLSPRING_TERASTAL", "SPECIES_OGERPON_HEARTHFLAME_TERASTAL",
    "SPECIES_OGERPON_CORNERSTONE_TERASTAL", "SPECIES_TERAPAGOS_TERASTAL",
    "SPECIES_TERAPAGOS_STELLAR",
    "SPECIES_OGERPON_GREEN", "SPECIES_OGERPON_BLUE", "SPECIES_OGERPON_RED", "SPECIES_OGERPON_GREY",
}
REGIONAL_SUFFIXES = ("_A", "_G", "_H", "_P", "_BLAZE_P", "_AQUA_P")


def parse_inventory():
    constants = {
        name: int(value, 0)
        for name, value in re.findall(
            r"^#define\s+(SPECIES_[A-Z0-9_]+)\s+(0x[0-9A-Fa-f]+|\d+)",
            SPECIES_H.read_text(encoding="utf-8"), re.M,
        )
    }
    insert_constants = {
        name: int(value, 0)
        for name, value in re.findall(
            r"^#define\s+(SPECIES_[A-Z0-9_]+)\s+(0x[0-9A-Fa-f]+|\d+)",
            INSERT_SPECIES_H.read_text(encoding="utf-8"), re.M,
        )
    }
    cfru_by_id = {value: name for name, value in constants.items()}
    mapped = re.findall(
        r"\[(SPECIES_[A-Z0-9_]+)\s*-\s*1\]\s*=\s*(NATIONAL_DEX_[A-Z0-9_]+)",
        DEX_MAP.read_text(encoding="utf-8"),
    )
    translated = [(cfru_by_id[insert_constants[species]], species, national)
                  for species, national in mapped if insert_constants[species] in cfru_by_id]
    bases = {}
    for compiled, inserted, national in translated:
        if inserted.removeprefix("SPECIES_") == national.removeprefix("NATIONAL_DEX_"):
            bases[national] = compiled
    forms = [(compiled, national) for compiled, inserted, national in translated
             if inserted != "SPECIES_EGG"
             and inserted.removeprefix("SPECIES_") != national.removeprefix("NATIONAL_DEX_")]
    # A few DPE families intentionally have no unsuffixed internal constant
    # (Basculin, Minior and Urshifu). Their first mapped form is the storage base.
    for compiled, _inserted, national in translated:
        bases.setdefault(national, compiled)
    return forms, constants, bases


def route_category(species, national):
    family = national.removeprefix("NATIONAL_DEX_")
    if species in UNSUPPORTED:
        return "UNSUPPORTED_PLACEHOLDER"
    if species in SAFE_FUSIONS:
        return "FUSION_FORM"
    if "_MEGA" in species or "_GIGA" in species or "_PRIMAL" in species or species in BATTLE_EXACT:
        return "BATTLE_ONLY"
    if species in HELD_EXACT or species.startswith(HELD_PREFIXES):
        return "HELD_ITEM_DERIVED"
    if species in KEY_EXACT or species.startswith(KEY_PREFIXES):
        return "KEY_ITEM_TOGGLE"
    if family in LAB_FAMILIES:
        return "FORM_LAB_SELECTABLE"
    if species.endswith(REGIONAL_SUFFIXES):
        return "REGIONAL_DISTINCT"
    return "ENCOUNTER_OR_EVOLUTION_LOCKED"


def binding(category):
    return {
        "BATTLE_ONLY": ("battle_engine", "IMPLEMENTED_UNVERIFIED", "BATTLE_ENGINE", "DoFormChange", "", "CFRU battle form tables"),
        "FUSION_FORM": ("existing_cfru_fusion_storage", "IMPLEMENTED_UNVERIFIED", "C_HANDLER", "ItemUseCB_FormChangeItem", "", "CFRU fusion item switch"),
        "HELD_ITEM_DERIVED": ("existing_cfru_held_item", "IMPLEMENTED_UNVERIFIED", "C_HANDLER", "HoldItemFormChange", "", "CFRU held-item form table"),
        "KEY_ITEM_TOGGLE": ("existing_cfru_key_item", "IMPLEMENTED_UNVERIFIED", "C_HANDLER", "ItemUseCB_FormChangeItem", "", "CFRU reusable form item switch"),
        "FORM_LAB_SELECTABLE": ("cinnabar_form_lab", "IMPLEMENTED_UNVERIFIED", "GENERATED_C_TABLE", "M5FormLabApplyPreparedForm", "EventScript_M5FormResearcher", "generated m5_form_routes.h"),
        "REGIONAL_DISTINCT": ("research_preserve_encounter", "NOT_IMPLEMENTED", "PENDING", "", "", "pending generated encounter binding"),
        "ENCOUNTER_OR_EVOLUTION_LOCKED": ("research_preserve_encounter", "NOT_IMPLEMENTED", "PENDING", "", "", "pending generated encounter/evolution binding"),
        "UNSUPPORTED_PLACEHOLDER": ("excluded", "NOT_IMPLEMENTED", "INTENTIONAL_EXCLUSION", "", "", "unsafe/non-obtainable internal slot"),
    }[category]


def build_rows():
    forms, constants, bases = parse_inventory()
    rows = []
    for species, national in forms:
        category = route_category(species, national)
        acquisition, status, handler_type, handler, script, source = binding(category)
        rows.append({
            "internal_id": str(constants[species]), "base_species": bases[national],
            "target_form": species, "route_category": category, "trigger_item": "",
            "trigger_location": "", "item_consumed": "false",
            "reversible": str(category in {"HELD_ITEM_DERIVED", "KEY_ITEM_TOGGLE", "FORM_LAB_SELECTABLE", "FUSION_FORM"}).lower(),
            "battle_only": str(category == "BATTLE_ONLY").lower(), "acquisition_method": acquisition,
            "implementation_status": status, "handler_type": handler_type,
            "handler_symbol": handler, "script_symbol": script, "binding_source": source,
            "notes": "Canonical alternate form from Species_To_Pokdex_Table.c",
        })
    return rows


def render_csv(rows):
    output = io.StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=FIELDS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue()


def render_header(rows):
    families = {}
    for row in rows:
        if row["route_category"] == "FORM_LAB_SELECTABLE":
            families.setdefault(row["base_species"], [row["base_species"]]).append(row["target_form"])
    lines = [
        "/* Generated by scripts/generate_form_routes.py. Do not edit. */",
        "#ifndef GUARD_GENERATED_M5_FORM_ROUTES_H", "#define GUARD_GENERATED_M5_FORM_ROUTES_H", "",
    ]
    for i, forms in enumerate(families.values()):
        lines.append(f"static const u16 sM5GeneratedFormFamily{i}[] = {{{', '.join(forms)}}};")
    lines.extend(["", "static const struct M5FormLabFamily sM5FormLabFamilies[] = {"])
    for i in range(len(families)):
        lines.append(f"    {{sM5GeneratedFormFamily{i}, ARRAY_COUNT(sM5GeneratedFormFamily{i})}},")
    lines.extend(["};", "", "#define M5_FORM_LAB_MAX_OPTIONS 20", "#endif", ""])
    return "\n".join(lines)


def update(path, content, check):
    old = path.read_text(encoding="utf-8") if path.exists() else None
    if old == content:
        return True
    if check:
        print(f"STALE {path.relative_to(ROOT)}")
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"Wrote {path.relative_to(ROOT)}")
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    rows = build_rows()
    ok = update(CSV_PATH, render_csv(rows), args.check)
    ok &= update(HEADER_PATH, render_header(rows), args.check)
    print(f"Canonical form inventory: {len(rows)} alternate forms")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
