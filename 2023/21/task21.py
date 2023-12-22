from collections import defaultdict

UP, DOWN, LEFT, RIGHT = (-1, 0), (1, 0), (0, -1), (0, 1)
ALL = [UP, DOWN, LEFT, RIGHT]

def are_in_bounds(matrix, r, c):
    return 0 <= r < len(matrix) and 0 <= c < len(matrix[0])

def _hash(matrix):
    return hash("".join(["".join(row) for row in matrix]))

def reset_state(matrix):
    for row in matrix:
        for c in range(len(matrix[0])):
            if row[c] != "#":
                row[c] = "."


def count_stars(matrix):
    cnt = 0
    for row in matrix:
        for c in row:
            if c == "*":
                cnt += 1
    return cnt

# with open("test21.txt") as f:
with open("21.input") as f:
    input_ro = []
    row, s_row, s_col = 0,0,0
    for line in f:
        if "S" in line:
            s_row, s_col = row, line.index("S")
        input_ro.append(list(line.strip()))
        row += 1

    matrices = defaultdict(lambda: [r[:] for r in input_ro])
    rows_num, cols_num = len(input_ro), len(input_ro[0])
    get_metrix_index = lambda ar, ac: (ar // rows_num, ac // cols_num)

    cells = [(s_row, s_col)]
    matrices_repeated_iself = set()
    seen_states = set()
    for i in range(26501365):
        if i % 1_00 == 0:
            print(f"At step {i}")
        next_cells = set()
        for m in matrices.values():
            reset_state(m)
        for r, c in cells:
            for move in ALL:
                r_adj, c_adj = r + move[0], c + move[1]
                m_row, m_col = get_metrix_index(r_adj, c_adj)
                matrix = matrices[m_row, m_col]
                r_adj_in_matrix, c_adj_in_matrix = rows_num * m_row - r_adj, cols_num * m_col - c_adj
                # print(f"Coordinates: {r_adj, c_adj}. Matrix {m_row, m_col}. In-matrix coordinates: {r_adj_in_matrix, c_adj_in_matrix}, Input size: {rows_num, cols_num}")
                cell_value = matrix[r_adj_in_matrix][c_adj_in_matrix]
                if cell_value != "#":
                    next_cells.add((r_adj, c_adj))
                    matrix[r_adj_in_matrix][c_adj_in_matrix] = "*"

        cells = list(next_cells)

        for m_coord, m in matrices.items():
            if m_coord in matrices_repeated_iself:
                continue
            h = f"{m_coord}_{_hash(m)}"
            if h in seen_states:
                print(f"Same state at iteration {i} for {m_coord} with count {count_stars(m)}. Total matrices: {len(matrices)}")
                matrices_repeated_iself.add(m_coord)
                # for row in input:
                #     print("".join(row))
                # print("------------------------------------------------------------------")
            else:
                seen_states.add(h)
    print(len(cells))
