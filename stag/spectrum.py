"""
Methods for computing eigenvalues and eigenvectors of sparse matrices.
"""
import numpy as np
from typing import Tuple

from . import utility
from . import graph
from . import stag_internal


def compute_eigensystem(g: graph.Graph,
                        matrix: str,
                        num: int,
                        which: str) -> Tuple[np.ndarray, np.ndarray]:
    r"""
    Compute the eigenvalues and eigenvectors of a given graph matrix.

    The second argument controls which graph matrix to use and should be one of
      - 'Laplacian',
      - 'NormalisedLaplacian', or
      - 'Adjacency'.

    The final argument specifies which eigenvalues to compute and should be
    either
      - 'Smallest', or
      - 'Largest'.

    The following example demonstrates how to compute the 3 largest eigenvectors
    and eigenvalues of the normalised Laplacian matrix of a cycle graph.

    \code{.py}
        import stag.graph
        import stag.spectrum

        myGraph = stag.graph.cycle_graph(10)
        eigenvalues, eigenvectors = stag.spectrum.compute_eigensystem(
            myGraph, 'NormalisedLaplacian', 3, 'Largest')
    \endcode

    @param g the graph whose spectrum you would like to compute
    @param matrix the name of the graph matrix on which to operate
    @param num the number of eigenvalues and eigenvectors to compute
    @param which whether to compute the smallest or largest eigenvalues
    @returns a tuple containing the computed eigenvalues and eigenvectors
    """
    if matrix not in ['Laplacian', 'NormalisedLaplacian', 'Adjacency']:
        raise ValueError("Matrix must be 'Laplacian', 'NormalisedLaplacian',"
                         "or 'Adjacency'")
    mat_conversion = {'Laplacian': stag_internal.Laplacian,
                      'NormalisedLaplacian': stag_internal.NormalisedLaplacian,
                      'Adjacency': stag_internal.Adjacency}
    int_matrix = mat_conversion[matrix]

    if which not in ['Smallest', 'Largest']:
        raise ValueError("The 'which' argument must be either 'Smallest' or"
                         "'Largest'.")
    which_conversion = {'Smallest': stag_internal.Smallest,
                        'Largest': stag_internal.Largest}
    int_which = which_conversion[which]

    # Call the internal eigensystem method.
    eigensystem = stag_internal.compute_eigensystem(
        g.internal_graph, int_matrix, num, int_which)
    return eigensystem.get0(), eigensystem.get1()


def compute_eigenvalues(g: graph.Graph,
                        matrix: str,
                        num: int,
                        which: str) -> np.ndarray:
    r"""
    Compute the eigenvalues of a specified graph matrix.

    The second argument controls which graph matrix to use and should be one of
      - 'Laplacian',
      - 'NormalisedLaplacian', or
      - 'Adjacency'.

    The final argument specifies which eigenvalues to compute and should be
    either
      - 'Smallest', or
      - 'Largest'.

    If you would like to calculate the eigenvectors and eigenvalues together, then
    you should instead use stag.spectrum.compute_eigensystem.

    @param g the graph whose spectrum you would like to compute
    @param matrix the name of the graph matrix on which to operate
    @param num the number of eigenvalues to compute
    @param which whether to compute the smallest or largest eigenvalues
    @returns a numpy array containing the computed eigenvalues
    """
    eigs, _ = compute_eigensystem(g, matrix, num, which)
    return eigs


def compute_eigenvectors(g: graph.Graph,
                         matrix: str,
                         num: int,
                         which: str) -> np.ndarray:
    r"""
    Compute the eigenvectors of a specified graph matrix.

    The second argument controls which graph matrix to use and should be one of
      - 'Laplacian',
      - 'NormalisedLaplacian', or
      - 'Adjacency'.

    The final argument specifies which eigenvectors to compute and should be
    either
      - 'Smallest', or
      - 'Largest'.

    If you would like to calculate the eigenvectors and eigenvalues together, then
    you should instead use stag.spectrum.compute_eigensystem.

    @param g the graph whose spectrum you would like to compute
    @param matrix the name of the graph matrix on which to operate
    @param num the number of eigenvectors to compute
    @param which whether to compute the vectors corresponding to the smallest or largest eigenvalues
    @returns a numpy array containing the computed eigenvectors as columns
    """
    _, eigvecs = compute_eigensystem(g, matrix, num, which)
    return eigvecs


@utility.convert_sprsmats
@utility.convert_ndarrays
def power_method(mat: utility.SprsMat,
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
            return stag_internal.power_method(mat.internal_sprsmat)
        else:
            return stag_internal.power_method(mat.internal_sprsmat,
                                              initial_vector.astype(float))
    elif initial_vector is None:
        return stag_internal.power_method(mat.internal_sprsmat,
                                          num_iterations)
    else:
        return stag_internal.power_method(mat.internal_sprsmat,
                                          num_iterations, initial_vector.astype(float))


@utility.convert_ndarrays
@utility.convert_sprsmats
def rayleigh_quotient(mat: utility.SprsMat, vec: np.ndarray) -> float:
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
    return stag_internal.rayleigh_quotient(mat.internal_sprsmat,
                                           vec)
