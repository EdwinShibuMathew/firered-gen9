# Full Playthrough Testing Checklist

Use this checklist while playing `test-release-rom/firered-gen9-test.gba` from the beginning through the postgame. It is written so that each checkbox is one small test.

You do not need technical knowledge. If something looks wrong, freezes, shows broken text, or behaves differently from the **Pass if** description, record it as a failure.

## Before you start

Fill this in once:

```text
Tester name or initials:
Date started:
mGBA version (Help > About):
Computer and operating system:
Controller or keyboard:
ROM SHA-256: ce5522a7229b6f46930f313d679c98567becc0036d3231f80f9f2ff68602ddc1
```

### How to mark a test

- Leave `[ ]` when you have not done the test.
- Change `[ ]` to `[x]` when it passes.
- For a failure, leave it unchecked and add `FAIL:` plus a short explanation below it.
- Write `SKIP:` if you could not perform the test, and explain why.
- Take a screenshot whenever something is wrong or confusing.

Example:

```text
- [ ] B07 Enter the Pokémon Center. Pass if the inside appears normally.
  FAIL: The screen stayed black. Screenshot: B07-black-screen.png
```

## How saving works

There are two useful kinds of saves. Use both.

### Normal game save

This is the save that must be tested.

1. Press `START` in the game.
2. Select **SAVE**.
3. Select **YES**.
4. Wait until the game says it has saved.

To test that it worked:

1. Close mGBA completely.
2. Open `firered-gen9-test.gba` again.
3. Select **CONTINUE**.
4. Check that you return to the correct place with the correct party and progress.

### Checkpoint file

A checkpoint lets you return to an earlier part of the playthrough without starting again. It does not replace the normal game save test.

1. Make a normal game save first.
2. In mGBA, choose **File > Save State File**.
3. Save it inside a folder named `checkpoints` next to the ROM.
4. Use the checkpoint name shown in this document.

To return to one later, choose **File > Load State File** and select it. Never load a checkpoint while testing whether **CONTINUE** works; close and reopen mGBA for that test.

## Quick checks to repeat everywhere

Use these checks whenever you enter a new route, building, cave, town, or island.

- [ ] `R01` Walk in all four directions. **Pass if:** movement and collision feel normal.
- [ ] `R02` Enter and leave each available door or cave. **Pass if:** the correct area loads without a black screen.
- [ ] `R03` Talk to nearby people and read signs. **Pass if:** text is readable and closes normally.
- [ ] `R04` Listen to the music and sound effects. **Pass if:** audio plays without loud noise, silence, or getting stuck.
- [ ] `R05` Open and close the menu. **Pass if:** graphics and controls remain normal.
- [ ] `R06` Start at least one trainer or wild battle. **Pass if:** battle starts and returns to the map normally.
- [ ] `R07` Pick up visible and hidden items you find. **Pass if:** the item appears in the correct Bag pocket.
- [ ] `R08` Save after important story events. **Pass if:** **CONTINUE** restores the new progress.

## 1. Start a new game

- [ ] `A01` Open the ROM in mGBA. **Pass if:** the title screen appears and does not freeze.
- [ ] `A02` Listen at the title screen. **Pass if:** music and button sounds play normally.
- [ ] `A03` Select **NEW GAME**. **Pass if:** Professor Oak's introduction begins.
- [ ] `A04` Choose the player appearance. **Pass if:** the chosen appearance is used in the game.
- [ ] `A05` Enter the player and rival names. **Pass if:** both names appear correctly later.
- [ ] `A06` Finish the bedroom introduction. **Pass if:** you can walk downstairs and leave the house.
- [ ] `A07` Open the Bag, party, settings, and save screens. **Pass if:** each screen opens and closes normally.
- [ ] `A08` Make a normal game save and restart mGBA. **Pass if:** **CONTINUE** returns you to the same place.
- [ ] `A09` Create checkpoint `01-new-game-start.ss1`.

## 2. Starter and first rival battle

- [ ] `B01` Enter Oak's lab and inspect the available starters. **Pass if:** the choices and text display normally.
- [ ] `B02` Cancel the starter choice once. **Pass if:** cancellation does not give a Pokémon or freeze the game.
- [ ] `B03` Choose the starter you want for the playthrough. **Pass if:** the correct Pokémon joins the party.
- [ ] `B04` Open the starter's summary. **Pass if:** name, level, type, ability, stats, moves, sprite, and held item are visible.
- [ ] `B05` If Charmander was selected, check its ability. **Pass if:** it shows **Contrary**.
- [ ] `B06` If Charmander was selected, check its moves. **Pass if:** Overheat, Psycho Boost, Thunderbolt, and Ice Beam are present.
- [ ] `B07` Complete the rival battle. **Pass if:** attacks, animations, cries, HP, experience, and the result work normally.
- [ ] `B08` Make a normal game save and restart mGBA. **Pass if:** the starter and rival progress remain saved.
- [ ] `B09` Create checkpoint `02-starter-and-rival.ss1`.

