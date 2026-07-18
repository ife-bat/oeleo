# Status: Issue #8

- [ ] Done

## What's done

- Plan accepted (defaults: retry next scheduler interval; probe at run start + after failed move-retry; minimal SharePoint probe).
- `Connector.ensure_connection()` on Protocol + Local / SSH / SharePoint.
- `Worker._ensure_external_connection` at `run` start and after exhausted move retry; `OeleoConnectionError` not swallowed in chunk handlers.
- `SimpleScheduler` catches connection loss, reports, retries next interval.
- Unit tests (local probe, abort at start, abort mid-run, continue on file-only failure, scheduler retry).
- README operator note + design-doc note under REL-02 (partial / #8).
- `uv run pytest -m "not ssh"` — 35 passed, 4 deselected.

## Remaining work

- `/iflow-close` (mark Done, commit hygiene, PR finalize).
