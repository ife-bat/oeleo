"""Unit tests for BUG-06: remove broken SharePoint reconnect / __delete__ hooks."""

import oeleo.connectors as connectors


def test_sharepoint_connection_has_no_reconnect():
    assert not hasattr(connectors.SharePointConnection, "reconnect")


def test_connectors_have_no_delete_hooks():
    assert not hasattr(connectors.SSHConnector, "__delete__")
    assert not hasattr(connectors.SharePointConnector, "__delete__")
    assert not hasattr(connectors.LocalConnector, "__delete__")
