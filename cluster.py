import heuristics


def cluster(transactions, heuristic, threshold=None):
    """
    transactions is an array 
    heuristics is a function. See heuristics.py for all functions
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
