# Code review: testing & quality gates

See [`code-review-overview.md`](code-review-overview.md) for the index.

## Current state

| Area | Status |
|------|--------|
| Unit tests | `tests/test_oeleo.py` — movers, local connector, checksum, simple worker, scheduler (+ subdirs) |
| SSH integration | `tests/test_ssh_integration.py` — list with/without subdirs, mkdir-on-put; gated by `OELEO_SSH_TESTS` / marker `ssh` |
| Fixtures | `tests/conftest.py` — tmp dirs, in-memory DB worker |
| CI | `.github/workflows/tests.yml` — unit (`not ssh`) + SSH service container job |
| Coverage tool | Not configured |
| Lint/type CI | Not configured (black/isort in dependency-groups only) |

## What is well tested

- Local filter by extension.
- Local checksum golden value.
- Local copy via mover and connector.
- End-to-end local worker: 2 matching + 1 non-matching extension.
- Scheduler two-interval local run.
- Subdir-preserving local copy via scheduler.
- SSH listing depth and remote parent creation (integration).

## Gaps (TEST-01)

Empty section stubs in `test_oeleo.py` mark intent without coverage:

| Component | Gap |
|-----------|-----|
| Filters | No direct tests for `not_before` / `startswith` / multi-extension lists |
| Models | No tests for codes `0/1/2`, `is_changed`, unique constraints |
| Checkers | Indirect only |
| Reporters | Manual `__main__` demos only |
| SharePoint | Entire connector untested (stubs + no integration) |
| SSH worker | Factory/`Worker.run` over SSH not covered (connector-only tests) |
| App | `oa.pyw` untested (desktop/tray hard); at least extract pure config parsing for unit tests |
| Negative paths | PermissionError, failed put, empty remote list errors |

Many SSH/SharePoint tests are `pass` placeholders — CI green does not mean those APIs are safe.

## Quality tooling gaps (QUAL-01)

Suggestions (incremental issues):

1. **ruff** (replace or complement black/isort) — CI `uv run ruff check`.
2. **mypy** or **ty** on `oeleo/` — start with connectors/models; ignore app tray if needed.
3. **pytest-cov** with a modest floor (e.g. 60%) once models/filters tests exist — don’t set 90% until SharePoint strategy is decided.
4. Pin CI to the same Python the team develops on **or** matrix 3.11–3.12 (README says 3.11; CI is 3.12 only).
5. `pytest` `log_cli=true` + DEBUG is noisy for CI — consider default quiet, verbose on failure.

## Flake / design risks in tests

- Module-level `start_logger()` in tests and conftest can add handlers multiple times if imported oddly.
- SSH tests assume Fabric accepts `host:port` — documented caveat in `tests/README.md`.
- Subdir test asserts counts only, not path layout equality — strengthen when fixing BUG-02.

## Recommended test plan for agents

When closing issues that touch core logic, prefer:

```bash
uv run pytest -m "not ssh"
# if connectors/ssh or movers remote:
# ensure docker compose/ssh container, then:
uv run pytest -m ssh
```

Add focused unit tests **before** broad refactors. Prefer temp dirs + `:memory:` DB over developer absolute paths (`main.py` examples are not tests).
