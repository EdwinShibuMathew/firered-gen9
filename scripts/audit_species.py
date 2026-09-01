#!/usr/bin/env python3
"""
M2 Species Audit Script

Static audit of CFRU species metadata to validate the source-level registry and
ensure the ROM source is aligned with the expected National Dex coverage.

This is intentionally source-driven: the vanilla ROM and generated build artifacts
are legal local inputs only, and the CFRU source tree exposes the species registry,
valid type IDs, and known form lists needed for M2 planning and validation.
"""

import argparse
import json
import re
import sys
from pathlib import Path


SRC_ROOT = Path(__file__).resolve().parents[1]
SPECIES_HEADER = SRC_ROOT / ".upstream/cfru/include/constants/species.h"
POKEMON_HEADER = SRC_ROOT / ".upstream/cfru/include/pokemon.h"
SPECIES_JSON = SRC_ROOT / ".upstream/cfru/assembly/data/species_tables.json"
ROM_PATH_DEFAULT = SRC_ROOT / ".upstream/cfru/test.gba"


class SpeciesAudit:
    """Audit CFRU species metadata and registry integrity."""

    FORM_SUFFIXES = (
        "_A", "_G", "_H", "_N", "_MEGA", "_PRIMAL", "_ORIGIN", "_THERIAN",
        "_CROWNED", "_ICE_RIDER", "_SHADOW_RIDER", "_DADA", "_ETERNAMAX",
        "_RED", "_BLUE", "_ORANGE", "_YELLOW", "_INDIGO", "_GREEN", "_VIOLET",
        "_SINGLE", "_RAPID", "_RESOLUTE", "_PIROUETTE", "_SKY", "_ALOLA",
        "_GALARIAN", "_HISUI", "_PALDEA", "_STELLAR", "_TERASTAL",
        "_FIGHT", "_FLYING", "_POISON", "_GROUND", "_ROCK", "_BUG", "_GHOST",
        "_STEEL", "_FIRE", "_WATER", "_GRASS", "_ELECTRIC", "_PSYCHIC",
        "_ICE", "_DRAGON", "_DARK", "_FAIRY", "_BLAZE", "_EAST", "_WEST",
        "_S", "_M", "_L", "_XL", "_P", "_D", "_R", "_Z", "_10",
    )

    def __init__(self, rom_path: Path | None = None):
        self.rom_path = Path(rom_path) if rom_path else ROM_PATH_DEFAULT
        self.issues = []
        self.species = self._parse_species_registry()
        self.type_values = self._parse_types()
        self.rom_exists = self.rom_path.exists()

    def _parse_species_registry(self):
        if not SPECIES_HEADER.exists():
            raise FileNotFoundError(f"Missing species registry: {SPECIES_HEADER}")
        text = SPECIES_HEADER.read_text(encoding="utf-8")
        matches = re.findall(r"^#define\s+(SPECIES_[A-Z0-9_]+)\s+0x([0-9A-Fa-f]+)", text, re.M)
        species = {}
        for name, value in matches:
            try:
                species[int(value, 16)] = name
            except ValueError:
                self.issues.append(f"Unable to parse species value for {name}: {value}")
        return dict(sorted(species.items()))

    def _parse_types(self):
        if not POKEMON_HEADER.exists():
            raise FileNotFoundError(f"Missing type definitions: {POKEMON_HEADER}")
        text = POKEMON_HEADER.read_text(encoding="utf-8")
        matches = re.findall(r"^#define\s+(TYPE_[A-Z_]+)\s+0x([0-9A-Fa-f]+)", text, re.M)
        values = {}
        for name, value in matches:
            values[int(value, 16)] = name
        return dict(sorted(values.items()))

    def _json_species_names(self):
        if not SPECIES_JSON.exists():
            return set()
        try:
            payload = json.loads(SPECIES_JSON.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return set()
        names = set()
        for obj in payload.values():
            if isinstance(obj, list):
                for item in obj:
                    if isinstance(item, str) and item.startswith("SPECIES_"):
                        names.add(item)
            elif isinstance(obj, dict):
                for item in obj.values():
                    if isinstance(item, str) and item.startswith("SPECIES_"):
                        names.add(item)
        return names

    def _is_form_species(self, name: str) -> bool:
        return any(name.endswith(suffix) for suffix in self.FORM_SUFFIXES) and name not in {"SPECIES_NONE"}

    def _count_base_species(self):
        return sum(1 for value in self.species.values() if not self._is_form_species(value))

    def _base_species_id_pattern(self):
        ids = list(self.species)
        if not ids:
            return []
        if ids[0] != 0:
            return ["Registry does not begin at species ID 0"]
        if ids[-1] != max(ids):
            return ["Registry ordering is inconsistent"]
        return []

    def validate_registry(self):
        issues = []
        ids = list(self.species)
        if not ids:
            return ["No species constants were parsed from species.h"]

        if min(ids) != 0:
            issues.append(f"Species registry starts at {min(ids)}, expected 0")

        duplicates = [v for v in ids if ids.count(v) > 1]
        if duplicates:
            issues.append(f"Duplicate species IDs found: {sorted(set(duplicates))[:10]}")

        expected_national = 1025
        base_count = self._count_base_species()
        if base_count < expected_national:
            issues.append(
                f"National Dex base-species coverage is only {base_count}; expected at least {expected_national}"
            )

        # Ensure the registry contains the expected core species names
        required = [
            "SPECIES_NONE",
            "SPECIES_BULBASAUR",
            "SPECIES_SQUIRTLE",
            "SPECIES_CHARMANDER",
            "SPECIES_PIKACHU",
            "SPECIES_MEW",
            "SPECIES_CELEBI",
            "SPECIES_DEOXYS",
            "SPECIES_ARCEUS",
            "SPECIES_GENESECT",
            "SPECIES_ETERNATUS",
            "SPECIES_TERAPAGOS",
            "SPECIES_PECHARUNT",
        ]
        missing = [name for name in required if name not in self.species.values()]
        if missing:
            issues.append(f"Missing required species constants: {missing}")

        # Validate JSON references exist in the registry
        ref_names = self._json_species_names()
        missing_refs = sorted(name for name in ref_names if name not in self.species.values())
        if missing_refs:
            issues.append(f"Species tables JSON references names absent from species.h: {missing_refs[:10]}")

        # Validate type constants are sane
        if not self.type_values:
            issues.append("No valid TYPE_* constants were parsed from pokemon.h")
        elif 0 not in self.type_values or 24 not in self.type_values:
            issues.append("Expected at least NORMAL and STELLAR type constants in pokemon.h")

        return issues

    def report(self):
        print("\n" + "=" * 70)
        print("M2 SPECIES REGISTRY AUDIT")
        print("=" * 70)
        print(f"ROM present: {'yes' if self.rom_exists else 'no'}")
        print(f"Species constants parsed: {len(self.species)}")
        print(f"Base species estimated: {self._count_base_species()}")
        print(f"Type constants parsed: {len(self.type_values)}")
        print(f"Range: {min(self.species)}..{max(self.species)}")

        issues = self.validate_registry()
        if issues:
            print("\nIssues found:")
            for issue in issues:
                print(f"  - {issue}")
            return 1

        print("\n✓ Source species registry is internally consistent.")
        print("  The CFRU source exposes a complete species registry with valid type metadata.")
        print("  M2 is progressing with source-level validation pending deeper ROM asset extraction.")
        return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit FireRed Gen 9 species registry metadata")
    parser.add_argument("--rom", type=Path, default=ROM_PATH_DEFAULT, help="Path to ROM file; optional for source-only audit")
    args = parser.parse_args()

    audit = SpeciesAudit(args.rom)
    return audit.report()


if __name__ == "__main__":
    raise SystemExit(main())
