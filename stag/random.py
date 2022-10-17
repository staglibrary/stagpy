from . import stag_internal
from .utility import return_graph


@return_graph
def sbm(n: int, k: int, p: float, q: float):
    return stag_internal.sbm(n, k, p, q)
