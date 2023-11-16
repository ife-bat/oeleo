import hashlib
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import os

import dotenv
import peewee
from rich.logging import RichHandler


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


def logger(name="oeleo", log_level=logging.DEBUG, screen=False, log_message_format=None):
    dotenv.load_dotenv()

    log = logging.getLogger(name)
    log.setLevel(log_level)

    # create logger for console:
    if screen:
        console_log_message_format = log_message_format or "%(message)s"
        console_formatter = logging.Formatter(
            console_log_message_format,
            datefmt="[%X]"
        )
        console_handler = RichHandler(rich_tracebacks=True, tracebacks_suppress=[peewee])
        console_handler.setLevel(log_level)
        console_handler.setFormatter(console_formatter)
        log.addHandler(console_handler)

    # create logger for file:
    logdir = os.environ.get("OELEO_LOG_DIR", os.getcwd())
    logdir = Path(logdir)
    logdir.mkdir(exist_ok=True)
    log_path = logdir / "oeleo.log"
    file_handler = RotatingFileHandler(
        log_path,
        maxBytes=FILE_LOG_MAX_BYTES,
        backupCount=FILE_LOG_BACKUP_COUNT)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(FILE_LOG_MESSAGE_FORMAT))
    log.addHandler(file_handler)
    return log
