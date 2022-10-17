import networkx

from . import stag_internal
from .utility import return_sparse_matrix


class Graph:
    """
    Represents a graph. We keep things very simple - a graph is represented by its sparse adjacency matrix.

    In the general case, this allows for
      - directed and undirected graphs
      - self-loops

    If you'd like to store meta-data about the graph, such as node or edge labels, you should implement a subclass of
    this one, and add that information yourself.

    This graph cannot be dynamically updated. It must be initialised with the complete adjacency matrix.
    Vertices are referred to by their index in the adjacency matrix.
    """

    def __init__(self, adj_mat, internal_graph=None):
        """
        Initialise the graph with an adjacency matrix.

        :param adj_mat: A sparse scipy matrix.
        :param from_internal:
        """
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

    @return_sparse_matrix
    def adjacency(self):
        """
        Return the sparse adjacency matrix of the graph.

        :return: a sparse matrix representing the graph adjacency matrix
        """
        return self.internal_graph.adjacency()

    @return_sparse_matrix
    def laplacian(self):
        """
        Construct the Laplacian matrix of the graph.

        The Laplacian matrix is defined by
          L = D - A
        where D is the diagonal matrix of vertex degrees and A is the adjacency
        matrix of the graph.

        :return: a sparse matrix representing the graph Laplacian
        """
        return self.internal_graph.laplacian()

    @return_sparse_matrix
    def normalised_laplacian(self):
        """
        Construct the normalised Laplacian matrix of the graph.

        The normalised Laplacian matrix is defined by
          Ln = D^{-1/2} L D^{-1/2}
        where D is the diagonal matrix of vertex degrees and L is the Laplacian
        matrix of the graph

        :return: a sparse matrix representing the normalised Laplacian
        """
        return self.internal_graph.normalised_laplacian()

    @return_sparse_matrix
    def degree_matrix(self):
        """
        The degree matrix of the graph.

        The degree matrix is an n x n matrix such that each diagonal entry is the degree
        of the corresponding node.

        :return: the sparse degree matrix
        """
        return self.internal_graph.degree_matrix()
    
    @return_sparse_matrix
    def inverse_degree_matrix(self):
        """
        The inverse degree matrix of the graph.

        The inverse degree matrix is an n x n matrix such that each diagonal entry is
        the inverse of the degree of the corresponding node, or 0 if the node
        has degree 0.

        :return: the sparse inverse degree matrix
        """
        return self.internal_graph.inverse_degree_matrix()
    
    @return_sparse_matrix
    def lazy_random_walk_matrix(self):
        """
        The lazy random walk matrix of the graph.

        The lazy random walk matrix is defined to be
           1/2 I + 1/2 A D^{-1}
        where I is the identity matrix, A is the graph adjacency matrix and
        D is the degree matrix of the graph.

        :return: the sparse lazy random walk matrix
        """
        return self.internal_graph.lazy_random_walk_matrix()

    def total_volume(self):
        """
        The volume of the graph.

        The volume is defined as the sum of the node degrees.

        :return: the graph's volume.
        """
        return self.internal_graph.total_volume()

    def number_of_vertices(self):
        """The number of vertices in the graph."""
        return self.internal_graph.number_of_vertices()

    def number_of_edges(self):
        """
        The number of edges in the graph.

        This is defined based on the number of non-zero elements in the adjacency
        matrix, and ignores the weights of the edges.
        """
        return self.internal_graph.number_of_edges()

    def degree(self, vertex: int):
        return self.internal_graph.degree(vertex)

    def degree_unweighted(self, vertex: int):
        return self.internal_graph.degree_unweighted(vertex)

    def neighbors(self, vertex: int):
        return self.internal_graph.neighbors(vertex)

    def neighbors_unweighted(self, vertex: int):
        return self.internal_graph.neighbors_unweighted(vertex)

    def to_networkx(self):
        """
        Construct a networkx graph object which is equivalent to this STAG graph.
        """
        return networkx.Graph(self.adjacency())


def cycle_graph(n):
    """
    Construct a cycle graph on n vertices.

    :param n:
    :return: a graph object representing the n-cycle
    """
    return Graph(None, internal_graph=stag_internal.cycle_graph(n))


def complete_graph(n):
    """
    Construct a complete graph on n vertices.

    :param n:
    :return: a graph object representing the complete graph
    """
    return Graph(None, internal_graph=stag_internal.complete_graph(n))


def from_networkx(netx_graph, edge_weight_attribute="weight"):
    """
    Given a networkx graph, convert it to a STAG graph object.

    Unless otherwise specified, this method will use the 'weight' attribute on the
    networkx edges to assign the weight of the edges. If no such attribute is present,
    the edges will be added with weight 1.

    :param netx_graph: The networkx graph object to be converted.
    :param edge_weight_attribute: (default 'weight') the edge attribute to be used to
                                  generate the weights
    :return: A STAG graph object which is equivalent to the networkx graph.
    """
    return Graph(networkx.adjacency_matrix(netx_graph, weight=edge_weight_attribute))
