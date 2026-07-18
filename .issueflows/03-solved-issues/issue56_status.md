# Issue #56 — Status

- [x] Done

## What's done

- Plan accepted with recommended options (full README migration, omit `site_url`, pin zensical, keep one short README example).
- Added `[dependency-groups] docs` with `zensical>=0.0.51` (`uv.lock` updated).
- Created `zensical.toml`, `docs/{index,install,usage,configuration,database,development}.md`.
- Added `.readthedocs.yaml` + pinned `docs/requirements.txt` (`zensical==0.0.51`).
- Slimmed `README.md` (install + one local example + links into `docs/`).
- Design note: `.issueflows/04-designs-and-guides/documentation-zensical-rtd.md` (+ pointer in `this-project.md`).
- Verified: `uv run zensical build` (no issues); `uv run pytest -m "not ssh"` passed (47).

## Remaining work

- Human/ops (outside this PR): connect the GitHub repo in the Read the Docs UI; set `site_url` in `zensical.toml` once the slug is known.
