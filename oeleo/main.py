import logging
import os
from datetime import datetime
from pathlib import Path

import dotenv

from oeleo.connectors import register_password
from oeleo.console import console
from oeleo.schedulers import SimpleScheduler, RichScheduler
from oeleo.utils import logger
from oeleo.workers import simple_worker, ssh_worker

log = logger()


def example_bare_minimum():
    log.setLevel(logging.DEBUG)
    log.debug(f"Starting oeleo!")
    console.print(f"Starting oeleo!")
    dotenv.load_dotenv()
    worker = simple_worker()
    worker.connect_to_db()

    worker.check(update_db=True)
    worker.filter_local()
    worker.run()


def example_with_simple_scheduler():
    log.setLevel(logging.DEBUG)
    log.debug(f"Starting oeleo!")
    dotenv.load_dotenv()
    worker = simple_worker()

    s = SimpleScheduler(
        worker,
        run_interval_time=2,
        max_run_intervals=2,
    )
    s.start()


def example_with_rich_scheduler():
    log.setLevel(logging.CRITICAL)
    dotenv.load_dotenv()
    worker = simple_worker()

    s = RichScheduler(
        worker,
        run_interval_time=4,
        max_run_intervals=4,
    )
    s.start()


def example_check_with_ssh_connection():
    print(" example_check_with_ssh_connection ".center(80, "-"))
    log.setLevel(logging.DEBUG)
    log.info(f"Starting oeleo!")
    dotenv.load_dotenv()

    external_dir = "/home/jepe@ad.ife.no/Temp"
    filter_extension = ".res"

    register_password(os.environ["OELEO_PASSWORD"])

    worker = ssh_worker(
        db_name=r"C:\scripting\oeleo\test_databases\test_ssh_to_odin.db",
        base_directory_from=Path(r"C:\scripting\processing_cellpy\raw"),
        base_directory_to=external_dir,
        extension=filter_extension,
    )
    worker.connect_to_db()
    try:
        worker.check(update_db=True)
        worker.filter_local()
        worker.run()
    finally:
        worker.close()


def example_check_first_then_run():
    print(" example_check_first_then_run ".center(80, "-"))
    log.setLevel(logging.DEBUG)
    log.info(f"Starting oeleo!")

    not_before = datetime(year=2021, month=3, day=1, hour=1, minute=0, second=0)
    not_after = datetime(year=2022, month=7, day=1, hour=1, minute=0, second=0)

    my_filters = [
        ("not_before", not_before),
        ("not_after", not_after),
    ]

    dotenv.load_dotenv()
    filter_extension = "res"
    worker = simple_worker(
        db_name=r"C:\scripting\oeleo\test_databases\another.db",
        base_directory_from=Path(r"C:\scripting\processing_cellpy\raw"),
        base_directory_to=Path(r"C:\scripting\trash"),
        extension=filter_extension,
    )
    worker.connect_to_db()
    worker.filter_local(additional_filters=my_filters)
    worker.check(additional_filters=my_filters)
    run_oeleo = input("\n Continue ([y]/n)? ") or "y"
    if run_oeleo.lower() in ["y", "yes"]:
        worker.run()


main = example_with_rich_scheduler

if __name__ == "__main__":
    main()
