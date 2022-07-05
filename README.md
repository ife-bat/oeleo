# oeleo
Python package / app that can be used for transferring files from an instrument-PC to a data server.

It is not very sophisticated. But I am not very sophisticated either.


## Features (or limitations)
- Transferring using an ssh connection should preferably be used with key-pairs. This might involve some
  setting up on your server (ACL) to prevent security issues (the `oeleo` user should only have access to
  the data folder on your server).
- Accessing ssh can be done using password if you are not able to figure out how to set proper ownerships 
  on your server.
- `oeleo` is one-eyed. Meaning that tracking of the "state of the duplicates" is only performed on the local side (where `oeleo` is running).
- However, `oeleo` contains a `check` method that can help you figure out if starting copying is a  
  good idea or not. And populate the database if you want.
- The db that stores information about the "state of the duplicates" is stored relative to the folder 
  `oeleo` is running from. If you delete it (by accident?), `oeleo` will make a new empty one from scratch next time you run.
- Configuration is done using environmental variables. 

## Usage

### Install

```bash
$ pip install oeleo
```
### Run

1. Create an `oeleo` worker instance.
2. Connect the worker's `bookkeeper` to a `sqlite3` database.
3. Filter local files.
4. Run to copy files.
5. Repeat from step 3.

### Examples

#### Simple script for copying between local folders

```python
import os
from pathlib import Path
import time

import dotenv

from oeleo.checkers import  SimpleChecker
from oeleo.models import SimpleDbHandler
from oeleo.movers import simple_mover
from oeleo.workers import Worker
from oeleo.utils import logger

def main():
    log = logger()
    # assuming you have made a .env file:
    dotenv.load_dotenv()
    
    db_name = os.environ["OELEO_DB_NAME"]
    base_directory_from = Path(os.environ["OELEO_BASE_DIR_FROM"])
    base_directory_to = Path(os.environ["OELEO_BASE_DIR_TO"])
    filter_extension = os.environ["OELEO_FILTER_EXTENSION"]
    
    bookkeeper = SimpleDbHandler(db_name)
    checker = SimpleChecker()
    
    worker = Worker(
        checker=checker,
        mover_method=simple_mover,
        from_dir=base_directory_from,
        to_dir=base_directory_to,
        bookkeeper=bookkeeper,
    )
    
    worker.connect_to_db()
    while True:
        worker.filter_local(filter_extension)
        worker.run()
        time.sleep(300)

if __name__ == "__main__":
    main()
```

#### Example .env file
```.env
OELEO_BASE_DIR_FROM=C:\data\local
OELEO_BASE_DIR_TO=C:\data\pub
OELEO_FILTER_EXTENSION=csv
OELEO_DB_NAME=local2pub.db

## only needed for SSHConnector:
# OELEO_EXTERNAL_HOST=<ssh hostname>
# OELEO_USERNAME=<ssh username>
# OELEO_PASSWORD=<ssh password>
# OELEO_KEY_FILENAME=<ssh key-pair filename>
```


## Future planned improvements

Just plans, no promises given.

- add tests.
- implement proxy for `peewee` database (makes it possible to switch db from `sqlite3` to for example `postgresql`).
- implement a `SharePointConnector`.
- create CLI.
- create an executable.
- create a web-app.
- create a GUI.

## Status

- [x] Works on my PC &rarr; PC
- [x] Works on my PC &rarr; my server
- [ ] Works on my server &rarr; my server
- [ ] Works on my instrument PC &rarr; my instrument PC
- [ ] Works on my instrument PC &rarr; my server
- [ ] Works OK
- [ ] Deployable

## Licence
MIT

## Development

Developed using `poetry` on `python 3.10`.

### Some useful commands

#### Update version

```bash
# update version e.g. from 0.3.1 to 0.3.2:
poetry version patch
```
Then edit `__init__.py`:
```python
__version__ = "0.3.2"
```
#### Build

```bash
poetry build
```

#### Publish

```bash
poetry publish
```

### Development lead
- Jan Petter Maehlen, IFE
