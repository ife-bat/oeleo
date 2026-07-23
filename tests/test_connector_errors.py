"""Unit tests for REL-02: connector list/checksum failures raise typed errors."""

from pathlib import Path, PurePosixPath
from unittest.mock import MagicMock

import pytest
from shareplum.errors import ShareplumRequestError

from oeleo.connectors import (
    OeleoConnectionError,
    OeleoTransferError,
    SharePointConnector,
    SSHConnector,
)
from oeleo.workers import Worker


@pytest.fixture
def ssh_env(monkeypatch):
    monkeypatch.setenv("OELEO_PASSWORD", "secret")
    monkeypatch.setenv("OELEO_USERNAME", "tester")
    monkeypatch.setenv("OELEO_EXTERNAL_HOST", "localhost")


def _connector_with_mock_run(ssh_env, directory="/tmp/remote"):
    connector = SSHConnector(
        directory=directory,
        use_password=True,
        is_posix=True,
    )
    fake = MagicMock()
    result = MagicMock()
    result.ok = True
    result.stdout = ""
    fake.run.return_value = result
    connector.c = fake
    return connector, fake, result


def test_list_content_raises_when_result_not_ok(ssh_env):
    connector, fake, result = _connector_with_mock_run(ssh_env)
    result.ok = False
    result.stdout = "permission denied"

    with pytest.raises(OeleoConnectionError, match="Failed to list remote content"):
        connector._list_content("*.txt", max_depth=1, hide=True)

    fake.run.assert_called_once()


def test_list_content_raises_on_fabric_exception(ssh_env):
    connector, fake, _result = _connector_with_mock_run(ssh_env)
    fake.run.side_effect = RuntimeError("transport down")

    with pytest.raises(OeleoConnectionError, match="Failed to list remote content"):
        connector._list_content("*.txt", max_depth=1, hide=True)


def test_list_content_empty_success_returns_empty_list(ssh_env):
    connector, _fake, result = _connector_with_mock_run(ssh_env)
    result.ok = True
    result.stdout = "\n"

    assert connector._list_content("*.txt", max_depth=1, hide=True) == []


def test_calculate_checksum_raises_when_result_not_ok(ssh_env):
    connector, _fake, result = _connector_with_mock_run(ssh_env)
    result.ok = False
    result.stdout = ""

    with pytest.raises(OeleoTransferError, match="Failed to calculate checksum"):
        connector.calculate_checksum(PurePosixPath("a.txt"), hide=True)


def test_calculate_checksum_raises_on_empty_stdout(ssh_env):
    connector, _fake, result = _connector_with_mock_run(ssh_env)
    result.ok = True
    result.stdout = "   \n"

    with pytest.raises(OeleoTransferError, match="empty output"):
        connector.calculate_checksum(PurePosixPath("a.txt"), hide=True)


def test_calculate_checksum_raises_on_fabric_exception(ssh_env):
    connector, fake, _result = _connector_with_mock_run(ssh_env)
    fake.run.side_effect = RuntimeError("broken pipe")

    with pytest.raises(OeleoTransferError, match="Failed to calculate checksum"):
        connector.calculate_checksum(PurePosixPath("a.txt"), hide=True)


def test_sharepoint_calculate_checksum_raises_instead_of_false():
    connector = SharePointConnector.__new__(SharePointConnector)
    folder = MagicMock()
    folder.get_file.side_effect = ShareplumRequestError("nope", "403")
    connector.connection = MagicMock(folder=folder)

    with pytest.raises(OeleoTransferError, match="Failed to calculate checksum"):
        connector.calculate_checksum(Path("missing.txt"))


def _worker_for_check(tmp_path):
    local = MagicMock()
    local.directory = tmp_path / "from"
    local.directory.mkdir(exist_ok=True)

    external = MagicMock()
    external.directory = tmp_path / "to"
    external.directory.mkdir(exist_ok=True)

    bookkeeper = MagicMock()
    checker = MagicMock()
    reporter = MagicMock()
    reporter.should_die.return_value = False
    # progress() context manager used by check()
    progress = MagicMock()
    progress.add_task.return_value = 1
    reporter.progress.return_value.__enter__.return_value = progress
    reporter.progress.return_value.__exit__.return_value = None

    worker = Worker(
        checker=checker,
        bookkeeper=bookkeeper,
        local_connector=local,
        external_connector=external,
        reporter=reporter,
    )
    return worker, external, checker, reporter


def test_check_aborts_and_notifies_when_external_list_fails(tmp_path):
    worker, external, checker, reporter = _worker_for_check(tmp_path)
    f = tmp_path / "from" / "a.xyz"
    f.write_text("data")
    worker.file_names = [f]
    external.base_filter_sub_method.side_effect = OeleoConnectionError("list failed")

    with pytest.raises(OeleoConnectionError, match="list failed"):
        worker.check()

    reporter.notify.assert_called()
    checker.check.assert_not_called()


def test_check_continues_after_external_checksum_transfer_error(tmp_path):
    worker, external, checker, reporter = _worker_for_check(tmp_path)
    f = tmp_path / "from" / "a.xyz"
    f.write_text("data")
    worker.file_names = [f]
    worker.make_external_name = MagicMock()
    worker.external_name = Path("a.xyz")
    external.base_filter_sub_method.return_value = [Path("a.xyz")]
    checker.check.side_effect = [
        {"checksum": "local"},
        OeleoTransferError("md5 failed"),
    ]

    worker.check(update_db=True)

    reporter.notify.assert_called()
    worker.bookkeeper.update_record.assert_not_called()
    assert worker.number_of_duplicates_out_of_sync == 1


def test_process_file_notifies_on_checksum_transfer_error(tmp_path):
    worker, _external, checker, reporter = _worker_for_check(tmp_path)
    f = tmp_path / "from" / "a.xyz"
    f.write_text("data")
    checker.check.side_effect = OeleoTransferError("md5 failed")

    result = worker._process_file(f)

    assert result == f
    reporter.notify.assert_called()
