import re
import sys

import utils

test_mode = len(sys.argv) > 1
if test_mode:
    suffix = sys.argv[2] if len(sys.argv) > 2 else ""
    input_file = f"day06_test_input{suffix}.txt"
else:
    input_file = f"day06_input.txt"

data = utils.input_as_lines(input_file)

operators = re.split(r"\s+", data[-1].strip())
totals = [int(n) for n in re.split(r"\s+", data[0].strip())]

for line in data[1:-1]:
    for i, n_str in enumerate(re.split(r"\s+", line.strip())):
        n = int(n_str)
        op = operators[i]
        if op == "+":
            totals[i] += int(n)
        elif op == "*":
            totals[i] *= int(n)

total = sum(totals)

print(f"Part 1: {total}")

# Part 2
# Iterate column wise
operators = [
    (m.group(1), len(m.group(0)) - 1) for m in re.finditer(r"([*+])\s*", data[-1])
]

# Update the length of the last operator in case trailing whitespace is trimmed
max_len = max(len(l) for l in data)
last_space = max_len - len(data[-1].rstrip())
operators[-1] = (operators[-1][0], last_space + 1)

totals = []

start_col = 0
grand_total = 0

for i, (op, cols) in enumerate(operators):
    total = None
    for j in range(start_col, start_col + cols):
        n_str = ""
        for line in data[:-1]:
            if j < len(line) and line[j]:
                n_str += line[j]

        n = int(n_str.strip())

        if total is None:
            total = n
        else:
            if op == "+":
                total += int(n)
            elif op == "*":
                total *= int(n)

    grand_total += total
    start_col += cols + 1

print(f"Part 2: {grand_total}")
