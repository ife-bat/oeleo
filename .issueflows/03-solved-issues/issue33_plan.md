# Plan: Issue #33 — Fix register_password to set provided password

## Goal

Make `register_password(pwd)` actually set `OELEO_PASSWORD` when `pwd` is provided; keep getpass prompt when `pwd is None`.

## Approach

- In `oeleo/connectors.py`: if `pwd is None`, prompt via getpass (unchanged); else assign `os.environ["OELEO_PASSWORD"] = pwd`.
- Keep the function name (prefer setter behavior per issue).
- Unit tests with mocked getpass; never log the password value.
- Mark BUG-05 done in the correctness design doc.

## Files to touch

- `oeleo/connectors.py`
- `tests/test_register_password.py` (new)
- `.issueflows/04-designs-and-guides/code-review-correctness-and-bugs.md`

## Test strategy

`uv run pytest -m "not ssh"` — assert provided pwd sets env; `None` prompts and sets env from getpass.
