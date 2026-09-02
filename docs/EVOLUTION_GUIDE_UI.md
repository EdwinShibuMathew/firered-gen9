# Evolution Guide UI

## Runtime integration

The Evolution Guide is a second page of the existing Pokédex detail task (`Task_DexScreen_ShowMonPage`), not a Start-menu application. CFRU overlay `patches/cfru/0011-pokedex-evolution-guide.patch` hooks the detail input state at `0x08104418`; its runtime renderer reads `gEvolutionTable` directly, while `data/evolution_encyclopedia.csv` remains the generated audit view of the same ledger.

Overlay `patches/cfru/0016-complete-evolution-guide-formatters.patch` explicitly handles all 43 values in DPE's evolution-method enum, corrects the reusable Link Cable label, and adds pixel-width wrapping while retaining the 128-byte bounded text buffer.

Controls are `SELECT` to toggle detail/Guide, `B` or `SELECT` to return, `UP/DOWN` to select a route, `LEFT/RIGHT` to paginate, and `A` to open the target entry. Three routes fit per page; routes beyond that show `PAGE X/Y`. Species names and conditions are rendered even when unseen, while icons use the normal engine fallback.

## State transition contract

`DETAIL -> GUIDE` preserves the selected species and category cursor. `GUIDE -> DETAIL` restores the normal detail page. `GUIDE -> TARGET` stores the source species and selected route; returning from the target restores `GUIDE` rather than resetting the Pokédex list.

## Current implementation status

`IMPLEMENTED_UNVERIFIED`: the hook, route scan, condition formatter, three-route pagination, source/target icon sprites, target navigation, and originating-guide return state compile and insert in the candidate ROM. The page reuses Pokédex BG0/window/font state, validates species and route bounds, uses the engine's missing-icon fallback, and destroys route sprites/palettes before pagination or exit. Manual mGBA testing is required for repeated open/close, long text, icon placement, and target return behavior.
