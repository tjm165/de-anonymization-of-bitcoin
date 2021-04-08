

def optimal_change(transaction):
    """
    If there is an output that is uniquely less than all inputs
    Then that output can be clustered with the inputs
    """
    # sort the transactions
    inputs = transaction.inputs
    cluster = inputs.copy()
    outputs = transaction.outputs

    i = 0
    found_uniquely_less = False
    # stop once we found a uniquely less value
    while (i < len(outputs) and not found_uniquely_less):
        output_i = outputs[i]
        found_uniquely_less = all(output_i < input_i for input_i in inputs)
        if found_uniquely_less:
            cluster.append(output_i)
            return cluster

        i += 1
    return []


def multi_input(transaction):
    """
    Assume that all inputs are in a cluster together
    """
    inputs = transaction.inputs
    return inputs.copy()


def multi_input_optimal_change(transaction):
    """
    If there is an output that is uniquely less than all inputs
    Then that output can be clustered with the inputs
    Else cluster by inputs only
    """
    opt_change = optimal_change(transaction)
    if opt_change == []:
        return multi_input(transaction)
    return opt_change
