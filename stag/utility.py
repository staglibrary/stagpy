from . import stag_internal
import stag.graph
import scipy.sparse


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
    """
    A decorator which transforms a sparse matrix returned from the C++ library to a sparse scipy matrix for use within
    python. Note that this transformation incurs some overhead in terms of both time and space.

    :param func: the function whose output we would like to wrap
    :return: the decorated function
    """
    def decorated_function(*args, **kwargs):
        swig_sparse_matrix = func(*args, **kwargs)
        sp_sparse = swig_sprs_to_scipy(swig_sparse_matrix)
        del swig_sparse_matrix
        return sp_sparse

    return decorated_function


def return_graph(func):
    """
    A decorator which transforms a graph returned from the C++ library to the python version.

    :param func: the function whose output we would like to wrap
    :return: the decorated function
    """
    def decorated_function(*args, **kwargs):
        swig_graph = func(*args, **kwargs)
        return stag.graph.Graph(None, internal_graph=swig_graph)

    return decorated_function
