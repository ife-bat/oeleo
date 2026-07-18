"""Unit tests for BUG-05: register_password sets provided password."""

import os
from unittest.mock import patch

from oeleo.connectors import register_password


def test_register_password_sets_provided_pwd(monkeypatch):
    monkeypatch.delenv("OELEO_PASSWORD", raising=False)
    register_password("from-arg")
    assert os.environ["OELEO_PASSWORD"] == "from-arg"


def test_register_password_prompts_when_none(monkeypatch):
    monkeypatch.delenv("OELEO_PASSWORD", raising=False)
    with patch("oeleo.connectors.getpass.getpass", return_value="from-prompt") as mock_getpass:
        register_password(None)
    mock_getpass.assert_called_once_with(prompt="Password: ")
    assert os.environ["OELEO_PASSWORD"] == "from-prompt"


def test_register_password_overwrites_existing(monkeypatch):
    monkeypatch.setenv("OELEO_PASSWORD", "old")
    register_password("new")
    assert os.environ["OELEO_PASSWORD"] == "new"
