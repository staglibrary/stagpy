"""
A demonstration of local clustering on a neo4j database.
"""
import argparse
import stag.neo4j
import stag.cluster


def parse_args():
    parser = argparse.ArgumentParser(description="Movies Demonstration")
    parser.add_argument('uri', type=str, help="The location of the Neo4j database.")
    parser.add_argument('user', type=str, help="The username to log into the database.")
    parser.add_argument('password', type=str, help="The password to access the database.")
    return parser.parse_args()


def main():
    args = parse_args()

    # Create the graph object
    g = stag.neo4j.Neo4jGraph(args.uri, args.user, args.password)

    # Find the node id corresponding to the matrix
    node_id = g.query_id('title', "The Matrix Reloaded")
    assert node_id is not None

    # Find a local cluster
    cluster = stag.cluster.local_cluster(g, node_id, 100)

    # Display the cluster
    print(f"Found cluster with the following {len(cluster)} nodes: ")
    for v_id in cluster:
        labels = g.query_node_labels(v_id)
        if 'Movie' in labels:
            title = g.query_property(v_id, 'title')
            print(f"Movie: {title}")
        elif 'Person' in labels:
            name = g.query_property(v_id, 'name')
            print(f"Person: {name}")


if __name__ == "__main__":
    main()
