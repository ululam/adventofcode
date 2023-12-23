import sys
from collections import defaultdict

sys.setrecursionlimit(100_000)

UP, DOWN, LEFT, RIGHT = (-1, 0), (1, 0), (0, -1), (0, 1)
ALL = [UP, LEFT, DOWN, RIGHT]
VISITED = "*"
WALL = "█"

def are_in_bounds(matrix, r, c):
    return 0 <= r < len(matrix) and 0 <= c < len(matrix[0])

def can_move(matrix, r, c, move, check_arrows=False):
    if not are_in_bounds(matrix, r + move[0], c + move[1]):
        return False
    if matrix[r + move[0]][c + move[1]] == WALL: return False
    if matrix[r + move[0]][c + move[1]] == VISITED: return False
    if check_arrows:
        if matrix[r][c] == ">": return  move == RIGHT
        if matrix[r][c] == "v": return move == DOWN
        if matrix[r][c] == "<": return move == LEFT
        if matrix[r][c] == "^": return move == UP
    return True


def find_longest_hike(field):
    res = [0]

    def walk(r, c, steps):
        if r == len(field) - 1 and c == len(field[0]) - 2:
            if steps > res[0]:
                print(f"Found new max = {steps}")
                res[0] = steps
            return
        for dr, dc in ALL:
            if can_move(field, r, c, (dr, dc), True):
                current_char = field[r][c]
                field[r][c] = VISITED
                walk(r + dr, c + dc, steps + 1)
                field[r][c] = current_char

    walk(0, 1, 0)

    return res[0]

def build_graph(field):
    vertices = {}

    def walk_to_the_next_vertex(r, c, from_r, from_c, distance):
        possible_steps = 0
        move = None
        for dr, dc in ALL:
            if r + dr == from_r and c + dc == from_c:
                continue
            if can_move(field, r, c, (dr, dc)):
                possible_steps += 1
                move = (dr, dc)
        if possible_steps == 1:
            return walk_to_the_next_vertex(r + move[0], c + move[1], r, c, distance + 1)
        return (r, c), distance

    def find_distances_to_closest_vertices(r, c):
        if not (r, c) in vertices:
            vertices[r, c] = {}
        moves = [(dr, dc) for dr, dc in ALL if can_move(field, r, c, (dr, dc))]
        for dr, dc in moves:
            vertex, distance = walk_to_the_next_vertex(r + dr, c + dc, r, c, 1)
            # A -> B
            vertices[r, c][vertex] = distance
            if vertex in vertices:
                # We already were there, break the cycle
                vertices[vertex][r, c] = distance
            else:
                vertices[vertex] = {(r, c): distance}
                find_distances_to_closest_vertices(*vertex)

    find_distances_to_closest_vertices(0, 1)

    return vertices

def find_longest_distance_in_graph(g):
    max_distance = [0]
    current_path = set()

    # Graph is too small, and I'm too lazy.
    # Brute force still finds longest path in 10 secs (of course Dijkstra would be 100 times faster)
    def walk_graph(r,c, distance):
        if r == len(input) - 1 and c == len(input[0]) - 2:
            if max_distance[0] < distance:
                max_distance[0] = distance
                return
        if (r, c) not in g:
            return
        for vertex, dist in g[r, c].items():
            if (vertex[0], vertex[1]) in current_path:
                continue
            current_path.add((vertex[0], vertex[1]))
            walk_graph(vertex[0], vertex[1], distance + dist)
            current_path.remove((vertex[0], vertex[1]))

    walk_graph(0,1,0)
    return max_distance[0]

# with open("test23.txt") as f:
with open("23.input") as f:
    input = [list(l.strip()) for l in f]
    # p = find_longest_hike(input)
    g = build_graph(input)

    print(find_longest_distance_in_graph(g))
