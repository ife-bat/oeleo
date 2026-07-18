# Code review: architecture & maintainability

See [`code-review-overview.md`](code-review-overview.md) for the index and severity table.

## Intended design (good)

The library is organized around a small set of protocols/roles:

| Role | Implementation | Responsibility |
|------|----------------|----------------|
| Connector | `LocalConnector`, `SSHConnector`, `SharePointConnector` | list, checksum, move, connect/close |
| Checker | `ChecksumChecker` | produce `{checksum: …}` for bookkeeper |
| Bookkeeper | `SimpleDbHandler` / `MockDbHandler` | persist last known state + copy codes |
| Reporter | `Reporter`, `LogReporter`, `LogAndTrayReporter` | UX / tray / die / force-run |
| Worker | `Worker` | orchestrate filter → check/run |
| Scheduler | `SimpleScheduler` | interval loop around a worker |

Factories (`simple_worker`, `ssh_worker`, `sharepoint_worker`) hide env wiring. That is the right public surface for scripts and `app/oa.pyw`.

### Data flow

```text
filter_local()  → Worker.file_names
check()         → compare local vs external listing + optional DB update
run()           → for each file: register → is_changed → move → update_record
```

Codes (documented in README): `0` copy, `1` copy-if-changed, `2` never copy (lock). Enforcement of `2` is incomplete — see correctness doc **BUG-01**.

## Coupling & hotspots

### God-ish modules

- **`oeleo/connectors.py` (~450 lines):** three connectors + SharePoint auth helper + password registration. Local/SSH/SharePoint share a Protocol but diverge sharply (SSH remote shell vs SharePoint API). Candidate split: `connectors/local.py`, `connectors/ssh.py`, `connectors/sharepoint.py` — only when an issue needs it.
- **`oeleo/workers.py`:** orchestration + three factories + chunking + (disabled) threading. Still readable; avoid growing more connector-specific logic here — keep that in connectors/name generators.
- **`oeleo/reporters.py`:** console + log + tray + PIL icon drawing. Tray code is optional-dep heavy; keep imports guarded (already done).

### Cross-cutting smells

| ID | Smell | Evidence | Suggestion |
|----|-------|----------|------------|
| ARCH-01 | Module-global Peewee proxy | `models.database_proxy` shared by all `SimpleDbHandler` instances | Per-handler `SqliteDatabase` instance; drop proxy or scope it to one process/DB |
| ARCH-02 | Mutable dataclass default | ~~`Worker.reporter: ReporterBase = Reporter()`~~ — fixed (#35) | `field(default_factory=Reporter)` |
| ARCH-03 | Wrong `Protocol` import | ~~`from asyncio import Protocol`~~ — fixed (#35) | `from typing import Protocol` (same as models/connectors) |
| ARCH-04 | Eager connect in ctor | `Worker.__post_init__` calls `external_connector.connect()` | Connect lazily in `run`/`check` or factories; document lifecycle |
| ARCH-05 | Env as implicit API | Many `os.environ["OELEO_…"]` KeyErrors deep in constructors | Small `Settings`/`Config` dataclass loaded once with validation + clear errors (used by factories + app) |
| ARCH-06 | Incomplete Protocol parity | SSH additional_filters logged as unimplemented; SharePoint filter is substring `in` name | Document capability matrix; raise `NotImplementedError` or implement |

## API consistency issues

1. **Extension type:** factories type `extension: str` but `base_filter` accepts `list` of extensions (`main.simple_multi_dir` passes a list). Typing/docs should allow `str | list[str]`.
2. **`register_password`:** name implies “set password”; implementation only prompts when `pwd is None` and never assigns a provided password (**BUG-05**).
3. **Destructor misuse:** `__delete__` on connectors is not a Python finalizer (`__del__`). Dead/wrong hook — remove or replace with context manager (`__enter__`/`__exit__`).
4. **`connected_mover`:** thin wrapper rarely used by `Worker` (worker calls `connector.move_func` directly). Keep as public helper or demote to tests.

## Dead / duplicate / inconsistent code (CLEAN-*)

| Item | Location | Action |
|------|----------|--------|
| `base_filter_old` | `filters.py` | Delete once confirmed unused |
| `_check_connection_and_exit` + `check_connection_and_exit` | `SSHConnector` | Keep one debug helper or move to `check/` playground |
| Unused imports in `workers.py` | `multiprocessing`, `Panel`, `Text`, `ceil`, … | Trim when touching file |
| Dual consoles | `console.py` `simple_console` vs `console` | Merge or document why both exist |
| `main.py` as scratchpad | hard-coded developer paths | Keep examples generic or move to `docs/examples/` |
| Mix of `log` / `logging` / `print` | connectors, movers, reporters | Standardize on `log = logging.getLogger("oeleo")` |

## Suggested structural improvements (incremental)

1. **Config object** — single place for OELEO_* / OA_* parsing (`to_bool`, ints, path lists). Biggest UX win for “easy to use”.
2. **Capability matrix** in designs folder once filters/checksum differ by connector.
3. **Context-managed connectors** — `with ssh_worker(...) as w:` calling `close()`.
4. **Leave factories stable** — prefer additive kwargs over renaming public functions.
5. **CLI (README wishlist)** — wrap factories; do not invent a second orchestration path. Epic-sized.

## What not to do without an epic

- Rewrite peewee → SQLAlchemy/another ORM.
- Enable `use_threads=True` without fixing logging/DB thread-safety first.
- Merge app + library into one entrypoint framework.
- Bidirectional sync / remote-as-source-of-truth (contradicts product model).
