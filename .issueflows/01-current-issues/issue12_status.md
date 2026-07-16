# Status: Issue #12

- [ ] Done

## What's done

- Verified `poetry.lock` absent on `origin/main` (no deletion needed).
- Verified single resolved versions in `uv.lock` for all security-sensitive packages; all meet patched floors from DEP-01.
- Dependabot API: 403 in agent env — open alert count unverified here; maintainer should confirm on GitHub Security tab.
- Updated design docs:
  - `code-review-dependabot.md` — post-DEP-01 snapshot, residual paramiko note, DEP-02 resolved
  - `code-review-overview.md` — DEP-01/DEP-02 marked done
  - `code-review-packaging-and-ops.md` — dependency health section refreshed
- Posted summary comment on GitHub issue #12.
- `uv run pytest -m "not ssh"` — 20 passed, 3 deselected.

## Remaining work

- `/iflow-close`: commit, push, PR; maintainer confirms Dependabot alert count on Security tab and posts issue comment if desired (API blocked in agent env).

## Verification notes

| Package | Locked | Floor | OK |
|---------|--------|-------|-----|
| cryptography | 49.0.0 | ≥ 48.0.1 | yes |
| urllib3 | 2.7.0 | ≥ 2.7.0 | yes |
| pillow | 12.3.0 | ≥ 12.2.0 | yes |
| lxml | 6.1.1 | ≥ 6.1.0 | yes |
| python-dotenv | 1.2.2 | ≥ 1.2.2 | yes |
| black | 26.5.1 | ≥ 26.3.1 | yes |
| pytest | 9.1.1 | ≥ 9.0.3 | yes |
| idna | 3.18 | ≥ 3.15 | yes |
| paramiko | 5.0.0 | no SHA-1 patch | residual — documented |
