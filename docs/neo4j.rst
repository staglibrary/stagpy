STAG and Neo4j
==============

The STAG Python library provides a convenient interface with Neo4j,
a popular graph database.
This allows graph algorithms to be executed directly on a graph stored in
the database.

This tutorial will give a quick introduction to Neo4j and demonstrate how to
run your first graph algorithms on a graph stored in Neo4j.
In this tutorial, we will connect to a Neo4j database running in the AuraDB
cloud service.
The STAG library can also connect to a database running locally.

Setting up a Neo4j Database
---------------------------

You should begin by following the introductory steps in the
`Neo4j documentation <https://neo4j.com/>`_ to set up a database in the cloud
using the AuraDB service.
We recommend first experimenting with the provided 'Movie' dataset.
You will need to note the following information when you create the new database
instance.

- The generated password for accessing the database instance.
- The connection URI.

Connecting to the Database with STAG
------------------------------------

Once the database instance is up and running, you can connect to it with the
following code.

.. code-block:: python

    import stag.neo4j
    connection_uri = "<your connection URI>"
    username = "neo4j"
    password = "<your password>"
    g = stag.neo4j.Neo4jGraph(connection_uri, username, password)

Then, we can test that the connection was successful by querying the database.
This command will return the degree of the node with ID 0.

.. code-block:: python

    print(g.degree(0))

