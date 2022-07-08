import logging
import time
from datetime import datetime
from typing import Protocol, Union

from oeleo.workers import WorkerBase

log = logging.getLogger("oeleo")


class SchedulerBase(Protocol):
    worker: WorkerBase = None
    state: dict = None

    def _setup(self):
        ...

    def start(self):
        ...

    def _update_db(self):
        ...

    # consider adding a close_all or clean_up method


class SimpleScheduler(SchedulerBase):
    def __init__(
        self, worker: WorkerBase, run_interval_time=43_200, max_run_intervals=1000
    ):
        self.worker = worker
        self.state = {}
        # self.update_interval = 3_600  # not used
        self.run_interval_time = run_interval_time
        self.max_run_intervals = max_run_intervals
        # self._last_update = None
        self._sleep_interval = max(run_interval_time / 10, 1)
        self._last_run = None
        self._run_counter = 0

    def _setup(self):
        self.worker.connect_to_db()
        self.worker.check(update_db=True)
        # self._last_update = datetime.now()

    def start(self):
        self._setup()
        while True:
            self.worker.filter_local()
            self.worker.run()
            self._last_run = datetime.now()
            self._run_counter += 1

            if self._run_counter >= self.max_run_intervals:
                break

            used_time = 0.0

            while used_time < self.run_interval_time:
                time.sleep(self._sleep_interval)
                used_time = (datetime.now() - self._last_run).total_seconds()
        self.worker.close()

    def _update_db(self):
        pass
