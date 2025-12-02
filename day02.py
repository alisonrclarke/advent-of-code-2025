import sys

import utils

test_mode = len(sys.argv) > 1
if test_mode:
    suffix = sys.argv[2] if len(sys.argv) > 2 else ""
    input_file = f"day02_test_input{suffix}.txt"
else:
    input_file = f"day02_input.txt"

data = utils.input_as_string(input_file)

# Part 1
total = 0

for range_str in data.split(","):
    start, end = range_str.split("-")
    for n in range(int(start), int(end) + 1):
        id_str = str(n)
        str_len = len(id_str)
        if str_len % 2 == 0:
            if id_str[: str_len // 2] == id_str[str_len // 2 :]:
                total += n

print(f"Part 1: {total}")

# Part 2 - a bit slow but it works
total = 0

for range_str in data.split(","):
    start, end = range_str.split("-")
    for n in range(int(start), int(end) + 1):
        id_str = str(n)
        str_len = len(id_str)
        for i in range(1, str_len):
            if str_len % i == 0:
                chunks = [id_str[j : j + i] for j in range(0, str_len, i)]
                if len(set(chunks)) == 1:
                    total += n
                    break

print(f"Part 2: {total}")
