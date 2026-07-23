# Plan: Issue #39 — Raise on SSH list/checksum failure (REL-02)

## Goal

Stop soft connector failures from looking like success: SSH list failures must not look like an empty directory, and checksum failures must not return sentinel `False` / parse bad stdout. Fail loudly with typed exceptions and surface via the reporter.

## Constraints

- Finding **REL-02** — see [`.issueflows/04-designs-and-guides/code-review-correctness-and-bugs.md`](.issueflows/04-designs-and-guides/code-review-correctness-and-bugs.md). Distinct from **#8** (`ensure_connection` destination-loss abort), which is already done.
- Do **not** change `die_if_necessary` / `sys.exit` (**#40** / REL-04) or SharePoint product strategy (**#45**).
- Keep `#17` reconnect defaults and `#8` probe/abort paths unchanged.
- Public composition API (`Worker` + connectors) stays; prefer raising from connectors over silent sentinels.
- Unit tests: `uv run pytest -m "not ssh"` with mocks (same style as `tests/test_ssh_shell_safety.py` / `#8` tests). No new Docker SSH requirement for acceptance.
- Scope this PR to **list + checksum error semantics** (SSH + SharePoint checksum sentinel). Do **not** rewrite `move_func` / `simple_mover` `False` returns here (related REL-02 note, separate follow-up if needed).

### Prior art

- `OeleoConnectionError` — [`oeleo/connectors.py`](oeleo/connectors.py): used by `ensure_connection` / `reconnect`; propagated by `Worker.run` and caught by `SimpleScheduler`.
- `SSHConnector.ensure_connection` — Fabric `run(..., warn=True)` + `result.ok` → raise; **mirror** this failure style for `_list_content` / `calculate_checksum`.
- `SSHConnector._list_content` — catches `Exception`, `print`s, returns `[]`; `result.ok` false → still returns `[]`.
- `SSHConnector.calculate_checksum` — logs “should raise” but still parses `stdout` (can IndexError / return garbage).
- `SharePointConnector.calculate_checksum` — `ShareplumRequestError` → returns `False` (typed as `Hash` / `str`).
- `Worker.check` — `filter_external` → empty list looks like “no remote files” → everything marked out of sync; external checksum via `checker.check(..., connector=external)`.
- `Worker._process_file` — already `try/except Exception` around `checker.check` (returns failed file); does **not** `notify` today.
- `Worker._ensure_external_connection` — `reporter.report` + `reporter.notify` + re-raise pattern to **mirror** for check/list abort.
- Tests: [`tests/test_ssh_shell_safety.py`](tests/test_ssh_shell_safety.py) mock Fabric `run` for `_list_content` / `calculate_checksum` quoting — extend with negative paths.
- Toolbox: none. Graph: `SSHConnector` god-node; Communities 3/4 (connectors / `OeleoConnectionError`).

## Approach

1. **Typed exceptions** — Keep `OeleoConnectionError` for unreachable / transport / remote command infrastructure failures. Add `OeleoTransferError` for “connected but this file/list operation failed” (failed `md5sum`, SharePoint get_file error, non-ok `find` when the host answered). Both subclasses of a thin `OeleoError` **or** sibling exceptions under the same module — keep imports from `oeleo.connectors` as today.
2. **`SSHConnector._list_content`** — On Fabric/transport exception or `not result.ok`: raise `OeleoConnectionError` (or `OeleoTransferError` if the session is up but `find` failed — see open Q1). Never return `[]` for failure. On success with empty stdout, return a true empty list (filter blank lines from `split`), so “no files” ≠ “error”.
3. **`SSHConnector.calculate_checksum`** — If `not result.ok`, empty/unparseable stdout, or Fabric raises: raise `OeleoTransferError` (message includes path). Do not parse failed stdout.
4. **`SharePointConnector.calculate_checksum`** — On `ShareplumRequestError` (and unexpected errors): raise `OeleoTransferError` instead of `False`. Happy path unchanged (`md5` hex digest).
5. **Worker surfacing**
   - `filter_external` / `check`: let list failures propagate; wrap at `check` (and optionally `filter_external`) with `reporter.report` + `reporter.notify` then re-raise so a failed listing cannot look like zero remote files.
   - Per-file checksum failure in `check`: catch `OeleoTransferError`, notify, treat that file as not-in-sync / skip DB update for that iteration (do not abort the whole check unless we decide otherwise — see Q2).
   - `_process_file`: on checksum/`checker` `OeleoTransferError`, `reporter.notify` then return failed file (keep run going for other files), matching current soft per-file failure style for moves.
6. **Tests** — Mocked negative paths: list `ok=False` / exception → raises, not `[]`; checksum `ok=False` / empty stdout → raises; SharePoint get_file error → raises (not `False`); optional thin Worker test that a raised list error triggers notify + abort of `check`.
7. **Docs** — Update REL-02 note in the correctness design doc (mark addressed / point to #39). No README epic unless operator-visible behavior needs one line.

## Files to touch

| Path | Change |
|------|--------|
| [`oeleo/connectors.py`](oeleo/connectors.py) | Add `OeleoTransferError`; harden `_list_content` + SSH/SharePoint `calculate_checksum` |
| [`oeleo/workers.py`](oeleo/workers.py) | Notify + propagate/catch typed errors in `check` / `_process_file` as above |
| [`tests/test_ssh_shell_safety.py`](tests/test_ssh_shell_safety.py) (and/or new `tests/test_connector_errors.py`) | Negative-path unit tests with mocks |
| [`tests/test_oeleo.py`](tests/test_oeleo.py) | Optional Worker notify/abort coverage for list failure |
| [`.issueflows/04-designs-and-guides/code-review-correctness-and-bugs.md`](.issueflows/04-designs-and-guides/code-review-correctness-and-bugs.md) | Note REL-02 addressed by #39 |

## Test strategy

- Command: `uv run pytest -m "not ssh"`.
- Primary: extend shell-safety-style mocks for failure cases (no live SSH).
- Assert exceptions and that successful empty listing still returns `[]` without raising.

## Open questions

1. **Exception split:** Introduce `OeleoTransferError` for checksum / failed list-op (**recommended**), or reuse only `OeleoConnectionError` for everything in this PR (simpler, weaker typing)?
2. **Checksum failure in `Worker.check`:** notify + skip/mark out-of-sync for that file and continue (**recommended**), or abort the entire `check` on first checksum error?
3. **SSH `_list_content` failure type:** `OeleoConnectionError` (**recommended** — empty listing already misleads sync the same way as a dead host) vs `OeleoTransferError`?

## Scope check

One concern (connector error semantics), few modules, no unrelated refactors. Fits one PR. Move-path `False` returns and REL-04 stay out of scope.
