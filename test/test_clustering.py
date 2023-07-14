"""Tests for the clustering algorithms."""
import scipy.sparse
import pytest
import numpy as np
from context import stag
import stag.graph
import stag.cluster
import stag.random

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

def test_spectral_clustering():
    graph = stag.graph.barbell_graph(10)
    labels = stag.cluster.spectral_cluster(graph, 2)
    gt_labels = stag.random.sbm_gt_labels(20, 2)
    assert stag.cluster.adjusted_rand_index(gt_labels, labels) == 1


def test_cheeger_cut():
    graph = stag.graph.barbell_graph(10)
    labels = stag.cluster.cheeger_cut(graph)
    gt_labels = stag.random.sbm_gt_labels(20, 2)
    assert stag.cluster.adjusted_rand_index(gt_labels, labels) == 1


def test_default_local_clustering():
    # Construct a graph object with the barbell adjacency matrix
    graph = stag.graph.Graph(BARBELL5_ADJ_MAT)

    # Find a local cluster near the first vertex
    cluster = stag.cluster.local_cluster(graph, 1, 21)

    # Assert that the correct clusters have been found.
    assert (set(cluster) == {0, 1, 2, 3, 4})


def test_local_clustering_float_weight():
    # Construct a graph object with the barbell adjacency matrix
    graph = stag.graph.Graph(BARBELL5_ADJ_MAT)

    # Find a local cluster near the first vertex
    cluster = stag.cluster.local_cluster(graph, 1, 20.23)

    # Assert that the correct clusters have been found.
    assert (set(cluster) == {0, 1, 2, 3, 4})


def test_acl_local_clustering():
    # Construct a graph object with a well-defined cluster structure
    graph = stag.graph.barbell_graph(10)

    # Run the acl clustering method
    cluster = stag.cluster.local_cluster_acl(graph, 0, 0.9, 0.0001)

    # Check that we found one of the clusters
    expected_cluster = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}

    assert set(cluster) == expected_cluster


def test_approximate_pagerank():
    # For easier manual verification, we use a cycle graph with 0.5 weights on the edges
    adj = 0.5 * stag.graph.cycle_graph(4).adjacency().to_scipy()
    graph = stag.graph.Graph(adj)

    # Construct seed matrix.
    s = scipy.sparse.lil_matrix((4, 1))
    s[0, 0] = 1

    # Run the personalised pagerank and check that we get the right result
    p, r = stag.cluster.approximate_pagerank(graph, s.tocsc(), 1./3, 1./8)
    expected_p = [41./81, 2./27, 0, 2./27]
    expected_r = [5./81, 2./27 + 5./162, 2./27, 2./27 + 5./162]
    np.testing.assert_almost_equal(p.todense().transpose().tolist()[0], expected_p)
    np.testing.assert_almost_equal(r.todense().transpose().tolist()[0], expected_r)


def test_sweep_set():
    # Construct a simple graph to test with
    graph = stag.graph.barbell_graph(4)

    # Create the vector to test. The optimal conductance will be the first 4 vertices
    s = scipy.sparse.lil_matrix((8, 1))
    s[0, 0] = 0.1
    s[1, 0] = 0.25
    s[2, 0] = 0.2
    s[3, 0] = 0.15
    s[4, 0] = 0.05
    
    # Compute the sweep set
    sweep_set = stag.cluster.sweep_set_conductance(graph, s.tocsc())
    assert type(sweep_set) == type([1])
    assert set(sweep_set) == {0, 1, 2, 3}


def test_connected_component():
    # Construct a graph with two connected components.
    graph = stag.random.sbm(10, 2, 1, 0)
    cc = stag.cluster.connected_component(graph, 0)
    assert type(cc) == type([1])
    assert set(cc) == {0, 1, 2, 3, 4}


def test_connected_components():
    # Construct a graph with two connected components
    graph = stag.random.sbm(10, 2, 1, 0)
    ccs = stag.cluster.connected_components(graph)
    assert type(ccs) == type([[1]])
    assert type(ccs[0]) == type([0])
    assert set(ccs[0]) == {0, 1, 2, 3, 4}
    assert set(ccs[1]) == {5, 6, 7, 8, 9}


def test_ari():
    gt_labels = [0, 0, 1, 1, 1, 1, 2, 2, 2, 2]
    labels = [0, 1, 0, 1, 1, 2, 2, 2, 2, 2]
    expected_ari = 0.31257344
    actual_ari = stag.cluster.adjusted_rand_index(gt_labels, labels)
    assert actual_ari == pytest.approx(expected_ari, 0.0001)

    # Check that we can pass numpy ndarray to the adjusted rand index
    # method
    labels = np.asarray(labels)
    actual_ari = stag.cluster.adjusted_rand_index(gt_labels, labels)
    assert actual_ari == pytest.approx(expected_ari, 0.0001)

    gt_labels = np.asarray(gt_labels)
    actual_ari = stag.cluster.adjusted_rand_index(gt_labels, labels)
    assert actual_ari == pytest.approx(expected_ari, 0.0001)


def test_nmi():
    gt_labels = [0, 0, 1, 1, 1, 1, 2, 2, 2, 2]
    labels    = [0, 1, 0, 1, 1, 2, 2, 2, 2, 2]
    expected_nmi = 0.4558585
    actual_nmi = stag.cluster.normalised_mutual_information(gt_labels, labels)
    assert actual_nmi == pytest.approx(expected_nmi, 0.0001)

    # Check that we can call with numpy arrays
    actual_nmi = stag.cluster.normalised_mutual_information(np.asarray(gt_labels),
                                                            np.asarray(labels))
    assert actual_nmi == pytest.approx(expected_nmi, 0.0001)

    # Check the exact clustering
    labels = [1, 1, 2, 2, 2, 2, 0, 0, 0, 0]
    actual_nmi = stag.cluster.normalised_mutual_information(gt_labels, labels)
    assert actual_nmi == 1


def test_conductance():
    g = stag.graph.Graph(BARBELL5_ADJ_MAT)
    cluster = [0, 1, 2, 3, 4]
    expected_cond = 1/21
    cond = stag.cluster.conductance(g, cluster)
    assert cond == pytest.approx(expected_cond, 0.0001)

    # Try with an ndarray cluster
    cluster = np.asarray(cluster)
    cond = stag.cluster.conductance(g, cluster)
    assert cond == pytest.approx(expected_cond, 0.0001)


def test_sym_diff():
    s = [1, 4, 5, 2, 6]
    t = [1, 5, 3, 7]
    sym_diff = stag.cluster.symmetric_difference(s, t)
    assert set(sym_diff) == {2, 3, 4, 6, 7}

    # Check that ndarray arrays work
    s = np.asarray(s)
    t = np.asarray(t)
    sym_diff = stag.cluster.symmetric_difference(s, t)
    assert set(sym_diff) == {2, 3, 4, 6, 7}
