# Issue #12: Document residual Dependabot cases; remove stale poetry.lock if present

Source: https://github.com/ife-bat/oeleo/issues/12

## Original issue text

## Summary
After DEP-01, handle leftovers: paramiko SHA-1 (no patched release listed), any remaining vulnerable lock markers, and stop Dependabot scanning a legacy `poetry.lock` if it still exists on the default branch.

**Finding ID:** DEP-02  
**Size:** yolo-fit  
**Depends on:** DEP-01  
**Design doc:** `.issueflows/04-designs-and-guides/code-review-dependabot.md`

## Acceptance
- [ ] Residual alerts documented (issue comment or design doc)
- [ ] Stale `poetry.lock` removed from default branch if present
