"""
Some objects used for interoperability between C++ and Python.
"""
from . import stag_internal
import scipy.sparse
import inspect
import numpy as np
from typing import Union, List, Tuple

class DenseMat(object):
    """
    An object representing a dense matrix for use with the STAG library.
    The data is stored natively on the 'C++' side of the library, allowing
    for fast computation.

    The object is designed for easy interoperability with numpy ndarray
    objects. The DenseMat object can be constructed directly from a numpy
    ndarray object, and the to_numpy() method can be used to convert back
    to a numpy ndarray.

    If they are only used as arguments to STAG library methods, they will be
    very efficient since the data will stay on the C++ side of the library.
    """

    def __init__(self, matrix: Union[np.ndarray, List[List[float]]]):
        """
        Construct a STAG DenseMat.

        Pass either a numpy ndarray or a List of Lists representing the matrix.
        """
        ##
        # \cond
        # Do not document the internal workings of the DenseMat object
        ##
        self.numpy_mat = None

        if isinstance(matrix, np.ndarray):
            self.numpy_mat = matrix.astype(float)
        if isinstance(matrix, List):
            self.numpy_mat = np.ndarray(matrix, dtype=float)

        if isinstance(matrix, stag_internal.DenseMat):
            self.internal_densemat = matrix
        else:
            assert self.numpy_mat is not None
            self.internal_densemat = stag_internal.denseMatFromNdarray(self.numpy_mat)
        ##
        # \endcond
        ##

    def to_numpy(self):
        """
        Convert the STAG DenseMat object to a numpy matrix.
        """
        if self.numpy_mat is None:
            self.numpy_mat = stag_internal.ndArrayFromDenseMat(self.internal_densemat)
        return self.numpy_mat

    def transpose(self) -> 'DenseMat':
        """
        Return the transpose of the matrix.
        """
        return DenseMat(self.internal_densemat.__transpose__())


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

    def __init__(self, matrix: Union[scipy.sparse.spmatrix, List[List[float]]]):
        r"""
        Construct a STAG SprsMat.

        Pass either a scipy sparse matrix object or a List of Lists representing
        the dense matrix to be stored in sparse format.

        For example:

        \code{python}
        >>> import stag.utility
        >>> import stag.graph
        >>>
        >>> adj_mat = stag.utility.SprsMat([[0, 1, 1, 1],
        ...                                 [1, 0, 1, 1],
        ...                                 [1, 1, 0, 1],
        ...                                 [1, 1, 1, 0]])
        >>> g = stag.graph.Graph(adj_mat)
        \endcode
        """
        ##
        # \cond
        # Do not document the internal workings of the SprsMat object
        ##
        self.scipy_mat = None

        try:
            if issubclass(type(matrix), scipy.sparse.sparray):
                # Handle the sparse array format
                matrix = scipy.sparse.csc_matrix(matrix)
        except AttributeError:
            # The sparray attribute could not be found: we are using an
            # older version of scipy. We can ignore this error.
            pass
        if issubclass(type(matrix), scipy.sparse.spmatrix):
            self.scipy_mat = matrix.tocsc().astype(np.double)
        if isinstance(matrix, List):
            self.scipy_mat = scipy.sparse.csc_matrix(matrix, dtype=np.double)

        if isinstance(matrix, stag_internal.SprsMat):
            self.internal_sprsmat = matrix
        else:
            assert self.scipy_mat is not None
            col_starts = self.scipy_mat.indptr
            row_indices = self.scipy_mat.indices
            values = self.scipy_mat.data
            self.internal_sprsmat = stag_internal.sprsMatFromVectorsDims(
                self.scipy_mat.shape[0], self.scipy_mat.shape[1],
                col_starts, row_indices, values)
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
                (values, inner_indices, outer_starts),
                shape=self.shape())
        return self.scipy_mat

    def to_dense(self) -> np.ndarray:
        """
        Convert the STAG SprsMat object to a dense numpy matrix.
        """
        return self.to_scipy().toarray()

    def transpose(self) -> 'SprsMat':
        """
        Return the transpose of the matrix.
        """
        return SprsMat(self.internal_sprsmat.__transpose__())

    def shape(self) -> Tuple[int, int]:
        """
        Return the shape of the matrix.
        """
        return self.internal_sprsmat.get_rows(), self.internal_sprsmat.get_cols()

    ##
    # \cond
    # Do not document the operator methods
    ##
    def __sub__(self, other):
        if isinstance(other, SprsMat):
            if self.shape() != other.shape():
                raise ValueError(f"Matrix dimensions must match. {self.shape()} != {other.shape()}.")
            return SprsMat(self.internal_sprsmat - other.internal_sprsmat)
        else:
            return NotImplemented

    def __rsub__(self, other):
        if isinstance(other, SprsMat):
            if self.shape() != other.shape():
                raise ValueError("Matrix dimensions must match.")
            return SprsMat(other.internal_sprsmat - self.internal_sprsmat)
        else:
            return NotImplemented

    def __neg__(self):
        return SprsMat(-self.internal_sprsmat)

    def __add__(self, other):
        if isinstance(other, SprsMat):
            if self.shape() != other.shape():
                raise ValueError("Matrix dimensions must match.")
            return SprsMat(self.internal_sprsmat + other.internal_sprsmat)
        else:
            return NotImplemented

    def __radd__(self, other):
        return self.__add__(other)

    def __mul__(self, other):
        if isinstance(other, int):
            return SprsMat(self.internal_sprsmat.__mulint__(other))
        elif isinstance(other, float):
            return SprsMat(self.internal_sprsmat.__mulfloat__(other))
        elif isinstance(other, SprsMat):
            return SprsMat(self.internal_sprsmat * other.internal_sprsmat)
        else:
            return NotImplemented

    def __rmul__(self, other):
        if isinstance(other, SprsMat):
            return SprsMat(other.internal_sprsmat * self.internal_sprsmat)
        else:
            return self.__mul__(other)

    def __matmul__(self, other):
        return self.__mul__(other)

    def __rmatmul__(self, other):
        return self.__rmul__(other)

    def __truediv__(self, other):
        if isinstance(other, int):
            return SprsMat(self.internal_sprsmat.__truedivint__(other))
        elif isinstance(other, float):
            return SprsMat(self.internal_sprsmat.__truedivfloat__(other))
        else:
            return NotImplemented

    ##
    # \endcond
    ##

