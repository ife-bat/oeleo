import asyncio
import logging
import os
import time
from pathlib import Path
import dotenv
import pytest

from oeleo import utils
from oeleo.connectors import LocalConnector
from oeleo.movers import (
    simple_mover,
    connected_mover,
    async_simple_mover,
    async_connected_mover,
)
from oeleo.utils import start_logger
from oeleo.schedulers import SimpleScheduler
from oeleo.workers import simple_worker, simple_async_worker

start_logger()
log = logging.getLogger("test-oeleo")
TESTENV_PATH = Path(__file__).with_name(".testenv").resolve()


def test_import():
    from oeleo import connectors

    assert "SSHConnector" in dir(connectors)


def test_dotenv():
    dotenv.load_dotenv(TESTENV_PATH)
    assert "OELEO_BASE_DIR_FROM" in os.environ.keys()


# ----------- movers --------------------


def test_simple_mover(external_tmp_path, local_file_tmp_path):
    external_file_tmp_path = external_tmp_path / local_file_tmp_path.name
    assert not external_file_tmp_path.is_file()
    log.info(f"moving {local_file_tmp_path} to {external_file_tmp_path}")
    assert simple_mover(local_file_tmp_path, external_file_tmp_path)
    assert external_file_tmp_path.is_file()


def test_async_simple_mover(external_tmp_path, local_file_tmp_path):
    external_file_tmp_path = external_tmp_path / local_file_tmp_path.name
    assert not external_file_tmp_path.is_file()
    log.info(f"moving {local_file_tmp_path} to {external_file_tmp_path}")
    assert asyncio.run(async_simple_mover(local_file_tmp_path, external_file_tmp_path))
    assert external_file_tmp_path.is_file()


def test_connected_mover_default_connector(external_tmp_path, local_file_tmp_path):
    external_file_tmp_path = external_tmp_path / local_file_tmp_path.name
    assert not external_file_tmp_path.is_file()
    log.info(f"moving {local_file_tmp_path} to {external_file_tmp_path}")
    assert connected_mover(local_file_tmp_path, external_file_tmp_path)
    assert external_file_tmp_path.is_file()


def test_async_connected_mover_default_connector(
    external_tmp_path, local_file_tmp_path
):
    external_file_tmp_path = external_tmp_path / local_file_tmp_path.name
    assert not external_file_tmp_path.is_file()
    log.info(f"moving {local_file_tmp_path} to {external_file_tmp_path}")
    assert asyncio.run(
        async_connected_mover(local_file_tmp_path, external_file_tmp_path)
    )
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


def test_local_connector_async_move(external_tmp_path, local_file_tmp_path):
    local_connector = LocalConnector(local_file_tmp_path.parent)
    external_file_tmp_path = external_tmp_path / local_file_tmp_path.name
    log.info(f"moving {local_file_tmp_path} to {external_file_tmp_path}")
    assert asyncio.run(
        local_connector.async_move_func(local_file_tmp_path, external_file_tmp_path)
    )


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


def test_async_calculate_checksum(local_file_tmp_path):
    assert (
        asyncio.run(utils.async_calculate_checksum(local_file_tmp_path))
        == pytest.checksum_local_file_tmp_path
    )


def test_logger():
    utils.start_logger()
    logging.info("Hello from oeleo test suite")


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


def test_simple_async_worker(
    local_tmp_path, external_tmp_path, db_tmp_path
):
    worker = simple_async_worker(
        db_name=db_tmp_path,
        base_directory_from=local_tmp_path,
        base_directory_to=external_tmp_path,
    )
    from_directory = worker.local_connector.directory
    to_directory = worker.external_connector.directory

    worker.connect_to_db()
    worker.filter_local()
    asyncio.run(worker.async_run())

    assert len(os.listdir(from_directory)) == 3
    assert len(os.listdir(to_directory)) == 2


@pytest.mark.integration
def test_async_vs_sync_speed(local_tmp_path, external_tmp_path, tmp_path):
    if os.environ.get("OELEO_ASYNC_BENCH", "").lower() not in {"1", "true", "yes"}:
        pytest.skip("Set OELEO_ASYNC_BENCH=1 to run async/sync benchmark")

    sync_to = external_tmp_path / "sync"
    async_to = external_tmp_path / "async"
    sync_to.mkdir()
    async_to.mkdir()

    sync_worker = simple_worker(
        db_name=str(tmp_path / "sync.db"),
        base_directory_from=local_tmp_path,
        base_directory_to=sync_to,
    )
    async_worker = simple_async_worker(
        db_name=str(tmp_path / "async.db"),
        base_directory_from=local_tmp_path,
        base_directory_to=async_to,
    )

    sync_worker.connect_to_db()
    sync_worker.filter_local()
    t0 = time.perf_counter()
    sync_worker.run()
    sync_time = time.perf_counter() - t0

    async_worker.connect_to_db()
    async_worker.filter_local()
    t1 = time.perf_counter()
    asyncio.run(async_worker.async_run(max_concurrency=4))
    async_time = time.perf_counter() - t1

    log.info(f"sync_time={sync_time:.4f}s async_time={async_time:.4f}s")

    assert len(os.listdir(sync_to)) == 2
    assert len(os.listdir(async_to)) == 2

    if os.environ.get("OELEO_ASYNC_EXPECT_FASTER", "").lower() in {"1", "true", "yes"}:
        assert async_time <= sync_time


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


def test_worker_with_simple_scheduler_with_subdirs(
    local_tmp_path_with_subdirs,
    external_tmp_path,
    db_tmp_path,
):
    worker = simple_worker(
        db_name=db_tmp_path,
        base_directory_from=local_tmp_path_with_subdirs,
        base_directory_to=external_tmp_path,
        include_subdirs=True,
        external_subdirs=True,
    )
    from_directory = worker.local_connector.directory
    to_directory = worker.external_connector.directory

    s = SimpleScheduler(
        worker,
        run_interval_time=0.1,
        max_run_intervals=2,
    )
    s.start()

    assert len(list(Path(from_directory).rglob("*.xyz"))) == 4
    assert len(list(Path(to_directory).rglob("*.xyz"))) == 4