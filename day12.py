import operator
import re
import sys
from functools import reduce

import utils

test_mode = len(sys.argv) > 1
if test_mode:
    suffix = sys.argv[2] if len(sys.argv) > 2 else ""
    input_file = f"day12_test_input{suffix}.txt"
else:
    input_file = f"day12_input.txt"

data = utils.input_as_lines(input_file)

shapes = []
current_shape = []
regions = []

for line in data:
    if re.match(r"^(\d+):$", line):
        current_shape = []
    elif m := re.match(r"^(\d+)x(\d+): ([\d ]+)$", line):
        region_size = (int(m.group(1)), int(m.group(2)))
        region_shapes = [int(i) for i in m.group(3).split()]
        regions.append((region_size, region_shapes))
    elif line == "":
        if current_shape:
            shapes.append(current_shape)
    else:
        current_shape.append(line)

max_shape_size = max(
    max(len(s) for s in shapes),
    max(len(s[0]) for s in shapes),
)

shape_areas = [sum([row.count("#") for row in s]) for s in shapes]

ok = 0
failed = 0
unknown = 0

# First pass - just check size
for region_size, region_shapes in regions:
    # If no overlaps, can fit
    n_x = region_size[0] // max_shape_size
    n_y = region_size[1] // max_shape_size
    max_non_overlapping = n_x * n_y

    # min area needed for shapes
    min_area_needed = sum([n * shape_areas[i] for i, n in enumerate(region_shapes)])

    total_shapes_to_fit = sum(region_shapes)

    if min_area_needed > region_size[0] * region_size[1]:
        failed += 1
    elif total_shapes_to_fit <= max_non_overlapping:
        ok += 1
    else:
        unknown += 1

print(f"Part 1: {ok} OK, {failed} not OK, {unknown} unknown")
