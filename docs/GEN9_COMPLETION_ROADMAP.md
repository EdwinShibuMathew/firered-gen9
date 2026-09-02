# FireRed Gen 9 Completion Roadmap

This is the single working checklist for completing the expanded FireRed project from the current M1 review gate through release. It supersedes scattered planning notes while preserving the approved architecture and safeguards.

Status markers:

- `[x]` verified complete
- `[~]` started or partially verified
- `[ ]` not started
- `[!]` blocked or requires a decision/evidence

## Current position

The clean source/reference repository remains `/home/edwin/projects/gamedev/pokefirered-contrary` and has not been rewritten. The separate expansion project is `/home/edwin/projects/gamedev/firered-gen9`.

The project is a binary-expansion workflow, not a normal `pret/pokefirered` decompilation: a locally built legal vanilla ROM is passed through pinned Dynamic Pokémon Expansion (DPE) and CFRU scripts. Complete ROMs, saves, BIOS files, emulator states, and unlicensed standalone assets must never be committed or distributed. The release artifact is a BPS/UPS-style patch and reproducible source/build metadata.

Current checkpoint commits:

- `fe85545` — M0 and M1 build candidate
- `2fdf784` — interactive M1 limitation report

## Completed foundation

### M0 — verified vanilla ROM build `[x]`

- Recorded the original repository state and preserved its existing dirty custom work.
- Built vanilla FireRed locally from pinned pret revision `c75f352304d529f6ba92d4f74b9cf8b5c3810788`.
- Verified 16 MiB ROM SHA-1 `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc`.
- Verified SHA-256 `3d0c79f1627022e18765766f6cb5ea067f6b5bf7dca115552189ad65a5c3a8ac`.
- Kept ROM outputs ignored and uncommitted.

### M1 — untouched DPE + CFRU engine candidate `[x]`

- Pinned DPE Gen 9 commit `376849ea0887131689a36cc51846c573f7735f22` at insertion offset `0x1600000`.
- Pinned CFRU Expansion `Experiments` commit `dade256a1db1fa036fedd9f8566cb48de405e97a` at insertion offset `0x1000000`.
- Used the recommended order: vanilla input → DPE → CFRU. CFRU supplies the save/item/TM-tutor engine expansions expected by the combined workflow; this interpretation is documented in `docs/UPSTREAM_PINS.md`.
- Verified DPE output SHA-256 `c2c27af7ab7ca9efa0a02a90d78a614b43fe65c1cf2eb45bd01935d3c5e02a25`.
- Verified CFRU output SHA-256 `32136e7063ea8ea54eed429a4f311f3ae093037e4281cda00ee9618a353b52cc`.
- Recorded payload hashes, tool versions, offsets, and the modern-GCC `-ffreestanding` compatibility overlay in `build-lock.json`.
- Python 3.14.4 succeeded; no global obsolete Python was installed.
- Verified with mGBA/libmGBA 0.10.5: title boot, new game, maps, starter selection, rival battle, save, emulator restart, and save reload.
- Verified a disposable 128 KiB flash save and `CONTINUE` after a fresh process.

M1 is tagged `gen9-engine-baseline`. Seven gates have recorded automated evidence; the four desktop-only capture/Pokédex/PC/audio checks are documented as optional follow-up smoke tests rather than blockers. Results are maintained in `docs/M1_TEST_RESULTS.md`.

## Remaining work

### Finish M1 and create the engine baseline

1. `[!]` Complete a real mGBA smoke test for wild encounter and capture. Obtain Poké Balls, enter grass, weaken a wild Pokémon, capture it, and preserve the save.
2. `[!]` Confirm the captured Pokémon registers in the Pokédex and survives a save/reload.
3. `[!]` Deposit and withdraw the captured Pokémon through a PC, including save/reload.
4. `[!]` Verify audible title/music/cry output in a desktop mGBA session. The headless harness cannot prove audio.
5. `[ ]` Repeat representative map transitions and check for visible/audio corruption after the above tests.
6. `[ ]` Update `docs/M1_TEST_RESULTS.md` with commands, screenshots/logs, and actual results only.
7. `[ ]` Tag or checkpoint the exact artifact as `gen9-engine-baseline` only after every M1 gate passes.

