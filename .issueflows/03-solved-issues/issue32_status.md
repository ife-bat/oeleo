# Status: Issue #32

- [x] Done

## What's done

- Plan accepted (conditional `OELEO_PASSWORD` load; clearer `ValueError` for password path; new unit tests).
- `SSHConnector.__init__`: skip `OELEO_PASSWORD` when `use_password=False`; raise `ValueError` when password auth missing env.
- `SSHConnector.connect`: use `session_password` for password auth; key path unchanged (`OELEO_KEY_FILENAME` only).
- Added `tests/test_ssh_optional_password.py`.
- Updated `tests/README.md`, `.env_example`, and SEC-03 design note.
- `uv run pytest -m "not ssh"` — 39 passed, 4 deselected.
- Closed via `/iflow-close` (no version bump; no `HISTORY.md` in repo).

## Remaining work

- None.
