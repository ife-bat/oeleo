# Status: Issue #32

- [ ] Done

## What's done

- Plan accepted (conditional `OELEO_PASSWORD` load; clearer `ValueError` for password path; new unit tests).
- `SSHConnector.__init__`: skip `OELEO_PASSWORD` when `use_password=False`; raise `ValueError` when password auth missing env.
- `SSHConnector.connect`: use `session_password` for password auth; key path unchanged (`OELEO_KEY_FILENAME` only).
- Added `tests/test_ssh_optional_password.py`.
- Updated `tests/README.md` and `.env_example`.
- `uv run pytest -m "not ssh"` — passed.

## Remaining work

- `/iflow-close` (mark Done, commit hygiene, PR finalize).
