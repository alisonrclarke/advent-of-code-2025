import itertools
import math
import sys
from functools import cache

import utils

test_mode = len(sys.argv) > 1
if test_mode:
    suffix = sys.argv[2] if len(sys.argv) > 2 else ""
    input_file = f"day09_test_input{suffix}.txt"
else:
    input_file = f"day09_input.txt"

data = utils.input_as_lines(input_file)

red_tiles = []

for line in data:
    splits = line.split(",")
    x = int(splits[0])
    y = int(splits[1])
    red_tiles.append((x, y))

biggest_rect = 0
all_rectangles = []


for t1, t2 in itertools.combinations(red_tiles, 2):
    area = (abs(t1[0] - t2[0]) + 1) * (abs(t1[1] - t2[1]) + 1)
    all_rectangles.append((area, (t1, t2)))
    biggest_rect = max(area, biggest_rect)

print(f"Part 1: {biggest_rect}")

# Part 2

# # Visualise data
# import matplotlib.pyplot as plt
#
# from matplotlib.patches import Polygon
# import numpy as np
# xs = np.array([t[0] for t in red_tiles])
# ys = np.array([t[1] for t in red_tiles])
#
# p = Polygon(red_tiles, facecolor="orange", edgecolor="purple")
# fig, ax = plt.subplots()
#
# ax.add_patch(p)
# ax.set_xlim([0, 100000])
# ax.set_ylim([0,100000])
# plt.show()

# Add edges so we can use odd-even tactic to check if tile is inside polygon

edge_tiles = set()

for i, t1 in enumerate(red_tiles):
    j = i + 1
    if j == len(red_tiles):
        j = 0

    t2 = red_tiles[j]

    if t1[0] == t2[0]:
        start = min(t1[1], t2[1])
        end = max(t1[1], t2[1])
        for k in range(start + 1, end):
            edge_tiles.add((t1[0], k))
    elif t1[1] == t2[1]:
        start = min(t1[0], t2[0])
        end = max(t1[0], t2[0])
        for k in range(start + 1, end):
            edge_tiles.add((k, t1[1]))


coloured_tiles = edge_tiles.union(red_tiles)

# Get max/min bounds
min_x = min(t[0] for t in red_tiles) - 1
min_y = min(t[1] for t in red_tiles) - 1
max_x = max(t[0] for t in red_tiles) + 1
max_y = max(t[1] for t in red_tiles) + 1


@cache
def is_in_polygon(i, j):
    if (i, j) in coloured_tiles:
        return True
    else:
        # Work from left hand side and count times we cross a vertical edge to get here
        inside = False
        for x in range(min_x, i):
            if (x, j) in coloured_tiles and (x - 1, j) not in coloured_tiles:
                inside = not inside

        return inside


# Look for rectangles again, starting with the biggest found last time
all_rectangles.sort(key=lambda t: t[0])

biggest_rect = 0

for area, (t1, t2) in reversed(all_rectangles):
    ok = True

    has_inner_coloured_tiles = (
        next(
            (
                t
                for t in coloured_tiles
                if min(t1[0], t2[0]) < t[0] < max(t1[0], t2[0])
                and min(t1[1], t2[1]) < t[1] < max(t1[1], t2[1])
            ),
            None,
        )
        is not None
    )
    if has_inner_coloured_tiles:
        continue

    # Now points just inside the rectangle
    # Credit to https://aoc.winslowjosiah.com/solutions/2025/day/9/ for this idea
    min_x1 = min(t1[0], t2[0])
    min_y1 = min(t1[1], t2[1])
    max_x1 = max(t1[0], t2[0])
    max_y1 = max(t1[1], t2[1])

    inner_points = [
        (min_x1 + 1, min_y1 + 1),
        (min_x1 + 1, max_y1 - 1),
        (max_x1 - 1, min_y1 + 1),
        (max_x1 - 1, max_y1 - 1),
    ]

    ok = True
    for i, j in inner_points:
        if not is_in_polygon(i, j):
            ok = False
            break

    if ok:
        biggest_rect = area
        break

print(f"Part 2: {biggest_rect}")
