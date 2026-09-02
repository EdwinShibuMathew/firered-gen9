#!/usr/bin/env python3
"""Audit DPE's actual evolution table for offline availability."""

from __future__ import annotations

import argparse
import csv
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TABLE = ROOT / ".upstream/dpe/src/Evolution_Table.c"
TRANSFORM_METHODS = {"EVO_MEGA", "EVO_GIGANTAMAX"}
HARD_BLOCKERS = {"EVO_TRADE", "EVO_TRADE_ITEM"}
NEEDS_AVAILABILITY_PROOF = {
    "EVO_MAP", "EVO_FLAG_SET", "EVO_DAMAGE_LOCATION",
    "EVO_ITEM_LOCATION",
}


@dataclass(frozen=True)
class Evolution:
    source: str
    method: str
    param: str
    target: str
    extra: str
    line: int

    @property
    def status(self) -> str:
        if self.method in HARD_BLOCKERS:
            return "offline_blocker"
        if self.method in NEEDS_AVAILABILITY_PROOF:
            return "needs_proof"
        return "offline_capable"


def strip_comments_preserving_lines(text: str) -> str:
    def replace_block(match: re.Match[str]) -> str:
        return "\n" * match.group(0).count("\n")

    text = re.sub(r"/\*.*?\*/", replace_block, text, flags=re.S)
    return re.sub(r"//[^\n]*", "", text)


def parse_table(path: Path) -> list[Evolution]:
    if not path.is_file():
        raise FileNotFoundError(f"evolution table not found: {path}")
    text = strip_comments_preserving_lines(path.read_text(encoding="utf-8"))
    token = re.compile(
        # DPE contains both standard "[index] =" and legacy GNU "[index]" designators.
        r"\[\s*(SPECIES_[A-Z0-9_]+)\s*\]\s*(?:=)?"
        r"|\{\s*(EVO_[A-Z0-9_]+)\s*,\s*([^,{}]+?)\s*,\s*"
        r"(SPECIES_[A-Z0-9_]+)\s*,\s*([^{}]+?)\s*\}", re.S,
    )
    source: str | None = None
    records: list[Evolution] = []
    for match in token.finditer(text):
        if match.group(1):
            source = match.group(1)
            continue
        if source is None:
            raise ValueError("evolution entry appeared before a species designator")
        method, param, target, extra = match.group(2, 3, 4, 5)
        records.append(Evolution(
            source, method, " ".join(param.split()), target,
            " ".join(extra.split()), text.count("\n", 0, match.start()) + 1,
        ))
    if not records:
        raise ValueError(f"no evolution records parsed from {path}")
    return records


def edge_statuses(records: list[Evolution]) -> dict[tuple[str, str], str]:
    grouped: dict[tuple[str, str], list[Evolution]] = defaultdict(list)
    for evo in records:
        if evo.method not in TRANSFORM_METHODS:
            grouped[(evo.source, evo.target)].append(evo)
    statuses = {}
    for edge, alternatives in grouped.items():
        if any(e.status == "offline_capable" for e in alternatives):
            statuses[edge] = "offline_capable"
        elif any(e.status == "needs_proof" for e in alternatives):
            statuses[edge] = "needs_proof"
        else:
            statuses[edge] = "offline_blocker"
    return statuses


def write_csv(path: Path, records: list[Evolution]) -> None:
    resolved = edge_statuses(records)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(("source", "method", "param", "target", "extra", "record_status", "edge_status", "source_line"))
        for evo in records:
            edge_status = "transformation" if evo.method in TRANSFORM_METHODS else resolved[(evo.source, evo.target)]
            writer.writerow((evo.source, evo.method, evo.param, evo.target, evo.extra, evo.status, edge_status, evo.line))


def incomplete_records(records: list[Evolution]) -> list[Evolution]:
    statuses = edge_statuses(records)
    return [e for e in records if e.method not in TRANSFORM_METHODS and statuses[(e.source, e.target)] != "offline_capable"]


def report(records: list[Evolution], table: Path) -> None:
    acquisition = [e for e in records if e.method not in TRANSFORM_METHODS]
    transformations = [e for e in records if e.method in TRANSFORM_METHODS]
    resolved = edge_statuses(records)
    blockers = [e for e in acquisition if resolved[(e.source, e.target)] == "offline_blocker"]
    proof_needed = [e for e in acquisition if resolved[(e.source, e.target)] == "needs_proof"]
    raw_trade = [e for e in acquisition if e.status == "offline_blocker"]
    raw_proof = [e for e in acquisition if e.status == "needs_proof"]
    counts = Counter(e.method for e in acquisition)
    print("M3 EVOLUTION TABLE AUDIT")
    print(f"Table: {table}")
    print(f"Parsed records: {len(records)}")
    print(f"Acquisition evolutions: {len(acquisition)}")
    print(f"Battle-only transformations excluded: {len(transformations)}")
    print(f"Source species with evolutions: {len({e.source for e in acquisition})}")
    print(f"Evolution methods used: {len(counts)}\n")
    print("Method counts:")
    for method, count in sorted(counts.items()):
        marker = "BLOCK" if method in HARD_BLOCKERS else "PROVE" if method in NEEDS_AVAILABILITY_PROOF else "OK"
        print(f"  {marker:5} {method:31} {count:4}")
    print(f"\nTrade records: {len(raw_trade)} ({len(raw_trade) - len(blockers)} have an offline alternative)")
    print(f"Unresolved trade edges: {len(blockers)}")
    for evo in blockers:
        held = f" ({evo.param})" if evo.method == "EVO_TRADE_ITEM" else ""
        print(f"  {evo.source} -> {evo.target}: {evo.method}{held} [line {evo.line}]")
    print(f"\nEnvironment/content records: {len(raw_proof)} ({len(raw_proof) - len(proof_needed)} have an offline alternative)")
    print(f"Unresolved environment/content edges needing proof: {len(proof_needed)}")
    for evo in proof_needed:
        print(f"  {evo.source} -> {evo.target}: {evo.method} ({evo.param}) [line {evo.line}]")
    result = "NOT YET OFFLINE-COMPLETE" if blockers or proof_needed else "all acquisition evolutions are offline-capable"
    print(f"\nResult: {result}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--table", type=Path, default=DEFAULT_TABLE)
    parser.add_argument("--csv", type=Path, help="write the complete mapping as CSV")
    parser.add_argument("--require-complete", action="store_true", help="fail while blockers or unproved prerequisites remain")
    args = parser.parse_args()
    try:
        records = parse_table(args.table)
        report(records, args.table)
        if args.csv:
            write_csv(args.csv, records)
            print(f"\nWrote mapping: {args.csv}")
        return 1 if args.require_complete and incomplete_records(records) else 0
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
