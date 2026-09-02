# M7 Habitat Scanner — Progress

**Status:** `[~]` compiled and automated-tested; manual QA remains

- CFRU's DexNav/Habitat-style scanner plumbing is present and exposed behind `FLAG_SYS_DEXNAV`.
- M4 deterministic reserves already provide 1,025/1,025 coverage, so M7 is not an availability dependency.
- `SELECT` in the postgame DexNav opens a nine-region selector; `UP/DOWN` chooses Kanto, Johto, Hoenn, Sinnoh, Unova, Kalos, Alola, Galar/Hisui, or Paldea, and `A` persists the choice and rebuilds the scanner.
- `scripts/generate_m7_habitat.py` derives nine 16-species pools from the canonical National Dex mapping and excludes the Legendary contract entries.
- The selection persists in collision-audited expanded-save variable `VAR_M7_MIGRATION_GROUP` (`0x515A`). Migration species augment DexNav only; normal map encounter headers and map identity are unchanged.
- Overlay `patches/cfru/0018-dexnav-habitat-migrations.patch` contains the compiled integration. `scripts/audit_m7.py` validates the selector, postgame gate, generated pools, variable allocation, and scan bindings.
- Manual scanner encounter and save/reload QA remains in the M5 checklist.

Run `python3 scripts/generate_m7_habitat.py --check && python3 scripts/audit_m7.py`.
