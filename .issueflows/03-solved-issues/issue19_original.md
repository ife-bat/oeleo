# Issue #19: Align README with uv and the actual Python version floor

Source: https://github.com/ife-bat/oeleo/issues/19

## Original issue text

## Summary
README still mixes `pip` / `python -m build` guidance and says Python 3.8 is no longer required for â‰¥0.6, while `pyproject.toml` still has `requires-python = \">=3.8,<3.13\"`. Day-to-day toolchain is **uv**.

**Finding ID:** DOC-01  
**Size:** yolo-fit  
**Design doc:** `.issueflows/04-designs-and-guides/code-review-packaging-and-ops.md` and `this-project.md`

## Acceptance
- [ ] README install/dev/test commands match `uv` workflow
- [ ] Python version story matches `pyproject.toml` (raise floor or fix the README claim)
