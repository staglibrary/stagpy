import stag.graph
import stag.random
import stag.cluster
import scipy as sp
import scipy.sparse


def main():
    adj_mat = scipy.sparse.csc_matrix([[0, -1, 0, 1],
                                       [-1, 0, 1, 0],
                                       [0, 1, 0, 1],
                                       [1, 0, 1, 0]])
    g = stag.graph.Graph(adj_mat)
    cluster = stag.cluster.local_cluster(g, 0, 10)
    print(g.adjacency().todense())
    print(cluster)


if __name__ == "__main__":
    main()