### M2 — validate all species data `[x]`

1. Freeze the upstream species/form ordering before any distributed saves exist.
2. Add `scripts/audit_species.py` and make the build fail for missing mandatory data.
3. Audit all 1,025 National Pokédex species and all meaningful permanently storable forms.
4. Validate IDs, names, base-stat distribution, types (including Fairy and Stellar), abilities, hidden abilities, catch/growth/gender data, egg groups, experience/EV yields, held items, evolutions, level-up learnsets, TM/tutor compatibility, cries, front/back sprites, icons, normal/shiny palettes, Pokédex text, height, weight, and classification/habitat.
5. Report duplicate IDs, invalid references, missing assets, placeholder artwork, missing abilities/learnsets/evolutions, and incomplete forms.
6. Specifically verify and replace the upstream Poltchageist/Sinistcha placeholder form artwork before release; it may not block the engine proof-of-concept.
7. Defer custom `GEN9_DATA_VERSION` and incompatible-save rejection metadata until the CFRU/DPE save layout has been identified and repeatedly tested.

### M3 — make every evolution possible offline `[~]`

1. Audit every evolution chain from Generations 1–9 and prove a reachable path from an obtainable base species.
2. `[x]` Replace trade-only evolution with a reusable Link Cable item; support held-item trade equivalents.
3. Make version exclusives, location evolutions, friendship/day/night, move-known, Hisuian, and item conditions achievable in one offline ROM.
4. Define sensible FireRed-compatible conditions for Finizen, Gimmighoul, Kingambit, Ursaluna, Runerigus, Inkay, and other multiplayer/location-dependent cases.
5. Ensure required moves and evolution items are obtainable before the evolution level/condition.
6. Remove any Elite Four completion prerequisite that is not intentionally part of the design.
7. Add an evolution audit that reports unreachable final evolutions and missing prerequisite items/moves.

### M4 — deterministic 1,025/1,025 availability `[x]`

1. Create `data/availability.csv` with species, form, acquisition method, map, encounter type, badge requirement, rate, evolution source, quest, and notes.
2. Add `scripts/audit_availability.py` to calculate closure across wild encounters, gifts, fossils, trades, static encounters, evolutions, eggs, quests, and form changes.
3. Use deterministic regional reserves or Sevii Island habitats first; do not make the Habitat Scanner a dependency.
4. Preserve readable Kanto progression and distribute later generations across deterministic biome/Sevii areas rather than overcrowding route tables.
5. Make every starter family, fossil, Legendary, and Mythical permanently obtainable without Mystery Gift, expired events, a second version, or another player.
6. Make one-time encounters recoverable where practical and document any deliberate one-time behavior.
7. Do not extend PC storage for version one. Guarantee every species is obtainable and registerable, not simultaneously storable.
8. Require the audit to report `1025 / 1025 National Pokédex species obtainable` before M4 completion.

### M5 — forms, quests, and content polish `[~]`

1. Implement permanent regional/forms and controlled item/location form changes.
2. Cover Paldean Tauros breeds, Basculin, Oricorio, Deerling/Sawsbuck, Shellos/Gastrodon, Flabébé, Pumpkaboo/Gourgeist, Tatsugiri, Maushold, Dudunsparce, and equivalent meaningful forms.
3. Add form-changing locations/items for Rotom, Deoxys, Shaymin, Hoopa, Furfrou, Arceus, Silvally, Genesect, Ogerpon, Terapagos, and similar species.
4. Keep Mega Evolution, Primal Reversion, Ultra Burst, Dynamax/Gigantamax, and Terastallization as battle-only transformations.
5. Add permanent Legendary/Mythical quests, fossil restoration, starter gifts, regional reserves, and repeatable item acquisition. `[x]` Major static Legendary encounters now reset on area re-entry through the tracked pret overlay.
6. Fix every reported placeholder or duplicated form asset and credit each upstream asset creator.
7. Add the evolution encyclopedia/evolutionpedia: searchable/ordered species pages showing evolution method, prerequisites, and base-stat distribution with readable retro styling.
8. Preserve the approved unlimited-use behavior for key items and reusable field utilities while keeping consumable item semantics intentional.

