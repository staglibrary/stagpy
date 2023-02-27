"""
Methods for computing eigenvalues and eigenvectors of sparse matrices.
"""
import numpy as np
import scipy as sp
import scipy.sparse

from . import utility
from . import stag_internal

def power_method(mat: scipy.sparse.spmatrix,
                 num_iterations: int = None,
                 initial_vector: np.ndarray = None) -> np.ndarray:
    if num_iterations is None:
        if initial_vector is None:
            return stag_internal.power_method(utility.scipy_to_swig_sprs(mat))
        else:
            return stag_internal.power_method(utility.scipy_to_swig_sprs(mat),
                                              initial_vector.astype(float))
    elif initial_vector is None:
        return stag_internal.power_method(utility.scipy_to_swig_sprs(mat),
                                          num_iterations)
    else:
        return stag_internal.power_method(utility.scipy_to_swig_sprs(mat),
                                          num_iterations, initial_vector.astype(float))
