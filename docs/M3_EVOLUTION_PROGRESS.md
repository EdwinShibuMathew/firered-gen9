# M3 Evolution Availability — Progress Report

**Milestone:** Make every evolution possible offline  
**Status:** Phases 1–3 implemented; runtime validation remains  
**Last updated:** 2026-09-01

## Measured baseline

The authoritative audit now parses `.upstream/dpe/src/Evolution_Table.c` directly. Earlier figures counted `case` labels in CFRU runtime code and were not evolution counts.

- 883 total table records parsed
- 592 acquisition evolutions
- 291 Mega/Gigantamax battle transformations excluded from acquisition reachability
- 503 source species with acquisition evolutions
- 38 acquisition evolution methods in use
- 31 legacy trade-dependent records: all have offline alternatives in the pinned DPE table
- 7 environment-dependent map records, all with item alternatives
- 2 Gholdengo coin evolutions are supported by a new CFRU runtime overlay and FireRed's offline Game Corner

The complete machine-readable mapping is `data/evolution_mapping.csv`. Regenerate it with:

```sh
python3 scripts/m3_evolution_audit.py --csv data/evolution_mapping.csv
```

Use `--require-complete` as the eventual milestone gate. It intentionally fails while blockers or unproved prerequisites remain.

## Phase status

### Phase 1 — extraction and analysis `[x]`

- [x] Parse the actual evolution table, including multiline records.
- [x] Separate acquisition evolutions from battle-only transformations.
- [x] Record source, target, method, parameters, status, and source line.
- [x] Identify exact trade blockers and environment-dependent prerequisites.
- [x] Produce a reproducible CSV mapping.

### Phase 2 — offline method implementation `[x]`

- [x] Use the existing Link Cable alternatives for all 14 plain trade evolutions.
- [x] Use the held item directly for all 17 trade-item evolutions.
- [x] Sell the Link Cable in Celadon Department Store 4F for ₽3,000.
- [x] Make the Link Cable reusable while retaining normal consumption for evolution stones/items.
- [x] Add missing CFRU runtime support for Gholdengo and both Maushold outcomes.
- [x] Rebuild the patched vanilla → DPE → CFRU pipeline successfully.

All changes are represented by tracked patches under `patches/dpe/` and `patches/cfru/`, locked by SHA-256 in `build-lock.json`, and verified by `scripts/apply_overlays.py`.

### Phase 3 — prerequisite availability `[x]`

- [x] Provide item alternatives for all seven configured map-dependent records.
- [x] Replace Alolan Raichu's unavailable shallow-water condition with a Shiny Stone route.
- [x] Verify the 2,999 Coin Case requirement is attainable through FireRed's offline Game Corner.
- [x] Audit all 52 evolution items and provide deterministic acquisition for all of them.
- [x] Audit all 14 required moves against the evolving species and repair five missing learnsets.
- [x] Confirm time, weather, party, critical-hit, nature, gender, and held-item methods are implemented in source; runtime testing remains Phase 4.

### Phase 4 — reachability and emulator validation `[~]`

- [x] Extend the audit from method classification to item and move prerequisites.
- [x] Make both `--require-complete` source gates pass.
- [ ] Test representative examples of every evolution method in mGBA.
- [ ] Verify evolved species and item behavior across save/reload.
- [ ] Record commands and observable evidence; do not infer emulator success from source parsing.

The rebuilt ROM passes its locked SHA-256 check. The existing `test.sav` fixture is currently an empty 128 KiB save (party count zero), so the legacy M1 save-content assertions do not pass and cannot be used as M3 evolution evidence. Fresh targeted emulator fixtures are still required.

A save-independent SDL-dummy mGBA launch originally exposed an invalid vanilla map overlay: changing the base event-script layout before binary expansion broke CFRU's fixed-address assumptions and produced repeated `Illegal opcode: 0000ea00` logs. Item distribution was moved into CFRU's injected code space and the vanilla ROM returned to its canonical SHA-1. Vanilla, DPE, and CFRU now each run for the same two-second headless smoke window with zero emulator errors. This proves boot regression recovery, not individual evolution behavior.

An interactive mGBA run was also attempted on 2026-09-01, but the execution environment did not expose an authenticated X11 control channel for reliable input or observation. No evolution result was inferred from that attempt; the controlled runtime checklist remains open.

## Current blockers

The audit reports 31 legacy trade records, but every corresponding source→target edge has an offline item alternative. Link Cable acquisition and reuse are now implemented through tracked overlays.

Both source gates now pass: every acquisition edge has an offline-capable route, all referenced evolution items have acquisition evidence, and all move-known prerequisites appear in the evolving species' level-up learnset.

## Next action

Create controlled saves and test representative evolution methods in mGBA, including save/reload persistence.
