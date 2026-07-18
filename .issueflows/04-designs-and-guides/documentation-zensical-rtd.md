# Documentation toolchain (Zensical + Read the Docs)

**Issue:** [#56](https://github.com/ife-bat/oeleo/issues/56)

## Decision

- User-facing docs live under `docs/` as Markdown.
- Static site generator: **Zensical** (`zensical.toml` at repo root).
- Publish via **Read the Docs** (`.readthedocs.yaml` + `docs/requirements.txt`).
- Local: `uv sync --group docs` then `uv run zensical serve` / `zensical build`.
- Do **not** add a GitHub Pages docs workflow; RTD is the publish path.

## Alternatives considered

- MkDocs / Sphinx — rejected; issue specifies Zensical.
- `zensical new` scaffold — rejected for an existing repo (would add GH Pages workflow); hand-crafted instead.

## Ops note

Connecting the GitHub repo in the Read the Docs UI (and setting `site_url` in `zensical.toml` once the slug is known) is a human step, not part of the package runtime.
