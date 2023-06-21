import logging
import os
from datetime import datetime
from pathlib import Path

import dotenv

from oeleo.console import console
from oeleo.utils import logger
from oeleo.workers import simple_worker

log = logger()


def example_bare_minimum():
    log.setLevel(logging.DEBUG)
    log.debug(f"Starting oeleo!")
    console.print(f"Starting oeleo!")
    dotenv.load_dotenv()
    worker = simple_worker()
    worker.connect_to_db()

    # worker.check(update_db=True)
    worker.filter_local()
    worker.run()


def dump_oeleo_db_table(worker, code=None, verbose=True):
    if verbose:
        print("... dumping 'filelist' table")
        print(f"... file: {worker.bookkeeper.db_name}")
        print(" records ".center(80, "="))

    n_records = len(worker.bookkeeper.db_model)
    if code is None:
        records = worker.bookkeeper.db_model.filter()
    else:
        records = worker.bookkeeper.db_model.filter(code=code)

    if verbose:
        for i, record in enumerate(records):
            print(f" pk {record._pk:03} [{i:03}:{n_records:03}] ".center(80, "-"))
            print(f"local_name:     {record.local_name}")
            print(f"external_name:  {record.external_name}")
            print(f"code:           {record.code}")
            print(f"processed_date: {record.processed_date}")
            print(f"checksum:       {record.checksum}")

        print(80 * "=")
    else:
        for record in records:
            txt = f"{record._pk:05}\tc={record.code}\tlf={record.local_name}\tef={record.external_name}"
            print(txt)


def inspect_db(worker, table="filelist"):
    print(80*"=")
    print(f"db: {worker.bookkeeper.db_name}")
    tables = worker.bookkeeper.db_instance.obj.get_tables()
    print(f"tables: {tables}")
    if table is None:
        return

    print(f"selected table: {table}")
    columns = worker.bookkeeper.db_instance.obj.get_columns(table)
    print(f"columns:")
    for col in columns:
        print(f"  - {col.name}")
    n_records = len(worker.bookkeeper.db_model)

    print(f"number of records: {n_records}")
    print(80 * "=")


def check_01():
    log.setLevel(logging.DEBUG)
    log.debug(f"Starting oeleo!")
    console.print(f"Starting oeleo!")
    dotenv.load_dotenv()
    worker = simple_worker()
    worker.connect_to_db()
    dump_oeleo_db_table(worker, verbose=False)
    worker.filter_local()


if __name__ == "__main__":
    check_01()
