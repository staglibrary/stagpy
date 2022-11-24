"""Algorithms for finding clusters in graphs."""
import scipy.sparse
from typing import List, Tuple

from . import stag_internal
from . import graph
from . import utility


def local_cluster(g: graph.LocalGraph, seed_vertex: int, target_volume) -> List[int]:
    """
    Default local clustering algorithm.

    Given a graph and starting vertex, return a cluster which is close to the
    starting vertex. The ``target_volume`` parameter controls the size of the
    returned cluster.

    You should set ``target_volume`` to be your best guess for the volume of the
    cluster you would like to find. For example, the following code will find
    one of the 'clusters' in a barbell graph.

    .. code-block:: python

        import stag.graph
        import stag.cluster
        graph = stag.graph.barbell_graph(5)
        cluster = stag.cluster.local_cluster(graph, 1, 21)

    This method calls through to the :meth:`local_cluster_acl` method.

    :param g: a :class:`stag.graph.LocalGraph` object
    :param seed_vertex: the starting vertex in the graph
    :param target_volume: the approximate volume of the target cluster
    :return: a list of vertices in the same cluster as the seed vertex
    """
    return list(stag_internal.local_cluster(g.internal_graph, seed_vertex, target_volume))


def local_cluster_acl(g: graph.LocalGraph,
                      seed_vertex: int,
                      locality: float,
                      error=0.001) -> List[int]:
    """
    The ACL local clustering algorithm.

    Given a graph and starting vertex, returns a cluster close to the starting vertex.

    The ``locality`` and ``error`` parameters correspond to the :math:`\\alpha`
    and :math:`\\epsilon` parameters of the ACL algorithm.

    :param g: a graph object implementing the LocalGraph interface
    :param seed_vertex: the starting vertex in the graph
    :param locality:
      a value in :math:`(0, 1]` indicating how 'local' the cluster should
      be. A value of :math:`1` will return only the seed vertex
      and a value of :math:`0` will explore the whole graph.
    :param error: (optional) the acceptable error in the calculation of the approximate
                  pagerank. A smaller error will result in longer running time and
                  higher quality cluster.
    :return: a list containing the indices of vertices considered to be in the
             same cluster as the seed_vertex.
    :reference:
        [ACL] Andersen, Reid, Fan Chung, and Kevin Lang.
        "Local graph partitioning using pagerank vectors." FOCS'06.
    """
    return list(stag_internal.local_cluster_acl(g.internal_graph,
                                                seed_vertex,
                                                locality,
                                                error))


def approximate_pagerank(g: graph.LocalGraph,
                         seed_vector: scipy.sparse.csc_matrix,
                         alpha: float,
                         epsilon: float) -> Tuple[scipy.sparse.csc_matrix,
                                                  scipy.sparse.csc_matrix]:
    """
    Compute the approximate pagerank vector.

    The approximate pagerank vector :math:`\mathrm{apr}_G(s, \\alpha, \\epsilon)`
    is defined in [ACL] and this method implements their proposed algorithm
    for computing it.

    This method forms an important part of the :meth:`local_cluster_acl`
    algorithm.

    Note that the dimension of the returned vectors may not match the true
    number of vertices in the graph provided since the approximate
    pagerank is computed locally.

    :param g: a :class:`stag.graph.LocalGraph`
    :param seed_vector: a sparse column matrix defining the starting
                        distribution on the graph. Although this is a matrix type,
                        it should have exactly one column.
    :param alpha: a value in :math:`(0, 1]` controlling the teleportation parameter
                  of the personalised Pagerank.
    :param epsilon: a value in :math:`(0, 1]` controlling the approximation
                    guarantee.
    :return:
        - :math:`p` : the approximate pagerank vector
        - :math:`r` : the residual vector

    :raises ArgumentError: if the provided ``seed_vector`` is not a column vector.
    :reference:
        [ACL] Andersen, Reid, Fan Chung, and Kevin Lang.
        "Local graph partitioning using pagerank vectors." FOCS'06.
    """
    apr = stag_internal.approximate_pagerank(g.internal_graph,
                                              utility.scipy_to_swig_sprs(seed_vector),
                                              alpha,
                                              epsilon)
    return utility.swig_sprs_to_scipy(apr[0]), utility.swig_sprs_to_scipy(apr[1])


def sweep_set_conductance(g: graph.LocalGraph, v: scipy.sparse.csc_matrix) -> List[int]:
    """
    Find the sweep set of the given vector with the minimum conductance.
   
    First, sort the vertices such that :math:`v(1) \leq v(2) \leq \ldots \leq v(n)` .
    Then, let

    .. math::

        S_i = \\{j : j <= i\\}

    and return the set of original vertex indices that correspond to

    .. math::

        \\mathrm{argmin}_i \\quad \\phi(S_i),

    where

    .. math::

        \\phi(S_i) = \\frac{w(S_i, \overline{S_i})}{\mathrm{vol}(S_i)}

    is the conductance of :math:`S_i` .

    This method is expected to be run on vectors whose support is much less
    than the total size of the graph. If the total volume of the support of ``v``
    is larger than half of the volume of the total graph, then this method is
    likely to return the total support of ``v``.
   
    :param g: the :class:`stag.graph.LocalGraph` on which to operate
    :param v: a sparse column vector
    :return: a list of the indices of v which give the minimum
            conductance
    """
    return stag_internal.sweep_set_conductance(g.internal_graph, utility.scipy_to_swig_sprs(v))
