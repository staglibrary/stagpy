STAG and Neo4j
==============

The stag.neo4j.Neo4jGraph object provides a convenient interface with Neo4j,
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
[Neo4j documentation](https://neo4j.com/) to set up a database in the cloud
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

~~~~~~~{python}
    import stag.neo4j
    connection_uri = "<your connection URI>"
    username = "neo4j"
    password = "<your password>"
    g = stag.neo4j.Neo4jGraph(connection_uri, username, password)
~~~~~~~

Then, we can test that the connection was successful by querying the database.
This command will return the degree of the node with ID 0.

~~~~~~~{python}
    print(g.degree(0))
~~~~~~~

Finding Clusters in the Graph
-----------------------------
Once we have connected successfully to the database, we can find a cluster in
the data.

~~~~~~~{python}
    import stag.cluster
    cluster = stag.cluster.local_cluster(g, 0, 100)
~~~~~~~

Then, assuming we are testing against the Neo4j movies dataset, we can display
the cluster as follows.

~~~~~~~{python}
    for node in cluster:
        labels = g.query_node_labels(node)
        if 'Movie' in labels:
            print(g.query_property(node, 'title'))
        elif 'Person' in labels:
            print(g.query_property(node, 'name'))
~~~~~~~
