import heuristics
import matplotlib.pyplot as plt
import numpy as np


def cluster(transactions, heuristic, threshold=None):
    """
    transactions is an array 
    heuristics is a function. See heuristics.py for all functions

    returns a list of clusters
    Each cluster is a list of addresses
    """

    clusters = []

    if heuristic == heuristics.shadow:
        # Shadow heuristic relies on meta-data across multiple transactions
        address_to_merchant_count = heuristics.__get_shadow_data(transactions)
        for t in transactions:
            clusters.append(heuristics.shadow(
                t, address_to_merchant_count, threshold))
    else:
        # All other heursitics cluster based on current transaction only
        seen_addresses = set()
        for t in transactions:
            new_cluster = set(pair.address for pair in heuristic(t))
            single_addresses = set(pair.address for pair in t.inputs + t.outputs).difference(new_cluster)

            # Clustered addresses are added to the list of clusters
            # Each address is marked as "seen"
            if new_cluster:
                clusters.append(new_cluster)
                for address in new_cluster:
                    seen_addresses.add(address)

            # All unseen, unclustered addresses enter their own cluster
            for address in single_addresses:
                if address not in seen_addresses:
                    clusters.append({address})
                    seen_addresses.add(address)
        
        # Overlap between clusters likely exists - need to merge
        to_merge = True
        while to_merge:
            to_merge = False
            new_clusters = []
            while clusters:
                common, rest = clusters[0], clusters[1:]
                clusters = []
                for x in rest:
                    if x.isdisjoint(common):
                        clusters.append(x)
                    else:
                        to_merge = True
                        common |= x
                new_clusters.append(common)
            clusters = new_clusters
            
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
