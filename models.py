import datetime
import random
from pathlib import Path
from typing import Any

import peewee

DATABASE = peewee.SqliteDatabase(None)
DEFAULT_DB_NAME = "oeleo-file-list.db"

CODES = [
    (0, "should-be-copied"),
    (1, "should-be-copied-if-changed"),
    (2, "should-not-be-copied"),
]


class FileList(peewee.Model):
    processed_date = peewee.DateTimeField(default=datetime.datetime.now())
    local_name = peewee.CharField(unique=True)
    external_name = peewee.CharField(null=True)
    checksum = peewee.CharField(null=True)
    code = peewee.SmallIntegerField(choices=CODES, default=0)

    class Meta:
        database = DATABASE


class DbHandler:
    pass


class MockDbHandler:
    def __init__(self):
        self.db_name = "mock"

    @staticmethod
    def initialize_db():
        print("INITIALIZING DB")

    @staticmethod
    def register(f: Path):
        print(f"REGISTERING {f}")

    @staticmethod
    def is_changed(**checks) -> bool:
        print(f"CHECKING IF IT HAS CHANGED")
        print(f"checks: {checks}")
        _is_changed = random.choice([True, False])
        print(f"is-changed: {_is_changed}")
        return _is_changed

    @staticmethod
    def update_record(external_name: Path, **checks: Any):
        print("UPDATE RECORD IN DB")
        print(f"external name: {external_name}")
        print(f"additional: {checks}")


class SimpleDbHandler(DbHandler):
    CHECK_ON = "checksum"

    def __init__(self, db_name: str) -> None:
        self.db_name = db_name
        self.db_model: peewee.Model = FileList
        self._current_record = None
        self.db_instance = DATABASE

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
        self._current_record, new = self.db_model.get_or_create(local_name=f.name)
        if new:
            self.record.code = 0
            self.record.save()

    def is_changed(self, **checks) -> bool:
        if self.record.code == 0:
            return True

        _is_changed = False
        for k in checks:
            print(k)
            try:
                v = getattr(self.record, k)
            except AttributeError as e:
                raise AttributeError("oeleo-model-key mismatch") from e
            print(v)
            print(checks[k])
            if v != checks[k]:
                _is_changed = True
        return _is_changed

    def update_record(self, external_name: Path, code: int = 1, **checks: str):
        checksum = checks.get("checksum", None)
        self.record.checksum = checksum
        self.record.processed_date = datetime.datetime.now()
        self.record.code = code
        self.record.external_name = external_name
        self.record.save()

    @property
    def code(self):
        return self.record.code

    @code.setter
    def code(self, code):
        if code not in (0, 1, 2):
            raise ValueError(f"code is not valid")
        self.record.code = code
        self.record.save()
