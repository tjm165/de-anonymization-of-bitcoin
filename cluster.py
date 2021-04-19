import heuristics
import matplotlib.pyplot as plt
import numpy as np


class Cluster:
    def __init__(self, addresses):
        self.addresses = addresses


def cluster(transactions, heuristic, threshold=None):
    """
    transactions is an array
    heuristics is a function. See heuristics.py for all functions

    returns a list of clusters
    Each cluster is a list of addresses
    """

    clusters = []

    # All other heursitics cluster based on current transaction only
    # Map previously seen addresses to their cluster object
    cluster_map = {}
    args = None
    if heuristic == heuristics.shadow:
        threshold = 20
        args = (heuristics.__get_shadow_data(transactions), threshold)

    for t in transactions:
        clustered_addresses = set(pair.address for pair in heuristic(t, args))
        single_addresses = set(
            pair.address for pair in t.inputs + t.outputs).difference(clustered_addresses)

        # New cluster may overlap existing ones, join together
        joined_cluster = clustered_addresses
        for address in clustered_addresses:
            if address in cluster_map:
                joined_cluster = joined_cluster.union(
                    cluster_map[address].addresses)

        # Map all addresses in joined cluster to new cluster
        new_cluster = Cluster(joined_cluster)
        for address in joined_cluster:
            cluster_map[address] = new_cluster

        # Map all unseeen, single addresses to their own new cluster
        for address in single_addresses:
            cluster_map[address] = Cluster({address})

    # Extract clusters from cluster map
    clusters = list(c.addresses for c in set(cluster_map.values()))

    return clusters


def visualize_clusters(clusters):
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    data = __get_clusters_data(clusters)
    ax.bar(data['cluster_ids'], data['cluster_sizes'])
    plt.show()


def __get_clusters_data(clusters):
    """
    This data is intended to be used for plotting and for comparison metrics
    """

    ids = range(len(clusters))
    sizes = []

    for cluster in clusters:
        sizes.append(len(cluster))

    return {'cluster_ids': ids, 'cluster_sizes': sizes}
