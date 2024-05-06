"""
Tests for the kde module.
"""
import pytest
import numpy as np
import math
from context import stag
import stag.kde
import stag.utility
import stag.data

def test_gaussian_kernel_dist():
    # Create some test distances
    a = 1.2
    distances = [0, 0.1, 0.5, 1, 1.5, 2, 10]
    expected_values = [1, 0.8869204, 0.548812, 0.301194, 0.165299, 0.0907180, 0.00000614421]

    assert(len(distances) == len(expected_values))

    for i in range(len(distances)):
        val = stag.kde.gaussian_kernel_dist(a, distances[i])
        assert(val == pytest.approx(expected_values[i], 0.01))

def test_gaussian_kernel_point():
    # Create some test points
    data = stag.utility.DenseMat([[0, 0, 0], [0, 1, 1]])
    dp1 = stag.data.DataPoint(data, 0)
    dp2 = stag.data.DataPoint(data, 1)

    a = 1.5
    expected_value = 0.0497871
    true_value = stag.kde.gaussian_kernel(a, dp1, dp2)
    assert(true_value == pytest.approx(expected_value, 0.01))

