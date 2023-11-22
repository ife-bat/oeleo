import logging
import os
from datetime import datetime
from pathlib import Path

import dotenv

from oeleo.console import console
from oeleo.workers import simple_worker, ssh_worker
from oeleo.schedulers import SimpleScheduler
from oeleo.utils import start_logger
from oeleo.reporters import LogReporter, LogAndTrayReporter

dotenv.load_dotenv()
start_logger(only_oeleo=True)


def check_connection():
    print("Checking connection")
    worker = ssh_worker(
        base_directory_to="/home/jepe@ad.ife.no/Temp",
        db_name=r"../test_databases/testdb_ssh.db",
        reporter=LogAndTrayReporter()
    )
    worker.connect_to_db()
    worker.external_connector.connect()
    cmd = f"find {worker.external_connector.directory} -maxdepth 1 -name '*'"
    worker.external_connector.c.run(cmd)
    worker.external_connector.close()


def example_bare_minimum():

    logging.setLevel(logging.DEBUG)
    logging.debug(f"Starting oeleo!")
    console.print(f"Starting oeleo!")

    worker = simple_worker()
    worker.connect_to_db()

    worker.check(update_db=True)
    worker.filter_local()
    worker.run()


def example_with_simple_scheduler():
    logging.info(f"<Starting oeleo!>")
    worker = simple_worker()
    logging.debug(f"{worker.bookkeeper=}")
    logging.debug(f"{worker.bookkeeper.db_name=}")
    logging.debug(f"{worker.local_connector=}")
    logging.debug(f"{worker.external_connector=}")
    logging.debug(f"{worker.reporter=}")
    logging.debug(f"{worker.file_names=}")
    s = SimpleScheduler(
        worker,
        run_interval_time=2,
        max_run_intervals=200,
        add_check=False,
    )
    s.start()


def example_ssh_worker_with_simple_scheduler():
    HOURS_SLEEP = 0.5
    FROM_YEAR = 2023
    FROM_MONTH = 3
    FROM_DAY = 1

    my_filters = [
        (
            "not_before",
            datetime(
                year=FROM_YEAR,
                month=FROM_MONTH,
                day=FROM_DAY,
                hour=0,
                minute=0,
                second=0,
            ),
        ),
    ]
    run_interval_time = 3600 * HOURS_SLEEP

    print("creating reporter")
    reporter = LogAndTrayReporter()
    print("reporter created")

    logging.debug(f"Starting oeleo!")
    worker = ssh_worker(
        base_directory_to="/home/jepe@ad.ife.no/Temp",
        db_name=r"../test_databases/testdb_ssh.db",
        reporter=reporter,
    )
    logging.info(f"{worker.bookkeeper=}")
    logging.info(f"{worker.bookkeeper.db_name=}")
    logging.info(f"{worker.local_connector=}")
    logging.info(f"{worker.external_connector=}")
    logging.info(f"{worker.reporter=}")
    logging.info(f"{worker.file_names=}")
    s = SimpleScheduler(
        worker,
        run_interval_time=2,  # run_interval_time
        max_run_intervals=20,
        additional_filters=my_filters,
        add_check=True,
    )
    s.start()


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
    print(80 * "=")
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
    """Check that the database is working correctly

    1. Connect to the database
    2. Dump the contents of the database
    3. Filter the database

    """
    from oeleo.utils import dump_worker_db_table

    logging.setLevel(logging.DEBUG)
    logging.debug(f"Starting oeleo!")
    console.print(f"Starting oeleo!")
    dotenv.load_dotenv()
    worker = simple_worker()
    worker.connect_to_db()
    dump_worker_db_table(worker, verbose=True)
    worker.filter_local()


def check_db_dumper():
    from oeleo.utils import dump_db

    dump_db()


if __name__ == "__main__":
    example_ssh_worker_with_simple_scheduler()
