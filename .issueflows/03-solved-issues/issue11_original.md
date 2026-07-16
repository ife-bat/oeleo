# Issue #11: Clear Dependabot alerts: widen black/pytest pins and refresh uv.lock

Source: https://github.com/ife-bat/oeleo/issues/11

## Original issue text

## Summary
Clear open Dependabot security alerts (~29 as of 2026-07-16) by widening blocking pins and upgrading the lockfile.

**Finding ID:** DEP-01  
**Size:** standard (own PR — do not mix with BUG-* logic fixes)  
**Design doc:** `.issueflows/04-designs-and-guides/code-review-dependabot.md`

## Work
- Widen/remove `black<23` and `pytest<8` in `[dependency-groups] dev`
- Bump `python-dotenv>=1.2.2`
- `uv lock --upgrade` (or targeted package upgrades) toward floors: cryptography≥48.0.1, urllib3≥2.7, pillow≥12.2, lxml≥6.1, black≥26.3.1, pytest≥9.0.3
- Run unit tests; SSH job via CI
- Spot-check tray/Pillow import path with `--all-extras`

## Acceptance
- [ ] Open Dependabot alert count drops substantially (ideally only residuals like paramiko SHA-1)
- [ ] `uv run pytest -m "not ssh"` passes
- [ ] CI green

## Related
- Follow-ups: DEP-02, DEP-03
