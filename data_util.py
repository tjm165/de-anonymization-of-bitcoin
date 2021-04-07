
import os
import sys
import pickle
from collections import defaultdict


class Pair:

    def __init__(self, address, value):
        self.address = address
        self.value = value


class Input(Pair):

    def __init__(self, address, value):
        super().__init__(address, value)


class Output(Pair):

   def __init__(self, address, value):
        super().__init__(address, value)


class Transaction:

    def __init__(self, inputs, outputs):
        self.inputs = inputs
        self.outputs = outputs


def load_data(file_name):
    # Read data from file into Transaction objects
    with open(file_name, 'rb') as f:
        raw_data = pickle.load(f)

    data = []
    for transaction in raw_data:
        inputs = [Input(i[0], i[1]) for i in transaction[0]]
        outputs = [Output(o[0], o[1]) for o in transaction[1]]
        data.append(Transaction(inputs, outputs))

    return data


def parse_data(file_root):
    # Combine input and output data files from Kaggle dataset
    transaction_in, transaction_out = defaultdict(list), defaultdict(list)
    transaction_times = {}

    # Read from input file
    with open(file_root + '/txin.txt') as f:
        for line in f:
            txID, addrID, value = map(int, line.split())
            transaction_in[txID].append((addrID, value))

    # Read from output file
    with open(file_root + '/txout.txt') as f:
        for line in f:
            txID, addrID, value = map(int, line.split())
            transaction_out[txID].append((addrID, value))

    # Read from tx file
    with open(file_root + '/tx.txt') as f:
        for line in f:
            split_line = line.split()
            txID, time = int(split_line[0]), int(split_line[-1])
            transaction_times[txID] = time

    # Sort transactions by time (ascending)
    transaction_times = dict(sorted(transaction_times.items(), key=lambda v: v[1]))

    # Produce list of all transaction data
    data = [(transaction_in[txID], transaction_out[txID]) for txID in transaction_times]

    # Write data to file
    file_name = file_root.split(os.sep)[-1]
    with open(f'{file_name}.pkl', 'wb') as f:
        pickle.dump(data, f)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'USAGE: python3 {sys.argv[0]} <data directory>')
        sys.exit(0)

    file_root = sys.argv[1]
    if file_root[-1] in ['\\', '/']:
        file_root = file_root[:-1]

    parse_data(file_root)
