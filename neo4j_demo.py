"""
A demonstration of local clustering on a neo4j database of the wikipedia graph.
"""
import argparse
import stag.neo4j
import stag.cluster


def get_wikipedia_page_id(g: stag.neo4j.Neo4jGraph, title: str):
    return g.query_id('title', title)


def get_wikipedia_title(g: stag.neo4j.Neo4jGraph, id: int):
    return g.query_property(id, 'title')


def parse_args():
    parser = argparse.ArgumentParser(description="Wikipedia Demonstration")
    parser.add_argument('pageTitle', type=str, help="The title of the starting wikipedia page.")
    parser.add_argument('clusterVolume', type=float, help="The volume of the cluster you would like to find.")
    return parser.parse_args()


def main():
    # Create the graph object
    g = stag.neo4j.Neo4jGraph("bolt://localhost:7687", "neo4j", "password")

    # Set the parameters of the local cluster algorithm
    args = parse_args()
    page_title = args.pageTitle
    cluster_volume = args.clusterVolume

    # Run the clustering algorithm
    print(f"Finding cluster...")
    cluster = stag.cluster.local_cluster(g,
                                         get_wikipedia_page_id(g, page_title),
                                         cluster_volume)

    # Display the found cluster
    print(f"Found cluster:")
    print(cluster)
    for id in cluster:
        print(f"  - {get_wikipedia_title(g, id)}")


if __name__ == "__main__":
    main()
