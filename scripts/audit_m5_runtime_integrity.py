#!/usr/bin/env python3
"""Deterministic structural checks for M5 mutation and fusion safety boundaries."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
party = (ROOT / '.upstream/cfru/src/party_menu.c').read_text(encoding='utf-8')
scripting = (ROOT / '.upstream/cfru/src/scripting.c').read_text(encoding='utf-8')
system = (ROOT / '.upstream/cfru/assembly/overworld_scripts/system_scripts.s').read_text(encoding='utf-8')

checks = {
    'validated mutation boundary': all(token in party for token in (
        'bool8 TryChangeMonForm', 'MON_DATA_IS_EGG', 'targetSpecies >= NUM_SPECIES',
        'SpeciesToNationalPokedexNum(targetSpecies)', 'CalculateMonStats(mon)',
    )),
    'metadata-preserving species-only write': (
        'SetMonData(mon, MON_DATA_SPECIES, &targetSpecies);' in party
        and 'ZeroMonData(mon)' not in party[party.index('bool8 TryChangeMonForm'):party.index('void DoItemFormChange')]
    ),
    'hp clamped after stat recalculation': all(token in party for token in (
        'oldHp = GetMonData(mon, MON_DATA_HP',
        'newMaxHp = GetMonData(mon, MON_DATA_MAX_HP',
        'if (oldHp > newMaxHp)',
    )),
    'form lab validates before mutation': (
        scripting.index('void M5FormLabPrepareSelectedForm')
        < scripting.index('void M5FormLabApplyPreparedForm')
        < scripting.index('#define POKERUS_CURED')
        and 'TryChangeMonForm(&gPlayerParty[Var8004], Var8005)' in scripting
    ),
    'form lab cancellation path': all(token in system for token in (
        'compare LASTRESULT 0x7F', 'goto EventScript_M5FormResearcherCancel',
    )),
    'form preserve is encounter-only': all(token in system for token in (
        'EventScript_M5ResearchPreserve:', 'setwildbattle 0x8000 30 0', 'dowildbattle',
    )) and 'TryChangeMonForm' not in scripting[
        scripting.index('void M5ResearchPreservePrepareMenu'):
        scripting.index('// Called after ChoosePartyMon')
    ],
    'fusion full-party bound checked first': (
        'for (slotId = 0; slotId < PARTY_SIZE\n'
        '                                     && GetMonData(&gPlayerParty[slotId]' in party
    ),
    'fusion components use dedicated save storage': all(token in party for token in (
        'fusedReshiram', 'fusedZekrom', 'fusedSolgaleo', 'fusedLunala',
        'fusedGlastrier', 'fusedSpectrier',
    )),
    'necrozma lunala duplicate guard': (
        'case SPECIES_LUNALA:\n                                        if (GetMonData(&gSaveBlock1->fusedLunala' in party
    ),
}

for name, passed in checks.items():
    print(('PASS ' if passed else 'FAIL ') + name)
raise SystemExit(0 if all(checks.values()) else 1)
