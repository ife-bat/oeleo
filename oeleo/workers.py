from collections import deque
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
import multiprocessing
from multiprocessing import Process, Queue
import os
import sys
from asyncio import Protocol
from dataclasses import dataclass, field
from math import ceil
from pathlib import Path
from typing import Any, Generator, Union, Callable, Iterable, List, TypeVar

from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn

from oeleo.checkers import ChecksumChecker
from oeleo.connectors import (
    Connector,
    LocalConnector,
    SSHConnector,
    SharePointConnector,
)
from oeleo.console import console
from oeleo.models import DbHandler, MockDbHandler, SimpleDbHandler
from oeleo.reporters import Reporter, ReporterBase

T = TypeVar("T")

log = logging.getLogger("oeleo")


def chunkify(file_list: Iterable[T], n: int = 10) -> Iterable[List[T]]:
    """Split a file-list into chunks of size n"""
    file_list = iter(file_list)
    buffer = deque()
    while True:
        try:
            buffer.append(next(file_list))
        except StopIteration:
            break

        if len(buffer) == n:
            yield list(buffer)
            buffer.clear()
    if buffer:
        yield list(buffer)


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

    def die_if_necessary(self):
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

    def die_if_necessary(self):
        console.log("Dying if necessary")


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
        reconnect: Bool (reconnect to the external server if connection is lost)
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
    reconnect: bool = True
    file_names: Iterable[Path] = field(init=False, default_factory=list)
    subdirs: bool = False
    external_subdirs: bool = False
    _external_name: Union[Path, str] = field(init=False, default="")
    _status: dict = field(init=False, default_factory=dict)

    def __post_init__(self):
        if self.dry_run:
            log.debug("DRY RUN")
            self.bookkeeper = MockDbHandler()
        self.external_connector.connect()
        self.reporter.notify("oeleo started", title="info")
        self.number_of_local_files = 0
        self.number_of_external_duplicates = 0
        self.number_of_duplicates_out_of_sync = 0

    def _reset_check_counter(self):
        self.number_of_local_files = 0
        self.number_of_external_duplicates = 0
        self.number_of_duplicates_out_of_sync = 0

    def connect_to_db(self):
        self.status = ("state", "connect-to-db")
        self.bookkeeper.initialize_db()
        log.debug(f"Connecting to db -> '{self.bookkeeper.db_name}' DONE")

    def add_local(self, local_files: Iterable) -> List:
        """Add the files that should be processed."""
        if not isinstance(local_files, list):
            log.warning(
                "Please provide a list for local files when using add_local. "
                "If it is a generator, you will have to re-run "
                "add_local before each call to check or run."
            )
            local_files = list(local_files)
        self.status = ("state", "filter-local")
        self.status = ("filtered_once", False)
        self.file_names = local_files
        log.debug(f"Adding {len(local_files)} files to the worker")
        return local_files

    def filter_local(self, **kwargs):
        """Selects the files that should be processed through filtering."""
        self.status = ("state", "filter-local")
        self.status = ("filtered_once", True)
        local_files = self.local_connector.base_filter_sub_method(
            self.extension, **kwargs
        )

        self.file_names = local_files
        log.debug("Filtering files to the worker")
        log.debug(f"Files: {local_files}")

        return local_files

    def filter_external(self, **kwargs):
        """Filter for external files that correspond to local ones."""
        self.status = ("state", "filter-external")
        external_files = self.external_connector.base_filter_sub_method(
            self.extension, **kwargs
        )
        log.debug("Filtering external files to the worker")
        return external_files

    def _check_local(self, f: Path, sleep_time=1, max_check_counter=300):
        check_counter = 0
        while True:
            try:
                local_vals = self.checker.check(
                    f,
                    connector=self.local_connector,
                )
                break
            except Exception as e:
                log.error(f"Error when checking {f}: {e}")
                time.sleep(sleep_time)
                check_counter += 1
                if check_counter > max_check_counter:
                    raise e
        return local_vals

    def check(self, update_db=False, force=True, **kwargs):
        """Check for differences between the two directories.

        Arguments:
            update_db: set to True if you want the check to also update the db.
            force: set to True if you want to update db to also copy missing files (code=0) as
                long as the file is not set to a frozen state.

        Additional keyword arguments:
            sent to the filter functions.
        """
        log.debug("<CHECK>")
        self.status = ("state", "check")
        self.reporter.report(
            f"Comparing {self.local_connector.directory} <=> {self.external_connector.directory}"
        )

        with self.reporter.progress() as progress:
            self.die_if_necessary()
            task = progress.add_task("Getting local files...", total=None)
            local_files = self.file_names or self.filter_local(**kwargs)

            progress.remove_task(task)

            # cannot be a generator since we need to do a `if in` lookup:
            task = progress.add_task("Getting external files...", total=None)
            external_files = list(self.filter_external(**kwargs))
            log.debug(f"Checking {len(external_files)} files")
            progress.remove_task(task)

            self._reset_check_counter()

            task = progress.add_task("Checking...", total=None)
            for f in local_files:
                self.die_if_necessary()
                self.number_of_local_files += 1
                self.make_external_name(f)
                local_vals = self._check_local(f)

                if self.external_name in external_files:
                    log.info(f"{f.name} -> {self.external_name}")
                    code = 1
                    exists = True
                    self.number_of_external_duplicates += 1
                    external_vals = self.checker.check(
                        self.external_name,
                        connector=self.external_connector,
                    )
                    same = True
                    for k in local_vals:
                        if local_vals[k] != external_vals[k]:
                            same = False
                            self.number_of_duplicates_out_of_sync += 1
                            code = 0
                            break

                    log.debug(f"in sync: {same}")

                else:
                    self.number_of_duplicates_out_of_sync += 1
                    logging.debug(f"{f.name} -> {self.external_name}")
                    exists = False
                    code = 0

                if update_db:
                    log.debug("updating db")
                    self.bookkeeper.register(f)
                    if self.bookkeeper.code < 2:
                        if not force and not exists:
                            code = self.bookkeeper.code
                        self.bookkeeper.update_record(
                            self.external_name, code=code, **local_vals
                        )
            progress.remove_task(task)

        self.reporter.report("REPORT (CHECK):")
        self.reporter.report(
            f"-Total number of local files:    {self.number_of_local_files}"
        )
        self.reporter.report(
            f"-Files with external duplicates: {self.number_of_external_duplicates}"
        )
        self.reporter.report(
            f"-Files out of sync:              {self.number_of_duplicates_out_of_sync}"
        )
        log.debug("<CHECK FINISHED>")

    def run(self):
        """Copy the files that needs to be copied and update the db.

        Remarks:
            The method only iterates over the files that are registered in the
            self.file_names attribute. This attribute is typically set by the filter_local
            method.
        """
        use_threads = (
            False  # To be implemented - but need to fix log rotation etc. first
        )

        log.debug("<RUN>")
        self.die_if_necessary()
        self.status = ("state", "run")
        self.status = ("local_exists", False)

        failed_files = []

        for chunk in chunkify(self.file_names, n=20):
            self.die_if_necessary()
            if use_threads:
                failed = self._process_chunk(chunk)
            else:
                failed = self._process_single_chunk(chunk)
            failed_files.extend(failed)

        if not self.status["local_exists"]:
            self.reporter.report(
                "No files to handle. Did you forget to run `worker.filter_local()`?"
            )

        log.debug("<RUN FINISHED>")
        self.status = ("state", "finished")

    def _process_chunk(self, chunk):
        failed_files = []
        futures = []
        with ThreadPoolExecutor(max_workers=20) as executor:
            for f in chunk:
                self.status = ("local_exists", True)
                futures.append(executor.submit(self._process_file, f))
            for future in as_completed(futures):
                try:
                    failed_file = future.result()
                    if failed_file:
                        failed_files.append(failed_file)
                except Exception as e:
                    log.error(f"Error when processing file: {e}")
        return failed_files

    def _process_single_chunk(self, chunk):
        failed_files = []
        for f in chunk:
            self.status = ("local_exists", True)
            try:
                failed_file = self._process_file(f)
                if failed_file:
                    failed_files.append(failed_file)
            except Exception as e:
                log.error(f"Error when processing file: {e}")
                failed_files.append(f)
        return failed_files

    def _process_file(self, f):
        """Process a single file."""
        del self.status
        self.die_if_necessary()
        self.make_external_name(f)
        self.bookkeeper.register(f)
        try:
            checks = self.checker.check(f)
        except Exception as e:
            log.error(f"Error when checking {f}: {e}")
            return f

        if not self.bookkeeper.is_changed(**checks):
            log.debug(f"{f.name} == {self.external_name}")
            self.reporter.report(".", same_line=True)
            return

        log.debug(f"{f.name} -> {self.external_name}")

        self.status = ("changed", True)

        if self.reconnect:
            self.external_connector.reconnect()
        success = self.external_connector.move_func(f, self.external_name)

        if not success:
            log.debug("failed - so trying one more time after reconnecting...")
            self.external_connector.reconnect()
            success = self.external_connector.move_func(f, self.external_name)

        if success:
            self.status = ("moved", True)
            self.bookkeeper.update_record(self.external_name, **checks)
            self.reporter.report("o", same_line=True)
            log.debug(f"{f.name} -> {self.external_name} copied")
            return

        self.reporter.report("!", same_line=True)
        log.debug(f"{f.name} -> {self.external_name} FAILED COPY!")
        return f

    def _default_external_name_generator(self, f):
        log.debug(f"{self.subdirs=} {self.external_subdirs=}")

        if self.subdirs and self.external_subdirs:
            ext_name = self.external_connector.directory / f.relative_to(
                self.local_connector.directory
            )
        else:
            ext_name = self.external_connector.directory / f.name
        return ext_name

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
        if key == "state":
            self.reporter.status(value)

    @status.deleter
    def status(self):
        for k in self._status:
            if k != "state" and k != "local_exists":  # protected members
                self._status[k] = None

    @property
    def external_name(self):
        return self._external_name

    @external_name.setter
    def external_name(self, name):
        self._external_name = name

    def close(self):
        self.reporter.report("<CLOSE WORKER>")
        self.external_connector.close()
        self.reporter.close()

    def die_if_necessary(self):
        should_die = self.reporter.should_die()
        if should_die:
            self.reporter.report("You told me to die! Dying...")
            self.close()
            sys.exit(0)


