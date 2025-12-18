import itertools
import re
import sys
from collections import defaultdict
from functools import reduce, cache
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


# part 2: Re-parse data to get joltages
# Algorithm based on https://www.reddit.com/r/adventofcode/comments/1pk87hl/2025_day_10_part_2_bifurcate_your_way_to_victory/
# and https://aoc.winslowjosiah.com/solutions/2025/day/10/
# Use patterns of odd/even numbers and recurse


def get_valid_patterns(buttons: list[set[int]]) -> dict[list[set[int]], list[set[int]]]:
    patterns = defaultdict(list)

    # Get all possible combinations of button presses (1 press per button)
    # Include 0 presses here too, so we have a no-op option
    for n_presses in range(len(buttons) + 1):
        for presses in itertools.combinations(buttons, n_presses):
            pattern = set()
            for button in presses:
                pattern ^= button

            patterns[frozenset(pattern)].append(presses)

    return patterns


part2 = 0

for line in data:
    m = re.match(r"\[([\.#]+)\] (.+) \{([\d,]+)\}", line)

    joltages = tuple(int(i) for i in m.group(3).split(","))

    buttons = []
    # Use sets for buttons - can use XOR on sets to toggle values
    for bs in m.group(2).split():
        b = set(int(i) for i in bs.lstrip("(").rstrip(")").split(","))
        buttons.append(b)

    valid_patterns = get_valid_patterns(buttons)

    @cache
    def get_min_presses(target_joltage: tuple[int]) -> int | None:
        # Calculate min number of presses to get to the target
        if all(j == 0 for j in target_joltage):
            return 0

        # Work out which lights need an odd number of presses - how do we get to that?
        odd_lights = frozenset(i for i, j in enumerate(target_joltage) if j % 2 == 1)

        result = None

        for presses in valid_patterns[odd_lights]:
            # For each button sequence that can get us to the odd_lights pattern, press it and reduce the needed joltage
            next_target = list(target_joltage)
            for button in presses:
                for joltage_index in button:
                    next_target[joltage_index] -= 1

            # If we got to a negative target, continue as this sequence is no good
            if any(j < 0 for j in next_target):
                continue

            # Should now have even values in next_target, so we can divide and conquer...
            half_target = tuple(t // 2 for t in next_target)
            half_min_presses = get_min_presses(half_target)
            if half_min_presses is None:
                continue

            # If we get to half target, then repeat, we reach next_target, then add on the number of presses we've just done
            n_presses = (half_min_presses * 2) + len(presses)

            result = min(n_presses, result) if result is not None else n_presses

        return result

    min_presses = get_min_presses(joltages)
    if min_presses is not None:
        part2 += min_presses

print(f"Part 2: {part2}")
