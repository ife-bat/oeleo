# oeleo

Python package / app for transferring files from an instrument PC to a data server.

`oeleo` is **one-eyed**: transfer state is tracked only on the local side (SQLite bookkeeping by checksum). Configuration uses environment variables.

**Documentation:** see the [`docs/`](docs/) folder (Zensical). Preview locally with `uv sync --group docs` then `uv run zensical serve`. A Read the Docs site will be wired up separately.

## Install

From PyPI (end users):

```bash
pip install oeleo
```

From a clone (development), use **uv** — see [docs/development.md](docs/development.md).

## Quick example (local → local)

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
  start_logger()
  dotenv.load_dotenv()

  worker = Worker(
    checker=ChecksumChecker(),
    local_connector=LocalConnector(directory=Path(os.environ["OELEO_BASE_DIR_FROM"])),
    external_connector=LocalConnector(directory=Path(os.environ["OELEO_BASE_DIR_TO"])),
    bookkeeper=SimpleDbHandler(os.environ["OELEO_DB_NAME"]),
    extension=os.environ["OELEO_FILTER_EXTENSION"],
  )

  worker.connect_to_db()
  while True:
    worker.filter_local()
    worker.run()
    time.sleep(300)


if __name__ == "__main__":
  main()
```

More examples (scheduler, SSH), full env-var reference, and database details: [docs/usage.md](docs/usage.md), [docs/configuration.md](docs/configuration.md), [docs/database.md](docs/database.md).

## Licence

MIT

## Development lead

Jan Petter Maehlen, IFE
