

def optimal_change(transaction, args=None):
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


def multi_input(transaction, args=None):
    """
    Assume that all inputs are in a cluster together
    """
    inputs = transaction.inputs
    return inputs.copy()


def multi_input_optimal_change(transaction, args=None):
    """
    If there is an output that is uniquely less than all inputs
    Then that output can be clustered with the inputs
    Else cluster by inputs only
    """
    opt_change = optimal_change(transaction)
    if opt_change == []:
        return multi_input(transaction)
    return opt_change


# need to test
def __get_shadow_data(transactions):
    address_to_merchant_count = {}

    for t in transactions:
        for output in t.outputs:
            address = output.address
            if address in address_to_merchant_count:
                address_to_merchant_count[address] += 1
            else:
                address_to_merchant_count[address] = 1

    return address_to_merchant_count

# need to test


def shadow(transaction, args):
    address_to_merchant_count, threshold = args
    """
    threshold is asking "how many times does it appear on merchant count for us to assume merchant?"
    """
    outputs = transaction.outputs
    inputs = transaction.inputs

    # determine what could possibly be a change output
    change = set(transaction.outputs.copy())
    for output_i in outputs:
        if address_to_merchant_count[output_i.address] >= threshold:
            change.remove(output_i)

    # now we have the possible change output. Cluster them with the inputs
    return inputs + list(change)
