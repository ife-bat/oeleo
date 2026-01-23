import os
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

        setup_connector.c.run(
            f"mkdir -p {base_dir}/sub", hide=True, in_stream=False
        )
        setup_connector.c.run(
            f"printf 'root' > {base_dir}/root.txt", hide=True, in_stream=False
        )
        setup_connector.c.run(
            f"printf 'nested' > {base_dir}/sub/nested.txt",
            hide=True,
            in_stream=False,
        )

        yield base_dir
    finally:
        if base_dir:
            setup_connector.c.run(
                f"rm -rf {base_dir}",
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

        connector.c.run(
            f"rm -rf {remote_dir}",
            hide=True,
            in_stream=False,
            warn=True,
        )

        success = connector.move_func(local_file, remote_file)
        assert success is True

        result = connector.c.run(
            f"test -f {remote_file}",
            hide=True,
            in_stream=False,
            warn=True,
        )
        assert result.ok
    finally:
        connector.close()