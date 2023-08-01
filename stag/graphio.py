"""
Read and write graphs to disk.
"""
from . import stag_internal
from . import graph


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
    return graph.Graph(stag_internal.load_edgelist(filename))


def save_edgelist(g: graph.Graph, filename: str):
    """
    Save a graph as an edgelist file.

    @param g the graph object to be saved
    @param filename the name of the file to save the edgelist data to
    """
    stag_internal.save_edgelist(g.internal_graph, filename)


def load_adjacencylist(filename: str) -> graph.Graph:
    r"""
     Load a graph from an adjacencylist file.

    The adjacency list file format is defined in the following way.
      - Any lines beginning with `#` or `//` are ignored
      - Any blank lines are ignored
      - All other lines have the format `<node_id>: <list of neighbours>`, where
        `<node_id>` is an integer and `<list of neighbours>` is either a
        space-separated list of integers or a space-separated list of
        `<id>:<weight>` where `<id>` gives the id of the neighbour and
        `<weight>` is the weight of the edge.
      - The `<node IDs>` of each line must be sorted in increasing order.
      - The graph should have no self-loops.

    Here is an example adjacencylist file.

        # This line is ignored
        0: 1 2
        1: 0 2 3
        2: 0 1
        3: 1

    The following example includes weighted edges.

        # This line is ignored
        0: 1:0.5 2:0.5
        1: 0:0.5 2:1
        2: 0:0.5 1:1

    Note that this method loads the entire graph into memory. For large graphs,
    the stag.graph.AdjacencyListLocalGraph object can be used to access the graph
    in a 'local' way without reading the entire graph into memory.

    @param filename the name of the adjacency list file to be loaded
    @return stag.graph.Graph object
    @throws runtime_error if the file doesn't exist or cannot be parsed as
            an adjacency list
    """
    return graph.Graph(stag_internal.load_adjacencylist(filename))


def save_adjacencylist(g: graph.Graph, filename: str):
    r"""
    Save a graph as an adjacency list file.

    @param g the graph object to be saved.
    @param filename the name of the file to save the adjacency list data to.
    """
    stag_internal.save_adjacencylist(g.internal_graph, filename)


def edgelist_to_adjacencylist(edgelist_fname: str, adjacencylist_fname: str):
    r"""
    Convert an edgelist file to an adjacency list.

    @param edgelist_fname the name of the file containing the edgelist.
    @param adjacencylist_fname the name of the file to write the adjacency list.
    """
    stag_internal.edgelist_to_adjacencylist(edgelist_fname, adjacencylist_fname)


def adjacencylist_to_edgelist(adjacencylist_fname: str, edgelist_fname: str):
    r"""
    Convert an adjacency list file to an edgelist.

    @param adjacencylist_fname the name of the file containing the adjacency list.
    @param edgelist_fname the name of the file to write the edgelist.
    """
    stag_internal.adjacencylist_to_edgelist(adjacencylist_fname, edgelist_fname)
