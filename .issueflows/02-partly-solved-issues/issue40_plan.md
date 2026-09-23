# Plan: Issue #40 — catchable shutdown instead of `sys.exit`

## Goal

Replace `sys.exit(0)` in `Worker.die_if_necessary` with a dedicated exception so library callers can catch tray-quit / abort, while `SimpleScheduler` and `app/oa.pyw` still terminate cleanly.

## Constraints

- Keep process exit at the **app boundary only** (or natural process end after scheduler returns); no `sys.exit` on the library tray-quit path.
- Do **not** change debug-only `sys.exit()` helpers in `SSHConnector._check_connection_and_exit` / `check_connection_and_exit` (out of scope; noted in #8 plan).
- Preserve current behavior: on quit, report, `close()` worker/reporter, then stop the run/schedule loop.
- Avoid double-`close()` surprises on the tray reporter (icon already stopped).
- Scope: REL-04 only — no SharePoint / settings / nox work.

### Prior art

- `OeleoConnectionError` / `OeleoTransferError` in [`oeleo/connectors.py`](oeleo/connectors.py) — typed package errors; `SimpleScheduler` already catches `OeleoConnectionError` and retries next interval (mirror catch pattern for shutdown, but **break** instead of retry).
- `ScheduleAborted` in [`oeleo/schedulers.py`](oeleo/schedulers.py) — unused exception already documented as “Raised when the user aborts the run.” Overlaps naming; see Open questions.
- `Worker.die_if_necessary` — [`oeleo/workers.py`](oeleo/workers.py): `reporter.should_die()` → report → `close()` → `sys.exit(0)`. Called from `check` / `run` / `_process_file` and from the scheduler sleep poll.
- `LogAndTrayReporter.should_die` / `kill_me` — tray Quit sets the flag; polled during sleep and mid-run.
- Graph: Community 47 (SimpleScheduler), REL-04 node in correctness community; Suggested Q on `WorkerBase` ↔ `ScheduleAborted`.
- Toolbox: none relevant.

## Approach

1. **Add `OeleoShutdown(Exception)`** next to the other `Oeleo*` errors in `oeleo/connectors.py` (same home as connection/transfer errors; imported by workers/schedulers/app).
2. **`Worker.die_if_necessary`:** if `should_die()`, report, `close()`, then `raise OeleoShutdown(...)` instead of `sys.exit(0)`. Remove the `sys` import from `workers.py` if unused afterward.
3. **`SimpleScheduler.start`:** catch `OeleoShutdown` around `filter_local`/`run` **and** around the sleep-loop `die_if_necessary()` call. On catch: log/report a clean abort, `atexit.unregister(self._cleanup)`, break out of the outer loop **without** treating it as a connection error. Skip a second `worker.close()` if `die_if_necessary` already closed (or make `close` idempotent if a cheap guard is needed).
4. **`app/oa.pyw`:** wrap `single_ssh_connection()` / scheduled `ssh_connection()` so an uncaught `OeleoShutdown` ends the process quietly (log + return / `sys.exit(0)` only at this boundary). Scheduler path should normally return from `start()` after catch; single-run path needs the catch around `worker.run()`.
5. **`ScheduleAborted`:** alias or re-export as `OeleoShutdown` (or subclass) so the unused name is not left as a competing type — see Open questions.
6. **Tests:** unit test that a worker with `reporter.should_die() -> True` raises `OeleoShutdown` and does **not** raise `SystemExit`; optional small scheduler test that sleep-poll quit breaks the loop cleanly.

## Files to touch

| Path | Change |
|------|--------|
| [`oeleo/connectors.py`](oeleo/connectors.py) | Add `OeleoShutdown` |
| [`oeleo/workers.py`](oeleo/workers.py) | Raise `OeleoShutdown`; drop `sys.exit` / unused `sys` |
| [`oeleo/schedulers.py`](oeleo/schedulers.py) | Catch shutdown; relate/retire `ScheduleAborted`; clean break |
| [`app/oa.pyw`](app/oa.pyw) | Catch at app boundary for single-run (and belt-and-suspenders for scheduler) |
| [`tests/`](tests/) (new or extend) | Cover raise-vs-`SystemExit`; optional scheduler break |
| [`.issueflows/04-designs-and-guides/code-review-correctness-and-bugs.md`](.issueflows/04-designs-and-guides/code-review-correctness-and-bugs.md) / backlog | Mark REL-04 / #40 done when closing |

## Test strategy

- `uv run pytest -m "not ssh"` (project default CI path).
- New unit test(s) for `die_if_necessary` → `OeleoShutdown` (no `SystemExit`).
- Existing scheduler/worker tests that mock `should_die.return_value = False` should keep passing.

## Open questions

1. **Exception name / `ScheduleAborted`:** use new **`OeleoShutdown`** (issue text) and make `ScheduleAborted` an alias of it — **recommended**. Alternative: raise `ScheduleAborted` only and skip `OeleoShutdown`.
2. **Who calls `close()`:** keep close inside `die_if_necessary` (current behavior) and teach the scheduler not to double-close — **recommended**. Alternative: raise first and let outer layers close only.
