import os
import dotenv

from oeleo.utils import logger
from oeleo.schedulers import RichScheduler, SimpleScheduler

log = logger()


def test_import():
    from oeleo import connectors

    assert "SSHConnector" in dir(connectors)


def test_dotenv():
    dotenv.load_dotenv(".testenv")
    assert "OELEO_BASE_DIR_FROM" in os.environ.keys()


def test_simple_worker(simple_worker_with_two_matching_and_one_not_matching):

    filter_extension = os.environ["OELEO_FILTER_EXTENSION"]

    log.info(f"{filter_extension=}")

    worker = simple_worker_with_two_matching_and_one_not_matching
    from_directory = worker.local_connector.directory
    to_directory = worker.external_connector.directory

    assert from_directory.is_dir()
    assert to_directory.is_dir()
    assert len(os.listdir(to_directory)) == 0

    log.info(f"connecting to db: {worker.bookkeeper.db_name}")
    worker.connect_to_db()
    worker.filter_local()
    worker.check()
    worker.filter_local()
    worker.run()

    assert len(os.listdir(from_directory)) == 3
    assert len(os.listdir(to_directory)) == 2


def test_ssh_worker():
    # NOT IMPLEMENTED YET
    # Currently tested "manually" by the developer.
    pass


def test_worker_with_simple_scheduler(simple_worker_with_two_matching_and_one_not_matching):
    worker = simple_worker_with_two_matching_and_one_not_matching
    from_directory = worker.local_connector.directory
    to_directory = worker.external_connector.directory

    s = SimpleScheduler(
        simple_worker_with_two_matching_and_one_not_matching,
        run_interval_time=0.1,
        max_run_intervals=2,
    )
    s.start()

    assert len(os.listdir(from_directory)) == 3
    assert len(os.listdir(to_directory)) == 2


def test_worker_with_rich_scheduler(simple_worker_with_two_matching_and_one_not_matching):

    worker = simple_worker_with_two_matching_and_one_not_matching
    from_directory = worker.local_connector.directory
    to_directory = worker.external_connector.directory

    s = RichScheduler(
        worker,
        run_interval_time=0.1,
        max_run_intervals=2,
        auto_accept_check=True,
    )
    s.start()

    assert len(os.listdir(from_directory)) == 3
    assert len(os.listdir(to_directory)) == 2
