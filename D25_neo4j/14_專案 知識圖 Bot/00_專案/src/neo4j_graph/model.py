from typing import Any, Optional, List, Dict, NamedTuple


class Node(NamedTuple):
    name: str
    metadata: Optional[Dict[str, Any]] = None


class Edge(NamedTuple):
    relation: str
    metadata: Optional[Dict[str, Any]] = None


class Neo4jEdge(NamedTuple):
    src: Dict[str, Any]
    relation: Dict[str, Any]
    sink: Dict[str, Any]

    def to_statement(self) -> str:
        return " ".join(
            [
                self.src["name"],
                self.relation["name"],
                self.sink["name"],
            ]
        )


class Neo4jMultiEdge(NamedTuple):
    src: Dict[str, Any]
    relations: List[Any]
    sink: Dict[str, Any]

    def to_statement(self) -> str:
        statement_parts: List[str] = []
        statement_parts.append(self.src["name"])
        for relation in self.relations:
            statement_parts.append(relation["name"])
            rel_sink = relation.nodes[1]
            statement_parts.append(rel_sink["name"])

        return " ".join(statement_parts)