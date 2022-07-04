import logging
import os
from datetime import datetime
from pathlib import Path

import dotenv
import peewee
from rich.logging import RichHandler

from checkers import ConnectedChecker, SimpleChecker
from connectors import SSHConnector, register_password
from filters import filter_content
from models import SimpleDbHandler
from movers import simple_mover, connected_mover
from workers import Worker

FORMAT = "%(message)s"

logging.basicConfig(
    format=FORMAT,
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True, tracebacks_suppress=[peewee])],
)

log = logging.getLogger("oeleo")


def setup_worker(
    dry_run=False, db_name=None, base_directory_from=None, base_directory_to=None
):
    db_name = db_name or os.environ["DB_NAME"]
    base_directory_from = base_directory_from or Path(os.environ["BASE_DIR_FROM"])
    base_directory_to = base_directory_to or Path(os.environ["BASE_DIR_TO"])

    bookkeeper = SimpleDbHandler(db_name)
    checker = SimpleChecker()
    # mover = SimpleMover()

    log.info(
        f"[bold]from:[/] [bold green]{base_directory_from}[/]", extra={"markup": True}
    )
    log.info(
        f"[bold]to  :[/] [bold blue]{base_directory_to}[/]", extra={"markup": True}
    )

    worker = Worker(
        filter_method=filter_content,
        checker=checker,
        mover_method=simple_mover,
        from_dir=base_directory_from,
        to_dir=base_directory_to,
        bookkeeper=bookkeeper,
        dry_run=dry_run,
    )
    return worker


def setup_ssh_worker(
    connector: SSHConnector,
    dry_run: bool = False,
    db_name: str | None = None,
    base_directory_from: Path | None = None,
):
    db_name = db_name or os.environ["DB_NAME"]
    base_directory_from = base_directory_from or Path(os.environ["BASE_DIR_FROM"])
    base_directory_to = connector.directory

    # connector.connect()

    bookkeeper = SimpleDbHandler(db_name)
    checker = ConnectedChecker()
    # mover = SimpleMover()

    log.info(
        f"[bold]from:[/] [bold green]{base_directory_from}[/]", extra={"markup": True}
    )
    log.info(
        f"[bold]to  :[/] [bold blue]{connector.host}:{base_directory_to}[/]",
        extra={"markup": True},
    )

    worker = Worker(
        filter_method=filter_content,
        checker=checker,
        mover_method=connected_mover,
        from_dir=base_directory_from,
        to_dir=base_directory_to,
        external_connector=connector,
        bookkeeper=bookkeeper,
        dry_run=dry_run,
    )
    return worker


def main():
    log.setLevel(logging.INFO)
    log.info(f"Starting oeleo!")
    dotenv.load_dotenv()
    filter_extension = os.environ["FILTER_EXTENSION"]
    worker = setup_worker()
    worker.connect_to_db()
    worker.filter_local(filter_extension)
    worker.check(filter_extension)
    worker.run()


def example_check_with_ssh_connection():

    log.setLevel(logging.INFO)
    log.info(f"Starting oeleo!")
    dotenv.load_dotenv()

    external_dir = "/home/jepe@ad.ife.no/Temp"
    filter_extension = "res"

    register_password(os.environ["OELEO_PASSWORD"])
    connector = SSHConnector(directory=external_dir)
    connector.connect()

    worker = setup_ssh_worker(
        db_name="test_ssh_to_odin.db",
        base_directory_from=Path(r"C:\scripting\processing_cellpy\raw"),
        connector=connector,
    )
    worker.connect_to_db()
    try:
        worker.check(filter_extension, update_db=True)
        worker.filter_local(filter_extension)
        worker.run()
    finally:
        connector.close()


def example_check_first_then_run():

    not_before = datetime(year=2021, month=3, day=1, hour=1, minute=0, second=0)
    not_after = datetime(year=2022, month=7, day=1, hour=1, minute=0, second=0)
    print("Starting...")

    my_filters = [
        ("not_before", not_before),
        ("not_after", not_after),
    ]

    log.setLevel(logging.INFO)
    log.info(f"Starting oeleo!")
    dotenv.load_dotenv()
    filter_extension = "res"
    worker = setup_worker(
        db_name="another.db",
        base_directory_from=Path(r"C:\scripting\processing_cellpy\raw"),
        base_directory_to=Path(r"C:\scripting\trash"),
    )
    worker.connect_to_db()
    worker.filter_local(filter_extension)
    worker.check(filter_extension, additional_filters=my_filters)
    run_oeleo = input("\n Continue ([y]/n)? ") or "y"
    if run_oeleo.lower() in ["y", "yes"]:
        worker.run()


if __name__ == "__main__":
    print(f"HEI from {__name__} in {__file__}")
    example_check_with_ssh_connection()
    # example_check_first_then_run()
    # main()
