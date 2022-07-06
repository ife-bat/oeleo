import logging
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Generator, Union

from oeleo.checkers import ConnectedChecker
from oeleo.connectors import Connector, SSHConnector, LocalConnector
from oeleo.models import DbHandler, MockDbHandler, SimpleDbHandler
from oeleo.movers import mock_mover, connected_mover

log = logging.getLogger("oeleo")


@dataclass
class Worker:
    """The worker class is responsible for orchestrating the transfers.

    A typical transfer consists of the following steps:
    1. Asking the bookkeeper to connect to its database.
    >>> worker.connect_to_db()
    2. Collect (and filter) the files in the local directory that are candidates for copying to
       the external directory (server).
    >>> worker.filter_local("*.res", additional_filters=my_filters)
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
    extension: str = None,
    file_names: Generator[Path, None, None] = field(init=False, default=None)
    _external_name: str = field(init=False, default="")
    _status: dict = field(init=False, default_factory=dict)

    def __post_init__(self):
        if self.dry_run:
            log.info("[bold red blink]DRY RUN[/]", extra={"markup": True})
            self.bookkeeper = MockDbHandler()
        self.external_connector.connect()

    def connect_to_db(self):
        self.bookkeeper.initialize_db()
        log.info(f"Connecting to db -> '{self.bookkeeper.db_name}' DONE")

    def filter_local(self, **kwargs):
        """Selects the files that should be processed.txt

        TODO: This method should be updated so that it uses the value from the
           environment as default.
        """
        local_files = self.local_connector.base_filter_sub_method(self.extension, **kwargs)
        self.file_names = local_files
        return local_files

    def filter_external(self, **kwargs):
        external_files = self.external_connector.base_filter_sub_method(self.extension, **kwargs)
        return external_files

    def check(self, update_db=False, **kwargs):
        """Check for differences between the two directories.

        Arguments:
            update_db: set to True if you want the check to also update the db.
        Additional keyword arguments:
            sent to the filter functions.
        """
        # PLEASE, REFACTOR ME!
        print(f"Comparing {self.local_connector.directory} <=> {self.external_connector.directory}")
        local_files = self.filter_local(**kwargs)
        external_files = self.filter_external(**kwargs)

        number_of_local_files = 0
        number_of_external_duplicates = 0
        number_of_duplicates_out_of_sync = 0

        for f in local_files:
            print(f"Iterating: {f}")
            number_of_local_files += 1

            self.make_external_name(f)
            external_name = self.external_name
            log.debug(f"{f.name} -> {self.external_name}")
            print(f" (*) {f.name}", end=" ")
            if external_name in external_files:
                code = 1
                print(f"[FOUND EXTERNAL]")
                number_of_external_duplicates += 1
                local_vals = self.checker.check(
                    f,
                    connector=self.local_connector,
                )
                external_vals = self.checker.check(
                    external_name,
                    connector=self.external_connector,
                )

                same = True
                for k in local_vals:
                    print(f"     (L) {k}: {local_vals[k]}")
                    print(f"     (E) {k}: {external_vals[k]}")
                    if local_vals[k] != external_vals[k]:
                        same = False
                        number_of_duplicates_out_of_sync += 1
                print(f"     In sync: {same}")
            else:
                code = 0
                print("[ONLY LOCAL]")
            if update_db:
                print("     ! UPDATING DB")
                self.bookkeeper.register(f)
                if self.bookkeeper.code < 2:
                    self.bookkeeper.code = code
                if self.bookkeeper.code == 1:
                    self.bookkeeper.update_record(external_name, **local_vals)
            else:
                print()
        print()
        print(f" Total number of local files:    {number_of_local_files}")
        print(f" Files with external duplicates: {number_of_external_duplicates}")
        print(f" Files out of sync:              {number_of_duplicates_out_of_sync}")

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
                if self.external_connector.move_func(
                    f, self.external_name,
                ):
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
                txt += f"[/] -> [bold red blink]{f2} FAILED![/]"
        else:
            txt = f"[bold green]{f1} == {f2}[/]"

        log.info(txt, extra={"markup": True})

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
    checker = ConnectedChecker()
    local_connector = LocalConnector(directory=base_directory_from)
    external_connector = LocalConnector(directory=base_directory_to)

    log.info(
        f"[bold]from:[/] [bold green]{base_directory_from}[/]", extra={"markup": True}
    )
    log.info(
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
    is_posix: bool = True
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
    external_connector = SSHConnector(directory=base_directory_to, use_password=use_password, is_posix=is_posix)

    bookkeeper = SimpleDbHandler(db_name)
    checker = ConnectedChecker()

    log.info(
        f"[bold]from:[/] [bold green]{local_connector.directory}[/]", extra={"markup": True}
    )
    log.info(
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
