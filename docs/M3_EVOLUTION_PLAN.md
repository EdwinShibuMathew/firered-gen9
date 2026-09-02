# M3 Evolution Availability — Implementation Plan

**Milestone:** Make every acquisition evolution possible offline  
**Status:** Phases 1–3 implemented; emulator validation remains  
**Started:** 2026-09-01

## Scope

M3 covers acquisition evolutions in the pinned DPE table. Mega Evolution and Gigantamax records are battle transformations and are excluded. Proving that every base species is obtainable belongs to M4.

## Phase 1 — table extraction and method audit `[x]`

- [x] Parse the actual DPE evolution table, including legacy GNU designators and multiline records.
- [x] Separate 592 acquisition records from 291 battle transformations.
- [x] Evaluate source→target edges as alternative routes rather than treating legacy trade records as blockers.
- [x] Generate `data/evolution_mapping.csv`.
- [x] Make `scripts/m3_evolution_audit.py --require-complete` pass.

## Phase 2 — offline evolution mechanics `[x]`

- [x] Retain all 31 legacy trade records while proving each edge has an offline item alternative.
- [x] Make the Link Cable reusable and sell it in Celadon Department Store 4F.
- [x] Support direct held-item trade replacements.
- [x] Replace Alolan Raichu's unavailable shallow-water route with a Shiny Stone route.
- [x] Add missing CFRU runtime cases for Gholdengo and both Maushold outcomes.
- [x] Represent every change as a SHA-256-locked overlay.

## Phase 3 — item and move prerequisites `[x]`

- [x] Audit 52 distinct evolution item constants.
- [x] Add deterministic Celadon acquisition for the 41 expanded items with no existing FireRed source.
- [x] Validate manifest item IDs against DPE constants.
- [x] Audit 14 move-known prerequisites against each evolving species' level-up learnset.
- [x] Add Rage Fist, Twin Beam, Hyper Drill, Psyshield Bash, and Dragon Cheer to their evolving species.
- [x] Generate `data/evolution_prerequisites.csv`.
- [x] Make `scripts/m3_prerequisite_audit.py --require-complete` pass.

Celadon is the initial deterministic distribution point. Later content milestones may redistribute items for progression and world-building, but must preserve audit completeness.

## Phase 4 — runtime validation `[~]`

- [x] Rebuild the full patched vanilla → DPE → CFRU pipeline.
- [x] Verify overlay idempotence and lock the candidate artifact hashes.
- [ ] Create controlled save fixtures containing representative evolving species and prerequisites.
- [ ] Test Link Cable acquisition, reuse, and save persistence.
- [ ] Test a held-item replacement, Alolan Raichu, Gholdengo, both Maushold outcomes, and all five repaired move evolutions.
- [ ] Test representative friendship, time, gender, weather, party-member, stat, and personality conditions.
- [ ] Record observable mGBA evidence and repeat after save/reload.

The existing local M1 save fixture is empty and cannot provide evolution-test evidence. Source audits and successful compilation do not replace emulator tests.

The earlier SDL-dummy illegal-opcode failure was traced to modifying the fixed-layout vanilla input. After moving item distribution into CFRU's injected code, vanilla, DPE, and CFRU all pass the same error-free headless boot window. Controlled evolution fixtures are still required before M3 completion.

## Completion gate

M3 is complete only when both source gates pass, the full build is reproducible, and representative runtime tests have recorded evidence:

```sh
python3 scripts/m3_evolution_audit.py --require-complete
python3 scripts/m3_prerequisite_audit.py --require-complete
scripts/build_pipeline.sh
```

## Next action

Build targeted mGBA fixtures and validate the new Link Cable, Gholdengo/Maushold cases, Alolan Raichu route, and repaired move-known evolutions in the ROM.
