# Issue #34: Remove broken SharePoint reconnect helper and connector __delete__ hooks

Source: https://github.com/ife-bat/oeleo/issues/34

## Original issue text

## Summary
`SharePointConnection.reconnect` calls a missing `connect()` method (footgun). Connector `__delete__` hooks are not Python finalizers (`__del__`) and are dead/wrong. Prefer cleanup via context managers later; for now remove the broken helpers.

**Finding IDs:** BUG-06, CLEAN  
**Size:** yolo-fit  
**Design doc:** `.issueflows/04-designs-and-guides/code-review-correctness-and-bugs.md` and `code-review-architecture.md`

## Fix direction
- Delete or fix `SharePointConnection.reconnect` (connector Protocol `reconnect` already goes through `SharePointConnector.connect`)
- Remove unused `__delete__` methods on connectors
- Do not expand into a full context-manager rewrite in this issue

## Acceptance
- [ ] Broken SharePoint helper is gone or works
- [ ] No `__delete__` hooks left on connectors
- [ ] Existing unit tests still pass (`uv run pytest -m "not ssh"`)
