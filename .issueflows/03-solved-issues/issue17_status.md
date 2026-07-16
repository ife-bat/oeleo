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
- `uv run pytest -m "not ssh"` — 25 passed (incl. 5 new reconnect tests).

## Remaining work

- `/iflow-close` (confirm Done, PR merge/archive, version bump decision).
