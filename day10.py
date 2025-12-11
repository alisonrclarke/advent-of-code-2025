import itertools
import re
import sys
from functools import reduce
from operator import ior

import utils

test_mode = len(sys.argv) > 1
if test_mode:
    suffix = sys.argv[2] if len(sys.argv) > 2 else ""
    input_file = f"day10_test_input{suffix}.txt"
else:
    input_file = f"day10_input.txt"

data = utils.input_as_lines(input_file)


def find_target(target: int, buttons: list[int]) -> int:
    q = [0]
    visited = {0: None}

    while q:
        val = q.pop(0)
        if val == target:
            # Trace back to start in visited
            parent = visited[val]
            n_steps = 0
            while parent is not None:
                n_steps += 1
                parent = visited[parent]
            return n_steps

        else:
            for b in buttons:
                next_val = val ^ b
                if next_val not in visited:
                    visited[next_val] = val
                    q.append(next_val)

    breakpoint()


part1 = 0
for line in data:
    m = re.match(r"\[([\.#]+)\] (.+) \{([\d,]+)\}", line)

    target = int(m.group(1).replace(".", "0").replace("#", "1"), 2)
    n_lights = len(m.group(1))

    buttons = []
    for b in m.group(2).split():
        b = eval(b)
        if isinstance(b, int):
            b = (b,)

        b_val = 0
        for v in b:
            v_bin = 2 ** (n_lights - v - 1)
            b_val = b_val | v_bin

        buttons.append(b_val)

    joltages = m.group(3)

    part1 += find_target(target, buttons)

print(f"Part 1: {part1}")
