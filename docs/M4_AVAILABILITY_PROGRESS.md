# M4 Deterministic Availability — Progress Report

**Milestone:** 1,025/1,025 National Pokédex species obtainable offline  
**Status:** Automated implementation complete; manual encounter/capture QA deferred  
**Started:** 2026-09-01

## Baseline

The audit reads CFRU's active time-of-day wild table, stock FireRed wild encounters and scripted acquisitions, uses DPE's species-to-National-Dex mapping, and calculates evolution closure from the M3 table.

- 2,685 direct acquisition records
- 597 unique directly obtainable species/forms
- 1,053 species/forms after evolution closure
- 1,025 / 1,025 National Pokédex species covered
- 0 National Pokédex species missing

CFRU adds four Route 1 time tables and nine postgame Sevii reserve maps. The reserve generator assigns only uncovered evolution-family roots, with 48 deterministic morning/day/evening/night land slots per map; reserve tables are disabled until `FLAG_SYS_GAME_CLEAR`. Other coverage comes from stock FireRed maps and scripted acquisitions.

## Implemented infrastructure

- [x] Create `data/availability.csv` with the roadmap's acquisition fields.
- [x] Create `scripts/audit_availability.py`.
- [x] Parse active wild encounter records.
- [x] Map internal species/forms to National Pokédex entries.
- [x] Calculate iterative evolution closure.
- [x] Add a failing `--require-complete` gate.
- [x] Parse literal and variable-driven stock FireRed gifts, starters, fossils, static battles, and eggs.
- [x] Parse all nine stock FireRed in-game trades from their data table and map scripts.

## Remaining work

- [x] Import stock FireRed encounters not replaced by CFRU Route 1 time tables.
- [x] Parse all currently discoverable direct and variable-driven stock acquisitions.
- [x] Define deterministic Sevii reserve habitats without changing Kanto progression tables.
- [x] Add every starter, fossil, Legendary, Mythical, and version-exclusive family through direct or evolution-closure sources.
- [x] Make major static Legendary encounters repeatable after leaving and re-entering their area (Zapdos, Articuno, Moltres, Mewtwo, Ho-Oh, and Deoxys).
- [x] Reach and record `1025 / 1025 National Pokédex species obtainable`.
- [ ] Validate representative encounters and captures in mGBA.

## Next action

M4 automated gate is complete. The repeatable-encounter overlay resets each listed static encounter's fought/flew-away lock on map transition, so the area can be revisited and the encounter can be triggered again. Run `python3 scripts/generate_gen9_reserve.py --check`, `python3 scripts/audit_availability.py --require-complete`, and `python3 scripts/apply_overlays.py --check` after source changes. Manual mGBA encounter/capture/revisit QA remains part of the user-owned final test pass.
