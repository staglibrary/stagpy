"""Algorithms for finding clusters in graphs."""
import scipy.sparse
from typing import List, Tuple

from . import stag_internal
from . import graph
from . import utility


def spectral_cluster(g: graph.Graph, k: int) -> List[int]:
    r"""
    Spectral clustering algorithm.

    This is a simple graph clustering method, which provides a clustering of the entire graph.
    To use spectral clustering, simply pass a `stag.graph.Graph` object
    and the number of clusters you would like to find.

    \code{python}
    import stag.graph
    import stag.cluster

    myGraph = stag.graph.Graph.barbell_graph(10)
    labels = stag.cluster.spectral_cluster(myGraph, 2)
    print(labels)
    \endcode

    The spectral clustering algorithm has the following steps.
      - Compute the \f$k\f$ smallest eigenvectors of the normalised Laplacian matrix.
      - Embed the vertices into \f$\mathbb{R}^k\f$ according to the eigenvectors.
      - Cluster the vertices into \f$k\f$ clusters using a \f$k\f$-means clustering algorithm.

    @param g the graph object to be clustered
    @param k the number of clusters to find. Should be less than \f$n/2\f$.
    @return a list of ints giving the cluster membership for each vertex in the graph

    \par References
    A. Ng, M. Jordan, Y. Weiss.
    On spectral clustering: Analysis and an algorithm. NeurIPS'01
    """
    return list(stag_internal.spectral_cluster(g.internal_graph, k))

def local_cluster(g: graph.LocalGraph, seed_vertex: int, target_volume: float) -> List[int]:
    r"""
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
    r"""
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
    r"""
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
    r"""
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


def adjusted_rand_index(gt_labels: List[int], labels: List[int]) -> float:
    r"""
    Compute the Adjusted Rand Index between two label vectors.

    @param gt_labels the ground truth labels for the dataset
    @param labels the candidate labels whose ARI should be calculated
    @return the ARI between the two labels vectors

    \par References
    W. M. Rand.
    Objective criteria for the evaluation of clustering methods.
    Journal of the American Statistical Association. 66 (336): 846–850. 1971.
    """
    return stag_internal.adjusted_rand_index(stag_internal.vectorl(gt_labels),
                                             stag_internal.vectorl(labels))
