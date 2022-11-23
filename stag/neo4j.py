"""
Interface to a neo4j database, exposing a graph interface on which we can run
STAG algorithms.
"""
import neo4j
from typing import List
from functools import lru_cache

from . import graph


class Neo4jGraph(graph.LocalGraph):
    """
    Represent a neo4j database as a STAG LocalGraph object.

    This provides 'local' access to the graph only. Given a node, we can query
    its neighbors.

    For now, the graph does not support weighted edges, and it does not
    distinguish between edge types or directions.
    """
    def __init__(self, uri, username, password):
        super().__init__()

        self.driver = neo4j.GraphDatabase.driver(uri, auth=(username, password))

    def degree(self, v):
        return self.degree_unweighted(v)

    @lru_cache(maxsize=1024)
    def degree_unweighted(self, v) -> int:
        """Query the degree of the node with the given ID."""
        with self.driver.session() as session:
            result = session.execute_read(self._degree_query, v)
        return result

    @staticmethod
    def _degree_query(tx, node_id):
        # To get the degree of the given node, we will execute the following
        # Cypher command:
        #    MATCH (n1)-[]-(n2) WHERE id(n1) = v return count(n2)
        # which finds the nodes which are a single step from the node
        # with the given node ID.
        result = tx.run("MATCH (n1)-[]-(n2) "
                        "WHERE id(n1) = $node_id "
                        "RETURN count(n2)", node_id=node_id)
        return result.single()[0]

    def degrees(self, vertices: List[int]) -> List[float]:
        return self.degrees_unweighted(vertices)

    @lru_cache(maxsize=1024)
    def degrees_unweighted(self, vertices: List[int]) -> List[int]:
        with self.driver.session() as session:
            result = session.execute_read(self._degrees_query, vertices)
        return [x[0] for x in result]

    @staticmethod
    def _degrees_query(tx, node_ids):
        # To get the degree of the given nodes, we will execute the following
        # Cypher command:
        #    MATCH (n1) WHERE id(n1) in [node_ids] return size([p = (n1)--() | p]) as degree
        result = tx.run("MATCH (n1) "
                        f"WHERE id(n1) in {[x for x in node_ids]} "
                        "RETURN size([p = (n1)--() | p]) as degree")
        return list(result.values())

    def neighbors(self, v) -> List[graph.Edge]:
        return [graph.Edge(v, u, 1) for u in self.neighbors_unweighted(v)]

    @lru_cache(maxsize=1024)
    def neighbors_unweighted(self, v) -> List[int]:
        with self.driver.session() as session:
            result = session.execute_read(self._neighbors_query, v)
        return [x[0] for x in result]

    @staticmethod
    def _neighbors_query(tx, node_id):
        # To get the neighbors of the given node, we will execute the following
        # Cypher command:
        #    MATCH (n1)-[]-(n2) WHERE id(n1) = v return id(n2)
        # which finds the nodes which are a single step from the node
        # with the given node ID.
        result = tx.run("MATCH (n1)-[]-(n2) "
                        "WHERE id(n1) = $node_id "
                        "RETURN DISTINCT id(n2)", node_id=node_id)
        return list(result.values())

    def query_id(self, property_name: str, property_value: str) -> int:
        with self.driver.session() as session:
            result = session.execute_read(self._id_query, property_name, property_value)
        return result

    @staticmethod
    def _id_query(tx, property_name, property_value):
        result = tx.run(f'MATCH (n1 {{{property_name}: "{property_value}"}}) '
                        "RETURN id(n1) "
                        "LIMIT 1")
        return result.single()[0]

    def query_property(self, id: int, property_name: str) -> str:
        with self.driver.session() as session:
            result = session.execute_read(self._property_query, id, property_name)
        return result

    @staticmethod
    def _property_query(tx, node_id, property_name):
        result = tx.run("MATCH (n1) "
                        f"WHERE id(n1) = {node_id} "
                        f"RETURN (n1.{property_name}) "
                        "LIMIT 1")
        return result.single()[0]

    def __del__(self):
        # When the graph object it destroyed, close the connection to the backing
        # database.
        self.driver.close()
