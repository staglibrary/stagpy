from . import stag_internal
import stag.graph
import scipy.sparse


def return_sparse_matrix(func):
    """
    A decorator which transforms a sparse matrix returned from the C++ library to a sparse scipy matrix for use within
    python. Note that this transformation incurs some overhead in terms of both time and space.

    :param func: the function whose output we would like to wrap
    :return: the decorated function
    """
    def decorated_function(*args, **kwargs):
        swig_sparse_matrix = func(*args, **kwargs)
        outer_starts = stag_internal.sprsMatOuterStarts(swig_sparse_matrix)
        inner_indices = stag_internal.sprsMatInnerIndices(swig_sparse_matrix)
        values = stag_internal.sprsMatValues(swig_sparse_matrix)
        del swig_sparse_matrix
        return scipy.sparse.csc_matrix((values, inner_indices, outer_starts))

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
