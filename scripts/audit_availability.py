#!/usr/bin/env python3
"""Measure National Pokédex availability from tracked acquisition sources and evolution closure."""

from __future__ import annotations

import argparse
import csv
import io
import json
import re
from pathlib import Path

from m3_evolution_audit import DEFAULT_TABLE, TRANSFORM_METHODS, parse_table

ROOT = Path(__file__).resolve().parents[1]
WILD_TABLE = ROOT / ".upstream/cfru/src/Tables/wild_encounter_tables.c"
DEX_MAP = ROOT / ".upstream/dpe/src/Species_To_Pokdex_Table.c"
POKEDEX = ROOT / ".upstream/dpe/include/pokedex.h"
DEFAULT_CSV = ROOT / "data/availability.csv"
STOCK_WILD = ROOT / ".upstream/pret/src/data/wild_encounters.json"
INGAME_TRADES = ROOT / ".upstream/pret/src/data/ingame_trades.h"
RESERVE_CSV = ROOT / "data/gen9_reserve.csv"


def species_to_dex() -> dict[str, str]:
    text = DEX_MAP.read_text(encoding="utf-8")
    return dict(re.findall(
        r"\[\s*(SPECIES_[A-Z0-9_]+)\s*-\s*1\s*\]\s*=\s*(NATIONAL_DEX_[A-Z0-9_]+)", text
    ))


def national_targets() -> set[str]:
    text = POKEDEX.read_text(encoding="utf-8")
    return {
        f"NATIONAL_DEX_{name}" for name, value in re.findall(
            r"^#define\s+NATIONAL_DEX_([A-Z0-9_]+)\s+(\d+)", text, re.M
        ) if 1 <= int(value) <= 1025
    }


def parse_wild_rows() -> list[dict[str, str]]:
    text = WILD_TABLE.read_text(encoding="utf-8")
    rows: list[dict[str, str]] = []
    for time_name, body in re.findall(
        r"const struct WildPokemon\s+gRoute1_LandMons(Morning|Day|Evening|Night)\[\]\s*=\s*\{(.*?)\n\};",
        text, re.S,
    ):
        for minimum, maximum, species in re.findall(
            r"\{\s*(\d+)\s*,\s*(\d+)\s*,\s*(SPECIES_[A-Z0-9_]+)\s*\}", body
        ):
            rows.append({
                "species": species,
                "form": "",
                "acquisition_method": "wild",
                "map": "ROUTE_1",
                "encounter_type": "land",
                "badge_requirement": "0",
                "rate": "table slot",
                "evolution_source": "",
                "quest": "",
                "notes": f"{time_name.lower()}; levels {minimum}-{maximum}",
            })
    return rows


def parse_stock_wild_rows() -> list[dict[str, str]]:
    data = json.loads(STOCK_WILD.read_text(encoding="utf-8"))
    rows: list[dict[str, str]] = []
    for group in data["wild_encounter_groups"]:
        if group.get("label") != "gWildMonHeaders":
            continue
        rates = {field["type"]: field.get("encounter_rates", []) for field in group["fields"]}
        for encounter in group["encounters"]:
            map_name = encounter["map"]
            if map_name == "MAP_ROUTE_1" or encounter.get("base_label", "").endswith("_LeafGreen"):
                continue
            for encounter_type in ("land_mons", "water_mons", "rock_smash_mons", "fishing_mons"):
                table = encounter.get(encounter_type)
                if not table:
                    continue
                for index, mon in enumerate(table["mons"]):
                    rate = rates[encounter_type][index] if index < len(rates[encounter_type]) else ""
                    rows.append({
                        "species": mon["species"], "form": "", "acquisition_method": "wild",
                        "map": map_name.removeprefix("MAP_"),
                        "encounter_type": encounter_type.removesuffix("_mons"),
                        "badge_requirement": "varies", "rate": str(rate), "evolution_source": "",
                        "quest": "", "notes": f"stock FireRed; levels {mon['min_level']}-{mon['max_level']}",
                    })
    return rows


def parse_scripted_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    pattern = re.compile(r"\b(givemon|giveegg|setwildbattle)\s+(SPECIES_[A-Z0-9_]+)")
    for path in (ROOT / ".upstream/pret/data/maps").rglob("scripts.inc"):
        text = fire_red_preprocess(path.read_text(encoding="utf-8", errors="ignore"))
        for command, species in pattern.findall(text):
            method = "static" if command == "setwildbattle" else "egg" if command == "giveegg" else "gift"
            rows.append({
                "species": species, "form": "", "acquisition_method": method,
                "map": path.parent.name, "encounter_type": "scripted",
                "badge_requirement": "varies", "rate": "guaranteed", "evolution_source": "",
                "quest": "stock FireRed script", "notes": command,
            })
        variable_gifts = set(re.findall(r"\bgivemon\s+([A-Z][A-Z0-9_]*)", text))
        variable_gifts -= {species for _, species in pattern.findall(text)}
        for variable in variable_gifts:
            for species in sorted(set(re.findall(
                rf"\bsetvar\s+{re.escape(variable)}\s*,\s*(SPECIES_[A-Z0-9_]+)", text
            ))):
                rows.append({
                    "species": species, "form": "", "acquisition_method": "gift",
                    "map": path.parent.name, "encounter_type": "scripted",
                    "badge_requirement": "varies", "rate": "guaranteed", "evolution_source": "",
                    "quest": "stock FireRed script", "notes": f"givemon via {variable}",
                })
    return rows


