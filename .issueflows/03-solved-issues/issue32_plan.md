# Plan: Issue #32 — Make OELEO_PASSWORD optional for key-based SSH

## Goal

Allow `SSHConnector` (and `ssh_worker`) to construct and connect with key-based auth when `use_password=False` without `OELEO_PASSWORD` in the environment, while password auth still requires a password and secrets stay out of logs.

## Constraints

- Follow SEC-03 / [code-review-security.md](.issueflows/04-designs-and-guides/code-review-security.md): never log password or key material; prefer key-based examples.
- Scope is **SSH only**. Do not change SharePoint’s `OELEO_PASSWORD` requirement (`SharePointConnector` still needs it).
- Do not fix `register_password` (BUG-05 / #33) in this issue — separate yolo-fit item.
- Keep default `use_password=False` on `SSHConnector` / `ssh_worker` (already key-first).
- Back-compat: password path and existing SSH integration tests (`use_password=True` + env) must keep working.

### Prior art

- `SSHConnector.__init__` / `connect` in [`oeleo/connectors.py`](oeleo/connectors.py) — `__init__` always does `os.environ["OELEO_PASSWORD"]`; `connect` already branches on `use_password` (password vs `OELEO_KEY_FILENAME`). `self.session_password` is set on SSH but never read (SharePoint uses its own).
- Unit fixture pattern in [`tests/test_ssh_shell_safety.py`](tests/test_ssh_shell_safety.py) — monkeypatches `OELEO_PASSWORD` even though those tests use password auth; reusable for key-auth construction tests.
- Docs that state the current footgun: [`tests/README.md`](tests/README.md) (“requires `OELEO_PASSWORD` even if you plan to use keys”); README env reference already says password is “used when connecting with password”.
- Toolbox: none. Graphify: not present. Convention: fail via missing env `KeyError` today; keep failure obvious without dumping secret values.

## Approach

1. **`SSHConnector.__init__`:** set `self.use_password` before reading secrets. If `use_password` is true, read `OELEO_PASSWORD` into `self.session_password` (same as today — missing env → `KeyError`). If false, set `self.session_password = None` and do **not** touch `OELEO_PASSWORD`.
2. **`SSHConnector.connect`:** keep the existing branch. For password auth, keep reading `os.environ["OELEO_PASSWORD"]` (or reuse `self.session_password`); for key auth, keep requiring `OELEO_KEY_FILENAME` only. Do not log `connect_kwargs`.
3. **Docs:** remove/replace the outdated note in `tests/README.md`. Optionally clarify in `.env_example` that `OELEO_PASSWORD` is only needed for password SSH / SharePoint — one-line comment if cheap; no README rewrite beyond what’s already accurate.
4. **Out of scope:** `register_password`, SharePoint, making `OELEO_KEY_FILENAME` optional, Fabric identity defaults.

## Files to touch

| Path | Change |
|------|--------|
| [`oeleo/connectors.py`](oeleo/connectors.py) | Conditional password load in `SSHConnector.__init__` |
| [`tests/test_ssh_optional_password.py`](tests/test_ssh_optional_password.py) (new) or extend [`tests/test_ssh_shell_safety.py`](tests/test_ssh_shell_safety.py) | Unit tests: construct + mock-`connect` with `use_password=False` and `OELEO_PASSWORD` unset; password path still fails clearly when unset |
| [`tests/README.md`](tests/README.md) | Drop “requires OELEO_PASSWORD even for keys” |
| [`.env_example`](.env_example) | Optional one-line comment that password is for password-SSH / SharePoint |

## Test strategy

- `uv run pytest -m "not ssh"` (project default).
- New unit tests (no live SSH):
  - `use_password=False`, `OELEO_PASSWORD` unset, `OELEO_KEY_FILENAME` set → `__init__` succeeds; mocked `Connection` receives `key_filename` only (no password key).
  - `use_password=True`, `OELEO_PASSWORD` unset → `__init__` (or first password read) raises clearly (`KeyError` or a short `ValueError` / `OeleoConnectionError` without embedding secrets).
- Do not require `pytest -m ssh` for this change (integration suite already uses password auth).

## Open questions

None blocking — defaults below unless you override:

1. **Missing password when `use_password=True`:** keep eager fail in `__init__` via env lookup (current behavior), not only at `connect`.
2. **Clearer exception type:** prefer a short `ValueError("OELEO_PASSWORD is required when use_password=True")` wrapping/replacing bare `KeyError` for the password path only.
3. **Where to put tests:** new small `tests/test_ssh_optional_password.py` rather than bloating shell-safety tests.
