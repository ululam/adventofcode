class Solution:
    def __init__(self) -> None:
        self.expanded_rows, self.expanded_cols = None, None

    def expand(self, matrix):
        # Find rows and columns to expand
        self.expanded_rows = set([r for r in range(len(matrix)) if self.dots_only(matrix[r])])
        self.expanded_cols = set([c for c in range(len(matrix[0])) if self.dots_only([row[c] for row in matrix])])

    def dots_only(self, lst):
        return not any([c for c in lst if c != '.'])

    def assign_galaxy_numbers(self, matrix):
        cnt = 1
        for row in matrix:
            for i in range(len(row)):
                if row[i] == '#':
                    row[i] = str(cnt)
                    cnt += 1
        return cnt

    def solve(self, matrix):
        self.expand(matrix)
        max_galaxy_number = self.assign_galaxy_numbers(matrix)
        print(self.sum_distances(matrix, max_galaxy_number))

    def sum_distances(self, matrix, max_galaxy_number):
        return sum([self.min_distance(matrix, i, j) for i in range(1, max_galaxy_number) for j in range(i + 1, max_galaxy_number)])

    def min_distance(self, matrix, i, j):
        # We could save galaxies coordinates to avoid another search here
        ir, ic = self.find_galaxy_coords(matrix, i)
        jr, jc = self.find_galaxy_coords(matrix, j)
        dist = abs(ir - jr) + abs(ic - jc)
        # expansion_distance = 1                # Part1
        expansion_distance = 999_999            # Part2
        dist += sum([1 for r in range(min(ir, jr), max(ir, jr)) if r in self.expanded_rows]) * expansion_distance
        dist += sum([1 for c in range(min(ic, jc), max(ic, jc)) if c in self.expanded_cols]) * expansion_distance
        return dist

    def find_galaxy_coords(self, matrix, i):
        for r in range(len(matrix)):
            if str(i) in matrix[r]:
                return r, matrix[r].index(str(i))
        return -1,-1

# with open("test11.txt") as f:
with open("11.input") as f:
    matrix = [list(row.strip()) for row in f]
    s = Solution()
    s.solve(matrix)
