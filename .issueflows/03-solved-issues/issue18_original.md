# Issue #18: Shell-safe remote path handling in SSHConnector

Source: https://github.com/ife-bat/oeleo/issues/18

## Original issue text

## Summary
`SSHConnector` builds remote shell commands with string interpolation (`find`, `md5sum`, `mkdir -p`). Metacharacters or awkward paths can break commands or enable injection.

**Finding ID:** SEC-01  
**Size:** standard  
**Design doc:** `.issueflows/04-designs-and-guides/code-review-security.md`

## Fix direction
Prefer APIs that avoid a shell; otherwise `shlex.quote` every interpolated token. Add SSH tests with spaces in paths.

## Acceptance
- [ ] Remote path/glob interpolation is quoted or shell-free
- [ ] Integration test covers a remote path containing spaces (where feasible)
