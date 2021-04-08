def cluster(transactions, heuristic):
    """
    transactions is an array 
    heuristics is a function. See heuristics.py for all functions
    """

    clusters = []
    for t in transactions:
        clusters.append(heuristic(t))

    return clusters
