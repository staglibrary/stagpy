"""Algorithms for finding clusters in graphs."""
import scipy.sparse
from typing import List, Tuple

from . import stag_internal
from . import graph
from . import utility


def local_cluster(g: graph.LocalGraph, seed_vertex: int, target_volume: float) -> List[int]:
    """
    Local clustering algorithm based on personalised Pagerank.

    Given a graph and starting vertex, return a cluster which is close to the
    starting vertex.

    This method uses the ACL local clustering algorithm.

    @param g a graph object implementing the LocalGraph interface
    @param seed_vertex the starting vertex in the graph
    @param target_volume the approximate volume of the cluster you would like to find
    @return a vector containing the indices of vectors considered to be in the
            same cluster as the seed_vertex.

    \par References
    R. Andersen, F. Chung, K. Lang.
    Local graph partitioning using pagerank vectors. FOCS'06
    """
    return list(stag_internal.local_cluster(g.internal_graph, seed_vertex, target_volume))


def local_cluster_acl(g: graph.LocalGraph,
                      seed_vertex: int,
                      locality: float,
                      error: float = 0.001) -> List[int]:
    """
    The ACL local clustering algorithm. Given a graph and starting vertex,
    returns a cluster close to the starting vertex, constructed in a local way.

    The locality parameter is passed as the alpha parameter in the personalised
    pagerank calculation.

    @param g a graph object implementing the LocalGraph interface
    @param seed_vertex the starting vertex in the graph
    @param locality a value in \f$[0, 1]\f$ indicating how 'local' the cluster should
                    be. A value of \f$1\f$ will return the return only the seed vertex
                    and a value of \f$0\f$ will explore the whole graph.
    @param error (optional) - the acceptable error in the calculation of the approximate
                              pagerank. Default \f$0.001\f$.
    @return a vector containing the indices of vectors considered to be in the
            same cluster as the seed_vertex.

    \par References
    R. Andersen, F. Chung, K. Lang.
    Local graph partitioning using pagerank vectors. FOCS'06
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

    The parameters s, alpha, and epsilon are used as described in the ACL paper.

    Note that the dimension of the returned vectors may not match the true
    number of vertices in the graph provided since the approximate
    pagerank is computed locally.

    @param g a stag.graph.LocalGraph object
    @param seed_vector the seed vector of the personalised pagerank
    @param alpha the locality parameter of the personalised pagerank
    @param epsilon the error parameter of the personalised pagerank
    @return A tuple of sparse column vectors corresponding to
             - p: the approximate pagerank vector
             - r: the residual vector

            By the definition of approximate pagerank, it is the case that
               p + ppr(r, alpha) = ppr(s, alpha).

    @throws argument_error if the provided seed_vector is not a column vector.

    \par References
    R. Andersen, F. Chung, K. Lang.
    Local graph partitioning using pagerank vectors. FOCS'06
    """
    apr = stag_internal.approximate_pagerank(g.internal_graph,
                                              utility.scipy_to_swig_sprs(seed_vector),
                                              alpha,
                                              epsilon)
    return utility.swig_sprs_to_scipy(apr[0]), utility.swig_sprs_to_scipy(apr[1])


def sweep_set_conductance(g: graph.LocalGraph, v: scipy.sparse.csc_matrix) -> List[int]:
    """
    Find the sweep set of the given vector with the minimum conductance.

    First, sort the vector such that \f$v_1, \ldots, v_n\f$. Then let

    \f[
        S_i = \{v_j : j <= i\}
    \f]

    and return the set of original indices corresponding to

    \f[
        \mathrm{argmin}_i \phi(S_i)
    \f]

    where \f$\phi(S)\f$ is the conductance of \f$S\f$.

    This method is expected to be run on vectors whose support is much less
    than the total size of the graph. If the total volume of the support of vec
    is larger than half of the volume of the total graph, then this method may
    return unexpected results.

    Note that the caller is responsible for any required normalisation of the
    input vector. In particular, this method does not normalise the vector by
    the node degrees.

    @param g a stag.graph.LocalGraph object
    @param v the vector to sweep over
    @return a vector containing the indices of vec which give the minimum
            conductance in the given graph
    """
    return stag_internal.sweep_set_conductance(g.internal_graph, utility.scipy_to_swig_sprs(v))
