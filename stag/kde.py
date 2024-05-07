r"""
Methods for computing the kernel density estimation.

Given some *kernel function*
\f$k: \mathbb{R}^d \times \mathbb{R}^d \rightarrow \mathbb{R}\f$,
a set of *data points* \f$x_1, \ldots, x_n \in \mathbb{R}^d\f$,
and a *query point* \f$q \in \mathbb{R}^d\f$,
the *kernel density* of \f$q\f$ is given by

\f[
   K(q) = \frac{1}{n} \sum_{i = 1}^n k(q, x_i).
\f]

A common kernel function is the Gaussian kernel function
\f[
   k(u, v) = \exp\left(- a \|u - v\|_2^2\right),
\f]
where \f$a \geq 0\f$ is a parameter controlling the 'bandwidth' of the
kernel.

Computing the kernel density for a query point exactly requires computing the
distance from the query point to every data point, requiring
\f$\Omega(n d)\f$ time.
This motivates the study of *kernel density estimation*, in which the goal
is to estimate the kernel density within some error tolerance, in faster
time than computing it exactly.
Specifically, given some error parameter \f$\epsilon\f$, a kernel density
estimation algorithm will return \f$\mathrm{KDE}(q)\f$ for some query point
\f$q\f$ such that
\f[
 (1 - \epsilon) K(q) \leq \mathrm{KDE}(q) \leq (1 + \epsilon) K(q).
\f]

This module provides the stag::CKNSGaussianKDE data structure which takes
\f$O(\epsilon^{-1} n^{1.25})\f$ time for initialisation, and can then provide
KDE estimates in time \f$O(\epsilon^{-2} n^{0.25})\f$ for each query.
"""
import numpy as np
import math
from typing import Union, List

import stag.data
from . import stag_internal
from . import utility
from . import data

def gaussian_kernel(a: float, u: stag.data.DataPoint, v: stag.data.DataPoint):
    r"""
    Compute the Gaussian kernel similarity between the points u and v.

    Given a parameter \f$a \geq 0\f$ and points \f$u, v \in \mathbb{R}^n\f$,
    the Gaussian kernel similarity between \f$u\f$ and \f$v\f$ is given by

    \f[
       k(u, v) = \exp\left( - a \|u - v\|^2_2 \right).
    \f]

    Note that the Gaussian kernel is sometimes parameterised by \f$\sigma^2\f$,
    which is related to our parameter \f$a\f$ by

    \f[
       a = \frac{1}{\sigma^2}.
    \f]

    @param a the parameter a in the Gaussian kernel.
    @param u a data point \f$u\f$
    @param v a data point \f$v\f$
    @return the Gaussian kernel similarity between \f$u\f$ and \f$v\f$.
    """
    return stag_internal.gaussian_kernel(a,
                                         u.internal_datapoint,
                                         v.internal_datapoint)

def gaussian_kernel_dist(a: float, c: float) -> float:
    r"""
    Compute the Gaussian kernel similarity for two points at a squared distance
    \f$c\f$.

    Given a parameter \f$a \geq 0\f$, the Gaussian kernel similarity between
    two points at distance \f$c\f$ is given by

    \f[
       \exp\left( - a c \right).
    \f]

    @param a the parameter a in the Gaussian kernel.
    @param c the squared distance between two points.
    @return the kernel evaluated at distance \f$c\f$.
    """
    return stag_internal.gaussian_kernel(a, c)

