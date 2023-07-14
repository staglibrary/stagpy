"""
Test the performance of various STAG workflows in Python.
"""
import time
import pytest
from context import stag
import stag.graph
import stag.random
import stag.graphio
import stag.cluster
import stag.spectrum

#-------------------------------------------------------------------------------
# Generating graphs from the stochastic block model.
#-------------------------------------------------------------------------------

def gen_sbm_1000_10():
    g = stag.random.sbm(1000, 10, 0.1, 0.01)
    return g


def gen_sbm_100000_10():
    g = stag.random.sbm(100000, 10, 0.001, 0.0001)
    return g


def test_typical_small_sbm(benchmark):
    g = benchmark(gen_sbm_1000_10)
    assert g.number_of_vertices() == 1000


def test_typical_large_sbm(benchmark):
    g = benchmark(gen_sbm_100000_10)
    assert g.number_of_vertices() == 100000

#-------------------------------------------------------------------------------
# Create a graph and run spectral clustering.
#-------------------------------------------------------------------------------

def sc_1000():
    g = gen_sbm_1000_10()
    clusters = stag.cluster.spectral_cluster(g, 10)
    return clusters

def sc_100000():
    g = gen_sbm_100000_10()
    clusters = stag.cluster.spectral_cluster(g, 10)
    return clusters


def test_sc_small(benchmark):
    clusters = benchmark(sc_1000)


def test_sc_large(benchmark):
    clusters = benchmark(sc_100000)

#-------------------------------------------------------------------------------
# Passing data
#-------------------------------------------------------------------------------

def find_lap_eigvecs():
    g = gen_sbm_100000_10()
    lap = g.laplacian()
    eigs = stag.spectrum.compute_eigensystem(lap, 10)
    return eigs

def test_lap_eigvecs(benchmark):
    eigs = benchmark(find_lap_eigvecs)
