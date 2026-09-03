# FireRed Gen 9

This is an orchestration and patch project for a binary-expanded Pokémon FireRed build. It is not a `pret/pokefirered` decompilation. A matching vanilla FireRed ROM is built locally from source, then passed through pinned DPE Gen 9 and CFRU Expansion builds.

Complete ROMs, saves, BIOS files, emulator states, and unlicensed standalone assets must never be committed or distributed. The eventual distributable is a legal patch plus source changes, build scripts, locks, documentation, and credits.

Development is gated by milestones. M0–M4 and the compiled portions of M5–M8 are implemented and automated-tested. Current coverage is 1,025/1,025 National Pokédex species, 883 evolution edges, 442 canonical alternate-form IDs (439 runtime-bound and three intentionally unsafe placeholders), 26 Legendary/Mythical hub entries, and nine optional DexNav migration groups. Edwin's mGBA checklist and public asset-provenance review are the remaining release gates.

## Documentation

- [`docs/STATUS.md`](docs/STATUS.md) — current milestone state, build evidence, and remaining gates.
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — build pipeline, upstream pins, offsets, and reproducibility.
- [`docs/FEATURES.md`](docs/FEATURES.md) — implemented gameplay systems and their runtime contracts.
- [`docs/TESTING.md`](docs/TESTING.md) — automated evidence and the owner-led mGBA checklist.
- [`docs/FULL_PLAYTHROUGH_TEST_PLAN.md`](docs/FULL_PLAYTHROUGH_TEST_PLAN.md) — chronological intensive full-playthrough test checklist.
- [`docs/TEST_DASHBOARD_SETUP.md`](docs/TEST_DASHBOARD_SETUP.md) — shared testing dashboard deployment and access setup.
- [`docs/HISTORY.md`](docs/HISTORY.md) — consolidated M1–M4 execution history and retired document map.
- [`CREDITS.md`](CREDITS.md) — upstream attribution and asset-release boundaries.
