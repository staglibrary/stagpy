from . import stag_internal
import scipy.sparse
import inspect

##
# \cond
# This file is currently listed as an explicit exception in the doxyfile.
# It will not be processed for documentation at all.
##

def swig_sprs_to_scipy(swig_mat):
    """
    Take a swig sparse matrix and convert it to a scipy sparse matrix.
    """
    outer_starts = stag_internal.sprsMatOuterStarts(swig_mat)
    inner_indices = stag_internal.sprsMatInnerIndices(swig_mat)
    values = stag_internal.sprsMatValues(swig_mat)
    return scipy.sparse.csc_matrix((values, inner_indices, outer_starts))


def scipy_to_swig_sprs(scipy_mat: scipy.sparse.csc_matrix):
    """
    Take a scipy sparse matrix and convert it to a swig sprs matrix.
    """
    col_starts = stag_internal.vectorl(scipy_mat.indptr.tolist())
    row_indices = stag_internal.vectorl(scipy_mat.indices.tolist())
    values = stag_internal.vectord(scipy_mat.data.tolist())
    return stag_internal.sprsMatFromVectors(col_starts,
                                            row_indices,
                                            values)


def return_sparse_matrix(func):
    def decorated_function(*args, **kwargs):
        swig_sparse_matrix = func(*args, **kwargs)
        sp_sparse = swig_sprs_to_scipy(swig_sparse_matrix)
        del swig_sparse_matrix
        return sp_sparse

    # Set the metadata of the returned function to match the original.
    # This is used when generating the documentation
    decorated_function.__doc__ = func.__doc__
    decorated_function.__module__ = func.__module__
    decorated_function.__signature__ = inspect.signature(func)

    return decorated_function

##
# \endcond
##
