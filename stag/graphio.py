"""
Read and write graphs to disk.
"""
from . import stag_internal
from . import graph


@graph.return_graph
def load_edgelist(filename: str) -> graph.Graph:
    """
    Load a graph from an edgelist file.

    The edgelist file format is defined as follows.

    - Any lines beginning with ``#`` or ``//`` are ignored
    - Any blank lines are ignored
    - All other lines are of one of the following formats:

      - ``u, v, w``
      - ``u, v``
      - ``u v w``
      - ``u v``

    where ``u`` and ``v`` can be parsed as integers, and ``w`` can be parsed
    as a float.
    If the weight is omitted, it is taken to be :math:`1` .
    The data lines of the edgelist file should all have the same format.

    :return: a :class:`stag.graph.Graph` object constructed from the given edgelist file
    :except: error if the file cannot be parsed as an edgelist
    """
    return stag_internal.load_edgelist(filename)


def save_edgelist(g: graph.Graph, filename: str):
    """
    Save a graph as an edgelist file.

    :param g: the graph object to be saved
    :param filename: the name of the file to save the edgelist data to
    """
    stag_internal.save_edgelist(g.internal_graph, filename)
