# Issue #17: Stop reconnecting SSH before every file by default

Source: https://github.com/ife-bat/oeleo/issues/17

## Original issue text

## Summary
`Worker` defaults `reconnect=True` and reconnects the external connector before every file in `_process_file`. For SSH this thrash-opens Fabric sessions (plus retries inside `move_func`) — slow and fragile.

**Finding ID:** REL-01  
**Size:** standard (confirm ops preference)  
**Design doc:** `.issueflows/04-designs-and-guides/code-review-correctness-and-bugs.md`

## Fix direction
Default `reconnect=False`; reconnect only after a failed move (partially already done). Keep an opt-in for flaky networks if needed.

## Acceptance
- [ ] Successful multi-file SSH/local runs do not reconnect per file by default
- [ ] Failed move still retries with reconnect
- [ ] Behavior change noted for operators (changelog / README if relevant)
