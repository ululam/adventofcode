from collections import deque, defaultdict

UP, DOWN, LEFT, RIGHT = (-1, 0), (1, 0), (0, -1), (0, 1)

state_machine = {
    '/': {
        LEFT: [DOWN],
        RIGHT: [UP],
        UP: [RIGHT],
        DOWN: [LEFT]
    },
    '\\': {
        LEFT: [UP],
        RIGHT: [DOWN],
        UP: [LEFT],
        DOWN: [RIGHT]
    },
    '-': {
        UP: [LEFT, RIGHT],
        DOWN: [LEFT, RIGHT],
    },
    '|': {
        LEFT: [UP, DOWN],
        RIGHT: [UP, DOWN]
    }
}


def travel_light(matrix, start_pos=(0, 0, RIGHT)):
    visited = defaultdict(list)
    queue = deque()
    energized = 0
    r0, c0 = start_pos[0] - start_pos[2][0], start_pos[1] - start_pos[2][1]
    queue.append((r0, c0, start_pos[2]))
    while queue:
        r, c, dir = queue.popleft()
        r, c = r + dir[0], c + dir[1]
        if not are_in_bounds(matrix, r, c):
            continue
        energized += 1 if (r, c) not in visited else 0

        next_dirs = get_next_dirs(matrix[r][c], dir)
        cell_dirs_list = visited[(r, c)]
        for next_d in next_dirs:
            # Only energize if that the first beam in any direction
            if next_d not in cell_dirs_list:
                cell_dirs_list.append(next_d)
                # Start beam
                queue.append((r, c, next_d))
    return energized

def get_next_dirs(char, dir):
    if char not in state_machine or dir not in state_machine[char]:
        return [dir]
    return state_machine[char][dir]

def are_in_bounds(matrix, r, c):
    return 0 <= r < len(matrix) and 0 <= c < len(matrix[0])

# with open("test16.txt") as f:
with open("16.input") as f:
    input = [list(line.strip()) for line in f]
    max_tuple = (-1, -1, -1)
    options = []

    for c in range(len(input[0])):
        options.append((0, c, DOWN))
        options.append((len(input) - 1, c, UP))

    for r in range(len(input)):
        options.append((r, 0, RIGHT))
        options.append((r, len(input[0]) - 1, LEFT))

    for start_pos in options:
        v = travel_light(input, start_pos)
        if v > max_tuple[2]:
            max_tuple = (start_pos[0], start_pos[1], v)
    print(max_tuple)
