import sys
sys.setrecursionlimit(10_000)

BORDER = '#'
VISITED_BORDER = ','
INNER = '■'
FAILED_INNER = 'Ø'
OTHER = ' '

# char => delta r, delta c
UP, DOWN, RIGHT, LEFT = (-1, 0), (1, 0), (0, 1), (0, -1)

DIRS = [UP, DOWN, RIGHT, LEFT]

moves = {
    "|": [DOWN, UP],
    "-": [RIGHT, LEFT],
    "L": [UP, RIGHT],
    "J": [UP, LEFT],
    "7": [DOWN, LEFT],
    "F": [DOWN, RIGHT]
}

LEFT_SIDES = {
    UP: LEFT,
    DOWN: RIGHT,
    LEFT: DOWN,
    RIGHT: UP
}

def print_matrix(matrix):
    cnt = 0
    for row in matrix:
        print(f"{cnt}\t" + "".join(row).replace("L", "└").replace("J", "┘").replace("7", "┐").replace("F", "┌").replace("-", "─").replace("|", "│"))
        cnt += 1

def merge(matrix, original_matrix):
    for r in range(len(matrix)):
        for c in range(len(matrix[0])):
            if matrix[r][c] == BORDER:
                matrix[r][c] = original_matrix[r][c]
                if matrix[r][c] == "S":
                    matrix[r][c] = "7"
            elif matrix[r][c] not in [INNER, FAILED_INNER]:
                matrix[r][c] = "."


