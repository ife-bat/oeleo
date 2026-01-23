import atexit
import logging
import time
from datetime import datetime, timedelta
from typing import Protocol, Union, Any
import warnings

from rich import print
from rich.live import Live
from rich.panel import Panel

from oeleo.workers import WorkerBase

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
        self,
        worker: WorkerBase,
        run_interval_time=43_200,
        max_run_intervals=1000,
        update_db=True,
        force=False,
        add_check=False,
        additional_filters=None,
    ):
        self.worker = worker
        self.state = {"iterations": 0}
        # self.update_interval = 3_600  # not used
        self.run_interval_time = run_interval_time
        self.max_run_intervals = max_run_intervals
        self.update_db: bool = update_db
        self.force: bool = force
        self.additional_filters: Any = additional_filters
        self.add_check: bool = add_check
        # self._last_update = None
        self._sleep_interval = max(run_interval_time / 10, 1)
        self._last_run = None
        self._run_counter = 0

    def _setup(self):
        log.debug("setting up scheduler")
        self.worker.connect_to_db()
        if self.add_check:
            self.worker.check(
                update_db=self.update_db,
                force=self.force,
                additional_filters=self.additional_filters,
            )
        # self._last_update = datetime.now()
        atexit.register(self._cleanup)

    def _cleanup(self):
        self.worker.close()

    def start(self):
        log.debug("SimpleScheduler *STARTED*")
        self._setup()
        while True:
            self.state["iterations"] += 1
            log.debug(f"ITERATING ({self.state['iterations']})")

            self.worker.filter_local(additional_filters=self.additional_filters)
            self.worker.run()
            self._last_run = datetime.now()
            self._run_counter += 1
            next_run_at = self._last_run + timedelta(seconds=self.run_interval_time)
            self.worker.reporter.update_metadata(
                last_run_at=self._last_run, next_run_at=next_run_at
            )

            if self._run_counter >= self.max_run_intervals:
                log.debug("-> BREAK")
                break

            used_time = 0.0
            poll_interval = 1.0
            self.worker.reporter.status("sleep")

            while used_time < self.run_interval_time:
                time.sleep(poll_interval)
                self.worker.die_if_necessary()
                used_time = (datetime.now() - self._last_run).total_seconds()
                log.debug(f"slept for {used_time} s of {self.run_interval_time} s")
        atexit.unregister(self._cleanup)
        self.worker.close()

    def _update_db(self):
        pass
