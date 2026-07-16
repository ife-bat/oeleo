# Status: Issue #11

- [x] Done

## What's done

- Rebased onto `origin/main` (includes PR #20 for #14/#15/#16).
- Raised `requires-python` to `>=3.11,<3.13` (required by `python-dotenv>=1.2.2`).
- Floors in `pyproject.toml`: `python-dotenv>=1.2.2`, `black>=26.3.1`, `pytest>=9.0.3`.
- `uv lock --upgrade` + `uv sync --all-extras`.
- Verified locked floors (local env): cryptography 49.0.0, urllib3 2.7.0, pillow 12.3.0,
  lxml 6.1.1, python-dotenv 1.2.2, black 26.5.1, pytest 9.1.1, idna 3.18, requests 2.34.2.
- `uv run pytest -m "not ssh"` — 20 passed, 3 deselected.
- Pillow / `LogAndTrayReporter` import smoke OK.
- Minimal README + `this-project.md` Python-floor notes.

## Remaining work

- None for #11. Follow-ups: #12 (residuals), #13 (Dependabot config).
- Confirm Dependabot open-alert drop after this PR merges (may lag).

## Notes

- Full lock upgrade also moved major versions that still pass unit tests locally:
  peewee 3→4, paramiko→5, rich→15. Watch CI SSH job.
- No repo-wide Black reformat (per plan).
