"""
Tests for utility functions in the library.
"""
import pytest
import numpy as np
import scipy.sparse
from context import stag
import stag.stag_internal
import stag.cluster
import stag.utility


def test_numpy_data_types():
    np_vec = np.asarray([1, 2, 3], dtype=np.int64)
    np_vec_2 = np.asarray([2, 3, 4], dtype=np.int64)
    sym_diff = stag.cluster.symmetric_difference(np_vec, np_vec_2)
    assert set(sym_diff) == {1, 4}


def test_add_sprsmat():
    mat1 = scipy.sparse.csc_matrix([[0, 1, 0, 1],
                                    [1, 0, 1, 0],
                                    [0, 1, 0, 1],
                                    [1, 0, 1, 0]])
    mat2 = scipy.sparse.csc_matrix([[2, 0, 1, 1],
                                    [0, 2, 0, 0],
                                    [0, 0, 2, 0],
                                    [1, 1, 0, 2]])
    sprsmat1 = stag.utility.SprsMat(mat1)
    sprsmat2 = stag.utility.SprsMat(mat2)
    mat3 = (sprsmat1 + sprsmat2).to_scipy()

    expected_mat = scipy.sparse.csc_matrix([[2, 1, 1, 2],
                                            [1, 2, 1, 0],
                                            [0, 1, 2, 1],
                                            [2, 1, 1, 2]])
    mat_diff = mat3 - expected_mat
    assert(np.all(mat_diff.todense() == pytest.approx(0)))

    # Test the compound addition operator
    sprsmat1 += sprsmat2
    mat_diff = sprsmat1.to_scipy() - expected_mat
    assert(np.all(mat_diff.todense() == pytest.approx(0)))


def test_sub_sprsmat():
    mat1 = scipy.sparse.csc_matrix([[0, 1, 0, 1],
                                    [1, 0, 1, 0],
                                    [0, 1, 0, 1],
                                    [1, 0, 1, 0]])
    mat2 = scipy.sparse.csc_matrix([[2, 0, 1, 1],
                                    [0, 2, 0, 0],
                                    [0, 0, 2, 0],
                                    [1, 1, 0, 2]])
    sprsmat1 = stag.utility.SprsMat(mat1)
    sprsmat2 = stag.utility.SprsMat(mat2)
    mat3 = (sprsmat1 - sprsmat2).to_scipy()

    expected_mat = scipy.sparse.csc_matrix([[-2, 1, -1, 0],
                                            [1, -2, 1, 0],
                                            [0, 1, -2, 1],
                                            [0, -1, 1, -2]])
    mat_diff = (mat3 - expected_mat)
    assert(np.all(mat_diff.todense() == pytest.approx(0)))

    # Test the compound subtraction operator
    sprsmat1 -= sprsmat2
    mat_diff = sprsmat1.to_scipy() - expected_mat
    assert(np.all(mat_diff.todense() == pytest.approx(0)))


def test_subtract_bad_shapes():
    # Subtracting matrices with different shapes should not work
    mat1 = stag.utility.SprsMat([[1, 2, 3], [2, 3, 4]])
    mat2 = stag.utility.SprsMat([[1, 2], [3, 2], [4, 2]])

    assert mat1.shape() == (2, 3)
    assert mat2.shape() == (3, 2)

    with pytest.raises(Exception):
        mat3 = mat1 - mat2


def test_add_bad_shapes():
    # Adding matrices with different shapes should not work
    mat1 = stag.utility.SprsMat([[1, 2, 3], [2, 3, 4]])
    mat2 = stag.utility.SprsMat([[1, 2], [3, 2], [4, 2]])

    with pytest.raises(Exception):
        mat3 = mat1 + mat2


def test_unary_negation_sprsmat():
    mat1 = scipy.sparse.csc_matrix([[0, 1, 0, 1],
                                    [1, 0, 1, 0],
                                    [0, 1, 0, 1],
                                    [1, 0, 1, 0]])
    sprsmat1 = stag.utility.SprsMat(mat1)
    mat2 = (-sprsmat1).to_scipy()

    expected_mat = scipy.sparse.csc_matrix([[0, -1, 0, -1],
                                            [-1, 0, -1, 0],
                                            [0, -1, 0, -1],
                                            [-1, 0, -1, 0]])
    mat_diff = (mat2 - expected_mat)
    assert(np.all(mat_diff.todense() == pytest.approx(0)))


