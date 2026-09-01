# M2 Species Audit - Progress Report

**Milestone:** M2 Validate all species data  
**Status:** IN PROGRESS  
**Date Started:** 2026-09-01  
**Target:** 1,025/1,025 National Pokédex species validated

---

## M2 Milestones

### Phase 1: Framework Setup ✓
- [x] M1 complete and tagged (`gen9-engine-baseline`)
- [x] M2 planning document created (`docs/M2_SPECIES_AUDIT_PLAN.md`)
- [x] Audit script framework created (`scripts/audit_species.py`)
- [x] Initial validation harness working

### Phase 2: Data Extraction (In Progress)
- [ ] Extract base stats from compiled ROM
- [ ] Extract species names and Pokédex entries
- [ ] Map species forms and variants
- [ ] Extract move compatibility data
- [ ] Extract ability mappings
- [ ] Extract evolution chains

### Phase 3: Full Validation
- [ ] Run comprehensive validation against all 1,025 species
- [ ] Generate detailed audit report
- [ ] Identify critical issues
- [ ] Identify missing assets
- [ ] Flag placeholder artwork

### Phase 4: Remediation
- [ ] Fix critical issues
- [ ] Replace placeholder artwork (Poltchageist/Sinistcha)
- [ ] Verify form completeness
- [ ] Tag as `m2-species-audit-complete`

---

## Current Status Summary

✓ **Framework Ready**
- Audit script created and compiling successfully
- ROM loading verified (32 MiB CFRU artifact)
- Progress tracking functional
- Report generation structure in place

⏳ **Data Extraction Required**
- Need to parse ROM binary structure
- Need to identify species data tables in compiled ROM
- Need to validate against expected structure

ℹ️ **Key Information**
- Total species to audit: **1,025** (Gen 1-9, all forms)
- ROM artifact: `.upstream/cfru/test.gba` (32 MiB, SHA-256 verified)
- Audit framework: `scripts/audit_species.py`
- Planned validations: Stats, types, abilities, sprites, moves, evolutions

---

## Known Data Locations (from CFRU source)

From analysis of CFRU source code:

- **BaseStats Structure:** Defined in `include/pokemon.h`, includes:
  - HP, Attack, Defense, Speed, Sp. Atk, Sp. Def (6 bytes)
  - Type1, Type2 (2 bytes)
  - Catch Rate, EXP Yield (2 bytes)
  - EV Yield, Held Items, Gender Ratio, Habitat, Color, Pokedex ID
  - Approximately 28-40 bytes per species

- **Species Names:** String table (likely in compiled string section)

- **Sprites:** Graphics banks for front/back/shiny palettes

- **Pokédex Text:** Multiple entries per species

- **Move Learnsets:** `level_up_learnsets.c` (789950 bytes) provides structure

- **Evolution Data:** Evolution table in ROM

---

## Next Steps

### Immediate (this session)
1. Enhance audit script to extract actual ROM data
2. Parse BaseStats table from compiled ROM
3. Validate stats distribution
4. Run audit against all 1,025 species

### Short-term (next session if needed)
1. Extract sprite asset mappings
2. Verify Pokédex text completeness
3. Validate form coverage
4. Audit learnsets and moves

### Medium-term
1. Identify and flag placeholder assets
2. Plan replacements for incomplete forms
3. Create remediation tasks

---

## Validation Checklist (for each species)

- [ ] Valid species ID (1-1025)
- [ ] All 6 base stats > 0
- [ ] Valid type assignments (Normal-Stellar)
- [ ] Meaningful catch rate
- [ ] EXP yield assigned
- [ ] At least one ability
- [ ] Valid evolution chain (if applicable)
- [ ] Front sprite exists
- [ ] Back sprite exists
- [ ] Shiny palette exists
- [ ] Pokédex entries present
- [ ] Level-up moves defined
- [ ] At least one form defined

---

## Findings So Far

| Category | Count | Status |
|----------|-------|--------|
| Species Audited | 1025 | In Progress |
| Critical Issues | TBD | Pending full validation |
| High Issues | TBD | Pending full validation |
| Medium Issues | TBD | Pending full validation |
| Low Issues | TBD | Pending full validation |

---

## Appendix: Species Coverage by Generation

**Target Coverage:**
- Gen 1 (Kanto): 151 species (Bulbasaur-Mewtwo + Mew)
- Gen 2 (Johto): +100 species (Chikorita-Ho-Oh + Celebi)
- Gen 3 (Hoenn): +135 species (Treecko-Kyogre + Jirachi, Deoxys)
- Gen 4 (Sinnoh): +107 species (Turtwig-Dialga + Palkia, Giratina, Phione, Manaphy, Darkrai, Shaymin, Arceus)
- Gen 5 (Unova): +156 species (Snivy-Victini, B2W2 additions)
- Gen 6 (Kalos): +72 species (Chespin-Zygarde + Diancie, Hoopa, Volcanion)
- Gen 7 (Alola): +81 species (Rowlet-Magearna, Alola forms, Totem forms)
- Gen 8 (Galar): +89 species (Grookey-Eternatus, Galar forms, Dynamax)
- Gen 9 (Paldea): +96 species (Sprigatito-Pecharunt, Paldea forms, Terastallization)

**Total: 1,025 unique Pokédex entries (including forms as separate entries in some cases)**

---

## Roadmap Alignment

This M2 completion will gate:
- ✓ M3: Make every evolution possible offline
- ✓ M4: Deterministic 1,025/1,025 availability
- ✓ M5: Forms, quests, and content polish
- ✓ M6: Port existing custom starter work
- ✓ M7: Optional Habitat Scanner
- ✓ M8: Release patch and final testing

---

**Report Generated:** 2026-09-01 13:52  
**Next Review:** After full ROM data extraction and validation
