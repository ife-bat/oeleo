import datetime
import logging
import random
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Protocol, Union

import peewee

DEFAULT_DB_NAME = "oeleo-file-list.db"

CODES = [
    (0, "should-be-copied"),
    (1, "should-be-copied-if-changed"),
    (2, "should-not-be-copied"),
]

database_proxy = peewee.DatabaseProxy()
log = logging.getLogger("oeleo")


class FileList(peewee.Model):
    processed_date = peewee.DateTimeField(default=datetime.datetime.now())
    local_name = peewee.CharField(unique=True)
    external_name = peewee.CharField(null=True)
    checksum = peewee.CharField(null=True)
    code = peewee.SmallIntegerField(choices=CODES, default=0)

    class Meta:
        database = database_proxy


class DbHandler(Protocol):
    db_name: Union[Path, str] = None

    def initialize_db(self):
        ...

    def register(self, f: Path):
        ...

    def is_changed(self, record: Any, **checks: Any) -> bool:
        ...

    def update_record(
        self, record: Any, external_name: Path, code: int = 1, **checks: Any
    ):
        ...


class MockDbHandler(DbHandler):
    def __init__(self):
        self.db_name = "mock"
        self._current_record = None

    def initialize_db(self):
        print("INITIALIZING DB")

    def register(self, f: Path):
        print(f"REGISTERING {f}")
        self._current_record = SimpleNamespace(code=0)
        return self._current_record

    def is_changed(self, record: Any, **checks) -> bool:
        print("CHECKING IF IT HAS CHANGED")
        print(f"checks: {checks}")
        _is_changed = random.choice([True, False])
        print(f"is-changed: {_is_changed}")
        return _is_changed

    def update_record(
        self, record: Any, external_name: Path, code: int = 1, **checks: Any
    ):
        print("UPDATE RECORD IN DB")
        print(f"external name: {external_name}")
        print(f"additional checks: {checks}")
        if record is not None:
            record.code = code


class SimpleDbHandler(DbHandler):
    """A simple db bookkeeper using sqlite3 that checks on checksum."""

    def __init__(self, db_name: str) -> None:
        self.db_name = db_name
        self.db_model: peewee.Model = FileList
        self._current_record = None
        self.db_instance = database_proxy
        self._set_up_sqlite_db()

    @staticmethod
    def _set_up_sqlite_db():
        database_proxy.initialize(peewee.SqliteDatabase(None))

    def _ensure_connection(self) -> None:
        """Ensure this thread has an open connection."""
        if self.db_instance.is_closed():
            self.db_instance.connect(reuse_if_open=True)

    @property
    def record(self):
        return self._current_record

    @record.setter
    def record(self, value):
        self._current_record = value

    @record.deleter
    def record(self):
        self._current_record = None

    def initialize_db(self):
        self.db_instance.init(self.db_name)
        self.db_instance.connect()
        self.db_instance.create_tables([self.db_model])

    def register(self, f: Path):
        """Get or create record of the file and check if it needs to be copied."""
        self._ensure_connection()
        record, new = self.db_model.get_or_create(local_name=f.name)
        if new:
            record.code = 0
            record.save()
        return record

    def is_changed(self, record: FileList, **checks) -> bool:
        self._ensure_connection()
        if record.code == 0:
            return True

        _is_changed = False
        for k in checks:
            try:
                v = getattr(record, k)
            except AttributeError as e:
                raise AttributeError("oeleo-model-key mismatch") from e
            if v != checks[k]:
                _is_changed = True
        return _is_changed

    def update_record(
        self, record: FileList, external_name: Path, code: int = 1, **checks: Any
    ):
        self._ensure_connection()
        checksum = checks.get("checksum", None)
        record.checksum = checksum
        record.processed_date = datetime.datetime.now()
        record.code = code
        record.external_name = external_name
        record.save()

    @property
    def code(self):
        return self.record.code

    @code.setter
    def code(self, code):
        if code not in (0, 1, 2):
            raise ValueError("code is not valid")
        self.record.code = code
        self.record.save()
