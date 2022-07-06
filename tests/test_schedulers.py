import os
from pathlib import Path

import dotenv

from oeleo.utils import logger
from oeleo.workers import simple_worker, MockWorker
from oeleo.schedulers import SimpleScheduler

log = logger()


def test_creation():
    worker = MockWorker()
    s = SimpleScheduler(
        worker,
        run_interval_time=2,
        max_run_intervals=2,
    )
    s.start()
