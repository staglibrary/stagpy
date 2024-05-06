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
