from typing import List
from neo4j import ManagedTransaction, Record
from config import NEO4J_ENTITY_NAME_FULLTEXT_INDEX_NAME
from .model import (
    Node,
    Edge,
    Neo4jEdge,
    Neo4jMultiEdge,
)


def find_nodes(
    tx: ManagedTransaction,
    q: str,
) -> List[Record]:
    query = "MATCH (m:Entity {name: $name})"
    result = tx.run(query, name=q)
    return list(result)


def fulltext_search_nodes(
    tx: ManagedTransaction,
    q: str,
) -> List[Record]:
    query = "CALL db.index.fulltext.queryNodes($idx_name, $q)"
    results = tx.run(
        query,
        idx_name=NEO4J_ENTITY_NAME_FULLTEXT_INDEX_NAME,
        q=q,
    )
    return list(results)


def find_surrounding_edges(
    tx: ManagedTransaction,
    q: str,
    depth: int,
) -> List[Neo4jMultiEdge]:
    query = f"MATCH (a:Entity {{name: $name}})-[r*..{depth}]->(b) RETURN a, r, b"
    results: list[Neo4jMultiEdge] = []
    for record in tx.run(query, name=q):  # type: ignore
        results.append(
            Neo4jMultiEdge(
                src=record["a"],
                relations=record["r"],
                sink=record["b"],
            )
        )

    return results


def fulltext_search_surrounding_edges(
    tx: ManagedTransaction,
    q: str,
    depth: int,
) -> List[Neo4jMultiEdge]:
    query = (
        "CALL db.index.fulltext.queryNodes($idx_name, $q, {limit: 1}) YIELD node AS a "
        f"MATCH (a)-[r*..{depth}]->(b) RETURN a, r, b"
    )
    resp = tx.run(
        query,  # type: ignore
        idx_name=NEO4J_ENTITY_NAME_FULLTEXT_INDEX_NAME,
        q=q,
    )
    results: List[Neo4jMultiEdge] = []
    for record in resp:  # type: ignore
        results.append(
            Neo4jMultiEdge(
                src=record["a"],
                relations=record["r"],
                sink=record["b"],
            )
        )

    return results


def find_all_edges(tx: ManagedTransaction) -> List[Neo4jEdge]:
    query = "MATCH (a:Entity)-[r:RELATION]->(b:Entity) RETURN a, r, b"
    results: list[Neo4jEdge] = []
    for record in tx.run(query):
        results.append(
            Neo4jEdge(
                src=record["a"],
                relation=record["r"],
                sink=record["b"],
            )
        )

    return results


def add_node_if_not_exist(
    tx: ManagedTransaction,
    node: Node,
):
    query = "MERGE (n:Entity {name: $name})"
    tx.run(query, name=node.name)


def add_edge_and_node_if_not_exists(
    tx: ManagedTransaction,
    src: Node,
    relation: Edge,
    sink: Node,
):
    query = (
        "MERGE (a:Entity {name: $src_name}) "
        "MERGE (b:Entity {name: $sink_name}) "
        "MERGE (a)-[r:RELATION {name: $relation}]->(b)"
    )
    tx.run(
        query,
        src_name=src.name,
        relation=relation.relation,
        sink_name=sink.name,
    )


def delete_node(
    tx: ManagedTransaction,
    name: str,
):
    query = "MATCH (m:Entity {name: $name}) DETACH DELETE m"
    tx.run(query, name=name)


def delete_edge(
    tx: ManagedTransaction,
    src: Node,
    relation: Edge,
    sink: Node,
):
    query = (
        "MATCH (a:Entity {name: $src_name})-[r:RELATION {name: $relation}]->(b:Entity {name: $sink_name}) "
        "DELETE r "
        "OPTIONAL MATCH (n:Entity {name: $src_name}) WHERE NOT (n)--() "
        "DELETE n "
        "OPTIONAL MATCH (n:Entity {name: $sink_name}) WHERE NOT (n)--() "
        "DELETE n"
    )
    tx.run(
        query,
        src_name=src.name,
        relation=relation.relation,
        sink_name=sink.name,
    )


def clear_all(
    tx: ManagedTransaction,
):
    query = "MATCH (n:Entity) DETACH DELETE n"
    tx.run(query)
