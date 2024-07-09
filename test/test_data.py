"""
Tests for the data module.
"""
import pytest
import scipy as sp
import scipy.sparse
import math
from context import stag
import stag.data
import stag.utility


def test_create_datapoint():
    # Create a dense matrix
    mat = stag.utility.DenseMat([[1, 3],
                                 [4, 2],
                                 [5, 1]])

    # Create a data point. We're just making sure this doesn't fail.
    dp = stag.data.DataPoint(mat, 1)


def test_save_matrix():
    # Create a dense matrix
    mat = stag.utility.DenseMat([[1, 3],
                                 [4, 2],
                                 [5, 1]])

    # Save the matrix to file
    filename = "test.mat"
    stag.data.save_matrix(mat, filename)

    # Load the matrix again
    mat2 = stag.data.load_matrix(filename)
    assert(mat.internal_densemat == mat2.internal_densemat)