## 3. First wild Pokémon and Pokédex

- [ ] `C01` Receive the Pokédex. **Pass if:** it appears in the menu.
- [ ] `C02` Encounter a wild Pokémon in grass. **Pass if:** its name, level, sprite, cry, and battle work normally.
- [ ] `C03` Catch a wild Pokémon. **Pass if:** it joins the party or goes to the PC.
- [ ] `C04` Open the caught Pokémon's summary. **Pass if:** its information and sprite are correct and readable.
- [ ] `C05` Open its Pokédex entry. **Pass if:** it is marked as caught and its entry displays normally.
- [ ] `C06` Deposit the caught Pokémon in the PC. **Pass if:** it disappears from the party and appears in the chosen box.
- [ ] `C07` Withdraw the same Pokémon. **Pass if:** it returns with the same level, moves, stats, name, and held item.
- [ ] `C08` Make a normal game save and restart mGBA. **Pass if:** the caught Pokémon and Pokédex entry remain saved.
- [ ] `C09` Create checkpoint `03-first-capture.ss1`.

## 4. Normal story playthrough

Complete the main FireRed story normally. Repeat the quick checks `R01`–`R08` in every new area.

- [ ] `D01` Defeat Brock. **Pass if:** the badge, reward, and story progress are saved.
- [ ] `D02` Create checkpoint `04-brock.ss1`.
- [ ] `D03` Travel through Mt. Moon. **Pass if:** maps, ladders, battles, fossils, and exits work normally.
- [ ] `D04` Defeat Misty. **Pass if:** the badge, reward, and story progress are saved.
- [ ] `D05` Complete the S.S. Anne story. **Pass if:** trainers, rooms, rival battle, captain, and ship exit work.
- [ ] `D06` Defeat Lt. Surge. **Pass if:** the badge, reward, and story progress are saved.
- [ ] `D07` Complete Rock Tunnel. **Pass if:** lighting, encounters, ladders, and exits work normally.
- [ ] `D08` Complete the Celadon and Rocket Hideout events. **Pass if:** lifts, switches, battles, items, and story flags work.
- [ ] `D09` Buy and use the reusable Link Cable in Celadon. **Pass if:** it costs ₽3,000 and remains after use.
- [ ] `D10` Defeat Erika. **Pass if:** the badge, reward, and story progress are saved.
- [ ] `D11` Complete Pokémon Tower. **Pass if:** rival, ghosts, stairs, healing, and story events work.
- [ ] `D12` Complete Silph Co. **Pass if:** lifts, warp tiles, rival, boss battle, gift, and story events work.
- [ ] `D13` Defeat Koga. **Pass if:** the badge, reward, and story progress are saved.
- [ ] `D14` Defeat Sabrina. **Pass if:** the badge, reward, and story progress are saved.
- [ ] `D15` Complete Cinnabar Island and Pokémon Mansion. **Pass if:** doors, switches, encounters, and key item progress work.
- [ ] `D16` Defeat Blaine. **Pass if:** the badge, reward, and story progress are saved.
- [ ] `D17` Defeat Giovanni. **Pass if:** the eighth badge and final story progress are saved.
- [ ] `D18` Complete Victory Road. **Pass if:** strength puzzles, encounters, items, and exit work normally.
- [ ] `D19` Create checkpoint `05-before-elite-four.ss1`.

## 5. General battle and item checks

These can be completed whenever the required situation occurs.

- [ ] `E01` Let a party Pokémon faint. **Pass if:** battle continues or ends correctly.
- [ ] `E02` Lose a battle on purpose once. **Pass if:** you return to the correct healing location without losing story progress.
- [ ] `E03` Run from a wild battle. **Pass if:** the battle ends and the map returns normally.
- [ ] `E04` Use a healing item in battle. **Pass if:** the correct Pokémon recovers the correct amount.
- [ ] `E05` Use a status-healing item. **Pass if:** the status is removed.
- [ ] `E06` Use a TM or move-teaching item. **Pass if:** the selected Pokémon learns the move and menus remain correct.
- [ ] `E07` Give and remove a held item. **Pass if:** the correct item and Pokémon are updated.
- [ ] `E08` Fill the party with six Pokémon. **Pass if:** later captures go to the PC safely.
- [ ] `E09` Change party order. **Pass if:** the new order remains after a normal save and restart.

## 6. Evolution checks

You do not need to test all 883 evolution records. Test each kind you naturally reach, plus the examples below.

