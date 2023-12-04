# (1) Read line by triples
# Walk current line charwise. If faced a digit, make number: read until next char is not digit
# Check the number is adj: if any of its chars is adj: left, right, bottom, up, lup, rup, ldown, rdown
# For that, keep number -> list of it's char positions.
# If any of nubmer's char adj -> add number to res
# Continue with char next to the number's last char.
# Walk until the EoL
# (2) Essentially similar approach. but check numbers above, below and around
#
# Note: There are negative numbers. But all 5 of them are not "parts", so I removed logic dealing with negatives

def collect_line_numbers(line: str) -> list((int, int, int)):
    res, poses, digits = [], [], []
    for i in range(len(line)):
        if line[i].isdigit():
            digits.append(line[i])
            poses.append(i)
        elif digits:
            n = int(''.join(digits))
            res.append((n, poses[0], poses[-1]))
            digits, poses = [], []
    # Don't forget last number in line
    if digits:
        n = int(''.join(digits))
        res.append((n, poses[0], poses[-1]))
    return res

def collect_adj_numbers(prev_line, current_line, next_line):
    summa = 0
    for n, start, end in collect_line_numbers(current_line):
        if any([has_adj_chars(i, [prev_line, next_line]) for i in range(start, end + 1)]) \
                or is_char(start - 1, current_line) \
                or is_char(end + 1, current_line):
            summa += n
    return summa

def has_adj_chars(i: int, lines):
    return any([is_char(j, s) for j in [i - 1, i, i + 1] for s in lines])

def is_char(i: int, s: str):
    return s is not None and 0 <= i < len(s) and s[i] != '.'

# ------ 2 ------
def find_gears(prev_line, current_line, next_line):
    summa = 0
    for i in range(len(current_line)):
        if current_line[i] == '*':
            numbers = get_adj_numbers_to_position(i, [prev_line, current_line, next_line])
            if len(numbers) == 2:
                summa += numbers[0] * numbers[1]
    return summa

def get_adj_numbers_to_position(i: int, lines):
    if not lines[0] or not lines[1]:
        return []
    res = []
    # # It's not the time for binary search, ok
    for line in lines:
        for n, start, end in collect_line_numbers(line):
            if i in range(start - 1, end + 2):
                res.append(n)
    return res


def solution(f, fun):
    summa, current_line, next_line = 0, None, None
    for line in f:
        prev_line, current_line, next_line = current_line, next_line, line.strip()
        if current_line:
            summa += fun(prev_line, current_line, next_line)
    # Process last line
    summa += fun(current_line, next_line, None)
    print(summa)


with open("3.input") as f:
    # solution(f, collect_adj_numbers)
    solution(f, find_gears)
