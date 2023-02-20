"""
Read and write graphs to disk.
"""
from . import stag_internal
from . import graph


@graph.return_graph
def load_edgelist(filename: str) -> graph.Graph:
    """
    Load a graph from an edgelist file.

    We define an edgelist file in the following way.
      - Any lines beginning with '#' or '//' are ignored
      - Any blank lines are ignored
      - All other lines are of one of the formats
          - `<u>, <v>, <weight>`
          - `<u>, <v>`
          - `<u> <v> <weight>`
          - `<u> <v>`

        where `<u>` and `<v>` can be parsed as integers, and `<weight>` can be parsed
        as a double. If the weight is omitted, it is taken to be 1.

    Here is an example edgelist file.

    \code
    # This line is ignored
    0, 1, 0.5
    1, 2, 1
    2, 0, 0.5
    \endcode

    @param filename the name of the edgelist file to be loaded
    @return stag.graph.Graph object
    @throws runtime_error if the file doesn't exist or cannot be parsed as an edgelist
    """
    return stag_internal.load_edgelist(filename)


def save_edgelist(g: graph.Graph, filename: str):
    """
    Save a graph as an edgelist file.

    @param g the graph object to be saved
    @param filename the name of the file to save the edgelist data to
    """
    stag_internal.save_edgelist(g.internal_graph, filename)
