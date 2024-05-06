"""
Implementation of the Euclidean locality-sensitive hashing algorithm.
"""
import numpy as np
from typing import Union

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

