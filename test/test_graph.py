"""
Tests for the graph object.
"""
import numpy as np
import scipy as sp
import scipy.sparse
import networkx
import pytest
from context import stag
import stag.graph
import stag.random
import stag.graphio

# Define the adjacency matrices of some useful graphs.
C4_ADJ_MAT = scipy.sparse.csc_matrix([[0, 1, 0, 1], [1, 0, 1, 0], [0, 1, 0, 1], [1, 0, 1, 0]])
K6_ADJ_MAT = scipy.sparse.csc_matrix([[0, 1, 1, 1, 1, 1], [1, 0, 1, 1, 1, 1], [1, 1, 0, 1, 1, 1],
                                      [1, 1, 1, 0, 1, 1], [1, 1, 1, 1, 0, 1], [1, 1, 1, 1, 1, 0]])
BARBELL5_ADJ_MAT = scipy.sparse.csc_matrix([[0, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                                            [1, 0, 1, 1, 1, 0, 0, 0, 0, 0],
                                            [1, 1, 0, 1, 1, 0, 0, 0, 0, 0],
                                            [1, 1, 1, 0, 1, 0, 0, 0, 0, 0],
                                            [1, 1, 1, 1, 0, 1, 0, 0, 0, 0],
                                            [0, 0, 0, 0, 1, 0, 1, 1, 1, 1],
                                            [0, 0, 0, 0, 0, 1, 0, 1, 1, 1],
                                            [0, 0, 0, 0, 0, 1, 1, 0, 1, 1],
                                            [0, 0, 0, 0, 0, 1, 1, 1, 0, 1],
                                            [0, 0, 0, 0, 0, 1, 1, 1, 1, 0],
                                            ])


def test_graph_constructor():
    # Start by constructing the cycle graph on 4 vertices.
    graph = stag.graph.Graph(C4_ADJ_MAT)

    # The graph has 4 vertices and 4 edges
    assert graph.number_of_vertices() == 4
    assert graph.number_of_edges() == 4

    # Check the vertex degrees
    for i in range(4):
        assert graph.degree(i) == 2

    # Now, try creating the complete graph on 6 vertices.
    graph = stag.graph.Graph(K6_ADJ_MAT)
    assert graph.number_of_vertices() == 6
    assert graph.number_of_edges() == 15
    for i in range(4):
        assert graph.degree(i) == 5

    # Now, try the barbell graph
    graph = stag.graph.Graph(BARBELL5_ADJ_MAT)
    assert graph.number_of_vertices() == 10
    assert graph.number_of_edges() == 21
    assert graph.degree(2) == 4
    assert graph.degree(4) == 5


def test_complete_graph():
    # Create a complete graph
    n = 4
    graph = stag.graph.complete_graph(n)
    expected_adjacency_matrix = sp.sparse.csc_matrix([[0, 1, 1, 1],
                                                      [1, 0, 1, 1],
                                                      [1, 1, 0, 1],
                                                      [1, 1, 1, 0]])

    assert graph.number_of_vertices() == 4
    adj_mat_diff = (graph.adjacency() - expected_adjacency_matrix)
    adj_mat_diff.eliminate_zeros()
    assert adj_mat_diff.nnz == 0

    expected_norm_lap = sp.sparse.csc_matrix([[1, -1/3, -1/3, -1/3],
                                              [-1/3, 1, -1/3, -1/3],
                                              [-1/3, -1/3, 1, -1/3],
                                              [-1/3, -1/3, -1/3, 1]])
    norm_lap_diff = (graph.normalised_laplacian() - expected_norm_lap)
    assert(np.all(norm_lap_diff.todense() == pytest.approx(0)))


def test_star_graph():
    # Create a star graph
    n = 5
    graph = stag.graph.star_graph(n)
    expected_adjacency_matrix = sp.sparse.csc_matrix([[0, 1, 1, 1, 1],
                                                      [1, 0, 0, 0, 0],
                                                      [1, 0, 0, 0, 0],
                                                      [1, 0, 0, 0, 0],
                                                      [1, 0, 0, 0, 0]])
    assert graph.number_of_vertices() == 5
    adj_mat_diff = (graph.adjacency() - expected_adjacency_matrix)
    adj_mat_diff.eliminate_zeros()
    assert adj_mat_diff.nnz == 0


def test_cycle_graph():
    # Create a cycle graph
    n = 5
    graph = stag.graph.cycle_graph(n)
    expected_adjacency_matrix = sp.sparse.csc_matrix([[0, 1, 0, 0, 1],
                                                      [1, 0, 1, 0, 0],
                                                      [0, 1, 0, 1, 0],
                                                      [0, 0, 1, 0, 1],
                                                      [1, 0, 0, 1, 0]])

    assert graph.number_of_vertices() == 5
    adj_mat_diff = (graph.adjacency() - expected_adjacency_matrix)
    adj_mat_diff.eliminate_zeros()
    assert adj_mat_diff.nnz == 0

    expected_laplacian_matrix = sp.sparse.csc_matrix([[2, -1, 0, 0, -1],
                                                      [-1, 2, -1, 0, 0],
                                                      [0, -1, 2, -1, 0],
                                                      [0, 0, -1, 2, -1],
                                                      [-1, 0, 0, -1, 2]])
    lap_diff = (graph.laplacian() - expected_laplacian_matrix)
    lap_diff.eliminate_zeros()
    assert lap_diff.nnz == 0


def test_adjacency_matrix():
    graph = stag.graph.Graph(BARBELL5_ADJ_MAT)
    adj_mat_diff = (graph.adjacency() - BARBELL5_ADJ_MAT)
    adj_mat_diff.eliminate_zeros()
    assert adj_mat_diff.nnz == 0


def test_symmetry():
    # Generate a large graph from the stochastic block model
    big_graph = stag.random.sbm(1000, 5, 0.8, 0.2)

    # Check that all of the graph matrices are truly symmetric
    assert np.allclose(big_graph.adjacency().toarray(), big_graph.adjacency().toarray().T)

    lap_mat = big_graph.normalised_laplacian()
    lap_mat_dense = lap_mat.toarray()
    assert np.allclose(lap_mat_dense, lap_mat_dense.T)

    lap_mat = big_graph.laplacian()
    lap_mat_dense = lap_mat.toarray()
    assert np.allclose(lap_mat_dense, lap_mat_dense.T)


def test_num_edges():
    # Generate a known graph
    graph = stag.graph.Graph(BARBELL5_ADJ_MAT)

    # Check the number of edges in the graph
    assert graph.number_of_vertices() == 10
    assert graph.number_of_edges() == 21
    assert graph.total_volume() == 42

    # Now create a weighted graph and check the number of edges method.
    adjacency_matrix = scipy.sparse.csc_matrix([[0, 2, 0, 1],
                                                [2, 0, 3, 0],
                                                [0, 3, 0, 1],
                                                [1, 0, 1, 0]])
    graph = stag.graph.Graph(adjacency_matrix)
    assert graph.number_of_vertices() == 4
    assert graph.number_of_edges() == 4
    assert graph.total_volume() == 14


def test_float_weights():
    # Create a graph with floating-point edge weights.
    adjacency_matrix = scipy.sparse.csc_matrix([[0, 2.2, 0, 1],
                                                [2.2, 0, 3.1, 0],
                                                [0, 3.1, 0, 1.09],
                                                [1, 0, 1.09, 0]])
    graph = stag.graph.Graph(adjacency_matrix)
    assert graph.number_of_vertices() == 4
    assert graph.number_of_edges() == 4
    assert graph.total_volume() == pytest.approx(14.78)
    assert graph.degree(0) == pytest.approx(3.2)
    assert graph.degree(2) == pytest.approx(4.19)

    # Check the unweighted degrees
    assert graph.degree_unweighted(0) == 2
    assert graph.degree_unweighted(2) == 2


def test_networkx():
    # Test the methods for converting from and to networkx graphs.
    # Start by constructing a networkx graph
    netx_graph = networkx.generators.barbell_graph(4, 1)
    graph = stag.graph.from_networkx(netx_graph)

    assert graph.number_of_vertices() == 9
    assert graph.number_of_edges() == 14

    expected_adjacency_matrix = sp.sparse.csc_matrix([[0, 1, 1, 1, 0, 0, 0, 0, 0],
                                                      [1, 0, 1, 1, 0, 0, 0, 0, 0],
                                                      [1, 1, 0, 1, 0, 0, 0, 0, 0],
                                                      [1, 1, 1, 0, 0, 0, 0, 0, 1],
                                                      [0, 0, 0, 0, 0, 1, 1, 1, 1],
                                                      [0, 0, 0, 0, 1, 0, 1, 1, 0],
                                                      [0, 0, 0, 0, 1, 1, 0, 1, 0],
                                                      [0, 0, 0, 0, 1, 1, 1, 0, 0],
                                                      [0, 0, 0, 1, 1, 0, 0, 0, 0]])
    adj_mat_diff = (graph.adjacency() - expected_adjacency_matrix)
    adj_mat_diff.eliminate_zeros()
    assert adj_mat_diff.nnz == 0

    # Now, construct a graph using the sgtl Graph object, and convert it to networkx
    graph = stag.graph.Graph(expected_adjacency_matrix)
    netx_graph = graph.to_networkx()

    # Check that the networkx graph looks correct
    assert netx_graph.number_of_nodes() == 9
    assert netx_graph.number_of_edges() == 14
    assert netx_graph.has_edge(0, 1)
    assert netx_graph.has_edge(3, 8)
    assert netx_graph.has_edge(8, 4)
    assert not netx_graph.has_edge(2, 8)


def test_degree_matrix():
    # Construct a graph and get its degree matrix
    g = stag.graph.barbell_graph(4)
    expected_degree_mat = sp.sparse.diags([3, 3, 3, 4, 4, 3, 3, 3])
    deg_mat_diff = g.degree_matrix() - expected_degree_mat
    assert(np.all(deg_mat_diff.todense() == pytest.approx(0)))


def test_inverse_degree_matrix():
    # Construct a graph and get its inverse degree matrix
    g = stag.graph.barbell_graph(4)
    expected_inv_degree_mat = sp.sparse.diags([1/3, 1/3, 1/3, 1/4, 1/4, 1/3, 1/3, 1/3])
    inv_deg_mat_diff = g.inverse_degree_matrix() - expected_inv_degree_mat
    assert(np.all(inv_deg_mat_diff.todense() == pytest.approx(0)))


def test_lazy_random_walk_matrix():
    # Construct a graph
    g = stag.graph.barbell_graph(3)
    expected_rw_mat = sp.sparse.csc_matrix([[1/2, 1/4, 1/6,   0,   0,   0],
                                            [1/4, 1/2, 1/6,   0,   0,   0],
                                            [1/4, 1/4, 1/2, 1/6,   0,   0],
                                            [  0,   0, 1/6, 1/2, 1/4, 1/4],
                                            [  0,   0,   0, 1/6, 1/2, 1/4],
                                            [  0,   0,   0, 1/6, 1/4, 1/2]])
    rw_mat_diff = g.lazy_random_walk_matrix() - expected_rw_mat
    assert(np.all(rw_mat_diff.todense() == pytest.approx(0)))


def test_edge():
    # Test the edge object
    e = stag.graph.Edge(1, 2, 0.3)
    assert(e.v1 == 1)
    assert(e.v2 == 2)
    assert(e.weight == 0.3)

    # Define two edges and make sure they are equal
    e2 = stag.graph.Edge(1, 2, 0.3)
    assert(e == e2)

    # Define a different edge
    e3 = stag.graph.Edge(1, 3, 0.2)
    assert (e2 != e3)


def test_graph_equality():
    g1 = stag.graph.complete_graph(6)
    g2 = stag.graph.complete_graph(6)
    assert g1 == g2

    g3 = stag.graph.Graph(K6_ADJ_MAT)
    assert g2 == g3

    g4 = stag.graph.Graph(BARBELL5_ADJ_MAT)
    assert g2 != g4

    g5 = stag.graph.barbell_graph(5)
    assert g4 == g5


def test_graph_degrees():
    g1 = stag.graph.barbell_graph(4)
    degrees = g1.degrees_unweighted([0, 1, 2, 3, 4, 5])
    assert degrees == [3, 3, 3, 4, 4, 3]


def test_graph_average_degree():
    g = stag.graph.barbell_graph(4)
    avg_degree = g.average_degree()
    assert avg_degree == 26/8
