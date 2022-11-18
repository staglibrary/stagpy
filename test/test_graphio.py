"""
Tests for handling reading and writing graphs to disk.
"""
import scipy as sp
import scipy.sparse
from context import stag
import stag.graph
import stag.random
import stag.graphio


def test_edgelist():
    ##########
    # TEST 1 #
    ##########
    # Let's load the different test graphs, and check that we get what we'd expect.
    expected_adj_mat = sp.sparse.csc_matrix([[0, 1, 1],
                                             [1, 0, 1],
                                             [1, 1, 0]])
    graph = stag.graphio.load_edgelist("data/test1.edgelist")
    adj_mat_diff = (graph.adjacency() - expected_adj_mat)
    adj_mat_diff.eliminate_zeros()
    assert adj_mat_diff.nnz == 0

    # Now save and reload the graph and check that the adjacency matrix has not changed
    stag.graphio.save_edgelist(graph, "data/temp.edgelist")
    graph = stag.graphio.load_edgelist("data/temp.edgelist")
    adj_mat_diff = (graph.adjacency() - expected_adj_mat)
    adj_mat_diff.eliminate_zeros()
    assert adj_mat_diff.nnz == 0

    ##########
    # TEST 2 #
    ##########
    expected_adj_mat = sp.sparse.csc_matrix([[0, 0.5, 0.5],
                                             [0.5, 0, 1],
                                             [0.5, 1, 0]])
    graph = stag.graphio.load_edgelist("data/test2.edgelist")
    adj_mat_diff = (graph.adjacency() - expected_adj_mat)
    adj_mat_diff.eliminate_zeros()
    assert adj_mat_diff.nnz == 0

    # Now save and reload the graph and check that the adjacency matrix has not changed
    stag.graphio.save_edgelist(graph, "data/temp.edgelist")
    graph = stag.graphio.load_edgelist("data/temp.edgelist")
    adj_mat_diff = (graph.adjacency() - expected_adj_mat)
    adj_mat_diff.eliminate_zeros()
    assert adj_mat_diff.nnz == 0

    ##########
    # TEST 3 #
    ##########
    expected_adj_mat = sp.sparse.csc_matrix([[0, 1, 0.5],
                                             [1, 0, 1],
                                             [0.5, 1, 0]])
    graph = stag.graphio.load_edgelist("data/test3.edgelist")
    adj_mat_diff = (graph.adjacency() - expected_adj_mat)
    adj_mat_diff.eliminate_zeros()
    assert adj_mat_diff.nnz == 0

    # Now save and reload the graph and check that the adjacency matrix has not changed
    stag.graphio.save_edgelist(graph, "data/temp.edgelist")
    graph = stag.graphio.load_edgelist("data/temp.edgelist")
    adj_mat_diff = (graph.adjacency() - expected_adj_mat)
    adj_mat_diff.eliminate_zeros()
    assert adj_mat_diff.nnz == 0

    ##########
    # TEST 4 #
    ##########
    expected_adj_mat = sp.sparse.csc_matrix([[0, 1, 0.5],
                                             [1, 0, 1],
                                             [0.5, 1, 0]])
    graph = stag.graphio.load_edgelist("data/test4.edgelist")
    adj_mat_diff = (graph.adjacency() - expected_adj_mat)
    adj_mat_diff.eliminate_zeros()
    assert adj_mat_diff.nnz == 0

    # Now save and reload the graph and check that the adjacency matrix has not changed
    stag.graphio.save_edgelist(graph, "data/temp.edgelist")
    graph = stag.graphio.load_edgelist("data/temp.edgelist")
    adj_mat_diff = (graph.adjacency() - expected_adj_mat)
    adj_mat_diff.eliminate_zeros()
    assert adj_mat_diff.nnz == 0

    ##########
    # TEST 5 #
    ##########
    expected_adj_mat = sp.sparse.csc_matrix([[0, 0.5, 0.5],
                                             [0.5, 0, 1],
                                             [0.5, 1, 0]])
    graph = stag.graphio.load_edgelist("data/test5.edgelist")
    adj_mat_diff = (graph.adjacency() - expected_adj_mat)
    adj_mat_diff.eliminate_zeros()
    assert adj_mat_diff.nnz == 0

    # Now save and reload the graph and check that the adjacency matrix has not changed
    stag.graphio.save_edgelist(graph, "data/temp.edgelist")
    graph = stag.graphio.load_edgelist("data/temp.edgelist")
    adj_mat_diff = (graph.adjacency() - expected_adj_mat)
    adj_mat_diff.eliminate_zeros()
    assert adj_mat_diff.nnz == 0
