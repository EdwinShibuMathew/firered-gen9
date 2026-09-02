#!/usr/bin/env python3
"""Audit evolution item acquisition and species-specific move prerequisites."""

from __future__ import annotations

import argparse
import csv
import re
import sys
from dataclasses import dataclass
from pathlib import Path

from m3_evolution_audit import DEFAULT_TABLE, Evolution, parse_table

ROOT = Path(__file__).resolve().parents[1]
PRET_DATA = ROOT / ".upstream/pret/data"
LEARNSETS = ROOT / ".upstream/cfru/src/Tables/level_up_learnsets.c"
ITEM_SHOP = ROOT / "data/evolution_item_shop.csv"
ITEM_HEADER = ROOT / ".upstream/dpe/include/items.h"

PARAM_ITEM_METHODS = {
    "EVO_ITEM", "EVO_ITEM_NIGHT", "EVO_ITEM_HOLD_ITEM",
    "EVO_HOLD_ITEM_DAY", "EVO_HOLD_ITEM_NIGHT", "EVO_TRADE_ITEM",
}
EXTRA_ITEM_METHODS = {"EVO_LEVEL_HOLD_ITEM", "EVO_ITEM_HOLD_ITEM"}
MOVE_METHODS = {"EVO_MOVE", "EVO_MOVE_MALE", "EVO_MOVE_FEMALE"}


@dataclass(frozen=True)
class Prerequisite:
    kind: str
    value: str
    source: str
    target: str
    method: str
    available: bool
    evidence: str


def source_texts(root: Path) -> list[tuple[Path, str]]:
    return [(path, path.read_text(encoding="utf-8", errors="ignore")) for path in root.rglob("*.inc")]


def parse_learnsets(path: Path) -> dict[str, set[str]]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    arrays = {
        name: set(re.findall(r"MOVE_[A-Z0-9_]+", body))
        for name, body in re.findall(
            r"static const struct LevelUpMove\s+(\w+)\[\]\s*=\s*\{(.*?)\n\};",
            text, re.S,
        )
    }
    return {
        species: arrays.get(array, set())
        for species, array in re.findall(r"\[(SPECIES_[A-Z0-9_]+)\]\s*=\s*(\w+)", text)
    }


def load_shop_items() -> set[str]:
    definitions = {
        name: int(value, 0)
        for name, value in re.findall(
            r"^#define\s+(ITEM_[A-Z0-9_]+)\s+(0x[0-9A-Fa-f]+|\d+)",
            ITEM_HEADER.read_text(encoding="utf-8"), re.M,
        )
    }
    with ITEM_SHOP.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        expected = definitions.get(row["item"])
        if expected is None or expected != int(row["id"], 0):
            raise ValueError(f"shop ID mismatch for {row['item']}: manifest={row['id']} header={expected}")
    return {row["item"] for row in rows}


def item_available(item: str, texts: list[tuple[Path, str]], shop_items: set[str]) -> tuple[bool, str]:
    if item == "ITEM_LINK_CABLE":
        return True, "tracked Celadon shop overlay"
    if item in shop_items:
        return True, "data/evolution_item_shop.csv"
    pattern = re.compile(rf"\b{re.escape(item)}\b")
    matches = [str(path.relative_to(ROOT)) for path, text in texts if pattern.search(text)]
    if matches:
        return True, matches[0]
    return False, "no acquisition reference in pret data"


def collect(records: list[Evolution]) -> list[Prerequisite]:
    texts = source_texts(PRET_DATA)
    learnsets = parse_learnsets(LEARNSETS)
    shop_items = load_shop_items()
    found: list[Prerequisite] = []
    for evo in records:
        items: list[str] = []
        if evo.method in PARAM_ITEM_METHODS and evo.param.startswith("ITEM_"):
            items.append(evo.param)
        if evo.method in EXTRA_ITEM_METHODS and evo.extra.startswith("ITEM_"):
            items.append(evo.extra)
        for item in items:
            available, evidence = item_available(item, texts, shop_items)
            found.append(Prerequisite("item", item, evo.source, evo.target, evo.method, available, evidence))
        if evo.method in MOVE_METHODS:
            moves = learnsets.get(evo.source, set())
            available = evo.param in moves
            evidence = "source species level-up learnset" if available else "missing from source species level-up learnset"
            found.append(Prerequisite("move", evo.param, evo.source, evo.target, evo.method, available, evidence))
    return found


def write_csv(path: Path, prerequisites: list[Prerequisite]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(("kind", "value", "source", "target", "method", "available", "evidence"))
        for row in prerequisites:
            writer.writerow((row.kind, row.value, row.source, row.target, row.method, str(row.available).lower(), row.evidence))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path)
    parser.add_argument("--require-complete", action="store_true")
    args = parser.parse_args()
    try:
        prerequisites = collect(parse_table(DEFAULT_TABLE))
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    missing = [row for row in prerequisites if not row.available]
    item_values = {row.value for row in prerequisites if row.kind == "item"}
    move_values = {row.value for row in prerequisites if row.kind == "move"}
    missing_items = {row.value for row in missing if row.kind == "item"}
    missing_moves = {row.value for row in missing if row.kind == "move"}
    print("M3 EVOLUTION PREREQUISITE AUDIT")
    print(f"Item constants required: {len(item_values)}; without acquisition evidence: {len(missing_items)}")
    print(f"Move constants required: {len(move_values)}; missing from source level-up learnset: {len(missing_moves)}")
    print(f"Affected evolution records: {len(missing)}")
    for kind, values in (("items", missing_items), ("moves", missing_moves)):
        print(f"\nMissing {kind}:")
        for value in sorted(values):
            print(f"  {value}")
    if args.csv:
        write_csv(args.csv, prerequisites)
        print(f"\nWrote report: {args.csv}")
    print("\nResult: COMPLETE" if not missing else "\nResult: PREREQUISITES REMAIN")
    return 1 if args.require_complete and missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
