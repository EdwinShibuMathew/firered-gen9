#!/usr/bin/env python3
"""Create ignored PNG contact sheets for later visual form/asset review."""
from pathlib import Path
from PIL import Image, ImageDraw
import csv, math
ROOT=Path(__file__).resolve().parents[1]
out=ROOT/'build/m5_contact_sheets'; out.mkdir(parents=True, exist_ok=True)
rows=list(csv.DictReader((ROOT/'data/asset_provenance.csv').open(encoding='utf-8')))
images=[]
for row in rows:
    p=ROOT/row['asset_path']
    if p.suffix.lower() not in {'.png','.bmp','.jpg','.jpeg'}: continue
    try: im=Image.open(p).convert('RGBA')
    except Exception: continue
    im.thumbnail((64,64)); images.append((row['asset_path'],im))
for page in range(0,len(images),36):
    batch=images[page:page+36]; sheet=Image.new('RGBA',(6*128,6*96),(240,240,240,255)); d=ImageDraw.Draw(sheet)
    for i,(name,im) in enumerate(batch):
        x=(i%6)*128; y=(i//6)*96; sheet.alpha_composite(im,(x+32,y)); d.text((x+2,y+66),name[-20:],fill=(0,0,0,255))
    sheet.convert('RGB').save(out/f'assets_{page//36:03d}.png')
print(f'Generated {math.ceil(len(images)/36) if images else 0} ignored contact sheets in {out}')
