# Code review: security & trust boundaries

See [`code-review-overview.md`](code-review-overview.md) for the index.

## Threat model (pragmatic)

`oeleo` typically runs on a trusted instrument PC with credentials for a **restricted** destination account. The README already recommends SSH key pairs and ACL-limited users. Agents should preserve that guidance and not expand the blast radius.

Trust boundaries:

1. Local `.env` / process environment (secrets).
2. Local filesystem source tree (what gets read/copied).
3. Remote shell on SSH host (commands constructed by `SSHConnector`).
4. SharePoint / Office365 auth cookies.

## Findings

### ~~SEC-01 — Remote command construction (high)~~ (done in #18)

~~`SSHConnector` built shell commands with unquoted / lightly quoted interpolation.~~ **Resolved:** POSIX remotes use `_remote_shell_token` / `shlex.quote` for `find`, `md5sum`, and `mkdir -p` (and debug helpers). Windows remotes get best-effort `cmd.exe` quoting only. Unit tests assert quoted commands; gated SSH integration covers spaces in remote paths. Shell-free SFTP checksum/`mkdir` left as optional follow-up.

---

### SEC-02 — MD5 for change detection (low / informational)

Local and remote checksums use MD5 (`utils.calculate_checksum`, remote `md5sum`, SharePoint `hashlib.md5`). Fine for “did the file change?” sync. Do **not** document MD5 as integrity/security proof. Optional later: BLAKE2/SHA-256 with DB migration — epic-sized, low urgency.

---

### SEC-03 — Secrets handling (medium hygiene)

| Topic | Status | Suggestion |
|-------|--------|------------|
| `.env` gitignored | Yes | Keep; never log password/key contents |
| Password in env | Optional for key auth (#32); required when `use_password=True` | Done — `SSHConnector` skips `OELEO_PASSWORD` unless password auth |
| `register_password` | Puts secret in `os.environ` | OK for session; avoid writing back to `.env` from code |
| Logs | Rich/file logging can echo paths/hosts | Ensure connect kwargs never logged at INFO |
| Tray “Open log” | Opens log via OS handler | Log path is local — OK; don’t put secrets in log messages |

---

### SEC-04 — Least privilege & deployment (ops)

- `install_task.ps1` registers a startup task with S4U (no stored password) — good pattern for Windows services that must run headless.
- Document that the scheduled task’s working directory must contain a locked-down `.env` (ACLs on the file).
- Destination SSH user should only write the data tree (already in README — keep prominent in agent docs).

---

### SEC-05 — SharePoint auth (medium / dependency)

`SharePointConnection` uses SharePlum `Office365(...).GetCookies()`. Dependency age/maintenance and modern auth (MFA, app-only) are product risks. No code change required for agents unless an issue targets SharePoint; flag in plans that SharePoint may need a different client long-term.

---

### SEC-06 — Path traversal / copy destinations (low–medium)

Local movers use `shutil.copyfile` to a computed destination. With `external_subdirs=True`, relative paths from source are appended under destination. Symlinks under the source tree could surprise operators. Consider `Path.resolve()` confinement checks: destination must stay under `external_connector.directory`.

## What looks fine

- No `eval` / `pickle` / dynamic code execution found in package code.
- Subprocess usage in tray reporter uses argv lists (`open`, `xdg-open`), not `shell=True`.
- `.env` is gitignored; example env has placeholders.

## Agent rules when touching this area

1. Never add logging of `OELEO_PASSWORD` or key material.
2. Any new SSH remote invocation must quote or avoid the shell.
3. Prefer key-based examples in docs over password examples.
4. Security-sensitive fixes should include tests with awkward filenames (spaces, quotes) where feasible.
