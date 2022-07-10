import pytest
import logging
import os
from pathlib import Path

import dotenv

from oeleo.utils import logger
from oeleo.workers import simple_worker
from oeleo.schedulers import RichScheduler, SimpleScheduler

log = logger()


@pytest.fixture
def simple_worker_with_two_matching_and_one_not_matching(tmp_path):
    log.setLevel(logging.DEBUG)
    dotenv.load_dotenv(".testenv")

    content = "some random strings"

    d1 = tmp_path / "from"
    d2 = tmp_path / "to"
    d1.mkdir()
    d2.mkdir()

    p1 = d1 / "filename1.xyz"
    p1.write_text(content)

    p2 = d1 / "filename2.xyz"
    p2.write_text(content)

    p3 = d1 / "filename3.txt"
    p3.write_text(content)

    db_name = ":memory:"

    worker = simple_worker(
        db_name=db_name,
        base_directory_from=d1,
        base_directory_to=d2,
    )

    return worker
