# Knowledge Graph Artifacts

This directory contains the graph artifacts underlying the manuscript's Legal Graph-RAG framework.

The paper defines four conceptual components:

| Manuscript component | Current artifact location |
|---|---|
| Document Graph | `document_graph/nodes/`, `document_graph/edges/` |
| Annex Graph | `document_graph/source_annex/` |
| Reasoning Graph | `reasoning_graph/nodes/`, `reasoning_graph/edges/` |
| Provenance Layer | source-anchor fields and provenance relations reconstructed by `scripts/load_neo4j_graph.py` |

Additional Neo4j load artifacts, retrieval evaluations, development reports, and visual examples are retained in this directory for reproducibility and inspection.

The `source_annex` folder name is retained because it is part of the original preprocessing artifact layout. In the manuscript, these artifacts are treated as the **Annex Graph**.

See `../docs/GRAPH_SCHEMA.md` for the manuscript-level schema and node/edge counts.
