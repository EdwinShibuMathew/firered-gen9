#!/usr/bin/env python3
"""Validate form categories and resolve every claimed runtime binding to source."""
import csv
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
rows = list(csv.DictReader((ROOT / 'data/form_routes.csv').open(encoding='utf-8')))
categories = {
    'REGIONAL_DISTINCT', 'ENCOUNTER_OR_EVOLUTION_LOCKED',
    'HELD_ITEM_DERIVED', 'KEY_ITEM_TOGGLE', 'FORM_LAB_SELECTABLE',
    'FUSION_FORM', 'BATTLE_ONLY', 'COSMETIC_ALIAS',
    'UNSUPPORTED_PLACEHOLDER',
}
source_paths = [
    ROOT / '.upstream/cfru/src', ROOT / '.upstream/cfru/assembly',
    ROOT / '.upstream/cfru/include', ROOT / '.upstream/cfru/strings',
]
source = '\n'.join(
    path.read_text(encoding='utf-8', errors='ignore')
    for base in source_paths if base.exists()
    for path in base.rglob('*') if path.is_file()
)

bad = []
ids = set()
targets = set()
for row in rows:
    category = row['route_category']
    status = row['implementation_status']
    if category not in categories or not row['target_form']:
        bad.append((row, 'invalid category or target'))
        continue
    try:
        internal_id = int(row['internal_id'])
    except (KeyError, ValueError):
        bad.append((row, 'invalid internal ID'))
        continue
    if internal_id in ids or row['target_form'] in targets:
        bad.append((row, 'duplicate internal ID or target'))
    ids.add(internal_id)
    targets.add(row['target_form'])
    if row['base_species'] == 'derived_from_species_constant':
        bad.append((row, 'base species was not resolved'))
    if (category == 'BATTLE_ONLY') != (row['battle_only'] == 'true'):
        bad.append((row, 'battle-only marker mismatch'))
    if status == 'IMPLEMENTED_UNVERIFIED':
        handler = row['handler_symbol']
        script = row['script_symbol']
        if not handler or handler not in source:
            bad.append((row, f'unresolved handler {handler!r}'))
        if script and script not in source:
            bad.append((row, f'unresolved script {script!r}'))
    elif category != 'UNSUPPORTED_PLACEHOLDER':
        bad.append((row, 'safe form has no runtime binding'))
    if category in {'BATTLE_ONLY', 'REGIONAL_DISTINCT', 'ENCOUNTER_OR_EVOLUTION_LOCKED', 'UNSUPPORTED_PLACEHOLDER'} and row['acquisition_method'] == 'cinnabar_form_lab':
        bad.append((row, 'unsafe Form Lab exposure'))
    if category == 'FORM_LAB_SELECTABLE' and not all(
        token in source for token in (row['base_species'], row['target_form'], 'sM5FormLabFamilies')
    ):
        bad.append((row, 'generated Form Lab family is incomplete'))
    if category in {'REGIONAL_DISTINCT', 'ENCOUNTER_OR_EVOLUTION_LOCKED'} and not all(
        token in source for token in (row['target_form'], 'sM5ResearchPreserveForms')
    ):
        bad.append((row, 'generated preserve encounter is incomplete'))

mapped = re.findall(
    r'\[(SPECIES_[A-Z0-9_]+)\s*-\s*1\]\s*=\s*(NATIONAL_DEX_[A-Z0-9_]+)',
    (ROOT / '.upstream/dpe/src/Species_To_Pokdex_Table.c').read_text(encoding='utf-8'),
)
expected_count = sum(
    species != 'SPECIES_EGG'
    and species.removeprefix('SPECIES_') != national.removeprefix('NATIONAL_DEX_')
    for species, national in mapped
)
if len(rows) != expected_count:
    bad.append(({'target_form': '<inventory>'}, f'expected {expected_count} canonical alternate-form rows'))

counts = Counter(row['implementation_status'] for row in rows)
category_counts = Counter(row['route_category'] for row in rows)
print(f'Form route contract: {len(rows)} internal forms, {len(rows)-len(bad)} valid rows')
print('Binding states: ' + ', '.join(f'{key}={value}' for key, value in sorted(counts.items())))
print('Categories: ' + ', '.join(f'{key}={value}' for key, value in sorted(category_counts.items())))
if bad:
    for row, reason in bad[:20]:
        print(f"INVALID {row['target_form']}: {reason}")
raise SystemExit(1 if bad else 0)
