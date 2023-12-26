from collections import defaultdict


def fall(bricks):
    building = defaultdict(int)  # (x,y) -> min z
    for i in range(len(bricks)):
        b = bricks[i]
        # for each brick, find max z for its low leveled z-plane
        b = _apply_gravity(b, building)
        bricks[i] = b
        _put_brick_into_building(b, building)
    return bricks

def _put_brick_into_building(brick, building):
    for x in range(brick[0], brick[3] + 1):
        for y in range(brick[1], brick[4] + 1):
            building[x, y] = brick[5]

def _apply_gravity(b, building):
    max_z = 0
    for x in range(b[0], b[3] + 1):
        for y in range(b[1], b[4] + 1):
            max_z = max(max_z, building[x, y])
    return b[0], b[1], max_z + 1, b[3], b[4], b[5] - b[2] + max_z + 1

def _has_brick_moved(b1, b2):
    return b1[2] != b2[2]

def solve(bricks):
    count, count_moved = 0, 0
    new_building = defaultdict(int)
    # For each brick, skip it, and check if next bricks Zs are different, until upper bricks
    for i in range(len(bricks) - 1):
        moved = False
        current_it_building = new_building.copy()
        for j in range(i+1, len(bricks)):
            b2 = _apply_gravity(bricks[j], current_it_building)
            if _has_brick_moved(bricks[j], b2):      # To optimize, stop when covered (x,y) square of the current brick
                count_moved += 1
                moved = True
            _put_brick_into_building(b2, current_it_building)
        if not moved:
            count += 1
        _put_brick_into_building(bricks[i], new_building)

    # We can always move last brick
    return count + 1, count_moved

def read_input(f):
    res = []
    for line in f:
        left_right = line.strip().split("~")
        x1, y1, z1 = (int(c) for c in left_right[0].split(","))
        x2, y2, z2 = (int(c) for c in left_right[1].split(","))
        res.append((x1, y1, z1, x2, y2, z2))

    return sorted(res, key=lambda v: (v[2], v[5]))

# with open("test22.txt") as f:
with open("22.input") as f:
    answer, answer2 = solve(fall(read_input(f)))
    print(answer, answer2)