def simple_worker(
    base_directory_from=None,
    base_directory_to=None,
    db_name=None,
    dry_run=False,
    extension=None,
    reporter=None,
    include_subdirs=False,
    external_subdirs=False,
):
    """Create a Worker for copying files locally.

    Args:
        base_directory_from: directory to copy from.
        base_directory_to: directory to copy to.
        db_name: name of the database.
        dry_run: set to True if you would like to run without updating or moving anything.
        extension: file extension to filter on (for example '.csv').
        reporter: reporter to use. If None, a default reporter will be used.
        include_subdirs: set to True if you want to include subdirectories.
        external_subdirs: set to True if you want to include subdirectory structure in the external directory
          (only makes sense if include_subdirs is True).

    Returns:
        simple worker that can copy files between two local folder.

    Usage:
        >>> my_oeleo = simple_worker()  # reads necessary settings from .env or ENVs as default.
        >>> my_oeleo.filter_local()  # or my_oeleo.add_local(["file1.csv", "file2.csv"])
        >>> my_oeleo.run()
    """
    db_name = db_name or os.environ["OELEO_DB_NAME"]
    base_directory_from = base_directory_from or os.environ["OELEO_BASE_DIR_FROM"]
    base_directory_to = base_directory_to or os.environ["OELEO_BASE_DIR_TO"]
    if extension is None:
        extension = os.environ["OELEO_FILTER_EXTENSION"]

    bookkeeper = SimpleDbHandler(db_name)
    checker = ChecksumChecker()

    # Consider performing the setting of _include_subdirs in the worker instead
    local_connector = LocalConnector(
        directory=base_directory_from, include_subdirs=include_subdirs
    )
    external_connector = LocalConnector(
        directory=base_directory_to, include_subdirs=external_subdirs
    )
    reporter = reporter or Reporter()
    log.debug("<Simple Worker created>")
    log.debug(f"from:{base_directory_from}")
    log.debug(f"to  :{base_directory_to}")

    worker = Worker(
        checker=checker,
        local_connector=local_connector,
        external_connector=external_connector,
        bookkeeper=bookkeeper,
        extension=extension,
        dry_run=dry_run,
        reporter=reporter,
        reconnect=True,
        subdirs=include_subdirs,
        external_subdirs=external_subdirs,
    )
    return worker


