# Code review: Dependabot / dependency security

See [`code-review-overview.md`](code-review-overview.md) for the index.  
Snapshot date: **2026-07-16** (post-DEP-01 / DEP-02; re-check open alerts on GitHub → Security → Dependabot).

## Status summary

| Track | Issue | Status |
|-------|-------|--------|
| DEP-01 | [#11](https://github.com/ife-bat/oeleo/issues/11) — lock refresh + pin widen | **Done** (merged) |
| DEP-02 | [#12](https://github.com/ife-bat/oeleo/issues/12) — residuals + `poetry.lock` | **Done** (this PR) |
| DEP-03 | [#13](https://github.com/ife-bat/oeleo/issues/13) — grouped Dependabot config | **Done** (`.github/dependabot.yml`) |

**Pre-DEP-01 (2026-07-16):** 29 open alerts (13 high, 13 medium, 3 low), mostly on `uv.lock`, blocked by `black<23` and `pytest<8`.

**Post-DEP-01:** Floors raised, `uv.lock` refreshed; all previously flagged packages now resolve to patched versions (see table below). Open alert count should drop to **zero or paramiko-only** once GitHub re-scans the default branch — confirm on the Security tab (Dependabot API requires elevated token; agent env returned 403).

## Locked versions (post-DEP-01, `main`)

| Package | Locked | Floor | Status |
|---------|--------|-------|--------|
| `cryptography` | 49.0.0 | ≥ 48.0.1 | ✅ patched |
| `urllib3` | 2.7.0 | ≥ 2.7.0 | ✅ patched |
| `pillow` | 12.3.0 | ≥ 12.2.0 | ✅ patched |
| `lxml` | 6.1.1 | ≥ 6.1.0 | ✅ patched |
| `python-dotenv` | 1.2.2 | ≥ 1.2.2 | ✅ patched |
| `black` | 26.5.1 | ≥ 26.3.1 | ✅ patched |
| `pytest` | 9.1.1 | ≥ 9.0.3 | ✅ patched |
| `idna` | 3.18 | ≥ 3.15 | ✅ patched |
| `requests` | 2.34.2 | ≥ 2.33.0 | ✅ patched |
| `pygments` | 2.20.0 | ≥ 2.20.0 | ✅ patched |
| `filelock` | 3.30.0 | ≥ 3.20.3 | ✅ patched |
| `setuptools` | 83.0.0 | ≥ 78.1.1 | ✅ patched |
| `paramiko` | 5.0.0 | — | ⚠️ residual (see below) |

Each package above appears **once** in `uv.lock` (no vulnerable multi-marker branches).

## Residual alerts

### `paramiko` SHA-1 in `rsakey` (expected)

- **Advisory class:** low severity — SHA-1 used in RSA key handling inside paramiko.
- **Locked version:** 5.0.0 (via Fabric 3.2.3).
- **Why it remains:** GitHub Dependabot lists **no patched release** for this advisory at the time of DEP-02. Upgrading within the 5.x line does not clear it.
- **Exposure:** SSH transport for instrument → server file copy. Low practical risk for this use case; still re-check on every lock bump.
- **Action:** Document only — do **not** dismiss without maintainer review. Do not fork paramiko. Track upstream releases.

## `poetry.lock` / legacy Poetry

- **`poetry.lock` on `main`:** confirmed **absent** (2026-07-16). Dependabot should scan only `uv.lock` / `pyproject.toml`.
- **Legacy Poetry references:** `noxfile.py` `pack` session still calls `poetry version` / `poetry export` (TOOL-01, out of scope for DEP-02). Not scanned by Dependabot unless a lockfile is committed.

## Exposure notes (for prioritization)

| Risk | Packages | Comment for agents |
|------|----------|--------------------|
| Runtime SSH/TLS | `cryptography`, `paramiko`, `urllib3`, `requests`, `idna` | Bumped in DEP-01; paramiko SHA-1 may remain |
| SharePoint XML | `lxml` | Bumped in DEP-01 |
| Tray / optional | `pillow` | Bumped in DEP-01; use `uv sync --all-extras` in CI |
| Dev-only | `black`, `pytest`, `filelock`, `Pygments`, `setuptools` | Bumped in DEP-01 |
| Residual | `paramiko` SHA-1 | Document; re-check on lock bumps |

## Completed tracks

### DEP-01 — Security dependency refresh ([#11](https://github.com/ife-bat/oeleo/issues/11))

Widened `black` / `pytest` dev pins, raised `python-dotenv` floor, `uv lock --upgrade`, raised `requires-python` to `>=3.11,<3.13`. Unit tests green (`uv run pytest -m "not ssh"`).

### DEP-02 — Residual / hard cases ([#12](https://github.com/ife-bat/oeleo/issues/12))

| Item | Outcome |
|------|---------|
| `paramiko` SHA-1 | Documented above + GitHub issue comment |
| Multi-version markers in `uv.lock` | None found — single resolved version per package |
| Stale `poetry.lock` | Absent on `main` — no deletion needed |
| Recurring alerts | Deferred to DEP-03 ([#13](https://github.com/ife-bat/oeleo/issues/13)) |

### DEP-03 — Dependabot config ([#13](https://github.com/ife-bat/oeleo/issues/13)) — **Done**

`.github/dependabot.yml` configures weekly grouped updates for the `uv` lockfile (`dev-tools` pattern group + `all-dependencies` catch-all) and `github-actions`. uv groups use `patterns` only — not `dependency-type`.

## What not to do

- Do not dismiss alerts without upgrading when a patch exists.
- Do not pin `cryptography` / `urllib3` as direct deps unless resolution fails — prefer lock refresh via parents (`Fabric` / `requests`).
- Do not mix dependency refreshes with BUG-02 (DB identity epic) or large refactors.
- Do not lower `requires-python`; raise the floor if new wheels require it.

## Verification checklist (for `/iflow-close`)

- [x] `uv lock` / `uv.lock` committed (DEP-01)
- [x] `pyproject.toml` pins allow patched floors (DEP-01)
- [x] Unit CI green (DEP-01 / DEP-02)
- [ ] `gh api …/dependabot/alerts` open count — **maintainer verify** on Security tab (API 403 in agent env)
- [x] This doc + overview updated with residual alerts (DEP-02)

## Related docs

- [`code-review-packaging-and-ops.md`](code-review-packaging-and-ops.md) — toolchain, release
- [`code-review-security.md`](code-review-security.md) — app-level security (SSH quoting, secrets)
- [`code-review-improvement-backlog.md`](code-review-improvement-backlog.md) — ordered work
