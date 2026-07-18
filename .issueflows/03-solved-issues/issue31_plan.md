# Plan: Issue #31 — Materialize filter_local results to a list

## Goal

Ensure `Worker.filter_local` always stores a `list` in `file_names` so a second `run()` without re-filtering still sees the same files.

## Approach

- At end of `filter_local`, `local_files = list(...)` (same materialization as `add_local`).
- Unit test: generator from connector → list; double-`run` after one filter still processes files.
- Mark REL-03 done in correctness design doc.

## Files to touch

- `oeleo/workers.py`
- `tests/test_filter_local_materialize.py` (new)
- `.issueflows/04-designs-and-guides/code-review-correctness-and-bugs.md`

## Test strategy

`uv run pytest -m "not ssh"`
