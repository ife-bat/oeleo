# Install

## End users (PyPI)

```bash
pip install oeleo
```

## Development (clone)

Day-to-day toolchain is **uv** (`uv.lock` is committed). Requires Python `>=3.11,<3.13` (see `pyproject.toml`); develop on **3.11+** (CI uses 3.12).

```bash
uv sync
uv sync --all-extras   # when you need pystray (Windows tray app)
```

See [Development](development.md) for tests, formatting, docs builds, and publishing.
