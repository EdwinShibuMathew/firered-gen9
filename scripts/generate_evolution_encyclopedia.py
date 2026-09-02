#!/usr/bin/env python3
"""Generate the ordered evolution encyclopedia source ledger."""
from pathlib import Path
import csv
ROOT = Path(__file__).resolve().parents[1]
src = ROOT / "data/evolution_mapping.csv"
dst = ROOT / "data/evolution_encyclopedia.csv"
with src.open(newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
with dst.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=("order", "source", "method", "param", "target", "prerequisite", "status"))
    w.writeheader()
    for i, row in enumerate(rows, 1):
        w.writerow({"order": i, "source": row["source"], "method": row["method"], "param": row["param"], "target": row["target"], "prerequisite": row["extra"], "status": row["edge_status"]})
print(f"Wrote {len(rows)} encyclopedia entries: {dst}")
