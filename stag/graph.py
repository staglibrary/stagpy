"""
Graph object definitions and standard constructors.
"""
import networkx
from abc import ABC, abstractmethod
from typing import List
import inspect

from . import stag_internal
from . import utility


class Edge(object):
    """
    An object representing a weighted edge in a graph.

    Instances of this class have the following members:

    * ``v1: int`` : the first vertex in the edge
    * ``v2: int`` : the second vertex in the edge
    * ``weight: float`` : the weight of the edge
    """

    def __init__(self, v1: int, v2: int, weight: float):
        """
        Create an edge from two node ids and a weight.
        """
        self.v1 = v1
        self.v2 = v2
        self.weight = weight
        self.internal_edge = stag_internal.edge()
        self.internal_edge.v1 = v1
        self.internal_edge.v2 = v2
        self.internal_edge.weight = weight

    def __eq__(self, other):
        return self.v1 == other.v1 and self.v2 == other.v2 and self.weight == other.weight

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f"Edge({self.v1}, {self.v2}, weight={self.weight})"


class LocalGraph(ABC):
    """
    An abstract class representing local graph operations.
    For now, this class inherits directly from the internal local graph class.
    This 'intermediate' class is included for possible future python-specific functionality.
    """

    def __init__(self):
        """
        Base constructor.

        The constructor of any classes inheriting from this base class should
        call this constructor. For example:

        .. code-block:: python

            class MyLocalGraph(stag.graph.LocalGraph):
              def __init__(self):
                super().__init__(self)

                # Add custom initialisation for MyLocalGraph

        """
        self.internal_graph = _PythonDefinedLocalGraph(self)

    @abstractmethod
    def degree(self, v: int) -> float:
        """
        Given a vertex v, return its weighted degree.

        Given a graph :math:`G = (V, E, w)`, the degree ov vertex :math:`v` is
        defined by

        .. math::

            \mathrm{deg}(v) = \sum_{u \in V} w(v, u).

        """
        pass

    @abstractmethod
    def degree_unweighted(self, v: int) -> int:
        """
        Given a vertex v, return its unweighted degree. That is, the number of
        neighbors of v, ignoring the edge weights.
        """
        pass

    @abstractmethod
    def neighbors(self, v: int) -> List[Edge]:
        """
        Given a vertex v, return a list of edges representing the
        neighbors of v.

        The returned edge objects will all have the ordering ``(v1, v2)`` such that
        ``edge.v1 = v`` and ``edge.v2`` is a neighbor of ``v``.
        """
        pass

    @abstractmethod
    def neighbors_unweighted(self, v: int) -> List[int]:
        """
        Given a vertex v, return a list of neighbors of v.

        The weights of edges to the neighbors are not returned by this method.
        """
        pass

    def degrees(self, vertices: List[int]) -> List[float]:
        """
        Given a list of vertices, return a list of their weighted degrees.

        When developing implementations of the :class:`LocalGraph` class,
        providing an efficient method of returning a list of degrees will
        improve the performance of local clustering algorithms.
        """
        return [self.degree(v) for v in vertices]

    def degrees_unweighted(self, vertices: List[int]) -> List[int]:
        """
        Given a list of vertices, return a list of their unweighted degrees.

        When developing implementations of the :class:`LocalGraph` class,
        providing an efficient method of returning a list of degrees will
        improve the performance of local clustering algorithms.
        """
        return [self.degree_unweighted(v) for v in vertices]


class _PythonDefinedLocalGraph(stag_internal.LocalGraph):
    def __init__(self, python_local_graph: LocalGraph):
        super().__init__()
        self.python_graph = python_local_graph

    def degree(self, v: int):
        return self.python_graph.degree(v)

    def degree_unweighted(self, v: int):
        return self.python_graph.degree_unweighted(v)

    def neighbors(self, v: int):
        return [e.internal_edge for e in self.python_graph.neighbors(v)]

    def neighbors_unweighted(self, v: int):
        return self.python_graph.neighbors_unweighted(v)

    def degrees(self, vertices: List[int]):
        return self.python_graph.degrees(vertices)

    def degrees_unweighted(self, vertices):
        return self.python_graph.degrees_unweighted(vertices)


