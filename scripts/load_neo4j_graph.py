#!/usr/bin/env python
"""Load the public Graph-RAG CSV artifacts into Neo4j graph.v1.

The repository stores CSV source-of-truth files under graph_rag_knowledgement/.
This loader turns those CSVs into the Neo4j labels and relationships expected
by app/graph_rag_pipeline/graph_query_layer.py.
"""

from __future__ import annotations

import argparse
import csv
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


ALLOWED_DATABASE = "graph.v1"
DEFAULT_BATCH_SIZE = 1000

csv.field_size_limit(min(sys.maxsize, 2_147_483_647))


@dataclass(frozen=True)
class NodeSpec:
    path: str
    label: str
    key: str


@dataclass(frozen=True)
class EdgeSpec:
    path: str
    from_label: str
    from_key: str
    from_column: str
    rel_type: str
    to_label: str
    to_key: str
    to_column: str
    rel_columns: tuple[str, ...] = ()


NODE_SPECS: tuple[NodeSpec, ...] = (
    NodeSpec("reasoning_graph/nodes/nodes_rule.csv", "Rule", "rule_id"),
    NodeSpec("reasoning_graph/nodes/nodes_requirement.csv", "Requirement", "requirement_id"),
    NodeSpec("reasoning_graph/nodes/nodes_threshold.csv", "Threshold", "threshold_id"),
    NodeSpec("reasoning_graph/nodes/nodes_exception.csv", "Exception", "exception_id"),
    NodeSpec("reasoning_graph/nodes/nodes_temporal_rule.csv", "TemporalRule", "temporal_rule_id"),
    NodeSpec("reasoning_graph/nodes/nodes_entity_type.csv", "EntityType", "entity_type_id"),
    NodeSpec("reasoning_graph/nodes/nodes_list_item.csv", "ListItem", "list_item_id"),
    NodeSpec("document_graph/nodes/nodes_law.csv", "Law", "law_version_id"),
    NodeSpec("document_graph/nodes/nodes_heading.csv", "Heading", "heading_id"),
    NodeSpec("document_graph/nodes/nodes_article.csv", "Article", "article_id"),
    NodeSpec("document_graph/nodes/nodes_paragraph.csv", "Paragraph", "paragraph_id"),
    NodeSpec("document_graph/nodes/nodes_item.csv", "Item", "item_id"),
    NodeSpec("document_graph/nodes/nodes_subitem.csv", "Subitem", "subitem_id"),
    NodeSpec("document_graph/nodes/nodes_addendum.csv", "Addendum", "addendum_id"),
    NodeSpec("document_graph/source_annex/annexes.csv", "Annex", "annex_id"),
    NodeSpec("document_graph/source_annex/annex_logical_rows.csv", "LogicalRow", "logical_row_id"),
    NodeSpec("document_graph/source_annex/annex_logical_cells.csv", "LogicalCell", "logical_cell_id"),
    NodeSpec("document_graph/source_annex/annex_notes.csv", "AnnexNote", "note_id"),
)


