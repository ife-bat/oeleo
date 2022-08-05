import logging
import os
from datetime import datetime
from pathlib import Path

import dotenv

from checkers import ChecksumChecker
from models import SimpleDbHandler
from oeleo.connectors import register_password, LocalConnector, SharePointConnector
from oeleo.console import console
from oeleo.schedulers import RichScheduler, SimpleScheduler
from oeleo.utils import logger
from oeleo.workers import simple_worker, ssh_worker, Worker

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


def example_with_ssh_connection_and_rich_scheduler():
    log.setLevel(logging.CRITICAL)
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

    s = RichScheduler(
        worker,
        run_interval_time=4,
        max_run_intervals=4,
        force=True,
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
    not_after = datetime(year=2022, month=8, day=30, hour=1, minute=0, second=0)

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


def example_with_sharepoint_connector():

    def external_name_generator(con, name):
        return Path(name.name)

    log.setLevel(logging.DEBUG)
    log.debug(f"Starting oeleo!")
    console.print(f"Starting oeleo!")
    dotenv.load_dotenv()
    db_name = os.environ["OELEO_DB_NAME"]
    username = os.environ["OELEO_SHAREPOINT_USERNAME"]
    sitename = os.environ["OELEO_SHAREPOINT_SITENAME"]
    base_directory_from = Path(os.environ["OELEO_BASE_DIR_FROM"])
    base_directory_to = os.environ["OELEO_SHAREPOINT_DOC_LIBRARY"]
    extension = os.environ["OELEO_FILTER_EXTENSION"]

    local_connector = LocalConnector(directory=base_directory_from)
    external_connector = SharePointConnector(
        username=username,
        host=sitename,
        directory=base_directory_to,
    )
    print("created sharepoint connector")
    bookkeeper = SimpleDbHandler(db_name)
    checker = ChecksumChecker()

    log.debug(
        f"[bold]from:[/] [bold green]{local_connector.directory}[/]",
        extra={"markup": True},
    )
    log.debug(
        f"[bold]to  :[/] [bold blue]{external_connector.url}:{external_connector.directory}[/]",
        extra={"markup": True},
    )

    worker = Worker(
        checker=checker,
        local_connector=local_connector,
        external_connector=external_connector,
        bookkeeper=bookkeeper,
        extension=extension,
        external_name_generator=external_name_generator,
    )

    # TODO: Find out why nothing is copied over (probably to do with either that the db is pre-populated from
    #  other runs or that the check method has an error)
    log.debug(
        f"[bold]to  :[/] [bold blue] created worker [/]",
        extra={"markup": True},
    )
    worker.connect_to_db()
    log.debug(
        f"[bold]to  :[/] [bold blue] connected to db [/]",
        extra={"markup": True},
    )
    worker.check(update_db=True)
    log.debug(
        f"[bold]to  :[/] [bold blue] checked [/]",
        extra={"markup": True},
    )
    worker.filter_local()
    worker.run()


main = example_with_sharepoint_connector

if __name__ == "__main__":
    main()
    # example_with_ssh_connection_and_rich_scheduler()
