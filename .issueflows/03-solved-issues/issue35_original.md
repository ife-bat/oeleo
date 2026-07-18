# Issue #35: Fix Worker.reporter default_factory and typing.Protocol import

Source: https://github.com/ife-bat/oeleo/issues/35

## Original issue text

## Summary
`Worker.reporter` uses a mutable dataclass default (`Reporter()`), and `workers.py` imports `Protocol` from `asyncio` instead of `typing`.

**Finding IDs:** ARCH-02, ARCH-03  
**Size:** yolo-fit  
**Design doc:** `.issueflows/04-designs-and-guides/code-review-architecture.md`

## Fix direction
- `reporter: ReporterBase = field(default_factory=Reporter)`
- `from typing import Protocol` (same as models/connectors)

## Acceptance
- [ ] Fresh `Worker` instances do not share one reporter object
- [ ] Protocol import is from `typing`
- [ ] Unit tests still pass
