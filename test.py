import stag.graph
import scipy as sp
import scipy.sparse


def main():
    graph = stag.graph.cycle_graph(10)
    lap = graph.laplacian()
    print(lap.todense())
    print(graph.volume())


if __name__ == "__main__":
    main()
