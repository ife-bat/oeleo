import logging
import time
from datetime import datetime
from typing import Protocol, Union

from rich.live import Live
from rich.panel import Panel
from rich import print

from oeleo.layouts import create_layout, confirm
from oeleo.workers import WorkerBase
from oeleo.reporters import LayoutReporter

log = logging.getLogger("oeleo")


class ScheduleAborted(Exception):
    """Raised when the user aborts the run."""
    pass


class SchedulerBase(Protocol):
    worker: WorkerBase = None
    state: dict = None
    update_db: bool = True
    force: bool = False

    def _setup(self):
        ...

    def start(self):
        ...

    def _update_db(self):
        ...

    # consider adding a close_all or clean_up method


class SimpleScheduler(SchedulerBase):
    def __init__(
        self, worker: WorkerBase, run_interval_time=43_200, max_run_intervals=1000, update_db=True, force=False
    ):
        self.worker = worker
        self.state = {"iterations": 0}
        # self.update_interval = 3_600  # not used
        self.run_interval_time = run_interval_time
        self.max_run_intervals = max_run_intervals
        self.update_db: bool = update_db
        self.force: bool = force
        # self._last_update = None
        self._sleep_interval = max(run_interval_time / 10, 1)
        self._last_run = None
        self._run_counter = 0

    def _setup(self):
        log.debug("setting up scheduler")
        self.worker.connect_to_db()
        self.worker.check(update_db=self.update_db, force=self.force)
        # self._last_update = datetime.now()

    def start(self):
        log.debug("***** START:")
        self._setup()
        while True:
            self.state["iterations"] += 1
            log.debug(f"ITERATING ({self.state['iterations']})")

            self.worker.filter_local()
            self.worker.run()
            self._last_run = datetime.now()
            self._run_counter += 1

            if self._run_counter >= self.max_run_intervals:
                log.debug("-> BREAK")
                break

            used_time = 0.0

            while used_time < self.run_interval_time:
                time.sleep(self._sleep_interval)
                used_time = (datetime.now() - self._last_run).total_seconds()
        self.worker.close()

    def _update_db(self):
        pass


class RichScheduler(SchedulerBase):
    def __init__(
        self, worker: WorkerBase, run_interval_time=43_200, max_run_intervals=1000, update_db=True, force=False
    ):
        self.worker = worker
        self.state = {"iterations": 0}
        # self.update_interval = 3_600  # not used
        self.run_interval_time: Union[float, int] = run_interval_time
        self.max_run_intervals: int = max_run_intervals
        self.update_db: bool = update_db
        self.force: bool = force
        # self._last_update = None
        self._sleep_interval = max(run_interval_time / 10, 1)
        self._last_run = None
        self._run_counter = 0
        self.layout = None

    def _setup(self):
        log.debug("setting up scheduler")
        self.layout = create_layout()
        self.worker.reporter = LayoutReporter(self.layout)

    def start(self):
        log.debug("***** START:")
        try:
            self._setup()

            with Live(self.layout, refresh_per_second=20, screen=True):
                self.layout["middle_header"].update(
                    Panel(f"(L) {self.worker.local_connector.directory}")
                )
                self.layout["right_header"].update(
                    Panel(f"(E) {self.worker.external_connector.directory}")
                )
                self.worker.connect_to_db()

                self.layout["left_footer"].update(Panel(f"CHECK..."))
                self.worker.check(update_db=self.update_db, force=self.force)
                if not confirm(self.layout):
                    raise ScheduleAborted

                self.worker.reporter.clear()
                while True:
                    time.sleep(0.2)
                    self.state["iterations"] += 1
                    log.debug(f"ITERATING ({self.state['iterations']})")
                    self.layout["left_footer"].update(
                        Panel(f"I:{self.state['iterations']:06}")
                    )
                    self.worker.reporter.report(
                        f"\n[cyan bold]NEW ITERATION:[/cyan bold] {self.state['iterations']:06}/{self.max_run_intervals:06}"
                    )
                    self.layout["middle_footer"].update(Panel("filter local"))
                    self.worker.filter_local()
                    self.layout["middle_footer"].update(Panel("run"))
                    self.worker.run()
                    self._last_run = datetime.now()
                    self._run_counter += 1

                    if self._run_counter == self.max_run_intervals -2:
                        self.layout["status_footer"].update(Panel(":old_man_medium_skin_tone:"))

                    if self._run_counter >= self.max_run_intervals:
                        self.layout["middle_footer"].update(Panel("done"))
                        self.layout["status_footer"].update(Panel(":skull:"))
                        log.debug("-> BREAK")
                        time.sleep(0.2)
                        break

                    used_time = 0.0
                    self.layout["middle_footer"].update(
                        Panel(f"Idle for {round(used_time)}/{self.run_interval_time} s")
                    )
                    self.worker.reporter.report(".")
                    while used_time < self.run_interval_time:
                        time.sleep(self._sleep_interval)

                        # async sleep here
                        self.worker.reporter.report(".", same_line=True)
                        used_time = (datetime.now() - self._last_run).total_seconds()
                        self.layout["middle_footer"].update(
                            Panel(f"Idle for {round(used_time)}/{self.run_interval_time} s")
                        )
        except (KeyboardInterrupt, ScheduleAborted):
            print("[bold red]Interrupted by user ...exiting")

        else:
            print("[bold green]Finished ...exiting")

        finally:
            self.worker.close()

        for i, line in enumerate(self.worker.reporter.lines):
            print(f"[{i:03}] {line}")

    def _update_db(self):
        pass
