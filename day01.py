import sys

import utils

test_mode = len(sys.argv) > 1
if test_mode:
    suffix = sys.argv[2] if len(sys.argv) > 2 else ""
    input_file = f"day01_test_input{suffix}.txt"
else:
    input_file = f"day01_input.txt"

data = utils.input_as_lines(input_file)

DIRECTIONS = {"L": -1, "R": 1}

# Part 1
pos = 50
part1 = 0

for line in data:
    direction = line[0]
    n = int(line[1:])

    pos += DIRECTIONS[direction] * n
    pos = pos % 100

    if pos == 0:
        part1 += 1

print(f"Part 1: {part1}")


# Part 2
pos = 50
part2 = 0

for line in data:
    direction = line[0]
    n = int(line[1:])
    step = DIRECTIONS[direction]

    # Use double loop rather than trying to calculate with n // 100, to avoid off-by-one errors
    for i in range(n):
        pos += step

        if pos >= 100:
            pos = pos - 100
        elif pos < 0:
            pos = pos + 100

        if pos == 0:
            part2 += 1

print(f"Part 2: {part2}")
