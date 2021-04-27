import heuristics
import matplotlib.pyplot as plt
import numpy as np
import time


class Cluster:
    def __init__(self, addresses):
        self.addresses = addresses


def cluster(transactions, heuristic):
	"""
	transactions: a list of formatted transactions
	heuristics: a callable function. See heuristics.py for all functions

	returns a list of clusters, each cluster is a list of addresses
	"""

	clusters = []

    # Prepare arguments for shadow heuristic
	cluster_map = {}
	args = None
	if heuristic == heuristics.shadow:
		threshold = 20
		address_to_merchant_count = heuristics.__get_shadow_data(transactions)
		
		# Reduce merchant counts to set of merchants only
		merchants = {address for address, count in address_to_merchant_count.items() if count >= threshold}
		args = merchants
	
	# Handle each transaction in list sequentially
	start_time = time.time()
	next_percentage = 0
	
	try:
		for i, t in enumerate(transactions):
			# Print clustering progress
			percentage = int((i / len(transactions)) * 100)
			if percentage == next_percentage:
				next_percentage += 5
				minutes_elapsed = (time.time() - start_time) / 60
				print("Percent Complete:", percentage,
					  "\t\tMinutes Elapsed:", minutes_elapsed)

			# Get cluster from heuristic applied to current transaction
			clustered_addresses = set(pair.address for pair in heuristic(t, args))
			single_addresses = set(
				pair.address for pair in t.inputs + t.outputs).difference(clustered_addresses)

			# New cluster may overlap existing ones, join together
			joined_cluster = clustered_addresses
			for address in clustered_addresses:
				if address in cluster_map:
					joined_cluster = joined_cluster.union(cluster_map[address].addresses)

			# Map all addresses in joined cluster to new cluster
			new_cluster = Cluster(joined_cluster)
			for address in joined_cluster:
				cluster_map[address] = new_cluster

			# Map all unseen, single addresses to their own new cluster
			for address in single_addresses:
				cluster_map[address] = Cluster({address})
				
	except KeyboardInterrupt:
		# Allow early stopping
		pass

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
