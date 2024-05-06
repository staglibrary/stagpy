"""
Methods for processing datasets.
"""
import numpy as np
from . import stag_internal
from . import utility

class DataPoint(object):
    """
    A data point in d-dimensional space.

    A data point is a reference to a single row of a data matrix.
    """

    def __init__(self, mat: utility.DenseMat, row: int, int_dp=None):
        if int_dp is not None:
            self.internal_datapoint = int_dp
        else:
            self.internal_datapoint = stag_internal.DataPoint(mat.internal_densemat, row)

    def dimension(self) -> int:
        """Get the number of dimensions of this data point."""
        return self.internal_datapoint.dimension

    def to_numpy(self) -> np.ndarray:
        """Convert this data point to a numpy array."""
        return self.internal_datapoint.to_vector()