class CKNSGaussianKDE(object):
    r"""
    \brief A CKNS Gaussian KDE data structure.

    This data structure implements the CKNS algorithm for kernel density
    estimation. Given data \f$x_1, \ldots, x_n \in \mathbb{R}^d\f$, in matrix
    format, this data structure will preprocess the data in
    \f$O(\epsilon^{-2} n^{1.25})\f$ time, such that for any query point,
    a \f$(1 + \epsilon)\f$-approximate kernel density estimate can be returned
    in \f$O(\epsilon^{-2} n^{0.25})\f$ time.

    \par References
    Charikar, Moses, et al. "Kernel density estimation through density
    constrained near neighbor search." 2020 IEEE 61st Annual Symposium on
    Foundations of Computer Science (FOCS). IEEE, 2020.
    """

    def __init__(self, data: stag.utility.DenseMat, a: float,
                 eps: float = 1,
                 min_mu: float = None,
                 k1: int = None,
                 k2_constant: float = None,
                 sampling_offset: int = 0):
        r"""
        Initialise a new KDE data structure with the given dataset.

        Data should be a stag.utility.DenseMat matrix \f$X \in \mathbb{R}^{n \times d}\f$
        where each row represents a data point.

        The \f$\epsilon\f$ parameter is used to control the error guarantee of the
        CKNS data structure. A lower value of \f$\epsilon\f$ will give a more accurate
        estimate, at the cost of a higher processing time.
        The data structure should produce estimates which are within a
        \f$(1 \pm \epsilon)\f$ factor of the true kernel density.

        The initialisation time complexity of the data structure is
        \f$O(\epsilon^{-2} n^{1.25} \log^2(n))\f$ and the query time for each
        query point is \f$(O(\epsilon^{-2} n^{0.25} \log^2(n))\f$.

        Usually, the data structure can be initialised with only the dataset and the
        parameter \f$a\f$.
        If more control is needed, the eps and min_mu parameters
        offer a trade-off between running time and accuracy.

        For those familiar with the inner workings of the CKNS algorithm, the
        k1, k2_constant, and sampling_offset optional parameters offer even more
        fine-grained control over the performance of the algorithm.

        @param data the \f$(n \times d)\f$ matrix containing the dataset.
        @param a the parameter \f$a\f$ of the Gaussian kernel function.
        @param eps (optional) the error parameter \f$\epsilon\f$ of the KDE data
                   structure. Default is 1 (in practice this normally gives a
                   good result).
        @param min_mu (optional) the minimum kernel density value of any query
                      point. A smaller number will give longer preprocessing and
                      query time complexity. If a query point has a kernel density
                      smaller than this value, then the data structure may not
                      return the correct result.
                      Default is 1 / n.
        @param k1 (optional) the number of copies of the data structure to create in parallel.
                  This parameter controls the variance of the estimator returned
                  by the algorithm. Default is \f$\epsilon^{-2} \cdot \log(n)\f$.
        @param k2_constant (optional) controls the collision probability of each
                           of the E2LSH hash tables used within the data structure.
                           A higher value will give more accurate estimates at the cost of
                           higher memory and time complexity. Default is \f$0.1 \log(n)\f$.
        @param sampling_offset (optional) the CKNS algorithm samples the dataset with
                               various sampling probabilities. Setting a sampling offset
                               of \f$k\f$ will further subsample the data by a factor
                               of \f$1/2^k\f$. This will speed up the algorithm at the cost
                               of some accuracy. Default is \f$0\f$.
        """
        n = data.internal_densemat.get_rows()
        if min_mu is None:
            min_mu = 1 / data.internal_densemat.get_rows()
        if k1 is None:
            k1 = int(math.log(n) * 1 / (eps * eps))
        if k2_constant is None:
            k2_constant = 0.1 * math.log(n)
        self.internal_ckns = stag_internal.CKNSGaussianKDE(
            data.internal_densemat, a, min_mu, k1, k2_constant, sampling_offset)

    def query(self, q: Union[stag.utility.DenseMat, stag.data.DataPoint]) -> Union[float, np.ndarray]:
        r"""
        Calculate the KDE estimate for the given query points.

        The parameter q can be either a stag.data.DataPoint object to query
        one data point, or a stag.utility.DenseMat matrix with the query points
        as rows in order to query many data points.

        When querying many data points, passing a DenseMat will
        be more efficient than calling this method once for each data point.

        @param q the query data point(s)
        @return the KDE estimate(s) for the given query point(s), either as a
                float (for one data point) or a numpy array.
        """
        if isinstance(q, stag.data.DataPoint):
            return self.internal_ckns.query(q.internal_datapoint)
        else:
            return self.internal_ckns.query(q.internal_densemat)


class ExactGaussianKDE(object):
    r"""
    \brief A data structure for computing the exact Gauussian KDE.

    This data structure uses a brute-force algorithm to compute the kernel
    density of each query point.

    The time complexity of initialisation with \f$n\f$ data points is \f$O(1)\f$.
    The query time complexity is \f$O(m n d)\f$, where \f$m\f$ is the number
    of query points, and \f$d\f$ is the dimensionality of the data.
    """

    def __init__(self, data: stag.utility.DenseMat, a: float):
        r"""
        Initialise the data structure with the given dataset and Gaussian kernel
        parameter \f$a\f$.

        The initialisation time for this data structure is \f$O(1)\f$.

        @param data
        @param a
        """
        self.internal_kde = stag_internal.ExactGaussianKDE(data.internal_densemat,
                                                           a)

    def query(self, q: Union[stag.utility.DenseMat, stag.data.DataPoint]) -> Union[float, np.ndarray]:
        r"""
        Calculate the exact kernel density estimates for the given query points.

        The parameter q can be either a stag.data.DataPoint object to query
        one data point, or a stag.utility.DenseMat matrix with the query points
        as rows in order to query many data points.

        For querying many data points, passing the queries as a DenseMat will
        be more efficient.

        @param q the query data point(s)
        @return the kernel densities for the given query point(s)
        """
        if isinstance(q, stag.data.DataPoint):
            return self.internal_kde.query(q.internal_datapoint)
        else:
            return self.internal_kde.query(q.internal_densemat)
