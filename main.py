import logging
import os
from pathlib import Path

import dotenv
import peewee
from rich.logging import RichHandler

from checkers import SimpleChecker
from filters import filter_content
from models import SimpleDbHandler
from movers import simple_mover
from workers import Worker

FORMAT = "%(message)s"

logging.basicConfig(
    format=FORMAT,
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True, tracebacks_suppress=[peewee])],
)

log = logging.getLogger("oeleo")


def setup_worker(dry_run=False):
    bookkeeper = SimpleDbHandler(os.environ["DB_NAME"])
    checker = SimpleChecker()
    # mover = SimpleMover()

    base_directory_from = Path(os.environ["BASE_DIR_FROM"])
    base_directory_to = Path(os.environ["BASE_DIR_TO"])

    log.info(f"[bold]from:[/] [bold green]{base_directory_from}[/]", extra={"markup": True})
    log.info(f"[bold]to  :[/] [bold blue]{base_directory_to}[/]", extra={"markup": True})

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


def main():
    log.setLevel(logging.INFO)
    log.info(f"Starting oeleo!")
    dotenv.load_dotenv()
    filter_extension = os.environ["FILTER_EXTENSION"]
    worker = setup_worker()
    worker.connect_to_db()
    worker.filter_local(filter_extension)
    # worker.check(filter_extension)
    worker.run()


if __name__ == "__main__":
    print("HEI")
    main()
