# Development Completion Plan

**Last reconciled:** 2026-09-02  
**Code status:** development-complete, automated-tested, manual gameplay verification pending

This is the execution record for completing the repository. Each phase is tied to compiled code, an audit, and a local checkpoint rather than status-only documentation.

## Completed execution phases

1. `[x]` Preserve the pinned pret → DPE → CFRU pipeline and legal artifact boundaries.
2. `[x]` Validate all 1,025 National Pokédex species and achieve deterministic `1025/1025` availability.
3. `[x]` Implement offline evolution methods, prerequisite moves/items, reusable Link Cable behavior, and the 883-edge ledger.
4. `[x]` Implement one-capture Legendary recovery semantics and the 26-entry Generation I–IX Research Hub.
5. `[x]` Integrate the Pokédex Evolution Guide with all 43 ledger method values handled, bounded buffers, icon cleanup, pagination, and long-text wrapping.
6. `[x]` Replace heuristic form discovery with the canonical 442-ID DPE-to-National-Dex inventory.
7. `[x]` Bind 439 safe forms to compiled battle/item/fusion handlers, generated Form Lab tables, or generated permanent-form encounters. Exclude the three unsafe internal placeholders.
8. `[x]` Implement the Cinnabar Form Lab and postgame Form Preserve through the existing scientist object and scrolling-menu system.
9. `[x]` Implement the optional M7 postgame DexNav selector with nine generated migration groups and persistent variable `0x515A`.
10. `[x]` Build and round-trip a private M8 BPS candidate from the verified clean FireRed input.

## Remaining gates

1. `[ ]` Edwin runs `docs/M5_MANUAL_TEST_CHECKLIST.md` in mGBA and records actual results.
2. `[ ]` Fix any runtime defect found by that testing; no known code defect is currently open.
3. `[ ]` Visually review the ignored asset contact sheets. Unknown or suspicious asset provenance remains a public-release gate, not a private-build blocker.
4. `[ ]` After manual passes, update milestone states from `IMPLEMENTED_UNVERIFIED` to `MANUALLY_VERIFIED` and regenerate the final public BPS patch.

## Current build evidence

- Clean input SHA-1: `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc`
- Candidate ROM SHA-256: `e2d4da0696ac9b0cf6ba74ff3c117e6b3b55baa48f43f6839717f191340ec80d`
- Candidate BPS SHA-256: `ab4cc33cc061f8e5e8e763baa202ca38cecda53e566e2840da906ab9c0388167`
- Private ROM: `build/private/firered-gen9-m5-test.gba`
- Private patch: `build/private/firered-gen9-m8-test-candidate.bps`

Complete ROMs, saves, BIOS files, emulator states, contact sheets, and private artifacts remain ignored and must not be committed.
