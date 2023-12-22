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

def solve_eq_system():
    from sympy import symbols, Eq, solve

    a, b, c, t = symbols('a b c t')

    # Given equation
    L = a * t ** 2 + b * t + c
    given_L = 3799
    given_t = 65
    given_L_2 = 34047
    given_t_2 = 196
    given_L_3 = 94475
    given_t_3 = 327

    equation = Eq(L.subs(t, given_t), given_L)
    equation_2 = Eq(L.subs(t, given_t_2), given_L_2)
    equation_3 = Eq(L.subs(t, given_t_3), given_L_3)

    solution = solve((equation, equation_2, equation_3), (a, b, c))

    new_t = 26501365

    new_L = L.subs([(a, solution[a]), (b, solution[b]), (c, solution[c]), (t, new_t)])

    new_L_value = new_L.evalf()  # Evaluate to a numerical value
    print(new_L_value)

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
    '''
        Ax2 + Bx + C = L
        ----------------
        4225*A + 65*B + C = 3799
        196*196*A + 196*B + C = 34047
        327*327*A + 327*B + C = 94475
        ----------------

        I lazily use ChatGPT to
    '''
    for i in range(1, 65):       # 3799
    # for i in range(1, 65+131):     # 34047
    # for i in range(1, 65 + 2 * 131):  # 94475
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
                matrices_repeated_iself.add(m_coord)
                print(f"Same state at iteration {i} for {m_coord} with count {count_stars(m)}")
                print(f"\tTotal still matrices {len(matrices_repeated_iself)}, total matrices: {len(matrices)}, live: {len(matrices) - len(matrices_repeated_iself)}")
                # for row in input:
                #     print("".join(row))
                # print("------------------------------------------------------------------")
            else:
                seen_states.add(h)
    print(len(cells))

    solve_eq_system()

