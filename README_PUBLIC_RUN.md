# Public Run Guide

This repository contains a public-safe execution package for the Industrial Safety Law Graph-RAG System.

It includes the backend, frontend, Neo4j CSV graph artifacts, and the core v6 case-scenario workflow files needed to run the local system. It does not include live credentials, API keys, private review-response materials, manuscript audit packages, or Git history.

## Included

- `app/graph_rag_pipeline`: FastAPI Graph-RAG backend
- `frontend`: Vite/React local UI
- `graph_rag_knowledgement`: document, annex, reasoning, provenance graph artifacts
- `scripts/load_neo4j_graph.py`: Neo4j CSV loader
- `project/raw_cases`: source case files used by the public v6 workflow
- `project/generated_v6_case_scenario_eval`: public v6 case-scenario dataset and outputs

## Excluded

- `.env`
- API keys and credentials
- `.git`
- `node_modules`
- Python cache files
- reviewer-response packages
- manuscript-internal validation/audit outputs
- temporary experiment logs and backup files

## Requirements

- Python 3.10+
- Neo4j 5.x
- Node.js and npm
- OpenAI API key

Install Python dependencies:

```powershell
pip install -r requirements.txt
```

Create a local environment file:

```powershell
copy .env.example .env
notepad .env
```

Set at least:

```env
OPENAI_API_KEY=your_openai_api_key
NEO4J_URI=bolt://127.0.0.1:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_neo4j_password
NEO4J_DATABASE=graph.v1
```

## Load Neo4j Graph

First verify that the CSV graph artifacts can be read:

```powershell
python scripts/load_neo4j_graph.py --dry-run
```

Load the graph into an empty local Neo4j database:

```powershell
python scripts/load_neo4j_graph.py
```

To reload a disposable local database from scratch:

```powershell
python scripts/load_neo4j_graph.py --reset
```

Warning: `--reset` deletes all nodes and relationships in the configured Neo4j database before loading.

## Run Backend

```powershell
python -m uvicorn graph_rag_pipeline.ask_adapter:app --app-dir app --host 127.0.0.1 --port 8000
```

## Run Frontend

```powershell
cd frontend
npm ci
npm run dev
```

The frontend expects the backend at `http://127.0.0.1:8000` unless configured otherwise.

## Verification Performed Before Public Staging

- Neo4j loader dry-run passed.
- Backend import check passed.
- No `.env` file included.
- No obvious API key/token pattern detected.
- No file above GitHub's 100 MB file limit detected.
- Reviewer-response and manuscript-internal audit folders were excluded.
