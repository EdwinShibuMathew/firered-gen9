# FireRed Gen 9 Architecture

The build is a pinned three-stage pipeline:

1. `pret/pokefirered` supplies the canonical 16 MiB FireRed build.
2. DPE expands species, forms, moves, graphics, and data tables at offset `0x1600000`.
3. CFRU adds runtime mechanics and is inserted at offset `0x1000000`.

Tracked overlays under `patches/` are applied to ignored upstream checkouts by `scripts/apply_overlays.py`. `build-lock.json` records upstream commits, offsets, overlay hashes, and output checksums. Generated ledgers under `data/` are source-audit inputs, not ROM assets.

Milestone boundaries are deliberate: M3 audits offline evolution routes; M4 proves National Dex availability; M5 owns permanent forms, quests, and encyclopedia UI; M6 owns the preserved Contrary starter port; M7 is optional DexNav migration work; M8 owns release packaging and manual QA.

M5's authoritative 442-form contract generates both the Form Lab family table and the Form Preserve encounter table. M7 independently generates nine compact National Dex migration pools and injects one selected representative into DexNav without mutating the underlying wild encounter headers. Expanded save variable `0x515A` stores only the M7 group selection.

ROMs, saves, BIOS files, emulator states, and local toolchains remain ignored and are never distributed by this repository.
