"""Tests for the clustering algorithms."""
import scipy.sparse
import pytest
import math
import numpy as np
from context import stag
import stag.graph
import stag.cluster
import stag.random
import stag.spectrum

def test_power_method():
    g = stag.graph.complete_graph(3)
    lap = g.laplacian().to_scipy()
    assert(lap.shape == (3, 3))
    vec = np.asarray([[0, 1, 0]]).T
    assert vec.shape == (3, 1)

    newvec = stag.spectrum.power_method(lap,
                                        num_iterations=2,
                                        initial_vector=vec)

    assert np.allclose(newvec, np.asarray([[-1/math.sqrt(6),
                                             2/math.sqrt(6),
                                            -1/math.sqrt(6)]]).T, atol=0.00001)

    g = stag.graph.cycle_graph(10)
    lap = g.normalised_laplacian().to_scipy()
    dominant_eigvec = stag.spectrum.power_method(lap, num_iterations=1000)
    assert abs(2 - stag.spectrum.rayleigh_quotient(lap, dominant_eigvec)) < 0.0001


def test_eigensystem():
    g = stag.graph.complete_graph(10)
    eigval, eigvec = stag.spectrum.compute_eigensystem(
        g, 'NormalisedLaplacian', 4, 'Smallest')
    assert np.allclose(min(eigval), np.asarray([0]))
    assert(eigvec[:, np.argmin(eigval)][3] == pytest.approx(1 / math.sqrt(10)))


def test_real_eigenvalues():
    g = stag.random.sbm(1000, 2, 0.1, 0.01)
    eigvals = stag.spectrum.compute_eigenvalues(
        g, 'NormalisedLaplacian', 4, 'Smallest')
    assert(eigvals.dtype == np.dtype('float'))
