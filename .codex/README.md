# Project-local Codex workflow

`AGENTS.md` is the authoritative repository guidance. This directory contains thin, repeatable entrypoints so Codex can inspect, audit, and build the project without rediscovering its workflow.

## Actions

- `status.sh` — read-only worktree and milestone snapshot.
- `run-audits.sh` — deterministic source/data checks; does not build a ROM.
- `build-and-verify.sh` — full vanilla → DPE → CFRU build and ROM verification.
- `environments/environment.toml` — action metadata for Codex integrations that support project-local environment actions.

All binaries and intermediate outputs remain ignored. Manual gameplay verification is owner-led and follows `docs/TESTING.md`.
