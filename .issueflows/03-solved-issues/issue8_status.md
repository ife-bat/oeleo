# Status: Issue #8

- [x] Done

## What's done

- Plan accepted (defaults: retry next scheduler interval; probe at run start + after failed move-retry; minimal SharePoint probe).
- `Connector.ensure_connection()` on Protocol + Local / SSH / SharePoint.
- `Worker._ensure_external_connection` at `run` start and after exhausted move retry; `OeleoConnectionError` not swallowed in chunk handlers.
- `SimpleScheduler` catches connection loss, reports, retries next interval.
- Unit tests (local probe, abort at start, abort mid-run, continue on file-only failure, scheduler retry).
- Operator note in `docs/configuration.md` + design-doc note under REL-02 (partial / #8).
- Implementation landed on `main` via PR #29 (`9545452`).
- `/iflow-close`: `uv run pytest -m "not ssh"` — 47 passed, 4 deselected; issue group archived to `03-solved-issues`.

## Remaining work

- None.
