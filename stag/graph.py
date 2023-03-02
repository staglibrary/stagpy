"""
Graph object definitions and standard constructors.
"""
import networkx
from abc import ABC, abstractmethod
from typing import List
import inspect

import scipy.sparse

from . import stag_internal
from . import utility


class Edge(object):
    """
    An object representing a weighted edge in a graph.
    """

    def __init__(self, v1: int, v2: int, weight: float):
        """
        Create an edge from two node ids and a weight.
        """
        ## The ID of the first vertex in the edge.
        self.v1 = v1

        ## The ID of the second vertex in the edge.
        self.v2 = v2

        ## The weight of the edge
        self.weight = weight

        ##
        # \cond
        ##
        self.internal_edge = stag_internal.edge()
        self.internal_edge.v1 = v1
        self.internal_edge.v2 = v2
        self.internal_edge.weight = weight
        ##
        # \endcond
        ##

    ##
    # \cond
    ##

    def __eq__(self, other):
        return self.v1 == other.v1 and self.v2 == other.v2 and self.weight == other.weight

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f"Edge({self.v1}, {self.v2}, weight={self.weight})"

    ##
    # \endcond
    ##


class LocalGraph(ABC):
    """
    \brief An abstract class which defines methods for exploring the
    local neighborhood of vertices in a graph.

    To maximise the performance of the local algorithms using this class,
    subclasses should cache the results of expensive queries. For example,
    if querying the neighbors of a vertex requires accessing the disk, then
    the result should be cached.
    """

    def __init__(self):
        r"""
        Default LocalGraph constructor.

        The constructor of any classes inheriting from this base class should
        call this constructor. For example:

        \code{python}
        import stag.graph
        class MyLocalGraph(stag.graph.LocalGraph):
          def __init__(self):
          super().__init__()

          # Add custom initialisation for MyLocalGraph
        \endcode
        """
        ##
        # \cond
        ##
        self.internal_graph = _PythonDefinedLocalGraph(self)
        ##
        # \endcond
        ##

    @abstractmethod
    def degree(self, v: int) -> float:
        """
        Given a vertex v, return its weighted degree.
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
        ``edge.v1 = v``.

        @param v the ID of some vertex in the graph
        @return a list of stag.graph.Edge objects containing the neighbourhood
                of v
        """
        pass

    @abstractmethod
    def neighbors_unweighted(self, v: int) -> List[int]:
        """
        Given a vertex v, return a list of neighbors of v.

        The weights of edges to the neighbors are not returned by this method.

        @param v the ID of some vertex in the graph
        @return a list of vertex IDs giving the neighbours of v
        """
        pass

    def degrees(self, vertices: List[int]) -> List[float]:
        """
        Given a list of vertices, return a list of their weighted degrees.

        When developing implementations of the stag.graph.LocalGraph class,
        providing an efficient method of returning a list of degrees will
        improve the performance of local clustering algorithms.

        @param vertices a list of IDs representing the vertices to be queried
        @return a list of degrees
        """
        return [self.degree(v) for v in vertices]

    def degrees_unweighted(self, vertices: List[int]) -> List[int]:
        """
        Given a list of vertices, return a list of their unweighted degrees.

        When developing implementations of the stag.graph.LocalGraph class,
        providing an efficient method of returning a list of degrees will
        improve the performance of local clustering algorithms.

        @param vertices a list of IDs representing the vertices to be queried
        @return a list of unweighted degrees
        """
        return [self.degree_unweighted(v) for v in vertices]

    @abstractmethod
    def vertex_exists(self, v: int) -> bool:
        r"""
        Given a vertex ID, returns true or false to indicate whether the vertex exists
        in the graph.

        @param v the vertex index to check
        @return a boolean indicating whether there exists a vertex with the given index
        """
        pass

##
# \cond
# Do not document python defined local graph
##

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

    def vertex_exists(self, v: int):
        return self.python_graph.vertex_exists(v)

##
# \endcond
##

