import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Generator

from models import DbHandler, MockDbHandler
from movers import mock_mover

log = logging.getLogger("oeleo")


@dataclass
class Worker:
    filter_method: Any
    checker: Any
    mover_method: Any  # MAKE THIS A CLASS INSTEAD
    from_dir: Path
    to_dir: Path
    bookkeeper: DbHandler
    dry_run: bool = False
    local_connector: Any = None
    external_connector: Any = None
    file_names: Generator[Path, None, None] = field(init=False)
    _external_name: str = field(init=False, default="")
    _status: dict = field(init=False, default_factory=dict)

    def __post_init__(self):
        if self.dry_run:
            log.info("[bold red blink]DRY RUN[/]", extra={"markup": True})
            self.mover_method = mock_mover
            self.bookkeeper = MockDbHandler()

    def connect_to_db(self):
        self.bookkeeper.initialize_db()
        log.info(f"Connecting to db -> '{self.bookkeeper.db_name}' DONE")

    def filter_local(self, *args, **kwargs):
        """Selects the files that should be processed"""
        self.file_names = self._filter(
            None,
            self.from_dir,
            *args,
            **kwargs,
        )
        log.info("Filtering -> DONE")

    def _filter(self, connector, dir_path, *args, **kwargs):
        """Selects the files that should be checked .
        Arguments:
            connector:
            dir_path:
            additional_filters:
        """
        base_filter_func = kwargs.pop("base_filter_func", None)
        if (base_filter_func is None) and (connector is not None):
            base_filter_func = connector.base_filter_func
        file_names = self.filter_method(
            dir_path,
            *args,
            base_filter_func=base_filter_func,
            **kwargs,
        )
        return file_names

    def check(self, *args, **kwargs):
        """Check for differences between the two directories."""
        print(f"Comparing {self.from_dir} <=> {self.to_dir}")
        additional_filters = kwargs.pop("additional_filters", None)
        local_files = self._filter(
            self.local_connector,
            self.from_dir,
            *args,
            additional_filters=additional_filters,
            **kwargs,
        )
        external_files = list(
            self._filter(self.external_connector, self.to_dir, *args, **kwargs)
        )
        log.info(external_files)
        number_of_local_files = 0
        number_of_external_duplicates = 0
        number_of_duplicates_out_of_sync = 0

        for f in local_files:
            number_of_local_files += 1
            external_name = self._create_external_name(f)
            print(f" (*) {f.name}", end=" ")
            if external_name in external_files:
                print(f"[FOUND EXTERNAL]")
                number_of_external_duplicates += 1
                local_vals = self.checker.check(f)

                # ch = self.external_connector.calculate_checksum(external_name)
                # external_vals = {"checksum": ch}

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
                print("[ONLY LOCAL]")
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
                if self.mover_method(f, self.external_name, connector=self.external_connector):
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
        return self.to_dir / f.name

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
