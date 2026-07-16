# Plan: Issue #12 — Dependabot residuals (DEP-02)

## Goal

Close out the DEP-01 follow-up: confirm `poetry.lock` is gone, verify the
refreshed `uv.lock` has no vulnerable multi-marker branches, and document any
Dependabot alerts that remain open with no available patch (expected: paramiko
SHA-1).

## Constraints

- **Docs / verification only** — no dependency pin or lock changes unless grep
  finds a genuinely vulnerable locked version still present (unlikely after #11).
- Do not dismiss GitHub alerts without cause; document accepted residuals with
  rationale and upstream tracking.
- Do not implement DEP-03 (`.github/dependabot.yml`) here — that is #13.
- Do not mix BUG-*/SEC-* application fixes into this PR.
- Toolchain unchanged: `uv` for any verification commands.

### Prior art

- None found (toolbox empty; no graphify; grep + design docs checked).
- **#11 (DEP-01)** already raised floors and refreshed `uv.lock`; paramiko
  residuals explicitly deferred to this issue
  ([`issue11_plan.md`](../03-solved-issues/issue11_plan.md)).
- Design guidance:
  [`code-review-dependabot.md`](../04-designs-and-guides/code-review-dependabot.md)
  (DEP-02 table), [`this-project.md`](../04-designs-and-guides/this-project.md).
- **Poetry artifacts:** no `poetry.lock` on `main` or this branch; legacy Poetry
  references remain only in `noxfile.py` `pack` session (TOOL-01, out of scope).

## Approach

1. **Inventory post-DEP-01 lock state (read-only)**
   - Confirm `poetry.lock` absent: `git ls-tree -r origin/main --name-only |
     rg poetry.lock` (expect empty).
   - Grep `uv.lock` for single resolved versions of security-sensitive packages
     and compare to floors from the dependabot doc:

     | Package | Locked (main) | Floor |
     |---------|---------------|-------|
     | cryptography | 49.0.0 | ≥ 48.0.1 |
     | urllib3 | 2.7.0 | ≥ 2.7.0 |
     | pillow | 12.3.0 | ≥ 12.2.0 |
     | lxml | 6.1.1 | ≥ 6.1.0 |
     | python-dotenv | 1.2.2 | ≥ 1.2.2 |
     | black | 26.5.1 | ≥ 26.3.1 |
     | pytest | 9.1.1 | ≥ 9.0.3 |
     | paramiko | 5.0.0 | no patched SHA-1 fix listed |
     | idna | 3.18 | ≥ 3.15 |

   - Grep for duplicate `name = "urllib3"` / old version strings to ensure no
     vulnerable marker branches remain.

2. **Re-check Dependabot open alerts**
   - Preferred: `gh api repos/ife-bat/oeleo/dependabot/alerts --jq '…'`
     (filter `state=="open"`).
   - **Note:** this token may return 403; if so, record “unverified in agent
     env” in status and ask the maintainer to confirm on GitHub → Security →
     Dependabot before merge.
   - Expectation after #11: open count near zero; any survivor likely paramiko
     SHA-1 (low, transitive via Fabric).

3. **Document residuals (primary deliverable)**
   - Update
     [`code-review-dependabot.md`](../04-designs-and-guides/code-review-dependabot.md):
     - Refresh snapshot date and open-alert summary (post-DEP-01).
     - Mark DEP-01 steps as completed; move DEP-02 items to “resolved” or
       “residual” with locked versions.
     - Add a short **Residual alerts** subsection: paramiko SHA-1 advisory, why
       it cannot be fixed in-repo (no patched release), exposure note (SSH key
       handling; low severity), and “re-check on next lock bump”.
     - Note `poetry.lock` confirmed absent — Dependabot should only scan
       `uv.lock` / `pyproject.toml`.
   - Light touch on
     [`code-review-overview.md`](../04-designs-and-guides/code-review-overview.md)
     and
     [`code-review-packaging-and-ops.md`](../04-designs-and-guides/code-review-packaging-and-ops.md)
     to stop citing “29 open alerts” / `black<23` / `pytest<8` (stale
     pre-#11 text).
   - Post a **GitHub issue comment** on #12 summarizing: DEP-01 outcome,
     poetry.lock status, locked versions table, open alert count (or “verify on
     Security tab”), and paramiko residual rationale. Satisfies acceptance
     “documented (issue comment or design doc)” — do both.

4. **No `poetry.lock` deletion commit** unless step 1 finds the file on
   `origin/main` (currently absent — skip).

5. **Status file** — during `/iflow-start`, maintain
   `issue12_status.md` with verification commands run and alert count observed.

## Files to touch

| Path | Change |
|------|--------|
| `.issueflows/04-designs-and-guides/code-review-dependabot.md` | Post-DEP-01 snapshot; residual paramiko note; DEP-02 resolved |
| `.issueflows/04-designs-and-guides/code-review-overview.md` | Update DEP/DEP-02 status blurb (alert count, pins) |
| `.issueflows/04-designs-and-guides/code-review-packaging-and-ops.md` | Update “Dependency health” section (no stale 29-alert / pin text) |
| `.issueflows/01-current-issues/issue12_status.md` | Progress + verification results |
| GitHub issue #12 | Comment with residual summary (via `gh issue comment`) |

**Not expected:** `pyproject.toml`, `uv.lock`, `poetry.lock`, application code.

## Test strategy

No product code changes — run a quick sanity check only:

```bash
uv run pytest -m "not ssh"
```

Optional (if touching docs that reference SSH stack): rely on CI SSH job; no
local Docker required for this issue.

## Open questions

1. **Alert count verification:** Agent environment cannot list Dependabot alerts
   (403). OK to merge after doc + issue comment if maintainer confirms open
   alerts on GitHub Security tab? **Recommended:** yes — note unverified count
   in PR body if API stays blocked.
2. **paramiko dismissal:** If the SHA-1 alert remains open after #11, document
   only (do not dismiss on GitHub) unless the team prefers an explicit
   “risk accepted” dismissal with linked issue comment? **Recommended:**
   document only; dismissal is a maintainer call.
3. **nox Poetry `pack` session:** Out of scope for #12; track under TOOL-01 /
   separate issue? **Recommended:** yes — mention in dependabot doc as
   non-scanning legacy tooling only.
