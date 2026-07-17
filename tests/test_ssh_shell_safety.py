"""Unit tests for SEC-01: SSHConnector remote shell quoting (no live SSH)."""

import shlex
from pathlib import PurePosixPath
from unittest.mock import MagicMock

import pytest

from oeleo.connectors import SSHConnector


@pytest.fixture
def ssh_env(monkeypatch):
    monkeypatch.setenv("OELEO_PASSWORD", "secret")
    monkeypatch.setenv("OELEO_USERNAME", "tester")
    monkeypatch.setenv("OELEO_EXTERNAL_HOST", "localhost")


def _connector_with_mock_run(ssh_env, directory="/tmp/remote dest"):
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
    return connector, fake


def test_remote_shell_token_quotes_spaces_and_metacharacters(ssh_env):
    connector = SSHConnector(
        directory="/tmp/safe",
        use_password=True,
        is_posix=True,
    )
    awkward = "/tmp/dir with spaces; rm -rf /"
    quoted = connector._remote_shell_token(awkward)
    assert quoted == shlex.quote(awkward)
    assert quoted.startswith("'") and quoted.endswith("'")
    assert "; rm -rf" in quoted  # still present, but only inside quotes


def test_list_content_quotes_directory_and_glob(ssh_env):
    connector, fake = _connector_with_mock_run(ssh_env, directory="/data/out dir")
    fake.run.return_value.stdout = "/data/out dir/file.txt\n"

    files = connector._list_content("*.txt", max_depth=1, hide=True)

    cmd = fake.run.call_args.args[0]
    assert cmd == (
        f"find {shlex.quote('/data/out dir')} -maxdepth 1 "
        f"-name {shlex.quote('*.txt')}"
    )
    assert files == ["/data/out dir/file.txt"]


def test_list_content_quotes_injection_prone_glob(ssh_env):
    connector, fake = _connector_with_mock_run(ssh_env, directory="/data")
    evil_glob = "*.txt'; echo pwned"

    connector._list_content(evil_glob, max_depth=None, hide=True)

    cmd = fake.run.call_args.args[0]
    assert cmd == (
        f"find {shlex.quote('/data')} -name {shlex.quote(evil_glob)}"
    )
    assert "; echo pwned" not in cmd.replace(shlex.quote(evil_glob), "")


def test_calculate_checksum_quotes_remote_path(ssh_env):
    connector, fake = _connector_with_mock_run(
        ssh_env, directory="/data/my files"
    )
    fake.run.return_value.stdout = "abc123  /data/my files/a b.txt\n"

    checksum = connector.calculate_checksum(PurePosixPath("a b.txt"), hide=True)

    cmd = fake.run.call_args.args[0]
    expected_path = PurePosixPath("/data/my files") / "a b.txt"
    assert cmd == f"md5sum {shlex.quote(str(expected_path))}"
    assert checksum == "abc123"


def test_ensure_remote_dir_quotes_path(ssh_env):
    connector, fake = _connector_with_mock_run(ssh_env, directory="/data")
    remote_dir = PurePosixPath("/data/new dir/sub")

    connector._ensure_remote_dir(remote_dir)

    cmd = fake.run.call_args.args[0]
    assert cmd == f"mkdir -p {shlex.quote(str(remote_dir))}"
