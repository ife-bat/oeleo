# Plan: Issue #41 — dump_db CSV/JSON export

## Goal

Extend existing `dump_db` / `dump_bookkeeper` so operators can export `FileList` rows as CSV and JSON (not only human log lines), with a unit test and short docs.

## Constraints

- Library / script helper only — no GUI, no new console entry point in `pyproject.toml`.
- Preserve current `output_format="human"` logging behaviour (and `verbose` compact/verbose human modes).
- Stay small: no SharePoint/SSH work, no relative-path bookkeeping (#37).
- Use project toolchain: `uv run pytest -m "not ssh"`.

### Prior art

- `dump_db` / `dump_worker_db_table` / `dump_bookkeeper` in [`oeleo/utils.py`](oeleo/utils.py) — already accept `output_format` but only implement `"human"`; TODOs for csv/json/log.
- `FileList` + `SimpleDbHandler` in [`oeleo/models.py`](oeleo/models.py) — fields: `local_name`, `external_name`, `checksum`, `code`, `processed_date`.
- Duplicate dump loop in [`check/developers_playground.py`](check/developers_playground.py) (`dump_oeleo_db_table`) — leave as-is; playground can keep calling library `dump_*`.
- Docs table shape in [`docs/database.md`](docs/database.md) — natural place for a one-liner export example.
- Toolbox (`00-tools/`): empty — no helper to reuse.
- Graph: community around `dump_db` / `SimpleDbHandler` / TODOs — extend existing functions rather than a new module.

## Approach

1. **Row projection** — helper (private) that turns a Peewee queryset into ordered dicts with keys: `id` (pk), `local_name`, `external_name`, `checksum`, `code`, `processed_date` (ISO-ish string via `str(dt)`). Honour existing `code=` filter.
2. **Formats** — `output_format` values:
   - `"human"` — unchanged (log only, return `None`).
   - `"csv"` — header + rows via `csv` stdlib; return the string.
   - `"json"` — `json.dumps(list_of_dicts, indent=2)`; return the string.
   - Unknown format → `ValueError`.
3. **Optional file write** — add `output: Path | str | None = None`. When set and format is csv/json, write the returned string to that path (UTF-8). When unset, caller gets the string only (easy for tests / scripts).
4. **Wire-through** — same kwargs on `dump_db` and `dump_worker_db_table`.
5. **Out of scope** — “dump to log” TODO; leave that TODO or drop it with a note that human mode already logs.
6. **Docs** — expand `dump_db` docstring with formats + example; add a short “Export” subsection to `docs/database.md` (README already links there — no README bloat).

## Files to touch

| Path | Change |
|------|--------|
| `oeleo/utils.py` | Implement csv/json; optional `output`; docstring |
| `docs/database.md` | Short export example |
| `tests/test_dump_db.py` | New: temp SQLite, insert rows, assert csv/json content (+ optional write) |
| `.issueflows/01-current-issues/issue41_status.md` | Status after build |

## Test strategy

- `uv run pytest -m "not ssh"` (and specifically `tests/test_dump_db.py`).
- Temp DB via `tmp_path` + `SimpleDbHandler`: insert 2–3 `FileList` rows (mixed codes), assert CSV header/cells and JSON list shape; assert `code=` filter; assert writing to `output` path; assert human still returns `None` without crashing.

## Open questions

1. **Include `id` (pk) in export columns?** Recommended: **yes** (debug-friendly; matches docs table).
2. **“Dump to log” TODO in scope?** Recommended: **no** — human mode already logs; leave out of this PR.
3. **Return value for csv/json?** Recommended: **return `str`**; write only when `output=` is set (no silent stdout).
