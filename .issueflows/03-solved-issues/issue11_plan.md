# Plan: Issue #11 — Dependabot / lock refresh (DEP-01)

## Goal

Clear as many open Dependabot security alerts as possible by widening blocking
dev pins, raising the `python-dotenv` floor, and refreshing `uv.lock` — without
mixing in application logic fixes (BUG-*).

## Constraints

- Own PR / this branch only: `pyproject.toml`, `uv.lock`, and minimal doc touch-ups
  if `requires-python` must rise. No BUG-*/SEC-* code changes.
- Prefer transitive upgrades via lock refresh; add direct pins for
  `cryptography` / `urllib3` / etc. only if resolution cannot reach patched floors.
- Do not dismiss alerts without upgrading when a patch exists.
- Do not reformat the whole tree with the new Black in this PR (noise).
- Residual `paramiko` SHA-1 (no patched release) is out of scope → leave for #12
  (DEP-02). Dependabot config → #13 (DEP-03).
- Toolchain: `uv` only (`uv add` / `uv lock` / `uv sync` / `uv run pytest`).

### Prior art

- None found (toolbox empty; no graphify; no existing upgrade helper scripts).
- Design guidance: [`code-review-dependabot.md`](../04-designs-and-guides/code-review-dependabot.md),
  [`this-project.md`](../04-designs-and-guides/this-project.md).
- Blocking pins live in [`pyproject.toml`](../../pyproject.toml) `[dependency-groups] dev`.

## Approach

1. **Edit floors in `pyproject.toml`**
   - Runtime: `python-dotenv>=1.2.2` (was unpinned).
   - Dev: replace `black>=22.6.0,<23.0.0` with `black>=26.3.1`.
   - Dev: replace `pytest>=7.1.2,<8.0.0` with `pytest>=9.0.3`.
   - Leave `isort` / `nox` / `auto-py-to-exe` alone unless the lock resolve forces
     a bump (keep PR focused).

2. **Refresh lock**
   - `uv lock --upgrade` (full refresh preferred for clearing multi-marker
     vulnerable branches).
   - If full upgrade is too noisy or fails, fall back to targeted:
     `uv lock --upgrade-package cryptography --upgrade-package urllib3
     --upgrade-package pillow --upgrade-package lxml --upgrade-package idna
     --upgrade-package requests --upgrade-package pygments
     --upgrade-package filelock --upgrade-package setuptools`
     plus the direct packages above.
   - Verify locked versions meet floors (grep `uv.lock`): cryptography≥48.0.1,
     urllib3≥2.7.0, pillow≥12.2.0, lxml≥6.1.0, python-dotenv≥1.2.2,
     black≥26.3.1, pytest≥9.0.3, idna≥3.15, requests≥2.33.0.

3. **Python floor (only if needed)**
   - If the new resolve cannot satisfy `requires-python = ">=3.8,<3.13"`,
     raise the lower bound (prefer `>=3.10` or `>=3.11` to match README/CI)
     and note it in the PR + a one-line update to `this-project.md` / README
     only if we change it. Do **not** lower the upper bound casually; keep
     `<3.13` unless wheels require otherwise.

4. **Verify**
   - `uv sync --all-extras`
   - `uv run pytest -m "not ssh"`
   - Import smoke: `uv run python -c "from PIL import Image; from oeleo.reporters import LogAndTrayReporter"`
   - Re-check alert count:
     `gh api repos/ife-bat/oeleo/dependabot/alerts --jq '[.[]|select(.state=="open")]|length'`
     (alerts may lag until the lock is on the default branch; still record
     expected resolved packages in status).
   - SSH job: rely on CI after push, or run locally if Docker SSH is up.

5. **Status / docs**
   - Write `issue11_status.md` during `/iflow-start` with residual alerts noted.
   - Do not implement DEP-02/DEP-03 here.

## Files to touch

| Path | Change |
|------|--------|
| `pyproject.toml` | Floor bumps for `python-dotenv`, `black`, `pytest`; maybe `requires-python` |
| `uv.lock` | Regenerated |
| `.issueflows/04-designs-and-guides/this-project.md` | Only if Python floor changes |
| `README.md` | Only if Python floor / install note must match (minimal) |
| `.issueflows/01-current-issues/issue11_status.md` | Progress during start/close |

## Test strategy

```bash
uv sync --all-extras
uv run pytest -m "not ssh"
# optional / CI:
uv run pytest -m ssh
```

No new unit tests expected (dependency-only change). If pytest 9 breaks an
existing test due to API/config, fix the minimal test/config adaptation in this
PR (not product logic).

## Open questions

1. **Python floor:** If the upgrade forces dropping 3.8/3.9, OK to set
   `requires-python = ">=3.11,<3.13"` (align with README “develop on 3.11” + CI 3.12)?
   **Recommended:** yes.
2. **Black reformat:** Keep this PR lock-only (no repo-wide `black .`)?
   **Recommended:** yes — formatting can be a follow-up if desired.
