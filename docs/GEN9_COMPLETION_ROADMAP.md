# FireRed Gen 9 Completion Roadmap

**Reconciled:** 2026-09-02

Status markers: `[x]` automated/implemented, `[~]` implemented but awaiting manual verification, `[ ]` outstanding.

## Milestone state

- M0 `[x]` — verified clean FireRed input and pinned build pipeline.
- M1 `[x]` — DPE/CFRU engine baseline built and boot-tested; historical optional desktop checks remain recorded in M1 reports.
- M2 `[x]` — 1,025 National Dex species pass the data audit; asset provenance is separately tracked.
- M3 `[~]` — 883 offline evolution edges compile and audit; Edwin's representative evolution/save QA remains.
- M4 `[x]` — deterministic availability is `1025/1025`; static Legendary captures are once per save, with flee/defeat/blackout recovery.
- M5 `[~]` — runtime implementation is complete and automated-tested: Evolution Guide, generated Form Lab, generated Form Preserve, safe dedicated routes, fusion guards, and the 26-entry Legendary Hub. Manual mGBA verification remains.
- M6 `[~]` — Contrary Charizard starter data and Oak gift compile through pinned overlays; manual battle/save QA remains.
- M7 `[~]` — nine generated postgame DexNav migration groups compile; manual scanner/save QA remains.
- M8 `[~]` — clean private ROM and round-trip BPS candidate built; manual matrix and public asset review remain.

## Implemented checkpoints

- `28fa112` — compiled M5 gameplay integrations.
- `bde8b97` — canonical 442-form inventory, generated Form Lab, complete Evolution Guide formatters.
- `2ad2d11` — postgame permanent-form encounter bindings.
- `fd23112` — postgame DexNav habitat migration selector.

## Completion gates

1. `[x]` Preserve upstream pins, insertion offsets, overlay hashes, and ignored binary policy.
2. `[x]` Pass species, availability, evolution, form, Legendary, M5, M6, M7, provenance, and release-hygiene audits.
3. `[x]` Build the 32 MiB candidate from clean SHA-1 `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc`.
4. `[x]` Produce and round-trip the ignored BPS test candidate.
5. `[ ]` Edwin executes `docs/M5_MANUAL_TEST_CHECKLIST.md` and `docs/TEST_MATRIX.md` in mGBA.
6. `[ ]` Correct any concrete failures reported by manual testing.
7. `[ ]` Review asset contact sheets and resolve or explicitly exclude public-release provenance blockers.
8. `[ ]` Mark manually verified rows and publish only a legal patch plus source/documentation.

There are no known unimplemented gameplay-code tasks. The only unbound form IDs are the deliberately unsafe `SHADOW_WARRIOR`, Zygarde Cell, and Zygarde Core internal placeholders. See `docs/DEVELOPMENT_COMPLETION_PLAN.md` for the execution record.
