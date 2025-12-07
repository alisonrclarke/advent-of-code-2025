import sys
from functools import cache

import utils

test_mode = len(sys.argv) > 1
if test_mode:
    suffix = sys.argv[2] if len(sys.argv) > 2 else ""
    input_file = f"day07_test_input{suffix}.txt"
else:
    input_file = f"day07_input.txt"

data = utils.input_as_lines(input_file)


# Part 1

positions = {data[0].index("S")}
n_splits = 0

for i, line in enumerate(data[1:]):
    next_positions = set()

    for p in positions:
        if line[p] == "^":
            n_splits += 1
            next_positions.add(p - 1)
            next_positions.add(p + 1)
        else:
            next_positions.add(p)

    positions = next_positions

print(f"Part 1: {n_splits}")


# Part 2


@cache
def get_n_paths(row, col):
    if row == len(data) - 1:
        return 1
    else:
        if data[row][col] == "^":
            return get_n_paths(row + 1, col - 1) + get_n_paths(row + 1, col + 1)
        else:
            return get_n_paths(row + 1, col)


start_pos = data[0].index("S")
n_paths = get_n_paths(1, start_pos)

print(f"Part 2: {n_paths}")
