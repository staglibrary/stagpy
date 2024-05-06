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

def test_ckns_two_moons():
    # Load the two moons dataset
    filename = "data/moons.txt"
    data = stag.data.load_matrix(filename)

    # Create a CKINS KDE estimator
    a = 20
    eps = 0.5
    ckns_kde = stag.kde.CKNSGaussianKDE(data, a, eps=eps)

    # Create an exact kde
    exact_kde = stag.kde.ExactGaussianKDE(data, a)

    # Check that the estimates are accurate
    exact_densities = exact_kde.query(data)
    approx_densitites = ckns_kde.query(data)

    total_error = 0
    for i in range(len(exact_densities)):
        total_error += abs(exact_densities[i] - approx_densitites[i]) / exact_densities[i]
    avg_error = total_error / len(exact_densities)
    assert(avg_error <= 0.5 * eps)
