#!/usr/bin/env python3
"""Inventory upstream sprite/icon/palette/cry assets with hashes and provenance."""
from pathlib import Path
import csv, hashlib
ROOT = Path(__file__).resolve().parents[1]
roots = [ROOT / '.upstream/dpe', ROOT / '.upstream/cfru']
rows=[]
for root in roots:
    if not root.exists(): continue
    for path in root.rglob('*'):
        if not path.is_file() or not any(x in path.name.lower() for x in ('sprite','pic','icon','pal','cry')): continue
        rel = path.relative_to(ROOT).as_posix()
        kind = 'icon' if 'icon' in path.name.lower() else 'palette' if 'pal' in path.name.lower() else 'cry' if 'cry' in path.name.lower() else 'sprite'
        rows.append({'asset_path':rel,'asset_type':kind,'species_or_form':'UNRESOLVED','sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'source_repository':'local pinned upstream','source_commit':'see build-lock.json','upstream_credit_entry':'upstream repository credits','duplicate_group':'','status':'PROVENANCE_UNKNOWN','notes':'requires visual/contact-sheet review'})
out=ROOT/'data/asset_provenance.csv'
with out.open('w',newline='',encoding='utf-8') as f:
    fields=('asset_path','asset_type','species_or_form','sha256','source_repository','source_commit','upstream_credit_entry','duplicate_group','status','notes')
    w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(sorted(rows,key=lambda r:r['asset_path']))
print(f'Wrote {len(rows)} asset provenance rows: {out}')
