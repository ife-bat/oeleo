# Plan: Issue #18 — Shell-safe remote path handling in SSHConnector

## Goal

Make every `SSHConnector` remote shell command quote interpolated paths/globs (and keep Windows remote construction safe enough not to regress), so spaces and metacharacters cannot break or inject commands. Prove with unit asserts on built commands plus an SSH integration case with spaces when feasible.

## Constraints

- Finding **SEC-01** only — do not expand into REL-02 (silent empty list), SEC-03 (password optional), or connector package split.
- Prefer minimal change: `shlex.quote` on every interpolated token for POSIX remotes; keep Fabric `c.put` (already shell-free). Do **not** switch checksum to SFTP/`hashlib` in this PR unless quoting proves insufficient (that is a larger behavior/compat change).
- Preserve public API of `SSHConnector` (`base_filter_sub_method`, `calculate_checksum`, `move_func`, etc.).
- Tests: unit path via `uv run pytest -m "not ssh"`; space-path integration under `@pytest.mark.ssh` / `OELEO_SSH_TESTS=1`.
- Follow agent rule from [code-review-security.md](.issueflows/04-designs-and-guides/code-review-security.md): any new SSH remote invocation must quote or avoid the shell.

### Prior art

- `SSHConnector._list_content` — [`oeleo/connectors.py`](oeleo/connectors.py): `find {directory} [-maxdepth N] -name '{glob}'` unquoted directory; single-quoted glob (breaks on `'` / metacharacters).
- `SSHConnector.calculate_checksum` — `md5sum "{directory/f}"` (double quotes only; `$`, `` ` ``, `\` still dangerous).
- `SSHConnector._ensure_remote_dir` — `mkdir -p "{remote_dir}"` (same).
- Debug helpers `_check_connection_and_exit` / `check_connection_and_exit` — same `find` pattern; quote for consistency.
- `SSHConnector.move_func` — uses `c.put` (shell-free); only `_ensure_remote_dir` is the shell risk on the copy path.
- Design: [code-review-security.md](.issueflows/04-designs-and-guides/code-review-security.md) SEC-01 mitigations (quote preferred over SFTP for this issue size).
- Integration: [`tests/test_ssh_integration.py`](tests/test_ssh_integration.py) — no spaces today; fixture itself builds unquoted setup cmds (fix when adding space-path coverage).
- Toolbox: none. Graph: none. Grep: no existing `shlex` usage in package.

## Approach

1. **Helper** — Add a small private helper on `SSHConnector` (or module-level), e.g. `_remote_shell_token(value) -> str`, that stringifies path-likes and applies `shlex.quote` for POSIX (`is_posix=True`). Use it for every interpolated shell token.
2. **Quote call sites (POSIX):**
   - `_list_content`: quote `self.directory` and `glob_pattern`; keep `max_depth` as int-only (no string interpolation of untrusted depth).
   - `calculate_checksum`: quote `self.directory / f`.
   - `_ensure_remote_dir`: quote `remote_dir`.
   - Both connection-check helpers: quote `self.directory`.
3. **Windows remote (`is_posix=False`)** — Leave cmd shape (`dir` / `if not exist … mkdir`) but avoid naive `"` wrapping that still allows injection; either apply a documented Windows-safe escape or **scope Windows quoting as best-effort / follow-up** if unused by CI and lab path (see Open questions). Do not silently claim full Windows shell safety without a test.
4. **Unit tests (no Docker)** — Mock `Connection.run` (or inject a fake `c`):
   - Path with spaces builds a command containing `shlex.quote`’d tokens (and does not leave bare `my dir`).
   - Path / name with `;` or `$()` appears only inside quoted tokens (assert exact command string for a few fixtures).
   - Cover `_list_content`, `calculate_checksum`, `_ensure_remote_dir` at minimum.
5. **SSH integration (gated)** — Extend `tests/test_ssh_integration.py`: create remote dir/file with a space in the path (quote fixture setup cmds too); assert `move_func` and/or `base_filter_sub_method` / checksum succeed. Skip remains when `OELEO_SSH_TESTS != 1`.
6. **Design memory** — Mark SEC-01 done in security + overview + backlog when landing.

## Files to touch

| Path | Change |
|------|--------|
| [`oeleo/connectors.py`](oeleo/connectors.py) | Quote helper + apply at all SSH shell construction sites |
| [`tests/test_oeleo.py`](tests/test_oeleo.py) or new `tests/test_ssh_shell_safety.py` | Unit tests with mocked Fabric `run` |
| [`tests/test_ssh_integration.py`](tests/test_ssh_integration.py) | Space-in-path case; quote fixture remote cmds |
| [`.issueflows/04-designs-and-guides/code-review-security.md`](.issueflows/04-designs-and-guides/code-review-security.md) | Mark SEC-01 addressed |
| [`.issueflows/04-designs-and-guides/code-review-overview.md`](.issueflows/04-designs-and-guides/code-review-overview.md) | Strike SEC-01 in severity table |
| [`.issueflows/04-designs-and-guides/code-review-improvement-backlog.md`](.issueflows/04-designs-and-guides/code-review-improvement-backlog.md) | Mark #18 done |

## Test strategy

- Default CI / local: `uv run pytest -m "not ssh"` — must cover quoting via mocks.
- Optional: `OELEO_SSH_TESTS=1` + `uv run pytest -m ssh` for space-path integration (agent runs if env/Docker available; otherwise document as manual/CI-gated).
- No change to SharePoint / local connector tests expected.

## Open questions

1. **Windows remote quoting scope?** Recommended: **POSIX is the acceptance bar** (matches Docker SSH tests and typical `is_posix=True` deployments); apply a light Windows escape or leave Windows cmds with a short code comment + backlog note if no Windows SSH test harness exists.
2. **SFTP checksum/`mkdir` instead of shell?** Recommended: **no for this PR** — quoting satisfies SEC-01 acceptance; SFTP can be a follow-up if we want shell-free ops entirely.
3. **Reject “dangerous” path characters at validate time?** Recommended: **no** — quoting is enough; rejection would break legitimate lab paths with spaces.

## Scope check

Single connector concern, focused files, one PR. Fits without splitting.
