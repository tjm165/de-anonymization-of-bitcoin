import heuristics
import matplotlib.pyplot as plt


def cluster(transactions, heuristic, threshold=None):
    """
    transactions is an array 
    heuristics is a function. See heuristics.py for all functions

    returns a list of clusters
    Each cluster is a list of addresses
    """

    clusters = []

    if heuristic == heuristics.shadow:
        address_to_merchant_count = heuristics.__get_shadow_data(transactions)
        for t in transactions:
            clusters.append(heuristics.shadow(
                t, address_to_merchant_count, threshold))
    else:
        for t in transactions:
            clusters.append(heuristic(t))

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
