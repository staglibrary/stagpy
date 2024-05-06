r"""
Implementation of the Euclidean locality-sensitive hashing algorithm.

Locality-sensitive hashing is a primitive used for near-neighbour search.
In particular, a locality sensitive hash function (see stag.lsh.LSHFunction)
hashes vectors into buckets such that two vectors are more likely to be hashed
to the same bucket if their Euclidean distance is small.

The stag.lsh.E2LSH hash table implements a full approximate-near neighbor
data structure based on basic Euclidean locality sensitive hash functions.

\par Reference
Andoni, Alexandr, and Piotr Indyk. "Near-optimal hashing algorithms for approximate nearest neighbor in high
dimensions." Communications of the ACM 51.1 (2008): 117-122.
"""
import numpy as np
from typing import Union, List

import stag.data
from . import stag_internal
from . import utility
from . import data


class LSHFunction(object):
    r"""
    \brief A Euclidean locality-sensitive hash function.

    A function drawn at random from the standard family of Euclidean
    locality-sensitive hhash functions.
    This function is defined by a random vector \f$a \in \mathbb{R}^d\f$
    drawn from a Gaussian distribution, and a random offset
    \f$b \in [0, 4]\f$ drawn uniformly at random.
    Applying the function to some data point \f$x \in \mathbb{R}^d\f$ is
    equivalent to computing
    \f[
        h = \left\lfloor  \frac{\langle a, x \rangle + b}{4} \right\rfloor.
    \f]

    Given two data points \f$x_1\f$ and \f$x_2\f$, the probability that they
    are hashed to the same value is given by

    \f[
       p\left(\|x_1 - x_2\|_2\right) = \int_0^4 \frac{1}{\|x_1 - x_2\|_2} f\left(\frac{t}{\|x_1 - x_2\|_2}\right)\left(1 - \frac{t}{4}\right) \mathrm{dt},
    \f]

    where \f$f(\cdot)\f$ is the probability density function of the Gaussian
    distribution. The stag.lsh.LSHFunction.collision_probability function
    computes this value.

    Typical STAG users will use the E2LSH hash table rather than these
    the LSHFunction class directly.
    """

    def __init__(self, dimension: int):
        r"""
        Initialise a random LSH function with the given dimension.

        @param dimension the dimensionality of the data
        """
        self.internal_function: stag_internal.LSHFunction =\
            stag_internal.LSHFunction(dimension)

    @utility.convert_ndarrays
    def apply(self, point: Union[np.ndarray, data.DataPoint]) -> int:
        r"""
        Apply this hash function to the given data point.

        :param point: a numpy array or stag.data.DataPoint
        :return: the hashed value of this point
        """
        if isinstance(point, np.ndarray):
            densemat = utility.DenseMat(point)
            dp = data.DataPoint(densemat, 0)
        else:
            if not isinstance(point, data.DataPoint):
                raise TypeError("Data point must be ndarray or stag.data.DataPoint")
            dp = point
        return self.internal_function.apply(dp.internal_datapoint)

    @staticmethod
    def collision_probability(distance: float) -> float:
        r"""
        For two points at a given distance \f$c\f$, compute the probability that
        they will collide in a random Euclidean LSH function.

        This probability is given by

        \f[
          p(c) = \int_0^4 \frac{1}{c} f\left(\frac{t}{c}\right)\left(1 - \frac{t}{4}\right) \mathrm{dt},
        \f]

        where \f$f(\cdot)\f$ is the probability density function of the Gaussian
        distribution.
        This is equivalent to

        \f[
          p(c)=-\frac{1}{2\sqrt{2\pi}}\left( c e^{-\frac{8}{c^2}} \right) \left( e^{\frac{8}{c^2}} -1 \right) + \mathrm{erf}\left(\frac{2\sqrt{2}}{c}\right),
        \f]

        where \f$\mathrm{erf}(\cdot)\f$ is the [error function](https://en.wikipedia.org/wiki/Error_function).

        @param distance the distance \f$c\f$.
        @return the collision probability of two points at distance \f$c\f$.
        """
        return stag_internal.LSHFunction.collision_probability(distance)


class E2LSH(object):
    r"""
    \brief A Euclidean locality sensitive hash table.

    The E2LSH hash table is constructed with some set of data points, which are
    hashed with several copies of the stag::LSHFunction.

    Then, for any query point, the data structure returns the points in the
    original dataset which are close to the query point.
    The probability that a given point \f$x\f$ in the data set is returned for
    query \f$q\f$ is dependent on the distance between \f$q\f$ and \f$x\f$.

    The E2LSH hash table takes two parameters, K and L, which control the
    probability that two points will collide in the hash table.
    For query point \f$q\f$, a data point \f$x\f$ at distance \f$c \in \mathbb{R}\f$
    from \f$q\f$ is returned with probability
    \f[
       1 - (1 - p(c)^K)^L,
    \f]
    where \f$p(c)\f$ is the probability that a single stag::LSHFunction will
    hash \f$q\f$ and \f$x\f$ to the same value.
    This probability can be computed with the stag::E2LSH::collision_probability
    method.

    Larger values of K and L will increase both the construction and query time
    of the hash table.
    """

    def __init__(self, K: int, L: int, dataset: List[stag.data.DataPoint]):
        self.K = K
        self.L = L
        self.internal_e2lsh = stag.stag_internal.E2LSH(
            K, L, [dp.internal_datapoint for dp in dataset])

    def get_near_neighbors(self, query: stag.data.DataPoint) -> List[stag.data.DataPoint]:
        """
        Query the LSH table to find the near neighbors of a given query point.

        Each point in the dataset will be returned with some probability dependent
        on the distance to the query point and the parameters K and L.

        @param query the data point to be queried
        @return a list of stag.data.DataPoint objects representing the colliding
                data points.
        """
        results = [data.DataPoint(None, None, int_dp=dp) for dp in self.internal_e2lsh.get_near_neighbors(query.internal_datapoint)]
        for dp in results:
            dp.__parent = self
        return results

    def collision_probability(self, distance: float) -> float:
        """
        Compute the probability that a data point at a given distance from a
        query point will be returned by this hash table.

        @param distance the distance between a query point and data point
        """
        return stag.stag_internal.E2LSH.collision_probability(self.K, self.L, distance)