def parse_ingame_trade_rows() -> list[dict[str, str]]:
    text = c_fire_red_preprocess(INGAME_TRADES.read_text(encoding="utf-8"))
    trades = dict(re.findall(
        r"\[(INGAME_TRADE_[A-Z0-9_]+)\]\s*=\s*\{(.*?)\n\s*\},?", text, re.S
    ))
    species_by_trade = {
        trade: match.group(1)
        for trade, body in trades.items()
        if (match := re.search(r"\.species\s*=\s*(SPECIES_[A-Z0-9_]+)", body))
    }
    rows: list[dict[str, str]] = []
    for path in (ROOT / ".upstream/pret/data/maps").glob("*/scripts.inc"):
        script = fire_red_preprocess(path.read_text(encoding="utf-8", errors="ignore"))
        for trade in sorted(set(re.findall(
            r"\bsetvar\s+VAR_0x8008\s*,\s*(INGAME_TRADE_[A-Z0-9_]+)", script
        )), reverse=True):
            if trade in species_by_trade:
                rows.append({
                    "species": species_by_trade[trade], "form": "",
                    "acquisition_method": "in-game trade", "map": path.parent.name,
                    "encounter_type": "scripted", "badge_requirement": "varies",
                    "rate": "guaranteed", "evolution_source": "",
                    "quest": "stock FireRed in-game trade", "notes": trade,
                })
    return rows


def fire_red_preprocess(text: str) -> str:
    """Keep the FireRed side of simple assembly conditionals used by map scripts."""
    active = True
    stack: list[tuple[bool, bool]] = []
    kept: list[str] = []
    for line in text.splitlines():
        directive = re.match(r"\s*\.(ifdef|ifndef)\s+(FIRERED|LEAFGREEN)\s*$", line)
        if directive:
            kind, symbol = directive.groups()
            condition = symbol == "FIRERED"
            if kind == "ifndef":
                condition = not condition
            stack.append((active, condition))
            active = active and condition
        elif re.match(r"\s*\.else\s*$", line) and stack:
            parent, condition = stack[-1]
            stack[-1] = (parent, not condition)
            active = parent and not condition
        elif re.match(r"\s*\.endif\s*$", line) and stack:
            parent, _ = stack.pop()
            active = parent
        elif active:
            kept.append(line)
    return "\n".join(kept)


def c_fire_red_preprocess(text: str) -> str:
    """Resolve the FireRed/LeafGreen C preprocessor branches in acquisition data."""
    text = re.sub(r"#if\s+defined\((FIRERED|LEAFGREEN)\)", r".ifdef \1", text)
    text = re.sub(r"#elif\s+defined\((FIRERED|LEAFGREEN)\)", ".else", text)
    text = re.sub(r"#endif", ".endif", text)
    return fire_red_preprocess(text)


def render_rows(rows: list[dict[str, str]]) -> bytes:
    fields = ("species", "form", "acquisition_method", "map", "encounter_type",
              "badge_requirement", "rate", "evolution_source", "quest", "notes")
    handle = io.StringIO(newline="")
    writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(sorted(rows, key=lambda row: tuple(row[field] for field in fields)))
    return handle.getvalue().encode("utf-8")


def parse_reserve_rows() -> list[dict[str, str]]:
    if not RESERVE_CSV.exists():
        return []
    with RESERVE_CSV.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def evolution_closure(seed: set[str]) -> set[str]:
    available = set(seed)
    edges = [e for e in parse_table(DEFAULT_TABLE) if e.method not in TRANSFORM_METHODS]
    changed = True
    while changed:
        changed = False
        for evo in edges:
            if evo.source in available and evo.target not in available:
                available.add(evo.target)
                changed = True
    return available


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV)
    parser.add_argument("--require-complete", action="store_true")
    parser.add_argument("--check", action="store_true", help="compare the ledger without writing it")
    args = parser.parse_args()
    rows = (parse_wild_rows() + parse_stock_wild_rows() + parse_scripted_rows()
            + parse_ingame_trade_rows() + parse_reserve_rows())
    rendered = render_rows(rows)
    ledger_ok = True
    if args.check:
        ledger_ok = args.csv.is_file() and args.csv.read_bytes() == rendered
        print(f"{'PASS' if ledger_ok else 'STALE'} availability ledger: {args.csv}")
    else:
        args.csv.parent.mkdir(parents=True, exist_ok=True)
        args.csv.write_bytes(rendered)
        print(f"Wrote ledger: {args.csv}")
    seeds = {row["species"] for row in rows}
    closure = evolution_closure(seeds)
    dex_map = species_to_dex()
    covered = {dex_map[s] for s in closure if s in dex_map}
    targets = national_targets()
    missing = sorted(targets - covered)
    print("M4 NATIONAL AVAILABILITY AUDIT")
    print(f"Direct acquisition records: {len(rows)}")
    print(f"Unique direct species/forms: {len(seeds)}")
    print(f"Species/forms after evolution closure: {len(closure)}")
    print(f"National Pokédex coverage: {len(covered & targets)} / {len(targets)}")
    print(f"Missing National Pokédex species: {len(missing)}")
    if missing:
        print("First missing entries: " + ", ".join(name.removeprefix("NATIONAL_DEX_") for name in missing[:20]))
    return 1 if not ledger_ok or (args.require_complete and missing) else 0


if __name__ == "__main__":
    raise SystemExit(main())
