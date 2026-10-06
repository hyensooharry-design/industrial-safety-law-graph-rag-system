# Neo4j Graph Load

This repository includes the CSV artifacts needed to recreate the `graph.v1` Neo4j database used by the Legal Graph-RAG backend.

The source-of-truth graph artifacts are stored under `knowledge_graph/`.

## Prerequisites

- Python 3.10+ recommended
- Neo4j 5.x
- A Neo4j database named `graph.v1`
- Python dependencies installed from `requirements.txt`

```bash
pip install -r requirements.txt
```

Create a local `.env` from `.env.example` and set:

```env
NEO4J_URI=bolt://127.0.0.1:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
NEO4J_DATABASE=graph.v1
```

The backend intentionally refuses to use a different database name.

## Verify the load plan

```bash
python scripts/load_neo4j_graph.py --dry-run
```

Expected high-level dry-run output includes:

- `Rule`: 8,858 rows
- `SourceNode`: 8,858 rows
- `EXTRACTED_FROM`: 8,858 rows
- `SourceNode RESOLVES_TO`: 8,858 rows
- `ListItem ITEM_RESOLVES_TO`: 3,604 rows

## Load into Neo4j

```bash
python scripts/load_neo4j_graph.py
```

To clear a disposable local `graph.v1` database before loading:

```bash
python scripts/load_neo4j_graph.py --reset
```

## What the loader creates

The loader creates constraints and indexes, then loads the manuscript's four conceptual graph components:

- Document Graph nodes and hierarchy
- Annex Graph nodes and table structure
- Reasoning Graph nodes and semantic relations
- Provenance Layer relations: `EXTRACTED_FROM`, `RESOLVES_TO`, and `ITEM_RESOLVES_TO`

## Run the application

Backend:

```bash
python -m uvicorn graph_rag_pipeline.ask_adapter:app --app-dir app --host 127.0.0.1 --port 8000
```

Frontend:

```bash
cd frontend
npm ci
npm run dev
```
