from __future__ import annotations

import hashlib
import sqlite3
import xml.etree.ElementTree as ET

import pytest

from sage_data_graphs import (
    DATA_FILES,
    graph_database_connection,
    load_brouwer_database,
    open_resource,
    resource,
    resource_path,
)


EXPECTED_SHA256 = {
    "brouwer_srg_database.json": "7a8bb447211c6072481b1eb1c5ea3311691d6f0fb726909d63c5c9d8032d43c3",
    "graphs.db": "d4e9a45f4d9d71c4721e9e4d3adfd5367a488f6e51477f8eec3398e0624dd333",
    "isgci_sage.xml": "653990bea56ea7de39b554b6680cc1dac9d83467e2896965c5477c90c5667c50",
    "smallgraphs.txt": "d0f57d3d2cfc865ce5d59998a815c1a4cb5ec2e4d6b75bbfc3cb5775b2a20448",
}


def test_expected_resources_and_hashes() -> None:
    assert set(DATA_FILES) == set(EXPECTED_SHA256)
    for name, expected in EXPECTED_SHA256.items():
        with open_resource(name) as stream:
            assert hashlib.sha256(stream.read()).hexdigest() == expected


def test_resource_names_are_restricted() -> None:
    assert resource("graphs.db").name == "graphs.db"
    with pytest.raises(ValueError, match="unknown graph data resource"):
        resource("../graphs.db")
    with pytest.raises(ValueError, match="mode must"):
        open_resource("graphs.db", "wb")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="encoding"):
        open_resource("graphs.db", encoding="utf-8")


def test_resource_path_exists_inside_context() -> None:
    with resource_path("isgci_sage.xml") as path:
        assert path.is_file()
        assert path.name == "isgci_sage.xml"


def test_sqlite_database_integrity_shape_and_read_only_mode() -> None:
    expected_tables = {"aut_grp", "degrees", "graph_data", "misc", "spectrum"}
    with graph_database_connection() as connection:
        tables = {
            row[0]
            for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            )
        }
        assert tables == expected_tables
        assert connection.execute("PRAGMA integrity_check").fetchone() == ("ok",)
        assert connection.execute("PRAGMA query_only").fetchone() == (1,)
        for table in sorted(expected_tables):
            count = connection.execute(f'SELECT count(*) FROM "{table}"').fetchone()
            assert count == (1252,)
        with pytest.raises(sqlite3.OperationalError):
            connection.execute("CREATE TABLE must_not_be_created (value INTEGER)")


def test_brouwer_json_is_readable() -> None:
    records = load_brouwer_database()
    assert len(records) == 4538
    assert records[0][:5] == [5, 2, 0, 1, "exists"]
    assert records[-1][:5] == [1300, 867, 578, 578, "open"]


def test_isgci_xml_is_readable() -> None:
    with open_resource("isgci_sage.xml") as stream:
        root = ET.parse(stream).getroot()
    assert root.tag == "ISGCI"
    stats = root.find("stats")
    assert stats is not None
    assert stats.attrib["nodes"] == "1461"


def test_smallgraphs_text_is_readable() -> None:
    with open_resource("smallgraphs.txt", "r") as stream:
        lines = stream.readlines()
    assert len(lines) == 565
    assert lines[0].startswith("A \\cup K_1\t")
    assert all("\t" in line for line in lines)
