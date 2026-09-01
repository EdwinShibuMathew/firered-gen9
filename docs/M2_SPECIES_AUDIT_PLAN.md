# M2 Species Audit - Implementation Plan

**Milestone:** M2 Validate all species data  
**Status:** STARTING  
**Target Completion:** 1,025/1,025 National Pokédex species validated

---

## M2 Requirements

From `GEN9_COMPLETION_ROADMAP.md`:

1. **Freeze upstream species/form ordering** before distributed saves exist
2. **Create audit script** (`scripts/audit_species.py`) with build-time validation
3. **Audit all 1,025 National Pokédex species**
4. **Validate comprehensive data:**
   - IDs and national Pokédex ordering
   - Species names and forms
   - Base stat distribution (HP, ATK, DEF, SPA, SPD, SPE)
   - Types (including Fairy and Stellar for Gen 9)
   - Abilities and hidden abilities
   - Catch rates, experience yields, EV yields
   - Egg groups and gender ratios
   - Height, weight, classification, habitat
   - Pokédex text entries
   - Evolution chains and methods
   - Level-up learnsets
   - TM/HM/Tutor compatibility
   - Held items
   - Front/back sprites
   - Shiny palettes
   - Pokédex icons
   - Cries

5. **Report Issues:**
   - Duplicate species IDs
   - Invalid type references
   - Missing assets (sprites, palettes, cries, Pokédex entries)
   - Placeholder artwork
   - Missing abilities or learnsets
   - Incomplete evolution chains
   - Incomplete form data

6. **Special Cases:**
   - Verify and replace Poltchageist/Sinistcha placeholder artwork
   - Handle all Gen 9 species (906-1025)
   - Handle all Alola, Galar, Hisui forms

7. **Defer (for M2):**
   - Custom `GEN9_DATA_VERSION` metadata
   - Incompatible-save rejection system
   - Save layout identification (wait for CFRU/DPE testing)

---

## Implementation Strategy

### Phase 1: Data Extraction (this session)

- Extract all species information from compiled ROM using binary analysis
- Parse CFRU's generated ROM tables
- Build in-memory species database

### Phase 2: Validation Framework (this session)

- Create hierarchical validation rules
- Implement per-species audit functions
- Generate detailed validation reports

### Phase 3: Full Audit (this session)

- Run audit against all 1,025 species
- Categorize findings by severity
- Generate remediation plan

### Phase 4: Remediation (future sessions)

- Fix data issues discovered
- Replace placeholder artwork
- Verify Alola/Galar/Hisui forms

---

## Species Data Locations (in CFRU ROM)

Based on CFRU structure:

- **Base Stats Table:** Dynamically loaded at 0x80001BC (ROM offset determined at build)
- **Species Names:** Likely in string table
- **Sprites:** Graphics banks (various offsets)
- **Pokédex Text:** String tables
- **Move Learnsets:** `level_up_learnsets.c` (789950 bytes)
- **Abilities:** In BaseStats struct or separate table
- **Evolution Data:** Evolution table in ROM

---

## Audit Categories

### CRITICAL (Must fix before M2 complete)
- Missing species IDs (0 or > 1025)
- Duplicate IDs
- NULL pointers or uninitialized data
- Invalid type references

### HIGH (Should fix before release)
- Missing sprites (front/back/shiny)
- Missing Pokédex text
- Missing learnsets
- Placeholder artwork (non-final assets)

### MEDIUM (Nice to fix)
- Incomplete evolution chains
- Missing abilities
- Form data issues
- Missing form artwork

### LOW (Informational)
- Species statistics summary
- Form coverage report
- Cross-generation distribution

---

## Scripts to Create

### 1. `scripts/audit_species.py`

Main audit script that:
- Reads from `.upstream/cfru/test.gba`
- Extracts species data via binary analysis
- Validates against comprehensive rules
- Generates reports (JSON, CSV, markdown)
- Returns non-zero exit code if critical issues found
- Integrates into build pipeline

### 2. `scripts/extract_species_data.py`

Helper script that:
- Dumps raw species data from ROM
- Outputs structured JSON for analysis
- Useful for debugging and verification

### 3. `data/species_validation_schema.json`

Schema defining required fields for each species

### 4. `data/species_placeholder_map.json`

Mapping of known placeholder species (e.g., Poltchageist forms)

---

## Success Criteria

- [x] M1 Complete (prerequisite)
- [ ] `scripts/audit_species.py` created and integrated
- [ ] All 1,025 species audited
- [ ] Critical issues (if any) documented
- [ ] Species/form ordering frozen in code
- [ ] Report generated: `docs/M2_SPECIES_AUDIT_REPORT.md`
- [ ] All CRITICAL findings remediated
- [ ] Build fails if audit fails (make target)

---

## Timeline

- Phase 1: ~1-2 hours (data extraction)
- Phase 2: ~2-3 hours (validation framework)
- Phase 3: ~1 hour (full audit)
- Phase 4: TBD (remediation, typically future session)

**Total for M2 completion:** ~5 hours

---

## Next Steps

1. Extract base ROM species data
2. Create validation framework
3. Run comprehensive audit
4. Document findings
5. Tag as `m2-species-audit-complete` when all critical issues fixed

Let's start! 🔍