##
# \cond
##
def possibly_convert_list(argument):
    """
    Check whether argument is a python list.
    If it is, convert it to a numpy ndarray.
    Otherwise, return it as-is.
    """
    if isinstance(argument, list):
        return np.asarray(argument)
    else:
        return argument


def convert_ndarrays(func):
    """
    A decorator for methods which take ndarray objects as arguments.
    Converts python lists in the argument list to ndarrays.
    """
    def decorated_function(*args, **kwargs):
        new_args = [possibly_convert_list(arg) for arg in args]
        new_kwargs = {k: possibly_convert_list(v) for k, v in kwargs.items()}
        return func(*new_args, **new_kwargs)


    # Set the metadata of the returned function to match the original.
    # This is used when generating the documentation
    decorated_function.__doc__ = func.__doc__
    decorated_function.__module__ = func.__module__
    decorated_function.__signature__ = inspect.signature(func)

    return decorated_function


def possibly_convert_sprsmat(argument):
    """
    Check whether argument is a scipy sparse matrix.
    If it is, convert it to a stag SprsMat.
    Otherwise, return it as-is.
    """
    if issubclass(type(argument), scipy.sparse.spmatrix):
        return SprsMat(argument)
    else:
        return argument


def convert_sprsmats(func):
    """
    A decorator for methods which take SprsMat objects as arguments.
    Converts scipy sparse arrays in the argument list to stag SprsMat objects.
    """
    def decorated_function(*args, **kwargs):
        new_args = [possibly_convert_sprsmat(arg) for arg in args]
        new_kwargs = {k: possibly_convert_sprsmat(v) for k, v in kwargs.items()}
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
