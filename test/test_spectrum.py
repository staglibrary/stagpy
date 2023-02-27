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
    lap = g.laplacian()
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
    lap = g.normalised_laplacian()
    dominant_eigvec = stag.spectrum.power_method(lap, num_iterations=1000)
    assert abs(2 - stag.spectrum.rayleigh_quotient(lap, dominant_eigvec)) < 0.0001
