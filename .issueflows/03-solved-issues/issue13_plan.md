# Plan: Issue #13 — Grouped Dependabot config (DEP-03)

## Goal

Add `.github/dependabot.yml` so uv/pip dependency updates arrive as grouped PRs instead of one per transitive package.

## Constraints

- `uv` ecosystem only for lock updates — do not use `dependency-type` in groups (unsupported for uv).
- Config-only change; no lock or pin edits in this PR.
- Mark DEP-03 done in `code-review-dependabot.md`.

### Prior art

- None found (toolbox empty; no existing `dependabot.yml`).
- Design: [`code-review-dependabot.md`](../04-designs-and-guides/code-review-dependabot.md).

## Approach

1. Create `.github/dependabot.yml` with:
   - `package-ecosystem: uv`, `directory: /`, weekly schedule
   - Groups via `patterns`: `dev-tools` (named dev deps) before `all-dependencies` (`*`) catch-all
   - Optional `github-actions` ecosystem for workflow action bumps (grouped)
2. Update dependabot design doc — DEP-03 status → done
3. Sanity: `uv run pytest -m "not ssh"`

## Files to touch

| Path | Change |
|------|--------|
| `.github/dependabot.yml` | New grouped Dependabot config |
| `.issueflows/04-designs-and-guides/code-review-dependabot.md` | DEP-03 marked done |
| `.issueflows/01-current-issues/issue13_status.md` | Progress |

## Test strategy

```bash
uv run pytest -m "not ssh"
```

No new unit tests (YAML config only).

## Open questions

None — straightforward config per acceptance criteria.
