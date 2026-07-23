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
| ~~[#11](https://github.com/ife-bat/oeleo/issues/11)~~ | ~~Clear Dependabot alerts: widen black/pytest pins + refresh uv.lock~~ | ~~DEP-01~~ | **done** | Lock refresh; residual paramiko SHA-1 in DEP-02 |
| ~~[#12](https://github.com/ife-bat/oeleo/issues/12)~~ | ~~Document residual Dependabot cases; remove stale poetry.lock if present~~ | ~~DEP-02~~ | **done** | |
| ~~[#13](https://github.com/ife-bat/oeleo/issues/13)~~ | ~~Add grouped Dependabot config for uv/pip~~ | ~~DEP-03~~ | **done** | |

## P0 — Correctness (do first / can interleave with DEP-01)

| GitHub | Title | IDs | Size | Notes |
|--------|-------|-----|------|-------|
| ~~[#15](https://github.com/ife-bat/oeleo/issues/15)~~ | ~~Honor bookkeeping `code=2` (locked) during `Worker.run`~~ | ~~BUG-01~~ | **done** | |
| ~~[#14](https://github.com/ife-bat/oeleo/issues/14)~~ | ~~Fix `OA_SINGLE_RUN` crash: replace `worker.db_path`~~ | ~~BUG-03~~ | **done** | |
| ~~[#16](https://github.com/ife-bat/oeleo/issues/16)~~ | ~~Peewee `processed_date` default must be callable~~ | ~~BUG-04~~ | **done** | |
| ~~[#17](https://github.com/ife-bat/oeleo/issues/17)~~ | ~~Stop reconnecting SSH before every file by default~~ | ~~REL-01~~ | **done** | Default `False`; opt-in kwarg / `OELEO_RECONNECT`; fail-path retry kept |
| ~~[#8](https://github.com/ife-bat/oeleo/issues/8)~~ | ~~Ensure connection (abort run on destination loss)~~ | ~~#8 / REL-02 partial~~ | **done** | `ensure_connection`; scheduler retries next interval |

## P1 — Data model & identity

| GitHub | Title | IDs | Size | Notes |
|--------|-------|-----|------|-------|
| [#37](https://github.com/ife-bat/oeleo/issues/37) | Epic: bookkeep by relative path, not basename | BUG-02 | **epic** | Migration + subdir tests; use `iflow epic 37` |
| [#31](https://github.com/ife-bat/oeleo/issues/31) | Materialize `filter_local` results to a list | REL-03 | **yolo-fit** | Prevents empty second `run` · apply label `yolo` |

## P1 — Security / SSH hardening

| GitHub | Title | IDs | Size | Notes |
|--------|-------|-----|------|-------|
| ~~[#18](https://github.com/ife-bat/oeleo/issues/18)~~ | ~~Shell-safe remote path handling in `SSHConnector`~~ | ~~SEC-01~~ | **done** | POSIX `shlex.quote`; unit + gated SSH space-path tests |
| [#32](https://github.com/ife-bat/oeleo/issues/32) | Make `OELEO_PASSWORD` optional for key-based SSH | SEC-03 | **yolo-fit** | Don’t require env when `use_password=False` · apply label `yolo` |

## P2 — API cleanup

| GitHub | Title | IDs | Size | Notes |
|--------|-------|-----|------|-------|
| [#33](https://github.com/ife-bat/oeleo/issues/33) | Fix `register_password` to set provided password | BUG-05 | **yolo-fit** | Or rename to `prompt_password` · apply label `yolo` |
| [#34](https://github.com/ife-bat/oeleo/issues/34) | Remove broken SharePoint reconnect helper and `__delete__` hooks | BUG-06, CLEAN | **yolo-fit** | Prefer context managers later · apply label `yolo` |
| [#35](https://github.com/ife-bat/oeleo/issues/35) | `typing.Protocol` + `default_factory` for Worker.reporter | ARCH-02, ARCH-03 | **yolo-fit** | Mechanical · apply label `yolo` |
| [#38](https://github.com/ife-bat/oeleo/issues/38) | Introduce validated settings object for OELEO_*/OA_* | ARCH-05 | **standard** | Unlocks clearer app errors |

## P2 — Errors & observability

| GitHub | Title | IDs | Size | Notes |
|--------|-------|-----|------|-------|
| ~~[#39](https://github.com/ife-bat/oeleo/issues/39)~~ | ~~Raise on SSH list/checksum failure instead of empty/False~~ | ~~REL-02~~ | **done** | Typed errors + reporter.notify; move_func `False` still open |
| [#40](https://github.com/ife-bat/oeleo/issues/40) | Replace `sys.exit` in `die_if_necessary` with exception | REL-04 | **standard** | Catch in scheduler/app |
| [#41](https://github.com/ife-bat/oeleo/issues/41) | `dump_db` CSV/JSON export | utils TODOs | **standard** | Helps “easy to debug runs” README goal |

## P3 — Tests & quality gates

| GitHub | Title | IDs | Size | Notes |
|--------|-------|-----|------|-------|
| [#42](https://github.com/ife-bat/oeleo/issues/42) | Unit tests for filters + DbHandler codes | TEST-01 | **standard** | Foundations for BUG-01/02 |
| [#43](https://github.com/ife-bat/oeleo/issues/43) | Add ruff (and optionally mypy) to CI | QUAL-01 | **standard** | Start check-only |
| [#44](https://github.com/ife-bat/oeleo/issues/44) | Expand SSH tests: checksum + worker.run smoke | TEST-01 | **standard** | Needs container job |
| [#45](https://github.com/ife-bat/oeleo/issues/45) | Epic: decide SharePoint strategy | SharePoint gaps | **epic** | Product call · `iflow epic 45` |

## P3 — Docs & packaging hygiene

| GitHub | Title | IDs | Size | Notes |
|--------|-------|-----|------|-------|
| ~~[#19](https://github.com/ife-bat/oeleo/issues/19)~~ | ~~Align README with uv + actual Python floor~~ | ~~DOC-01~~ | **done** | |
| [#46](https://github.com/ife-bat/oeleo/issues/46) | Portable PyInstaller spec / build script | CLEAN-03 | **standard** | Relative paths |
| [#48](https://github.com/ife-bat/oeleo/issues/48) | Retire or rewrite Poetry-based `nox pack` | TOOL-01 | **standard** | Prefer #48 over empty #47 |
| [#36](https://github.com/ife-bat/oeleo/issues/36) | Delete `base_filter_old` and unused imports | CLEAN-01 | **yolo-fit** | apply label `yolo` |

## P4 — Product wishlist (defer unless requested)

| Title | Size | Notes |
|-------|------|-------|
| CLI entry point wrapping factories | **epic** | README wishlist · *not filed* |
| Web app / GUI | **epic** | Explicit non-goal for near-term agents · *not filed* |
| Enable threaded `Worker.run` | **epic** | Needs DB/logging thread-safety first · *not filed* |

---

## Suggested next wave

Filed 2026-07-18 (#31–#48). First-wave DEP/BUG/SEC/DOC items (#8, #11–#19) are closed.

**Quick yolo track** (apply `yolo` label if missing — create token could not set labels):

1. [#31](https://github.com/ife-bat/oeleo/issues/31) REL-03 — materialize `filter_local`
2. [#36](https://github.com/ife-bat/oeleo/issues/36) CLEAN-01 — dead filter / imports
3. [#35](https://github.com/ife-bat/oeleo/issues/35) ARCH-02/03 — reporter default + Protocol
4. [#33](https://github.com/ife-bat/oeleo/issues/33) BUG-05 — `register_password`
5. [#34](https://github.com/ife-bat/oeleo/issues/34) BUG-06 — SharePoint helper / `__delete__`
6. [#32](https://github.com/ife-bat/oeleo/issues/32) SEC-03 — optional password for key SSH

**Standard / epic track:**

1. [#38](https://github.com/ife-bat/oeleo/issues/38) ARCH-05 — settings object
2. [#40](https://github.com/ife-bat/oeleo/issues/40) REL-04 — `die_if_necessary` exception
3. [#37](https://github.com/ife-bat/oeleo/issues/37) BUG-02 — relative-path bookkeeping epic
4. [#45](https://github.com/ife-bat/oeleo/issues/45) SharePoint strategy epic

Housekeeping for maintainers: close empty [#47](https://github.com/ife-bat/oeleo/issues/47) (failed create) and probe [#49](https://github.com/ife-bat/oeleo/issues/49); add `yolo` to #31–#36 as listed above.

Pick with `iflow pick`.

## When updating this backlog

After fixing a finding: mark it done here (strike through or move to a “Completed” section) and adjust the severity table in `code-review-overview.md`. Keep docs durable — don’t delete history of *why* a rule exists.