- [ ] `F01` Evolve a Pokémon by level. **Pass if:** the correct species, sprite, cry, stats, and Pokédex entry appear.
- [ ] `F02` Evolve a Pokémon with a stone. **Pass if:** the item is used and the correct evolution appears.
- [ ] `F03` Evolve a Pokémon using the Link Cable. **Pass if:** evolution works and the Link Cable remains in the Bag.
- [ ] `F04` Evolve a Pokémon using a required held item. **Pass if:** the correct evolution occurs.
- [ ] `F05` Evolve a Pokémon through friendship. **Pass if:** it evolves only after the required friendship condition.
- [ ] `F06` Evolve one Pokémon with a time-of-day condition. **Pass if:** it follows the displayed condition.
- [ ] `F07` Evolve one Pokémon that must know a move. **Pass if:** it follows the displayed condition.
- [ ] `F08` Test one branching family such as Eevee. **Pass if:** the chosen condition produces the chosen branch.
- [ ] `F09` Cancel an evolution by pressing `B`. **Pass if:** the Pokémon remains unchanged and the game continues.
- [ ] `F10` Save and restart after an evolution. **Pass if:** the evolved Pokémon and Pokédex entry remain correct.

## 7. Pokédex Evolution Guide

- [ ] `G01` Open a Pokémon's Pokédex details and press `SELECT`. **Pass if:** the Evolution Guide opens.
- [ ] `G02` Press `SELECT` again. **Pass if:** normal details return for the same Pokémon.
- [ ] `G03` Open a Pokémon with no evolution. **Pass if:** it says **NO KNOWN EVOLUTIONS**.
- [ ] `G04` Open Eevee or another branching family. **Pass if:** all routes can be viewed.
- [ ] `G05` Press `UP` and `DOWN`. **Pass if:** the selected route changes.
- [ ] `G06` Press `LEFT` and `RIGHT` on a family with many routes. **Pass if:** pages change and show `PAGE X/Y`.
- [ ] `G07` Press `A` on an evolution route. **Pass if:** the target Pokémon's entry opens.
- [ ] `G08` Return from the target entry. **Pass if:** the original Pokémon, page, and route return.
- [ ] `G09` View a route with long text. **Pass if:** the text wraps and remains readable.
- [ ] `G10` Open and close the Guide 20 times. **Pass if:** it never freezes or shows broken graphics or stale text.

## 8. Cinnabar Form Lab

- [ ] `H01` Speak to the Form Lab scientist in Cinnabar Pokémon Lab Research Room. **Pass if:** the Form Lab menu opens.
- [ ] `H02` Cancel the party selection. **Pass if:** no Pokémon changes.
- [ ] `H03` Try to select an Egg. **Pass if:** it is refused and remains unchanged.
- [ ] `H04` Try an unsupported Pokémon. **Pass if:** a clear refusal appears and nothing changes.
- [ ] `H05` Change one supported Pokémon's form. **Pass if:** the chosen form appears correctly.
- [ ] `H06` Change that Pokémon back. **Pass if:** the original form returns.
- [ ] `H07` Test a Rotom form change. **Pass if:** its chosen appliance form appears correctly.
- [ ] `H08` Test a Deoxys form change. **Pass if:** its chosen form and stats appear correctly.
- [ ] `H09` Test a Furfrou form change. **Pass if:** its chosen trim appears correctly.
- [ ] `H10` Test Magearna or Zarude if available. **Pass if:** the chosen supported form appears correctly.
- [ ] `H11` Check the changed Pokémon's summary. **Pass if:** nickname, level, moves, item, nature, ability, and ownership did not unexpectedly change.
- [ ] `H12` Deposit the changed Pokémon in the PC and withdraw it. **Pass if:** its form and information remain correct.
- [ ] `H13` Make a normal game save and restart mGBA. **Pass if:** the form remains correct.
- [ ] `H14` Create checkpoint `06-form-lab.ss1`.

## 9. Elite Four and Champion

- [ ] `I01` Defeat each Elite Four member. **Pass if:** every battle starts and ends normally.
- [ ] `I02` Defeat the Champion. **Pass if:** the ending and Hall of Fame sequence complete.
- [ ] `I03` Watch the credits. **Pass if:** graphics, music, text, and the return to the title screen work.
- [ ] `I04` Select **CONTINUE** after the credits. **Pass if:** the postgame save loads correctly.
- [ ] `I05` Check the Hall of Fame record. **Pass if:** the winning party is displayed correctly.
- [ ] `I06` Create checkpoint `07-champion.ss1`.

## 10. Sevii Islands and postgame access

