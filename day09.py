import itertools
import sys

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

for t1, t2 in itertools.combinations(red_tiles, 2):
    area = (abs(t1[0] - t2[0]) + 1) * (abs(t1[1] - t2[1]) + 1)
    biggest_rect = max(area, biggest_rect)

print(f"Part 1: {biggest_rect}")
