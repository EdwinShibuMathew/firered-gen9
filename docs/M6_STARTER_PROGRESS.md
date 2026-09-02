# M6 Custom Starter Port — Progress Report

**Status:** Automated port complete; owner-led runtime validation deferred  
**Last updated:** 2026-09-02

The preserved `pokefirered-contrary` repository was inspected at commit `2d57c43dc562a42b81dce5e2e754f0b175c44d89`. Its starter overhaul has been ported through isolated DPE/CFRU overlays.

Implemented:

- Charmander, Charmeleon, and Charizard use Contrary in all ability slots.
- Their custom base stats and Fire/Dragon Charizard typing are represented in DPE source.
- Charmander’s level-1 learnset includes Overheat, Psycho Boost, Thunderbolt, and Ice Beam.
- Oak’s level-5 Charmander gift receives Timid nature, 31 IVs, 6 HP EVs, 252 Sp. Atk EVs, 252 Speed EVs, full HP, and Shell Bell.
- CFRU already contains the Contrary battle/stat-stage implementation required by the source repository’s behavior.

The port is reproducible through `patches/dpe/0002-contrary-charizard-starter-data.patch` and `patches/cfru/0007-contrary-charizard-starter-gift.patch`. Build and source checks pass. Manual battle, evolution, save/reload, and Contrary visual checks remain deferred to the owner’s QA pass.

`scripts/audit_m6_starter.py` verifies both overlay files against their SHA-256 entries in `build-lock.json`.