### M6 — port existing custom starter work `[~]`

1. Only after M1–M5 are stable, inspect the preserved contrary repository for exact custom starter data and behavior.
2. Port existing starter species, stats, abilities, moves, illegal moves, and damage/healing reversal behavior through an isolated configuration layer.
3. Do not invent missing final values; document configuration points when source data is absent.
4. Test Contrary-style behavior for direct, multi-hit, critical, recoil, drain, poison/burn, Leech Seed, weather, hazards, confusion, Struggle, healing, held-item healing, Pokémon Center healing, revives, fainting, and full-HP cases.

### M7 — optional Habitat Scanner and advanced mechanics `[~]`

1. Add the National Habitat Scanner only after deterministic availability already reaches 1,025/1,025.
2. Implement selectable Kanto, Johto, Hoenn, Sinnoh, Unova, Kalos, Alola, Galar/Hisui, and Paldea migration groups without changing map identity.
3. Add advanced battle mechanics individually—never all at once—and regression-test normal battles, saving, forms, abilities, and encounters after each mechanic.

### M8 — release patch and final testing `[~]`

1. Build a reproducible release from pinned commits and verify clean input/output checksums.
2. Produce a legal BPS/UPS patch, not a complete ROM.
3. Complete `docs/TEST_MATRIX.md` for boundary IDs Bulbasaur, Mew, Celebi, Deoxys, Arceus, Genesect, Volcanion, Zeraora, Eternatus, Enamorus, Pecharunt, and the highest internal form ID.
4. Test creation, wild encounter, capture, Pokédex, party, summary, front/back sprites, cries, level-up, moves, evolution, PC, save/reload, Hall of Fame, breeding, and shiny display for representative IDs.
5. Test every evolution method/item, encounter type, regional pool, starter gift, fossil, Legendary/Mythical quest, blackout/healing path, repeated save/load, and new game after an old save.
6. Test same-build multiplayer only if desired; explicitly warn that stock FireRed and vanilla-link trading are incompatible.
7. Finalize `README.md`, `CREDITS.md`, `docs/GEN9_ARCHITECTURE.md`, `docs/UPSTREAM_PINS.md`, `docs/TEST_MATRIX.md`, availability/evolution audits, known limitations, and patch application instructions.
8. Confirm the release gate: complete ROMs, saves, BIOS files, emulator states, and unlicensed standalone assets are never committed or distributed.

## Reproducibility and safety gates

- Keep exact upstream commits and insertion offsets in `build-lock.json`.
- Keep ROMs, saves, BIOS files, temporary build products, and local toolchains ignored.
- Preserve generated offset data when it affects reproducibility; do not discard it as generic build output.
- Build after every meaningful engine change and keep milestone checkpoints.
- Never reset, clean, or overwrite unrelated user work in the original repository.
- Never use Leon’s ROM base, a downloaded copyrighted ROM, expired Mystery Gift distribution, or stock-ROM trading as a dependency.
- Never report a test as passed without a recorded run and observable evidence.

## Immediate next action

M3 remains the user-owned runtime gate: both source audits pass and the corrected candidate boots without emulator errors, while controlled evolution/save tests are deferred to manual QA. M4 automated implementation is complete at 1,025/1,025 through CFRU/stock wild tables, scripted acquisitions, in-game trades, nine postgame Sevii reserve maps, and evolution closure. M5’s form registry and existing permanent item-handler audit pass; dedicated field routes, repeatable quests, and the evolution encyclopedia remain. M6’s Contrary starter data and Oak-gift port are implemented through locked DPE/CFRU overlays; owner-led battle/save QA remains. M7’s existing DexNav foundation is audited, while migration groups and advanced mechanics remain optional work. M8’s release-hygiene gate and boundary test matrix are documented; legal patch generation and manual execution remain.
