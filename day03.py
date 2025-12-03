import sys

import utils

test_mode = len(sys.argv) > 1
if test_mode:
    suffix = sys.argv[2] if len(sys.argv) > 2 else ""
    input_file = f"day03_test_input{suffix}.txt"
else:
    input_file = f"day03_input.txt"

data = utils.input_as_lines(input_file)


# Part 1
total = 0

for line in data:
    battery = [int(c) for c in line]
    d1 = max(battery[:-1])
    d1_pos = battery.index(d1)
    d2 = max(battery[d1_pos + 1 :])
    joltage = d1 * 10 + d2
    total += joltage

print(f"Part 1: {total}")

# Part 2
total = 0

for line in data:
    battery = [int(c) for c in line]
    joltage = 0
    start_pos = 0

    for i in range(12):
        if i < 11:
            d = max(battery[: i - 11])
        else:
            d = max(battery)

        start_pos = battery.index(d) + 1
        battery = battery[start_pos:]

        joltage += 10 ** (11 - i) * d

    total += joltage

print(f"Part 2: {total}")
