#!/usr/bin/env bash
set -euo pipefail

root_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$root_dir"

: "${BUILD_JOBS:=4}"
printf 'Building FireRed Gen 9 with BUILD_JOBS=%s\n' "$BUILD_JOBS"
BUILD_JOBS="$BUILD_JOBS" ./scripts/build_pipeline.sh

candidate="$root_dir/.upstream/cfru/test.gba"
if [[ -f "$candidate" ]]; then
    python3 scripts/verify_rom.py "$candidate"
else
    printf 'ERROR: expected candidate ROM was not produced: %s\n' "$candidate" >&2
    exit 1
fi
