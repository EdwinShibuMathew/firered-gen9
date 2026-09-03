# Milestone History

This document preserves the unique information from retired milestone plans, progress reports, generated reports, and summaries. It is historical evidence, not the source of current status; use `STATUS.md` for current claims and `TESTING.md` for active verification.

The retired files are removed only after this index and the repository's Git history preserve their contents. The manifest below records the pre-cleanup SHA-256 for auditability; the commit that performs the cleanup is the canonical archival point. Historical path references inside archived excerpts are intentionally left unchanged.

## Pre-cleanup content manifest

| Retired source | SHA-256 |
|---|---|
| `M1_COMPLETION_SUMMARY.md` | `08877344c441fe90dcf7ab85656d997349533afb4f93e1861b1998366022035d` |
| `docs/DEVELOPMENT_COMPLETION_PLAN.md` | `309a5d828a151a82bde3e8a19c02493a591cd399ad183cb4b97b67bface37dde` |
| `docs/EVOLUTION_GUIDE_UI.md` | `1e7dc0a89c7b892151c98e3f1279580459ded7f286e0d30cfeda4f47c0003121` |
| `docs/GEN9_ARCHITECTURE.md` | `79d93529617b0c507bbf03c47e83041f5119ffc55a55ad0c876a6daa7d7c02d7` |
| `docs/GEN9_COMPLETION_ROADMAP.md` | `2642186d30eeafd514041f4c5e99b99e58819ac0f5073ee433524b6d89343b98` |
| `docs/M1_COMPLETION_REPORT.md` | `aa2122bb2fa556c9cd4073e68d84777db98f11933e501026abd211556312630f` |
| `docs/M1_COMPLETION_STATUS.md` | `d2ce7c73b1b4ae3eb4e72329ae05b193c8d96ef1995b109b2043efc0028317ec` |
| `docs/M1_TEST_RESULTS.md` | `5ad31282fa1d45153af9ab81b98689bcef455b268752baea8eddba8cd3c1c167` |
| `docs/M2_SPECIES_AUDIT_PLAN.md` | `653bca1a10714c115f689cdd6e122b7174fdd5100eb4b859ba54f1bdef71f230` |
| `docs/M2_SPECIES_AUDIT_PROGRESS.md` | `b54edc4d95402bc9040d2c82361240cbadbdbb3878dea7a59b16d0c19afd5b6f` |
| `docs/M2_SPECIES_AUDIT_REPORT.md` | `6da3ab796263fd6934f30ee0c8d93f0f1b78400c9f16ee8958571d0767456669` |
| `docs/M3_EVOLUTION_PLAN.md` | `78dfc10f316b5c2b3b9e7f46da250be2f2fe3d9587715283b43726dbb6198d76` |
| `docs/M3_EVOLUTION_PROGRESS.md` | `569c5b2fd440734af186806f04e989c832b2218e9811f08bd026c4cd6d4cb570` |
| `docs/M4_AVAILABILITY_PROGRESS.md` | `7097331be1c9d7b86b1fa7eaadc7c9d161ab64c759efd0335e8cbf9cde5b6067` |
| `docs/M5_DESIGN_SPEC.md` | `efd5808c051f2ba04e512b282c5ce00f7e74d80722ada1f2140ab5c0e00011d2` |
| `docs/M5_FORMS_PROGRESS.md` | `01f705930b719c3064305616a0f5f88c9f43b75425c58886e3078f6b4032a7e9` |
| `docs/M5_MANUAL_TEST_CHECKLIST.md` | `afb97ba175984af3117a6b0c2a668491316a72f539a8a039e14e76ecad4e12cb` |
| `docs/M6_STARTER_PROGRESS.md` | `cdd307248e2af8875fb66a6f1674f44521f7c3b25c2b96c3dd403fc3e6c77c94` |
| `docs/M7_HABITAT_PROGRESS.md` | `ac3dc58274f98a62d7e2bbeaa56899dbb90769f7970d5808c12a41d122814982` |
| `docs/M8_RELEASE_PROGRESS.md` | `1948dabb85a8696e29ec4387956a55476de7bfef6ae46a8fa7026b89ef32145d` |
| `docs/TEST_MATRIX.md` | `733ea38bd37599692136c3d061c2f2887cfaca52652fd9e00e010abfc9363c67` |
| `docs/UPSTREAM_PINS.md` | `9d22035e6fc358c7922d24d907fa3d5a3206de4809201c52885a7914edfbfe70` |