def test_scalar_mul_sprsmat():
    mat1 = scipy.sparse.csc_matrix([[0, 1, 0, 1],
                                    [1, 0, 1, 0],
                                    [0, 1, 0, 1],
                                    [1, 0, 1, 0]])
    sprsmat1 = stag.utility.SprsMat(mat1)
    mat2 = (2 * sprsmat1).to_scipy()

    expected_mat = scipy.sparse.csc_matrix([[0, 2, 0, 2],
                                            [2, 0, 2, 0],
                                            [0, 2, 0, 2],
                                            [2, 0, 2, 0]])
    mat_diff = (mat2 - expected_mat)
    assert(np.all(mat_diff.todense() == pytest.approx(0)))

    mat2 = (sprsmat1 * 2).to_scipy()
    mat_diff = (mat2 - expected_mat)
    assert(np.all(mat_diff.todense() == pytest.approx(0)))

    sprsmat1 *= 2
    mat_diff = (sprsmat1.to_scipy() - expected_mat)
    assert(np.all(mat_diff.todense() == pytest.approx(0)))

    mat2 = (0.5 * sprsmat1).to_scipy()
    mat_diff = mat2 - mat1
    assert(np.all(mat_diff.todense() == pytest.approx(0)))


def test_scalar_div_sprsmat():
    mat1 = scipy.sparse.csc_matrix([[0, 2, 0, 2],
                                    [2, 0, 2, 0],
                                    [0, 2, 0, 2],
                                    [2, 0, 2, 0]])
    sprsmat1 = stag.utility.SprsMat(mat1)
    mat2 = (sprsmat1 / 2).to_scipy()

    expected_mat = scipy.sparse.csc_matrix([[0, 1, 0, 1],
                                            [1, 0, 1, 0],
                                            [0, 1, 0, 1],
                                            [1, 0, 1, 0]])
    mat_diff = (mat2 - expected_mat)
    assert(np.all(mat_diff.todense() == pytest.approx(0)))

    sprsmat1 /= 2
    mat_diff = sprsmat1.to_scipy() - expected_mat
    assert(np.all(mat_diff.todense() == pytest.approx(0)))

    mat2 = (sprsmat1 / 0.5).to_scipy()
    mat_diff = mat2 - mat1
    assert(np.all(mat_diff.todense() == pytest.approx(0)))


def test_sprsmat_transpose():
    mat1 = stag.utility.SprsMat([[0, 2, 0, 2],
                                 [1, 0, 2, 0],
                                 [0, 1, 0, 2],
                                 [1, 0, 1, 0]])
    mat2 = mat1.transpose()

    expected_mat = stag.utility.SprsMat([[0, 1, 0, 1],
                                         [2, 0, 1, 0],
                                         [0, 2, 0, 1],
                                         [2, 0, 2, 0]])
    mat_diff = mat2 - expected_mat
    assert(np.all(mat_diff.to_dense() == pytest.approx(0)))


def test_sprsmat_transpose_one_dim():
    mat1 = stag.utility.SprsMat([[1, 0, 0, 0]])
    mat2 = mat1.transpose()

    expected_mat = stag.utility.SprsMat([[1], [0], [0], [0]])
    mat_diff = mat2 - expected_mat
    assert(np.all(mat_diff.to_dense() == pytest.approx(0)))


def test_sprsmat_multiplication():
    mat1 = stag.utility.SprsMat([[0, 1, 0, 1],
                                 [1, 0, 1, 0],
                                 [0, 1, 0, 1],
                                 [1, 0, 1, 0]])
    mat2 = stag.utility.SprsMat([[0, 3, 1, 1],
                                 [0, 0, 0, 2],
                                 [3, 0, 0, 2],
                                 [1, 1, 1, 1]])
    expected_mat = stag.utility.SprsMat([[1, 1, 1, 3],
                                         [3, 3, 1, 3],
                                         [1, 1, 1, 3],
                                         [3, 3, 1, 3]])
    mat3 = mat1 * mat2
    mat_diff = mat3 - expected_mat
    assert(np.all(mat_diff.to_dense() == pytest.approx(0)))

    mat3 = mat1 @ mat2
    mat_diff = mat3 - expected_mat
    assert(np.all(mat_diff.to_dense() == pytest.approx(0)))

    expected_mat = stag.utility.SprsMat([[4, 1, 4, 1],
                                         [2, 0, 2, 0],
                                         [2, 3, 2, 3],
                                         [2, 2, 2, 2]])
    mat3 = mat2 * mat1
    mat_diff = mat3 - expected_mat
    assert(np.all(mat_diff.to_dense() == pytest.approx(0)))

    mat3 = mat2 @ mat1
    mat_diff = mat3 - expected_mat
    assert(np.all(mat_diff.to_dense() == pytest.approx(0)))

    mat2 *= mat1
    mat_diff = mat2 - expected_mat
    assert(np.all(mat_diff.to_dense() == pytest.approx(0)))


def test_sprsmat_outer_product():
    vec1 = stag.utility.SprsMat([[1, 2, 0, 1]])
    vec2 = stag.utility.SprsMat([[0, -2, 1, 0]])

    expected_mat = stag.utility.SprsMat([[0, -2, 1, 0],
                                         [0, -4, 2, 0],
                                         [0, 0, 0, 0],
                                         [0, -2, 1, 0]])
    mat3 = vec1.transpose() @ vec2
    mat_diff = mat3 - expected_mat
    assert(np.all(mat_diff.to_dense() == pytest.approx(0)))
