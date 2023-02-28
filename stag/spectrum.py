"""
Methods for computing eigenvalues and eigenvectors of sparse matrices.
"""
import numpy as np
import scipy as sp
import scipy.sparse
from typing import Tuple

from . import utility
from . import stag_internal


def compute_eigensystem(mat: scipy.sparse.spmatrix,
                        num: int,
                        which: str = 'SM') -> Tuple[np.ndarray, np.ndarray]:
    r"""
    Compute the eigenvalues and eigenvectors of a given matrix.

    By default, this will compute the eigenvalues of smallest magnitude.
    This default can be overridden by the `which `parameter which takes a
    string and should take one of the following values.
      - `SM` will return the eigenvalues with smallest magnitude
      - `LM` will return the eigenvalues with largest magnitude

    The following example demonstrates how to compute the 3 largest eigenvectors
    and eigenvalues of a cycle graph.

    \code{.py}
        import stag.graph
        import stag.spectrum

        myGraph = stag.graph.cycle_graph(10)
        lap = myGraph.normalised_laplacian()
        eigenvalues, eigenvectors = stag.spectrum.compute_eigensystem(
            lap, 3, 'LM')
    \endcode

    @param mat the matrix on which to operate
    @param num the number of eigenvalues and eigenvectors to compute
    @param which (optional) a string indicating which eigenvectors to calculate
    @returns a tuple containing the computed eigenvalues and eigenvectors
    """
    return sp.sparse.linalg.eigs(mat, k=num, which=which)


def compute_eigenvalues(mat: scipy.sparse.spmatrix,
                        num: int,
                        which: str = 'SM') -> np.ndarray:
    r"""
    Compute the eigenvalues of a given matrix.

    By default, this will compute the eigenvalues of smallest magnitude.
    This default can be overridden by the which parameter which takes a string
    and should be one of the following.
      - `SM` will return the eigenvalues with smallest magnitude
      - `LM` will return the eigenvalues with largest magnitude

    If you would like to calculate the eigenvectors and eigenvalues together, then
    you should instead use stag.spectrum.compute_eigensystem.

    @param mat the matrix on which to operate
    @param num the number of eigenvalues to compute
    @param which (optional) a string indicating which eigenvalues to calculate
    @returns a numpy array containing the computed eigenvalues
    """
    eigs, _ = compute_eigensystem(mat, num, which=which)
    return eigs

def compute_eigenvectors(mat: scipy.sparse.spmatrix,
                         num: int,
                         which: str = 'SM') -> np.ndarray:
    r"""
    Compute the eigenvectors of a given matrix.

    By default, this will compute the eigenvectors corresponding to the
    eigenvalues of smallest magnitude.
    This default can be overridden by the which parameter which takes a string
    and should be one of the following.
      - `SM` will return the vectors corresponding to eigenvalues with smallest magnitude
      - `LM` will return the vectors corresponding to eigenvalues with largest magnitude

    If you would like to calculate the eigenvectors and eigenvalues together, then
    you should instead use stag.spectrum.compute_eigensystem.

    @param mat the matrix on which to operate
    @param num the number of eigenvectors to compute
    @param which (optional) a string indicating which eigenvectors to calculate
    @returns a numpy array containing the computed eigenvectors as columns
    """
    _, eigvecs = compute_eigensystem(mat, num, which=which)
    return eigvecs


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
