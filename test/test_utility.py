"""
Tests for utility functions in the library.
"""
import pytest
import numpy as np
from context import stag
import stag.stag_internal
import stag.cluster


def test_numpy_data_types():
    np_vec = np.asarray([1, 2, 3], dtype=np.int64)

    # This should not throw an error.
    stag_vec = stag.stag_internal.vectorl(np_vec)

    np_vec_2 = np.asarray([2, 3, 4], dtype=np.int64)
    sym_diff = stag.cluster.symmetric_difference(np_vec, np_vec_2)
    assert set(sym_diff) == {1, 4}
