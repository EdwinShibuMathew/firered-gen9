# FireRed Gen 9 repository guidance

## Project shape

This repository is an orchestration and patch project, not a `pret/pokefirered` decompilation. A clean vanilla FireRed build is passed through the pinned DPE and CFRU checkouts. The tracked source of truth is in `patches/`, `scripts/`, `data/`, `build-lock.json`, and `docs/`.

Read `docs/STATUS.md` for current work, `docs/ARCHITECTURE.md` for the pipeline, `docs/FEATURES.md` for runtime contracts, and `docs/TESTING.md` for verification requirements. Historical claims belong in `docs/HISTORY.md`.

The shared testing dashboard is generated from `docs/FULL_PLAYTHROUGH_TEST_PLAN.md`. After changing checklist items, run `python3 scripts/generate_test_dashboard_data.py` and commit both generated outputs.

## Working rules

- Inspect relevant files and `git status` before editing.
- Use `apply_patch` for tracked-file edits; preserve unrelated user changes.
- Never commit or distribute ROMs, saves, BIOS files, emulator states, local toolchains, contact sheets, or private build outputs.
- Treat `.upstream/`, `.tools/`, `.venv/`, `build/`, `dist/`, and `base-rom/` as local/ignored inputs unless the user explicitly requests otherwise.
- Do not change pinned upstream checkouts when a tracked overlay is the appropriate fix.
- Prefer `rg` for search and the smallest relevant audit before a full build.
- Do not claim runtime behavior from static audits; manual mGBA results belong in `docs/TESTING.md`.

## Verification commands

```sh
.codex/status.sh
.codex/run-audits.sh
BUILD_JOBS=4 .codex/build-and-verify.sh
```

Run the build only when upstream checkouts and local toolchains are available. Before handoff, run `git diff --check`, the focused audit for the changed subsystem, and `python3 scripts/audit_release.py` when release-facing files changed.
