# Project Status

**Last reconciled:** 2026-09-05
**Code status:** development-complete; the P0 boot regression is fixed and smoke-tested; owner-led full gameplay verification remains pending

Status markers: `[x]` implemented/automated-tested, `[~]` implemented but awaiting manual verification, `[ ]` outstanding.

## Milestones

- M0 `[x]` — verified clean FireRed input and pinned build pipeline.
- M1 `[x]` — DPE/CFRU engine baseline built, boot-tested, and manually verified. Historical evidence is retained in `HISTORY.md`.
- M2 `[x]` — all 1,025 National Pokédex species pass the data audit; asset provenance is tracked separately.
- M3 `[~]` — 883 evolution-table records compile and audit; representative evolution/save QA remains.
- M4 `[x]` — deterministic availability is 1,025/1,025; static Legendary captures are once per save with flee, defeat, and blackout recovery.
- M5 `[~]` — Evolution Guide, generated Form Lab and Form Preserve, safe dedicated routes, fusion guards, and the 26-entry Legendary Hub compile and pass structural audits.
- M6 `[~]` — Contrary Charizard starter data and Oak gift compile through pinned overlays; battle/save QA remains.
- M7 `[~]` — nine generated postgame DexNav migration groups compile; scanner/save QA remains.
- M8 `[~]` — a clean, boot-tested private ROM exists; the earlier BPS candidate was invalidated by the boot fix and must be regenerated after the manual matrix and public asset review.

## Completed implementation

1. Preserved the pinned pret → DPE → CFRU pipeline and legal artifact boundary.
2. Validated every National Pokédex species and achieved deterministic 1,025/1,025 availability.
3. Implemented offline evolution methods, prerequisite moves/items, reusable Link Cable behavior, and the 883-record ledger.
4. Implemented one-capture Legendary recovery semantics and the 26-entry Generation I–IX Research Hub.
5. Integrated the Pokédex Evolution Guide with all 43 method values handled, bounded buffers, icon cleanup, pagination, and long-text wrapping.
6. Replaced heuristic form discovery with the canonical 442-ID DPE-to-National-Dex inventory.
7. Bound 439 safe forms to battle/item/fusion handlers, generated Form Lab tables, or generated permanent-form encounters. The three unsafe internal placeholders remain excluded.
8. Implemented the Cinnabar Form Lab and postgame Form Preserve through the existing scientist and scrolling-menu system.
9. Implemented the optional postgame DexNav selector with nine generated migration groups and persistent variable `0x515A`.
10. Built a private ROM from the verified clean FireRed input. The earlier round-trip-tested BPS is retained only as historical evidence because it predates the boot-regression fix.
11. Preserved the field-speed defaults and made input ordering and compression padding reproducible across isolated workspaces without changing the locked ROM. Current automated emulator evidence is recorded in `TESTING.md`.

Key checkpoints:

- `28fa112` — compiled M5 gameplay integrations.
- `bde8b97` — canonical form inventory, generated Form Lab, and complete Evolution Guide formatters.
- `2ad2d11` — postgame permanent-form encounter bindings.
- `fd23112` — postgame DexNav habitat migration selector.
- `9cf595a` — reconciled development-completion documentation.

## Remaining gates

1. `[ ]` Edwin executes `TESTING.md` in mGBA and records actual results.
2. `[ ]` Any further concrete runtime failures become targeted development fixes; no known boot defect is currently open.
3. `[ ]` Visually review ignored asset contact sheets and resolve or explicitly exclude suspicious provenance records.
4. `[ ]` Change relevant milestones from `IMPLEMENTED_UNVERIFIED` to `MANUALLY_VERIFIED` after observed passes.
5. `[ ]` Regenerate the final public BPS and release notes only after manual and asset gates pass.

Two owner-observed NPC issues remain open in [TEST_OBSERVATIONS.md](TEST_OBSERVATIONS.md): no dialogue below Oak's lab, and an unexpected rival battle beside a Pokémon Centre. Each was observed once; the cleanup does not mark either resolved.

The only unbound internal forms are deliberately unsafe placeholders: `SHADOW_WARRIOR`, Zygarde Cell, and Zygarde Core. They are not ordinary safe forms and are excluded rather than risking invalid save data.

## Current build evidence

- Clean input SHA-1: `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc`
- Candidate ROM SHA-256: `2cd43618ea7a8bf9eeca2783e60df9b64710c23792a498b8cfd0b0ca17437358`
- Superseded BPS SHA-256: `ab4cc33cc061f8e5e8e763baa202ca38cecda53e566e2840da906ab9c0388167` (must not be released)
- Pipeline ROM: `.upstream/cfru/test.gba` (verify before copying to a private test location)
- Superseded private patch: `build/private/firered-gen9-m8-test-candidate.bps`
- Full build: `BUILD_JOBS=4 ./scripts/build_pipeline.sh`

Complete ROMs, saves, BIOS files, emulator states, contact sheets, and private artifacts remain ignored and must not be committed.
