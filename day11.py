import itertools
import sys
from functools import cache

import utils

test_mode = len(sys.argv) > 1
if test_mode:
    suffix = sys.argv[2] if len(sys.argv) > 2 else ""
    input_file = f"day11_test_input{suffix}.txt"
else:
    input_file = f"day11_input.txt"

data = utils.input_as_lines(input_file)

graph = {}

for line in data:
    splits = line.split()
    in_ = splits[0].removesuffix(":")
    graph[in_] = splits[1:]


@cache
def find_n_paths(node):
    if node == "out":
        return 1
    else:
        return sum([find_n_paths(n) for n in graph[node]])


if not test_mode or suffix == "":
    part1 = find_n_paths("you")
    print(f"Part 1: {part1}")

paths = []


@cache
def find_n_paths_to_target(node, target, avoid_list_str):
    # print(node, target, avoid_list_str)
    if node == target:
        return 1
    else:
        return sum(
            [
                find_n_paths_to_target(n, target, avoid_list_str)
                for n in graph[node]
                if n not in avoid_list_str
            ]
        )


if not test_mode or suffix == "2":
    routes = [("svr", "fft", "dac", "out"), ("svr", "dac", "fft", "out")]
    part2 = 0
    for route in routes:
        n_paths = 1
        for n1, n2 in itertools.pairwise(route):
            n_sub_paths = find_n_paths_to_target(
                n1, n2, ",".join([n for n in route if n not in (n1, n2)])
            )
            n_paths = n_paths * n_sub_paths

        # print(n_paths)
        part2 += n_paths

    print(f"Part2: {part2}")
