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
    Represent a neo4j database as a stag.graph.LocalGraph object.

    This provides 'local' access to the graph only. Given a node, we can query
    its neighbors and its degree.
    The graph does not support weighted edges, and it does not
    distinguish between edge types or directions.

    The neo4j ``<id>`` attributes are used as the STAG vertex ids.

    All methods which make calls to the database backend have a small cache of
    recent queries, meaning that consecutive queries for the same node will be
    fast.
    """
    def __init__(self, uri: str, username: str, password: str):
        r"""
        Connect to a neo4j database backend.

        For example, assuming that there is a Neo4j database running locally,
        the graph object can be created as follows.

        \code{python}
        import stag.neo4j
        g = stag.neo4j.Neo4jGraph("bolt://localhost:7687", "neo4j", "password")
        \endcode

        It is also possible to connect to a remote Neo4j database by passing
        the relevant ``uri`` to the constructor.

        @param uri the location of the neo4j database
        @param username the neo4j username
        @param password the neo4j password
        """
        super().__init__()

        ## The neo4j database driver object used to query the underlying
        # database.
        self.driver = neo4j.GraphDatabase.driver(uri, auth=(username, password))

        ##
        # \cond
        # The partially-constructed adjacency list of all nodes we've queried
        # so far.
        ##
        self.adjacency_list = {}
        self.labels_cache = {}
        ##
        # \endcond
        ##

    def degree(self, v):
        """
        Equivalent to stag.neo4j.Neo4jGraph.degree_unweighted.
        """
        return self.degree_unweighted(v)

    def degree_unweighted(self, v: int) -> int:
        """Query the degree of the node with the given neo4j ID."""
        # The degree of a node is the length of its list of neighbours
        ns = self.neighbors_unweighted(v)
        return len(ns)

    def neighbors(self, v: int) -> List[graph.Edge]:
        """
        Fetch the neighbors of the node with the given Neo4j node ID.

        The returned stag.graph.Edge objects all have weight 1.
        """
        return [graph.Edge(v, u, 1) for u in self.neighbors_unweighted(v)]

    def neighbors_unweighted(self, v: int) -> List[int]:
        """
        Fetch the neighbors of the node with the given Neo4j node ID.

        Returns the Neo4j node IDs of the neighboring nodes.
        """
        if v not in self.adjacency_list:
            with self.driver.session() as session:
                result = session.execute_read(self._neighbors_query, v)
            self.adjacency_list[v] =  [x[0] for x in result]
        return self.adjacency_list[v]

    ##
    # \cond
    ##
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
    ##
    # \endcond
    ##

    def query_node_labels(self, node_id: int) -> List[str]:
        r"""
        Query the labels of the given node.

        For example, using the Neo4j movie database example, you can query
        whether a given node represents a person or a movie as follows.

        \code{python}
            >>> import stag.neo4j
            >>> g = stag.neo4j.Neo4jGraph("bolt://localhost:7687", "neo4j", "password")
            >>> labels = g.query_node_labels(0)
            ['Movie']
            >>> labels = g.query_node_labels(1)
            ['Person']
        \endcode

        """
        if node_id not in self.labels_cache:
            with self.driver.session() as session:
                result = session.execute_read(self._labels_query, node_id)
            self.labels_cache[node_id] = [x[0] for x in result]
        return self.labels_cache[node_id]

    ##
    # \cond
    ##
    @staticmethod
    def _labels_query(tx, node_id: int):
        # To get the neighbors of the given node, we will execute the following
        # Cypher command:
        #    MATCH (n1)-[]-(n2) WHERE id(n1) = v return id(n2)
        # which finds the nodes which are a single step from the node
        # with the given node ID.
        result = tx.run("MATCH (n1) "
                        "WHERE id(n1) = $node_id "
                        "RETURN DISTINCT labels(n1)", node_id=node_id)
        return result.values()[0]
    ##
    # \endcond
    ##

    def query_id(self, property_name: str, property_value: str) -> int:
        r"""
        Find the Neo4j ID of a node with the given property.

        For example, using the Neo4j movie database example you can find the
        Neo4j node corresponding to a given movie as follows.
        
        \code{python}
            import stag.neo4j
            g = stag.neo4j.Neo4jGraph("bolt://localhost:7687", "neo4j", "password")
            node_id = g.query_id("title", "Avatar")
        \endcode

        This will make a query to the database to find a node with the given
        property.
        This query will be slow unless the database has an index for
        ``property_name``.
        For more information, see the Neo4j documentation on
        [creating an index](https://neo4j.com/docs/cypher-manual/current/indexes-for-search-performance/).

        @param property_name the node property to query
        @param property_value the value of the node property to search for
        @return the Neo4j node ID of a node with the given property value.
                Returns None if there is no node in the dataabase with the
                requested property.
        """
        with self.driver.session() as session:
            result = session.execute_read(self._id_query, property_name, property_value)
        return result

    ##
    # \cond
    ##
    @staticmethod
    def _id_query(tx, property_name, property_value):
        result = tx.run(f'MATCH (n1 {{{property_name}: "{property_value}"}}) '
                        "RETURN id(n1) "
                        "LIMIT 1")
        result = result.single()
        if result is None:
            return None
        else:
            return result[0]
    ##
    # \endcond
    ##

    def query_property(self, id: int, property_name: str) -> str:
        r"""
        Find the requested property of a Neo4j node.

        For example, using the Neo4j movie database example, you can find the
        title of a movie node as follows.

        \code{python}
            import stag.neo4j
            g = stag.neo4j.Neo4jGraph("bolt://localhost:7687", "neo4j", "password")
            title = g.query_property(1, "title")
        \endcode

        @param id the Neo4j node ID to query
        @param property_name the name of the property to query
        @return the value of the requested property on the given node. Returns
                None if the requested property is not set on the requested node,
                or if the node id does not exist.
        """
        with self.driver.session() as session:
            result = session.execute_read(self._property_query, id, property_name)
        return result

    @lru_cache(maxsize=1024)
    def vertex_exists(self, v: int) -> bool:
        with self.driver.session() as session:
            result = session.execute_read(self._exists_query, v)
        return result

    ##
    # \cond
    ##
    @staticmethod
    def _exists_query(tx, id: int):
        result = tx.run('MATCH (n1) '
                        f"WHERE id(n1) = {id} "
                        "RETURN n1 "
                        "LIMIT 1")
        result = result.single()
        if result is None:
            return False
        else:
            return True
    ##
    # \endcond
    ##

    ##
    # \cond
    ##
    @staticmethod
    def _property_query(tx, node_id, property_name):
        result = tx.run("MATCH (n1) "
                        f"WHERE id(n1) = {node_id} "
                        f"RETURN (n1.{property_name}) "
                        "LIMIT 1")
        result = result.single()
        if result is None:
            return None
        else:
            return result[0]

    def __del__(self):
        # When the graph object it destroyed, close the connection to the backing
        # database.
        self.driver.close()
    ##
    # \endcond
    ##
