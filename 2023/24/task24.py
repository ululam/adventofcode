import z3 as z3
import numpy as np

def read_input(f):
    stones = []
    for line in f:
        left_right = line.strip().split(" @ ")
        init_pos = [int(v) for v in left_right[0].split(", ")]
        velocity = [int(v) for v in left_right[1].split(", ")]
        stones.append((init_pos, velocity))
    return stones

def solve(stones, area):
    collision_within_area_counter = 0
    for i in range(len(stones) - 1):
        for j in range(i+1, len(stones)):
            x, y = find_collision(stones[i], stones[j])
            # print(f"{stones[i]} x {stones[j]} => ({x}, {y})")
            if x and is_within(x, y, area):
                collision_within_area_counter += 1
    return collision_within_area_counter

def solve2(stones):
    # I failed, used solution from Reddit
    # https://www.reddit.com/r/adventofcode/comments/18pnycy/comment/kev3buh/?utm_source=reddit&utm_medium=web2x&context=3
    (X1, Y1, Z1), (Vx1, Vy1, Vz1) = stones[0]
    (X2, Y2, Z2), (Vx2, Vy2, Vz2) = stones[1]
    (X3, Y3, Z3), (Vx3, Vy3, Vz3) = stones[2]
    # Now, we know that 0-hailstone intersects all them.
    # Let's write it in X0, Y0, Z0, vx, vy, zy
    t1, t2, t3, X0, Y0, Z0, vx, vy, vz = z3.Reals("t1 t2 t3 X0 Y0 Z0 vx vy vz")
    equations = [
        X0 + t1 * vx == X1 + t1 * Vx1,
        Y0 + t1 * vy == Y1 + t1 * Vy1,
        Z0 + t1 * vz == Z1 + t1 * Vz1,

        X0 + t2 * vx == X2 + t2 * Vx2,
        Y0 + t2 * vy == Y2 + t2 * Vy2,
        Z0 + t2 * vz == Z2 + t2 * Vz2,

        X0 + t3 * vx == X3 + t3 * Vx3,
        Y0 + t3 * vy == Y3 + t3 * Vy3,
        Z0 + t3 * vz == Z3 + t3 * Vz3
    ]

    solver = z3.Solver()
    solver.add(*equations)
    solver.check()
    r = solver.model()
    initial_pos = [r[x].as_long() for x in [X0, Y0, Z0]]
    return sum(initial_pos)

def find_collision(s1, s2):
    x1, y1, z1 = s1[0]
    Vx1, Vy1, Vz1 = s1[1]
    x2, y2, z2 = s2[0]
    Vx2, Vy2, Vz2 = s2[1]

    A1 = Vy1/Vx1
    A2 = Vy2/Vx2

    if A1 == A2:
        return None, None
    x = (A1 * x1 - A2 * x2 - y1 + y2) / (A1 - A2)
    y = (A1 * A2 * x1 - A1 * A2 * x2 + A1 * y2 - A2 * y1) / (A1 - A2)

    if _is_in_past(x, x1, Vx1) or _is_in_past(x, x2, Vx2) \
            or _is_in_past(y, y1, Vy1) or _is_in_past(y, y2, Vy2):
        return None, None

    return x, y

def _is_in_past(c, c0, v):
    return (v > 0 and c < c0) or (v < 0 and c > c0)

def is_within(x, y, area):
    delta = 0.1
    x_area, y_area = area
    if abs(x_area[0] - x) < delta or abs(x_area[1] - x) < delta \
            or abs(y_area[0] - y) < delta or abs(y_area[1] - y) < delta:
        print(f"Close: {x}, {y}")
    # todo Handle rounding error
    return x_area[0] <= x <= x_area[1] and y_area[0] <= y <= y_area[1]

# with open("test24.txt") as f:
with open("24.input") as f:
    stones = read_input(f)
    # area = ([7, 27], [7, 27])
    area = ([200000000000000, 400000000000000], [200000000000000, 400000000000000])
    answer = solve(stones, area)
    print(answer)

    answer2 = solve2(stones)
    print(answer2)