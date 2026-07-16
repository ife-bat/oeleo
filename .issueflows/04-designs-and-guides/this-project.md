# oeleo

## What this project is

`oeleo` (“one-eyed”) copies files from an instrument or lab PC to a destination (local folder, SSH host, or SharePoint), tracking transfer state only on the **local** side via a SQLite bookkeeping DB keyed by checksum changes. Primary users are researchers / lab operators (IFE context) who need reliable, schedule-friendly sync without a full bidirectional sync product.

## Stack / runtime

- **Language:** Python (`requires-python = ">=3.11,<3.13"` in `pyproject.toml`; develop with **3.11+**; CI uses **3.12**).
- **Package manager:** **`uv`** (`uv.lock` present). Prefer `uv run` / `uv sync` — do **not** assume Poetry for day-to-day work (`noxfile.py` still mentions Poetry; treat that as legacy).
- **Build backend:** hatchling.
- **Core deps:** peewee, python-dotenv, rich, Fabric, SharePlum; optional `pystray` via `[project.optional-dependencies] all`.
- **App packaging:** PyInstaller (`oeleo_runner.spec`, `app/oa.pyw`), `auto-py-to-exe` as a dev helper.
- **External services:** SSH servers (Fabric/paramiko); Microsoft SharePoint (SharePlum/Office365); local Docker OpenSSH for integration tests.
- **Quality tools (dev):** pytest, black, isort, nox (legacy pack session). No mypy/ruff configured yet.

## How to run / test

```bash
# Install / sync (with tray extras when building the Windows app)
uv sync
uv sync --all-extras   # when you need pystray

# Unit tests (default CI path)
uv run pytest -m "not ssh"

# SSH integration tests (needs Docker SSH — see tests/README.md)
source ./set-ssh-env.sh   # or set OELEO_SSH_TESTS=1 and OELEO_* vars
uv run pytest -m ssh

# Format (project historically uses black + isort; not enforced in CI)
uv run black oeleo tests app
uv run isort oeleo tests app
```

Config is via **environment variables** / `.env` (see `.env_example` and README). Never commit `.env`.

## Conventions

- Issue work goes through **issue-flow** (`.issueflows/`, `iflow …` skills). Focus issue only under `01-current-issues`.
- Branch names: `<N>-<short-slug>`. Assume squash-merges; use `iflow cleanup` after merge.
- Before planning/implementing, skim `.issueflows/04-designs-and-guides/` — especially [`code-review-overview.md`](code-review-overview.md). Dependency/security bumps: [`code-review-dependabot.md`](code-review-dependabot.md).
- Public composition API: factories in `oeleo/workers.py` + `Worker` methods `connect_to_db` → `filter_local` → (`check`) → `run` → `close`.
- Logging: package logger name `"oeleo"`; prefer `start_logger(...)` from `oeleo.utils`.
- **Multi-root workspaces:** this repo uses **uv**, not conda. Sibling repos may differ — keep toolchain notes here.

## Release & version bump

- **Static version (uv):** `[project] version` lives in `pyproject.toml` (currently `0.7.0`).
- Bump with `uv version --bump <level>` before the release commit when closing a release-oriented issue.
- Publish historically via build + twine (README); keep PyPI tokens out of the repo.

## Entry points

| Path | Purpose |
|------|---------|
| `oeleo/workers.py` | Factories + `Worker` orchestration |
| `oeleo/connectors.py` | Local / SSH / SharePoint connectors |
| `oeleo/models.py` | Peewee `FileList` + `SimpleDbHandler` |
| `oeleo/main.py` | Example / scratch runners (not the shipped app) |
| `app/oa.pyw` | Windows scheduled / tray app |
| `oeleo_runner.spec` | PyInstaller one-file windowed build |
| `install_task.ps1` | Register Windows scheduled task for `dist\oeleo_runner.exe` |
| `tests/` | pytest unit + SSH integration |

Agent onboarding docs: [`code-review-overview.md`](code-review-overview.md).

## Non-goals / known limitations

- **One-eyed only:** destination is not the source of truth; deleting remote files is not mirrored locally.
- Not a general sync/backup product (no bidirectional sync, no conflict UI).
- SharePoint support is thinner than local/SSH (filters incomplete; few automated tests).
- Threaded `Worker.run` path exists but is disabled (`use_threads = False`).
- Near-term agent work should prefer hardening existing transfer/DB paths over new GUI/web-app features (README “future” list).
