# Read line by triples
# Walk current line charwise. If faced a digit, make number: read until next char is not digit
# Check the number is adj: if any of its chars is adj: left, right, bottom, up, lup, rup, ldown, rdown
# For that, keep number -> list of it's char positions.
# If any of nubmer's char adj -> add number to res
# Continue with char next to the number's last char.
# Walk until the EoL

def collect_adj_numbers(prev_line, current_line, next_line):
    poses, digits = [], []
    summa = 0
    for i in range(len(current_line)):
        if current_line[i].isdigit():
            # Check for negative number
            # if not digits and i > 0 and current_line[i-1] == '-':
            #     poses.append(i-1)
            #     digits.append("-")
            digits.append(current_line[i])
            poses.append(i)
        else:
            summa += check_number(digits, poses, prev_line, current_line, next_line)
            digits, poses = [], []
    # Don't forget to check last number in the line
    return summa + check_number(digits, poses, prev_line, current_line, next_line)

def check_number(digits, poses, prev_line, current_line, next_line):
    if digits:
        if any([has_adj_chars(i, [prev_line, next_line]) for i in poses]) \
                or is_char(poses[0] - 1, current_line) \
                or is_char(poses[-1] + 1, current_line):
            return int(''.join(digits))
    return 0

def has_adj_chars(i: int, lines):
    return any([is_char(j, s) for j in [i - 1, i, i + 1] for s in lines])

def is_char(i: int, s: str):
    return s is not None and 0 <= i < len(s) and s[i] != '.'
        # and (not s[i] == "-" or (i >= len(s) or not s[i+1].isdigit()))

def solution(f, fun):
    summa, current_line, next_line = 0, None, None
    for line in f:
        prev_line, current_line, next_line = current_line, next_line, line.strip()
        if current_line:
            summa += fun(prev_line, current_line, next_line)
    # Process last line
    summa += collect_adj_numbers(current_line, next_line, None)
    print(summa)


# with open("test3.txt") as f:
with open("3.input") as f:
    solution(f, collect_adj_numbers)
