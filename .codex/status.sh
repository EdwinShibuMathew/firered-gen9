#!/usr/bin/env bash
set -euo pipefail

root_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$root_dir"

printf '%s\n' '== FireRed Gen 9 status =='
git status --short
printf '\n%s\n' '== Change summary =='
git diff --stat
printf '\n%s\n' '== Canonical docs =='
for file in docs/STATUS.md docs/ARCHITECTURE.md docs/FEATURES.md docs/TESTING.md docs/HISTORY.md; do
    if [[ -f "$file" ]]; then printf 'PASS %s\n' "$file"; else printf 'MISSING %s\n' "$file"; fi
done
printf '\n%s\n' '== Latest commit =='
git log -1 --oneline --decorate