REASONING_EDGE_SPECS: tuple[EdgeSpec, ...] = (
    EdgeSpec(
        "reasoning_graph/edges/edges_rule_requirement.csv",
        "Rule",
        "rule_id",
        "from_rule_id",
        "HAS_REQUIREMENT",
        "Requirement",
        "requirement_id",
        "to_requirement_id",
        ("rel",),
    ),
    EdgeSpec(
        "reasoning_graph/edges/edges_rule_threshold.csv",
        "Rule",
        "rule_id",
        "from_rule_id",
        "HAS_THRESHOLD",
        "Threshold",
        "threshold_id",
        "to_threshold_id",
        ("rel", "threshold_role"),
    ),
    EdgeSpec(
        "reasoning_graph/edges/edges_rule_exception.csv",
        "Rule",
        "rule_id",
        "from_rule_id",
        "HAS_EXCEPTION",
        "Exception",
        "exception_id",
        "to_exception_id",
        ("rel",),
    ),
    EdgeSpec(
        "reasoning_graph/edges/edges_rule_temporal.csv",
        "Rule",
        "rule_id",
        "from_rule_id",
        "HAS_TEMPORAL_CONDITION",
        "TemporalRule",
        "temporal_rule_id",
        "to_temporal_id",
        ("rel",),
    ),
    EdgeSpec(
        "reasoning_graph/edges/edges_rule_entity.csv",
        "Rule",
        "rule_id",
        "from_rule_id",
        "RELATED_ENTITY",
        "EntityType",
        "entity_type_id",
        "to_entity_type_id",
        ("rel",),
    ),
    EdgeSpec(
        "reasoning_graph/edges/edges_rule_list_item.csv",
        "Rule",
        "rule_id",
        "from_rule_id",
        "HAS_LIST_ITEM",
        "ListItem",
        "list_item_id",
        "to_list_item_id",
        ("rel", "needs_review"),
    ),
    EdgeSpec(
        "reasoning_graph/edges/edges_rule_reasoning.csv",
        "Rule",
        "rule_id",
        "from_rule_id",
        "RELATED_RULE",
        "Rule",
        "rule_id",
        "to_rule_id",
        ("rel", "reasoning_note", "source_edge_id"),
    ),
    EdgeSpec(
        "reasoning_graph/edges/edges_rule_source.csv",
        "Rule",
        "rule_id",
        "from_rule_id",
        "EXTRACTED_FROM",
        "SourceNode",
        "source_node_id",
        "to_node_id",
        ("rel", "to_node_type"),
    ),
)


DOCUMENT_EDGE_SPECS: tuple[EdgeSpec, ...] = (
    EdgeSpec(
        "document_graph/nodes/nodes_heading.csv",
        "Law",
        "law_version_id",
        "law_version_id",
        "CONTAINS",
        "Heading",
        "heading_id",
        "heading_id",
    ),
    EdgeSpec(
        "document_graph/nodes/nodes_article.csv",
        "Heading",
        "heading_id",
        "heading_id",
        "CONTAINS",
        "Article",
        "article_id",
        "article_id",
    ),
    EdgeSpec(
        "document_graph/nodes/nodes_paragraph.csv",
        "Article",
        "article_id",
        "article_id",
        "CONTAINS",
        "Paragraph",
        "paragraph_id",
        "paragraph_id",
    ),
    EdgeSpec(
        "document_graph/nodes/nodes_item.csv",
        "Paragraph",
        "paragraph_id",
        "paragraph_id",
        "CONTAINS",
        "Item",
        "item_id",
        "item_id",
    ),
    EdgeSpec(
        "document_graph/nodes/nodes_subitem.csv",
        "Item",
        "item_id",
        "item_id",
        "CONTAINS",
        "Subitem",
        "subitem_id",
        "subitem_id",
    ),
    EdgeSpec(
        "document_graph/nodes/nodes_addendum.csv",
        "Law",
        "law_version_id",
        "law_version_id",
        "CONTAINS",
        "Addendum",
        "addendum_id",
        "addendum_id",
    ),
    EdgeSpec(
        "document_graph/source_annex/annex_logical_rows.csv",
        "Annex",
        "annex_id",
        "annex_id",
        "HAS_LOGICAL_ROW",
        "LogicalRow",
        "logical_row_id",
        "logical_row_id",
    ),
    EdgeSpec(
        "document_graph/source_annex/annex_logical_cells.csv",
        "LogicalRow",
        "logical_row_id",
        "logical_row_id",
        "HAS_LOGICAL_CELL",
        "LogicalCell",
        "logical_cell_id",
        "logical_cell_id",
    ),
    EdgeSpec(
        "document_graph/source_annex/annex_notes.csv",
        "Annex",
        "annex_id",
        "annex_id",
        "HAS_NOTE",
        "AnnexNote",
        "note_id",
        "note_id",
    ),
)


