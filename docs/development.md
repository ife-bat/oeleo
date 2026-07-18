# Development

Day-to-day toolchain is **uv** (`uv.lock` is committed). Requires Python `>=3.11,<3.13` (see `pyproject.toml`); develop on **3.11+** (CI uses 3.12).

```bash
# Sync the project environment (add --all-extras when you need pystray)
uv sync
uv sync --all-extras

# Unit tests (default / CI path)
uv run pytest -m "not ssh"

# SSH integration tests (needs a local SSH server — see tests/README.md)
uv run pytest -m ssh

# Format (black + isort; not enforced in CI)
uv run black oeleo tests app
uv run isort oeleo tests app

# Bump version in pyproject.toml (e.g. 0.7.0 → 0.7.1)
uv version --bump patch

# Build and publish
uv build
uv publish   # uses PyPI token from the environment / keyring
```

## Documentation (Zensical)

Docs live under `docs/` and are built with [Zensical](https://zensical.org/). Publishing is intended for Read the Docs (see `.readthedocs.yaml` at the repo root).

```bash
# Install the docs tool
uv sync --group docs

# Preview locally
uv run zensical serve

# Build static site into site/ (gitignored)
uv run zensical build
```

Read the Docs installs from `docs/requirements.txt` and runs `zensical build`. Connecting the GitHub repo in the RTD UI is a separate ops step.

### Development lead

Jan Petter Maehlen, IFE
