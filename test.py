import stag.graph
import scipy as sp
import scipy.sparse


def main():
    adj_mat = sp.sparse.csr_matrix([[0, 1, 1, 1], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0]])
    graph = stag.graph.Graph(adj_mat)
    lap = graph.laplacian()
    print(lap.todense())
    print(graph.volume())


if __name__ == "__main__":
    main()
