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
