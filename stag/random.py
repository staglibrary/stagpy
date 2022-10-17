from . import stag_internal
from .utility import return_graph


@return_graph
def sbm(n: int, k: int, p: float, q: float):
    return stag_internal.sbm(n, k, p, q)


@return_graph
def erdos_renyi(n: int, p: float):
    return stag_internal.erdos_renyi(n, p)