ANCHOR_SPECS: tuple[tuple[str, str, str, str], ...] = (
    ("article", "Article", "article_id", "document_graph/nodes/nodes_article.csv"),
    ("paragraph", "Paragraph", "paragraph_id", "document_graph/nodes/nodes_paragraph.csv"),
    ("item", "Item", "item_id", "document_graph/nodes/nodes_item.csv"),
    ("subitem", "Subitem", "subitem_id", "document_graph/nodes/nodes_subitem.csv"),
    ("addendum", "Addendum", "addendum_id", "document_graph/nodes/nodes_addendum.csv"),
    ("annex", "Annex", "annex_id", "document_graph/source_annex/annexes.csv"),
    ("logical_row", "LogicalRow", "logical_row_id", "document_graph/source_annex/annex_logical_rows.csv"),
    ("logical_cell", "LogicalCell", "logical_cell_id", "document_graph/source_annex/annex_logical_cells.csv"),
    ("annex_note", "AnnexNote", "note_id", "document_graph/source_annex/annex_notes.csv"),
)


CONSTRAINTS_AND_INDEXES: tuple[str, ...] = (
    "CREATE CONSTRAINT rule_rule_id_unique IF NOT EXISTS FOR (n:Rule) REQUIRE n.rule_id IS UNIQUE",
    "CREATE CONSTRAINT requirement_requirement_id_unique IF NOT EXISTS FOR (n:Requirement) REQUIRE n.requirement_id IS UNIQUE",
    "CREATE CONSTRAINT threshold_threshold_id_unique IF NOT EXISTS FOR (n:Threshold) REQUIRE n.threshold_id IS UNIQUE",
    "CREATE CONSTRAINT exception_exception_id_unique IF NOT EXISTS FOR (n:Exception) REQUIRE n.exception_id IS UNIQUE",
    "CREATE CONSTRAINT temporalrule_temporal_rule_id_unique IF NOT EXISTS FOR (n:TemporalRule) REQUIRE n.temporal_rule_id IS UNIQUE",
    "CREATE CONSTRAINT entitytype_entity_type_id_unique IF NOT EXISTS FOR (n:EntityType) REQUIRE n.entity_type_id IS UNIQUE",
    "CREATE CONSTRAINT listitem_list_item_id_unique IF NOT EXISTS FOR (n:ListItem) REQUIRE n.list_item_id IS UNIQUE",
    "CREATE CONSTRAINT sourcenode_source_node_id_unique IF NOT EXISTS FOR (n:SourceNode) REQUIRE n.source_node_id IS UNIQUE",
    "CREATE CONSTRAINT law_law_version_id_unique IF NOT EXISTS FOR (n:Law) REQUIRE n.law_version_id IS UNIQUE",
    "CREATE CONSTRAINT heading_heading_id_unique IF NOT EXISTS FOR (n:Heading) REQUIRE n.heading_id IS UNIQUE",
    "CREATE CONSTRAINT article_article_id_unique IF NOT EXISTS FOR (n:Article) REQUIRE n.article_id IS UNIQUE",
    "CREATE CONSTRAINT paragraph_paragraph_id_unique IF NOT EXISTS FOR (n:Paragraph) REQUIRE n.paragraph_id IS UNIQUE",
    "CREATE CONSTRAINT item_item_id_unique IF NOT EXISTS FOR (n:Item) REQUIRE n.item_id IS UNIQUE",
    "CREATE CONSTRAINT subitem_subitem_id_unique IF NOT EXISTS FOR (n:Subitem) REQUIRE n.subitem_id IS UNIQUE",
    "CREATE CONSTRAINT addendum_addendum_id_unique IF NOT EXISTS FOR (n:Addendum) REQUIRE n.addendum_id IS UNIQUE",
    "CREATE CONSTRAINT annex_annex_id_unique IF NOT EXISTS FOR (n:Annex) REQUIRE n.annex_id IS UNIQUE",
    "CREATE CONSTRAINT logicalrow_logical_row_id_unique IF NOT EXISTS FOR (n:LogicalRow) REQUIRE n.logical_row_id IS UNIQUE",
    "CREATE CONSTRAINT logicalcell_logical_cell_id_unique IF NOT EXISTS FOR (n:LogicalCell) REQUIRE n.logical_cell_id IS UNIQUE",
    "CREATE CONSTRAINT annexnote_note_id_unique IF NOT EXISTS FOR (n:AnnexNote) REQUIRE n.note_id IS UNIQUE",
    "CREATE INDEX rule_law_name_index IF NOT EXISTS FOR (n:Rule) ON (n.law_name)",
    "CREATE INDEX rule_article_no_index IF NOT EXISTS FOR (n:Rule) ON (n.article_no)",
    "CREATE INDEX rule_rule_type_index IF NOT EXISTS FOR (n:Rule) ON (n.rule_type)",
    "CREATE INDEX rule_rule_subtype_index IF NOT EXISTS FOR (n:Rule) ON (n.rule_subtype)",
    "CREATE INDEX rule_annex_title_index IF NOT EXISTS FOR (n:Rule) ON (n.annex_title)",
    "CREATE INDEX listitem_item_text_index IF NOT EXISTS FOR (n:ListItem) ON (n.item_text)",
    "CREATE INDEX listitem_list_item_type_index IF NOT EXISTS FOR (n:ListItem) ON (n.list_item_type)",
    "CREATE INDEX sourcenode_law_name_index IF NOT EXISTS FOR (n:SourceNode) ON (n.law_name)",
    "CREATE INDEX sourcenode_article_no_index IF NOT EXISTS FOR (n:SourceNode) ON (n.article_no)",
    "CREATE INDEX sourcenode_annex_title_index IF NOT EXISTS FOR (n:SourceNode) ON (n.annex_title)",
)


