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

