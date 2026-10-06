# Knowledge Graph-Based Legal Chain Reasoning for Industrial Safety Decision Support

**산업안전 의사결정 지원을 위한 법령 지식 그래프 기반 Legal Chain 추론**

Research implementation for the manuscript by **Hyeonsu Jeong, Hyemin Koo, Seyoung Park, and Seonghyeon Moon**.

> **Publication status:** publication-specific metadata is not yet included. Journal, volume/issue/pages, DOI, final publisher link, and `CITATION.cff` will be added upon publication.

## Overview

Industrial safety statutes contain hierarchical structures, cross-references, subordinate regulations, annexes, and legal consequences that are difficult to represent with document-level retrieval alone. This repository implements a domain-specific **Legal Graph-RAG** framework that connects statutory structure, semantic legal rules, source provenance, and case-relevant evidence.

The framework is designed around four graph components:

- **Document Graph** — preserves statutory hierarchy such as law, heading, article, paragraph, subparagraph/item, and addendum.
- **Annex Graph** — represents annexes, forms, logical rows/cells, notes, and their links to statutory provisions.
- **Reasoning Graph** — represents legal reasoning units such as obligations, prohibitions, requirements, thresholds, exceptions, temporal conditions, entities, and related rules.
- **Provenance Layer** — links extracted reasoning units back to their original statutory or annex evidence.

Retrieved evidence is normalized into an **Evidence Pack**, and case-relevant legal grounds are organized as a **Legal Chain**:

```text
User / Case Query
      ↓
Hybrid Graph Retrieval
      ↓
Evidence Pack
      ↓
Obligation
      ↓
Detailed Requirement
      ↓
Legal Consequence
      ↓
Evidence-grounded Answer
```

The implementation focuses on traceable legal evidence rather than unconstrained legal text generation.

## Manuscript Scope

The manuscript focuses on the Korean **Occupational Safety and Health Act** and the **Serious Accidents Punishment Act**, together with relevant subordinate regulations, safety standards, annexes, and forms.

The evaluation uses **42 industrial-safety legal scenarios**:

| Scenario source | Cases |
|---|---:|
| Criminal precedent-based scenarios | 33 |
| Administrative adjudication-based scenarios | 9 |
| **Total** | **42** |

The reported F1-scores for direct legal-reference selection are:

| Reference level | F1-score |
|---|---:|
| Article | **0.737** |
| Paragraph | **0.715** |
| Subparagraph / Item | **0.607** |

See [`docs/EVALUATION.md`](docs/EVALUATION.md) for the manuscript-facing evaluation summary.

## Repository Structure

```text
.
├── README.md
├── requirements.txt
├── .env.example
├── app/
│   └── graph_rag_pipeline/
│       ├── ask_adapter.py
│       ├── graph_query_layer.py
│       ├── evidence_pack_assembler.py
│       ├── answer_generator.py
│       ├── citation_formatter.py
│       ├── claim_check.py
│       ├── extractors/
│       └── llm/
├── knowledge_graph/
│   ├── document_graph/
│   ├── reasoning_graph/
│   ├── neo4j_load/
│   ├── retrieval_evaluation/
│   └── visual_examples/
├── evaluation/
├── data/
│   └── raw_cases/
├── frontend/
├── scripts/
│   └── load_neo4j_graph.py
└── docs/
    ├── PAPER_IMPLEMENTATION.md
    ├── GRAPH_SCHEMA.md
    ├── EVALUATION.md
    ├── RUNNING.md
    └── NEO4J_LOAD.md
```

The paper's **Annex Graph** artifacts are stored under `knowledge_graph/document_graph/source_annex/`. The **Provenance Layer** is reconstructed from source-anchor information and provenance relationships during Neo4j loading. See [`knowledge_graph/README.md`](knowledge_graph/README.md) and [`docs/GRAPH_SCHEMA.md`](docs/GRAPH_SCHEMA.md).

## Paper-to-Code Mapping

| Manuscript component | Repository implementation |
|---|---|
| Query analysis and hybrid graph retrieval | `app/graph_rag_pipeline/graph_query_layer.py` |
| Evidence Pack construction | `app/graph_rag_pipeline/evidence_pack_assembler.py` |
| Legal Chain / answer assembly | `app/graph_rag_pipeline/answer_generator.py` |
| Citation construction | `app/graph_rag_pipeline/citation_formatter.py` |
| Evidence sufficiency / claim checking | `app/graph_rag_pipeline/claim_check.py` |
| API entrypoint | `app/graph_rag_pipeline/ask_adapter.py` |
| Neo4j graph reconstruction | `scripts/load_neo4j_graph.py` |

A more detailed mapping is available in [`docs/PAPER_IMPLEMENTATION.md`](docs/PAPER_IMPLEMENTATION.md).

## Quick Start

Python 3.10+, Neo4j 5.x, Node.js, and npm are recommended.

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

Create a local environment file from `.env.example`, then configure the Neo4j connection and any model/API credentials required by your local setup.

Verify the graph artifacts before loading:

```bash
python scripts/load_neo4j_graph.py --dry-run
```

Load the graph:

```bash
python scripts/load_neo4j_graph.py
```

Run the backend:

```bash
python -m uvicorn graph_rag_pipeline.ask_adapter:app --app-dir app --host 127.0.0.1 --port 8000
```

Run the frontend:

```bash
cd frontend
npm ci
npm run dev
```

For detailed instructions, see [`docs/RUNNING.md`](docs/RUNNING.md) and [`docs/NEO4J_LOAD.md`](docs/NEO4J_LOAD.md).

## Evaluation Artifacts

The public repository retains the case-scenario evaluation workspace, reviewed results, extraction/mapping artifacts, and supporting reports. The raw source-case collection is separated under `data/raw_cases/`, while manuscript-oriented evaluation artifacts are under `evaluation/`.

The manuscript reports the final 42-case evaluation; the repository also contains broader intermediate source inventories and development artifacts used during dataset construction and system validation.

## Research Limitations

The manuscript identifies several current limitations: the evaluation set is limited to 42 scenarios; internal evidence selection and Legal Chain construction remain relatively article-centered; ranking weights are heuristic rather than learned and were not subjected to a systematic sensitivity analysis; and old-to-current statutory mapping can contain ambiguity after legal revisions.

## Publication and Citation

The manuscript title is:

**Knowledge Graph-Based Legal Chain Reasoning for Industrial Safety Decision Support**

Authors: **Hyeonsu Jeong, Hyemin Koo, Seyoung Park, Seonghyeon Moon**

The following items are **to be added upon publication**:

- Journal / proceedings information
- Publication year and bibliographic details
- DOI
- Publisher URL
- Final BibTeX entry
- `CITATION.cff`

## Disclaimer

This repository is a research implementation for industrial-safety legal information retrieval and evidence tracing. It is not a substitute for professional legal advice or authoritative statutory interpretation.
