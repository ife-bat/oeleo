import logging
import os
from asyncio import Protocol
from dataclasses import dataclass, field
from math import ceil
from pathlib import Path
from typing import Any, Generator, Union

from rich.panel import Panel
from rich.text import Text

from oeleo.layouts import N_ROWS_NOT_BODY, N_COLS_NOT_BODY
from oeleo.checkers import ChecksumChecker
from oeleo.connectors import Connector, LocalConnector, SSHConnector
from oeleo.console import console
from oeleo.models import DbHandler, MockDbHandler, SimpleDbHandler

log = logging.getLogger("oeleo")


class ReporterBase(Protocol):
    layout = None
    lines: list = None

    def report(self, status, events=None, same_line=False, replace_line=False):
        ...

    def clear(self):
        ...


class Reporter:
    layout = None
    lines = []

    @staticmethod
    def report(status, events=None, same_line=False, replace_line=False):
        log.debug(status)

    def clear(self):
        pass


class LayoutReporter:
    def __init__(self, layout):
        self.layout = layout
        self.lines = []
        self.max_lines = 200
        self.min_lines = 100

    def report(self, status, events=None, same_line=False, replace_line=False):
        if same_line and len(self.lines):
            self.lines[-1] = f"{self.lines[-1]}{status}"
        elif replace_line and len(self.lines):
            self.lines[-1] = f"{status}"
        else:
            self.lines.append(status)
        if events:
            log.debug(
                f"Events ({events}) given - however, events are not implemented yet."
            )

        self._trim_if_needed()
        body_panel = self._update_body_panel()
        self.layout["body"].update(body_panel)

    def clear(self):
        self.lines = []

    def _trim_if_needed(self):
        if len(self.lines) > self.max_lines:
            self.lines = self.lines[-self.min_lines :]

    def _update_body_panel(self):
        number_of_columns, number_of_rows = os.get_terminal_size()
        number_of_rows -= N_ROWS_NOT_BODY
        number_of_columns -= N_COLS_NOT_BODY

        _lines = self.lines[-number_of_rows:]
        needed_rows_due_to_wrapping = 0
        _new_lines = []
        for _line in reversed(_lines):
            needed_rows_due_to_wrapping += ceil(
                Text(_line).cell_len / number_of_columns
            )
            if needed_rows_due_to_wrapping < number_of_rows:
                _new_lines.append(_line)
            else:
                break
        _lines = reversed(_new_lines)

        s = "\n".join(_lines)

        p = Panel(s)
        return p


class WorkerBase(Protocol):
    checker: Any
    bookkeeper: DbHandler
    local_connector: Connector = None
    external_connector: Connector = None
    reporter: ReporterBase = None

    def connect_to_db(self):
        ...

    def filter_local(self, **kwargs):
        ...

    def filter_external(self, **kwargs):
        ...

    def check(self, update_db=False, force=False, **kwargs):
        ...

    def run(self):
        ...

    def run_statistics(self):
        ...

    def close(self):
        ...


class MockWorker(WorkerBase):
    def connect_to_db(self):
        console.log("Connecting to database")

    def filter_local(self, **kwargs):
        console.log("Filtering local directory")

    def filter_external(self, **kwargs):
        console.log("Filtering external directory")

    def check(self, update_db=False, force=False, **kwargs):
        console.log("Performing a comparison between local and " "external directory")
        console.log(f" - update-db:  {update_db}")
        console.log(f" - kwargs:  {kwargs}")

    def run(self):
        console.log("Running...")

    def run_statistics(self):
        console.log("Showing report after run")

    def close(self):
        console.log("Closing all connections")


