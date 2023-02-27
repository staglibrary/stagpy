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
    r"""
    Apply the power method to compute the dominant eigenvector of a matrix.

    Given a matrix \f$M\f$, an initial vector \f$v_0\f$, and a number of
    iterations \f$t\f$, the power method calculates the vector

    \f[
       v_t = M^t v_0,
    \f]

    which is close to the eigenvector of \f$M\f$ with largest eigenvalue.

    The running time of the power method is \f$O(t \cdot \mathrm{nnz}(M))\f$, where
    \f$\mathrm{nnz}(M)\f$ is the number of non-zero elements in the matrix \f$M\f$.

    @param mat the matrix \f$M\f$ on which to operate.
    @param num_iterations (optional) the number of iterations of the power
                          method to apply. It this argument is omitted,
                          \f$O(\log(n))\f$ iterations are used which results
                          in a vector whose Rayleigh quotient is a \f$(1 - \epsilon)\f$
                          approximation of the dominant eigenvalue.
    @param initial_vector (optional) the initial vector to use for the power
                          iteration. If this argument is omitted, a random unit
                          vector will be used.
    @return the vector \f$v_t\f$ computed by repeated multiplication with \f$M\f$.
    """
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


def rayleigh_quotient(mat: scipy.sparse.spmatrix, vec: np.ndarray) -> float:
    r"""
    Compute the Rayleigh quotient of the given vector and matrix.

    Given a matrix \f$M\f$, the Rayleigh quotient of vector \f$v\f$ is

    \f[
       R(M, v) = \frac{v^\top M v}{v^\top v}.
    \f]

    @param mat a sparse matrix \f$M \in \mathbb{R}^{n \times n}\f$.
    @param vec a vector \f$v \in \mathbb{R}^n\f$.
    @return the Rayleigh quotient \f$R(M, v)\f$.
    """
    return stag_internal.rayleigh_quotient(utility.scipy_to_swig_sprs(mat),
                                           vec)
