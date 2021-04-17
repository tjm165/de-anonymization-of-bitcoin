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

    # create initial clusters through the heuristic
    clusters = []

    if heuristic == heuristics.shadow:
        address_to_merchant_count = heuristics.__get_shadow_data(transactions)
        for t in transactions:
            clusters.append(heuristics.shadow(
                t, address_to_merchant_count, threshold))
    else:
        for t in transactions:
            clusters.append(heuristic(t))

    # join clusters
    address_to_cluster = {}
    new_cluster_id = 0
    for cluster in clusters:
        new_cluster_id += 1  # we might use this id or we might pass up on it
        found_join = False

        i = 0
        while not found_join and i < len(cluster):
            address = cluster[i].address
            if address in address_to_cluster.keys():
                found_join = True
                cluster_id = address_to_cluster[address]
            i += 1

        if not found_join:
            new_cluster_id += 1
            cluster_id = new_cluster_id

        for obj in cluster:
            address = obj.address
            address_to_cluster[address] = cluster_id

    return __address_to_cluster_dict_to_lists(address_to_cluster)


def __address_to_cluster_dict_to_lists(address_to_cluster):
    """
    address_to_cluster should be {address1: cluster_id, address2: cluster_id....}

    this will be converted to [[addresses in cluster_id1], [addresses in cluster_id2] ..... ]
    """

    cluster_to_address = {}

    for key in address_to_cluster.keys():
        cluster_id = address_to_cluster[key]
        if cluster_id in cluster_to_address:
            cluster_to_address[cluster_id].append(key)
        else:
            cluster_to_address[cluster_id] = [key]

    return list(cluster_to_address.values())


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
