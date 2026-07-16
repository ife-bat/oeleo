# Status: Issue #17

- [ ] Done

## What's done

- Plan confirmed (default `reconnect=False`; kwarg + `OELEO_RECONNECT` opt-in).
- `Worker.reconnect` default flipped to `False`; docstring clarified.
- `resolve_reconnect()` + factory kwarg/`OELEO_RECONNECT` on `simple_worker`, `ssh_worker`, `sharepoint_worker`.
- Failure-path reconnect+retry left unconditional.
- README + `.env_example` operator docs.
- Unit tests for per-file skip/opt-in, fail-path reconnect, env/kwarg resolution.
- Design docs: REL-01 marked done (overview, correctness, backlog).

## Remaining work

- Run `uv run pytest -m "not ssh"` and confirm green.
- `/iflow-close` (PR merge, archive tracking, version bump decision).
