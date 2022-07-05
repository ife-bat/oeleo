import os
from pathlib import Path

import dotenv
from oeleo.utils import logger
from oeleo.workers import simple_worker

log = logger()


def test_import():
    from oeleo import connectors
    assert "SSHConnector" in dir(connectors)


def test_dotenv():
    dotenv.load_dotenv(".testenv")
    assert "OELEO_BASE_DIR_FROM" in os.environ.keys()


def test_simple_worker():
    dotenv.load_dotenv(".testenv")
    log.info(f"Starting oeleo!")
    filter_extension = os.environ["OELEO_FILTER_EXTENSION"]

    db_name = str(Path(os.environ["OELEO_DB_NAME"]).resolve())
    base_directory_from = Path(os.environ["OELEO_BASE_DIR_FROM"]).resolve()
    base_directory_to = Path(os.environ["OELEO_BASE_DIR_TO"]).resolve()

    log.info(f"pytest running in {Path(os.environ['OELEO_BASE_DIR_FROM']).resolve()}")
    log.info(f"{db_name=}")
    log.info(f"{base_directory_from=}")
    log.info(f"{base_directory_to=}")

    assert base_directory_to.is_dir()
    assert base_directory_from.is_dir()

    worker = simple_worker(
        db_name=db_name,
        base_directory_from=base_directory_from,
        base_directory_to=base_directory_to,
    )
    worker.connect_to_db()
    worker.filter_local(filter_extension)
    worker.check(filter_extension)
    worker.run()
