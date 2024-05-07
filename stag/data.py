"""
Methods for processing datasets.
"""
import numpy as np

import stag.utility
from . import stag_internal
from . import utility

class DataPoint(object):
    """
    A data point in d-dimensional space.

    A data point is a reference to a single row of a data matrix.
    """

    def __init__(self, mat: utility.DenseMat, row: int):
        """
        Initialise a data point object.

        This object refers to a single row of the provided stag.utility.DenseMat
        object.
        """
        ##
        # \cond
        ##
        if isinstance(mat, stag_internal.DataPoint):
            self.internal_datapoint = mat
        else:
            self.internal_datapoint = stag_internal.DataPoint(mat.internal_densemat, row)
        ##
        # \endcond
        ##

    def dimension(self) -> int:
        """Get the number of dimensions of this data point."""
        return self.internal_datapoint.dimension

    def to_numpy(self) -> np.ndarray:
        """Convert this data point to a numpy array."""
        return self.internal_datapoint.to_vector()

def load_matrix(filename: str) -> stag.utility.DenseMat:
    r"""
    Load data into a matrix from a file.

    Each line of the file corresponds to a row in the matrix. On each row,
    matrix entries should be separated by blank spaces, or commas.
    Every row in the file must contain the same number of entries.

    Lines beginning with '#' or '//' are ignored.

    @param filename the name of the file containing the data
    @return a stag.utility.DenseMat containing the data from the file
    @throws a runtime exception  if the file doesn't exist or cannot be parsed
    """
    return stag.utility.DenseMat(stag_internal.load_matrix(filename))
