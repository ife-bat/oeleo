import logging
import os
from datetime import datetime
from pathlib import Path

import dotenv

from oeleo.connectors import register_password
from oeleo.console import console
from oeleo.schedulers import RichScheduler, SimpleScheduler
from oeleo.utils import logger
from oeleo.workers import simple_worker, ssh_worker, sharepoint_worker

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


def check_01():
    print("hei")


if __name__ == "__main__":
    check_01()
