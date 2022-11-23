Getting Started
===============
The STAG library is an easy-to-use Python library providing several spectral
algorithms for graphs.
The library is based on the STAG C++ library.

Installation
------------
Begin by installing STAG via pip.

.. code-block::

   pip install stag

Creating Graphs
---------------

You can create a variety of standard graphs using the :mod:`stag.graph` module.
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
matrix and we make this dense with the ``todense`` method.
