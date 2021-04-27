import os
import pickle


def optimal_change(transaction, args=None):
	"""
    If there is an output that is uniquely less than all inputs,
    then that output can be clustered with the inputs
    """
	inputs = transaction.inputs
	outputs = transaction.outputs
	
	if not inputs:
		return []
	
	min_input = min(inputs).value
	less_outputs = [o for o in outputs if o.value < min_input]
	
	if len(less_outputs) == 1:
		return inputs.copy() + less_outputs
	else:
		return []


def multi_input(transaction, args=None):
    """
    Assume that all inputs are in a cluster together.
    """
    inputs = transaction.inputs
    return inputs.copy()


def multi_input_optimal_change(transaction, args=None):
    """
    If there is an output that is uniquely less than all inputs,
    then that output can be clustered with the inputs.
    Else, cluster by inputs only
    """
    opt_change = optimal_change(transaction)
    if opt_change == []:
        return multi_input(transaction)
    return opt_change


def __get_shadow_data(transactions):
	"""
	Get number of times each address appears as an output
	Addresses with high output counts are likely merchants
	"""
	
	# Load previously created file if available
	pickle_file = 'dataset_3_shadow_metadata.pkl'
	if os.path.exists(pickle_file):
		with open(pickle_file, 'rb') as f:
			return pickle.load(f)
			
	# Create dictionary of counts
	address_to_merchant_count = {}
	for t in transactions:
		for output in t.outputs:
			address = output.address
			if address in address_to_merchant_count:
				address_to_merchant_count[address] += 1
			else:
				address_to_merchant_count[address] = 1
	with open(pickle_file, 'wb') as f:
		pickle.dump(address_to_merchant_count, f)

	return address_to_merchant_count

	
def shadow(transaction, args):
	"""
	If an output exceeds the threshold argument, then we assume that it belongs to a merchant
	Note that this calculation is done in pre-processing to produce a list of merchants
	Then, any remaining non-merchant output must be for change and can be clustered with the input
	"""
	merchants = args
	outputs = transaction.outputs
	inputs = transaction.inputs

	non_merchant_outputs = [o for o in outputs if o.address not in merchants]
	if len(outputs) > 1 and len(non_merchant_outputs) == 1:
		return inputs.copy() + non_merchant_outputs
	else:
		return inputs.copy()
