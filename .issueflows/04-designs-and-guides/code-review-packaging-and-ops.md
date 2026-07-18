# Code review: packaging, tooling & ops

See [`code-review-overview.md`](code-review-overview.md) for the index.

## Packaging (library)

| Item | Current | Notes |
|------|---------|-------|
| Build | hatchling via `pyproject.toml` | Good |
| Lock | `uv.lock` | Source of truth for agents |
| Version | static `0.7.0` in `[project]` | Bump with `uv version --bump` |
| Entry points | None (`console_scripts`) | CLI still wishlist |
| Optional deps | `all` → pystray | App needs `uv sync --all-extras` |
| Classifiers / keywords | Present | keywords `ssh`, `db` OK |

### DOC-01 — Docs/toolchain drift

**Resolved in #19** (floor raised earlier in #11): README Development uses `uv sync` / `uv run` / `uv build` / `uv publish`, and states `requires-python = ">=3.11,<3.13"`. Consumer install remains `pip install oeleo` from PyPI.

Still open / related:

- `requirements.txt` at repo root is tiny/legacy relative to `uv.lock`.
- Prefer **`uv`** + `pyproject.toml` if any remaining doc anecdotes disagree.

## Windows app / PyInstaller

| Item | Current | Issue |
|------|---------|-------|
| Entry | `app/oa.pyw` | Production path for instrument PCs |
| Spec | `oeleo_runner.spec` | **Absolute** paths to this developer machine (CLEAN-03) |
| `.gitignore` | ignores `*.spec` | Spec may be local-only — document canonical build recipe in `app/readme.md` |
| Tray / headless | `_has_interactive_desktop` | Good for Task Scheduler session 0 |
| Task install | `install_task.ps1` | Expects `dist\oeleo_runner.exe` beside script |

**Improvements:**

1. Make the spec relative (`app/oa.pyw`, `app/oeleo.ico`) or generate via a small `uv run` script.
2. Decide whether to **track** a portable `.spec` (force-add) or keep auto-py-to-exe `config.json` as source of truth.
3. Smoke-test checklist after build: single-run, scheduler, missing `.env` error path.

## Legacy packing (TOOL-01)

`noxfile.py` `pack` session shells out to **Poetry** (`poetry version`, `poetry export`) and downloads wheels for offline install. The project build backend is hatchling/uv — this session is likely stale.

**Options:**

- Rewrite pack around `uv export` / `uv build`, or
- Delete/archive with a note in `00-tools` if unused.

Do not run `nox -s pack` expecting it to match current packaging without verification.

## Ops artifacts in repo

| Path | Concern |
|------|---------|
| `oeleo.log`, `test_app.db` at root | Local runtime artifacts; ensure gitignored (`.log` is; `/*.db` is) |
| `check/`, `output/`, `dist/`, `build/` | Dev/demo trees |
| `.env` | Must stay untracked |

## Version & release workflow for issue-flow

1. Implement on issue branch.
2. On `iflow close`, bump version only when the change is user-facing/release-worthy (skill reads this-project “Release & version bump”).
3. Publish remains a human/ops step (PyPI token); agents prepare the bump + changelog note, don’t upload secrets.

## Dependency health & Dependabot

- **DEP-01 done (#11):** `uv.lock` refreshed; `black>=26.3.1`, `pytest>=9.0.3`, `python-dotenv>=1.2.2`; `requires-python = ">=3.11,<3.13"`.
- **DEP-02 done (#12):** `poetry.lock` confirmed absent on `main`; residual paramiko SHA-1 documented (no patched release). See [`code-review-dependabot.md`](code-review-dependabot.md).
- **DEP-03 done (#13):** grouped `.github/dependabot.yml` for uv/pip.
- **SharePlum** / older Office365 cookie auth may constrain SharePoint longevity (also pulls `lxml`) — product decision in [#45](https://github.com/ife-bat/oeleo/issues/45).
- **Fabric** → paramiko 5.0.0 / cryptography 49.0.0; paramiko SHA-1 advisory may remain open until upstream fix.
- Legacy `noxfile.py` `pack` session still references Poetry ([#48](https://github.com/ife-bat/oeleo/issues/48) TOOL-01) — not a Dependabot scan target without a committed lockfile.
