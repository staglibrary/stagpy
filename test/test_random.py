"""
Tests for the random module.
"""
import pytest
import numpy as np
from context import stag
import stag.random


def test_sbm():
    # Generate a graph with a fixed p and q
    n = 2000
    p = 0.8
    q = 0.2
    graph = stag.random.sbm(n, 4, p, q, exact=True)
    assert graph.number_of_vertices() == 2000

    # The adjacency matrix should be symmetric
    sym_diff = (graph.adjacency() - graph.adjacency().transpose())
    sym_diff.eliminate_zeros()
    assert sym_diff.nnz == 0

    # The number of edges should be about
    # n * ((n/4) * p + (3 * n/4) * q)
    assert abs((graph.total_volume() / (n * ((n/4) * p + (3 * n/4) * q))) - 1) <= 0.1

    # The approximate version should give approximately the same number of edges
    graphapx = stag.random.sbm(n, 4, p, q)
    assert graphapx.number_of_vertices() == n
    assert abs((graphapx.number_of_edges() / graph.number_of_edges()) - 1) <= 0.5


def test_general_sbm():
    # Key thing to test is that the parameters go through to C++
    cluster_sizes = [10, 100, 1000]
    probabilities = np.asarray([[0.9, 0.1, 0.01],
                                [0.1, 0.9, 0.2],
                                [0.01, 0.2, 0.1]])
    g = stag.random.general_sbm(cluster_sizes, probabilities)
    assert g.number_of_vertices() == 1110
    assert g.number_of_edges() > 30000


def test_erdos_renyi():
    # Generate a graph
    n = 1000
    graph = stag.random.erdos_renyi(n, 0.1, exact=True)

    # Check that the graph has the expected number of vertices and edges.
    assert graph.number_of_vertices() == n
    assert abs((graph.total_volume() / (int(2 * 0.1 * (n * (n - 1)) / 2) + n)) - 1) <= 0.1

def test_sbm_gt_labels():
    n = 6
    k = 3
    labels = stag.random.sbm_gt_labels(n, k)
    assert labels == [0, 0, 1, 1, 2, 2]

def test_general_sbm_gt_labels():
    cluster_sizes = [4, 2]
    gt_labels = stag.random.general_sbm_gt_labels(cluster_sizes)
    assert gt_labels == [0, 0, 0, 0, 1, 1]
