import logging
import os
import dotenv
import pytest

import utils
from connectors import LocalConnector
from movers import simple_mover, connected_mover
from oeleo.utils import start_logger
from oeleo.schedulers import RichScheduler, SimpleScheduler

log = start_logger()


def test_import():
    from oeleo import connectors

    assert "SSHConnector" in dir(connectors)


def test_dotenv():
    dotenv.load_dotenv(".testenv")
    assert "OELEO_BASE_DIR_FROM" in os.environ.keys()


# ----------- movers --------------------


def test_simple_mover(external_tmp_path, local_file_tmp_path):
    external_file_tmp_path = external_tmp_path / local_file_tmp_path.name
    assert not external_file_tmp_path.is_file()
    log.info(f"moving {local_file_tmp_path} to {external_file_tmp_path}")
    assert simple_mover(local_file_tmp_path, external_file_tmp_path)
    assert external_file_tmp_path.is_file()


def test_connected_mover_default_connector(external_tmp_path, local_file_tmp_path):
    external_file_tmp_path = external_tmp_path / local_file_tmp_path.name
    assert not external_file_tmp_path.is_file()
    log.info(f"moving {local_file_tmp_path} to {external_file_tmp_path}")
    assert connected_mover(local_file_tmp_path, external_file_tmp_path)
    assert external_file_tmp_path.is_file()


def test_connected_mover_ssh_connector():
    # NOT IMPLEMENTED YET
    # Currently tested "manually" by the developer.
    pass


def test_connected_mover_sharepoint_connector():
    # NOT IMPLEMENTED YET
    # Currently tested "manually" by the developer.
    pass


# ----------- connectors ----------------


def test_local_connector_filter(local_tmp_path):
    local_connector = LocalConnector(local_tmp_path)
    assert local_connector.directory.is_dir()
    base_filter = local_connector.base_filter_sub_method(".xyz")
    assert len(list(base_filter)) == 2
    base_filter = local_connector.base_filter_sub_method(".txt")
    assert len(list(base_filter)) == 1
    base_filter = local_connector.base_filter_sub_method(".*")
    assert len(list(base_filter)) == 3
    base_filter = local_connector.base_filter_sub_method(".kollargoll")
    assert len(list(base_filter)) == 0


def test_local_connector_calc_checksum(local_file_tmp_path):
    local_connector = LocalConnector(local_file_tmp_path.parent)
    assert local_connector.directory.is_dir()
    checksum = local_connector.calculate_checksum(local_file_tmp_path)
    assert checksum == "7920697396c631989f51a80df0813e86"


def test_local_connector_move(external_tmp_path, local_file_tmp_path):
    local_connector = LocalConnector(local_file_tmp_path.parent)
    external_file_tmp_path = external_tmp_path / local_file_tmp_path.name
    log.info(f"moving {local_file_tmp_path} to {external_file_tmp_path}")
    assert local_connector.move_func(local_file_tmp_path, external_file_tmp_path)


def test_ssh_connector_connect():
    # NOT IMPLEMENTED YET
    # Currently tested "manually" by the developer.
    pass


def test_ssh_connector_filter():
    # NOT IMPLEMENTED YET
    # Currently tested "manually" by the developer.
    pass


def test_ssh_connector_calc_checksum():
    # NOT IMPLEMENTED YET
    # Currently tested "manually" by the developer.
    pass


def test_ssh_connector_calc_move():
    # NOT IMPLEMENTED YET
    # Currently tested "manually" by the developer.
    pass


def test_sharepoint_connector():
    # NOT IMPLEMENTED YET
    # Currently tested "manually" by the developer.
    pass


# ----------- utils ------------------


def test_calculate_checksum(local_file_tmp_path):
    assert (
        utils.calculate_checksum(local_file_tmp_path)
        == pytest.checksum_local_file_tmp_path
    )


def test_logger():
    test_log = utils.start_logger(name="test-oeleo")
    test_log.info("Hello from oeleo test suite")


def test_logger_debug():
    test_log = utils.start_logger(name="test-oeleo", log_level=logging.DEBUG)
    test_log.debug("Hello from oeleo test suite")


def test_logger_format():
    # not finished yet
    test_log = utils.start_logger(
        name="test-oeleo",
        log_level=logging.INFO,
        log_message_format="%(asctime)s %(message)s",
    )
    test_log.info("Hello with time from oeleo test suite")


# ----------- filters ----------------


# ----------- models -----------------


# ----------- checkers ---------------


# ----------- reporters --------------


# ----------- layouts ----------------


# ----------- schedulers -------------


# ----------- workers ----------------


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


def test_worker_with_simple_scheduler(
    simple_worker_with_two_matching_and_one_not_matching,
):
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


def test_worker_with_rich_scheduler(
    simple_worker_with_two_matching_and_one_not_matching,
):

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
