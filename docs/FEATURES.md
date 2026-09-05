# Implemented Gameplay Systems

All systems below are compiled and structurally audited. Items explicitly marked manual remain subject to the owner-led cases in `TESTING.md`.

## Evolution and Evolution Guide

The authoritative DPE table contains 883 records: 592 acquisition evolutions and 291 Mega/Gigantamax battle transformations. All acquisition edges have an offline-capable route. The project provides a reusable ₽3,000 Link Cable in Celadon, direct held-item trade replacements, a Shiny Stone route for Alolan Raichu, runtime support for Gholdengo and both Maushold outcomes, all 52 required evolution items, and repaired learnsets for five missing move prerequisites.

The Evolution Guide is a second page in `Task_DexScreen_ShowMonPage`, not a Start-menu application. Overlay `patches/cfru/0011-pokedex-evolution-guide.patch` hooks the detail input state at `0x08104418`; the renderer reads `gEvolutionTable` directly. `data/evolution_encyclopedia.csv` is an audit view of the same ledger, not a second manually maintained database.

Controls:

- `SELECT` toggles detail and Guide; `B` or `SELECT` returns to details.
- `UP/DOWN` selects a route; `LEFT/RIGHT` paginates three routes per page.
- `A` opens the target entry; returning restores the originating species, page, and route.

All 43 DPE evolution-method enum values have explicit formatters. Conditions use a bounded 128-byte buffer and pixel-width wrapping. Species/route bounds, icon fallback, sprite/palette cleanup, branching routes, pre-evolutions, unseen target names, `PAGE X/Y`, and `NO KNOWN EVOLUTIONS` are implemented. Visual layout and repeated navigation remain manual checks.

## Forms and Cinnabar research services

`data/form_routes.csv` is authoritative for 442 canonical alternate-form IDs. The audit classifies every form; 439 resolve to compiled battle/item/fusion handlers, generated Form Lab data, or generated Form Preserve encounters. `SHADOW_WARRIOR`, Zygarde Cell, and Zygarde Core are intentionally unsupported because they are unsafe internal placeholders.

`TryChangeMonForm` is the validated mutation boundary. It checks the source and target before mutation, preserves Pokémon identity and metadata through supported accessors, recalculates derived stats, and clamps current HP after a maximum-HP change.

Cinnabar Pokémon Lab Research Room scientist object slot 1 provides:

- **FORM LAB** — safe, reversible, non-consuming transformations for 19 routes across Rotom, Deoxys, Furfrou, Magearna, and Zarude. It uses the stock party picker and scrolling menu and excludes Eggs, no-op targets, regional, encounter-locked, battle-only, unsafe fusion, and unsupported forms.
- **FORM PRESERVE** — postgame wild acquisition for all 203 regional or encounter/evolution-locked forms. Those permanent forms never appear as generic laboratory mutations.

Existing CFRU handlers cover Gracidea, Reveal Glass, Prison Bottle, Oricorio nectars, DNA Splicers, Necrozma fusers, Calyrex reins, held-item forms, and battle-only forms. Fusion guards correct full-party defusion bounds and the Necrozma/Lunala duplication condition. Party/PC persistence and representative metadata preservation remain manual checks.

## Legendary and Mythical Research Hub

Seven Island Pokémon Center 1F object slot 2 hosts a Generation I–IX coordinator generated from `data/legendary_encounters.csv`. It exposes 26 entries as `LOCKED`, `AVAILABLE`, or `COMPLETED`, provides prerequisite hints, transports seven entries to existing static maps, and runs the other nineteen through a shared capture-only battle handler.

Each encounter separates unlock, active/reset, and permanent capture-completion state. Flee, defeat, or blackout leaves the encounter recoverable through re-entry or coordinator recalibration. Capture alone sets permanent completion; trading or releasing the captured Pokémon never creates a replacement. There are no daily resets, repeatable captures, Mystery Gift requirements, or second-version dependencies.

## Contrary starter

The preserved Contrary checkout was inspected at commit `2d57c43dc562a42b81dce5e2e754f0b175c44d89` and was not modified. DPE/CFRU overlays give Charmander, Charmeleon, and Charizard Contrary in every ability slot; apply the custom stats and Fire/Dragon Charizard typing; give Charmander Overheat, Psycho Boost, Thunderbolt, and Ice Beam at level 1; and configure Oak's level-5 gift with Timid nature, 31 IVs, 6 HP/252 Sp. Atk/252 Speed EVs, full HP, and Shell Bell.

## Habitat Scanner

After Hall of Fame completion, `SELECT` in DexNav opens a nine-region selector. `UP/DOWN` chooses Kanto, Johto, Hoenn, Sinnoh, Unova, Kalos, Alola, Galar/Hisui, or Paldea; `A` saves the choice and rebuilds the scanner; cancel preserves the old selection.

`scripts/generate_m7_habitat.py` derives nine 16-species pools from the National Dex mapping and excludes Legendary contract entries. Variable `VAR_M7_MIGRATION_GROUP` (`0x515A`) persists the selected group. Migration species augment DexNav only; normal map encounter headers and map identity remain unchanged.

## Field-speed defaults

CFRU overlay `0020` returns speed 2 for ordinary walking and initializes new saves with fast text plus the bike and surf turbo flags. These save defaults are initialized for a new game; this overlay does not retroactively set the flags in existing saves. Movement and menu behavior remain subject to the manual playthrough checklist.
