ROCK = "O"
def tilt(matrix: list[list[str]]) -> list[list[str]]:
    for c in range(len(matrix[0])):
        max_north_row = find_max_available_north_position(matrix, c, 0)
        r = max_north_row
        while r < len(matrix):
            if max_north_row < 0:
                break
            if matrix[r][c] == "#":
                max_north_row = find_max_available_north_position(matrix, c, r+1)
                r = max_north_row
            elif matrix[r][c] == ROCK:
                matrix[r][c], matrix[max_north_row][c] = ".", ROCK
                max_north_row = find_max_available_north_position(matrix, c, max_north_row+1)
                r = max_north_row
            r += 1

    return matrix

def find_max_available_north_position(matrix, c, from_row):
    for r in range(from_row, len(matrix)):
        if matrix[r][c] == ".":
            return r
    return -1

def rotate_clockwise(a_matrix: list[list[str]]):
    list_of_tuples = zip(*a_matrix[::-1])
    return [list(elem) for elem in list_of_tuples]      # Avoid list of immutable tuples

def calc_load(a_matrix: list[list[str]]) -> int:
    total = 0
    for i, a_row in enumerate(a_matrix):
        total += (len(a_matrix) - i) * sum([1 if c == ROCK else 0 for c in a_row])
    return total

def hash_matrix(a_matrix: list[list[str]]) -> int:
    return hash("".join(["".join(row) for row in a_matrix]))

# with open("test14.txt") as f:
# with open("test14.1.txt") as f:
with open("14.input") as f:
    matrix = [list(line.strip()) for line in f]
    iter_hashes = {}
    fast_forwarded = False
    iterations, i = 1_000_000_000, 1
    while i < iterations + 1:
        # Check if we already saw this configuration, and if yes, use that knowledge to fast-forward
        h = hash_matrix(matrix)
        if h in iter_hashes:
            prev_i = iter_hashes[h]
            if not fast_forwarded:
                cycle = i - prev_i
                skip_cycles = round((iterations - prev_i - cycle) // cycle)
                i = prev_i + skip_cycles * cycle
                fast_forwarded = True
                continue
        elif not fast_forwarded:
            iter_hashes[hash_matrix(matrix)] = i
        matrix = tilt(matrix)
        matrix = tilt(rotate_clockwise(matrix))
        matrix = tilt(rotate_clockwise(matrix))
        matrix = tilt(rotate_clockwise(matrix))
        matrix = rotate_clockwise(matrix)
        i += 1
    print(calc_load(matrix))
