import stag.graph
import stag.random
import stag.cluster
import scipy as sp
import scipy.sparse


def main():
    graph = stag.random.sbm(10, 2, 1, 0)
    ccs = stag.cluster.connected_components(graph)
    print(ccs)
    print(type(ccs))


if __name__ == "__main__":
    main()
