# sage-data-graphs

`sage-data-graphs` packages the graph database resources historically shipped
as SageMath's `graphs` data package.  It has no dependency on Sage and performs
no network access or writes at import or run time.

The distribution contains:

- `graphs.db`, an immutable SQLite database of unlabeled graphs;
- `brouwer_srg_database.json`, the strongly regular graph parameter database;
- `isgci_sage.xml`, the ISGCI graph-class database; and
- `smallgraphs.txt`, the small-graph names used with the ISGCI data.

## Installation

```console
python -m pip install sage-data-graphs
```

## API

Use the resource API when consuming the raw files:

```python
from sage_data_graphs import open_resource, resource, resource_path

with open_resource("smallgraphs.txt", "r") as stream:
    first_line = stream.readline()

# `resource_path` also works when a loader needs a real filesystem path.
with resource_path("isgci_sage.xml") as path:
    print(path)
```

The SQLite helper always opens the bundled database read-only and closes the
connection after the context exits:

```python
from sage_data_graphs import graph_database_connection

with graph_database_connection() as connection:
    rows = connection.execute("SELECT count(*) FROM graph_data").fetchone()[0]
```

The Brouwer JSON data can be decoded with one call:

```python
from sage_data_graphs import load_brouwer_database

records = load_brouwer_database()
```

Only known top-level resource names are accepted.  The package never modifies
its installed resources; applications that download updates should store them
in a separate user-writable location.

## Data provenance and licensing

The Python source and packaging files are provided under GPL-2.0-or-later.
The bundled databases come from several upstream sources and retain their
source-specific terms.  Sage's existing `COPYING.txt` labels `graphs` as
`None (database)`, so the precise redistribution terms must be confirmed with
the data owners before a public PyPI release.  See [DATA_LICENSES.md](DATA_LICENSES.md)
for the provenance currently recorded by Sage.

