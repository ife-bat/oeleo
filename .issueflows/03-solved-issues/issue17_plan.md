# Plan: Issue #17 — Stop reconnecting SSH before every file by default

## Goal

Stop thrashing SSH sessions by making per-file reconnect opt-in (`Worker.reconnect=False` by default), while keeping reconnect-and-retry after a failed move. Document the behavior change for operators.

## Constraints

- Finding **REL-01** only — do not fix BUG-06 (broken `SharePointConnection.reconnect`), SEC-01 (path quoting), or SSH `move_func` inner retry loop in this PR.
- Keep public composition API: factories + `Worker` methods; constructors remain the opt-in surface unless we add a small env toggle (see Open questions).
- Behavior change is intentional and must be noted (README / env docs). No project `CHANGELOG` file today.
- Tests via `uv run pytest -m "not ssh"` (unit path); no new SSH Docker requirement for the happy-path mock test.
- Cite REL-01 in status when closing; update `code-review-correctness-and-bugs.md` / backlog when the finding is done (close step or this PR if touching docs anyway).

### Prior art

- `Worker._process_file` — [`oeleo/workers.py`](oeleo/workers.py): per-file `if self.reconnect: external_connector.reconnect()` then `move_func`; on failure, unconditional `reconnect()` + second `move_func` (keep).
- `Worker.reconnect: bool = True` — dataclass default; docstring already describes “if connection is lost” (out of sync with always-on behavior).
- `simple_worker` / `ssh_worker` — hardcode `reconnect=True`; `sharepoint_worker` relies on dataclass default.
- `Connector.reconnect` protocol + `SSHConnector.reconnect` — close/connect; `LocalConnector.reconnect` is a no-op.
- `SSHConnector.move_func` — own `CONNECTION_RETRIES` loop with `reconnect()` on failure (leave alone; complements Worker-level retry).
- Design: [`.issueflows/04-designs-and-guides/code-review-correctness-and-bugs.md`](.issueflows/04-designs-and-guides/code-review-correctness-and-bugs.md) (REL-01 + recommended test #5).
- Toolbox: none. Graph: none. Grep: no existing reconnect tests.

## Approach

1. **Flip default** — `Worker.reconnect = False`. Clarify docstring: when `True`, reconnect before each changed file; failed moves always reconnect once and retry regardless.
2. **Factories** — Remove hard-coded `reconnect=True` from `simple_worker` and `ssh_worker` (inherit `False`), or pass through an optional `reconnect=` / env (per Open questions).
3. **Leave failure path** — Keep the post-failure `external_connector.reconnect()` + second `move_func` unconditional on the flag.
4. **Opt-in for flaky networks** — At minimum, `Worker(..., reconnect=True)` and factory kwarg. Optionally honor `OELEO_RECONNECT` (`1`/`true`/`yes`) in factories so scheduled `app/oa.pyw` / `.env` can opt in without code changes.
5. **Docs** — README env section (and `.env_example` if env is added): default is no per-file reconnect; how to opt in; note that a failed copy still reconnects once.
6. **Design memory** — Mark REL-01 done in correctness + backlog docs (small durable update).

## Files to touch

| Path | Change |
|------|--------|
| [`oeleo/workers.py`](oeleo/workers.py) | Default `reconnect=False`; docstring; factories stop forcing `True` (+ optional env/kwarg) |
| [`README.md`](README.md) | Operator note + env if added |
| [`.env_example`](.env_example) | Optional `OELEO_RECONNECT` line if env is added |
| [`tests/test_oeleo.py`](tests/test_oeleo.py) (or small new test module) | Mock `external_connector`: multi-file success with `reconnect=False` → `reconnect()` only on failures (0 on all-success); `reconnect=True` → called before each changed file; failed `move_func` still triggers reconnect when flag is `False` |
| [`.issueflows/04-designs-and-guides/code-review-correctness-and-bugs.md`](.issueflows/04-designs-and-guides/code-review-correctness-and-bugs.md) | Mark REL-01 addressed |
| [`.issueflows/04-designs-and-guides/code-review-improvement-backlog.md`](.issueflows/04-designs-and-guides/code-review-improvement-backlog.md) | Strike/complete #17 |
| [`.issueflows/04-designs-and-guides/code-review-overview.md`](.issueflows/04-designs-and-guides/code-review-overview.md) | Adjust severity table for REL-01 if still listed as open |

## Test strategy

- Command: `uv run pytest -m "not ssh"` (and the new test(s) specifically).
- Prefer a focused unit test with a fake/mock connector counting `reconnect` / `move_func` — matches recommended test #5 in the correctness doc; no Fabric needed.
- Existing `simple_worker` integration-style tests should keep passing (local reconnect is already a no-op).

## Open questions

1. **Confirm default flip to `False`?** (Recommended: **yes** — matches issue acceptance and REL-01. Alternative: keep default `True` and only document opt-out — weaker fix.)
2. **Opt-in surface:** Python kwarg only on `Worker` / factories, or also **`OELEO_RECONNECT`** for `.env` / Windows scheduled runs? (Recommended: **both** — tiny, matches how ops configure oeleo today.)
3. **Version bump on close?** Behavior change for SSH operators — recommend **minor** note in PR; bump only if `/iflow-close` release policy says so for this class of change (likely patch/docs-level unless you want a minor for “operator-visible default”).

## Scope check

Single concern, few files, no unrelated refactors. Fits one PR. Does **not** need splitting.
