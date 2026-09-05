#!/usr/bin/env python3
"""Verify layout-preserving one-capture static Legendary recovery changes."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATCH = ROOT / "patches/pret/0001-repeatable-legendary-encounters.patch"
FLAGS = (
    "FLAG_FOUGHT_ZAPDOS",
    "FLAG_FOUGHT_ARTICUNO",
    "FLAG_FOUGHT_MOLTRES",
    "FLAG_FOUGHT_MEWTWO",
    "FLAG_LUGIA_FLEW_AWAY",
    "FLAG_HO_OH_FLEW_AWAY",
    "FLAG_DEOXYS_FLEW_AWAY",
)


def changed_lines(text: str, prefix: str) -> list[str]:
    return [
        line[1:].strip()
        for line in text.splitlines()
        if line.startswith(prefix) and not line.startswith(prefix * 3)
    ]


text = PATCH.read_text(encoding="utf-8")
added = changed_lines(text, "+")
removed = changed_lines(text, "-")
expected_added = {f"clearflag {flag}" for flag in FLAGS}
expected_removed = {f"setflag {flag}" for flag in FLAGS}
errors = []

if set(added) != expected_added or len(added) != len(FLAGS):
    errors.append("additions are not exactly the seven same-size clearflag commands")
if set(removed) != expected_removed or len(removed) != len(FLAGS):
    errors.append("removals are not exactly the seven matching setflag commands")
if text.count("diff --git a/data/maps/") != len(FLAGS):
    errors.append("unexpected number of map files changed")

if errors:
    for error in errors:
        print(f"FAIL M4 layout contract: {error}")
    raise SystemExit(1)

print("PASS M4 one-capture recovery: 7/7 defeat flags use layout-preserving opcode swaps")
