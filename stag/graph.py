from . import stag_internal
import scipy.sparse

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

    def __init__(self, adj_mat):
        """
        Initialise the graph with an adjacency matrix.

        :param adj_mat: A sparse scipy matrix.
        """
        # This class is essentially a thin wrapper around the stag_internal library, written in C++.
        # Initialise the internal graph object with the provided adjacency matrix.
        adj_mat_csr = adj_mat.tocsr()
        outer_starts = stag_internal.vectori(adj_mat_csr.indptr.tolist())
        inner_indices = stag_internal.vectori(adj_mat_csr.indices.tolist())
        values = stag_internal.vectord(adj_mat_csr.data.tolist())
        self.internal_graph = stag_internal.Graph(outer_starts, inner_indices, values)

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

    def volume(self):
        """
        The volume of the graph.

        The volume is defined as the sum of the node degrees.

        :return: the graph's volume.
        """
        return self.internal_graph.volume()