def ssh_worker(
    base_directory_from: Union[str, None, Path] = None,
    base_directory_to: Union[str, None, Path] = None,
    db_name: Union[str, None] = None,
    extension: str = None,
    use_password: bool = False,
    dry_run: bool = False,
    reporter: ReporterBase = None,
    is_posix: bool = True,
    include_subdirs: bool = False,
    external_subdirs: bool = False,
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
        reporter: reporter to use. If None, a default reporter will be used.
        include_subdirs: include subdirectories when filtering local files.
        external_subdirs: include subdirectories when filtering remote files.

    Returns:
        worker with SSHConnector attached to it.
    """

    db_name = db_name or os.environ["OELEO_DB_NAME"]
    base_directory_from = base_directory_from or os.environ["OELEO_BASE_DIR_FROM"]
    base_directory_to = base_directory_to or os.environ["OELEO_BASE_DIR_TO"]
    extension = extension or os.environ["OELEO_FILTER_EXTENSION"]

    local_connector = LocalConnector(
        directory=base_directory_from,
        include_subdirs=include_subdirs,
    )
    external_connector = SSHConnector(
        directory=base_directory_to,
        use_password=use_password,
        is_posix=is_posix,
        include_subdirs=external_subdirs,
    )

    bookkeeper = SimpleDbHandler(db_name)
    checker = ChecksumChecker()
    reporter = reporter or Reporter()

    log.debug("<SSH Worker created>")
    log.debug(f"from:{local_connector.directory}")
    log.debug(f"to  :{external_connector.host}:{external_connector.directory}")

    worker = Worker(
        checker=checker,
        local_connector=local_connector,
        external_connector=external_connector,
        bookkeeper=bookkeeper,
        extension=extension,
        dry_run=dry_run,
        reporter=reporter,
        reconnect=True,
        subdirs=include_subdirs,
        external_subdirs=external_subdirs,
    )
    return worker


def sharepoint_worker(
    base_directory_from: Union[Path, None] = None,
    url: Union[Path, None] = None,
    sitename: Union[str, None] = None,
    doc_library_to: Union[str, None] = None,
    db_name: Union[str, None] = None,
    extension: str = None,
    reporter: ReporterBase = None,
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
        reporter: reporter to use. If None, a default reporter will be used.
        dry_run: set to True if you would like to run without updating or moving anything.

    Returns:
        worker with SharePoint attached to it.
    """

    def external_name_generator(con, name):
        return Path(name.name)

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
    reporter = reporter or Reporter()
    log.debug("<SSH Worker created>")

    log.debug(f"from: {local_connector.directory}")
    log.debug(f"to  :{external_connector.url}:{external_connector.directory}")

    worker = Worker(
        checker=checker,
        local_connector=local_connector,
        external_connector=external_connector,
        bookkeeper=bookkeeper,
        extension=extension,
        external_name_generator=external_name_generator,
        dry_run=dry_run,
        reporter=reporter,
    )
    return worker
