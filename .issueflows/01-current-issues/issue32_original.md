# Issue #32: Make OELEO_PASSWORD optional for key-based SSH

Source: https://github.com/ife-bat/oeleo/issues/32

## Original issue text

## Summary
`SSHConnector.__init__` requires `OELEO_PASSWORD` from the environment even when `use_password=False` (key-based auth). Operators using keys still need a dummy password env var.

**Finding ID:** SEC-03  
**Size:** yolo-fit  
**Design doc:** `.issueflows/04-designs-and-guides/code-review-security.md`

## Fix direction
When `use_password=False`, do not require `OELEO_PASSWORD`. Keep requiring it (or prompt path) when password auth is used.

## Acceptance
- [ ] Key-based SSH works without `OELEO_PASSWORD` set
- [ ] Password auth still fails clearly if password is missing
- [ ] No logging of password/key material