## Retired document map

| Retired path | Preserved in |
|---|---|
| `M1_COMPLETION_SUMMARY.md` | M1 and M2 sections below |
| `docs/M1_COMPLETION_REPORT.md` | M1 generated-report snapshot below |
| `docs/M1_COMPLETION_STATUS.md` | Same snapshot; duplicate provenance note below |
| `docs/M1_TEST_RESULTS.md` | `TESTING.md` baseline evidence and M1 history below |
| `docs/M2_SPECIES_AUDIT_PLAN.md` | M2 original plan below |
| `docs/M2_SPECIES_AUDIT_PROGRESS.md` | M2 execution and findings below |
| `docs/M2_SPECIES_AUDIT_REPORT.md` | M2 final metrics and audit details below |
| `docs/M3_EVOLUTION_PLAN.md` | M3 scope and execution below |
| `docs/M3_EVOLUTION_PROGRESS.md` | M3 measurements, fixes, and emulator history below |
| `docs/M4_AVAILABILITY_PROGRESS.md` | M4 measurements and implementation below |
| `docs/DEVELOPMENT_COMPLETION_PLAN.md` | `STATUS.md` |
| `docs/GEN9_COMPLETION_ROADMAP.md` | `STATUS.md` |
| `docs/GEN9_ARCHITECTURE.md` | `ARCHITECTURE.md` |
| `docs/UPSTREAM_PINS.md` | `ARCHITECTURE.md` |
| `docs/M5_DESIGN_SPEC.md` | `FEATURES.md` |
| `docs/EVOLUTION_GUIDE_UI.md` | `FEATURES.md` |
| `docs/M5_FORMS_PROGRESS.md` | `STATUS.md` and `FEATURES.md` |
| `docs/M5_MANUAL_TEST_CHECKLIST.md` | `TESTING.md` |
| `docs/M6_STARTER_PROGRESS.md` | `STATUS.md` and `FEATURES.md` |
| `docs/M7_HABITAT_PROGRESS.md` | `STATUS.md` and `FEATURES.md` |
| `docs/M8_RELEASE_PROGRESS.md` | `STATUS.md`, `ARCHITECTURE.md`, and `TESTING.md` |
| `docs/TEST_MATRIX.md` | `TESTING.md` |

## M0–M1 engine baseline

M1 established a reproducible vanilla → DPE → CFRU build and verified the baseline engine. The historical CFRU artifact had SHA-256 `32136e7063ea8ea54eed429a4f311f3ae093037e4281cda00ee9618a353b52cc`.

The 11 gates were ROM integrity, boot/new game, map transitions, starter selection, rival battle, save/reload, graphics, wild encounter/capture, Pokédex registration, PC deposit/withdraw, and audio. Seven were automated and four were owner-observed. Headless testing reached the title, intro, bedroom, downstairs, Pallet Town, Oak's lab, starter battle, and post-rival state. A 131,088-byte mGBA save container was restarted in a separate core and restored with `CONTINUE`; its historical SHA-256 was `cb19f54b26f918fc0f485c7bc32d650bf2478a0d1d7e6352b2f96456471cce6a`.

The manual procedures captured a Route 1 Pokémon, checked its caught Pokédex state, deposited and withdrew it at a Pokémon Center PC, saved/restarted, and checked title/battle music, cries, menu sounds, and overworld audio. All gates were recorded complete on 2026-09-01 in commit `cb60518098ec99d89aa68d0d19a04d4515ede358`; tag `gen9-engine-baseline` identifies the baseline.

