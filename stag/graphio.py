from . import stag_internal
from . import graph
from .utility import return_graph


@return_graph
def load_edgelist(filename: str):
    """
    Load a graph from an edgelist file.

    We define an edgelist file in the following way.
      - Any lines beginning with '#' or '//' are ignored
      - Any blank lines are ignored
      - All other lines are of some format:
          <u>, <v>, <weight>
          <u>, <v>
          <u> <v> <weight>
          <u> <v>
        where <u> and <v> can be parsed as integers, and <weight> can be parsed
        as a double. If the weight is ommitted, it is taken to be 1. The
        data lines of the edgelist file should all have the same format.

    :return: a STAG graph object constructed from the given edgelist file
    :except: error if the file cannot be parsed as an edgelist
    """
    return stag_internal.load_edgelist(filename)


def save_edgelist(g: graph.Graph, filename: str):
    """
    Save the given graph as an edgelist file.

    :param g: the graph object to be saved
    :param filename: the name of the file to save the edgelist data to
    """
    stag_internal.save_edgelist(g.internal_graph, filename)
