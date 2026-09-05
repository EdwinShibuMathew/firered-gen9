# Contributing

Read [status](docs/STATUS.md), [Linux setup](docs/DEVELOPMENT_SETUP.md),
[architecture](docs/ARCHITECTURE.md), [runtime contracts](docs/FEATURES.md),
and [testing](docs/TESTING.md), in that order. Commands and their write effects
are listed in the [script reference](docs/SCRIPTS.md).

## Ownership and vocabulary

- **Upstream:** an ignored, pinned dependency checkout under `.upstream/`.
- **Overlay:** a tracked patch applied to an upstream checkout in lockfile order.
- **Lock:** `build-lock.json`, recording upstream revisions, overlay digests,
  insertion offsets, and expected artifact hashes.
- **Ordering manifest:** a reviewed input sequence in `data/build_order/`;
  filesystem discovery order is not a source of truth.
- **Ledger:** generated CSV evidence. Change its source and generator deliberately,
  then regenerate; do not conceal stale data by editing the output alone.
- **Artifact:** a private local build result, not distributable repository source.

The repository owns `patches/`, `scripts/`, `data/`, the lock, and documentation.
Do not make permanent fixes only inside ignored upstream checkouts. Preserve
upstream pins, gameplay behavior, binary layout, and locked hashes during cleanup.
Never update expected hashes just to make a failed build pass. Keep ROMs, saves,
BIOS files, toolchains, contact sheets, and emulator states out of Git.

## One focused change at a time

1. Run `.codex/status.sh` and inspect `git diff`. Identify and preserve existing work.
2. Describe the problem and the smallest intended change. Check ownership above.
3. Make one focused change, then run its focused checks below.
4. Review `git diff` and `git diff --check`, including generated outputs.
5. Run the required broader checks. Stop on failure; fix this step before starting another.
6. Submit a focused review. Keep unrelated work in separate changes. Revert only
   your own change if recovery is necessary; never reset the whole dirty worktree.

## Verification by change

| Change | Focused verification | Broader gate |
|---|---|---|
| Documentation | Documentation audit; check relative links and artifact claims | Release audit and `git diff --check` |
| Generated ledger | Generator twice, then `--check`; inspect record changes | Full audit suite; generation must be intentional |
| Overlay | Apply/check in a pinned isolated checkout; update overlay SHA-256 in lock | Full audits, build and artifact verification; relevant emulator checks |
| Ordering manifest or padding helper | Unit tests including missing/duplicate/unexpected inputs | Two clean differently created workspaces plus incremental builds; unchanged locked hashes |
| Dashboard checklist | Generate both `test-dashboard/checklist.json` and `supabase/seed.sql`, then `--check` | Documentation audit; review both outputs together |
| Dashboard application | Follow dashboard setup's local checks | Keep administration/deployment separate; do not deploy as part of source cleanup |

For overlays, develop against the pinned checkout and export only the intended
diff as an additional tracked patch. Append it without reordering existing
overlays; record its digest in the lock. Test application from clean pinned
sources, not just the already modified checkout. See architecture for manifest
ownership and the deliberate input-addition procedure.

Typical prepared-workspace gate:

```sh
python3 -m unittest discover -s tests -v
.codex/run-audits.sh
BUILD_JOBS=4 .codex/build-and-verify.sh
python3 scripts/audit_release.py
git diff --check
```

Build only with the documented upstreams and tools. Audit passes do not establish
runtime behavior. Record manual results with the exact ROM hash in testing docs.

## Review notes

Include the problem, ownership/source changed, intended behavior change (or
“none”), commands and outcomes, artifact hash when applicable, remaining manual
checks, and recovery scope. Never include private artifacts in review attachments.
For a generated file, name its source and reproduction command.

## Fellow-programmer onboarding acceptance

The owner explicitly waived this cleanup's human walkthrough and requested removal
of its progress checkpoint; see [history](docs/HISTORY.md). No human onboarding pass
is claimed. For future onboarding reviews, a programmer other than the implementing
assistant should follow the Linux guide in a fresh workspace and record the date,
platform, commands/results, final CFRU hash, and confusing or missing instructions
in the review notes. This is separate from automated reproduction and emulator smoke tests.

During that walkthrough, trace these three examples:

1. Overlay: lock entry → patch → pinned upstream → stage artifact verification.
2. Availability ledger: upstream acquisition data → audit generation → CSV →
   non-writing `--check` (use a scratch output for generation experiments).
3. Dashboard: playthrough checklist → generator → both JSON and SQL outputs →
   generation check; no deployment is required.

Cleanup acceptance does not imply public-release readiness.
