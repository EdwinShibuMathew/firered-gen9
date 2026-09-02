# M7 Habitat Scanner — Progress

**Status:** `[~]` optional foundation present; migration groups and QA remain

- CFRU's DexNav/Habitat-style scanner plumbing is present and exposed behind `FLAG_SYS_DEXNAV`.
- M4 deterministic reserves already provide 1,025/1,025 coverage, so M7 is not an availability dependency.
- National migration groups (Kanto through Paldea/Hisui), UI polish, and advanced-mechanics regression tests remain to be implemented and manually validated.
- `data/habitat_migration_groups.csv` defines all nine selectable regional groups as the implementation contract; each row is currently pending UI integration.

Run `python3 scripts/audit_m7.py` for the source prerequisite check.
