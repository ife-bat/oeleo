# Status: Issue #40

- [ ] Done

## What's done

- Added `OeleoShutdown` in `oeleo/connectors.py`; `ScheduleAborted` aliases it.
- `Worker.die_if_necessary` raises `OeleoShutdown` after `close()` (no `sys.exit`).
- `SimpleScheduler.start` catches shutdown on run + sleep poll; skips double-close.
- `app/oa.pyw` catches at single-run and scheduled entry points.
- `LogAndTrayReporter.close` made idempotent (clears `icon` before stop).
- Unit tests in `tests/test_oeleo_shutdown.py`; `uv run pytest -m "not ssh"` green.
- Design docs: REL-04 / backlog #40 marked done.

## Remaining work

- `/iflow-close` (changelog, PR, move issue group when fully done).
