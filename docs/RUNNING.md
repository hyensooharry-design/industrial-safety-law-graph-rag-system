# Running the Legal Graph-RAG System

This repository contains the backend, frontend, Neo4j graph artifacts, case-scenario evaluation artifacts, and source data needed for a local research run.

## Requirements

- Python 3.10+
- Neo4j 5.x
- Node.js and npm
- API credentials required by the configured model backend

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Create a local environment file:

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
copy .env.example .env
```

Configure at least the Neo4j connection:

```env
NEO4J_URI=bolt://127.0.0.1:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_neo4j_password
NEO4J_DATABASE=graph.v1
```

## Verify and load the graph

Dry-run:

```bash
python scripts/load_neo4j_graph.py --dry-run
```

Load the graph:

```bash
python scripts/load_neo4j_graph.py
```

For a disposable local database only:

```bash
python scripts/load_neo4j_graph.py --reset
```

`--reset` deletes the existing nodes and relationships in the configured Neo4j database before reloading.

## Run the backend

```bash
python -m uvicorn graph_rag_pipeline.ask_adapter:app --app-dir app --host 127.0.0.1 --port 8000
```

## Run the frontend

```bash
cd frontend
npm ci
npm run dev
```

The frontend expects the backend at `http://127.0.0.1:8000` unless configured otherwise.

## Repository paths after paper-oriented cleanup

- Graph artifacts: `knowledge_graph/`
- Final and intermediate evaluation artifacts: `evaluation/`
- Broader raw source cases: `data/raw_cases/`
- Backend: `app/graph_rag_pipeline/`
- Frontend: `frontend/`
- Neo4j loader: `scripts/load_neo4j_graph.py`

## Publication-specific additions

A DOI-pinned release, final citation metadata, and publication-linked reproduction notes are planned after publication.
