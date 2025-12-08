import itertools
import math
import sys
from collections import OrderedDict

import utils

test_mode = len(sys.argv) > 1
if test_mode:
    suffix = sys.argv[2] if len(sys.argv) > 2 else ""
    input_file = f"day08_test_input{suffix}.txt"
else:
    input_file = f"day08_input.txt"

data = utils.input_as_lines(input_file)

positions = []

for line in data:
    splits = line.split(",")
    positions.append(tuple(int(s) for s in splits))

# Get distances between each set of points
distances = {}

for p1, p2 in itertools.combinations(positions, 2):
    distance = math.sqrt(
        (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2
    )
    distances[distance] = (p1, p2)

# Now set up groups then combine
groups = [[p] for p in positions]

n_to_check = 10 if test_mode else 1000

for i, k in enumerate(sorted(distances)):
    p1, p2 = distances[k]
    group1 = next((g for g in groups if p1 in g), None)
    group2 = next((g for g in groups if p2 in g), None)

    if group1 != group2:
        # Combine groups
        group1.extend(group2)
        groups.pop(groups.index(group2))

    if i == n_to_check - 1:
        # End of part 1
        groups = sorted(groups, key=lambda g: len(g), reverse=True)
        part1 = len(groups[0]) * len(groups[1]) * len(groups[2])
        print(f"Part 1: {part1}")
    elif len(groups) == 1:
        # End of part 2
        part2 = p1[0] * p2[0]
        print(f"Part 2: {part2}")
        break
