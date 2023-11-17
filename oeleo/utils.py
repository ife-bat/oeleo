import hashlib
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import os

import dotenv
import peewee
from rich.logging import RichHandler

from oeleo.models import SimpleDbHandler


# FILE_LOG_MESSAGE_FORMAT = "%(asctime)s - %(name)s (%(filename)s-%(funcName)s) - %(levelname)s - %(message)s"
FILE_LOG_MESSAGE_FORMAT = "[%(asctime)s - %(name)s] || %(levelname)7s || %(message)s"
FILE_LOG_MAX_BYTES = 1_000_000
FILE_LOG_BACKUP_COUNT = 3


def calculate_checksum(file_path: Path) -> str:
    with open(file_path, "rb") as f:
        file_hash = hashlib.md5()
        while chunk := f.read(8192):
            file_hash.update(chunk)
    return file_hash.hexdigest()


def logger(
    name="oeleo", log_level=logging.DEBUG, screen=False, log_message_format=None
):
    """Create a logger for the oeleo package"""

    log = logging.getLogger(name)
    log.setLevel(log_level)

    # create logger for console:
    if screen:
        console_log_message_format = log_message_format or "%(message)s"
        console_formatter = logging.Formatter(
            console_log_message_format, datefmt="[%X]"
        )
        console_handler = RichHandler(
            rich_tracebacks=True, tracebacks_suppress=[peewee]
        )
        console_handler.setLevel(log_level)
        console_handler.setFormatter(console_formatter)
        log.addHandler(console_handler)

    # create logger for file:
    logdir = os.environ.get("OELEO_LOG_DIR", os.getcwd())
    logdir = Path(logdir)
    logdir.mkdir(exist_ok=True)
    log_path = logdir / "oeleo.log"
    file_handler = RotatingFileHandler(
        log_path, maxBytes=FILE_LOG_MAX_BYTES, backupCount=FILE_LOG_BACKUP_COUNT
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(FILE_LOG_MESSAGE_FORMAT))
    log.addHandler(file_handler)
    return log


def dump_db(db_name=None, code=None, verbose=False, output_format="human"):
    """Dump the contents of the database"""
    db_name = db_name or os.environ.get("OELEO_DB_NAME")
    if db_name is None:
        raise ValueError("db_name must be provided")
    bookkeeper = SimpleDbHandler(db_name)
    bookkeeper.initialize_db()
    dump_bookkeeper(bookkeeper, code=code, verbose=verbose, output_format=output_format)


def dump_worker_db_table(worker, code=None, verbose=True, output_format="human"):
    """Dump the contents of the database"""
    bookkeeper = worker.bookkeeper
    dump_bookkeeper(bookkeeper, code=code, verbose=verbose, output_format=output_format)


def dump_bookkeeper(bookkeeper, code=None, verbose=False, output_format="human"):
    # currently only dumps to screen in a human-readable format
    # TODO: option to dump as csv-table
    # TODO: option to dump as json
    # TODO: option to dump to log

    if verbose:
        print("... dumping 'filelist' table")
        print(f"... file: {bookkeeper.db_name}")
        print(" records ".center(80, "="))
    n_records = len(bookkeeper.db_model)
    if code is None:
        records = bookkeeper.db_model.filter()
    else:
        records = bookkeeper.db_model.filter(code=code)
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
