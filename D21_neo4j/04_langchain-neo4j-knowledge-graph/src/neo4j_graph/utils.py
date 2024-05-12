from typing import List
import networkx as nx
from .model import Neo4jEdge


def add_neo4j_edges_to_networkx_graph(graph: nx.DiGraph, edge_records: List[Neo4jEdge]):
    for record in edge_records:
        if not graph.has_node(record.src["name"]):
            graph.add_node(record.src["name"])
        if not graph.has_node(record.sink["name"]):
            graph.add_node(record.sink["name"])
        graph.add_edge(
            record.src["name"],
            record.sink["name"],
            relation=record.relation["name"],
        )