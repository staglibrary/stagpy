"""Algorithms for finding clusters in graphs."""
from typing import List, Tuple
import numpy as np

import stag.utility
from . import stag_internal
from . import graph
from . import utility


def spectral_cluster(g: graph.Graph, k: int) -> np.ndarray:
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
    @return an array ints giving the cluster membership for each vertex in the graph

    \par References
    A. Ng, M. Jordan, Y. Weiss.
    On spectral clustering: Analysis and an algorithm. NeurIPS'01
    """
    return stag_internal.spectral_cluster(g.internal_graph, k)


def cheeger_cut(g: graph.Graph) -> np.ndarray:
    r"""
    Find the Cheeger cut in a graph.

    Let \f$G = (V, E)\f$ be a graph and \f$\mathcal{L}\f$ be its normalised Laplacian
    matrix with eigenvalues \f$0 = \lambda_1 \leq \lambda_2 \leq \ldots \leq \lambda_n\f$.
    Then, Cheeger's inequality states that

    \f[
      \frac{\lambda_2}{2} \leq \Phi_G \leq \sqrt{2 \lambda_2},
    \f]

    where

    \f[
       \Phi_G = \min_{S \subset V} \phi(S)
    \f]

    is the conductance of \f$G\f$. The proof of Cheeger's inequality is
    constructive: by computing the eigenvector corresponding to \f$\lambda_2\f$,
    and performing the sweep set operation, we are able to find a set \f$S\f$
    with conductance close to the optimal. The partition returned by this
    algorithm is called the 'Cheeger cut' of the graph.

    @param g the graph object to be partitioned
    @return An array giving the cluster membership for each vertex in the graph.
            Each entry in the array is either \f$0\f$ or \f$1\f$ to indicate
            which side of the cut the vertex belongs to.
    """
    return stag_internal.cheeger_cut(g.internal_graph)


def local_cluster(g: graph.LocalGraph, seed_vertex: int, target_volume: float) -> np.ndarray:
    r"""
    Local clustering algorithm based on personalised Pagerank.

    Given a graph and starting vertex, return a cluster which is close to the
    starting vertex.

    This method uses the ACL local clustering algorithm.

    @param g a graph object implementing the LocalGraph interface
    @param seed_vertex the starting vertex in the graph
    @param target_volume the approximate volume of the cluster you would like to find
    @return an array containing the indices of vertices considered to be in the
            same cluster as the seed_vertex.

    \par References
    R. Andersen, F. Chung, K. Lang.
    Local graph partitioning using pagerank vectors. FOCS'06
    """
    return stag_internal.local_cluster(g.internal_graph, seed_vertex, target_volume)


def local_cluster_acl(g: graph.LocalGraph,
                      seed_vertex: int,
                      locality: float,
                      error: float = 0.001) -> np.ndarray:
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
    @return an array containing the indices of vertices considered to be in the
            same cluster as the seed_vertex.

    \par References
    R. Andersen, F. Chung, K. Lang.
    Local graph partitioning using pagerank vectors. FOCS'06
    """
    return stag_internal.local_cluster_acl(g.internal_graph,
                                           seed_vertex,
                                           locality,
                                           error)


def approximate_pagerank(g: graph.LocalGraph,
                         seed_vector: stag.utility.SprsMat,
                         alpha: float,
                         epsilon: float) -> Tuple[stag.utility.SprsMat,
                                                  stag.utility.SprsMat]:
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
                                              seed_vector.internal_sprsmat,
                                              alpha,
                                              epsilon)
    p = utility.SprsMat(apr[0])
    r = utility.SprsMat(apr[1])
    p.__parent = apr
    r.__parent = apr
    return p, r


@utility.convert_sprsmats
def sweep_set_conductance(g: graph.LocalGraph, v: stag.utility.SprsMat) -> np.ndarray:
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
    return stag_internal.sweep_set_conductance(g.internal_graph,
                                               v.internal_sprsmat)


def connected_component(g: graph.LocalGraph, v: int) -> np.ndarray:
    r"""
    Return the vertex indices of every vertex in the same connected component
    as the specified vertex.

    The running time of this method is proportional to the size of the returned
    connected component.

    The returned array is not sorted.

    @param g a stag.graph.LocalGraph object
    @param v a vertex of the graph
    @return an array containing the vertex ids of every vertex in the connected
            component corresponding to v
    """
    return stag_internal.connected_component(g.internal_graph, v)


def connected_components(g: graph.Graph) -> List[np.ndarray]:
    r"""
    Return a list of the connected components in the specified graph.

    @param g a stag.graph.Graph object
    @return a list containing the connected components of the graph
    """
    return list(stag_internal.connected_components(g.internal_graph))


@utility.convert_ndarrays
def adjusted_rand_index(gt_labels: np.ndarray, labels: np.ndarray) -> float:
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
    return stag_internal.adjusted_rand_index(gt_labels, labels)


@utility.convert_ndarrays
def mutual_information(gt_labels: np.ndarray, labels: np.ndarray) -> float:
    r"""
    Compute the Mutual Information between two label vectors.

    @param gt_labels the ground truth labels for the dataset
    @param labels the candidate labels whose MI should be calculated
    @return the MI between the two labels vectors
    """
    return stag_internal.mutual_information(gt_labels, labels)


@utility.convert_ndarrays
def normalised_mutual_information(gt_labels: np.ndarray,
                                  labels: np.ndarray) -> float:
    r"""
    Compute the Normalised Mutual Information between two label vectors.

    @param gt_labels the ground truth labels for the dataset
    @param labels the candidate labels whose NMI should be calculated
    @return the NMI between the two labels vectors

    \par References
    Vinh, Epps, and Bailey, (2009). Information theoretic measures for
    clusterings comparison. 26th Annual International Conference on Machine
    Learning (ICML ‘09).
    """
    return stag_internal.normalised_mutual_information(gt_labels, labels)


@utility.convert_ndarrays
def conductance(g: graph.LocalGraph, cluster: np.ndarray) -> float:
    r"""
     Compute the conductance of the given cluster in a graph.

    Given a graph \f$G = (V, E)\f$, the conductance of \f$S \subseteq V\f$
    is defined to be

    \f[
       \phi(S) = \frac{w(S, V \setminus S)}{\mathrm{vol}(S)},
    \f]

    where \f$\mathrm{vol}(S) = \sum_{v \in S} \mathrm{deg}(v)\f$ is the volume
    of \f$S\f$ and \f$w(S, V \setminus S)\f$ is the total weight of edges crossing
    the cut between \f$S\f$ and \f$V \setminus S\f$.

    @param g a stag.graph.LocalGraph object representing \f$G\f$.
    @param cluster an array of node IDs in \f$S\f$.
    @return the conductance \f$\phi_G(S)\f$.
    """
    return stag_internal.conductance(g.internal_graph, cluster)


@utility.convert_ndarrays
def symmetric_difference(s: np.ndarray, t: np.ndarray) -> np.ndarray:
    r"""
    Compute the symmetric difference of two sets of integers.

    Given sets \f$S\f$ and \f$T\f$, the symmetric difference \f$S \triangle T\f$
    is defined to be

    \f[
        S \triangle T = \{S \setminus T\} \cup \{T \setminus S\}.
    \f]

    Although \f$S\f$ and \f$T\f$ are provided as lists, they are treated as sets
    and any duplicates will be ignored.

    @param s an array containing the first set of integers
    @param t an array containing the second set of integers
    @return an array containing the vertices in the symmetric difference of
             \f$S\f$ and \f$T\f$.
    """
    return stag_internal.symmetric_difference(s, t)
