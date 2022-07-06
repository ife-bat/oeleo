import time
from datetime import datetime, timedelta
from typing import Protocol, Union

from oeleo.workers import Worker


class Scheduler(Protocol):
    worker: Union[Worker, None] = None

    def _setup(self):
        ...

    def start(self):
        ...

    def _update_db(self):
        ...


class SimpleScheduler(Scheduler):
    def __init__(self, worker: Worker, run_interval=43_200, max_run_intervals=1000):
        self.worker = worker
        # self.update_interval = 3_600  # not used
        self.run_interval = timedelta(seconds=run_interval)
        self.max_run_intervals = max_run_intervals
        # self._last_update = None
        self._sleep_interval = run_interval / 10
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

            used_time = 0
            while used_time < self.run_interval:
                time.sleep(self._sleep_interval)
                used_time = self._last_run - datetime.now()

    def _update_db(self):
        pass

