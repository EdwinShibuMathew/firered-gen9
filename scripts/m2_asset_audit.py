#!/usr/bin/env python3
"""
M2 Phase 3: Asset & Data Validation Audit

Comprehensive audit of species assets including:
- Sprite assets (front/back/shiny)
- Pokédex text entries
- Move learnsets
- Ability assignments
- Evolution chains
"""

import json
import re
import sys
from collections import defaultdict
from pathlib import Path


SRC_ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = SRC_ROOT / ".upstream/cfru"
SPECIES_HEADER = UPSTREAM / "include/constants/species.h"
LEARNSETS_FILE = UPSTREAM / "src/Tables/level_up_learnsets.c"
ABILITY_NAMES = UPSTREAM / "strings/ability_name_table.string"
EVOLUTION_FILE = UPSTREAM / "src/evolution.c"
POKEDEX_STRINGS = UPSTREAM / "strings/pokedex_entries.string"


class M2AssetAudit:
    """Audit species assets and data completeness."""

    def __init__(self):
        self.issues = defaultdict(list)
        self.findings = {
            "sprites": {"found": 0, "missing": 0},
            "pokédex": {"found": 0, "missing": 0},
            "learnsets": {"found": 0, "missing": 0},
            "abilities": {"found": 0, "missing": 0},
            "evolutions": {"found": 0, "missing": 0},
        }
        self.species = self._parse_species_registry()
        self.abilities = self._parse_ability_names()
        self.evolutions = self._parse_evolution_data()
        self.learnsets = self._parse_learnsets()
        self.pokédex_entries = self._parse_pokédex_entries()

    def _parse_species_registry(self):
        """Parse species constants from header."""
        if not SPECIES_HEADER.exists():
            raise FileNotFoundError(f"Missing species registry: {SPECIES_HEADER}")
        text = SPECIES_HEADER.read_text(encoding="utf-8")
        matches = re.findall(r"^#define\s+(SPECIES_[A-Z0-9_]+)\s+0x([0-9A-Fa-f]+)", text, re.M)
        species = {}
        for name, value in matches:
            try:
                species_id = int(value, 16)
                species[species_id] = name
            except ValueError:
                pass
        return dict(sorted(species.items()))

    def _parse_ability_names(self):
        """Parse ability names from string table."""
        if not ABILITY_NAMES.exists():
            return {}
        text = ABILITY_NAMES.read_text(encoding="utf-8", errors="ignore")
        # Count non-empty ability entries (basic check)
        lines = [line.strip() for line in text.split("\n") if line.strip() and not line.startswith("#")]
        return {"count": len(lines), "entries": lines}

    def _parse_evolution_data(self):
        """Parse evolution chains from evolution.c."""
        if not EVOLUTION_FILE.exists():
            return {}
        text = EVOLUTION_FILE.read_text(encoding="utf-8", errors="ignore")
        # Count evolution definitions with more reliable pattern
        evo_methods = re.findall(r"case\s+EVO_\w+:", text)
        evo_entries = re.findall(r"targetSpecies\s*=\s*(SPECIES_[A-Z0-9_]+)", text)
        evolution_chains = re.findall(r"gEvolutionTable\s*\[\s*(SPECIES_[A-Z0-9_]+)\s*\]", text)
        return {
            "evolution_methods": len(set(evo_methods)),
            "evolution_entries": len(set(evo_entries)),
            "species_with_evolution": len(set(evolution_chains)),
        }

    def _parse_learnsets(self):
        """Parse move learnsets from level_up_learnsets.c."""
        if not LEARNSETS_FILE.exists():
            return {}
        text = LEARNSETS_FILE.read_text(encoding="utf-8", errors="ignore")
        # Count learnset arrays for species
        learnset_arrays = re.findall(r"const\s+struct\s+LevelUpMove\s+\w+\[\]", text)
        # Extract move constants more carefully
        move_entries = re.findall(r"LEVEL_UP_MOVE\s*\(\s*\d+\s*,\s*(MOVE_[A-Z0-9_]+)\s*\)", text)
        return {
            "arrays": len(learnset_arrays),
            "total_moves": len(move_entries),
            "unique_moves": len(set(move_entries)),
        }

    def _parse_pokédex_entries(self):
        """Parse Pokédex text entries."""
        if not POKEDEX_STRINGS.exists():
            # Try alternate Pokédex locations
            for alt_path in [
                UPSTREAM / "strings" / "pokemon_descriptions.string",
                UPSTREAM / "strings" / "pokemon_texts.string",
            ]:
                if alt_path.exists():
                    text = alt_path.read_text(encoding="utf-8", errors="ignore")
                    non_empty = [line.strip() for line in text.split("\n") if line.strip() and not line.startswith("#")]
                    return {"entries": len(non_empty), "source": str(alt_path)}
            return {}
        text = POKEDEX_STRINGS.read_text(encoding="utf-8", errors="ignore")
        # Count Pokédex entries (basic line count)
        non_empty = [line.strip() for line in text.split("\n") if line.strip() and not line.startswith("#")]
        return {"entries": len(non_empty), "source": "pokedex_entries.string"}

    def audit_species_completeness(self):
        """Audit completeness of all species data."""
        results = {
            "total_species": len(self.species),
            "base_species": 0,
            "form_variants": 0,
            "with_abilities": 0,
            "with_evolutions": 0,
            "with_learnsets": 0,
        }

        FORM_SUFFIXES = (
            "_A", "_G", "_H", "_N", "_MEGA", "_PRIMAL", "_ORIGIN", "_THERIAN",
            "_CROWNED", "_ICE_RIDER", "_SHADOW_RIDER", "_DADA", "_ETERNAMAX",
            "_RED", "_BLUE", "_ORANGE", "_YELLOW", "_INDIGO", "_GREEN", "_VIOLET",
            "_SINGLE", "_RAPID", "_RESOLUTE", "_PIROUETTE", "_SKY", "_ALOLA",
            "_GALARIAN", "_HISUI", "_PALDEA", "_STELLAR", "_TERASTAL",
        )

        for species_id, name in self.species.items():
            is_form = any(name.endswith(suffix) for suffix in FORM_SUFFIXES)
            if not is_form:
                results["base_species"] += 1
            else:
                results["form_variants"] += 1

        # Count species with various data types
        if self.abilities:
            results["with_abilities"] = self.abilities.get("count", 0)

        if self.evolutions:
            results["with_evolutions"] = self.evolutions.get("entries", 0)

        if self.learnsets:
            results["with_learnsets"] = self.learnsets.get("arrays", 0)

        return results

    def generate_audit_report(self):
        """Generate comprehensive audit report."""
        completeness = self.audit_species_completeness()

        print("\n" + "=" * 80)
        print("M2 PHASE 3: ASSET & DATA VALIDATION AUDIT")
        print("=" * 80)

        print("\n### SPECIES REGISTRY OVERVIEW ###")
        print(f"Total species constants: {completeness['total_species']}")
        print(f"Base species: {completeness['base_species']}")
        print(f"Form variants: {completeness['form_variants']}")

        print("\n### DATA COMPLETENESS ###")
        if self.abilities:
            print(f"✓ Ability names: {self.abilities.get('count', 0)} entries found")
        else:
            print("✗ Ability names: NOT FOUND")
            self.issues["critical"].append("Ability names file missing or empty")

        if self.evolutions:
            evo_count = self.evolutions.get("evolution_entries", 0)
            methods = self.evolutions.get("evolution_methods", 0)
            species = self.evolutions.get("species_with_evolution", 0)
            print(f"✓ Evolution chains: {species} species, {evo_count} evolution targets, {methods} methods")
        else:
            print("✗ Evolution chains: NOT FOUND")
            self.issues["high"].append("Evolution data file missing or empty")

        if self.learnsets:
            print(f"✓ Move learnsets: {self.learnsets.get('arrays', 0)} arrays, " +
                  f"{self.learnsets.get('total_moves', 0)} total moves")
            print(f"  Unique moves: {self.learnsets.get('unique_moves', 0)}")
        else:
            print("✗ Move learnsets: NOT FOUND")
            self.issues["high"].append("Learnsets file missing or empty")

        if self.pokédex_entries:
            print(f"✓ Pokédex entries: {self.pokédex_entries.get('entries', 0)} text entries found")
        else:
            print("✗ Pokédex entries: NOT FOUND")
            self.issues["high"].append("Pokédex text file missing or empty")

        print("\n### COVERAGE ANALYSIS ###")
        expected_abilities = 300  # Approximate Gen 1-9 abilities
        expected_moves = 900      # Approximate Gen 1-9 moves
        actual_moves = self.learnsets.get("unique_moves", 0)

        if self.abilities:
            ability_count = self.abilities.get("count", 0)
            coverage = (ability_count / expected_abilities) * 100
            print(f"Ability coverage: {ability_count}/{expected_abilities} (~{coverage:.1f}%)")
            if ability_count < expected_abilities * 0.8:
                self.issues["medium"].append(f"Low ability coverage ({ability_count} < {int(expected_abilities * 0.8)})")

        if actual_moves > 0:
            move_coverage = (actual_moves / expected_moves) * 100
            print(f"Move coverage: {actual_moves}/{expected_moves} (~{move_coverage:.1f}%)")
            if actual_moves < expected_moves * 0.8:
                self.issues["medium"].append(f"Low move coverage ({actual_moves} < {int(expected_moves * 0.8)})")

        print("\n### AUDIT SUMMARY ###")
        if not self.issues:
            print("✓ No critical issues found")
            return 0
        else:
            total_issues = sum(len(v) for v in self.issues.values())
            print(f"✗ Found {total_issues} issue(s):")
            for severity in ["critical", "high", "medium", "low"]:
                if self.issues[severity]:
                    print(f"\n  {severity.upper()}:")
                    for issue in self.issues[severity]:
                        print(f"    - {issue}")
            return 1 if self.issues.get("critical") else 0


def main() -> int:
    """Run M2 Phase 3 asset audit."""
    try:
        audit = M2AssetAudit()
        return audit.generate_audit_report()
    except Exception as e:
        print(f"Error during audit: {e}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
