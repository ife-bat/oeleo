# Plan: Issue #8 — Ensure connection

## Goal

Stop oeleo from quietly continuing a transfer run when the **destination** connection is gone. Detect loss, report it, and abort the current run instead of marking every remaining file `!` and looping forever.

## Constraints

- Scope is **connection health for the external (destination) connector** during `Worker.run` / scheduled loops — not a full REL-02 connector-error rewrite (SSH list/checksum soft failures stay a follow-up).
- Do not change tray quit / `die_if_necessary` → `sys.exit` (REL-04) in this PR.
- Keep #17 behavior: default `reconnect=False`; failed moves still reconnect once and retry.
- Public API stays composition-friendly (`Worker` + connectors); prefer a small Protocol method over ad-hoc checks only in `Worker`.
- Unit tests via `uv run pytest -m "not ssh"`; no new Docker SSH requirement for the happy path.
- Cite #8 / connection-ensure in status and a short design-doc note when closing.

### Prior art

- `OeleoConnectionError` — [`oeleo/connectors.py`](oeleo/connectors.py): already raised from `SSHConnector.reconnect` on close/connect failure.
- `Connector` Protocol — `connect` / `reconnect` / `close` / `move_func`; no health probe today.
- `SSHConnector._check_connection_and_exit` / `check_connection_and_exit` — debug-only probes that `sys.exit()`; keep as-is or leave unused (CLEAN-01); do **not** call from production path.
- `Worker._process_file` — failed `move_func` → reconnect + retry → report `!` and continue; `_process_single_chunk` swallows exceptions into `failed_files`.
- `SimpleScheduler.start` — infinite interval loop; only aborts via `die_if_necessary` (tray) or `max_run_intervals`.
- `LocalConnector` / `simple_mover` — destination missing/unwritable → `False`, no abort.
- Design: REL-02 / REL-04 in [`code-review-correctness-and-bugs.md`](.issueflows/04-designs-and-guides/code-review-correctness-and-bugs.md) — related but **not** this issue’s acceptance.
- Toolbox: none. Graph: none.

## Approach

1. **Protocol probe** — Add `ensure_connection(self) -> None` on `Connector`. Success = no-op return; failure = raise `OeleoConnectionError` (reuse existing type).
   - **LocalConnector:** destination `directory` must exist and be a directory (and ideally accessible — `os.access` / `stat`). Missing network mount / deleted folder → raise.
   - **SSHConnector:** lightweight remote probe (reuse the find/dir idea from the debug helpers **without** `sys.exit`); treat Fabric/transport failure as connection lost.
   - **SharePointConnector:** minimal probe (e.g. touch `self.connection.folder` / list once); Shareplum errors → raise. Keep small; no SharePoint rewrite.
2. **Worker abort path** — Introduce a clear abort signal (raise `OeleoConnectionError` out of `run`, or a thin `OeleoAborted` alias — prefer reusing `OeleoConnectionError`):
   - Call `external_connector.ensure_connection()` at the **start of `run()`**.
   - After a failed move + reconnect-retry still fails, call `ensure_connection()` again; if that raises, **stop the run** (do not process remaining files). If the probe still passes, keep current per-file `!` behavior (file-level failure, connection OK).
   - Notify via `reporter.report` / `reporter.notify` with a clear message before aborting.
   - Ensure `_process_single_chunk` / `run` do **not** swallow `OeleoConnectionError` into “failed file and continue”.
3. **Scheduler** — In `SimpleScheduler.start`, catch `OeleoConnectionError` around `filter_local`/`run`: report, then **skip to the next sleep interval** (recommended) so a transient outage does not kill the Windows scheduled app. Document that the process stays alive unless the operator uses tray quit.
4. **Tests** — Mock external connector: (a) `ensure_connection` fails at run start → no `move_func`; (b) first moves succeed, then move fails and `ensure_connection` fails → remaining files not processed; (c) move fails but `ensure_connection` OK → continue with `!` for that file only.
5. **Docs** — Short README / design note: destination loss aborts the current run; scheduler retries next interval.

## Files to touch

| Path | Change |
|------|--------|
| [`oeleo/connectors.py`](oeleo/connectors.py) | `ensure_connection` on Protocol + Local / SSH / SharePoint implementations |
| [`oeleo/workers.py`](oeleo/workers.py) | Probe at `run` start + after exhausted move retry; propagate `OeleoConnectionError` |
| [`oeleo/schedulers.py`](oeleo/schedulers.py) | Catch connection loss; notify; continue to next interval |
| [`tests/test_oeleo.py`](tests/test_oeleo.py) (or `tests/test_ensure_connection.py`) | Unit tests with mocks as above |
| [`README.md`](README.md) | Operator note (brief) |
| [`.issueflows/04-designs-and-guides/code-review-correctness-and-bugs.md`](.issueflows/04-designs-and-guides/code-review-correctness-and-bugs.md) | Optional short “#8 / connection ensure” note; leave REL-02 open |

## Test strategy

- Command: `uv run pytest -m "not ssh"`.
- Focused unit tests with mocked `external_connector.ensure_connection` / `move_func` (same style as #17 reconnect tests).
- No new SSH integration case required for acceptance; optional later.

## Open questions

1. **After connection loss in the scheduler, sleep until next interval (recommended) or stop the whole scheduler / process?** Recommended: **sleep and retry next interval** — matches lab PCs that lose VPN/mount temporarily. Alternative: hard stop (closer to issue’s “crash if needed”).
2. **Probe frequency:** start of `run` + after failed move-retry (recommended), or also every chunk (`n=20`)? Recommended: **start + post-failure** — enough for #8 without probing before every file.
3. **SharePoint in this PR?** Recommended: **yes, minimal probe** so Protocol is complete; keep SharePoint logic tiny. Alternative: Local + SSH only and stub SharePoint as no-op/`NotImplemented` (weaker).

## Scope check

One concern, few modules, no unrelated refactors. Fits one PR. REL-02 (soft SSH list/checksum failures) and REL-04 (`sys.exit` in `die_if_necessary`) stay separate.
