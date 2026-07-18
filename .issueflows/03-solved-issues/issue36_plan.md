# Plan: Issue #36 — Delete base_filter_old and unused imports

## Goal

Remove dead `base_filter_old` and unused imports in touched modules with no behavior change.

## Approach

- Delete `base_filter_old` from `filters.py` (confirmed unused).
- Trim unused imports from `workers.py`: multiprocessing/Process/Queue, ceil, Rich Panel/Text/Progress helpers, unused `Generator` typing.
- Mark CLEAN-01 items done in architecture design doc.
- Rely on existing unit suite (no behavior tests needed).

## Files to touch

- `oeleo/filters.py`
- `oeleo/workers.py`
- `.issueflows/04-designs-and-guides/code-review-architecture.md`

## Test strategy

`uv run pytest -m "not ssh"`
