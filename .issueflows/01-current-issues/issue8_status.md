# Status: Issue #8

- [ ] Done

## What's done

- Plan accepted (defaults: retry next scheduler interval; probe at run start + after failed move-retry; minimal SharePoint probe).

## Remaining work

- Implement `Connector.ensure_connection` (Local / SSH / SharePoint).
- Wire Worker abort + Scheduler catch.
- Unit tests, README note, design-doc note.
- Run `uv run pytest -m "not ssh"`.
