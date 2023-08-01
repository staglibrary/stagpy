import stag.graph
import stag.random
import stag.cluster
import scipy as sp
import scipy.sparse
import numpy as np


def main():
    g1 = stag.graph.barbell_graph(4)
    degrees = g1.degrees_unweighted([0, 1, 2, 3, 4, 5])
    print(degrees)


if __name__ == "__main__":
    main()
