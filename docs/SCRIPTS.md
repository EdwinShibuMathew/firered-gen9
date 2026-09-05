# Script reference

Run from the repository root. See [Linux setup](DEVELOPMENT_SETUP.md) for the
prepared environment and [contribution rules](../CONTRIBUTING.md) for gates.
“Prepared” means pinned upstream sources with overlays applied; builds additionally
need the local toolchain. Check commands do not regenerate tracked outputs.

## Entry points and build tools

| Command | Prerequisites | Write effects |
|---|---|---|
| `.codex/status.sh` | Source checkout | None |
| `.codex/run-audits.sh` | Prepared sources, Python | Checks only; temporary validation/cache files may be created |
| `.codex/build-and-verify.sh` | Prepared sources and toolchain | Ignored build/ROM outputs |
| `python3 scripts/apply_overlays.py --check` | Pinned upstreams | Temporary validation checkouts; no application to working upstreams |
| `python3 scripts/apply_overlays.py` | Pinned upstreams | Applies tracked overlays to ignored upstreams |
| `python3 scripts/verify_build_artifact.py cfru ROM` | Private ROM and lock | None; also accepts `vanilla` and `dpe` |
| `python3 scripts/verify_rom.py ROM --sha1 HASH` | Private ROM | None; without `--sha1` only reports digest |

`build_pipeline.sh` implements the build wrapper. `ordered_build_inputs.py` is
the non-writing manifest helper; `grit_lz_padding.py` normalizes ignored generated
DPE sprite assembly during builds.

## Ledgers and generators

The following commands support `--check`. Omit it only for deliberate generation.
Use `python3 scripts/NAME.py` with the flags shown.

| Script/flags | Inputs | Output when generating |
|---|---|---|
| `audit_availability.py --require-complete --check` | Prepared upstream acquisition sources | `data/availability.csv` (or `--csv` target) |
| `audit_forms.py --require-complete --check` | Prepared form sources | `data/forms.csv` |
| `generate_gen9_reserve.py --check` | Acquisition/evolution data and prepared sources | `data/gen9_reserve.csv`, `data/gen9_reserve_tables.inc` |
| `generate_form_routes.py --check` | Form data and prepared sources | `data/form_routes.csv`, upstream `include/generated/m5_form_routes.h` |
| `generate_evolution_encyclopedia.py --check` | `data/evolution_mapping.csv` | `data/evolution_encyclopedia.csv` |
| `generate_m7_habitat.py --check` | Habitat data and prepared sources | `data/habitat_migration_groups.csv`, upstream `include/generated/m7_habitat_groups.h` |
| `generate_test_dashboard_data.py --check` | `docs/FULL_PLAYTHROUGH_TEST_PLAN.md` | `test-dashboard/checklist.json` AND `supabase/seed.sql` |

Generated upstream headers must remain reproducible through the tracked overlay
workflow. Do not rely on an unrecorded local header change.

## Focused audits

Source-only: `audit_documentation.py` (needs full Git history) and
`audit_release.py` (hygiene only, not release certification).

Prepared-source, non-writing checks: `audit_species.py`,
`audit_m4_repeatable.py`, `audit_legendary_encounters.py`,
`audit_form_routes.py`, `audit_m5_runtime_integrity.py`,
`audit_m5_content.py --require-audited`, `audit_m6_starter.py`, and `audit_m7.py`.
`audit_species.py --rom ROM` optionally inspects a private artifact.

`m3_evolution_audit.py --require-complete` and
`m3_prerequisite_audit.py --require-complete` are read-only unless given `--csv`.
`m3_offline_evolution.py` is a compatibility entry point to the evolution audit.

`python3 -m unittest discover -s tests -v` checks ordering, padding, and audit
failure behavior. Upstream-dependent integration tests explicitly skip in a
source-only checkout; skips are not build acceptance.

## Deliberate generation and private utilities

- `generate_asset_provenance.py` overwrites `data/asset_provenance.csv` with
  unresolved/default review metadata. It has no check mode: do not rerun casually
  over human provenance reviews.
- `generate_m5_contact_sheets.py` needs Pillow/assets and writes private ignored
  `build/m5_contact_sheets/` images.
- `create_bps_patch.py SOURCE TARGET OUTPUT --source-sha1 HASH` creates a patch;
  use a private ignored output path. Release approval remains separate.

## Historical helpers: not current acceptance gates

`m2_asset_audit.py` and `m2_comprehensive_audit.py` are legacy heuristic reports.
The latter's successful exit is not proof of complete asset coverage.

`m1_automated_test.py` writes the historical root `m1_test_output.txt` by default
and may create save backups. `m1_completion_report.py` generates a report with
historical assumptions; it cannot certify fresh manual results.
`m1_interactive_test.py` launches a GUI and has legacy route instructions.
`m1_save_completer.py` modifies saves using approximate offsets: do not use it on
real progress or to manufacture acceptance evidence. Use [testing](TESTING.md)
for the current exact-artifact procedure instead.