class Graph(LocalGraph):
    """
    Graph(adj_mat)

    Core graph object.

    The graph object is initialised with a sparse adjacency matrix and this
    is used directly as the internal representation of the graph.

    Throughout the library, we use the scipy sparse matrix
    object. It may be useful to refer to the
    `scipy.sparse documentation <https://docs.scipy.org/doc/scipy/reference/sparse.html>`_.
    Matrices returned by STAG methods will be instances of the
    ``scipy.sparse.csc_matrix`` class.

    This graph object cannot be dynamically updated.
    It is initialised with an adjacency matrix.
    Vertices are always referred to by their index in the adjacency matrix.
    """

    def __init__(self, adj_mat, internal_graph=None):
        """
        __init__(adj_mat)

        Initialise the graph with an adjacency matrix.
        
        For example:
        
        .. code-block:: python
        
            import stag.graph
            import scipy.sparse
            
            adj_mat = scipy.sparse.csc_matrix([[0, 1, 1, 1],
                                               [1, 0, 1, 1],
                                               [1, 1, 0, 1],
                                               [1, 1, 1, 0]])
            g = stag.graph.Graph(adj_mat)

        :param adj_mat: A sparse scipy matrix, such as ``scipy.sparse.csc_matrix``.
        """
        # Call the LocalGraph initialisation method - it is important that this
        # is called first. This is because we override the internal_graph
        # object in the current constructor.
        super().__init__()

        # This class is essentially a thin wrapper around the stag_internal library, written in C++.
        if internal_graph is None:
            # Initialise the internal graph object with the provided adjacency matrix.
            adj_mat_csr = adj_mat.tocsr()
            outer_starts = stag_internal.vectorl(adj_mat_csr.indptr.tolist())
            inner_indices = stag_internal.vectorl(adj_mat_csr.indices.tolist())
            values = stag_internal.vectord(adj_mat_csr.data.tolist())
            self.internal_graph: stag_internal.Graph = stag_internal.Graph(outer_starts, inner_indices, values)
        else:
            # The initialiser was called with an internal graph object.
            self.internal_graph: stag_internal.Graph = internal_graph

    @utility.return_sparse_matrix
    def adjacency(self):
        """
        Return the sparse adjacency matrix of the graph.

        :return: a ``scipy.sparse.csc_matrix`` representing the graph adjacency matrix
        """
        return self.internal_graph.adjacency()

    @utility.return_sparse_matrix
    def laplacian(self):
        """
        Construct the Laplacian matrix of the graph.

        The Laplacian matrix is defined by

        .. math::

            L = D - A

        where :math:`D` is the diagonal matrix of vertex degrees
        and :math:`A` is the adjacency matrix of the graph.

        :return: a ``scipy.sparse.csc_matrix`` representing the graph Laplacian
        """
        return self.internal_graph.laplacian()

    @utility.return_sparse_matrix
    def normalised_laplacian(self):
        """
        Construct the normalised Laplacian matrix of the graph.

        The normalised Laplacian matrix is defined by

        .. math::

            \mathcal{L} = D^{-1/2} L D^{-1/2}

        where :math:`D` is the diagonal matrix of vertex degrees and :math:`L`
        is the Laplacian matrix of the graph.

        :return: a ``scipy.sparse.csc_matrix`` representing the normalised Laplacian
        """
        return self.internal_graph.normalised_laplacian()

    @utility.return_sparse_matrix
    def degree_matrix(self):
        """
        The degree matrix of the graph.

        The degree matrix :math:`D \in \mathbb{R}^{n \\times n}`
        is a diagonal matrix such that :math:`D(i, i) = \mathrm{deg}(i)`
        where :math:`\mathrm{deg}(i)` is the degree of vertex :math:`i` and
        :math:`n` is the number of vertices in the graph.

        :return: a ``scipy.sparse.csc_matrix`` representing the degree matrix
        """
        return self.internal_graph.degree_matrix()
    
    @utility.return_sparse_matrix
    def inverse_degree_matrix(self):
        """
        The inverse degree matrix of the graph.

        The degree matrix :math:`D^{-1} \in \mathbb{R}^{n \\times n}`
        is a diagonal matrix such that

        .. math::

            D(i, i) =  \\left\\{
                    \\begin{array}{lll}
                        \\mathrm{deg}(i) & \\mbox{if } \\mathrm{deg}(i) > 0 \\\\
                        0 & \\mbox{otherwise}
                    \\end{array}
                \\right.

        where :math:`\mathrm{deg}(i)` is the degree of vertex :math:`i` and
        :math:`n` is the number of vertices in the graph.

        :return: a ``scipy.sparse.csc_matrix`` representing the inverse degree matrix
        """
        return self.internal_graph.inverse_degree_matrix()
    
    @utility.return_sparse_matrix
    def lazy_random_walk_matrix(self):
        """
        The lazy random walk matrix of the graph.

        The lazy random walk matrix is defined by

        .. math::

            W = \\frac 1 2 I + \\frac 1 2 A D^{-1}

        where :math:`I` is the identity matrix, :math:`A` is the graph adjacency
        matrix and :math:`D` is the degree matrix of the graph.

        :return: a ``scipy.sparse.csc_matrix`` representing the lazy random walk
                 matrix

        """
        return self.internal_graph.lazy_random_walk_matrix()

    def total_volume(self) -> float:
        """
        The volume of the graph.

        The volume of a graph :math:`G = (V, E, w)` is defined by

        .. math::

            \mathrm{vol}(G) = \sum_{u \in V} \mathrm{deg}(u),

        where :math:`\mathrm{deg}(u)` is the degree of vertex :math:`u`.

        :return: the graph's volume, :math:`\mathrm{vol}(G)`
        """
        return self.internal_graph.total_volume()

    def number_of_vertices(self) -> int:
        """The number of vertices in the graph."""
        return self.internal_graph.number_of_vertices()

    def number_of_edges(self) -> int:
        """
        The number of edges in the graph.

        This method ignores the weights of the edges.
        """
        return self.internal_graph.number_of_edges()

    def degree(self, v: int) -> float:
        return self.internal_graph.degree(v)

    def degree_unweighted(self, v: int) -> int:
        return self.internal_graph.degree_unweighted(v)

    def neighbors(self, v: int) -> List[Edge]:
        return self.internal_graph.neighbors(v)

    def neighbors_unweighted(self, v: int) -> List[int]:
        return self.internal_graph.neighbors_unweighted(v)

    def __eq__(self, other):
        #
        # IMPORTANT NOTE
        # Checking whether two graphs are the same is thought to be a 'difficult'
        # problem, and so this method does not really check for mathematical equivalence.
        # Rather, we just check that the adjacency matrices are the same. As such, this method
        # should not be relied on to test for graph isomorphism!
        #

        # Check basic size information about the two graphs first
        if self.number_of_vertices() != other.number_of_vertices():
            return False

        if self.number_of_edges() != other.number_of_edges():
            return False

        # Check that the data vectors of the graph adjacency matrices are equal.
        a1 = self.internal_graph.adjacency()
        a2 = other.internal_graph.adjacency()
        if stag_internal.sprsMatOuterStarts(a1) != stag_internal.sprsMatOuterStarts(a2):
            return False
        if stag_internal.sprsMatInnerIndices(a1) != stag_internal.sprsMatInnerIndices(a2):
            return False
        return stag_internal.sprsMatValues(a1) == stag_internal.sprsMatValues(a2)

    def __ne__(self, other):
        return not self.__eq__(other)

    def to_networkx(self):
        """
        Construct a networkx graph object which is equivalent to this STAG graph.

        See the
        `networkx documentation <https://networkx.org/documentation/stable/reference/classes/graph.html>`_.
        """
        return networkx.Graph(self.adjacency())


