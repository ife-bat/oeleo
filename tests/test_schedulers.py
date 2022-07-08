import os
from pathlib import Path

import dotenv

from oeleo.schedulers import SimpleScheduler
from oeleo.utils import logger
from oeleo.workers import MockWorker, simple_worker

log = logger()


def test_creation():
    worker = MockWorker()
    s = SimpleScheduler(
        worker,
        run_interval_time=2,
        max_run_intervals=2,
    )
    s.start()
