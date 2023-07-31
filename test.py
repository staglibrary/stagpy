import stag.graph
import stag.random
import stag.cluster
import scipy as sp
import scipy.sparse
import numpy as np


def main():
    vec1 = np.asarray([1, 1, 0, 0])
    vec2 = np.asarray([0, 0, 1, 1])
    ari = stag.cluster.adjusted_rand_index(vec1, vec2)
    print(ari)


if __name__ == "__main__":
    main()
