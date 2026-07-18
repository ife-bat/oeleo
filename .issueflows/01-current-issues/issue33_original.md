# Issue #33: Fix register_password to set provided password

Source: https://github.com/ife-bat/oeleo/issues/33

## Original issue text

## Summary
`register_password(pwd)` only prompts when `pwd is None` and never assigns a provided `pwd` to `os.environ`. Call sites like `register_password(os.environ["OELEO_PASSWORD"])` are no-ops.

**Finding ID:** BUG-05  
**Size:** yolo-fit  
**Design doc:** `.issueflows/04-designs-and-guides/code-review-correctness-and-bugs.md`

## Fix direction
Either set `os.environ["OELEO_PASSWORD"]` when `pwd` is provided, or rename to `prompt_password()` and update call sites. Prefer fixing the setter behavior if the name stays.

## Acceptance
- [ ] Providing `pwd` sets the session password env var
- [ ] `pwd is None` still prompts via getpass
- [ ] Call sites behave as expected
