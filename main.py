import logging
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Generator

import dotenv
import peewee
from rich.logging import RichHandler

from checkers import SimpleChecker
from filters import filter_content
from models import DbHandler, SimpleDbHandler
from movers import simple_mover

FORMAT = "%(message)s"

logging.basicConfig(
    format=FORMAT,
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True, tracebacks_suppress=[peewee])],
)

log = logging.getLogger(__name__)


@dataclass
class Worker:
    filter_method: Any
    checker: Any
    mover_method: Any  # MAKE THIS A CLASS INSTEAD
    from_dir: Path
    to_dir: Path
    bookkeeper: DbHandler
    check_to: bool = False  # NOT IMPLEMENTED YET (checking to directory) (needs a better checker)
    dry_run: bool = False  # NOT IMPLEMENTED YET (perform without copying/moving and updating db)

    file_names: Generator[Path, None, None] = field(init=False)

    _external_name: str = field(init=False, default="")
    _status: dict = field(init=False, default_factory=dict)

    def connect_to_db(self):
        self.bookkeeper.initialize_db()
        log.info(f"Connecting to db -> '{self.bookkeeper.db_name}' DONE")

    def filter(self, *args, **kwargs):
        """ Selects the files that should be processed """
        self.file_names = self.filter_method(
            self.from_dir,
            *args,
            **kwargs,
        )
        log.info("Filtering -> DONE")

    def check(self):
        """Check for differences between the two directories."""
        pass

    def run(self):
        """Copy the files that needs to be copied and update the db."""
        log.info("Running...")
        for f in self.file_names:
            del self.status
            self.make_external_name(f)
            log.debug(f"{f.name} -> {self.external_name}")
            self.bookkeeper.register(f)
            checks = self.checker.check(f)

            if self.bookkeeper.is_changed(**checks):
                self.status = ("changed", True)
                if self.mover_method(f, self.external_name):
                    self.status = ("moved", True)
                    self.bookkeeper.update_record(self.external_name, **checks)

            self.report()

    def report(self):
        status = self.status
        f1 = status["name"]
        f2 = status["external_name"]

        if status.get("changed", False):
            txt = f"[bold blue]{f1}"
            if status.get("moved", False):
                txt += f" -> {f2}[/]"
            else:
                txt += f"[/] -> [bold red blink]{f2}[/]"
        else:
            txt = f"[bold green]{f1} == {f2}[/]"

        log.info(txt, extra={"markup": True})

    def make_external_name(self, f):
        name = self.to_dir / f.name
        self.external_name = name
        self.status = ("name", f.name)
        self.status = ("external_name", str(self._external_name))

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, pair: tuple):
        key, value = pair
        self._status[key] = value

    @status.deleter
    def status(self):
        self._status = {}

    @property
    def external_name(self):
        return self._external_name

    @external_name.setter
    def external_name(self, name):
        self._external_name = name


def main():

    log.setLevel(logging.INFO)
    log.info(f"Starting oeleo!")

    dotenv.load_dotenv()

    bookkeeper = SimpleDbHandler(os.environ["DB_NAME"])
    checker = SimpleChecker()
    # mover = SimpleMover()

    base_directory_from = Path(os.environ["BASE_DIR_FROM"])
    base_directory_to = Path(os.environ["BASE_DIR_TO"])
    filter_extension = os.environ["FILTER_EXTENSION"]

    log.info(f"[bold]from:[/] [bold green]{base_directory_from}[/]", extra={"markup": True})
    log.info(f"[bold]to  :[/] [bold blue]{base_directory_to}[/]", extra={"markup": True})

    worker = Worker(
        filter_method=filter_content,
        checker=checker,
        mover_method=simple_mover,
        from_dir=base_directory_from,
        to_dir=base_directory_to,
        bookkeeper=bookkeeper,
    )

    worker.connect_to_db()
    worker.filter(filter_extension)
    worker.check()
    worker.run()


if __name__ == "__main__":
    main()
