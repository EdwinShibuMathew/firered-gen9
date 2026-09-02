# Upstream pins

The build uses exact commits rather than moving branches. See `build-lock.json` for machine-readable pins, offsets, and artifact hashes.

The generated vanilla ROM is used only as a local legal build input. Tracked overlays are applied first, then DPE runs and CFRU runs. CFRU's current README recommends the pinned grilokapu DPE fork and warns against Leon's ROM base.

## Exact pins and insertion offsets

| Component | Commit | Offset |
|---|---|---|
| `pret/pokefirered` | `c75f352304d529f6ba92d4f74b9cf8b5c3810788` | n/a |
| `grilokapu/Dynamic-Pokemon-Expansion-Gen-9` | `376849ea0887131689a36cc51846c573f7735f22` | `0x1600000` |
| `Shiny-Miner/CFRU-expansion` (`Experiments`) | `dade256a1db1fa036fedd9f8566cb48de405e97a` | `0x1000000` |

CFRU's follower sprite insertion reported `0x900000`. This generated value is recorded here rather than treated as disposable offset metadata.

## Commands used for M0/M1

The local tool directories are ignored because they are reconstructed dependencies. In each expansion checkout, `BPRE0.gba` is the preceding verified artifact and is never tracked.

```sh
make -j2
```

The clean pret build produced the documented FireRed SHA-1 `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc`.

For DPE and then CFRU, from the respective pinned checkout:

```sh
PATH="<arm-gcc>/usr/bin:<toolchain>/usr/bin:<grit>:<wav2agb>:<mid2agb>:$PATH" \
COMPILER_PATH="<arm-assembler-shim>" \
LD_LIBRARY_PATH="<local-freeimage>/usr/lib/x86_64-linux-gnu" \
python3 scripts/make.py
```

Python 3.14.4 succeeded; no obsolete global Python was installed. CFRU required Pillow 12.3.0 and the tracked `-ffreestanding` compatibility overlay for modern GCC. The overlay prevents GCC 14 from replacing CFRU's private string loop with an unresolved hosted-libc `strlen` call; it does not change game data or behavior.

Run `scripts/build_pipeline.sh` from the project root to verify all locked overlays and reproduce the current vanilla → DPE → CFRU artifact. The M3 overlays add the Celadon Link Cable listing, reusable Link Cable behavior, Alolan Raichu's Shiny Stone route, and missing Gholdengo/Maushold runtime methods.

## Installation-order note

DPE's README says a save-block expansion and TM/tutor expansion must precede DPE when it is used without Complete FireRed Upgrade. In this baseline, DPE is immediately followed by the pinned CFRU Expansion/Complete FireRed Upgrade, which supplies those engine expansions. No separate prepatched ROM or Leon ROM base was used. This interpretation still requires the remaining M1 save/data smoke tests before it is accepted as the engine baseline.