Historical troubleshooting retained from the M1 summary:

- The local SDL frontend is `.tools/mgba-sdl/usr/games/mgba`; a system `mgba` is also acceptable.
- Missing local shared libraries can be supplied through the ignored tool directory's `LD_LIBRARY_PATH`.
- `.upstream/cfru/test.sav` is disposable. A fresh save can be produced by playing through startup and the rival battle.
- No BIOS was used; automated tests used mGBA's HLE BIOS.

Two generated M1 reports were retained previously. Their bodies were identical; only their timestamps differed: `2026-09-01T13:07:01.245000` (`M1_COMPLETION_REPORT`) and `2026-09-01T13:09:51.794195` (`M1_COMPLETION_STATUS`). Their report body recorded the 11 gates above, the ROM/save hashes, the manual procedure, and the then-future M2 audit. It also referenced a historical `m1_complete_final.py --capture` command that is not part of the current workflow.

Early checkpoint commits were:

- `9837f1c` — testing infrastructure and documentation.
- `cb60518` — all M1 gates verified.
- `1e9b125` — began M2 framework and planning.
- `3d9c383` — M2 registry validation.
- `6f71ffa` — M2 comprehensive asset/data validation.

## M2 species audit

### Original plan and criteria

The M2 goal was to freeze species/form ordering and validate National Dex IDs, names/forms, six base stats, types including Fairy/Stellar, abilities, catch/EXP/EV data, egg/gender data, physical/Pokédex metadata, evolution chains, learnsets, compatibility, held items, front/back sprites, shiny palettes, icons, and cries. Findings were classified as critical (invalid/missing/duplicate IDs, null data, invalid types), high (missing assets/text/learnsets or placeholders), medium (chains, abilities, forms), and informational statistics.

The original four phases were extraction, validation framework, full audit, and remediation. Proposed helpers included ROM extraction and JSON validation schemas; the implemented source-oriented tools became `scripts/audit_species.py`, `scripts/m2_asset_audit.py`, and `scripts/m2_comprehensive_audit.py`. Save-layout metadata and rejection screens were deliberately deferred.

### Execution and fixes

- Parsed 1,464 compiled species constants and confirmed all nine generations.
- Reconciled the later authoritative inventory to 442 canonical alternate-form IDs from DPE's `Species_To_Pokdex_Table.c`; earlier documents used heuristic counts of 264 forms and 1,200 “base species,” which are retained only as historical measurements.
- Parsed 1,107 learnset arrays, 17,861 move entries, and 779 unique moves.
- Found 394 ability definitions and 22 type constants.
- Counted 994 named moves and 554 descriptions (55.7% historical source coverage); descriptions/Pokédex text may be generated during build.
- Validated the 43-method evolution structure.
- Corrected `TYPE_STELLAR` validation from decimal 18 to `0x18` (24).
- Corrected three undefined `SPECIES_URSHIFU_SINGLE_STRIKE` JSON references to `SPECIES_URSHIFU_SINGLE`.
- Improved learnset and multiline evolution parsing.
- Reported zero critical findings and five of five comprehensive checks passing.

The original validation checklist required valid IDs, nonzero stats, types, catch/EXP/EV values, abilities, evolution data, graphics/palettes/text, moves, and form records. The final report's source locations were CFRU's species constants/base-stat structures, `src/Tables/level_up_learnsets.c`, ability/move string tables, `src/evolution.c`, and `graphics/`. Current paths are materialized in ignored pinned checkouts and may differ from the early estimates.

