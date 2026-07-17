# Code review overview (entry point for agents)

**Date:** 2026-07-16  
**Scope:** Static review of `oeleo` package, `app/`, tests, CI, packaging, and ops scripts.  
**Audience:** Future agents working via **issue-flow** (`iflow pick` / `iflow plan` / `iflow start` / …).

This folder holds durable design memory. Use this file as the **map**; open topic docs only for the area you are changing.

## Read first

1. [`this-project.md`](this-project.md) — what the repo is, how to run/test, conventions.
2. This overview — severity summary and where to dig deeper.
3. The topic doc that matches your issue (links below).
4. When planning work: [`code-review-improvement-backlog.md`](code-review-improvement-backlog.md) for suggested GitHub-issue-sized slices.

Do **not** treat this review as a license to refactor broadly. Prefer small issue-flow issues; cite the finding IDs (e.g. `BUG-01`) in `issue<N>_plan.md`.

## What oeleo is (one paragraph)

`oeleo` is a one-eyed file-transfer toolkit for instrument/lab PCs: filter local files, track checksums in a local SQLite DB, and copy changed files to a destination via local FS, SSH (Fabric), or SharePoint (SharePlum). The Windows app (`app/oa.pyw` → PyInstaller `oeleo_runner`) runs on a scheduler with optional system-tray UI.

## Architecture at a glance

```text
env (.env) → factories (simple_worker / ssh_worker / sharepoint_worker)
                → Worker
                     ├── LocalConnector (source)
                     ├── Connector (dest: Local / SSH / SharePoint)
                     ├── ChecksumChecker
                     ├── SimpleDbHandler (peewee / SQLite)
                     └── Reporter (console / log / tray)
                → SimpleScheduler (optional loop)
```

| Module | Role |
|--------|------|
| `oeleo/workers.py` | Orchestration (`filter` → `check` / `run`) |
| `oeleo/connectors.py` | Transport + remote listing/checksum/copy |
| `oeleo/models.py` | Bookkeeping DB |
| `oeleo/filters.py` | Extension + date/name filters |
| `oeleo/movers.py` | Local copy helpers |
| `oeleo/checkers.py` | Checksum comparison payload |
| `oeleo/schedulers.py` | Interval loop + tray “force run” |
| `oeleo/reporters.py` | User feedback / tray lifecycle |
| `oeleo/utils.py` | Logging, MD5, DB dump helpers |
| `app/oa.pyw` | Production Windows entry |

## Document index

| Document | Contents |
|----------|----------|
| [`this-project.md`](this-project.md) | Project brief for agents (stack, commands, entry points) |
| [`code-review-architecture.md`](code-review-architecture.md) | Structure, coupling, API design, dead code |
| [`code-review-correctness-and-bugs.md`](code-review-correctness-and-bugs.md) | Concrete bugs and reliability issues |
| [`code-review-security.md`](code-review-security.md) | Credentials, remote command construction, trust boundaries |
| [`code-review-testing-and-quality.md`](code-review-testing-and-quality.md) | Coverage gaps, CI, lint/types |
| [`code-review-packaging-and-ops.md`](code-review-packaging-and-ops.md) | Packaging, PyInstaller, nox/poetry drift, deploy |
| [`code-review-dependabot.md`](code-review-dependabot.md) | Open Dependabot alerts, pin blockers, upgrade plan |
| [`code-review-improvement-backlog.md`](code-review-improvement-backlog.md) | Prioritized backlog sized for issue-flow / yolo / epic |

## Severity summary

### Critical / high (fix or decide soon)

