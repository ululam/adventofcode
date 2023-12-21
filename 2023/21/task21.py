UP, DOWN, LEFT, RIGHT = (-1, 0), (1, 0), (0, -1), (0, 1)
ALL = [UP, DOWN, LEFT, RIGHT]

def are_in_bounds(matrix, r, c):
    return 0 <= r < len(matrix) and 0 <= c < len(matrix[0])

# with open("test21.txt") as f:
with open("21.input") as f:
    input = []
    row, s_row, s_col = 0,0,0
    for line in f:
        if "S" in line:
            s_row, s_col = row, line.index("S")
        input.append(list(line.strip()))
        row += 1

    cells = [(s_row, s_col)]
    for i in range(64):
        next_cells = set()
        for r, c in cells:
            for move in ALL:
                r_adj, c_adj = r + move[0], c + move[1]
                if 0 <= r_adj < len(input) and 0 <= c_adj < len(input[0]):
                    if input[r_adj][c_adj] != "#":
                        next_cells.add((r_adj, c_adj))
        cells = list(next_cells)

    print(len(cells))
