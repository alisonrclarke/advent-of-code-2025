import copy
import sys

import utils

test_mode = len(sys.argv) > 1
if test_mode:
    suffix = sys.argv[2] if len(sys.argv) > 2 else ""
    input_file = f"day04_test_input{suffix}.txt"
else:
    input_file = f"day04_input.txt"

data = utils.input_as_lines(input_file)

# Pad the grid to avoid having to do boundary checks
grid = [
    " " * (len(data[0]) + 2),
    *[" " + d + " " for d in data],
    " " * (len(data[0]) + 2),
]

steps = [
    -1 - 1j,
    -1j,
    1 - 1j,
    -1,
    1,
    -1 + 1j,
    1j,
    1 + 1j,
]


def get_val(grid, pos: complex):
    return grid[int(pos.imag)][int(pos.real)]


# Part 1

total = 0

for y in range(1, len(grid) - 1):
    for x in range(1, len(grid[0]) - 1):
        pos = complex(x, y)

        if get_val(grid, pos) == "@":
            can_access = True
            n_adjacent_rolls = 0
            for step in steps:
                step_pos = pos + step

                if get_val(grid, step_pos) == "@":
                    n_adjacent_rolls += 1
                    if n_adjacent_rolls >= 4:
                        can_access = False
                        break

            if can_access:
                total += 1

print(f"Part 1: {total}")


# Part 2
grid = [
    " " * (len(data[0]) + 2),
    *[" " + d + " " for d in data],
    " " * (len(data[0]) + 2),
]
total = 0
prev_total = 0


while True:
    next_grid = copy.deepcopy(grid)

    for y in range(1, len(grid) - 1):
        for x in range(1, len(grid[0]) - 1):
            pos = complex(x, y)

            if get_val(grid, pos) == "@":
                can_access = True
                n_adjacent_rolls = 0
                for step in steps:
                    step_pos = pos + step

                    if get_val(grid, step_pos) == "@":
                        n_adjacent_rolls += 1
                        if n_adjacent_rolls >= 4:
                            can_access = False
                            break

                if can_access:
                    total += 1
                    new_line = next_grid[y]
                    new_line = new_line[:x] + "." + new_line[x + 1 :]
                    next_grid[y] = new_line
                    assert next_grid[y] != grid[y]

    if total == prev_total:
        break

    grid = next_grid
    prev_total = total

print(f"Part 2: {total}")
