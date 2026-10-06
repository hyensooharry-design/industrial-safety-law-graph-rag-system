# Legal Knowledge Graph Schema

The manuscript defines three functional graphs and one provenance layer: **Document Graph**, **Annex Graph**, **Reasoning Graph**, and **Provenance Layer**.

## Document Graph

The Document Graph preserves the formal hierarchy of statutory text.

| Node type | Count reported in manuscript |
|---|---:|
| Law | 6 |
| Heading | 194 |
| Article | 1,270 |
| Paragraph | 2,567 |
| Subparagraph | 2,957 |
| Item | 513 |
| Addendum | 81 |

The repository stores these artifacts primarily under:

```text
knowledge_graph/document_graph/nodes/
knowledge_graph/document_graph/edges/
```

The main hierarchical relation is `CONTAINS`, with additional statutory reference relationships represented in the source artifacts.

## Annex Graph

The Annex Graph represents statutory annexes and forms as structured table-like evidence.

| Node type | Count reported in manuscript |
|---|---:|
| Annex | 201 |
| LogicalRow | 7,972 |
| LogicalCell | 16,741 |
| AnnexNote | 119 |

Key relationships include `HAS_LOGICAL_ROW`, `HAS_LOGICAL_CELL`, `HAS_NOTE`, and links between annexes and statutory articles.

The current source artifacts are stored under:

```text
knowledge_graph/document_graph/source_annex/
```

This path reflects the preprocessing origin of the annex data; conceptually, these files correspond to the manuscript's **Annex Graph**.

## Reasoning Graph

The Reasoning Graph represents legal meaning units used for retrieval and decision support.

| Node type | Count reported in manuscript |
|---|---:|
| Rule | 8,858 |
| Requirement | 3,639 |
| Threshold | 1,782 |
| Exception | 647 |
| TemporalRule | 227 |
| EntityType | 586 |
| ListItem | 3,604 |

Key relationships include `HAS_REQUIREMENT`, `HAS_THRESHOLD`, `HAS_EXCEPTION`, `HAS_TEMPORAL_CONDITION`, `RELATED_ENTITY`, `HAS_LIST_ITEM`, and `RELATED_RULE`.

Artifacts are stored under:

```text
knowledge_graph/reasoning_graph/nodes/
knowledge_graph/reasoning_graph/edges/
```

## Provenance Layer

The Provenance Layer links extracted legal reasoning units back to concrete source text.

The manuscript reports:

| Provenance element | Count |
|---|---:|
| SourceNode | 8,858 |
| EXTRACTED_FROM | 8,858 |
| RESOLVES_TO | 8,858 |
| ITEM_RESOLVES_TO | 3,604 |

The loader reconstructs provenance relations using source-anchor information from the graph artifacts. In particular:

- `EXTRACTED_FROM` links a `Rule` to a `SourceNode`.
- `RESOLVES_TO` links a `SourceNode` to a concrete document or annex node.
- `ITEM_RESOLVES_TO` links `ListItem` evidence to a concrete source anchor.

See `scripts/load_neo4j_graph.py` for the executable graph-loading definition.
