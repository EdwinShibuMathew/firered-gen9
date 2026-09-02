# M8 Release and Final Testing — Progress

**Status:** `[~]` reproducible build hygiene is automated; release and manual QA remain

- `scripts/audit_release.py` checks lock metadata, required ledgers/docs (including architecture and credits), and the no-ROM/save/BIOS/emulator-state policy.
- `docs/TEST_MATRIX.md` defines the required boundary-ID and workflow rows.
- An ignored local BPS test candidate has been generated at `build/private/firered-gen9-m8-test-candidate.bps` and round-trip verified. It remains a private test candidate until M5 manual verification passes.
- Clean input SHA-1: `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc`.
- Candidate ROM SHA-256: `7853001d128494c4cea3919808227531abf0ac97fb325d22413c1dee4a81ce79`.
- Candidate BPS SHA-256: `227052d6a67942050c96ce1c09a678f1b77e7791c63098d8992d8525d4869462`.
- Rebuild command: `python3 scripts/create_bps_patch.py base-rom/PokemonFireRedVersion.gba build/private/firered-gen9-m5-test.gba build/private/firered-gen9-m8-test-candidate.bps --source-sha1 41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc`.
- `CREDITS.md` and `docs/GEN9_ARCHITECTURE.md` are still finalization tasks listed by the roadmap; they are not being represented as complete.
- Manual emulator testing remains pending by owner request; no gameplay row is inferred from source compilation.
