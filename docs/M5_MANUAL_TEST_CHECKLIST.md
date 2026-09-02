# M5 Manual Test Checklist

Candidate ROM: `build/private/firered-gen9-m5-test.gba`

Use a separate test save and the existing CFRU debug facilities. After every representative mutation, save in-game, close mGBA completely, reopen it, and reload the save.

1. Open a normal Pokédex detail page and press `SELECT`; confirm the Evolution Guide opens without changing the selected species.
2. Test a no-evolution species and confirm `NO KNOWN EVOLUTIONS`.
3. Test a linear and three-stage family; confirm immediate pre-evolution and immediate forward routes only.
4. Test Eevee; use `UP/DOWN` and `LEFT/RIGHT`, confirm three routes per page and correct `PAGE X/Y` behavior.
5. Check Link Cable, held-item, friendship/day/night, known-move, and a compound/special route such as Kingambit.
6. Press `A` on a route, confirm the target detail entry opens, then press `B`; confirm the original guide, page, and selection return.
7. Repeatedly toggle `SELECT` and `B` at least 20 times; confirm no missing windows, corrupted tiles, frozen input, or stale text.
8. In Cinnabar Pokémon Lab Research Room, speak to scientist object slot 1 and cancel at the party picker; confirm no mutation.
9. Select an Egg and an unsupported species; confirm a clear refusal and no mutation.
10. Test Rotom, Deoxys, Furfrou, Magearna, and Zarude changes; revisit to cycle/reverse and confirm nickname, OT/IDs, personality, nature, IVs/EVs, level/EXP, moves/PP, friendship, held item, Ball, ribbons, and shiny state remain unchanged.
11. Deposit each representative changed form in the PC, save/reload, withdraw it, and verify species/form, stats, icon, summary, and metadata.
12. Test existing held/key-item handlers for Arceus, Silvally, Genesect, Ogerpon, Reveal Glass, Gracidea, Prison Bottle, DNA Splicers, Necrozma fusers, and Calyrex reins where safely available.
13. Confirm regional, encounter/evolution-locked, battle-only, and unsupported/fusion-only forms never appear in the Form Lab service.
14. Select **FORM PRESERVE** at the same scientist after the Hall of Fame. Encounter one regional and one encounter-locked cosmetic form; confirm neither was offered as a Form Lab mutation.
15. In Seven Island Pokémon Center 1F, speak to sailor object slot 2; confirm the Generation I–IX coordinator menus and every cancel/back path.
16. Before League completion, confirm the hub reports `LOCKED`; for Lugia/Ho-Oh/Deoxys confirm missing ticket research flags report `LOCKED`.
17. For one encounter in each generation, flee and re-enter or reselect it at the hub; confirm it remains available.
18. Defeat the encounter and re-enter; confirm it respawns. Repeat once with player blackout.
19. Save and restart before capture; confirm the encounter and unrelated completion flags remain correct.
20. Capture the encounter, re-enter its map, and query the coordinator; confirm it reports `COMPLETED` and never respawns.
21. Trade away or release a captured Legendary; confirm its completion flag remains permanent and the encounter does not respawn.
22. Open DexNav after the Hall of Fame and press `SELECT`; confirm all nine migration groups appear and cancellation preserves the old selection.
23. Choose a migration with `UP/DOWN` and `A`; confirm DexNav rebuilds, keeps normal map entries, and adds a searchable migration species.
24. Save, fully restart mGBA, and confirm the migration selection persists in a different map.
25. Repeat save/load cycles with a party form, boxed form, high internal form ID, active Pokédex data, migration selection, and several Legendary completion flags.

Result template:

```text
Test:
Expected:
Actual:
Pass/Fail:
Screenshot or notes:
```
