# Plan: Issue #34 — Remove broken SharePoint reconnect / `__delete__`

## Goal

Remove the broken `SharePointConnection.reconnect` footgun and dead connector `__delete__` hooks without a context-manager rewrite.

## Approach

- Delete `SharePointConnection.reconnect` (Protocol `SharePointConnector.reconnect` → `close`+`connect` remains).
- Delete `__delete__` on `SSHConnector` and `SharePointConnector`.
- Unit test: helpers absent; suite still green.
- Mark BUG-06 / destructor note done in design docs.

## Files to touch

- `oeleo/connectors.py`
- `tests/test_connector_cleanup_hooks.py` (new)
- `.issueflows/04-designs-and-guides/code-review-correctness-and-bugs.md`
- `.issueflows/04-designs-and-guides/code-review-architecture.md`

## Test strategy

`uv run pytest -m "not ssh"`
