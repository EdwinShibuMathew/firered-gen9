#!/usr/bin/env python3
"""Verify and apply the tracked upstream patches declared in build-lock.json."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOCK_PATH = ROOT / "build-lock.json"
UPSTREAM_DIRS = {
    "pret_pokefirered": ROOT / ".upstream/pret",
    "dpe_gen9": ROOT / ".upstream/dpe",
    "cfru_expansion": ROOT / ".upstream/cfru",
}


def git_apply(repo: Path, patch: Path, *options: str) -> bool:
    result = subprocess.run(
        ["git", "apply", *options, str(patch)], cwd=repo,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False,
    )
    return result.returncode == 0


def touched_paths(patch: Path) -> set[str]:
    paths: set[str] = set()
    for line in patch.read_text(encoding="utf-8").splitlines():
        if line.startswith("+++ b/"):
            paths.add(line[6:])
        elif line.startswith("--- a/"):
            paths.add(line[6:])
    return paths


def validate_clean_chains(overlays: list[tuple[str, dict, Path, Path]]) -> bool:
    """Prove every overlay applies in declared order to a clean upstream."""
    valid = True
    for upstream, source in UPSTREAM_DIRS.items():
        selected = [(name, patch) for name, cfg, repo, patch in overlays if cfg.get("upstream", "cfru_expansion") == upstream]
        if not selected:
            continue
        with tempfile.TemporaryDirectory(prefix=f"overlay-{upstream}-") as temp:
            clone = Path(temp) / "repo"
            cloned = subprocess.run(
                ["git", "-c", "advice.detachedHead=false", "clone", "--quiet", "--shared", str(source), str(clone)],
                check=False,
            ).returncode == 0
            if not cloned:
                print(f"ERROR   {upstream}: could not create clean validation clone")
                valid = False
                continue
            for name, patch in selected:
                if not git_apply(clone, patch, "--check") or not git_apply(clone, patch):
                    print(f"ERROR   {name}: does not apply in clean declared order")
                    valid = False
                    break
    return valid


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify state without applying pending patches")
    args = parser.parse_args()
    lock = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
    failed = False
    overlays: list[tuple[str, dict, Path, Path]] = []
    for name, overlay in lock.get("compatibility_overlays", {}).items():
        patch = ROOT / overlay["path"]
        repo = UPSTREAM_DIRS.get(overlay.get("upstream", "cfru_expansion"))
        if repo is not None:
            overlays.append((name, overlay, repo, patch))
    clean_chains_valid = validate_clean_chains(overlays)
    failed |= not clean_chains_valid
    later_paths: dict[str, set[str]] = {}
    accumulated: dict[str, set[str]] = {}
    for name, overlay, _repo, patch in reversed(overlays):
        upstream = overlay.get("upstream", "cfru_expansion")
        later_paths[name] = set(accumulated.get(upstream, set()))
        accumulated.setdefault(upstream, set()).update(touched_paths(patch) if patch.is_file() else set())

    for name, overlay, repo, patch in overlays:
        if repo is None or not repo.is_dir() or not patch.is_file():
            print(f"ERROR   {name}: missing repository or patch")
            failed = True
            continue
        actual_hash = hashlib.sha256(patch.read_bytes()).hexdigest()
        if actual_hash != overlay["sha256"]:
            print(f"ERROR   {name}: SHA-256 mismatch")
            failed = True
            continue
        if git_apply(repo, patch, "--check"):
            if args.check:
                print(f"PENDING {name}")
                failed = True
            elif git_apply(repo, patch):
                print(f"APPLIED {name}")
            else:
                print(f"ERROR   {name}: application failed")
                failed = True
        elif git_apply(repo, patch, "--reverse", "--check"):
            print(f"OK      {name}: already applied")
        elif clean_chains_valid and touched_paths(patch) & later_paths.get(name, set()):
            print(f"OK      {name}: applied and extended by a later overlay")
        else:
            print(f"ERROR   {name}: upstream does not match patch context")
            failed = True
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
