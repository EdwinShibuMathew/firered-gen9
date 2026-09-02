# M5 Design Specification

This is the authoritative implementation specification for forms, the Evolution Guide, and Legendary encounter outcomes.

## Evolution Guide

The Guide is a second page of the existing Pokédex detail task. `SELECT` toggles between the normal detail and Guide pages; `B`/`SELECT` returns to detail, `UP/DOWN` selects a route, `LEFT/RIGHT` paginates, and `A` opens the target entry. Up to three routes are rendered per page using existing Pokédex windows, fonts, palettes, and icons. Conditions are sourced from `data/evolution_encyclopedia.csv`; no manually duplicated condition database is permitted.

## Form routes

`data/form_routes.csv` is authoritative. Every internal form ID is assigned exactly one category. Regional and encounter-locked forms are not freely toggled. Held-item and key-item routes reuse CFRU's existing held-item and field callbacks. Fusion uses CFRU's existing storage implementation. Battle-only forms are excluded from the Form Lab. Unsupported forms remain explicitly reported rather than silently exposed.

The Cinnabar Form Research Lab is the fallback for safe, reversible, permanently storable or cosmetic routes without a canonical trigger. It validates ownership and target routes, preserves all mon data, consumes no item, and never exposes battle-only or regional-family conversions.

## Legendary outcomes

Each encounter has unlock, active, and capture-completed state. Flee, defeat, and blackout leave it available; capture permanently completes it. The current static re-entry overlay implements the first six Kanto/Sevii encounters, with `data/legendary_encounters.csv` documenting the complete intended contract.

## Release boundary

Private builds may contain unresolved upstream assets. Public release remains blocked by provenance review, legal patch generation, and manual mGBA verification.
