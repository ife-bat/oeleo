import datetime
from pathlib import Path

import peewee

db = peewee.SqliteDatabase(None)

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
        database = db


implemented_models = [FileList]


def initialize_db(database_name: str = DEFAULT_DB_NAME) -> peewee.Database:
    db.init(database_name)
    db.connect()
    db.create_tables(implemented_models)
    return db


def get_record_and_status(f: Path, checksum):
    record, new = FileList.get_or_create(local_name=f.name)
    needs_updating = True
    if new:
        print(f"Creating a new record for {f.name}")
        record.checksum = checksum
        record.code = 0
        record.save()
    else:
        print(f"Reading record for {f.name}")
        if record.checksum == checksum:
            needs_updating = False
    return record, needs_updating


def update(record, external_name: Path, checksum: str):
    record.checksum = checksum
    record.processed_date = datetime.datetime.now()
    record.code = 1
    record.external_name = external_name
    record.save()
