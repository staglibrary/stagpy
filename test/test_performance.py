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

def test_sbm(benchmark):
    benchmark(stag.random.sbm, 1000, 10, 0.1, 0.01)

def test_load_edgelist(benchmark):
    benchmark(stag.graphio.load_edgelist, "data/test6.edgelist")

def test_spectral_cluster(benchmark):
    g = stag.graphio.load_edgelist("data/test6.edgelist")
    benchmark(stag.cluster.spectral_cluster, g, 10)

def test_local_cluster(benchmark):
    g = stag.graphio.load_edgelist("data/test6.edgelist")
    benchmark(stag.cluster.local_cluster, g, 0, 1000)

def test_compute_eigensystem(benchmark):
    g = stag.graphio.load_edgelist("data/test6.edgelist")
    benchmark(stag.spectrum.compute_eigensystem, g, "Laplacian", 10, "Smallest")

#-------------------------------------------------------------------------------
# Multi-step workflows - this is to test the efficiency of passing data back and
# forth from Python to C++
#-------------------------------------------------------------------------------
def find_lap_eigvecs():
    g = stag.graphio.load_edgelist("data/test6.edgelist")
    eigs = stag.spectrum.compute_eigensystem(g, "Laplacian", 10, "Smallest")
    return eigs

def test_lap_eigvecs(benchmark):
    benchmark(find_lap_eigvecs)
