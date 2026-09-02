# FireRed Gen 9

This is an orchestration and patch project for a binary-expanded Pokémon FireRed build. It is not a `pret/pokefirered` decompilation. A matching vanilla FireRed ROM is built locally from source, then passed through pinned DPE Gen 9 and CFRU Expansion builds.

Complete ROMs, saves, BIOS files, emulator states, and unlicensed standalone assets must never be committed or distributed. The eventual distributable is a legal patch plus source changes, build scripts, locks, documentation, and credits.

Development is gated by milestones. M0–M4 and the compiled portions of M5–M8 are implemented and automated-tested. Current coverage is 1,025/1,025 National Pokédex species, 883 evolution edges, 442 canonical alternate-form IDs (439 runtime-bound and three intentionally unsafe placeholders), 26 Legendary/Mythical hub entries, and nine optional DexNav migration groups. The private ROM and round-trip-verified BPS candidate remain ignored. Edwin's mGBA checklist and public asset-provenance review are the remaining release gates; see `docs/DEVELOPMENT_COMPLETION_PLAN.md`.
