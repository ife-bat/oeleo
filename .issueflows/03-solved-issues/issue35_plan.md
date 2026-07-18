# Plan: Issue #35 — Reporter default_factory + typing.Protocol

## Goal

Stop sharing one `Reporter` across `Worker` instances, and import `Protocol` from `typing`.

## Approach

- `reporter: ReporterBase = field(default_factory=Reporter)`
- Move `Protocol` into the `typing` import; drop `asyncio.Protocol`
- Unit test: two Workers get distinct reporter objects
- Mark ARCH-02/03 done in architecture design doc

## Files to touch

- `oeleo/workers.py`
- `tests/test_worker_reporter_default.py` (new)
- `.issueflows/04-designs-and-guides/code-review-architecture.md`

## Test strategy

`uv run pytest -m "not ssh"`