@dataclass
class Worker(WorkerBase):
    """The worker class is responsible for orchestrating the transfers.

    A typical transfer consists of the following steps:
    1. Asking the bookkeeper to connect to its database.
    >>> worker.connect_to_db()
    2. Collect (and filter) the files in the local directory that are candidates for copying to
       the external directory (server).
    >>> worker.filter_local(additional_filters=my_filters)
    3. Calculate checksum for each file collected and check copy if they have changed.
    >>> worker.run()

    A worker needs to be initiated with the at least the following handlers:
        checker: Checker object
        bookkeeper: DbHandler to interact with the db
        local_connector: Connector = None
        external_connector: Connector = None
    """

    checker: Any
    bookkeeper: DbHandler
    dry_run: bool = False
    local_connector: Connector = None
    external_connector: Connector = None
    extension: str = None
    reporter: ReporterBase = Reporter()
    file_names: Generator[Path, None, None] = field(init=False, default=None)
    _external_name: Union[Path, str] = field(init=False, default="")
    _status: dict = field(init=False, default_factory=dict)

    def __post_init__(self):
        if self.dry_run:
            log.debug("[bold red blink]DRY RUN[/]", extra={"markup": True})
            self.bookkeeper = MockDbHandler()
        self.external_connector.connect()

    def connect_to_db(self):
        self.status = ("state", "filter")
        self.bookkeeper.initialize_db()
        log.debug(f"Connecting to db -> '{self.bookkeeper.db_name}' DONE")

    def filter_local(self, **kwargs):
        """Selects the files that should be processed."""

        local_files = self.local_connector.base_filter_sub_method(
            self.extension, **kwargs
        )
        self.file_names = local_files
        return local_files

    def filter_external(self, **kwargs):
        """Filter for external files that correspond to local ones."""
        self.status = ("state", "filter")
        external_files = self.external_connector.base_filter_sub_method(
            self.extension, **kwargs
        )
        return external_files

    def check(self, update_db=False, force=False, **kwargs):
        """Check for differences between the two directories.

        Arguments:
            update_db: set to True if you want the check to also update the db.
            force: set to True if you want to update db to also copy missing files (code=0) as
                long as the file is not set to a frozen state.

        Additional keyword arguments:
            sent to the filter functions.
        """

        self.status = ("state", "check")
        log.debug("****** CHECK:")
        self.reporter.report(
            f"Comparing {self.local_connector.directory} <=> {self.external_connector.directory}"
        )
        local_files = self.filter_local(**kwargs)

        # cannot be a generator since we need to do a `if in` lookup:
        external_files = list(self.filter_external(**kwargs))
        log.debug(external_files)

        number_of_local_files = 0
        number_of_external_duplicates = 0
        number_of_duplicates_out_of_sync = 0

        for f in local_files:
            # self.reporter.report(f"Iterating: {f}")
            number_of_local_files += 1
            self.make_external_name(f)
            external_name = self.external_name
            local_vals = self.checker.check(
                f,
                connector=self.local_connector,
            )
            if external_name in external_files:
                self.reporter.report(
                    f"[cyan]{f.name}[/cyan] -> [cyan]{self.external_name}[/cyan]"
                )
                code = 1
                exists = True

                log.debug(f"[FOUND EXTERNAL]")
                number_of_external_duplicates += 1

                external_vals = self.checker.check(
                    external_name,
                    connector=self.external_connector,
                )

                same = True
                for k in local_vals:
                    self.reporter.report(f"    (L) {k}: {local_vals[k]}")

                    if local_vals[k] != external_vals[k]:
                        same = False
                        number_of_duplicates_out_of_sync += 1
                        code = 0
                        self.reporter.report(
                            f"    (E) {k}: [red]{external_vals[k]}[/red]"
                        )
                    else:
                        self.reporter.report(
                            f"    (E) {k}: [green]{external_vals[k]}[/green]"
                        )
                log.debug(f"In sync: {same}")

            else:
                self.reporter.report(
                    f"[cyan]{f.name}[/cyan] -> [red]{self.external_name}[/red]"
                )
                exists = False
                code = 0
                log.debug("[ONLY LOCAL]")

            if update_db:
                log.debug("Updating db")
                self.bookkeeper.register(f)
                if self.bookkeeper.code < 2:

                    if not force and not exists:
                        code = self.bookkeeper.code

                    self.bookkeeper.update_record(
                        external_name, code=code, **local_vals
                    )

        self.reporter.report("\n[green bold]REPORT (CHECK):[/green bold]")
        self.reporter.report(
            f"-Total number of local files:    {number_of_local_files}"
        )
        self.reporter.report(
            f"-Files with external duplicates: {number_of_external_duplicates}"
        )
        self.reporter.report(
            f"-Files out of sync:              {number_of_duplicates_out_of_sync}"
        )

    def run(self):
        """Copy the files that needs to be copied and update the db."""

        self.status = ("state", "run")
        log.debug("****** RUN:")

        for f in self.file_names:
            del self.status
            self.make_external_name(f)
            self.bookkeeper.register(f)
            checks = self.checker.check(f)

            if not self.bookkeeper.is_changed(**checks):
                log.debug(f"{f} not changed")
                self.reporter.report(
                    f":smiley: [green]{f.name}[/green] == [green]{self.external_name}[/green]"
                )

            else:
                self.reporter.report(
                    f":arrow_forward: [green]{f.name}[/green] -> [blue]{self.external_name}[/blue]"
                )
                self.status = ("changed", True)
                if self.external_connector.move_func(
                    f,
                    self.external_name,
                ):
                    self.status = ("moved", True)
                    self.bookkeeper.update_record(self.external_name, **checks)
                    self.reporter.report(" :smiley:", same_line=True)
                else:
                    self.reporter.report(
                        f":warning: [green]{f.name}[/green] -> "
                        f"[red]{self.external_name}[/red] :slightly_frowning_face: failed copy!",
                        replace_line=True,
                    )

            self.run_statistics()

    def run_statistics(self):
        log.warning("deprecated")
        status = self.status
        f1 = status["name"]
        f2 = status["external_name"]

        if status.get("changed", False):
            txt = f"[bold blue]{f1}"
            if status.get("moved", False):
                txt += f" -> {f2}[/]"
            else:
                txt += f"[/] -> [bold red blink]{f2} FAILED![/]"
        else:
            txt = f"[bold green]{f1} == {f2}[/]"

        log.debug(txt, extra={"markup": True})
        return txt

    def _create_external_name(self, f):
        return self.external_connector.directory / f.name

    def make_external_name(self, f):
        name = self._create_external_name(f)
        self.external_name = name
        self.status = ("name", f.name)
        self.status = ("external_name", str(self.external_name))

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

    def close(self):
        self.external_connector.close()


