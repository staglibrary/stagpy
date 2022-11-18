import scipy.sparse

from . import stag_internal
from . import graph
from . import utility


def local_cluster(g: graph.LocalGraph, seed_vertex: int, target_volume: int):
    """
    Default local clustering algorithm. Given a graph and starting vertex,
    return a cluster which is close to the starting vertex.

    This method defaults to use the ACL local clustering algorithm.

    [ACL] Andersen, Reid, Fan Chung, and Kevin Lang.
    "Local graph partitioning using pagerank vectors." 2006
    47th Annual IEEE Symposium on Foundations of Computer Science (FOCS'06). IEEE, 2006.

    :param g: - a graph object implementing the LocalGraph interface
    :param seed_vertex: - the starting vertex in the graph
    :param target_volume: - the approximate volume of the cluster you would like to find
    :return: a vector containing the indices of vectors considered to be in the
            same cluster as the seed_vertex.
    """
    return stag_internal.local_cluster(g.internal_graph, seed_vertex, target_volume)


def local_cluster_acl(g: graph.LocalGraph, seed_vertex: int, locality: float, error=0.001):
    """
    The ACL local clustering algorithm. Given a graph and starting vertex,
    returns a cluster close to the starting vertex, constructed in a local way.

    The locality parameter is passed as the alpha parameter in the personalised
    pagerank calculation.

    [ACL] Andersen, Reid, Fan Chung, and Kevin Lang.
    "Local graph partitioning using pagerank vectors." 2006
    47th Annual IEEE Symposium on Foundations of Computer Science (FOCS'06). IEEE, 2006.

    :param g: - a graph object implementing the LocalGraph interface
    :param seed_vertex: - the starting vertex in the graph
    :param locality: - a value in [0, 1] indicating how 'local' the cluster should
                      be. A value of '1' will return the return only the seed vertex
                      and a value of '0' will explore the whole graph.
    :param error: (optional) - the acceptable error in the calculation of the approximate
                              pagerank. Default 0.001.
    :return: a vector containing the indices of vectors considered to be in the
            same cluster as the seed_vertex.
    """
    return stag_internal.local_cluster_acl(g.internal_graph, seed_vertex, locality, error)


def approximate_pagerank(g: graph.LocalGraph, seed_vector: scipy.sparse.csc_matrix, alpha: float, epsilon: float):
    """
    Compute the approximate pagerank vector as described in ACL:

    [ACL] Andersen, Reid, Fan Chung, and Kevin Lang.
    "Local graph partitioning using pagerank vectors." 2006
    47th Annual IEEE Symposium on Foundations of Computer Science (FOCS'06). IEEE, 2006.

    The parameters s, alpha, and epsilon are used as described in the paper.

    Note that the dimension of the returned vectors may not match the true
    number of vertices in the graph provided since the approximate
    pagerank is computed locally.

    :param g:
    :param seed_vector:
    :param alpha:
    :param epsilon:
    :return: A tuple of sparse column vectors corresponding to
               p - the approximate pagerank vector
               r - the residual vector
            By the definition of approximate pagerank, it is the case that
               p + pr(r, alpha) = pr(s, alpha)

    :raises ArgumentError: if the provided seed_vector is not a column vector.
    """
    apr = stag_internal.approximate_pagerank(g.internal_graph,
                                              utility.scipy_to_swig_sprs(seed_vector),
                                              alpha,
                                              epsilon)
    return utility.swig_sprs_to_scipy(apr[0]), utility.swig_sprs_to_scipy(apr[1])


def sweep_set_conductance(g: graph.LocalGraph, vec: scipy.sparse.csc_matrix):
    """
    Find the sweep set of the given vector with the minimum conductance.
   
    First, sort the vector, and then let
        S_i = {v_j : j <= i}
    and return the set of original indices corresponding to
        argmin_i conducance(S_i)
   
    This method is expected to be run on vectors whose support is much less
    than the total size of the graph. If the total volume of the support of vec
    is larger than half of the volume of the total graph, then this method may
    return unexpected results.
   
    :param: graph
    :param: vec
    :return: a vector containing the indices of vec which give the minimum
            conductance in the given graph
    """
    return stag_internal.sweep_set_conductance(g.internal_graph, utility.scipy_to_swig_sprs(vec))
