# M8 Release and Final Testing — Progress

**Status:** `[~]` private release candidate built; manual QA and public asset review remain

- `scripts/audit_release.py` checks lock metadata, required ledgers/docs (including architecture and credits), and the no-ROM/save/BIOS/emulator-state policy.
- `docs/TEST_MATRIX.md` defines the required boundary-ID and workflow rows.
- An ignored local BPS test candidate has been generated at `build/private/firered-gen9-m8-test-candidate.bps` and round-trip verified. It remains a private test candidate until M5 manual verification passes.
- Clean input SHA-1: `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc`.
- Candidate ROM SHA-256: `e2d4da0696ac9b0cf6ba74ff3c117e6b3b55baa48f43f6839717f191340ec80d`.
- Candidate BPS SHA-256: `ab4cc33cc061f8e5e8e763baa202ca38cecda53e566e2840da906ab9c0388167`.
- Rebuild command: `python3 scripts/create_bps_patch.py base-rom/PokemonFireRedVersion.gba build/private/firered-gen9-m5-test.gba build/private/firered-gen9-m8-test-candidate.bps --source-sha1 41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc`.
- `CREDITS.md`, architecture, pins, patch instructions, and the completion plan are present and release-audited.
- Manual emulator testing remains pending by owner request; no gameplay row is inferred from source compilation.
