# Issue #13: Add grouped Dependabot config for uv/pip

Source: https://github.com/ife-bat/oeleo/issues/13

## Original issue text

## Summary
Add `.github/dependabot.yml` (or equivalent) so dependency bumps arrive as grouped PRs and security alerts do not pile up again.

**Finding ID:** DEP-03  
**Size:** yolo-fit  
**Design doc:** `.issueflows/04-designs-and-guides/code-review-dependabot.md`

## Acceptance
- [ ] Dependabot (or equivalent) configured for the pip/uv ecosystem
- [ ] Prefer grouped updates over one PR per transitive package
