# Testing and Manual Verification

Automated source/build gates are recorded here separately from owner-observed emulator results. Never mark a runtime row passed solely because code compiles or an audit succeeds.

## Automated baseline evidence

M1 used headless libmGBA 0.10.5 with deterministic input, framebuffer capture, and separate save/reload processes. No BIOS was supplied; mGBA's HLE BIOS was used.

Tested historical artifact: CFRU SHA-256 `32136e7063ea8ea54eed429a4f311f3ae093037e4281cda00ee9618a353b52cc`.

| Check | Result | Evidence |
|---|---|---|
| ROM boot/new game | PASS | Title and intro completed; player reached the bedroom. |
| Map transitions | PASS | Bedroom → downstairs → Pallet Town → Oak's lab. |
| Starter/rival battle | PASS | Squirtle appeared in battle/follower view; rival Bulbasaur battle completed. |
| Graphics | PASS | Title, maps, selection UI, front/back sprites, and follower rendered correctly. |
| Save/restart | PASS | A 131,088-byte mGBA container was written and `CONTINUE` restored the post-rival state. |
| Save SHA-256 | PASS | `cb19f54b26f918fc0f485c7bc32d650bf2478a0d1d7e6352b2f96456471cce6a` (disposable, untracked). |
| Pokédex structure | PASS | Bulbasaur ID 1 and Squirtle ID 7 were present in the save bitfield. |
| Party/PC structure | PASS | Party and box regions were structurally valid for CFRU Expansion. |

All 11 M1 gates—seven automated plus wild capture, Pokédex, PC, and audio checks—were recorded complete on 2026-09-01 in commit `cb60518098ec99d89aa68d0d19a04d4515ede358`; tag `gen9-engine-baseline` points to that milestone.

Historical supporting commands (not the current acceptance workflow):

```sh
python3 scripts/m1_automated_test.py
python3 scripts/m1_completion_report.py
python3 scripts/m1_interactive_test.py
```

The report generator writes to ignored `build/reports/` by default. The automated M1 helper defaults to rewriting the tracked root `m1_test_output.txt`, and the save-completer mutates its input save. Their approximate save analysis and simulated operations cannot certify runtime behavior. Use disposable saves and explicit ignored output paths if investigating these historical helpers.

## Historical startup-regression evidence

The clean 2026-09-04 CFRU artifact has SHA-256 `ce5522a7229b6f46930f313d679c98567becc0036d3231f80f9f2ff68602ddc1`. It was tested with the local mGBA 0.10.5 SDL frontend and HLE BIOS.

| Check | Result | Evidence |
|---|---|---|
| Clean pipeline | PASS | Vanilla, DPE, and CFRU stages matched their locked digests and boot-critical layout checks. |
| Headless boot smoke | PASS | An eight-second run stayed alive with no bad-memory, invalid-address, illegal-opcode, crash, or unimplemented-memory log entry. |
| Startup/title path | PASS | Symbolic debugger breakpoints reached `CB2_InitCopyrightScreenAfterBootup`, `CB2_InitTitleScreen`, and `CB2_TitleScreenRun`. |
| Existing save load | PASS | Deterministic debugger input selected `CONTINUE` from the existing disposable save and reached `CB2_Overworld`. |
| Initial overworld frames | PASS | The ROM ran for approximately ten additional seconds and `gMain.callback2` remained `CB2_Overworld` (`0x080565B5`). |
| Sound initialization contract | PASS | CFRU's intended `0xC500` to `0xCC00` Direct Sound replacement remains at ROM offset `0x1DD0C8`; the adjacent loop count remains four. At the title callback, `SOUND_INFO_PTR` referenced `gSoundInfo`, whose identifier and all four `gMPlayInfo` identifiers were the valid `0x68736D53`. |
| Legendary defeat recovery | STATIC PASS | The seven intended `setflag` to `clearflag` event-command swaps compile at their locked offsets without changing vanilla layout. Runtime flee/defeat/capture/blackout cases remain in the manual procedure below. |

This is targeted regression evidence, not completion of the full manual feature matrix.

## 2026-09-05 cleanup verification

Current artifact SHA-256: `2cd43618ea7a8bf9eeca2783e60df9b64710c23792a498b8cfd0b0ca17437358`. Earlier `ce5522…` observations above remain attached to that earlier artifact.

| Check | Result | Evidence |
|---|---|---|
| Isolated rebuilds | PASS | Two workspaces with different discovery order reproduced all stage and payload digests. One used clean upstream clones, rebuilt agbcc/grit, locally extracted compiler libraries, and no copied ROM build outputs. |
| Incremental rebuild | PASS | Rebuilding after the isolated source corrections retained the exact current CFRU hash. |
| Ordering/padding regression tests | PASS | Missing, duplicate, unlisted, and unsafe inputs fail; normalization preserves compressed bytes, handles tail widths, and leaves malformed streams unchanged. |
| Audit check modes | PASS | Good/missing/stale/altered ledgers tested; 2,685 availability records including duplicates preserved; full audit suite changed no tracked file content. |
| New game | PASS (automated emulator) | mGBA 0.10.5 SDL with dummy video/audio and HLE BIOS reached the title callback, then a new game reached `CB2_Overworld` after 5,302 injected-input frames. |
| In-game save and restart | PASS (automated emulator) | Start-menu Save produced a 131,088-byte container; a separate mGBA process selected Continue and reached `CB2_Overworld`. |
| Continued execution | PASS (automated emulator) | 600 additional frames retained `gMain.callback2 = 0x080565B5`. Debugger logs contained no illegal-opcode, invalid-address, bad-memory, crash, or unimplemented-memory entries. |

