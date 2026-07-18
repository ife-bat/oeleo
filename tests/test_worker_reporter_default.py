"""Unit tests for ARCH-02/03: Worker reporter default_factory and Protocol import."""

import oeleo.workers as workers_mod
from oeleo.checkers import ChecksumChecker
from oeleo.connectors import LocalConnector
from oeleo.models import SimpleDbHandler
from oeleo.workers import Worker


def test_protocol_imported_from_typing():
    assert workers_mod.Protocol is __import__("typing").Protocol


def _make_worker(db_tmp_path, local_tmp_path, external_tmp_path):
    return Worker(
        checker=ChecksumChecker(),
        bookkeeper=SimpleDbHandler(db_tmp_path),
        local_connector=LocalConnector(directory=local_tmp_path),
        external_connector=LocalConnector(directory=external_tmp_path),
    )


def test_workers_do_not_share_default_reporter(
    db_tmp_path, local_tmp_path, external_tmp_path
):
    w1 = _make_worker(db_tmp_path, local_tmp_path, external_tmp_path)
    w2 = _make_worker(db_tmp_path, local_tmp_path, external_tmp_path)
    assert w1.reporter is not w2.reporter


def test_worker_dataclass_field_uses_default_factory():
    field_obj = Worker.__dataclass_fields__["reporter"]
    assert field_obj.default_factory is workers_mod.Reporter
