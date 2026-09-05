"""Replay reviewed build-input order without relying on filesystem traversal."""
from __future__ import annotations

from glob import glob as discover
import json
import os
from pathlib import Path


def ordered_glob(pathname: str, *, manifest: Path, recursive: bool = False) -> list[str]:
    """Check the discovered set, then return paths in the manifest's link order."""
    data = json.loads(manifest.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1:
        raise ValueError(f"Unsupported build-order schema: {manifest}")
    pattern = os.path.normpath(pathname)
    try:
        expected = data["groups"][pattern]
    except KeyError:
        raise ValueError(f"Unlisted build-input pattern {pattern!r}; update {manifest}") from None
    if not isinstance(expected, list) or any(
        not isinstance(path, str) or Path(path).is_absolute()
        or ".." in Path(path).parts or os.path.normpath(path) != path
        for path in expected
    ):
        raise ValueError(f"Invalid relative paths for {pattern!r} in {manifest}")
    if len(expected) != len(set(expected)):
        raise ValueError(f"Duplicate build inputs for {pattern!r} in {manifest}")
    actual = discover(pathname, recursive=recursive)
    paths = {os.path.normpath(path): path for path in actual}
    if len(paths) != len(actual):
        raise ValueError(f"Duplicate discovered build inputs for {pattern!r}")
    missing = sorted(set(expected) - paths.keys())
    unexpected = sorted(paths.keys() - set(expected))
    if missing or unexpected:
        raise ValueError(
            f"Build-input mismatch for {pattern!r}: missing={missing}, unexpected={unexpected}. "
            f"Restore the pinned inputs or review {manifest}; do not accept new ROM hashes automatically."
        )
    return [paths[path] for path in expected]