- [ ] `J01` Use the ferry to visit each available island. **Pass if:** destinations and return trips work normally.
- [ ] `J02` Enter Pokémon Centers, caves, routes, and special buildings on the islands. **Pass if:** maps load correctly.
- [ ] `J03` Complete available island story events. **Pass if:** progress remains after a normal save and restart.
- [ ] `J04` Visit the Form Lab after becoming Champion. **Pass if:** **FORM PRESERVE** is available.
- [ ] `J05` Use Form Preserve to meet one regional form. **Pass if:** the correct wild form appears and can be caught.
- [ ] `J06` Use Form Preserve to meet one special cosmetic or encounter-only form. **Pass if:** the correct wild form appears and can be caught.
- [ ] `J07` Check both caught forms in the party and PC. **Pass if:** their form, sprite, icon, moves, and information remain correct.
- [ ] `J08` Make a normal game save and restart mGBA. **Pass if:** both forms remain correct.
- [ ] `J09` Create checkpoint `08-postgame-forms.ss1`.

## 11. Legendary and Mythical Research Hub

- [ ] `K01` Speak to the coordinator in Seven Island Pokémon Center 1F. **Pass if:** the Research Hub menu opens.
- [ ] `K02` View every generation menu. **Pass if:** entries, status labels, and hints are readable.
- [ ] `K03` Back out of every menu once. **Pass if:** cancellation returns to the previous menu or the game.
- [ ] `K04` Select an available Legendary encounter. **Pass if:** the correct encounter or destination opens.
- [ ] `K05` Run from one Legendary. **Pass if:** it can be selected or encountered again.
- [ ] `K06` Defeat one Legendary without catching it. **Pass if:** it can be selected or encountered again.
- [ ] `K07` Lose to one Legendary. **Pass if:** it remains available after healing.
- [ ] `K08` Save before catching a Legendary and restart mGBA. **Pass if:** it is still available.
- [ ] `K09` Catch the Legendary. **Pass if:** the coordinator changes its status to **COMPLETED**.
- [ ] `K10` Try to encounter the same Legendary again. **Pass if:** it does not return.
- [ ] `K11` Put the captured Legendary in the PC and restart mGBA. **Pass if:** it remains stored and the entry remains **COMPLETED**.
- [ ] `K12` Create checkpoint `09-legendary-hub.ss1`.

Do not release the captured Legendary unless you are willing to restore checkpoint `09-legendary-hub.ss1` afterward.

## 12. DexNav migration groups

- [ ] `L01` Open DexNav after becoming Champion and press `SELECT`. **Pass if:** a region selector opens.
- [ ] `L02` Scroll through the selector. **Pass if:** Kanto, Johto, Hoenn, Sinnoh, Unova, Kalos, Alola, Galar/Hisui, and Paldea appear.
- [ ] `L03` Cancel without choosing. **Pass if:** the previous choice remains unchanged.
- [ ] `L04` Choose one region and press `A`. **Pass if:** the choice is accepted and DexNav refreshes.
- [ ] `L05` Search for a migration Pokémon. **Pass if:** it can be found through DexNav.
- [ ] `L06` Walk in the same area without DexNav. **Pass if:** the normal wild Pokémon still appear.
- [ ] `L07` Make a normal game save and restart mGBA. **Pass if:** the selected migration region remains active.
- [ ] `L08` Change to a second region. **Pass if:** the new choice replaces the old one only after confirmation.
- [ ] `L09` Create checkpoint `10-dexnav.ss1`.

## 13. Final checks

- [ ] `M01` Load each checkpoint file once. **Pass if:** every checkpoint opens at the expected part of the game.
- [ ] `M02` Load the latest normal save using **CONTINUE**. **Pass if:** the final party, PC, badges, Pokédex, forms, and postgame progress are present.
- [ ] `M03` Review the checklist for unchecked items. **Pass if:** every unchecked item has a `FAIL` or `SKIP` explanation.
- [ ] `M04` Review screenshots and notes. **Pass if:** every failure has enough information for another person to reproduce it.
- [ ] `M05` Play for at least 30 minutes after the final postgame test. **Pass if:** there are no new crashes, freezes, corrupted graphics, or broken audio.

## Bug report form

Copy this block for every failure:

```text
Test ID:
Result: FAIL
Checkpoint used:
Location in the game:
Pokémon or item involved:
What I did:
What I expected:
What happened instead:
Can I make it happen again? Yes / No / Not tried
Screenshot or video filename:
Extra notes:
```

## Playthrough summary

Fill this in after finishing:

```text
Date finished:
Final play time:
Number of passed tests:
Number of failed tests:
Number of skipped tests:
Any crash or freeze? Yes / No
Any lost or corrupted save? Yes / No
Any story progress blocked? Yes / No
Overall result: PASS / PASS WITH MINOR ISSUES / FAIL
```
