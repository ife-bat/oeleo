# Code review: improvement backlog (issue-flow ready)

Use this list when creating or picking GitHub issues. Cite finding IDs in `issue<N>_plan.md`.  
Entry point: [`code-review-overview.md`](code-review-overview.md).

**Legend**

- **yolo-fit** — small, low-risk; suitable for `iflow yolo` / label `yolo` after green tests.
- **standard** — needs explicit `iflow plan` confirmation; one PR.
- **epic** — use `iflow epic`; split into staged issues.

---

## P0 — Correctness (do first)

| Title (suggested GitHub issue) | IDs | Size | Notes |
|--------------------------------|-----|------|-------|
| Honor bookkeeping `code=2` (locked) during `Worker.run` | BUG-01 | **yolo-fit** | Unit test required |
| Fix `OA_SINGLE_RUN` crash: replace `worker.db_path` | BUG-03 | **yolo-fit** | Log `bookkeeper.db_name` |
| Peewee `processed_date` default must be callable | BUG-04 | **yolo-fit** | One-liner + test |
| Stop reconnecting SSH before every file by default | REL-01 | **yolo-fit** / standard | Confirm ops preference; reconnect-on-failure only |

## P1 — Data model & identity

| Title | IDs | Size | Notes |
|-------|-----|------|-------|
| Bookkeep by relative path, not basename | BUG-02 | **epic** | Migration + subdir tests; stages: schema, write path, migrate tool, docs |
| Materialize `filter_local` results to a list | REL-03 | **yolo-fit** | Prevents empty second `run` |

## P1 — Security / SSH hardening

| Title | IDs | Size | Notes |
|-------|-----|------|-------|
| Shell-safe remote path handling in `SSHConnector` | SEC-01 | **standard** | `shlex.quote` or avoid shell; tests with spaces |
| Make `OELEO_PASSWORD` optional for key-based SSH | SEC-03 | **yolo-fit** | Don’t require env when `use_password=False` |

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

| Title | IDs | Size | Notes |
|-------|-----|------|-------|
| Align README with uv + actual Python floor | DOC-01 | **yolo-fit** | |
| Portable PyInstaller spec / build script | CLEAN-03 | **standard** | Relative paths |
| Retire or rewrite Poetry-based `nox pack` | TOOL-01 | **standard** | |
| Delete `base_filter_old` and unused imports | CLEAN-01 | **yolo-fit** | |

## P4 — Product wishlist (defer unless requested)

| Title | Size | Notes |
|-------|------|-------|
| CLI entry point wrapping factories | **epic** | README wishlist |
| Web app / GUI | **epic** | Explicit non-goal for near-term agents |
| Enable threaded `Worker.run` | **epic** | Needs DB/logging thread-safety first |

---

## Suggested first wave (concrete sequence)

Good sequence for issue-flow without an epic:

1. BUG-03 (`db_path`) — yolo  
2. BUG-01 (locked files) — yolo  
3. BUG-04 (datetime default) — yolo  
4. REL-01 (reconnect default) — plan + confirm  
5. SEC-01 (quote SSH paths) — plan  
6. DOC-01 (README/uv) — yolo  

Then open an **epic** for BUG-02 (relative-path bookkeeping).

## When updating this backlog

After fixing a finding: mark it done here (strike through or move to a “Completed” section) and adjust the severity table in `code-review-overview.md`. Keep docs durable — don’t delete history of *why* a rule exists.