class Graph(LocalGraph):
    """
    \brief The core object used to represent graphs for use with the library.

    Graphs are always constructed from sparse matrices, and this is the internal
    representation used as well.
    Vertices of the graph are always referred to by their unique integer index.
    This index corresponds to the position of the vertex in the stored adjacency
    matrix of the graph.
    """

    def __init__(self, adj_mat: scipy.sparse.spmatrix,
                 internal_graph: stag_internal.Graph = None):
        r"""
        Initialise the graph with an adjacency matrix.
        
        For example:

        \code{python}
        >>> import stag.graph
        >>> import scipy.sparse
        >>>
        >>> adj_mat = scipy.sparse.csc_matrix([[0, 1, 1, 1],
        ...                                    [1, 0, 1, 1],
        ...                                    [1, 1, 0, 1],
        ...                                    [1, 1, 1, 0]])
        >>> g = stag.graph.Graph(adj_mat)
        \endcode

        :param adj_mat: A sparse scipy matrix, such as ``scipy.sparse.csc_matrix``.
        :param internal_graph: (optional) specify a STAG C++ graph object to
                                initialise with. Use this only if you understand
                                the internal workings of the STAG library.
        """
        # Call the LocalGraph initialisation method - it is important that this
        # is called first. This is because we override the internal_graph
        # object in the current constructor.
        super().__init__()

        ##
        # \cond
        # Do not document the internal implementation of the graph object
        ##

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

        ##
        # \endcond
        ##

    @utility.return_sparse_matrix
    def adjacency(self) -> scipy.sparse.csc_matrix:
        """
        Return the sparse adjacency matrix of the graph.

        :return: a ``scipy.sparse.csc_matrix`` representing the graph adjacency matrix
        """
        return self.internal_graph.adjacency()

    @utility.return_sparse_matrix
    def laplacian(self) -> scipy.sparse.csc_matrix:
        """
        Construct the Laplacian matrix of the graph.

        The Laplacian matrix is defined by

        \f[
            L = D - A
        \f]

        where \f$D\f$ is the diagonal matrix of vertex degrees
        and \f$A\f$ is the adjacency matrix of the graph.

        :return: a ``scipy.sparse.csc_matrix`` representing the graph Laplacian
        """
        return self.internal_graph.laplacian()

    @utility.return_sparse_matrix
    def normalised_laplacian(self) -> scipy.sparse.csc_matrix:
        r"""
        Construct the normalised Laplacian matrix of the graph.

        The normalised Laplacian matrix is defined by

        \f[
            \mathcal{L} = D^{-1/2} L D^{-1/2}
        \f]

        where \f$D\f$ is the diagonal matrix of vertex degrees and \f$L\f$
        is the Laplacian matrix of the graph.

        :return: a ``scipy.sparse.csc_matrix`` representing the normalised Laplacian
        """
        return self.internal_graph.normalised_laplacian()

    @utility.return_sparse_matrix
    def normalised_laplacian(self) -> scipy.sparse.csc_matrix:
        r"""
        Construct the normalised Laplacian matrix of the graph.

        The normalised Laplacian matrix is defined by

        \f[
            \mathcal{L} = D^{-1/2} L D^{-1/2}
        \f]

        where \f$D\f$ is the diagonal matrix of vertex degrees and \f$L\f$
        is the Laplacian matrix of the graph.

        :return: a ``scipy.sparse.csc_matrix`` representing the normalised Laplacian
        """
        return self.internal_graph.normalised_laplacian()

    @utility.return_sparse_matrix
    def signless_laplacian(self) -> scipy.sparse.csc_matrix:
        """
        Construct the signless Laplacian matrix of the graph.

        The signless Laplacian matrix is defined by

        \f[
            J = D + A
        \f]

        where \f$D\f$ is the diagonal matrix of vertex degrees
        and \f$A\f$ is the adjacency matrix of the graph.

        :return: a ``scipy.sparse.csc_matrix`` representing the signless graph Laplacian
        """
        return self.internal_graph.signless_laplacian()

    @utility.return_sparse_matrix
    def normalised_signless_laplacian(self) -> scipy.sparse.csc_matrix:
        r"""
        Construct the normalised signless Laplacian matrix of the graph.

        The normalised signless Laplacian matrix is defined by

        \f[
            \mathcal{J} = D^{-1/2} J D^{-1/2}
        \f]

        where \f$D\f$ is the diagonal matrix of vertex degrees and \f$J\f$
        is the signless Laplacian matrix of the graph.

        :return: a ``scipy.sparse.csc_matrix`` representing the normalised signless Laplacian
        """
        return self.internal_graph.normalised_signless_laplacian()

    @utility.return_sparse_matrix
    def degree_matrix(self) -> scipy.sparse.csc_matrix:
        r"""
        The degree matrix of the graph.

        The degree matrix \f$D \in \mathbb{R}^{n \\times n}\f$
        is a diagonal matrix such that \f$D(i, i) = \mathrm{deg}(i)\f$
        where \f$\mathrm{deg}(i)\f$ is the degree of vertex \f$i\f$ and
        \f$n\f$ is the number of vertices in the graph.

        :return: a ``scipy.sparse.csc_matrix`` representing the degree matrix
        """
        return self.internal_graph.degree_matrix()
    
    @utility.return_sparse_matrix
    def inverse_degree_matrix(self) -> scipy.sparse.csc_matrix:
        r"""
        The inverse degree matrix of the graph.

        The degree matrix \f$D^{-1} \in \mathbb{R}^{n \times n}\f$
        is a diagonal matrix such that

        \f[
            D(i, i) =  \left\{
                    \begin{array}{lll}
                        \mathrm{deg}(i) & \mbox{if } \mathrm{deg}(i) > 0 \\
                        0 & \mbox{otherwise}
                    \end{array}
                \right.
        \f]

        where \f$\mathrm{deg}(i)\f$ is the degree of vertex \f$i\f$ and
        \f$n\f$ is the number of vertices in the graph.

        :return: a ``scipy.sparse.csc_matrix`` representing the inverse degree matrix
        """
        return self.internal_graph.inverse_degree_matrix()
    
    @utility.return_sparse_matrix
    def lazy_random_walk_matrix(self) -> scipy.sparse.csc_matrix:
        """
        The lazy random walk matrix of the graph.

        The lazy random walk matrix is defined by

        \f[
            W = \frac 1 2 I + \frac 1 2 A D^{-1}
        \f]

        where \f$I\f$ is the identity matrix, \f$A\f$ is the graph adjacency
        matrix and \f$D\f$ is the degree matrix of the graph.

        @return a ``scipy.sparse.csc_matrix`` representing the lazy random walk
                matrix
        """
        return self.internal_graph.lazy_random_walk_matrix()

    def total_volume(self) -> float:
        r"""
        The volume of the graph.

        The volume of a graph \f$G = (V, E, w)\f$ is defined by

        \f[
            \mathrm{vol}(G) = \sum_{u \in V} \mathrm{deg}(u),
        \f]

        where \f$\mathrm{deg}(u)\f$ is the degree of vertex \f$u\f$.

        :return: the graph's volume, \f$\mathrm{vol}(G)\f$
        """
        return self.internal_graph.total_volume()

    def average_degree(self) -> float:
        r"""
        The average degree of the graph.

        This is defined as the sum of the node degrees divided by the number of nodes.

        @return the graph's average degree.
        """
        return self.internal_graph.average_degree()

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

    def vertex_exists(self, v: int) -> bool:
        return self.internal_graph.vertex_exists(v)

    ##
    # \cond
    # Do not document the eq method for the graph object.
    ##
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

    ##
    # \endcond
    ##

    def to_networkx(self) -> networkx.Graph:
        """
        Construct a networkx graph object which is equivalent to this STAG graph.

        See the
        [networkx documentation](https://networkx.org/documentation/stable/reference/classes/graph.html).
        """
        return networkx.Graph(self.adjacency())

    def draw(self, **kwargs):
        """
        Plot the graph with matplotlib.

        This uses the networkx draw method and accepts any the keyword arguments
        will be passed through directly.

        \par Example

        \code{python}
        import matplotlib.pyplot as plt
        import stag.graph
        myGraph = stag.graph.star_graph(10)
        myGraph.draw()
        plt.show()
        \endcode
        """
        netx_graph = self.to_networkx()
        networkx.draw(netx_graph, **kwargs)

