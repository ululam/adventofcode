# | is a vertical pipe connecting north and south.
# - is a horizontal pipe connecting east and west.
# L is a 90-degree bend connecting north and east.
# J is a 90-degree bend connecting north and west.
# 7 is a 90-degree bend connecting south and west.
# F is a 90-degree bend connecting south and east.

import sys
sys.setrecursionlimit(100000)

# char => delta r, delta c
UP, DOWN, RIGHT, LEFT = (-1, 0), (1, 0), (0, 1), (0, -1)

moves = {
    "|": [DOWN, UP],
    "-": [RIGHT, LEFT],
    "L": [UP, RIGHT],
    "J": [UP, LEFT],
    "7": [DOWN, LEFT],
    "F": [DOWN, RIGHT]
}


class Solution:

    def __init__(self) -> None:
        self.found = False
        self.counter = 0

    def walk(self, matrix, row, col):
        # row, col = self.find_first_cell_to_move(matrix, row, col)
        col -= 1        # Set it manually, as seen from the data
        self.counter += 1
        while matrix[row][col] != 'S':
            matrix[row][col], (row, col) = "*", self.possible_next_cells_from(matrix, row, col)
            self.counter += 1
        print(self.counter >> 1)

    # In fact, there doesn't even need to be a full tile path to the outside
    # for tiles to count as outside the loop - squeezing between pipes is also allowed!
    def part2(self):
        pass

    def find_first_cell_to_move(self, matrix, row_start, col_start):
        for dr, dc in reversed([RIGHT, LEFT, DOWN, UP]):
            if self.can_move_to(matrix, row_start + dr, col_start + dc):
                return row_start + dr, col_start + dc

    def possible_next_cells_from(self, matrix, row, col):
        next_moves = moves[matrix[row][col]]
        for dr, dc in next_moves:
            if self.can_move_to(matrix, row + dr, col + dc):
                return row + dr, col + dc

    def can_move_to(self, matrix, row, col):
        if 0 <= row < len(matrix) and 0 <= col < len(matrix[0]):
            v = matrix[row][col]
            return v in moves.keys() or (v == "S" and self.counter > 2)     # Don't return to S immediately
        return None

    def solve(self, f):
        matrix = [list(l.strip()) for l in f]
        for s_row in range(len(matrix)):
            if "S" in matrix[s_row]:
                s_col = matrix[s_row].index("S")
                break
        print(f"Starting at {s_row}, {s_col} => {matrix[s_row][s_col]}")
        self.walk(matrix, s_row, s_col)


# with open("test10.txt") as f:
# with open("test10.1.txt") as f:
with open("10.input") as f:
    Solution().solve(f)
