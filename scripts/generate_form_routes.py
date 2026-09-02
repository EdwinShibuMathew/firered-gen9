#!/usr/bin/env python3
"""Generate the authoritative, explicitly categorized internal-form route table."""
from pathlib import Path
import csv
import re

ROOT = Path(__file__).resolve().parents[1]
text = (ROOT / '.upstream/cfru/include/constants/species.h').read_text(encoding='utf-8')
defines = []
SAFE_FUSIONS = {
    'SPECIES_KYUREM_BLACK', 'SPECIES_KYUREM_WHITE',
    'SPECIES_NECROZMA_DUSK_MANE', 'SPECIES_NECROZMA_DAWN_WINGS',
    'SPECIES_CALYREX_ICE_RIDER', 'SPECIES_CALYREX_SHADOW_RIDER',
}
FORM_LAB_PREFIXES = ('SPECIES_ROTOM_', 'SPECIES_DEOXYS_', 'SPECIES_FURFROU_')
FORM_LAB_EXACT = {'SPECIES_SHAYMIN_SKY', 'SPECIES_HOOPA_UNBOUND'}
KEY_ITEM_PREFIXES = (
    'SPECIES_TORNADUS_', 'SPECIES_THUNDURUS_', 'SPECIES_LANDORUS_',
    'SPECIES_ENAMORUS_',
)
HELD_ITEM_PREFIXES = ('SPECIES_ARCEUS_', 'SPECIES_SILVALLY_', 'SPECIES_GENESECT_')
HELD_ITEM_EXACT = {
    'SPECIES_GIRATINA_ORIGIN', 'SPECIES_ZACIAN_CROWNED',
    'SPECIES_ZAMAZENTA_CROWNED', 'SPECIES_OGERPON_WELLSPRING_MASK',
    'SPECIES_OGERPON_HEARTHFLAME_MASK', 'SPECIES_OGERPON_CORNERSTONE_MASK',
}
for name, value in re.findall(r'^#define\s+(SPECIES_[A-Z0-9_]+)\s+(0x[0-9A-Fa-f]+|\d+)', text, re.M):
    tail = name[len('SPECIES_'):]
    if '_' not in tail:
        continue
    upper = tail
    battle = ('MEGA' in upper or 'GIGA' in upper or 'DYNAMAX' in upper or 'PRIMAL' in upper or 'TERA' in upper or upper.endswith('_HERO') or upper.endswith('_SCHOOL') or upper.endswith('_NOICE') or upper.endswith('_BUSTED') or upper.endswith('_ZEN'))
    regional = any(x in upper for x in ('_ALOLA', '_GALAR', '_HISUI', '_PALDEAN', '_PALDEA'))
    if battle:
        category = 'BATTLE_ONLY'
    elif regional:
        category = 'REGIONAL_DISTINCT'
    elif name in SAFE_FUSIONS:
        category = 'FUSION_FORM'
    elif name in HELD_ITEM_EXACT or name.startswith(HELD_ITEM_PREFIXES):
        category = 'HELD_ITEM_DERIVED'
    elif name in FORM_LAB_EXACT or name.startswith(FORM_LAB_PREFIXES):
        category = 'FORM_LAB_SELECTABLE'
    elif name.startswith(KEY_ITEM_PREFIXES):
        category = 'KEY_ITEM_TOGGLE'
    elif any(x in upper for x in ('_HEAT', '_WASH', '_FROST', '_FAN', '_MOW', '_SKY', '_UNBOUND', '_THERIAN', '_BLAZE', '_AQUA', '_WELLSPRING_MASK', '_HEARTHFLAME_MASK', '_CORNERSTONE_MASK')):
        category = 'KEY_ITEM_TOGGLE'
    elif any(x in upper for x in ('_RED', '_BLUE', '_WHITE', '_YELLOW', '_ORANGE', '_SUMMER', '_WINTER', '_AUTUMN', '_EAST', '_THREE', '_FOUR', '_LARGE', '_SMALL', '_XL', '_M', '_S', '_F', '_ATTACK', '_DEFENSE', '_SPEED')):
        category = 'ENCOUNTER_OR_EVOLUTION_LOCKED'
    else:
        category = 'UNSUPPORTED_PLACEHOLDER'
    defines.append((name, category, value))

out = ROOT / 'data/form_routes.csv'
with out.open('w', newline='', encoding='utf-8') as f:
    fields = ('base_species', 'target_form', 'route_category', 'trigger_item', 'trigger_location', 'item_consumed', 'reversible', 'battle_only', 'acquisition_method', 'implementation_status', 'handler_type', 'handler_symbol', 'script_symbol', 'notes')
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    for name, category, value in defines:
        bindings = {
            'BATTLE_ONLY': ('battle_engine', 'IMPLEMENTED_UNVERIFIED', 'BATTLE_ENGINE', 'DoFormChange', ''),
            'FUSION_FORM': ('existing_cfru_fusion_storage', 'IMPLEMENTED_UNVERIFIED', 'C_HANDLER', 'ItemUseCB_FormChangeItem', ''),
            'HELD_ITEM_DERIVED': ('existing_cfru_held_item', 'IMPLEMENTED_UNVERIFIED', 'C_HANDLER', 'HoldItemFormChange', ''),
            'KEY_ITEM_TOGGLE': ('existing_cfru_key_item', 'IMPLEMENTED_UNVERIFIED', 'C_HANDLER', 'ItemUseCB_FormChangeItem', ''),
            'FORM_LAB_SELECTABLE': ('cinnabar_form_lab', 'IMPLEMENTED_UNVERIFIED', 'C_HANDLER', 'M5FormLabApplyPreparedForm', 'EventScript_M5FormResearcher'),
        }
        acquisition, status, handler_type, handler, script = bindings.get(
            category, ('encounter_or_evolution' if category in {'REGIONAL_DISTINCT', 'ENCOUNTER_OR_EVOLUTION_LOCKED'} else 'form_lab_review', 'NOT_IMPLEMENTED', 'PENDING', '', ''))
        writer.writerow({'base_species': 'derived_from_species_constant', 'target_form': name, 'route_category': category, 'trigger_item': '', 'trigger_location': '', 'item_consumed': 'false', 'reversible': str(category in {'KEY_ITEM_TOGGLE', 'FORM_LAB_SELECTABLE', 'FUSION_FORM'}).lower(), 'battle_only': str(category == 'BATTLE_ONLY').lower(), 'acquisition_method': acquisition, 'implementation_status': status, 'handler_type': handler_type, 'handler_symbol': handler, 'script_symbol': script, 'notes': f'internal id {value}'})
print(f'Wrote {len(defines)} categorized form routes: {out}')
