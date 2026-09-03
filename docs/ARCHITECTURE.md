# Architecture and Reproducible Build

## Pipeline

This repository orchestrates a pinned three-stage binary build:

1. `pret/pokefirered` supplies the canonical 16 MiB FireRed build.
2. DPE expands species, forms, moves, graphics, and data tables at offset `0x1600000`.
3. CFRU adds runtime mechanics and is inserted at offset `0x1000000`.

Tracked overlays under `patches/` are applied to ignored upstream checkouts by `scripts/apply_overlays.py`. `build-lock.json` records upstream commits, offsets, overlay hashes, and output checksums. Generated ledgers under `data/` are audit inputs, not ROM assets.

M3 owns offline evolution routes, M4 National Dex availability, M5 permanent forms/quests/encyclopedia UI, M6 the preserved Contrary starter port, M7 optional DexNav migrations, and M8 release packaging and QA.

M5's authoritative 442-form contract generates the Form Lab family table and Form Preserve encounter table. M7 independently generates nine compact National Dex migration pools and injects one representative into DexNav without changing wild encounter headers. Expanded-save variable `0x515A` stores only the selected M7 group.

## Exact upstream pins

| Component | Commit | Offset |
|---|---|---|
| `pret/pokefirered` | `c75f352304d529f6ba92d4f74b9cf8b5c3810788` | n/a |
| `grilokapu/Dynamic-Pokemon-Expansion-Gen-9` | `376849ea0887131689a36cc51846c573f7735f22` | `0x1600000` |
| `Shiny-Miner/CFRU-expansion` (`Experiments`) | `dade256a1db1fa036fedd9f8566cb48de405e97a` | `0x1000000` |

CFRU's follower sprite insertion reported `0x900000`. This generated value is retained as build metadata. CFRU recommends the pinned grilokapu DPE fork and warns against Leon's ROM base.

## Reproduction

The clean pret build must produce FireRed SHA-1 `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc`. In each ignored expansion checkout, `BPRE0.gba` is the preceding verified artifact and is never tracked.

The upstream build command is:

```sh
make -j2
```

DPE and CFRU use their respective pinned checkouts with:

```sh
PATH="<arm-gcc>/usr/bin:<toolchain>/usr/bin:<grit>:<wav2agb>:<mid2agb>:$PATH" \
COMPILER_PATH="<arm-assembler-shim>" \
LD_LIBRARY_PATH="<local-freeimage>/usr/lib/x86_64-linux-gnu" \
python3 scripts/make.py
```

Python 3.14.4 succeeded. CFRU required Pillow 12.3.0 and the tracked `-ffreestanding` compatibility overlay, which prevents GCC 14 from replacing CFRU's private string loop with an unresolved hosted-libc `strlen`; it does not change gameplay data.

Run `BUILD_JOBS=4 ./scripts/build_pipeline.sh` from the project root to verify locks and reproduce the vanilla → DPE → CFRU result. M3 overlays add the Celadon Link Cable listing, reusable Link Cable behavior, Alolan Raichu's Shiny Stone route, and missing Gholdengo/Maushold runtime methods. CFRU overlays `0015`–`0018` generate canonical Form Lab data, complete Evolution Guide formatters, bind Form Preserve encounters, and integrate the DexNav migration selector.

## Compatibility and artifact policy

DPE documents save-block and TM/tutor expansion prerequisites when used without Complete FireRed Upgrade. Here DPE is immediately followed by pinned CFRU Expansion, which supplies those engine expansions. No separate prepatched ROM or Leon ROM base is used.

The combined output is a reproducible 32 MiB ROM. ROMs, saves, BIOS files, emulator states, local toolchains, contact sheets, and private patches remain ignored. Public distribution is limited to legal patches, source changes, scripts, locks, documentation, and credits.