##
# \cond
# A decorator which transforms a graph returned from the C++ library to the
# python Graph object.
##
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

##
# \endcond
##

@return_graph
def cycle_graph(n) -> Graph:
    """
    Construct a cycle graph on n vertices.

    @param n the number of vertices in the constructed graph
    @return a stag.graph.Graph object representing a cycle graph
    """
    return stag_internal.cycle_graph(n)


@return_graph
def complete_graph(n) -> Graph:
    """
    Construct a complete graph on n vertices.

    @param n the number of vertices in the constructed graph
    @return a stag.graph.Graph object representing a complete graph
    """
    return stag_internal.complete_graph(n)


@return_graph
def barbell_graph(n) -> Graph:
    """
    Construct a barbell graph. The barbell graph consists of 2 cliques on n
    vertices, connected by a single edge.

    @param n the number of vertices in each of the two cliques.
             The returned graph will have \f$2n\f$ vertices.
    @return a stag.graph.Graph object representing the barbell graph
    """
    return stag_internal.barbell_graph(n)


@return_graph
def star_graph(n) -> Graph:
    """
    Construct a star graph. The star graph consists of one central vertex
    connected by an edge to n-1 outer vertices.

    @param n the number of vertices in the constructed graph
    @return a stag.graph.Graph object representing the star graph
    """
    return stag_internal.star_graph(n)


def from_networkx(netx_graph: networkx.Graph,
                  edge_weight_attribute: str = "weight"):
    """
    Given a networkx graph, convert it to a stag.graph.Graph object.

    Unless otherwise specified, this method will use the 'weight' attribute on the
    networkx edges to assign the weight of the edges. If no such attribute is present,
    the edges will be added with weight \f$1\f$.

    @param netx_graph The networkx graph object to be converted.
    @param edge_weight_attribute (default 'weight') the edge attribute to be used to
                                  generate the weights
    @return A stag.graph.Graph object which is equivalent to the networkx graph.
    """
    return Graph(networkx.adjacency_matrix(netx_graph,
                                           weight=edge_weight_attribute))