Input was injected into `gMain` key fields immediately after `ReadKeys` at `0x0800041E`; gameplay/save routines were not bypassed. The ROM and logs were kept in a disposable directory. These checks do not establish visual/audio quality, full save compatibility, or completion of the manual feature matrix. Owner observations stay in `TEST_OBSERVATIONS.md`.

## Current candidate procedure

Candidate ROM: `.upstream/cfru/test.gba`, verified with `python3 scripts/verify_build_artifact.py cfru .upstream/cfru/test.gba`. Copy it to a separate ignored location for manual testing; verify any older private copy before using it.

Use a separate save and existing CFRU debug facilities. After every representative mutation, save in-game, close mGBA completely, reopen it, and load the save.

### Evolution Guide

1. Open a normal Pokédex detail page and press `SELECT`; confirm the Guide opens without changing species.
2. Check a no-evolution species for `NO KNOWN EVOLUTIONS`.
3. Check linear and three-stage families for immediate pre-evolution and immediate forward routes only.
4. Check Eevee branching with `UP/DOWN` and `LEFT/RIGHT`; confirm three routes per page and `PAGE X/Y`.
5. Check Link Cable, held-item, friendship/day/night, known-move, and a compound route such as Kingambit.
6. Press `A` on a route and then return; confirm the original guide, page, and selection are restored.
7. Toggle `SELECT`/`B` at least 20 times; confirm no missing windows, corrupt tiles, frozen input, or stale text.

### Form Lab, routes, and storage

8. In Cinnabar Pokémon Lab Research Room, speak to scientist object slot 1 and cancel the party picker; confirm no mutation.
9. Select an Egg and unsupported species; confirm a clear refusal and no mutation.
10. Test Rotom, Deoxys, Furfrou, Magearna, and Zarude changes and reversals. Confirm nickname, OT/IDs, personality, nature, IVs/EVs, level/EXP, moves/PP/PP Ups, friendship, held item, Ball, ribbons, and shiny state remain unchanged.
11. Deposit each representative changed form, save/reload, withdraw it, and verify form, stats, icon, summary, and metadata.
12. Test Arceus, Silvally, Genesect, Ogerpon, Reveal Glass, Gracidea, Prison Bottle, DNA Splicers, Necrozma fusers, and Calyrex reins where safely available.
13. Confirm regional, encounter/evolution-locked, battle-only, unsupported, and fusion-only forms never appear in Form Lab.
14. After Hall of Fame, select **FORM PRESERVE**. Encounter one regional and one encounter-locked cosmetic form and confirm neither was offered by Form Lab.

### Legendary outcomes

15. In Seven Island Pokémon Center 1F, speak to object slot 2; test Generation I–IX menus and all cancel/back paths.
16. Before League completion, verify `LOCKED`; verify Lugia, Ho-Oh, and Deoxys also require their research/ticket flags.
17. For one encounter from multiple generations, flee and re-enter/reselect it; confirm availability.
18. Defeat it and re-enter; confirm it respawns. Repeat once with player blackout.
19. Save/restart before capture; verify the encounter and unrelated completion flags.
20. Capture it, re-enter/query the coordinator, and confirm `COMPLETED` with no respawn.
21. Trade away or release the captured Legendary; confirm completion remains permanent.

### Habitat and repeated persistence

22. After Hall of Fame, press `SELECT` in DexNav; verify all nine migration groups and that cancellation preserves the old choice.
23. Choose a group with `UP/DOWN` and `A`; verify normal map entries remain and a migration species is searchable.
24. Save, restart mGBA, and confirm the migration persists on another map.
25. Repeat save/load cycles with a party form, boxed form, highest internal form ID, active Pokédex data, migration selection, and several Legendary completion flags.

## Boundary matrix

| Boundary ID | Creation/wild/Pokédex/party/summary | Sprite/cry | Moves/evolution | Save/reload | Status |
|---|---|---|---|---|---|
| Bulbasaur | pending | pending | pending | pending | manual |
| Mew | pending | pending | pending | pending | manual |
| Celebi | pending | pending | pending | pending | manual |
| Deoxys | pending | pending | pending | pending | manual |
| Arceus | pending | pending | pending | pending | manual |
| Genesect | pending | pending | pending | pending | manual |
| Volcanion | pending | pending | pending | pending | manual |
| Zeraora | pending | pending | pending | pending | manual |
| Eternatus | pending | pending | pending | pending | manual |
| Enamorus | pending | pending | pending | pending | manual |
| Pecharunt | pending | pending | pending | pending | manual |
| Highest internal form ID | pending | pending | pending | pending | manual |

The final pass must also cover every evolution method/item, encounter type, regional pool, starter/fossil, recoverable one-capture Legendary, blackout/healing path, repeated save/load, and a new game after an old save.

## Result template

```text
Test:
Expected:
Actual:
Pass/Fail:
Screenshot or notes:
```
