"""Unit tests for SEC-03: OELEO_PASSWORD optional when use_password=False."""

from unittest.mock import MagicMock, patch

import pytest

from oeleo.connectors import SSHConnector


@pytest.fixture
def key_ssh_env(monkeypatch):
    monkeypatch.delenv("OELEO_PASSWORD", raising=False)
    monkeypatch.setenv("OELEO_USERNAME", "tester")
    monkeypatch.setenv("OELEO_EXTERNAL_HOST", "localhost")
    monkeypatch.setenv("OELEO_KEY_FILENAME", "/tmp/fake_id_rsa")


@pytest.fixture
def password_ssh_env(monkeypatch):
    monkeypatch.delenv("OELEO_PASSWORD", raising=False)
    monkeypatch.setenv("OELEO_USERNAME", "tester")
    monkeypatch.setenv("OELEO_EXTERNAL_HOST", "localhost")


def test_key_auth_init_without_password(key_ssh_env):
    connector = SSHConnector(
        directory="/tmp/remote",
        use_password=False,
        is_posix=True,
    )
    assert connector.use_password is False
    assert connector.session_password is None


def test_key_auth_connect_uses_key_filename_only(key_ssh_env):
    connector = SSHConnector(
        directory="/tmp/remote",
        use_password=False,
        is_posix=True,
    )
    fake_connection = MagicMock()
    with patch("oeleo.connectors.Connection", return_value=fake_connection) as mock_conn:
        connector.connect()

    mock_conn.assert_called_once_with(
        host="localhost",
        user="tester",
        connect_kwargs={"key_filename": ["/tmp/fake_id_rsa"]},
    )
    assert connector.c is fake_connection
    assert "password" not in mock_conn.call_args.kwargs["connect_kwargs"]


def test_password_auth_init_requires_password(password_ssh_env):
    with pytest.raises(ValueError, match="OELEO_PASSWORD is required when use_password=True"):
        SSHConnector(
            directory="/tmp/remote",
            use_password=True,
            is_posix=True,
        )


def test_password_auth_connect_uses_session_password(monkeypatch):
    monkeypatch.setenv("OELEO_PASSWORD", "secret")
    monkeypatch.setenv("OELEO_USERNAME", "tester")
    monkeypatch.setenv("OELEO_EXTERNAL_HOST", "localhost")

    connector = SSHConnector(
        directory="/tmp/remote",
        use_password=True,
        is_posix=True,
    )
    fake_connection = MagicMock()
    with patch("oeleo.connectors.Connection", return_value=fake_connection) as mock_conn:
        connector.connect()

    mock_conn.assert_called_once_with(
        host="localhost",
        user="tester",
        connect_kwargs={"password": "secret"},
    )
    assert connector.c is fake_connection