| ID | Finding | Topic doc |
|----|---------|-----------|
| ~~DEP-01~~ | ~~29 open Dependabot alerts~~ — **resolved in #11** (lock refresh); residual paramiko SHA-1 documented in DEP-02 | dependabot |
| BUG-01 | Frozen files (`code=2`) are **not** respected in `Worker.run` / `is_changed` | correctness |
| BUG-02 | DB keys files by **basename only** → collisions when `include_subdirs=True` | correctness |
| BUG-03 | `app/oa.pyw` logs `worker.db_path` which **does not exist** on `Worker` | correctness |
| ~~SEC-01~~ | ~~SSH `find` / `md5sum` / `mkdir` string interpolation~~ — **resolved in #18** (`shlex.quote` / `_remote_shell_token`) | security |
| ~~REL-01~~ | ~~`Worker.reconnect=True` reconnects **before every file**~~ — **resolved in #17** (`reconnect=False` default; opt-in via kwarg / `OELEO_RECONNECT`) | correctness |

### Medium

| ID | Finding | Topic doc |
|----|---------|-----------|
| BUG-04 | Peewee `processed_date` default is `datetime.now()` evaluated once at import | correctness |
| BUG-05 | `register_password(pwd)` ignores a provided `pwd` (only prompts when `None`) | correctness |
| BUG-06 | `SharePointConnection.reconnect` calls missing `connect()` | correctness |
| ARCH-01 | Global `database_proxy` → multi-DB / multi-worker unsafe | architecture |
| ARCH-02 | Mutable default `reporter: ReporterBase = Reporter()` on `Worker` dataclass | architecture |
| ARCH-03 | `from asyncio import Protocol` instead of `typing.Protocol` | architecture |
| TEST-01 | Large stubbed test surface; SharePoint untested; many SSH paths only lightly covered | testing |
| TOOL-01 | `noxfile.py` still Poetry-based while project uses `uv` + hatchling | packaging |
| DOC-01 | README vs `pyproject.toml` Python version / build commands drift | packaging |
| ~~DEP-02~~ | Residual Dependabot cases — **resolved in #12** (`poetry.lock` absent; paramiko SHA-1 documented) | dependabot |
| DEP-03 | No Dependabot/grouped auto-update config → alerts pile up | dependabot |

### Low / cleanup

| ID | Finding | Topic doc |
|----|---------|-----------|
| CLEAN-01 | Dead helpers (`base_filter_old`, duplicate `check_connection_and_exit`, unused imports) | architecture |
| CLEAN-02 | Inconsistent logging (`logging` vs `log`), `print` in hot paths | architecture |
| CLEAN-03 | Machine-absolute paths in `oeleo_runner.spec` and example scripts | packaging |
| QUAL-01 | No ruff/mypy/coverage gate in CI | testing |
| SEC-02 | MD5 for change detection (acceptable for sync, not for integrity guarantees) | security |

## Strengths (keep these)

- Clear **connector + worker + bookkeeper** separation; factories (`simple_worker`, `ssh_worker`, `sharepoint_worker`) are the right public API.
- **One-eyed** model is documented and honest; `check()` vs `run()` is a useful operational split.
- Optional tray reporter with **headless fallback** in `app/oa.pyw` (`_has_interactive_desktop`) is production-aware.
- CI runs unit tests and a real **Docker SSH** job (`pytest -m ssh`).
- Dev workflow is already on **`uv`** with a lockfile; issue-flow fits this repo well.

## How agents should use this with issue-flow

1. **`iflow pick`** — prefer items from the backlog that match an open GitHub issue, or create issues from backlog titles.
2. **`iflow plan`** — cite finding IDs; keep scope to one severity band when possible.
3. **`iflow yolo` / label `yolo`** — only for backlog rows marked **yolo-fit**.
4. **`iflow epic`** — use for rows marked **epic** (DB identity, connector hardening, CLI).
5. **DEP-01** and **DEP-02** are done (#11, #12). Next dependency track: **DEP-03** (#13, Dependabot config). Do not mix dependency PRs with logic bugs (BUG-*).
6. After non-trivial decisions, **update the relevant topic doc** (and this overview’s summary table if severity changes).

## Out of scope for this review

- Runtime profiling of large transfer sets.
- SharePoint live behavior against a real tenant.
- Whether SharePlum / Fabric dependency versions are still maintained long-term (flagged only lightly under packaging).
- Filling product roadmap items from README (“web-app”, “GUI”) beyond noting them as non-goals for near-term agent work.
