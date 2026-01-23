import hashlib
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import os

import dotenv
import peewee
from rich.logging import RichHandler

from oeleo.models import SimpleDbHandler

STDOUT_LOG_MESSAGE_FORMAT = "%(message)s"
FILE_LOG_MESSAGE_FORMAT = "[%(asctime)s - %(name)s] || %(levelname)7s || %(message)s"
FILE_LOG_MESSAGE_FORMAT_ALL = (
    "[%(asctime)s - %(name)24s] || %(levelname)7s || %(message)s"
)

FILE_LOG_MAX_BYTES = 1_000_000
FILE_LOG_BACKUP_COUNT = 3


def to_bool(value):
    """Convert a value to a boolean"""
    if not value:
        return False
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        value = value.lower()
        if value in ["true", "yes", "y", "1"]:
            return True
        if value in ["false", "no", "n", "0"]:
            return False
    raise ValueError(f"Could not convert {value} to a boolean")


def calculate_checksum(file_path: Path) -> str:
    with open(file_path, "rb") as f:
        file_hash = hashlib.md5()
        while chunk := f.read(8192):
            file_hash.update(chunk)
    return file_hash.hexdigest()


def get_log_path(logdir=None) -> Path:
    if logdir is None:
        logdir = os.environ.get("OELEO_LOG_DIR", os.getcwd())
    logdir = Path(logdir)
    return logdir / "oeleo.log"


def start_logger(logdir=None, only_oeleo=False, screen_level=logging.CRITICAL):
    """Start logging to file for the oeleo package"""

    log = logging.getLogger()
    log.setLevel(logging.DEBUG)

    # create screen logger:
    screen_handler = RichHandler()
    screen_handler.setLevel(screen_level)
    screen_handler.setFormatter(logging.Formatter(STDOUT_LOG_MESSAGE_FORMAT))
    log.addHandler(screen_handler)

    # create start_logger for file:
    if logdir is None:
        logdir = os.environ.get("OELEO_LOG_DIR", os.getcwd())

    logdir = Path(logdir)

    try:
        logdir.mkdir(exist_ok=True)
    except Exception as e:
        log.debug(f"Could not use log directory {logdir}: {e}")
        logdir = Path(os.getcwd())
        log.debug(f"Using {logdir} instead")

    log_path = get_log_path(logdir)
    file_handler = RotatingFileHandler(
        log_path, maxBytes=FILE_LOG_MAX_BYTES, backupCount=FILE_LOG_BACKUP_COUNT
    )
    file_handler.setLevel(logging.DEBUG)

    if only_oeleo:
        file_handler.addFilter(logging.Filter("oeleo"))
        file_handler.setFormatter(logging.Formatter(FILE_LOG_MESSAGE_FORMAT))
        screen_handler.addFilter(logging.Filter("oeleo"))
    else:
        file_handler.setFormatter(logging.Formatter(FILE_LOG_MESSAGE_FORMAT_ALL))

    log.addHandler(file_handler)


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
        logging.info("... dumping 'filelist' table")
        logging.info(f"... file: {bookkeeper.db_name}")
        logging.info(" records ".center(80, "="))
    n_records = len(bookkeeper.db_model)
    if code is None:
        records = bookkeeper.db_model.filter()
    else:
        records = bookkeeper.db_model.filter(code=code)
    if verbose:
        for i, record in enumerate(records):
            logging.info(
                f" pk {record._pk:03} [{i:03}:{n_records:03}] ".center(80, "-")
            )
            logging.info(f"local_name:     {record.local_name}")
            logging.info(f"external_name:  {record.external_name}")
            logging.info(f"code:           {record.code}")
            logging.info(f"processed_date: {record.processed_date}")
            logging.info(f"checksum:       {record.checksum}")

        logging.info(80 * "=")
    else:
        for record in records:
            txt = f"{record._pk:05}\tc={record.code}\tlf={record.local_name}\tef={record.external_name}"
            logging.info(txt)