def read_env(path: Path) -> dict[str, str]:
    env = dict(os.environ)
    if path.exists():
        for raw in path.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            env[key.strip()] = value.strip().strip('"').strip("'")
    return env


def require_env(env: dict[str, str]) -> dict[str, str]:
    required = ("NEO4J_URI", "NEO4J_USER", "NEO4J_PASSWORD", "NEO4J_DATABASE")
    missing = [key for key in required if not env.get(key)]
    if missing:
        raise SystemExit(f"Missing required environment keys: {', '.join(missing)}")
    if env["NEO4J_DATABASE"] != ALLOWED_DATABASE:
        raise SystemExit(f"Refusing to load database {env['NEO4J_DATABASE']!r}; expected {ALLOWED_DATABASE!r}.")
    return {key: env[key] for key in required}


def coerce(value: str) -> Any:
    if value == "":
        return None
    if value == "True":
        return True
    if value == "False":
        return False
    return value


def read_csv_rows(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [{key: coerce(value) for key, value in row.items()} for row in csv.DictReader(handle)]


def chunks(items: list[dict[str, Any]], size: int) -> Iterable[list[dict[str, Any]]]:
    for start in range(0, len(items), size):
        yield items[start : start + size]


def run_batch(session: Any, cypher: str, rows: list[dict[str, Any]], batch_size: int, dry_run: bool) -> int:
    if dry_run:
        return len(rows)
    total = 0
    for batch in chunks(rows, batch_size):
        session.execute_write(lambda tx, b=batch: tx.run(cypher, rows=b).consume())
        total += len(batch)
    return total


def load_node(session: Any, base: Path, spec: NodeSpec, batch_size: int, dry_run: bool) -> int:
    rows = read_csv_rows(base / spec.path)
    cypher = f"""
    UNWIND $rows AS row
    WITH row WHERE row.{spec.key} IS NOT NULL
    MERGE (n:{spec.label} {{{spec.key}: row.{spec.key}}})
    SET n += row
    """
    return run_batch(session, cypher, rows, batch_size, dry_run)


def load_source_nodes(session: Any, base: Path, batch_size: int, dry_run: bool) -> int:
    rows_by_id: dict[str, dict[str, Any]] = {}
    for row in read_csv_rows(base / "reasoning_graph/nodes/nodes_rule.csv"):
        source_node_id = row.get("source_node_id")
        if source_node_id:
            rows_by_id[str(source_node_id)] = row
    rows = list(rows_by_id.values())
    cypher = """
    UNWIND $rows AS row
    WITH row WHERE row.source_node_id IS NOT NULL
    MERGE (n:SourceNode {source_node_id: row.source_node_id})
    SET n += row
    """
    return run_batch(session, cypher, rows, batch_size, dry_run)


def load_edge(session: Any, base: Path, spec: EdgeSpec, batch_size: int, dry_run: bool) -> int:
    rows = read_csv_rows(base / spec.path)
    rel_props = ", ".join(f"{column}: row.{column}" for column in spec.rel_columns)
    set_clause = f"SET r += {{{rel_props}}}" if rel_props else ""
    cypher = f"""
    UNWIND $rows AS row
    WITH row
    WHERE row.{spec.from_column} IS NOT NULL AND row.{spec.to_column} IS NOT NULL
    MATCH (a:{spec.from_label} {{{spec.from_key}: row.{spec.from_column}}})
    MATCH (b:{spec.to_label} {{{spec.to_key}: row.{spec.to_column}}})
    MERGE (a)-[r:{spec.rel_type}]->(b)
    {set_clause}
    """
    return run_batch(session, cypher, rows, batch_size, dry_run)


def anchor_indexes(base: Path) -> dict[str, tuple[str, str]]:
    index: dict[str, tuple[str, str]] = {}
    for _kind, label, key, rel_path in ANCHOR_SPECS:
        for row in read_csv_rows(base / rel_path):
            value = row.get(key)
            if value:
                index[str(value)] = (label, key)
    return index


def source_resolution_rows(base: Path, source_path: str) -> dict[tuple[str, str], list[dict[str, Any]]]:
    anchors = anchor_indexes(base)
    result: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for row in read_csv_rows(base / source_path):
        source_id = row.get("source_node_id")
        if not source_id:
            continue
        target = anchors.get(str(source_id))
        if not target:
            continue
        label, key = target
        result.setdefault((label, key), []).append({"source_node_id": source_id, "target_id": source_id})
    return result


def load_source_resolution(session: Any, base: Path, batch_size: int, dry_run: bool) -> int:
    rows_by_target = source_resolution_rows(base, "reasoning_graph/nodes/nodes_rule.csv")
    total = 0
    for (label, key), rows in rows_by_target.items():
        cypher = f"""
        UNWIND $rows AS row
        MATCH (s:SourceNode {{source_node_id: row.source_node_id}})
        MATCH (a:{label} {{{key}: row.target_id}})
        MERGE (s)-[:RESOLVES_TO]->(a)
        """
        total += run_batch(session, cypher, rows, batch_size, dry_run)
    return total


def load_listitem_resolution(session: Any, base: Path, batch_size: int, dry_run: bool) -> int:
    anchors = anchor_indexes(base)
    rows_by_target: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for row in read_csv_rows(base / "reasoning_graph/nodes/nodes_list_item.csv"):
        list_item_id = row.get("list_item_id")
        source_id = row.get("source_node_id")
        if not list_item_id or not source_id:
            continue
        target = anchors.get(str(source_id))
        if not target:
            continue
        label, key = target
        rows_by_target.setdefault((label, key), []).append(
            {"list_item_id": list_item_id, "target_id": source_id}
        )
    total = 0
    for (label, key), rows in rows_by_target.items():
        cypher = f"""
        UNWIND $rows AS row
        MATCH (li:ListItem {{list_item_id: row.list_item_id}})
        MATCH (a:{label} {{{key}: row.target_id}})
        MERGE (li)-[:ITEM_RESOLVES_TO]->(a)
        """
        total += run_batch(session, cypher, rows, batch_size, dry_run)
    return total


def validate_counts(session: Any, dry_run: bool) -> dict[str, Any]:
    if dry_run:
        return {}
    queries = {
        "total_nodes": "MATCH (n) RETURN count(n) AS count",
        "total_relationships": "MATCH ()-[r]->() RETURN count(r) AS count",
        "rules_without_source": "MATCH (r:Rule) WHERE NOT (r)-[:EXTRACTED_FROM]->(:SourceNode) RETURN count(r) AS count",
        "unresolved_source_nodes": "MATCH (s:SourceNode) WHERE NOT (s)-[:RESOLVES_TO]->() RETURN count(s) AS count",
        "listitems_without_anchor": "MATCH (li:ListItem) WHERE NOT (li)-[:ITEM_RESOLVES_TO]->() RETURN count(li) AS count",
    }
    result: dict[str, Any] = {}
    for key, cypher in queries.items():
        record = session.execute_read(lambda tx, q=cypher: tx.run(q).single())
        result[key] = record["count"] if record else None
    return result


def run_loader(args: argparse.Namespace) -> None:
    repo_root = Path(args.repo_root).resolve()
    base = repo_root / "graph_rag_knowledgement"
    env = {} if args.dry_run else require_env(read_env(repo_root / ".env"))
    driver = None
    try:
        if args.dry_run:
            session = None
            _run_load_steps(session, base, args)
        else:
            from neo4j import GraphDatabase

            driver = GraphDatabase.driver(
                env["NEO4J_URI"], auth=(env["NEO4J_USER"], env["NEO4J_PASSWORD"])
            )
            with driver.session(database=env["NEO4J_DATABASE"]) as session:
                _run_load_steps(session, base, args)
    finally:
        if driver is not None:
            driver.close()


def _run_load_steps(session: Any, base: Path, args: argparse.Namespace) -> None:
    if args.reset:
        if args.dry_run:
            print("[dry-run] Would delete all nodes and relationships.")
        else:
            session.execute_write(lambda tx: tx.run("MATCH (n) DETACH DELETE n").consume())
            print("Reset existing graph.")

    for statement in CONSTRAINTS_AND_INDEXES:
        if args.dry_run:
            print(f"[dry-run] {statement}")
        else:
            session.execute_write(lambda tx, q=statement: tx.run(q).consume())
    print(f"Prepared {len(CONSTRAINTS_AND_INDEXES)} constraints/indexes.")

    for spec in NODE_SPECS:
        count = load_node(session, base, spec, args.batch_size, args.dry_run)
        print(f"Loaded {count:>6} rows as :{spec.label}")

    source_count = load_source_nodes(session, base, args.batch_size, args.dry_run)
    print(f"Loaded {source_count:>6} rows as :SourceNode")

    for spec in REASONING_EDGE_SPECS:
        count = load_edge(session, base, spec, args.batch_size, args.dry_run)
        print(f"Loaded {count:>6} rows as :{spec.rel_type}")

    for spec in DOCUMENT_EDGE_SPECS:
        count = load_edge(session, base, spec, args.batch_size, args.dry_run)
        print(f"Loaded {count:>6} rows as :{spec.rel_type}")

    resolved = load_source_resolution(session, base, args.batch_size, args.dry_run)
    print(f"Loaded {resolved:>6} SourceNode RESOLVES_TO rows")

    listitem_resolved = load_listitem_resolution(session, base, args.batch_size, args.dry_run)
    print(f"Loaded {listitem_resolved:>6} ListItem ITEM_RESOLVES_TO rows")

    counts = validate_counts(session, args.dry_run)
    if counts:
        print("Validation summary:")
        for key, value in counts.items():
            print(f"  {key}: {value}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Load Graph-RAG CSV artifacts into Neo4j graph.v1.")
    parser.add_argument("--repo-root", default=Path.cwd(), help="Repository root containing .env and graph_rag_knowledgement/")
    parser.add_argument("--batch-size", type=int, default=DEFAULT_BATCH_SIZE)
    parser.add_argument("--reset", action="store_true", help="Delete the existing graph before loading.")
    parser.add_argument("--dry-run", action="store_true", help="Print planned operations without writing to Neo4j.")
    return parser.parse_args()


if __name__ == "__main__":
    run_loader(parse_args())
