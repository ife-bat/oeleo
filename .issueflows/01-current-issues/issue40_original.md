# Issue #40: Replace sys.exit in die_if_necessary with a catchable exception

Source: https://github.com/ife-bat/oeleo/issues/40

## Original issue text

## Summary
Tray quit → `die_if_necessary` calls `sys.exit(0)` from deep inside the worker. Hard to test and surprising when `oeleo` is used as a library.

**Finding ID:** REL-04  
**Size:** standard  
**Design doc:** `.issueflows/04-designs-and-guides/code-review-correctness-and-bugs.md`

## Fix direction
Raise a dedicated exception (e.g. `OeleoShutdown`) caught by `SimpleScheduler` / `app/oa.pyw`. Keep process exit at the app boundary only.

## Acceptance
- [ ] Library path does not call `sys.exit` for tray quit
- [ ] Scheduler/app still terminate cleanly on quit
- [ ] Behavior covered by a unit test where feasible
