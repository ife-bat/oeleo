import pytest
import logging

import dotenv

from oeleo.utils import logger
from oeleo.workers import simple_worker

log = logger()


def pytest_configure():
    pytest.checksum_local_file_tmp_path = "7920697396c631989f51a80df0813e86"


@pytest.fixture
def local_tmp_path(tmp_path):
    """create tmp dir with two .xyz files and one .txt file"""
    log.setLevel(logging.DEBUG)
    dotenv.load_dotenv(".testenv")

    content = "some random strings"

    d1 = tmp_path / "from"
    d1.mkdir()

    p1 = d1 / "filename1.xyz"
    p1.write_text(content)

    p2 = d1 / "filename2.xyz"
    p2.write_text(content)

    p3 = d1 / "filename3.txt"
    p3.write_text(content)

    return d1


@pytest.fixture
def local_file_tmp_path(local_tmp_path):
    return local_tmp_path / "filename1.xyz"


@pytest.fixture
def external_tmp_path(tmp_path):
    d2 = tmp_path / "to"
    d2.mkdir()
    return d2


@pytest.fixture
def db_tmp_path():
    return ":memory:"


@pytest.fixture
def simple_worker_with_two_matching_and_one_not_matching(
    db_tmp_path, local_tmp_path, external_tmp_path
):
    worker = simple_worker(
        db_name=db_tmp_path,
        base_directory_from=local_tmp_path,
        base_directory_to=external_tmp_path,
    )

    return worker
