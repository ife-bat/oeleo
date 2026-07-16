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

- README still shows `pip install oeleo` and `python -m build` / twine; day-to-day is **uv**.
- README: “Python 3.8 support is no longer required” for ≥0.6, but `requires-python = ">=3.8,<3.13"` remains.
- `requirements.txt` at repo root is tiny/legacy relative to `uv.lock`.
- Agents should follow **`uv`** + `pyproject.toml` over README anecdotes when they conflict; fix docs in a dedicated issue.

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

## Dependency health (informational)

- **SharePlum** / older Office365 cookie auth may constrain SharePoint longevity.
- **Fabric** is appropriate for SSH; pin/transitively watch paramiko.
- Dev pins: `black<23`, `pytest<8`, `nox<2024` — consider refreshing in a dedicated chore issue (not mixed with feature work).
