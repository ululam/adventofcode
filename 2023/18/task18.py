import sys
from collections import deque

sys.setrecursionlimit(10_000)

UP, DOWN, LEFT, RIGHT = (-1, 0, "U"), (1, 0, "D"), (0, -1, "L"), (0, 1, "R")
ALL = [UP, DOWN, LEFT, RIGHT]
DIR_MAP = {t[2]: (t[0], t[1]) for t in ALL}
DIGGED = "#"
# FILL = "0"

def dig(input: list[list[str]]):
    field, r, c = get_field(input)
    perimenter_len = 0
    field[r][c] = DIGGED

    visited_points, loop_points = set(), set()

    for direct, count, color in input:
        dr, dc = DIR_MAP.get(direct)
        for _ in range(int(count)):
            r, c = r + dr, c + dc
            field[r][c] = DIGGED
            if (r,c) in visited_points:
                loop_points.add((r, c))
            else:
                visited_points.add((r,c))
        perimenter_len += int(count)

    print(f"Loop points: {len(loop_points)}")

    start_from = find_internal_point(field)
    print(f"Starting filling at {start_from}")
    for row in field:
        print(" ".join(row))

    print()
    print()

    return fill_and_count_square(field, start_from) + perimenter_len

def fill_and_count_square(field, start=(1, 1)):
    square = 0
    queue = deque([start])
    while queue:
        r, c = queue.popleft()
        for dr, dc, _ in ALL:
            if can_move_to(field, r + dr, c + dc):
                field[r + dr][c + dc] = DIGGED
                square += 1
                queue.append((r + dr, c + dc))

    # for row in field[:100]:
    #     print(" ".join(row))

    return square

def can_move_to(field, r, c):
    return 0 <= r < len(field) and 0 <= c < len(field[0]) and field[r][c] != DIGGED

def find_internal_point(field):
    r, potential_c = len(field), -1
    while r > 0:
        r >>= 1
        row = field[r]
        borders = 0
        for i in range(len(row) - 1):
            if row[i] == DIGGED and row[i+1] != DIGGED:
                if borders % 2 == 1:
                    return (r, potential_c)
                borders += 1
                potential_c = i + 1
    return None

def get_field(input):
    r, c = 0, 0
    max_row, max_col = -1, -1
    min_row, min_col = 0, 0
    for direct, count, color in input:
        dr, dc = DIR_MAP.get(direct)
        for _ in range(int(count)):
            r, c = r + dr, c + dc
        max_row = max(max_row, r)
        min_row = min(min_row, r)
        max_col = max(max_col, c)
        min_col = min(min_col, c)

    field = []
    for r in range(max_row - min_row + 1):
        field.append(['.' for c in range(max_col - min_col + 1)])
    return field, abs(min_row), abs(min_col)

# with open("test18.txt") as f:
with open("18.input") as f:
    v = dig([line.strip().split() for line in f])
    print(v)

