# Usage

## Run flow

1. Create an `oeleo` worker instance.
2. Connect the worker's bookkeeper to a SQLite database.
3. Filter local files.
4. Run to copy files.
5. Repeat from step 3.

You can build a worker with the `Worker` class or the factory helpers in `oeleo.workers` (for example `simple_worker` and `ssh_worker`).

## Local folder → local folder

```python
import os
from pathlib import Path
import time

import dotenv

from oeleo.checkers import ChecksumChecker
from oeleo.models import SimpleDbHandler
from oeleo.connectors import LocalConnector
from oeleo.workers import Worker
from oeleo.utils import start_logger


def main():
  log = start_logger()
  # assuming you have made a .env file:
  dotenv.load_dotenv()

  db_name = os.environ["OELEO_DB_NAME"]
  base_directory_from = Path(os.environ["OELEO_BASE_DIR_FROM"])
  base_directory_to = Path(os.environ["OELEO_BASE_DIR_TO"])
  filter_extension = os.environ["OELEO_FILTER_EXTENSION"]

  # Making a worker using the Worker class.
  # You can also use the `factory` functions in `oeleo.workers`
  # (e.g. `ssh_worker` and `simple_worker`)
  bookkeeper = SimpleDbHandler(db_name)
  checker = ChecksumChecker()
  local_connector = LocalConnector(directory=base_directory_from)
  external_connector = LocalConnector(directory=base_directory_to)

  worker = Worker(
    checker=checker,
    local_connector=local_connector,
    external_connector=external_connector,
    bookkeeper=bookkeeper,
    extension=filter_extension
  )

  # Running the worker with 5 minutes intervals.
  # You can also use an oeleo scheduler for this.
  worker.connect_to_db()
  while True:
    worker.filter_local()
    worker.run()
    time.sleep(300)


if __name__ == "__main__":
  main()
```

## Using an `oeleo` scheduler

Instead of a `while` loop, you can use an external scheduler (for example `rocketry`, `watchdog`, `schedule`, or Airflow), or oeleo's own `SimpleScheduler`:

```python
import dotenv

from oeleo.schedulers import SimpleScheduler
from oeleo.workers import simple_worker

# assuming you have created an appropriate .env file
dotenv.load_dotenv()
worker = simple_worker()
s = SimpleScheduler(
        worker,
        run_interval_time=4,  # seconds
        max_run_intervals=4,
    )
s.start()
```

## Windows PC → Linux server (SSH)

```python
import logging
import os
from pathlib import Path

import dotenv

from oeleo.connectors import register_password
from oeleo.utils import start_logger
from oeleo.workers import ssh_worker

log = start_logger()

print(" ssh ".center(80, "-"))
log.setLevel(logging.DEBUG)
log.info(f"Starting oeleo!")
dotenv.load_dotenv()

external_dir = "/srv/data"
filter_extension = ".res"

register_password(os.environ["OELEO_PASSWORD"])

worker = ssh_worker(
  db_name="ssh_to_server.db",
  base_directory_from=Path(r"data\raw"),
  base_directory_to=external_dir,
  extension=filter_extension,
)
worker.connect_to_db()
try:
  worker.check(update_db=True)
  worker.filter_local()
  worker.run()
finally:
  worker.close()
```

See [Configuration](configuration.md) for environment variables and [Database](database.md) for bookkeeping details.
