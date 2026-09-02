#!/usr/bin/env python3
"""Generate the ordered Evolution Guide audit ledger."""
import argparse
import csv
import io
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
src = ROOT / "data/evolution_mapping.csv"
dst = ROOT / "data/evolution_encyclopedia.csv"
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--check", action="store_true")
args = parser.parse_args()
with src.open(newline="", encoding="utf-8") as handle:
    rows = list(csv.DictReader(handle))
output = io.StringIO(newline="")
writer = csv.DictWriter(output, fieldnames=("order", "source", "method", "param", "target", "prerequisite", "status"), lineterminator="\n")
writer.writeheader()
for index, row in enumerate(rows, 1):
    writer.writerow({"order": index, "source": row["source"], "method": row["method"],
                     "param": row["param"], "target": row["target"],
                     "prerequisite": row["extra"], "status": row["edge_status"]})
content = output.getvalue()
if not dst.exists() or dst.read_text(encoding="utf-8") != content:
    if args.check:
        raise SystemExit("STALE data/evolution_encyclopedia.csv")
    dst.write_text(content, encoding="utf-8")
    print(f"Wrote {len(rows)} encyclopedia entries: {dst}")
else:
    print(f"Evolution encyclopedia current: {len(rows)} entries")