class Solution:

    def __init__(self) -> None:
        self.found = False
        self.counter = 0
        self.dot_counter = 0
        self.original_matrix = None
        # min_row, min_column, max_row, max_column
        # [0, 5, 137, 136], and matrix is [140, 140]. No much sense to use this optimisation
        # self.corners = [100_000, 100_000, -1, -1]

    def walk(self, matrix, row, col):
        self.original_matrix = [row[:] for row in matrix]
        row, col = self.find_first_move(matrix, row, col)
        self.counter += 1
        while matrix[row][col] != 'S':
            matrix[row][col], (row, col) = BORDER, self.possible_next_cells_from(matrix, row, col)
            self.counter += 1
        matrix[row][col] = BORDER       # Replace S
        print(self.counter >> 1)

    def find_islands(self, matrix):
        perimiter = [(0, i) for i in range(len(matrix[0]))]
        perimiter += [(len(matrix)-1, i) for i in range(len(matrix[0]))]
        perimiter += [(i, 0) for i in range(len(matrix))]
        perimiter += [(i, len(matrix[0])-1) for i in range(len(matrix))]

        def fill(row, col):
            matrix[row][col] = OTHER

            for dr, dc in DIRS:
                if self.part2_can_move_to(matrix, row + dr, col + dc):
                    fill(row + dr, col + dc)

        for row, col in perimiter:
            c = matrix[row][col]
            if c == BORDER or c == OTHER:
                continue
            fill(row, col)

        # Everything left is candidate for inner tile
        for r in range(len(matrix)):
            for c in range(len(matrix[0])):
                if matrix[r][c] not in [BORDER, OTHER]:
                    matrix[r][c] = INNER

        # Eliminate leaking inner tiles
        # Find the first bottom left border. If we go clockwise up, the internal is always to the right
        for r in range(len(matrix)-1, -1, -1):
            if BORDER in matrix[r]:
                start_row, start_col = r, matrix[r].index(BORDER)
                break
        starting_cell = (start_row, start_col)

        # Recover original border path
        merge(matrix, self.original_matrix)

        # Now travel the circle clockwise, marking inner cells
        # Inner cells are always to the right of the walker
        matrix[starting_cell[0]][starting_cell[1]] = VISITED_BORDER     # Step up always exists
        cell = (starting_cell[0]-1, starting_cell[1])
        self.mark_external(matrix, starting_cell, cell)
        while cell != starting_cell:
            next_cell = self.possible_next_cells_from(matrix, *cell)
            if not next_cell:
                break
            self.mark_external(matrix, next_cell, cell)
            matrix[cell[0]][cell[1]] = VISITED_BORDER
            cell = next_cell

        inner_tile_sum = sum([1 if col == INNER else 0 for row in matrix for col in row])

        # Recover to fancy print
        for r in range(len(matrix)):
            for c in range(len(matrix[0])):
                if matrix[r][c] == VISITED_BORDER:
                    matrix[r][c] = self.original_matrix[r][c]
        print_matrix(matrix)
        print(f"Total inner tiles: {inner_tile_sum}")

    def mark_external(self, matrix, next_cell, prev_cell):
        r, c = next_cell
        # We just know that the maze is several cells away from all frontiers.
        # That could be done more correct if checking corner case in each if, but its too much of cognitive complexity
        if r < 2 or r > len(matrix) - 2 or c < 2 or c > len(matrix[0]) - 2:
            return

        move = (r - prev_cell[0], c - prev_cell[1])
        self.unset_if_inner(matrix, r, c, LEFT_SIDES[move])
        if move == UP:
            # U: L-, R+
            if matrix[r][c] == "F":     # up -> right
                self.unset_if_inner(matrix, r, c, LEFT_SIDES[RIGHT])
            if matrix[r][c] == "7":  # up -> left
                self.unset_if_inner(matrix, r, c, LEFT_SIDES[LEFT])
        if move == DOWN:
            # D: R-, L+
            if matrix[r][c] == "J":  # down -> left
                self.unset_if_inner(matrix, r, c, LEFT_SIDES[LEFT])
            if matrix[r][c] == "L":  # up -> right
                self.unset_if_inner(matrix, r, c, LEFT_SIDES[RIGHT])
        if move == LEFT:
            # L: D-, U+
            if matrix[r][c] == "F":  # left -> down
                self.unset_if_inner(matrix, r, c, LEFT_SIDES[DOWN])
            if matrix[r][c] == "L":  # left -> up
                self.unset_if_inner(matrix, r, c, LEFT_SIDES[UP])
        if move == RIGHT:
            # R: U-, D+
            if matrix[r][c] == "7":  # right -> down
                self.unset_if_inner(matrix, r, c, LEFT_SIDES[DOWN])
            if matrix[r][c] == "J":  # right -> up
                self.unset_if_inner(matrix, r, c, LEFT_SIDES[UP])

    def unset_if_inner(self, matrix, row, col, move):
        row, col = row + move[0], col + move[1]
        if matrix[row][col] == INNER:
            matrix[row][col] = FAILED_INNER

    def part2_can_move_to(self, matrix, row, col):
        return 0 <= row < len(matrix) and 0 <= col < len(matrix[0]) \
               and matrix[row][col] != BORDER and matrix[row][col] != OTHER

    def find_first_cell_to_move(self, matrix, row_start, col_start):
        for dr, dc in DIRS:
            if self.can_move_to(matrix, row_start + dr, col_start + dc):
                return row_start + dr, col_start + dc

    def possible_next_cells_from(self, matrix, row, col):
        next_moves = moves[matrix[row][col]]
        for dr, dc in next_moves:
            if self.can_move_to(matrix, row + dr, col + dc):
                return row + dr, col + dc

    def can_move_to(self, matrix, row, col):
        if self.is_in_bounds(matrix, row, col):
            v = matrix[row][col]
            return v in moves.keys() or (v == "S" and self.counter > 2)     # Don't return to S immediately
        return None

    def is_in_bounds(self, matrix, row, col):
        return 0 <= row < len(matrix) and 0 <= col < len(matrix[0])

    def find_first_move(self, matrix, row, col):
        # up
        if self.is_in_bounds(matrix, row-1, col) and matrix[row-1][col] in "|7F":
            return row-1, col
        # down
        if self.is_in_bounds(matrix, row+1, col) and matrix[row+1][col] in "|LJ":
            return row+1, col
        # Else any of left or right works, as we guarantee to have 2 paths
        return row, col-1

    def solve(self, f):
        matrix = [list(l.strip()) for l in f]
        for s_row in range(len(matrix)):
            if "S" in matrix[s_row]:
                s_col = matrix[s_row].index("S")
                break
        print(f"Starting at {s_row}, {s_col} => {matrix[s_row][s_col]}")
        self.walk(matrix, s_row, s_col)
        self.find_islands(matrix)


# with open("test10.txt") as f:
# with open("test10.1.txt") as f:
# with open("test10.2.txt") as f:
# with open("test10.2.1.txt") as f:
# with open("test10.2.2.txt") as f:
with open("10.input") as f:
    Solution().solve(f)

