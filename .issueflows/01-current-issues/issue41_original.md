# Issue #41: Implement dump_db CSV/JSON export for bookkeeping DB

Source: https://github.com/ife-bat/oeleo/issues/41

## Original issue text

## Summary
`oeleo.utils` has TODOs around `dump_db` / exporting the bookkeeping DB. Operators need an easy way to inspect transfer state for debugging (README “easy to debug runs” goal).

**Finding ID:** utils TODOs / observability  
**Size:** standard  
**Design doc:** `.issueflows/04-designs-and-guides/code-review-improvement-backlog.md` (P2 Errors & observability)

## Fix direction
Implement CSV and/or JSON export of `FileList` rows (path/key, checksum, code, processed_date). Keep it a small CLI helper or library function callable from scripts; no GUI.

## Acceptance
- [ ] Can export bookkeeping rows to CSV and/or JSON
- [ ] Documented in README or utils docstring
- [ ] Basic unit test on a temp/in-memory DB
