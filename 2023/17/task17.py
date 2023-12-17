import heapq
from collections import defaultdict

UP, DOWN, LEFT, RIGHT = (-1, 0, "U"), (1, 0, "D"), (0, -1, "L"), (0, 1, "R")
ALL = [UP, DOWN, LEFT, RIGHT]

def find_path_deiksra(matrix):
    def are_in_bounds(r,c):
        return 0 <= r < len(matrix) and 0 <= c < len(matrix[0])
    distances = []
    for r in range(len(matrix)):
        distances.append([defaultdict(lambda: float('inf')) for _ in range(len(matrix[0]))])
    # total heat, coordinates, cell_where_came_from, streak_lem
    # Let's put two first steps.
    queue = [(matrix[1][0], (1, 0), (1, 0), 1), (matrix[0][1], (0, 1), (0, 1), 1)]
    while queue:
        total_heap, (r, c), dir, streak = heapq.heappop(queue)

        for dr, dc, _ in ALL:
            neib_r, neib_c = r + dr, c + dc
            if not are_in_bounds(neib_r, neib_c):
                continue

            # Part 1
            # new_streak = get_next_streak(dir, (dr, dc), streak)
            # if not new_streak or new_streak > 3:
            #     continue  # We cannot move here
            # Part 2
            new_streak = get_next_streak_part_2(dir, (dr, dc), streak)
            if not new_streak or new_streak > 10:
                continue  # We cannot move here

            new_total_heap = total_heap + matrix[neib_r][neib_c]
            existing_total_heap = distances[neib_r][neib_c][dr, dc, new_streak]
            if new_total_heap < existing_total_heap:
                distances[neib_r][neib_c][dr, dc, new_streak] = new_total_heap
                heapq.heappush(queue, (new_total_heap, (neib_r, neib_c), (dr, dc), new_streak))

    return min(distances[len(matrix) - 1][len(matrix[0]) - 1].values())

def get_next_streak(dir, new_dir, streak):
    if dir[0] == -new_dir[0] and dir[1] == -new_dir[1]:
        return None     # We cannot move back
    if dir == new_dir:
        return streak + 1
    return 1

def get_next_streak_part_2(dir, new_dir, streak):
    if dir[0] == -new_dir[0] and dir[1] == -new_dir[1]:
        return None     # We cannot move back
    if dir == new_dir:
        return streak + 1       # Same dir, always ok. Bounds check is outside
    if streak >= 4:
        return 1
    return None

# with open("test17.txt") as f:
with open("17.input") as f:
    input = [list(line.strip()) for line in f]
    for row in input:
        for c in range(len(input[0])):
            row[c] = int(row[c])
    answer = find_path_deiksra(input)
    print(answer)
