"""
Some objects used for interoperability between C++ and Python.
"""
from . import stag_internal
import scipy.sparse
import inspect
import numpy as np
from typing import Optional

class SprsMat(object):
    """
    An object representing a sparse matrix for use by the STAG library.
    The data is stored natively on the 'C++' side of the library, allowing
    for fast computation.

    The object is designed for easy interoperability with scipy sparse matrix
    objects. The SprsMat object can be constructed directly from a scipy
    sparse matrix, and the to_scipy() method can be used to convert back
    to a scipy matrix.

    If they are only used as arguments to STAG library methods, they will be very
    efficient since the data will stay on the C++ side of the library.
    """

    def __init__(self, scipy_mat: Optional[scipy.sparse.csc_matrix],
                 internal_sprsmat: stag_internal.SprsMat = None):
        """
        Construct a STAG SprsMat from a scipy sparse matrix.

        The optional internal_sprsmat parameter is included for use by the
        library developers or advanced users.
        """
        ##
        # \cond
        # Do not document the internal workings of the SprsMat object
        ##
        self.scipy_mat = scipy_mat
        if internal_sprsmat is not None:
            self.internal_sprsmat = internal_sprsmat
        else:
            col_starts = stag_internal.vectorl(scipy_mat.indptr.tolist())
            row_indices = stag_internal.vectorl(scipy_mat.indices.tolist())
            values = stag_internal.vectord(scipy_mat.data.tolist())
            self.internal_sprsmat = stag_internal.sprsMatFromVectors(col_starts,
                                                                     row_indices,
                                                                     values)
        ##
        # \endcond
        ##

    def to_scipy(self) -> scipy.sparse.csc_matrix:
        """
        Convert the STAG SprsMat object to a scipy sparse matrix.
        """
        if self.scipy_mat is None:
            outer_starts = stag_internal.sprsMatOuterStarts(self.internal_sprsmat)
            inner_indices = stag_internal.sprsMatInnerIndices(self.internal_sprsmat)
            values = stag_internal.sprsMatValues(self.internal_sprsmat)
            self.scipy_mat = scipy.sparse.csc_matrix(
                (values, inner_indices, outer_starts))
        return self.scipy_mat

    def to_dense(self) -> np.ndarray:
        """
        Convert the STAG SprsMat object to a dense numpy matrix.
        """
        return self.to_scipy().toarray()

    ##
    # \cond
    # Do not document the operator methods
    ##
    def __sub__(self, other):
        if isinstance(other, SprsMat):
            return SprsMat(None, internal_sprsmat=
                                (self.internal_sprsmat - other.internal_sprsmat))
        else:
            return NotImplemented

    def __rsub__(self, other):
        if isinstance(other, SprsMat):
            return SprsMat(None, internal_sprsmat=
                                (other.internal_sprsmat - self.internal_sprsmat))
        else:
            return NotImplemented

    def __neg__(self):
        return SprsMat(None, internal_sprsmat=(-self.internal_sprsmat))

    def __add__(self, other):
        if isinstance(other, SprsMat):
            return SprsMat(None, internal_sprsmat=
                                (self.internal_sprsmat + other.internal_sprsmat))
        else:
            return NotImplemented

    def __radd__(self, other):
        return self.__add__(other)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return SprsMat(None, internal_sprsmat=(self.internal_sprsmat * other))
        else:
            return NotImplemented

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return SprsMat(None, internal_sprsmat=(self.internal_sprsmat / other))
        else:
            return NotImplemented

    ##
    # \endcond
    ##


##
# \cond
# Ignore the remainder of this file in the documentation.
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


def possibly_convert_ndarray(argument):
    """
    Check whether argument is a numpy ndarray.
    If it is, convert it to a list. Otherwise return it as-is.
    """
    if isinstance(argument, np.ndarray):
        return argument.tolist()
    else:
        return argument


def convert_ndarrays(func):
    """A decorator for methods which take lists as arguments.
    Converts *all* ndarrays in the arguments to lists."""
    def decorated_function(*args, **kwargs):
        new_args = [possibly_convert_ndarray(arg) for arg in args]
        new_kwargs = {k: possibly_convert_ndarray(v) for k, v in kwargs.items()}
        return func(*new_args, **new_kwargs)


    # Set the metadata of the returned function to match the original.
    # This is used when generating the documentation
    decorated_function.__doc__ = func.__doc__
    decorated_function.__module__ = func.__module__
    decorated_function.__signature__ = inspect.signature(func)

    return decorated_function

##
# \endcond
##
