#!/usr/bin/env bash
set -euo pipefail

root_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$root_dir"
run() {
    printf '\n== %s ==\n' "$*"
    "$@"
}

run python3 scripts/apply_overlays.py --check
run python3 scripts/generate_gen9_reserve.py --check
run python3 scripts/audit_availability.py --require-complete
run python3 scripts/audit_m4_repeatable.py
run python3 scripts/audit_legendary_encounters.py
run python3 scripts/audit_forms.py --require-complete
run python3 scripts/generate_form_routes.py --check
run python3 scripts/audit_form_routes.py
run python3 scripts/audit_m5_runtime_integrity.py
run python3 scripts/generate_evolution_encyclopedia.py --check
run python3 scripts/audit_m5_content.py --require-audited
run python3 scripts/audit_m6_starter.py
run python3 scripts/generate_m7_habitat.py --check
run python3 scripts/audit_m7.py
run python3 scripts/generate_test_dashboard_data.py --check
run python3 scripts/audit_documentation.py
run python3 scripts/audit_release.py
