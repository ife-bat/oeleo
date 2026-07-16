# Issue #19 plan

## Goal

Align README install/dev/test/build guidance with the project's **uv** workflow and the current `requires-python` floor (`>=3.11,<3.13`).

## Constraints

- Docs-only; do not change `pyproject.toml` unless the README claim still disagrees (floor already raised in #11).
- Keep a clear PyPI end-user install path (`pip install oeleo` is fine for consumers).
- Match day-to-day commands in `.issueflows/04-designs-and-guides/this-project.md`.
- Update DOC-01 note in `code-review-packaging-and-ops.md` so agents do not re-open closed drift.

### Prior art

- `this-project.md` — canonical `uv sync` / `uv run pytest -m "not ssh"` commands.
- `code-review-packaging-and-ops.md` DOC-01 — source finding for this issue.
- Issue #11 — already raised `requires-python` to `>=3.11,<3.13`; README Dev bullets already reflect that.

## Approach

1. Expand **Development** with `uv sync` / `uv sync --all-extras`, version bump via `uv version --bump`, and tests matching CI (`not ssh` default).
2. Replace `python -m build` / `python -m twine …` with `uv build` / `uv publish`.
3. Leave consumer `pip install oeleo` under Install; optionally note from-source/dev uses uv.
4. Confirm Python version wording matches `pyproject.toml` (no floor change needed).
5. Mark DOC-01 addressed in the packaging design doc.

## Files to touch

| File | Change |
|------|--------|
| `README.md` | uv-first dev/test/build/publish; Python floor consistency |
| `.issueflows/04-designs-and-guides/code-review-packaging-and-ops.md` | DOC-01 resolved note |

## Test strategy

`uv run pytest -m "not ssh"` (docs-only; regression check).

## Open questions

None — yolo auto-confirm.
