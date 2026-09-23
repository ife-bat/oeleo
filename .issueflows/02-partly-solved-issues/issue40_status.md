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

- `/iflow-close` (changelog, finalize PR with Closes #40, move issue group when fully done).

## Notes

- Branch renamed to `cursor/40-catchable-shutdown-exception-eca3` for cloud PR tooling.
- Draft PR opened during build (early_pr off; cloud agent required a PR).