def simple_worker(
    base_directory_from=None,
    base_directory_to=None,
    db_name=None,
    dry_run=False,
    extension=None,
):
    """Create a Worker for copying files locally.

    Args:
        base_directory_from: directory to copy from.
        base_directory_to: directory to copy to.
        db_name: name of the database.
        dry_run: set to True if you would like to run without updating or moving anything.
        extension: file extension to filter on (for example '.csv').

    Returns:
        simple worker that can copy files between two local folder.
    """
    db_name = db_name or os.environ["OELEO_DB_NAME"]
    base_directory_from = base_directory_from or Path(os.environ["OELEO_BASE_DIR_FROM"])
    base_directory_to = base_directory_to or Path(os.environ["OELEO_BASE_DIR_TO"])
    extension = extension or os.environ["OELEO_FILTER_EXTENSION"]
    bookkeeper = SimpleDbHandler(db_name)
    checker = ChecksumChecker()
    local_connector = LocalConnector(directory=base_directory_from)
    external_connector = LocalConnector(directory=base_directory_to)

    log.debug(
        f"[bold]from:[/] [bold green]{base_directory_from}[/]", extra={"markup": True}
    )
    log.debug(
        f"[bold]to  :[/] [bold blue]{base_directory_to}[/]", extra={"markup": True}
    )

    worker = Worker(
        checker=checker,
        local_connector=local_connector,
        external_connector=external_connector,
        bookkeeper=bookkeeper,
        extension=extension,
        dry_run=dry_run,
    )
    return worker


def ssh_worker(
    base_directory_from: Union[Path, None] = None,
    base_directory_to: Union[Path, str, None] = None,
    db_name: Union[str, None] = None,
    extension: str = None,
    use_password: bool = False,
    dry_run: bool = False,
    is_posix: bool = True,
):
    """Create a Worker with SSHConnector.

    Args:
        base_directory_from: directory to copy from.
        base_directory_to: directory to copy to.
        db_name: name of the database.
        dry_run: set to True if you would like to run without updating or moving anything.
        extension: file extension to filter on (for example '.csv').
        use_password: set to True if you want to connect using a password instead of key-pair.
        is_posix: make external path (base_directory_to) a PurePosixPath.

    Returns:
        worker with SSHConnector attached to it.
    """

    db_name = db_name or os.environ["OELEO_DB_NAME"]
    base_directory_from = base_directory_from or Path(os.environ["OELEO_BASE_DIR_FROM"])
    base_directory_to = base_directory_to or Path(os.environ["OELEO_BASE_DIR_TO"])
    extension = extension or os.environ["OELEO_FILTER_EXTENSION"]

    local_connector = LocalConnector(directory=base_directory_from)
    external_connector = SSHConnector(
        directory=base_directory_to, use_password=use_password, is_posix=is_posix
    )

    bookkeeper = SimpleDbHandler(db_name)
    checker = ChecksumChecker()

    log.debug(
        f"[bold]from:[/] [bold green]{local_connector.directory}[/]",
        extra={"markup": True},
    )
    log.debug(
        f"[bold]to  :[/] [bold blue]{external_connector.host}:{external_connector.directory}[/]",
        extra={"markup": True},
    )

    worker = Worker(
        checker=checker,
        local_connector=local_connector,
        external_connector=external_connector,
        bookkeeper=bookkeeper,
        extension=extension,
        dry_run=dry_run,
    )
    return worker
