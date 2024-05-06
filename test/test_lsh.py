"""
Tests for the lsh module.
"""
import pytest
import numpy as np
import math
from context import stag
import stag.lsh
import stag.utility
import stag.data

def test_lsh_function_collision_prob():
    # Create an lsh function object
    lsh_function = stag.lsh.LSHFunction(3)

    prob = lsh_function.collision_probability(math.sqrt(3))
    assert(prob == pytest.approx(0.657590637))

def test_lsh_function_apply():
    lsh_function = stag.lsh.LSHFunction(3)
    dp = np.asarray([[0, 1, 2]])
    val = lsh_function.apply(dp)
    assert(isinstance(val, int))

def test_lsh_function_correct_prob():
    dim = 3
    data_mat = stag.utility.DenseMat([[0, 1, 1],
                                      [1, 0, 0]])
    dp1 = stag.data.DataPoint(data_mat, 0)
    dp2 = stag.data.DataPoint(data_mat, 1)

    distance = math.sqrt(dim)

    prob = stag.lsh.LSHFunction.collision_probability(distance)

    # Create 1000 lsh functions
    num_funcs = 1000
    funcs = []
    for i in range(num_funcs):
        funcs.append(stag.lsh.LSHFunction(dim))

    # Apply the functions, and compute how many collisions we get
    num_collisions = 0
    for func in funcs:
        if (func.apply(dp1) == func.apply(dp2)):
            num_collisions += 1

    # Check that the number of collisions is approximately correct
    assert(num_collisions == pytest.approx(prob * num_funcs, 0.2))

def test_e2lsh11():
    # Check that an E2LSH table with K = 1 and L = 1 behaves like a single
    # LSHFunction

    # Create two data vectors
    dim = 3
    data_mat = stag.utility.DenseMat([[0, 1, 1],
                                      [1, 0, 0]])
    dp1 = stag.data.DataPoint(data_mat, 0)
    dp2 = stag.data.DataPoint(data_mat, 1)

    # Create 1000 E2LSH tables
    num_tables = 1000
    tables = []
    for i in range(num_tables):
        tables.append(stag.lsh.E2LSH(1, 1, [dp1]))

    # Compute the number for which the given vectors collide
    num_collisions = 0
    for table in tables:
        near_points = table.get_near_neighbors(dp2)
        if len(near_points) > 0:
            num_collisions += 1

    distance = math.sqrt(dim)
    prob = stag.lsh.LSHFunction.collision_probability(distance)
    assert(num_collisions == pytest.approx(prob * num_tables, 0.2))

def test_e2lsh510():
    # Check that an E2LSH table with K = 5 and L=10 creates the correct number
    # of collisions.
    K = 5
    L = 10
    dim = 3
    data_mat = stag.utility.DenseMat([[0, 1, 1],
                                      [1, 0, 0]])
    dp1 = stag.data.DataPoint(data_mat, 0)
    dp2 = stag.data.DataPoint(data_mat, 1)

    # Create 1000 E2LSH tables
    num_tables = 1000
    tables = []
    for i in range(num_tables):
        tables.append(stag.lsh.E2LSH(K, L, [dp1]))

    # Compute the number for which the given vectors collide
    num_collisions = 0
    for table in tables:
        near_points = table.get_near_neighbors(dp2)
        if len(near_points) > 0:
            num_collisions += 1

    distance = math.sqrt(dim)
    prob = tables[0].collision_probability(distance)
    assert(num_collisions == pytest.approx(prob * num_tables, 0.2))

def test_e2lsh_more_data():
    # Check that an E2LSH table with K = 1 and L = 1 creates the correct number
    # of collisions for different data points.
    K = 1
    L = 1

    # Create data vectors
    dim = 3
    data_mat = stag.utility.DenseMat([[0, 0, 0],
                                      [1, 0, 0],
                                      [1, 1, 0],
                                      [1, 1, 1]])
    dp1 = stag.data.DataPoint(data_mat, 0)
    dp2 = stag.data.DataPoint(data_mat, 1)
    dp3 = stag.data.DataPoint(data_mat, 2)
    dp4 = stag.data.DataPoint(data_mat, 3)

    # Create 1000 tables
    num_tables = 1000
    tables = []
    for i in range(num_tables):
        tables.append(stag.lsh.E2LSH(K, L, [dp2, dp3, dp4]))

    # Compute the number of collisions for each data point.
    num_collisions = [0, 0, 0]
    for table in tables:
        neighbors = table.get_near_neighbors(dp1)
        for neighbor in neighbors:
            assert(neighbor.dimension() == dim)
            if np.all(neighbor.to_numpy() == dp2.to_numpy()):
                num_collisions[0] += 1
            elif np.all(neighbor.to_numpy() == dp3.to_numpy()):
                num_collisions[1] += 1
            elif np.all(neighbor.to_numpy() == dp4.to_numpy()):
                num_collisions[2] += 1
            else:
                # Should never get here
                assert False

    # Check that the collision probabilities look right.
    for i in range(1, dim + 1):
        dist = math.sqrt(i)
        prob = tables[0].collision_probability(dist)
        assert(num_collisions[i-1] == pytest.approx(prob * num_tables, 0.2))
