# Code review: correctness & reliability

See [`code-review-overview.md`](code-review-overview.md) for the index.

## High severity

### BUG-01 — Locked files (`code=2`) still copy on `run`

**Documented behavior (README):** editing `code` to `2` locks a file so it should never be copied.

**Actual `check` path:** respects lock via `if self.bookkeeper.code < 2` before updating.

**Actual `run` path:** `SimpleDbHandler.is_changed` only short-circuits for `code == 0`:

```python
# models.py — is_changed
if self.record.code == 0:
    return True
# no early False for code == 2
```

So a locked file whose checksum changed (or was never stored) can still be transferred in `_process_file`.

**Fix direction:** In `is_changed` (or at start of `_process_file`): if `code == 2`, return `False` / skip. Add a unit test that sets `code=2`, mutates the file, runs worker, asserts destination unchanged.

**Issue size:** small, **yolo-fit**.

---

### BUG-02 — Bookkeeping uses basename only (subdir collisions)

`SimpleDbHandler.register` does:

```python
self._current_record, new = self.db_model.get_or_create(local_name=f.name)
```

With `include_subdirs=True`, `a/foo.csv` and `b/foo.csv` share one DB row. Checksums/codes overwrite each other; wrong skip/copy decisions follow. External path generation *can* preserve relative paths (`Worker._default_external_name_generator`), but the DB key cannot distinguish them.

**Fix direction:** Store relative path from `local_connector.directory` (POSIX-normalized string) as `local_name` uniqueness key; migrate existing DBs carefully (docs + optional rewrite tool under `.issueflows/00-tools/`).

**Issue size:** medium–large; likely **epic** if migration required, or a breaking change flagged in changelog.

---

### BUG-03 — `app/oa.pyw` references missing `worker.db_path`

```python
log.debug(f"*A2O* connecting to db ({worker.db_path})")
```

`Worker` has no `db_path`. AttributeError on `OA_SINGLE_RUN=true` before transfer. Scheduled multi-run path does not hit this line.

**Fix:** log `worker.bookkeeper.db_name` (or add a property). **yolo-fit**.

---

### ~~REL-01 — Reconnect before every file~~ (done in #17)

~~`Worker` defaults `reconnect=True`.~~ **Resolved:** default is `reconnect=False`; opt-in via `Worker(..., reconnect=True)`, factory `reconnect=`, or `OELEO_RECONNECT`. Failed moves still reconnect once and retry. Per-file reconnect remains available for flaky networks.

## Medium severity

### BUG-04 — Peewee default timestamp frozen at import

```python
processed_date = peewee.DateTimeField(default=datetime.datetime.now())
```

`now()` runs once at class definition. New rows without an explicit `processed_date` can share the same stale timestamp. `update_record` sets `datetime.now()` explicitly (OK for updates); `get_or_create` path may not.

**Fix:** `default=datetime.datetime.now` (callable) or `peewee.DateTimeField(default=datetime.datetime.now)`.

**yolo-fit.**

---

### BUG-05 — `register_password(pwd)` ignores `pwd`

```python
def register_password(pwd: str = None) -> None:
    if pwd is None:
        session_password = getpass.getpass(...)
        os.environ["OELEO_PASSWORD"] = session_password
```

Call sites like `register_password(os.environ["OELEO_PASSWORD"])` are no-ops. Either set `os.environ` when `pwd` is provided, or rename to `prompt_password()`.

**yolo-fit.**

---

### BUG-06 — `SharePointConnection.reconnect` broken

```python
def reconnect(self, **kwargs) -> None:
    self.close()
    self.connect()  # method does not exist on SharePointConnection
```

If anything calls this helper’s `reconnect`, it fails. `SharePointConnector.reconnect` uses Protocol default → `SharePointConnector.connect` (OK). Dead/broken helper still a footgun.

**yolo-fit** cleanup.

---

### REL-02 — Soft failures become silent skips

Examples:

- SSH `_list_content`: catches Exception, prints, returns `[]` → empty remote listing may mark everything out of sync or miss duplicates.
- SSH `calculate_checksum`: failed `md5sum` logs “should raise” but still parses stdout.
- SharePoint `calculate_checksum` returns `False` on error (type says `Hash` / str) → comparison weirdness.
- Local `simple_mover` uses `print` on failure; caller only sees `False`.

**Fix direction:** typed exceptions (`OeleoConnectionError`, `OeleoTransferError`); fail the run or per-file with reporter notify; never return sentinel `False` as checksum.

**Issue size:** medium; good epic stage “harden connector errors”.

---

### REL-03 — Generator consumption / `file_names` lifecycle

`filter_local` may leave a generator in `file_names`. `run` chunks it once; a second `run` without re-filter sees empty. `add_local` warns about generators; `filter_local` does not always materialize to `list`.

**Fix:** materialize to `list` in `filter_local` (tests already often use lists from local connector when extension is list; glob generators are the risk).

**yolo-fit.**

---

### REL-04 — `die_if_necessary` calls `sys.exit(0)`

Tray quit → hard process exit from deep inside worker. Hard to test; surprising in library use. Prefer raising a dedicated exception caught by scheduler/app.

**Medium**, app-focused.

## Lower severity / polish

| ID | Issue |
|----|-------|
| REL-05 | `Reporter.progress` swallows exceptions with `print("*")` |
| REL-06 | `LogAndTrayReporter._update_icon` infinite loop with no stop flag (relies on daemon thread) |
| REL-07 | `MockDbHandler.is_changed` is random — fine for demos, dangerous if used in “tests” accidentally |
| REL-08 | `check()` uses `force=True` default; docstring and `SimpleScheduler` interact subtly — document |

## Recommended test additions (pair with fixes)

1. Locked `code=2` never copied after local change.
2. Two same basenames in different subdirs get two DB rows and two destinations.
3. `OA_SINGLE_RUN` path does not AttributeError.
4. Failed SSH list does not look like “empty directory” without error status.
5. ~~`reconnect=False` performs one connect for N successful copies (mock Fabric Connection).~~ — covered by unit tests in #17.