# A decorator which transforms a graph returned from the C++ library to the
# python Graph object.
def return_graph(func):
    def decorated_function(*args, **kwargs):
        swig_graph = func(*args, **kwargs)
        return Graph(None, internal_graph=swig_graph)

    # Set the metadata of the returned function to match the original.
    # This is used when generating the documentation
    decorated_function.__doc__ = func.__doc__
    decorated_function.__module__ = func.__module__
    decorated_function.__signature__ = inspect.signature(func)

    return decorated_function


@return_graph
def cycle_graph(n) -> Graph:
    """
    Construct a cycle graph on :math:`n` vertices.
    """
    return stag_internal.cycle_graph(n)


@return_graph
def complete_graph(n) -> Graph:
    """
    Construct a complete graph on :math:`n` vertices.
    """
    return stag_internal.complete_graph(n)


@return_graph
def barbell_graph(n) -> Graph:
    """
    Construct a barbell graph on :math:`2n` vertices.

    The barbell graph consists of 2 cliques on :math:`n` vertices,
    connected by a single edge.
    """
    return stag_internal.barbell_graph(n)


@return_graph
def star_graph(n) -> Graph:
    """
    Construct a star graph on :math:`n` vertices.

    The star graph consists of one central vertex connected
    by an edge to :math:`(n-1)` surrounding vertices.
    """
    return stag_internal.star_graph(n)


def from_networkx(netx_graph, edge_weight_attribute="weight"):
    """
    Given a networkx graph, convert it to a STAG :class:`Graph` object.

    Unless otherwise specified, this method will use the 'weight' attribute on the
    networkx edges to assign the weight of the edges. If no such attribute is present,
    the edges will be added with weight :math:`1`.

    :param netx_graph: The networkx graph object to be converted.
    :param edge_weight_attribute: (default 'weight') the edge attribute to be used to
                                  generate the weights
    :return: A STAG :class:`Graph` object which is equivalent to the networkx graph.
    """
    return Graph(networkx.adjacency_matrix(netx_graph, weight=edge_weight_attribute))
