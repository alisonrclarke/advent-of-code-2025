import sys

import utils

test_mode = len(sys.argv) > 1
if test_mode:
    suffix = sys.argv[2] if len(sys.argv) > 2 else ""
    input_file = f"day05_test_input{suffix}.txt"
else:
    input_file = f"day05_input.txt"

data = utils.input_as_lines(input_file)


# list of tuples of (start, end)
ranges = []

id_start = 0

for i, line in enumerate(data):
    if line == "":
        id_start = i + 1
        break

    left, right = line.split("-")
    start = int(left)
    end = int(right)

    ranges.append((start, end))


# Remove overlaps before continuing
ranges = sorted(ranges, key=lambda x: x[0])

while True:
    next_ranges = []
    for i, (start, end) in enumerate(ranges):
        if i > 0:
            prev_start, prev_end = next_ranges[-1]
            if start <= prev_end and end >= prev_start:
                # overlap with previous so update previous item
                next_ranges[-1] = (
                    min(start, next_ranges[-1][0]),
                    max(end, next_ranges[-1][1]),
                )
            else:
                next_ranges.append((start, end))
        else:
            next_ranges.append((start, end))

    if len(next_ranges) == len(ranges):
        break

    ranges = next_ranges

# Part 1: Now we have ranges, go through the values and count which are in range
total = 0
for line in data[id_start:]:
    n = int(line)

    for s, e in ranges:
        if n >= s and n <= e:
            total += 1
            break

print(f"Part 1: {total}")


# Part 2: sum up the sizes of the ranges
total = 0

for start, end in ranges:
    total += (end - start) + 1

print(f"Part 2: {total}")
