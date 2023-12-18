UP, DOWN, LEFT, RIGHT = (-1, 0, "U"), (1, 0, "D"), (0, -1, "L"), (0, 1, "R")
ALL = [UP, DOWN, LEFT, RIGHT]
DIR_MAP = {t[2]: (t[0], t[1]) for t in ALL}

def dig(input: list[list[str]]):
    perimenter_len, area = 0, 0
    r, c = 0, 0
    for instruction in input:
        direct, count = get_line_instruction(instruction)
    # for direct, count, color in input:
    #     count = int(count)
        dr, dc = DIR_MAP.get(direct)
        r_next, c_next = r + dr * count, c + dc * count
        area += (r + r_next ) * (c - c_next)
        r, c = r_next, c_next
        perimenter_len += count

    # Pick's theorem on top of Gauss area formula
    return ((area + perimenter_len) >> 1) + 1


def get_line_instruction(s):
    s = s[2].replace("(", "").replace(")", "").replace("#", "")
    steps = int(s[:5], 16)
    direct = list("RDLU")[int(s[-1])]
    return direct, steps

# with open("test18.txt") as f:
with open("18.input") as f:
    v = dig([line.strip().split() for line in f])
    print(v)

