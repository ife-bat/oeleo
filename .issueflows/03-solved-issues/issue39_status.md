# Status: Issue #39 — Raise on SSH list/checksum failure (REL-02)

- [x] Done

## What's done

- Plan accepted (recommended answers applied).
- Added `OeleoTransferError`; SSH `_list_content` raises `OeleoConnectionError` on failure; SSH/SharePoint `calculate_checksum` raise `OeleoTransferError` (no `False` / silent `[]`).
- `Worker.check` notifies + aborts on list failure; per-file checksum transfer errors notify and continue without DB update. `_process_file` notifies on checksum transfer error.
- Unit tests in `tests/test_connector_errors.py`; design docs updated (REL-02 / backlog).
- `uv run pytest -m "not ssh"` — 59 passed.
- Closed via `/iflow-close`; tracking moved to `03-solved-issues`.

## Remaining work

- None.