Historical generation targets were 151 Kanto, 100 Johto, 135 Hoenn, 107 Sinnoh, 156 Unova, 72 Kalos, 81 Alola, 89 Galar, and 96 Paldea-era entries, totaling the 1,025 National Dex goal. The audit was tagged `m2-species-audit-complete` after all critical checks passed. Per-file asset provenance later moved to `data/asset_provenance.csv`; public asset review remains separate from species completeness.

## M3 offline evolution

M3 scoped acquisition evolutions from the pinned DPE table and excluded Mega/Gigantamax battle transformations. The corrected baseline is 883 records: 592 acquisition records, 291 battle transformations, 503 sources with acquisition evolutions, 38 acquisition methods in use, 31 legacy trade records with offline alternatives, seven environment-dependent records with item alternatives, and two Gholdengo coin evolutions supported by CFRU and the offline Game Corner.

Implemented work:

- `data/evolution_mapping.csv` is generated from the actual multiline/legacy-designator table.
- All 14 plain trade edges have Link Cable alternatives; all 17 trade-item edges use the held item directly.
- Link Cable is reusable and sold at Celadon Department Store 4F for ₽3,000.
- Alolan Raichu uses a Shiny Stone instead of an unavailable shallow-water condition.
- CFRU runtime cases cover Gholdengo and both Maushold outcomes.
- All 52 evolution-item constants have deterministic acquisition; Celadon is the initial distribution point.
- Fourteen known-move prerequisites were checked; Rage Fist, Twin Beam, Hyper Drill, Psyshield Bash, and Dragon Cheer were added where missing.
- `data/evolution_prerequisites.csv`, the method audit, and prerequisite audit pass.

Required source gates are:

```sh
python3 scripts/m3_evolution_audit.py --require-complete
python3 scripts/m3_prerequisite_audit.py --require-complete
```

An early attempt to modify fixed-layout vanilla event data caused repeated mGBA `Illegal opcode: 0000ea00` logs. Moving item distribution to CFRU's injected space restored the canonical vanilla input. Vanilla, DPE, and CFRU then survived equal two-second headless smoke windows without emulator errors. This proved boot recovery, not individual evolution behavior. Representative Link Cable, item, friendship/time, move, environment, gender/stat/party/personality, Gholdengo, Maushold, and save/reload cases remain in the current manual test gate.

## M4 deterministic availability

The availability audit combines CFRU time-of-day tables, stock FireRed wild/scripted acquisitions, DPE National Dex mapping, and iterative evolution closure.

Historical measured result:

- 2,685 direct acquisition records.
- 597 unique directly obtainable species/forms.
- 1,053 internal species/forms after evolution closure.
- 1,025/1,025 National Pokédex entries covered; zero missing.

CFRU adds four Route 1 time tables and nine postgame Sevii reserve maps. Reserve generation assigns uncovered evolution-family roots to 48 morning/day/evening/night land slots per map and gates them behind `FLAG_SYS_GAME_CLEAR`. Stock maps, variable/literal gifts, starters, fossils, static battles, eggs, and all nine FireRed in-game trades supply the remaining direct records.

Major static Legendary encounters reset temporary fought/fled locks on re-entry while successful captures remain permanent once per save. The later M5 Research Hub generalized this behavior to the 26-entry contract. Current regeneration/audit commands are:

```sh
python3 scripts/generate_gen9_reserve.py --check
python3 scripts/audit_availability.py --require-complete
python3 scripts/apply_overlays.py --check
```

## M5–M8 completion history

M5 added the direct Evolution Guide, canonical generated form routing, `TryChangeMonForm`, Cinnabar Form Lab/Form Preserve, fusion guards, and Generation I–IX Legendary Hub. M6 ported the Contrary starter through isolated overlays without modifying its reference checkout. M7 added the optional nine-group DexNav selector. M8 produced the ignored ROM and round-trip BPS candidate.

The current implementation details, hashes, and pending gates live in `FEATURES.md`, `ARCHITECTURE.md`, `STATUS.md`, and `TESTING.md`; this separation prevents historical plans from contradicting the active handoff.
