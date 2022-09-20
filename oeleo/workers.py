import logging
import os
from asyncio import Protocol
from dataclasses import dataclass, field
from math import ceil
from pathlib import Path
from typing import Any, Generator, Union, Callable, Iterable, List

from rich.panel import Panel
from rich.text import Text

from oeleo.checkers import ChecksumChecker
from oeleo.connectors import (
    Connector,
    LocalConnector,
    SSHConnector,
    SharePointConnector,
)
from oeleo.console import console
from oeleo.layouts import N_COLS_NOT_BODY, N_ROWS_NOT_BODY
from oeleo.models import DbHandler, MockDbHandler, SimpleDbHandler
from oeleo.reporters import Reporter, ReporterBase

log = logging.getLogger("oeleo")


class WorkerBase(Protocol):
    checker: Any
    bookkeeper: DbHandler
    local_connector: Connector = None
    external_connector: Connector = None
    reporter: ReporterBase = None

    def connect_to_db(self):
        ...

    def add_local(self, **kwargs):
        ...

    def filter_local(self, **kwargs):
        ...

    def filter_external(self, **kwargs):
        ...

    def check(self, update_db=False, force=False, **kwargs):
        ...

    def run(self):
        ...

    def close(self):
        ...


class MockWorker(WorkerBase):
    def connect_to_db(self):
        console.log("Connecting to database")

    def add_local(self, **kwargs):
        console.log("Adding local files directly for transfer")

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

    Additional optinal arguments:
        dry_run: Bool
        extension: str (with the .)
        reporter: Reporter
        external_name_generator: Callable that accepts the class instance and a string
    """

    checker: Any
    bookkeeper: DbHandler
    dry_run: bool = False
    local_connector: Connector = None
    external_connector: Connector = None
    extension: str = None
    reporter: ReporterBase = Reporter()
    external_name_generator: Callable[[Any, Path], Path] = field(default=None)

    file_names: Iterable[Path] = field(init=False, default_factory=list)

    _external_name: Union[Path, str] = field(init=False, default="")
    _status: dict = field(init=False, default_factory=dict)

    def __post_init__(self):
        if self.dry_run:
            log.debug("DRY RUN")
            self.bookkeeper = MockDbHandler()
        self.external_connector.connect()

    def connect_to_db(self):
        self.status = ("state", "connect-to-db")
        self.bookkeeper.initialize_db()
        log.debug(f"Connecting to db -> '{self.bookkeeper.db_name}' DONE")

    def add_local(self, local_files: Iterable) -> List:
        """Add the files that should be processed."""
        if not isinstance(local_files, list):
            logging.warning(
                "Please provide a list for local files when using add_local. "
                "If it is a generator, you will have to re-run "
                "add_local before each call to check or run."
            )
            local_files = list(local_files)
        self.status = ("state", "filter-local")
        self.status = ("filtered_once", False)
        self.file_names = local_files
        return local_files

    def filter_local(self, **kwargs):
        """Selects the files that should be processed through filtering."""
        self.status = ("state", "filter-local")
        self.status = ("filtered_once", True)
        local_files = self.local_connector.base_filter_sub_method(
            self.extension, **kwargs
        )
        self.file_names = local_files
        return local_files

    def filter_external(self, **kwargs):
        """Filter for external files that correspond to local ones."""
        self.status = ("state", "filter-external")
        external_files = self.external_connector.base_filter_sub_method(
            self.extension, **kwargs
        )
        return external_files

    def check(self, update_db=False, force=True, **kwargs):
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
        local_files = self.file_names or self.filter_local(**kwargs)

        # cannot be a generator since we need to do a `if in` lookup:
        external_files = list(self.filter_external(**kwargs))

        number_of_local_files = 0
        number_of_external_duplicates = 0
        number_of_duplicates_out_of_sync = 0

        for f in local_files:
            number_of_local_files += 1
            self.make_external_name(f)
            external_name = self.external_name
            local_vals = self.checker.check(
                f,
                connector=self.local_connector,
            )
            if external_name in external_files:
                self.reporter.report(
                    f"{f.name} -> {self.external_name}"
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
                            f"    (E) {k}: {external_vals[k]}"
                        )
                    else:
                        self.reporter.report(
                            f"    (E) {k}: {external_vals[k]}"
                        )
                log.debug(f"In sync: {same}")

            else:
                number_of_duplicates_out_of_sync += 1
                self.reporter.report(
                    f"{f.name} -> {self.external_name}"
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

        self.reporter.report("\nREPORT (CHECK):")
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

        log.debug("****** RUN:")
        self.status = ("state", "run")
        local_files_found = False
        for f in self.file_names:
            local_files_found = True
            self._process_file(f)
        if not local_files_found:
            self.reporter.report(
                "No files to handle. Did you forget to run `worker.filter_local()`?"
            )

    def _process_file(self, f):
        del self.status
        self.make_external_name(f)
        self.bookkeeper.register(f)
        checks = self.checker.check(f)
        if not self.bookkeeper.is_changed(**checks):
            log.debug(f"{f} not changed")
            self.reporter.report(
                f"{f.name} == {self.external_name}"
            )

        else:
            self.reporter.report(
                f"{f.name} -> {self.external_name}"
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
                    f"{f.name} -> "
                    f"{self.external_name} failed copy!",
                    replace_line=True,
                )

    def _default_external_name_generator(self, f):
        return self.external_connector.directory / f.name

    def make_external_name(self, f):
        if self.external_name_generator is not None:
            name = self.external_name_generator(self.external_connector, f)
        else:
            name = self._default_external_name_generator(f)
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
        for k in self._status:
            if k != "state":  # protected member
                self._status[k] = None

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
    base_directory_from = base_directory_from or os.environ["OELEO_BASE_DIR_FROM"]
    base_directory_to = base_directory_to or os.environ["OELEO_BASE_DIR_TO"]
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
    base_directory_from: Union[str, None] = None,
    base_directory_to: Union[str, None] = None,
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
    base_directory_from = base_directory_from or os.environ["OELEO_BASE_DIR_FROM"]
    base_directory_to = base_directory_to or os.environ["OELEO_BASE_DIR_TO"]
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


def sharepoint_worker(
    base_directory_from: Union[Path, None] = None,
    url: Union[Path, None] = None,
    sitename: Union[str, None] = None,
    doc_library_to: Union[str, None] = None,
    db_name: Union[str, None] = None,
    extension: str = None,
    dry_run: bool = False,
):
    """Create a Worker with SharePointConnector.

    Args:
        base_directory_from: directory to copy from.
        url: sharepoint url (e.g. https://yourcompany.sharepoint.com).
        sitename: name of the specific SharePoint site.
        doc_library_to: folder within the SharePoint site to copy to.
        db_name: name of the database.
        extension: file extension to filter on (for example '.csv').
        dry_run: set to True if you would like to run without updating or moving anything.

    Returns:
        worker with SharePoint attached to it.
    """

    def external_name_generator(con, name):
        return Path(name.name)

    log.setLevel(logging.DEBUG)
    log.debug(f"Starting oeleo!")
    console.print(f"Starting oeleo!")

    db_name = db_name or os.environ["OELEO_DB_NAME"]

    base_directory_from = base_directory_from or os.environ["OELEO_BASE_DIR_FROM"]
    doc_library_to = doc_library_to or os.environ["OELEO_SHAREPOINT_DOC_LIBRARY"]
    url = url or os.getenv("OELEO_SHAREPOINT_URL")
    sitename = sitename or os.getenv("OELEO_SHAREPOINT_SITENAME")

    extension = extension or os.environ["OELEO_FILTER_EXTENSION"]
    username = os.getenv("OELEO_SHAREPOINT_USERNAME", None)

    local_connector = LocalConnector(directory=base_directory_from)

    external_connector = SharePointConnector(
        username=username,
        host=sitename,
        url=url,
        directory=doc_library_to,
    )

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
        dry_run=dry_run,
    )
    return worker
