#!/usr/bin/env bash
set -eu

project_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
tool_path="$project_root/.tools/arm-gcc/usr/bin:$project_root/.tools/bin:$project_root/.upstream/pret/tools/wav2agb:$project_root/.upstream/pret/tools/mid2agb:$PATH"
compiler_path="$project_root/.tools/compiler-path"
newlib_path="$project_root/.tools/arm-gcc/usr/include/newlib"
freeimage_path="$project_root/.tools/freeimage/usr/lib/x86_64-linux-gnu"

python3 "$project_root/scripts/apply_overlays.py" --check
python3 "$project_root/scripts/generate_gen9_reserve.py" --check
python3 "$project_root/scripts/audit_availability.py" --require-complete
python3 "$project_root/scripts/audit_m4_repeatable.py"
python3 "$project_root/scripts/audit_legendary_encounters.py"
python3 "$project_root/scripts/audit_forms.py" --require-complete
python3 "$project_root/scripts/generate_form_routes.py" --check
python3 "$project_root/scripts/audit_form_routes.py"
python3 "$project_root/scripts/audit_m5_runtime_integrity.py"
python3 "$project_root/scripts/generate_evolution_encyclopedia.py" --check
python3 "$project_root/scripts/audit_m5_content.py" --require-audited
python3 "$project_root/scripts/audit_m6_starter.py"
python3 "$project_root/scripts/generate_m7_habitat.py" --check
python3 "$project_root/scripts/audit_m7.py"
python3 "$project_root/scripts/audit_documentation.py"
python3 "$project_root/scripts/audit_release.py"

PATH="$tool_path" make -C "$project_root/.upstream/pret" -j"${BUILD_JOBS:-2}"
cp "$project_root/.upstream/pret/pokefirered.gba" "$project_root/.upstream/dpe/BPRE0.gba"

(
    cd "$project_root/.upstream/dpe"
    PATH="$tool_path" COMPILER_PATH="$compiler_path" LD_LIBRARY_PATH="$freeimage_path" \
        python3 scripts/make.py
)

cp "$project_root/.upstream/dpe/test.gba" "$project_root/.upstream/cfru/BPRE0.gba"
(
    cd "$project_root/.upstream/cfru"
    PATH="$tool_path" COMPILER_PATH="$compiler_path" C_INCLUDE_PATH="$newlib_path" \
        LD_LIBRARY_PATH="$freeimage_path" python3 scripts/make.py
)

python3 "$project_root/scripts/verify_rom.py" "$project_root/.upstream/cfru/test.gba"
