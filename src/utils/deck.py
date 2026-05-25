import random


def create_pairs(pair_count):
    values = list(range(1, pair_count + 1)) * 2
    random.shuffle(values)
    return values