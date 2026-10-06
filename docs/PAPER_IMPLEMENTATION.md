# Paper-to-Implementation Mapping

This document maps the manuscript **Knowledge Graph-Based Legal Chain Reasoning for Industrial Safety Decision Support** to the public repository.

## Research framework

The manuscript pipeline is implemented as:

```text
Legal source collection and preprocessing
        ↓
Document / Annex / Reasoning graph construction
        ↓
Provenance linking
        ↓
Query feature extraction and hybrid retrieval
        ↓
Evidence Pack assembly
        ↓
Legal Chain construction
        ↓
Citation and claim checking
        ↓
Evidence-grounded answer
```

## Component mapping

| Manuscript concept | Repository location | Role |
|---|---|---|
| Document Graph | `knowledge_graph/document_graph/nodes/`, `knowledge_graph/document_graph/edges/` | Preserves statutory hierarchy and references |
| Annex Graph | `knowledge_graph/document_graph/source_annex/` | Represents annex/form structure, logical rows/cells, notes, and article links |
| Reasoning Graph | `knowledge_graph/reasoning_graph/nodes/`, `knowledge_graph/reasoning_graph/edges/` | Stores rules, requirements, thresholds, exceptions, temporal conditions, entities, and related-rule links |
| Provenance Layer | source-anchor fields, `edges_rule_source.csv`, and loader-generated `EXTRACTED_FROM`, `RESOLVES_TO`, `ITEM_RESOLVES_TO` relations | Traces reasoning units back to source text |
| Hybrid Retrieval | `app/graph_rag_pipeline/graph_query_layer.py` | Retrieves document, annex, reasoning, and provenance evidence |
| Evidence Pack | `app/graph_rag_pipeline/evidence_pack_assembler.py` | Normalizes retrieved evidence into a structured evidence bundle |
| Legal Chain | Evidence Pack / answer-generation pipeline | Connects obligation → detailed requirement → legal consequence |
| Citation formatting | `app/graph_rag_pipeline/citation_formatter.py` | Formats traceable statutory references |
| Claim checking | `app/graph_rag_pipeline/claim_check.py` | Rule-based evidence sufficiency and answerability checks |
| Answer generation | `app/graph_rag_pipeline/answer_generator.py` | Produces evidence-grounded, structured responses |
| API layer | `app/graph_rag_pipeline/ask_adapter.py` | Exposes the local backend |
| Graph loading | `scripts/load_neo4j_graph.py` | Reconstructs the Neo4j graph from repository CSV artifacts |

## Evaluation mapping

The manuscript evaluates 42 case-based industrial-safety scenarios derived from 33 criminal precedents and 9 administrative adjudications. Repository evaluation artifacts are under `evaluation/`, while the broader raw case source collection is under `data/raw_cases/`.

The manuscript-facing quantitative summary is maintained in `docs/EVALUATION.md`.

## Publication metadata

Journal, volume/issue/pages, DOI, publisher link, final BibTeX, and `CITATION.cff` are intentionally left pending and will be added upon publication.
