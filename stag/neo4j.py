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
    Represent a neo4j database as a :class:`stag.graph.LocalGraph` object.

    This provides 'local' access to the graph only. Given a node, we can query
    its neighbors and its degree.
    The graph does not support weighted edges, and it does not
    distinguish between edge types or directions.

    The neo4j ``<id>`` attributes are used as the STAG vertex ids.

    All methods which make calls to the database backend have a small cache of
    recent queries, meaning that consecutive queries for the same node will be
    fast.
    """
    def __init__(self, uri, username, password):
        """
        Connect to a neo4j database backend.

        For example, assuming that there is a Neo4j database running locally,
        the graph object can be created as follows.

        .. code-block:: python

            import stag.neo4j
            g = stag.neo4j.Neo4jGraph("bolt://localhost:7687", "neo4j", "password")

        It is also possible to connect to a remote Neo4j database by passing
        the relevant ``uri`` to the constructor.

        :param uri: the location of the neo4j database
        :param username: the neo4j username
        :param password: the neo4j password
        """
        super().__init__()

        self.driver = neo4j.GraphDatabase.driver(uri, auth=(username, password))

    def degree(self, v):
        """
        Equivalent to :meth:`degree_unweighted`.
        """
        return self.degree_unweighted(v)

    @lru_cache(maxsize=1024)
    def degree_unweighted(self, v) -> int:
        """Query the degree of the node with the given neo4j ID."""
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
        """
        Equivalent to :meth:`degrees_unweighted`.
        """
        return self.degrees_unweighted(vertices)

    @lru_cache(maxsize=1024)
    def degrees_unweighted(self, vertices: List[int]) -> List[int]:
        """
        Query the degrees of the nodes with the given neo4j IDs.

        This method makes a single query to the database to return all of the
        node degrees.
        """
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
        """
        Fetch the neighbors of the node with the given Neo4j node ID.

        The returned :class:`stag.graph.Edge` objects all have weight :math:`1` .
        """
        return [graph.Edge(v, u, 1) for u in self.neighbors_unweighted(v)]

    @lru_cache(maxsize=1024)
    def neighbors_unweighted(self, v) -> List[int]:
        """
        Fetch the neighbors of the node with the given Neo4j node ID.

        Returns the Neo4j node IDs of the neighboring nodes.
        """
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

    @lru_cache(maxsize=1024)
    def query_node_labels(self, node_id: int) -> List[str]:
        """
        Query the labels of the given node.

        For example, using the Neo4j movie database example, you can query
        whether a given node represents a person or a movie as follows.

            >>> import stag.neo4j
            >>> g = stag.neo4j.Neo4jGraph("bolt://localhost:7687", "neo4j", "password")
            >>> labels = g.query_node_labels(0)
            ['Movie']
            >>> labels = g.query_node_labels(1)
            ['Person']

        """
        with self.driver.session() as session:
            result = session.execute_read(self._labels_query, node_id)
        return [x[0] for x in result]

    @staticmethod
    def _labels_query(tx, node_id):
        # To get the neighbors of the given node, we will execute the following
        # Cypher command:
        #    MATCH (n1)-[]-(n2) WHERE id(n1) = v return id(n2)
        # which finds the nodes which are a single step from the node
        # with the given node ID.
        result = tx.run("MATCH (n1) "
                        "WHERE id(n1) = $node_id "
                        "RETURN DISTINCT labels(n1)", node_id=node_id)
        return result.values()[0]

    def query_id(self, property_name: str, property_value: str) -> int:
        """
        Find the Neo4j ID of a node with the given property.

        For example, using the Neo4j movie database example you can find the
        Neo4j node corresponding to a given movie as follows.
        
        .. code-block:: python
        
            import stag.neo4j
            g = stag.neo4j.Neo4jGraph("bolt://localhost:7687", "neo4j", "password")
            node_id = g.query_id("title", "Avatar")

        This will make a query to the database to find a node with the given
        property.
        This query will be slow unless the database has an index for
        ``property_name``.
        For more information, see the Neo4j documentation on
        `creating an index <https://neo4j.com/docs/cypher-manual/current/indexes-for-search-performance/>`_ .

        :param property_name: the node property to query
        :param property_value: the value of the node property to search for
        :return: the Neo4j node ID of a node with the given property value
        """
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
        """
        Find the requested property of a Neo4j node.

        For example, using the Neo4j movie database example, you can find the
        title of a movie node as follows.

        .. code-block:: python

            import stag.neo4j
            g = stag.neo4j.Neo4jGraph("bolt://localhost:7687", "neo4j", "password")
            title = g.query_property(1, "title")

        :param id: the Neo4j node ID to query
        :param property_name: the name of the property to query
        :return: the value of the requested property on the given node
        """
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
