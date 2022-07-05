import hashlib
import logging
from pathlib import Path

import peewee
from rich.logging import RichHandler


def calculate_checksum(file_path: Path) -> str:
    with open(file_path, "rb") as f:
        file_hash = hashlib.md5()
        while chunk := f.read(8192):
            file_hash.update(chunk)
    return file_hash.hexdigest()


def logger(name="oeleo", log_level=logging.INFO, log_message_format=None):
    log_message_format = log_message_format or "%(message)s"

    logging.basicConfig(
        format=log_message_format,
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True, tracebacks_suppress=[peewee])],
    )

    log = logging.getLogger(name)
    log.setLevel(log_level)
    return log
