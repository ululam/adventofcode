def read_matrices(f):
    matrices = [[]]
    for line in f:
        if not line.strip():
            matrices.append([])
            continue
        matrices[-1].append(line.strip())
    return matrices

def get_value(matrix: list[str]) -> int:
    cols = [[row[c] for row in matrix] for c in range(len(matrix[0]))]
    return 100 * find_mirror(matrix) + find_mirror(cols)

def diff(s1, s2):
    return sum([1 if s1[i] != s2[i] else 0 for i in range(len(s1))])

def find_mirror(array: list) -> (int, int):
    for pivot in range(len(array)-1):
        step = 0
        errors = 0
        while pivot + step + 1 < len(array) and pivot - step >= 0:
            # if not are_same(array[pivot - step], array[pivot + step + 1]):
            errors += diff(array[pivot - step], array[pivot + step + 1])
            step += 1
        # if errors == 0:
        if errors == 1:
            return pivot + 1
    return 0

def solve(f):
    total = 0
    for matrix in read_matrices(f):
        total += get_value(matrix)
    print(f"Answer is: {total}")

# with open("test13.txt") as f:
with open("13.input") as f:
    solve(f)
# 41600 + 259