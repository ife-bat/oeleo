import os
import shlex
from pathlib import PurePosixPath

import pytest

from oeleo.connectors import SSHConnector


def _missing_env_vars():
    required = [
        "OELEO_USERNAME",
        "OELEO_EXTERNAL_HOST",
        "OELEO_PASSWORD",
    ]
    return [key for key in required if not os.getenv(key)]


def _run_quoted(connector, template, *parts, **kwargs):
    """Run a remote command with each path-like part shell-quoted."""
    quoted = [shlex.quote(str(p)) for p in parts]
    return connector.c.run(template.format(*quoted), **kwargs)


@pytest.fixture(scope="module")
def ssh_remote_dir():
    if os.getenv("OELEO_SSH_TESTS") != "1":
        pytest.skip("Set OELEO_SSH_TESTS=1 to enable SSH integration tests.")

    missing = _missing_env_vars()
    if missing:
        pytest.skip(f"Missing SSH env vars: {', '.join(missing)}")

    setup_connector = SSHConnector(
        directory="/tmp",
        use_password=True,
        is_posix=True,
    )
    setup_connector.connect()
    base_dir = None
    try:
        result = setup_connector.c.run("mktemp -d", hide=True, in_stream=False)
        base_dir = result.stdout.strip()

        _run_quoted(
            setup_connector,
            "mkdir -p {}/sub",
            base_dir,
            hide=True,
            in_stream=False,
        )
        _run_quoted(
            setup_connector,
            "printf 'root' > {}/root.txt",
            base_dir,
            hide=True,
            in_stream=False,
        )
        _run_quoted(
            setup_connector,
            "printf 'nested' > {}/sub/nested.txt",
            base_dir,
            hide=True,
            in_stream=False,
        )

        yield base_dir
    finally:
        if base_dir:
            _run_quoted(
                setup_connector,
                "rm -rf {}",
                base_dir,
                warn=True,
                hide=True,
                in_stream=False,
            )
        setup_connector.close()


@pytest.mark.ssh
def test_ssh_connector_no_subdirs(ssh_remote_dir):
    connector = SSHConnector(
        directory=ssh_remote_dir,
        use_password=True,
        is_posix=True,
        include_subdirs=False,
    )
    connector.connect()
    try:
        files = connector.base_filter_sub_method(".txt")
        file_names = {f.name for f in files}
        assert "root.txt" in file_names
        assert "nested.txt" not in file_names
    finally:
        connector.close()


@pytest.mark.ssh
def test_ssh_connector_with_subdirs(ssh_remote_dir):
    connector = SSHConnector(
        directory=ssh_remote_dir,
        use_password=True,
        is_posix=True,
        include_subdirs=True,
    )
    connector.connect()
    try:
        files = connector.base_filter_sub_method(".txt")
        file_names = {f.name for f in files}
        assert "root.txt" in file_names
        assert "nested.txt" in file_names
    finally:
        connector.close()


@pytest.mark.ssh
def test_ssh_connector_creates_missing_remote_dirs(ssh_remote_dir, tmp_path):
    connector = SSHConnector(
        directory=ssh_remote_dir,
        use_password=True,
        is_posix=True,
        include_subdirs=True,
    )
    connector.connect()
    try:
        local_file = tmp_path / "local.txt"
        local_file.write_text("hello")

        remote_dir = PurePosixPath(ssh_remote_dir) / "newdir"
        remote_file = remote_dir / "local.txt"

        _run_quoted(
            connector,
            "rm -rf {}",
            remote_dir,
            hide=True,
            in_stream=False,
            warn=True,
        )

        success = connector.move_func(local_file, remote_file)
        assert success is True

        result = _run_quoted(
            connector,
            "test -f {}",
            remote_file,
            hide=True,
            in_stream=False,
            warn=True,
        )
        assert result.ok
    finally:
        connector.close()


@pytest.mark.ssh
def test_ssh_connector_handles_spaces_in_remote_path(ssh_remote_dir, tmp_path):
    connector = SSHConnector(
        directory=ssh_remote_dir,
        use_password=True,
        is_posix=True,
        include_subdirs=True,
    )
    connector.connect()
    try:
        local_file = tmp_path / "spaced name.txt"
        local_file.write_text("hello spaces")

        remote_dir = PurePosixPath(ssh_remote_dir) / "dir with spaces"
        remote_file = remote_dir / "spaced name.txt"

        _run_quoted(
            connector,
            "rm -rf {}",
            remote_dir,
            hide=True,
            in_stream=False,
            warn=True,
        )

        success = connector.move_func(local_file, remote_file)
        assert success is True

        checksum = connector.calculate_checksum(
            PurePosixPath("dir with spaces") / "spaced name.txt"
        )
        assert isinstance(checksum, str) and len(checksum) == 32

        files = connector.base_filter_sub_method(".txt")
        assert any(f.name == "spaced name.txt" for f in files)

        result = _run_quoted(
            connector,
            "test -f {}",
            remote_file,
            hide=True,
            in_stream=False,
            warn=True,
        )
        assert result.ok
    finally:
        connector.close()
