"""Unit tests for dump_db CSV/JSON export (#41)."""

import csv
import io
import json
from pathlib import Path

import pytest

from oeleo.models import FileList, SimpleDbHandler
from oeleo.utils import dump_bookkeeper, dump_db


def _seed_db(db_path: Path) -> SimpleDbHandler:
    bookkeeper = SimpleDbHandler(str(db_path))
    bookkeeper.initialize_db()
    FileList.create(
        local_name="a.xyz",
        external_name="/to/a.xyz",
        checksum="aaa",
        code=0,
    )
    FileList.create(
        local_name="b.xyz",
        external_name="/to/b.xyz",
        checksum="bbb",
        code=1,
    )
    FileList.create(
        local_name="c.xyz",
        external_name="/to/c.xyz",
        checksum="ccc",
        code=2,
    )
    return bookkeeper


def test_dump_bookkeeper_csv_and_json(tmp_path):
    db_path = tmp_path / "book.db"
    bookkeeper = _seed_db(db_path)

    csv_text = dump_bookkeeper(bookkeeper, output_format="csv")
    assert csv_text is not None
    rows = list(csv.DictReader(io.StringIO(csv_text)))
    assert [r["local_name"] for r in rows] == ["a.xyz", "b.xyz", "c.xyz"]
    assert rows[0]["checksum"] == "aaa"
    assert rows[1]["code"] == "1"
    assert "id" in rows[0]
    assert "processed_date" in rows[0]

    json_text = dump_bookkeeper(bookkeeper, output_format="json")
    data = json.loads(json_text)
    assert len(data) == 3
    assert data[2]["local_name"] == "c.xyz"
    assert data[2]["code"] == 2


def test_dump_bookkeeper_code_filter_and_output_path(tmp_path):
    db_path = tmp_path / "book.db"
    bookkeeper = _seed_db(db_path)
    out = tmp_path / "locked.json"

    text = dump_bookkeeper(
        bookkeeper, code=2, output_format="json", output=out
    )
    data = json.loads(text)
    assert len(data) == 1
    assert data[0]["local_name"] == "c.xyz"
    assert out.read_text(encoding="utf-8") == text


def test_dump_bookkeeper_human_returns_none(tmp_path):
    bookkeeper = _seed_db(tmp_path / "book.db")
    assert dump_bookkeeper(bookkeeper, output_format="human") is None


def test_dump_bookkeeper_rejects_unknown_format(tmp_path):
    bookkeeper = _seed_db(tmp_path / "book.db")
    with pytest.raises(ValueError, match="unsupported output_format"):
        dump_bookkeeper(bookkeeper, output_format="xml")


def test_dump_db_csv_roundtrip(tmp_path):
    db_path = tmp_path / "book.db"
    bookkeeper = _seed_db(db_path)
    bookkeeper.db_instance.close()

    text = dump_db(db_name=str(db_path), output_format="csv")
    rows = list(csv.DictReader(io.StringIO(text)))
    assert len(rows) == 3
