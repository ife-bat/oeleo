from datetime import datetime
import time
import os
import logging

import dotenv

try:
    import pystray
except ImportError:
    pystray = None

import oeleo
from oeleo.utils import start_logger, to_bool
from oeleo.reporters import LogAndTrayReporter, LogReporter
from oeleo.workers import ssh_worker
from oeleo.schedulers import SimpleScheduler

dotenv.load_dotenv()
start_logger(only_oeleo=False)
log = logging.getLogger("oeleo")

log.debug(f"*A2O* starting oeleo!")
log.debug(f"{oeleo.__file__=}")
log.debug(f"{oeleo.__version__=}")

startswith = os.environ.get("OA_STARTS_WITH")
if startswith and ";" in startswith:
    startswith = startswith.split(";")

single_run = os.environ.get("OA_SINGLE_RUN", False)
add_check = os.environ.get("OA_ADD_CHECK", False)
single_run = to_bool(single_run)
add_check = to_bool(add_check)

max_run_intervals = os.environ.get("OA_MAX_RUN_INTERVALS", 200)
max_run_intervals = int(max_run_intervals)
hours_sleep = os.environ.get("OA_HOURS_SLEEP", 0.5)
hours_sleep = float(hours_sleep)

from_year = os.environ.get("OA_FROM_YEAR", 2023)
from_month = os.environ.get("OA_FROM_MONTH", 1)
from_day = os.environ.get("OA_FROM_DAY", 1)

from_year = int(from_year)
from_month = int(from_month)
from_day = int(from_day)

my_filters = [
    (
        "not_before",
        datetime(
            year=from_year, month=from_month, day=from_day, hour=0, minute=0, second=0
        ),
    ),
]

if startswith:
    my_filters.append(("startswith", startswith))


log.debug(f"*A2O* settings")
log.debug(f"{single_run=}")
log.debug(f"{add_check=}")
log.debug(f"{startswith=}")
log.debug(f"{from_year=}")
log.debug(f"{from_month=}")
log.debug(f"{max_run_intervals=}")
log.debug(f"{hours_sleep=}")


def ssh_connection():
    run_interval_time = 3600 * hours_sleep

    if pystray is not None:
        reporter = LogAndTrayReporter()
    else:
        reporter = LogReporter()

    log.debug(f"*A2O* creating worker")
    worker = ssh_worker(reporter=reporter)
    log.debug(f"*A2O* creating scheduler")
    s = SimpleScheduler(
        worker,
        run_interval_time=run_interval_time,
        max_run_intervals=max_run_intervals,
        additional_filters=my_filters,
        add_check=add_check,
    )
    log.debug(f"*A2O* starting scheduler")
    s.start()


def single_ssh_connection():
    if pystray is not None:
        reporter = LogAndTrayReporter()
    else:
        reporter = LogReporter()

    log.debug(f"*A2O* creating worker")
    worker = ssh_worker(reporter=reporter)
    log.debug(f"*A2O* connecting to db ({worker.db_path})")
    worker.connect_to_db()
    if add_check:
        log.debug(f"*A2O* checking")
        worker.check(update_db=True, additional_filters=my_filters)
    log.debug(f"*A2O* filtering local")
    worker.filter_local(additional_filters=my_filters)
    log.debug(f"*A2O* running")
    worker.run()


if __name__ == "__main__":
    if single_run:
        single_ssh_connection()
    else:
        ssh_connection()
