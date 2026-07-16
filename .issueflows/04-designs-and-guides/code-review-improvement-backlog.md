# Code review: improvement backlog (issue-flow ready)

Use this list when creating or picking GitHub issues. Cite finding IDs in `issue<N>_plan.md`.  
Entry point: [`code-review-overview.md`](code-review-overview.md).

**Legend**

- **yolo-fit** — small, low-risk; suitable for `iflow yolo` / label `yolo` after green tests.
- **standard** — needs explicit `iflow plan` confirmation; one PR.
- **epic** — use `iflow epic`; split into staged issues.

---

## P0 — Dependabot / dependency security (parallel track)

Do this as a **dedicated PR**, not mixed with BUG-* logic fixes. Details: [`code-review-dependabot.md`](code-review-dependabot.md).

| GitHub | Title | IDs | Size | Notes |
|--------|-------|-----|------|-------|
| [#11](https://github.com/ife-bat/oeleo/issues/11) | Clear Dependabot alerts: widen black/pytest pins + refresh uv.lock | DEP-01 | **standard** | ~29 open alerts; floors: cryptography≥48.0.1, urllib3≥2.7, pillow≥12.2, lxml≥6.1, python-dotenv≥1.2.2, black≥26.3.1, pytest≥9.0.3 |
| [#12](https://github.com/ife-bat/oeleo/issues/12) | Document residual Dependabot cases; remove stale poetry.lock if present | DEP-02 | **yolo-fit** | After DEP-01 · label `yolo` |
| [#13](https://github.com/ife-bat/oeleo/issues/13) | Add grouped Dependabot config for uv/pip | DEP-03 | **yolo-fit** | Prevent recurrence · label `yolo` |

## P0 — Correctness (do first / can interleave with DEP-01)

| GitHub | Title | IDs | Size | Notes |
|--------|-------|-----|------|-------|
| [#15](https://github.com/ife-bat/oeleo/issues/15) | Honor bookkeeping `code=2` (locked) during `Worker.run` | BUG-01 | **yolo-fit** | Unit test required · label `yolo` |
| [#14](https://github.com/ife-bat/oeleo/issues/14) | Fix `OA_SINGLE_RUN` crash: replace `worker.db_path` | BUG-03 | **yolo-fit** | Log `bookkeeper.db_name` · label `yolo` |
| [#16](https://github.com/ife-bat/oeleo/issues/16) | Peewee `processed_date` default must be callable | BUG-04 | **yolo-fit** | One-liner + test · label `yolo` |
| [#17](https://github.com/ife-bat/oeleo/issues/17) | Stop reconnecting SSH before every file by default | REL-01 | **standard** | Confirm ops preference; reconnect-on-failure only |

## P1 — Data model & identity

| Title | IDs | Size | Notes |
|-------|-----|------|-------|
| Bookkeep by relative path, not basename | BUG-02 | **epic** | Migration + subdir tests; stages: schema, write path, migrate tool, docs |
| Materialize `filter_local` results to a list | REL-03 | **yolo-fit** | Prevents empty second `run` |

## P1 — Security / SSH hardening

| GitHub | Title | IDs | Size | Notes |
|--------|-------|-----|------|-------|
| [#18](https://github.com/ife-bat/oeleo/issues/18) | Shell-safe remote path handling in `SSHConnector` | SEC-01 | **standard** | `shlex.quote` or avoid shell; tests with spaces |
| — | Make `OELEO_PASSWORD` optional for key-based SSH | SEC-03 | **yolo-fit** | Don’t require env when `use_password=False` · *not filed yet* |

## P2 — API cleanup

| Title | IDs | Size | Notes |
|-------|-----|------|-------|
| Fix `register_password` to set provided password | BUG-05 | **yolo-fit** | Or rename to `prompt_password` |
| Remove broken `__delete__` / SharePoint reconnect helper | BUG-06, CLEAN | **yolo-fit** | Prefer context managers later |
| `typing.Protocol` + `default_factory` for Worker.reporter | ARCH-02, ARCH-03 | **yolo-fit** | Mechanical |
| Introduce validated settings object for OELEO_*/OA_* | ARCH-05 | **standard** | Unlocks clearer app errors |

## P2 — Errors & observability

| Title | IDs | Size | Notes |
|-------|-----|------|-------|
| Raise on SSH list/checksum failure instead of empty/False | REL-02 | **standard** | Pair with reporter.notify |
| Replace `sys.exit` in `die_if_necessary` with exception | REL-04 | **standard** | Catch in scheduler/app |
| `dump_db` CSV/JSON export | utils TODOs | **standard** | Helps “easy to debug runs” README goal |

## P3 — Tests & quality gates

| Title | IDs | Size | Notes |
|-------|-----|------|-------|
| Unit tests for filters + DbHandler codes | TEST-01 | **yolo-fit** / standard | Foundations for BUG-01/02 |
| Add ruff (and optionally mypy) to CI | QUAL-01 | **standard** | Start check-only |
| Expand SSH tests: checksum + worker.run smoke | TEST-01 | **standard** | Needs container job |
| Decide SharePoint strategy: test, document limits, or demote | SharePoint gaps | **epic** | Product call |

## P3 — Docs & packaging hygiene

| GitHub | Title | IDs | Size | Notes |
|--------|-------|-----|------|-------|
| [#19](https://github.com/ife-bat/oeleo/issues/19) | Align README with uv + actual Python floor | DOC-01 | **yolo-fit** | label `yolo` |
| — | Portable PyInstaller spec / build script | CLEAN-03 | **standard** | Relative paths · *not filed yet* |
| — | Retire or rewrite Poetry-based `nox pack` | TOOL-01 | **standard** | *not filed yet* |
| — | Delete `base_filter_old` and unused imports | CLEAN-01 | **yolo-fit** | *not filed yet* |

## P4 — Product wishlist (defer unless requested)

| Title | Size | Notes |
|-------|------|-------|
| CLI entry point wrapping factories | **epic** | README wishlist |
| Web app / GUI | **epic** | Explicit non-goal for near-term agents |
| Enable threaded `Worker.run` | **epic** | Needs DB/logging thread-safety first |

---

## Suggested first wave (concrete sequence)

Filed on GitHub (2026-07-16). Two parallel tracks (separate branches/PRs):

**Track A — dependencies**

1. [#11](https://github.com/ife-bat/oeleo/issues/11) DEP-01 — plan + confirm  
2. [#12](https://github.com/ife-bat/oeleo/issues/12) DEP-02 / [#13](https://github.com/ife-bat/oeleo/issues/13) DEP-03 — yolo  

**Track B — correctness**

1. [#14](https://github.com/ife-bat/oeleo/issues/14) BUG-03 — yolo  
2. [#15](https://github.com/ife-bat/oeleo/issues/15) BUG-01 — yolo  
3. [#16](https://github.com/ife-bat/oeleo/issues/16) BUG-04 — yolo  
4. [#17](https://github.com/ife-bat/oeleo/issues/17) REL-01 — plan + confirm  
5. [#18](https://github.com/ife-bat/oeleo/issues/18) SEC-01 — plan  
6. [#19](https://github.com/ife-bat/oeleo/issues/19) DOC-01 — yolo  

Later: open an **epic** for BUG-02 (relative-path bookkeeping) — not filed yet.

Prefer landing **#11 (DEP-01)** early so CI and local envs are not stuck on known-vulnerable wheels while other work continues. Pick with `iflow pick`.

## When updating this backlog

After fixing a finding: mark it done here (strike through or move to a “Completed” section) and adjust the severity table in `code-review-overview.md`. Keep docs durable — don’t delete history of *why* a rule exists.
