Getting Started
===============
The STAG library is an easy-to-use Python library providing several spectral
algorithms for graphs.
The library is based on the STAG C++ library.

Installation
------------
Begin by installing STAG via pip, the python package manager.

.. code-block::

   pip install stag

Creating Graphs
---------------
The core graph object is :class:`stag.graph.Graph` which can be created using
a sparse adjacency matrix.

.. code-block:: python

    import stag.graph
    import scipy.sparse
    adj_mat = scipy.sparse.csc_matrix([[0, 1, 1, 1],
                                       [1, 0, 1, 1],
                                       [1, 1, 0, 1],
                                       [1, 1, 1, 0]])
    g = stag.graph.Graph(adj_mat)

You can also create a variety of standard graphs using the :mod:`stag.graph` module.
For example, to create a complete graph on :math:`5` vertices, use the following
code.

.. code-block:: python

    import stag.graph
    g = stag.graph.complete_graph(5)

You can see the adjacency matrix of your constructed graphs with the following.

.. code-block:: python

    import scipy.sparse
    print(g.adjacency().todense())

Notice that the :meth:`stag.graph.Graph.adjacency` method returns a sparse ``scipy``
matrix and we make this dense with the ``todense()`` method.

Reading Graphs from Disk
------------------------

STAG supports the edgelist file format for reading graphs from disk and the
:mod:`stag.graphio` module provides methods for reading and writing them.

Suppose you have a simple edgelist file like this one.

.. code-block::
    :caption: graph.edgelist

    0 1
    1 2
    0 2
    2 3
    3 4
    4 5
    3 5

Then, we can read it as follows.

.. code-block:: python

    >>> import stag.graphio
    >>> g = stag.graphio.load_edgelist("graph.edgelist")
    >>> print(g.agjacency().todense())
    [[0. 1. 1. 0. 0. 0.]
     [1. 0. 1. 0. 0. 0.]
     [1. 1. 0. 1. 0. 0.]
     [0. 0. 1. 0. 1. 1.]
     [0. 0. 0. 1. 0. 1.]
     [0. 0. 0. 1. 1. 0.]]

We can also save graphs as an edgelist.

.. code-block:: python

    import stag.graph
    import stag.graphio
    g = stag.graph.star_graph(5)
    stag.graphio.save_edgelist(g, "star.edgelist")

Edgelist files can also include edge weights as a third parameter - notice that
the generated ``star.edgelist`` file specifies an edge weight of :math:`1` for
every edge.

.. code-block::
    :caption: star.edgelist

    0 1 1
    0 2 1
    0 3 1
    0 4 1

Finding Clusters
----------------

The :mod:`stag.cluster` module provides methods for finding clusters in graphs
using local clustering algorithms.
The main method provided by this module is :meth:`stag.cluster.local_cluster` .
This method takes three arguments:

- **g** - a STAG graph object;
- **seed_vertex** - the ID of a vertex in the graph;
- **target_volume** - an estimate of the volume of the cluster to find.
  To estimate the target volume, you could first estimate the number of vertices
  in the cluster you would like to find, and then multiply by the degree of the
  seed vertex.

Given these arguments, :meth:`stag.cluster.local_cluster` will return a list
of vertices which form a cluster around the seed vertex, and whose total volume
is close to the target volume.

For example, to find the clusters in a barbell graph:

.. code-block:: python

    import stag.graph
    import stag.cluster
    g = stag.graph.barbell_graph(5)
    cluster = stag.cluster.local_cluster(g, 0, 20)
    print(cluster)
    cluster = stag.cluster.local_cluster(g, 9, 20)
    print(cluster)

