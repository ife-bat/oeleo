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
        """ Selects the files that should be processed """
        self.file_names = self.filter_method(
            self.from_dir,
            *args,
            **kwargs,
        )
        log.info("Filtering -> DONE")

    def _filter(self, connector, dir_path, *args, **kwargs):
        """ Selects the files that should be checked """
        file_names = self.filter_method(
            dir_path,
            *args,
            **kwargs,
        )
        return file_names

    def check(self, *args, **kwargs):
        """Check for differences between the two directories."""
        log.info("Running...")
        local_files = self._filter(self.local_connector, self.from_dir, *args, **kwargs)
        external_files = list(self._filter(self.external_connector, self.to_dir, *args, **kwargs))

        for f in local_files:
            external_name = self._create_external_name(f)
            if external_name in external_files:
                print(f"FOUND {external_name}")
                local_vals = self.checker.check(f)
                external_vals = self.checker.check(external_name)
                same = True
                for k in local_vals:
                    print(f"{k}: {local_vals[k]}")
                    print(f"{k}: {external_vals[k]}")
                    if local_vals[k] != external_vals[k]:
                        same = False
                print(f"Same file: {same}")

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

