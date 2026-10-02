# Bundled data provenance and licensing

This file records the provenance available in SageMath's
`build/pkgs/graphs/SPKG.rst`.  It is not a declaration that every bundled data
file is covered by the GPL license in this repository.

## `graphs.db`

Sage describes this as a database of combinatorial graphs created by Emily
Kirkman based on the work of Jason Grout.  The original graph-database project is available at:

- <https://github.com/jasongrout/graph_database>

## `isgci_sage.xml` and `smallgraphs.txt`

These files accompany the Information System on Graph Classes and their
Inclusions (ISGCI) data.  Sage records the following upstream contact:

- H. N. de Ridder, `hnridder@graphclasses.org`
- <https://www.graphclasses.org/>

## `brouwer_srg_database.json`

Sage records that the underlying data comes from Andries E. Brouwer's website:

- <https://aeb.win.tue.nl/>
- data contact: Andries E. Brouwer, `aeb@cwi.nl`

The parser used to create the JSON file is available at:

- <https://github.com/sagemath/strongly_regular_graphs_database>

## Release blocker

Sage's top-level `COPYING.txt` currently lists the `graphs` component's license
as **`None (database)`**.  No more specific license statements were present in
the source archive used to create this repository.  Before publishing this
distribution to PyPI, obtain or locate explicit redistribution terms for each
of the four files above and update this document and the package metadata as
needed.  In particular, the GPL-2.0-or-later license for the Python code and
packaging must not be assumed to relicense the bundled data.

