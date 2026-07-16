# Code review: Dependabot / dependency security

See [`code-review-overview.md`](code-review-overview.md) for the index.  
Snapshot date: **2026-07-16** (re-check with `gh api repos/:owner/:repo/dependabot/alerts` before implementing).

## Why this is in scope

GitHub reports **29 open** Dependabot alerts on this repo (**13 high**, **13 medium**, **3 low**), almost all against `uv.lock`. Several are blocked by **tight upper bounds** in `pyproject.toml` (notably `black<23` and `pytest<8`). Fixing them is a first-class track alongside correctness bugs — not a separate afterthought.

## Open alerts by package (deduped)

| Package | Alerts | Max severity | Locked (approx.) | Target / note | Role |
|---------|--------|--------------|------------------|---------------|------|
| `urllib3` | 7 | high | 2.2.3 / 2.6.3 (multi-marker) | **≥ 2.7.0** | transitive (requests stack) |
| `pillow` | 6 | high | 10.4 / 11.3 / 12.1 | **≥ 12.2.0** | optional tray (`pystray` / PIL) |
| `cryptography` | 4 | high | 46.0.3 | **≥ 48.0.1** | transitive (paramiko / Fabric) |
| `black` | 2 | high | 22.12.0 | **≥ 26.3.1** | **direct** — blocked by `black>=22.6,<23` |
| `lxml` | 1 | high | 6.0.2 | **≥ 6.1.0** | transitive (SharePlum) |
| `setuptools` | 1 | high | 75.3 / 80.9 | **≥ 78.1.1** (already OK on newer marker?) | transitive / build |
| `python-dotenv` | 1 | medium | 1.0.1 / 1.2.1 | **≥ 1.2.2** | **direct** runtime |
| `pytest` | 1 | medium | 7.4.4 | **≥ 9.0.3** | **direct** — blocked by `pytest>=7.1,<8` |
| `idna` | 1 | medium | 3.11 | **≥ 3.15** | transitive |
| `requests` | 1 | medium | 2.32.x | **≥ 2.33.0** | transitive |
| `filelock` | 2 | medium | mixed; some markers already 3.20.3 | ensure **≥ 3.20.3** everywhere | transitive |
| `Pygments` | 1 | low | 2.19.2 | **≥ 2.20.0** | transitive (rich) |
| `paramiko` | 1 | low | 3.5.1 / 4.0.0 | **no patched release listed** (SHA-1 in rsakey) | transitive (Fabric) |

Dependabot also previously filed against `poetry.lock` (e.g. virtualenv) — treat Poetry lockfiles as **legacy**; keep a single lock source (`uv.lock`) and remove stale Poetry artifacts from the default branch if they still exist remotely.

## Exposure notes (for prioritization)

| Risk | Packages | Comment for agents |
|------|----------|--------------------|
| Runtime SSH/TLS | `cryptography`, `paramiko`, `urllib3`, `requests`, `idna` | Hits instrument → server path; bump early |
| SharePoint XML | `lxml` | XXE class issue in default parsers — bump with SharePoint stack |
| Tray / optional | `pillow` | Only needed with `pystray` / tray reporter; still bump (CI/`--all-extras`) |
| Dev-only | `black`, `pytest`, `filelock`, `Pygments`, `setuptools` | Lower exploit surface on instrument PCs, but CI/dev machines pull them — still clear alerts |
| Residual | `paramiko` SHA-1 | May remain open until upstream ships a fix; document if unresolvable |

## Root cause of stuck alerts

`pyproject.toml` currently pins:

```toml
"black>=22.6.0,<23.0.0",
"pytest>=7.1.2,<8.0.0",
```

Those ceilings **prevent** Dependabot/uv from resolving to patched versions. Any security refresh **must** widen (or drop) those upper bounds and re-lock.

`python-dotenv` has no upper pin — a lock refresh / `uv add "python-dotenv>=1.2.2"` should clear that alert easily.

## Recommended issue-flow plan

### DEP-01 — Security dependency refresh (standard / one PR preferred)

**Goal:** Clear as many open alerts as possible in one coordinated lock bump.

**Steps:**

1. Widen/remove blocking pins in `[dependency-groups] dev`:
   - `black` → current stable (e.g. `>=26.3.1` or unpinned lower bound only).
   - `pytest` → `>=9.0.3` (or `>=8` minimum if 9 breaks something — prefer patched floor).
   - Optionally refresh `nox` / `isort` / `auto-py-to-exe` while here (chore, not security-critical).
2. Bump direct runtime floor: `python-dotenv>=1.2.2`.
3. `uv lock --upgrade` (or targeted `uv lock --upgrade-package …` for the table above).
4. `uv sync --all-extras` and run:
   - `uv run pytest -m "not ssh"`
   - `uv run pytest -m ssh` if Docker SSH available / rely on CI.
5. Spot-check tray import path: `from PIL import Image` / `LogAndTrayReporter` still imports after Pillow 12.2.
6. Confirm Dependabot alerts auto-close or dismiss fixed ones; leave a note for any residual (paramiko).

**Size:** **standard** (not pure yolo — pin changes can break black formatting / pytest APIs).  
**Label:** consider `dependencies` + normal issue-flow; avoid mixing with BUG-01 logic fixes in the same PR.

### DEP-02 — Residual / hard cases (follow-up)

| Item | Action |
|------|--------|
| `paramiko` SHA-1 (no patched version) | Track upstream; if still open after DEP-01, document in this file + GitHub alert comment; do not invent a fork |
| Multi-version markers in `uv.lock` | After upgrade, grep lock for old urllib3/pillow/cryptography lines; eliminate vulnerable marker branches if possible |
| Stale `poetry.lock` on remote | Delete if present so Dependabot stops scanning a second ecosystem |
| Recurring alerts | Add `.github/dependabot.yml` for weekly `uv` / pip ecosystem PRs (grouped) so this does not pile up again |

### DEP-03 — Dependabot config (yolo-fit after DEP-01)

Add Dependabot (or equivalent) config so security bumps arrive as small PRs. Prefer **grouped** updates for transitive noise. Agents should not spam one PR per urllib3 CVE.

## What not to do

- Do not “fix” alerts by dismissing without upgrading when a patch exists.
- Do not pin `cryptography` / `urllib3` as direct deps unless resolution fails — prefer lock refresh via parents (`Fabric` / `requests`).
- Do not mix DEP-01 with BUG-02 (DB identity epic) or large refactors.
- Do not lower `requires-python` further; if a new pillow/cryptography wheel drops old Pythons, **raise** the floor in the same PR and update README/`this-project.md`.

## Verification checklist (for `/iflow-close`)

- [ ] `uv lock` / `uv.lock` committed
- [ ] `pyproject.toml` pins allow patched floors
- [ ] Unit CI green; SSH job green if touched Fabric/paramiko stack
- [ ] `gh api …/dependabot/alerts` open count dropped (ideally to paramiko-only or zero)
- [ ] Overview / this doc updated with residual alerts

## Related docs

- [`code-review-packaging-and-ops.md`](code-review-packaging-and-ops.md) — toolchain, release
- [`code-review-security.md`](code-review-security.md) — app-level security (SSH quoting, secrets)
- [`code-review-improvement-backlog.md`](code-review-improvement-backlog.md) — ordered work
