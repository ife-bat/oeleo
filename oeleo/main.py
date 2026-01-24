import asyncio
import logging
import os
from datetime import datetime
from pathlib import Path

import dotenv

from oeleo.connectors import register_password
from oeleo.console import console
from oeleo.schedulers import SimpleScheduler
from oeleo.reporters import LogAndTrayReporter
from oeleo.utils import start_logger
from oeleo.workers import (
    simple_worker,
    simple_async_worker,
    ssh_worker,
    sharepoint_worker,
)


DEFAULT_ENVIRONMENT = """
OELEO_BASE_DIR_FROM=C:\scripting\oeleo\check\from
OELEO_BASE_DIR_TO=/somewher_in_myserver
OELEO_FILTER_EXTENSION=.xyz
OELEO_DB_NAME=test_app.db
OELEO_LOG_DIR=log
OELEO_EXTERNAL_HOST=A-IP-NUMBER
OELEO_USERNAME=coolkid
OELEO_PASSWORD=
OELEO_KEY_FILENAME=C:\\Users\\coolkid\\.ssh\\id_myserver

# oeleo app config:
OA_SINGLE_RUN=false
OA_MAX_RUN_INTERVALS=200
OA_HOURS_SLEEP=0.01
OA_FROM_YEAR=2023
OA_FROM_MONTH=1
OA_FROM_DAY=1
OA_STARTS_WITH=2023;2024
OA_ADD_CHECK=true
OA_INCLUDE_SUBDIRS=true
OA_EXTERNAL_SUBDIRS=true
"""

def load_default_environment():
    """Load the default environment variables."""
    for line in DEFAULT_ENVIRONMENT.split("\n"):
        if line.startswith("#"):
            continue
        if line.strip():
            key, value = line.strip().split("=")
            os.environ[key] = value

def simple_multi_dir():
    dotenv.load_dotenv()
    start_logger(screen_level=logging.CRITICAL, only_oeleo=True)
    filter_extension = [".pdf", ".docx", ".doc", "pptx", "ppt", "xyz"]

    register_password(os.environ["OELEO_PASSWORD"])
    db_name = Path(r"..\test_databases\multi_to_single6.db")
    assert db_name.parent.is_dir()
    worker = simple_worker(
        db_name=db_name,
        extension=filter_extension,
        include_subdirs=True,
        external_subdirs=False,
    )

    worker.connect_to_db()

    worker.check(update_db=True)
    worker.filter_local()
    worker.run()


def example_bare_minimum():
    start_logger(screen_level=logging.DEBUG, only_oeleo=True)
    dotenv.load_dotenv()
    logging.debug("Starting oeleo!")
    console.print("Starting oeleo!")

    worker = simple_worker()
    worker.connect_to_db()

    # worker.check(update_db=True)
    worker.filter_local()
    worker.run()


def example_with_simple_scheduler():
    dotenv.load_dotenv()
    start_logger(screen_level=logging.DEBUG, only_oeleo=True)
    logging.debug("Starting oeleo!")
    worker = simple_worker()

    s = SimpleScheduler(
        worker,
        run_interval_time=2,
        max_run_intervals=2,
    )
    s.start()


def example_with_ssh_connection_and_scheduler():
    dotenv.load_dotenv()
    logging.setLevel(logging.CRITICAL)

    external_dir = "/home/jepe@ad.ife.no/Temp"
    filter_extension = ".res"

    register_password(os.environ["OELEO_PASSWORD"])

    worker = ssh_worker(
        db_name=r"C:\scripting\oeleo\test_databases\test_ssh_to_odin.db",
        base_directory_from=Path(r"C:\scripting\processing_cellpy\raw"),
        base_directory_to=external_dir,
        extension=filter_extension,
    )

    s = SimpleScheduler(
        worker,
        run_interval_time=4,
        max_run_intervals=4,
        force=True,
    )
    s.start()


def example_check_with_ssh_connection():
    print(" example_check_with_ssh_connection ".center(80, "-"))
    dotenv.load_dotenv()
    start_logger(screen_level=logging.DEBUG, only_oeleo=True)
    logging.info("Starting oeleo!")

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
    dotenv.load_dotenv()
    start_logger(screen_level=logging.DEBUG, only_oeleo=True)
    logging.info("Starting oeleo!")

    not_before = datetime(year=2021, month=3, day=1, hour=1, minute=0, second=0)
    not_after = datetime(year=2022, month=8, day=30, hour=1, minute=0, second=0)

    my_filters = [
        ("not_before", not_before),
        ("not_after", not_after),
    ]

    filter_extension = ".res"
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


def example_with_sharepoint_connector():
    print(" example_check_first_then_run ".center(80, "-"))
    dotenv.load_dotenv()
    start_logger()
    start_logger(screen_level=logging.DEBUG, only_oeleo=True)
    logging.info("Starting oeleo!")

    worker = sharepoint_worker()
    worker.connect_to_db()
    worker.check(update_db=True)
    worker.filter_local()
    worker.run()


def example_with_ssh_and_env():
    print(" Single run SSH with env parameters ".center(80, "-"))
    dotenv.load_dotenv()
    start_logger(screen_level=logging.DEBUG, only_oeleo=True)
    logging.info("Starting oeleo!")
    worker = ssh_worker()
    worker.connect_to_db()
    worker.check(update_db=True)
    worker.filter_local()
    worker.run()


def example_with_tray_reporter():
    print(" Scheduler with tray reporter ".center(80, "-"))
    load_default_environment()
    start_logger(screen_level=logging.DEBUG, only_oeleo=True)
    logging.info("Starting oeleo!")

    hours_sleep = float(os.environ.get("OA_HOURS_SLEEP", 0.5))
    max_run_intervals = int(os.environ.get("OA_MAX_RUN_INTERVALS", 200))

    reporter = LogAndTrayReporter()
    try:
        worker = ssh_worker(reporter=reporter)
    except KeyError as exc:
        missing = str(exc).strip("'")
        logging.error(f"Missing env var: {missing}")
        logging.error("Load your .env or set the required OELEO_* variables.")
        reporter.notify(f"Missing env var: {missing}", title="oeleo")
        return

    s = SimpleScheduler(
        worker,
        run_interval_time=3600 * hours_sleep,
        max_run_intervals=max_run_intervals,
    )
    s.start()


def example_async_check():
    """Run an async check using the async worker wrapper."""
    dotenv.load_dotenv()
    start_logger(screen_level=logging.DEBUG, only_oeleo=True)
    logging.info("Starting oeleo async check!")

    worker = simple_async_worker()
    worker.connect_to_db()
    asyncio.run(worker.async_check(update_db=True))




main = example_with_tray_reporter

if __name__ == "__main__":
    if os.environ.get("OELEO_ASYNC_CHECK", "").lower() in {"1", "true", "yes"}:
        example_async_check()
    else:
        main()
    # example_with_ssh_connection_and_rich_scheduler()
    # simple_multi_dir()
