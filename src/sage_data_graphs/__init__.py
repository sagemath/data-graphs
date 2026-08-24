"""Read-only access to the graph data resources distributed by this package."""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from importlib.resources import as_file, files
import json
from pathlib import Path
import sqlite3
from typing import IO, Any, Literal, Optional, overload

__all__ = [
    "DATA_FILES",
    "__version__",
    "graph_database_connection",
    "load_brouwer_database",
    "open_resource",
    "resource",
    "resource_path",
]

__version__ = "20210214.0"

DATA_FILES = (
    "brouwer_srg_database.json",
    "graphs.db",
    "isgci_sage.xml",
    "smallgraphs.txt",
)

_DATA_PACKAGE = "sage_data_graphs.data"
_TEXT_ENCODINGS = {
    "brouwer_srg_database.json": "utf-8",
    "isgci_sage.xml": "iso-8859-1",
    "smallgraphs.txt": "utf-8",
}


def resource(name: str) -> Any:
    """Return the package resource named *name*.

    Only the four documented top-level filenames are accepted.  Restricting
    names prevents accidental path traversal and makes the public data surface
    explicit.
    """

    if name not in DATA_FILES:
        choices = ", ".join(DATA_FILES)
        raise ValueError(f"unknown graph data resource {name!r}; choose from {choices}")
    return files(_DATA_PACKAGE).joinpath(name)


@overload
def open_resource(
    name: str, mode: Literal["rb"] = "rb", *, encoding: None = None
) -> IO[bytes]: ...


@overload
def open_resource(
    name: str, mode: Literal["r"], *, encoding: Optional[str] = None
) -> IO[str]: ...


def open_resource(
    name: str,
    mode: Literal["r", "rb"] = "rb",
    *,
    encoding: Optional[str] = None,
) -> IO[Any]:
    """Open a bundled resource for reading.

    Binary mode is the default.  Text mode uses the resource's known encoding
    unless *encoding* is supplied explicitly.  Write and update modes are not
    supported.
    """

    item = resource(name)
    if mode == "rb":
        if encoding is not None:
            raise ValueError("encoding is only valid in text mode")
        return item.open("rb")
    if mode == "r":
        selected_encoding = encoding or _TEXT_ENCODINGS.get(name, "utf-8")
        return item.open("r", encoding=selected_encoding)
    raise ValueError("mode must be 'r' or 'rb'")


@contextmanager
def resource_path(name: str) -> Iterator[Path]:
    """Yield a filesystem path for a bundled resource.

    The path is only guaranteed to remain valid for the duration of the
    context, which also supports importers that must extract resources.
    """

    with as_file(resource(name)) as path:
        yield path


@contextmanager
def graph_database_connection() -> Iterator[sqlite3.Connection]:
    """Yield a read-only connection to the bundled ``graphs.db`` database."""

    with resource_path("graphs.db") as database_path:
        uri = f"{database_path.resolve().as_uri()}?mode=ro&immutable=1"
        connection = sqlite3.connect(uri, uri=True)
        try:
            connection.execute("PRAGMA query_only = ON")
            yield connection
        finally:
            connection.close()


def load_brouwer_database() -> list[list[Any]]:
    """Decode and return the records in ``brouwer_srg_database.json``."""

    with open_resource("brouwer_srg_database.json", "r") as stream:
        data = json.load(stream)
    if not isinstance(data, list):
        raise ValueError("Brouwer database must contain a JSON list")
    return data
