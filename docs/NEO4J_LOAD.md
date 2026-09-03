# Neo4j Graph Load

This repository includes the CSV artifacts needed to recreate the `graph.v1`
Neo4j database used by the Graph-RAG backend.

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

## Verify The Load Plan

Run a dry-run first. This does not connect to Neo4j and only verifies that the
CSV files can be read and mapped into the expected graph structure.

```bash
python scripts/load_neo4j_graph.py --dry-run
```

Expected high-level dry-run output includes:

- `Rule`: 8,858 rows
- `SourceNode`: 8,858 rows
- `EXTRACTED_FROM`: 8,858 rows
- `SourceNode RESOLVES_TO`: 8,858 rows
- `ListItem ITEM_RESOLVES_TO`: 3,604 rows

## Load Into Neo4j

To load into an empty `graph.v1` database:

```bash
python scripts/load_neo4j_graph.py
```

To clear the current `graph.v1` contents before loading:

```bash
python scripts/load_neo4j_graph.py --reset
```

Use `--reset` only for a disposable local database. It runs
`MATCH (n) DETACH DELETE n` before loading.

## What The Loader Creates

The loader creates constraints and indexes, then loads:

- Reasoning nodes: `Rule`, `Requirement`, `Threshold`, `Exception`,
  `TemporalRule`, `EntityType`, `ListItem`
- Source/document nodes: `SourceNode`, `Law`, `Heading`, `Article`,
  `Paragraph`, `Item`, `Subitem`, `Addendum`, `Annex`, `LogicalRow`,
  `LogicalCell`, `AnnexNote`
- Reasoning relationships: `HAS_REQUIREMENT`, `HAS_THRESHOLD`,
  `HAS_EXCEPTION`, `HAS_TEMPORAL_CONDITION`, `RELATED_ENTITY`,
  `HAS_LIST_ITEM`, `RELATED_RULE`, `EXTRACTED_FROM`
- Source relationships: `RESOLVES_TO`, `CONTAINS`, `HAS_LOGICAL_ROW`,
  `HAS_LOGICAL_CELL`, `HAS_NOTE`, `ITEM_RESOLVES_TO`

## Run The Backend

After loading:

```bash
python -m uvicorn graph_rag_pipeline.ask_adapter:app --app-dir app --host 127.0.0.1 --port 8000
```

Then run the frontend:

```bash
cd frontend
npm ci
npm run dev
```

The frontend defaults to `http://127.0.0.1:8000`. Override it with
`VITE_API_BASE_URL` if needed.
