# Issue #36: Delete base_filter_old and unused imports

Source: https://github.com/ife-bat/oeleo/issues/36

## Original issue text

## Summary
`filters.py` still has `base_filter_old`, and `workers.py` carries unused imports (`multiprocessing`, Rich `Panel`/`Text`, `ceil`, …). Dead code noise for agents and readers.

**Finding ID:** CLEAN-01  
**Size:** yolo-fit  
**Design doc:** `.issueflows/04-designs-and-guides/code-review-architecture.md`

## Fix direction
Confirm `base_filter_old` is unused, delete it, and trim clearly unused imports in files you touch. No behavior change.

## Acceptance
- [ ] `base_filter_old` removed
- [ ] Unused imports cleaned in touched modules
- [ ] `uv run pytest -m "not ssh"` green
