from collections import deque
import sys

sys.setrecursionlimit(20_000)


UP, DOWN, LEFT, RIGHT = (-1, 0, "up"), (1, 0, "down"), (0, -1, "left"), (0, 1, "right")
ALL = [UP, DOWN, LEFT, RIGHT]

def find_path(matrix):
    visited = {}
    min_heat = [float("inf")]

    def bfs(r, c, path, heat):
        if heat > 37148:
            return
        key = f"{r}_{c}"
        # if came_with_limitation(path):         # We need to distinguish when next direction limitation apply
        #     limit_dir = path[-1]
        #     key += f"_{limit_dir}"
        if key in visited and visited.get(key) < heat:
            # print(f"Stopping as already seen less heat [{r}, {c}]")
            return
        if r == len(matrix) - 1 and c == len(matrix[0]) - 1:
            if heat < min_heat[0]:
                min_heat[0] = min(min_heat[0], heat)
                if min_heat[0] < 107600:
                    print(F"Min heat now = {min_heat[0]}")
            return
        visited[key] = heat

        options = []
        for next_dir in get_next_dirs(path):
            # Find greedy next step
            next_r, next_c = r + next_dir[0], c + next_dir[1]
            if are_in_bounds(matrix, next_r, next_c):
                options.append((next_r, next_c, next_dir))
        for next_r, next_c, next_dir in sorted(options, key=lambda v: matrix[v[0]][v[1]]):
            path.append(next_dir)
            heat += int(matrix[next_r][next_c])
            bfs(next_r, next_c, path, heat)
            heat -= int(matrix[next_r][next_c])
            path.pop()

    bfs(0, 0, deque(), 0)
    for r in range(len(matrix)):
        row = []
        for c in range(len(matrix[0])):
            row.append(str(visited.get(f"{r}_{c}", "inf")))
        print(" ".join(row))
    return min_heat[0]

def get_next_dirs(path):
    if not path:
        return ALL  # first cell
    last_dir = path[-1]
    options = filter(lambda v: v != counter_dir(last_dir), ALL)
    if came_with_limitation(path):
        return filter(lambda v: v != last_dir, options)
    return options

def came_with_limitation(path):
    return len(path) >= 3 and path[-3] == path[-2] == path[-1]

def counter_dir(dir):
    if dir == UP: return DOWN
    if dir == DOWN: return UP
    if dir == LEFT: return RIGHT
    if dir == RIGHT: return LEFT

def are_in_bounds(matrix, r, c):
    return 0 <= r < len(matrix) and 0 <= c < len(matrix[0])

# with open("test17.txt") as f:
with open("17.input") as f:
    answer = find_path([list(line.strip()) for line in f])
    print(answer)

