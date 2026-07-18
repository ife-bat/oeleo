# Issue #39: Raise on SSH list/checksum failure instead of empty/False sentinels

Source: https://github.com/ife-bat/oeleo/issues/39

## Original issue text

## Summary
Soft connector failures become silent skips: SSH `_list_content` catches exceptions and returns `[]`; `calculate_checksum` logs “should raise” but still parses stdout; SharePoint checksum returns `False` on error. Empty remote listing can look like “no files” and drive wrong sync decisions.

**Finding ID:** REL-02  
**Size:** standard  
**Design doc:** `.issueflows/04-designs-and-guides/code-review-correctness-and-bugs.md`

## Related
Destination health probes from #8 (`ensure_connection`) are separate. This issue is about list/checksum error semantics, not connection-lost abort.

## Fix direction
Typed exceptions (`OeleoConnectionError` / `OeleoTransferError`); fail the run or per-file with `reporter.notify`; never return sentinel `False` as a checksum or treat list failure as empty success.

## Acceptance
- [ ] SSH list failure does not look like an empty directory without error status
- [ ] Checksum failures raise or surface via reporter (no `False` sentinel)
- [ ] Unit tests cover negative paths (mock failures)
