import datetime
from pathlib import Path

import peewee

DATABASE = peewee.SqliteDatabase(None)
DEFAULT_DB_NAME = "oeleo-file-list.db"

CODES = [
    (0, "new"),
    (1, "updated-minimum-once"),
    (2, "locked"),
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
        _is_changed = False
        for k in checks:
            try:
                v = getattr(self.record, k)
            except AttributeError as e:
                raise AttributeError("oeleo-model-key mismatch") from e
            if v != checks[k]:
                _is_changed = True
        return _is_changed

    def update_record(self, external_name: Path, checksum: str):
        self.record.checksum = checksum
        self.record.processed_date = datetime.datetime.now()
        self.record.code = 1
        self.record.external_name = external_name
        self.record.save()
